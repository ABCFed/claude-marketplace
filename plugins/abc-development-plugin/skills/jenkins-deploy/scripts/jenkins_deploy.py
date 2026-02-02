#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
ABC Jenkins 发布脚本
支持交互式参数输入和自动填充 Git 信息
"""

import argparse
import os
import sys
import time
import xml.etree.ElementTree as ET
import subprocess
import json
import re
import multiprocessing
import platform
import signal
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import requests


# ============================================================================
# 配置常量
# ============================================================================

JENKINS_URL = "http://ci.abczs.cn/"
JENKINS_ENVS = ["abc-his", "abc-bis", "abc-cooperation", "abc-global", "abc-oa", "mira"]
JENKINS_STAGES = ["dev", "test"]

# 获取脚本所在目录（skill 目录）
SCRIPT_DIR = Path(__file__).parent.resolve()
CACHE_DIR = SCRIPT_DIR / "cache"
CACHE_FILE = CACHE_DIR / "jobs.json"
LOG_FILE = CACHE_DIR / "jenkins_monitor.log"  # 监控日志文件

# 全局变量：用于监控取消
_monitor_should_stop = False
_cancel_info = {'auth': None, 'job_path': '', 'job_name': '', 'build_number': None}


# ============================================================================
# 工具函数
# ============================================================================

def print_colored(message: str, color: str = 'white') -> None:
    """打印彩色输出（终端支持时）"""
    colors = {
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'reset': '\033[0m'
    }
    color_code = colors.get(color, '')
    reset_code = colors.get('reset', '')
    print(f"{color_code}{message}{reset_code}")


# ============================================================================
# 配置读取
# ============================================================================

def get_jenkins_auth() -> Tuple[str, str]:
    """
    获取 Jenkins 认证信息
    优先级: 环境变量 > IDEA 插件配置
    """
    # 1. 尝试从环境变量读取
    user = os.getenv('JENKINS_USER')
    token = os.getenv('JENKINS_TOKEN')
    if user and token:
        return user, token

    # 2. 从 IDEA 插件配置读取
    auth_xml_path = find_auth_state_xml()
    if auth_xml_path:
        return parse_auth_xml(auth_xml_path)

    raise Exception(
        "未找到 Jenkins 认证配置。请设置环境变量 JENKINS_USER 和 JENKINS_TOKEN，"
        "或在 IDEA 插件中配置（Settings → ABC Settings → Jenkins 配置）"
    )


def find_auth_state_xml() -> Optional[str]:
    """查找 IDEA 插件的 authState.xml 配置文件"""
    home = Path.home()
    possible_paths = []

    # macOS
    possible_paths.extend([
        home / "Library" / "Application Support" / "JetBrains" / "IntelliJIdea" / "options" / "authState.xml",
        home / "Library" / "Application Support" / "JetBrains" / "IntelliJIdea2025.3" / "options" / "authState.xml",
    ])

    # Linux
    possible_paths.extend([
        home / ".local" / "share" / "JetBrains" / "IntelliJIdea" / "options" / "authState.xml",
    ])

    # Windows
    if os.name == 'nt':
        appdata = os.getenv('APPDATA')
        if appdata:
            possible_paths.extend([
                Path(appdata) / "JetBrains" / "IntelliJIdea" / "options" / "authState.xml",
            ])

    for path in possible_paths:
        if path.exists():
            return str(path)

    return None


def parse_auth_xml(xml_path: str) -> Tuple[str, str]:
    """解析 authState.xml 获取认证信息"""
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()

        # IDEA 的 PersistentStateComponent 格式
        # <option name="jenkinsUserName" value="xxx" />
        # <option name="jenkinsApiToken" value="xxx" />

        user = None
        token = None

        for option in root.findall('.//option'):
            name = option.get('name')
            value = option.get('value')
            if name == 'jenkinsUserName':
                user = value
            elif name == 'jenkinsApiToken':
                token = value

        if user and token:
            return user, token

        raise Exception("authState.xml 中未找到完整的认证信息")

    except Exception as e:
        raise Exception(f"解析 authState.xml 失败: {e}")


# ============================================================================
# Git 信息获取
# ============================================================================

def get_git_info() -> Dict[str, str]:
    """获取当前 Git 仓库信息"""
    try:
        # 获取当前分支
        branch = subprocess.check_output(
            ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
            stderr=subprocess.DEVNULL
        ).decode('utf-8').strip()

        # 获取最新标签
        try:
            tag = subprocess.check_output(
                ['git', 'describe', '--tags', '--abbrev=0'],
                stderr=subprocess.DEVNULL
            ).decode('utf-8').strip()
        except subprocess.CalledProcessError:
            tag = ""

        # 获取 Git 远程仓库 URL（用于过滤项目）
        try:
            remote_url = subprocess.check_output(
                ['git', 'ls-remote', '--get-url', 'origin'],
                stderr=subprocess.DEVNULL
            ).decode('utf-8').strip()
            # 保持原始格式（SSH/HTTP），is_equal_remote 函数会处理路径匹配
        except subprocess.CalledProcessError:
            remote_url = ""

        # 从分支名解析 TAPD ID（标准化流程：feature/xxx-{TAPD_ID}）
        tapd_id = ""
        if branch:
            # 分支名格式：feature/medicine-receipt-chinese-1122044681001112866
            # 提取最后一部分作为 TAPD ID
            parts = branch.split('-')
            if parts:
                last_part = parts[-1]
                # TAPD ID 是纯数字，验证后使用
                if last_part.isdigit():
                    tapd_id = last_part

        return {
            'branch': branch,
            'tag': tag,
            'remote_url': remote_url,
            'tapd_id': tapd_id
        }

    except FileNotFoundError:
        raise Exception("未找到 Git 命令，请确保在 Git 仓库中运行")
    except subprocess.CalledProcessError:
        raise Exception("获取 Git 信息失败，请确保在 Git 仓库中运行")


# ============================================================================
# Jenkins API 调用
# ============================================================================

def get_jenkins_projects(auth: Tuple[str, str], filter_git_url: Optional[str] = None, refresh: bool = False) -> List[Dict]:
    """
    获取 Jenkins 项目列表
    优先从缓存读取，缓存不存在或 refresh=True 时从 API 获取
    """
    # 1. 尝试从缓存读取（除非强制刷新）
    if not refresh:
        cached_projects, cached_at = load_projects_from_cache()
        if cached_projects:
            cached_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(cached_at))
            print(f"✓ 使用缓存数据 (缓存时间: {cached_time})")
            projects = cached_projects
        else:
            print("缓存不存在，正在从 Jenkins 获取...")
            projects = fetch_projects_from_jenkins(auth)
            save_projects_to_cache(projects)
    else:
        print("强制刷新，正在从 Jenkins 获取...")
        projects = fetch_projects_from_jenkins(auth)
        save_projects_to_cache(projects)

    # 2. 根据 Git URL 过滤
    if filter_git_url:
        projects = filter_projects_by_git(projects, filter_git_url)

    return projects


def load_projects_from_cache() -> Optional[Tuple[List[Dict], float]]:
    """从缓存加载项目列表，返回 (项目列表, 缓存时间戳)"""
    if CACHE_FILE.exists():
        try:
            with open(CACHE_FILE, 'r') as f:
                data = json.load(f)
                return data.get('projects', []), data.get('cached_at', 0)
        except Exception:
            pass

    return None, None


def save_projects_to_cache(projects: List[Dict]):
    """保存项目列表到缓存"""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    cache_data = {
        'projects': projects,
        'cached_at': time.time(),
        'cached_at_readable': time.strftime('%Y-%m-%d %H:%M:%S')
    }

    try:
        with open(CACHE_FILE, 'w') as f:
            json.dump(cache_data, f, indent=2, ensure_ascii=False)
        return True
    except Exception:
        return False


def fetch_projects_from_jenkins(auth: Tuple[str, str]) -> List[Dict]:
    """从 Jenkins API 获取项目列表"""
    user, token = auth
    projects = []

    for env in JENKINS_ENVS:
        for stage in JENKINS_STAGES:
            url = f"{JENKINS_URL}job/{env}/job/{stage}/api/json"
            try:
                response = requests.get(url, auth=(user, token), timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    jobs = data.get('jobs', [])

                    for job in jobs:
                        if 'url' not in job:
                            continue

                        job_url = job['url']
                        job_config_url = f"{job_url}api/json?pretty=true"

                        try:
                            job_response = requests.get(job_config_url, auth=(user, token), timeout=10)
                            if job_response.status_code == 200:
                                job_data = parse_job_config(job_response.json())
                                projects.append(job_data)
                        except Exception:
                            continue

            except Exception:
                continue

    return projects


def parse_job_config(job_data: Dict) -> Dict:
    """解析 Jenkins 项目配置"""
    job = {
        'name': job_data.get('name', ''),
        'full_name': job_data.get('fullName', ''),
        'env': job_data.get('fullName', '').split('/')[1] if '/' in job_data.get('fullName', '') else '',
        'git': '',
        'parameters': []
    }

    properties = job_data.get('property', [])
    parameters = []

    for prop in properties:
        if 'parameterDefinitions' in prop:
            for param_def in prop['parameterDefinitions']:
                param = {
                    'name': param_def.get('name', ''),
                    'description': param_def.get('description', ''),
                    'type': param_def.get('type', ''),
                    'default_value': param_def.get('defaultParameterValue', {}).get('value', '')
                }

                if param_def.get('type') == 'ChoiceParameterDefinition':
                    param['choices'] = param_def.get('choices', [])

                # 提取 Git URL
                if param_def.get('name') == 'repoUrl':
                    job['git'] = param_def.get('defaultParameterValue', {}).get('value', '')

                parameters.append(param)

    # 将常用参数放到最后
    key_params = ['repoBranch', 'repoTag', 'featureNo']
    for key in key_params:
        for param in parameters:
            if param['name'] == key:
                parameters.remove(param)
                parameters.append(param)

    job['parameters'] = parameters
    return job


def filter_projects_by_git(projects: List[Dict], git_url: Optional[str]) -> List[Dict]:
    """根据 Git URL 过滤相关项目，如果 git_url 为 None 则返回所有项目"""
    if git_url is None:
        return projects

    filtered = []
    for project in projects:
        project_git = project.get('git', '')
        if project_git and is_equal_remote(git_url, project_git):
            filtered.append(project)
    return filtered


def is_equal_remote(remote: str, local: str) -> bool:
    """
    判断两个 Git remote URL 是否指向同一仓库
    提取关键字后的路径部分进行精确匹配
    """
    if not remote or not local:
        return False

    remote_path = ''
    local_path = ''

    # 查找关键字位置（支持 abcyun 和 abc-clinic）
    keywords = ['abcyun', 'abc-clinic']
    remote_index = -1
    local_index = -1
    matched_keyword = None

    for keyword in keywords:
        idx = remote.find(keyword)
        if idx != -1:
            remote_index = idx
            matched_keyword = keyword
            break

    if matched_keyword:
        local_index = local.find(matched_keyword)

    if remote_index != -1:
        remote_path = remote[remote_index:].strip()
    if local_index != -1:
        local_path = local[local_index:].strip()

    return remote_path == local_path


# ============================================================================
# 参数收集
# ============================================================================

def smart_infer_parameters(project: Dict, git_info: Dict) -> Dict[str, str]:
    """
    智能推断参数值
    返回 {参数名: 推断值} 的字典
    """
    inferred = {}
    branch = git_info.get('branch', '')
    tag = git_info.get('tag', '')
    tapd_id = git_info.get('tapd_id', '')
    project_name = project.get('name', '')
    project_env = project.get('env', '')

    for param in project.get('parameters', []):
        name = param['name']
        param_type = param['type']
        default_value = param.get('default_value', '')
        choices = param.get('choices', [])

        # 1. Git 相关参数自动填充
        if name == 'repoBranch':
            if branch:
                inferred[name] = branch
            elif default_value:
                inferred[name] = default_value
            continue

        if name == 'repoTag':
            if tag:
                inferred[name] = tag
            elif default_value:
                inferred[name] = default_value
            continue

        # 2. TAPD ID 自动填充（PcFeatureTest 项目）
        if name == 'tapdId' or name == 'tapdid':
            if tapd_id:
                inferred[name] = tapd_id
            elif default_value:
                inferred[name] = default_value
            continue

        # 3. 环境参数推断
        if name == 'execType' and param_type == 'ChoiceParameterDefinition':
            # 有 tag 时默认 deploy，否则 build
            if tag and 'deploy' in choices:
                inferred[name] = 'deploy'
            elif 'build' in choices:
                inferred[name] = 'build'
            continue

        # 4. 使用默认值
        if default_value:
            inferred[name] = default_value

        # 5. Choice 类型使用第一个非空选项作为默认值
        if param_type == 'ChoiceParameterDefinition' and choices and name not in inferred:
            # 选择第一个非空选项
            for choice in choices:
                if choice.strip():
                    inferred[name] = choice
                    break

    return inferred


def collect_build_parameters(project: Dict, git_info: Dict, provided_params: Dict = None, non_interactive: bool = False) -> Dict[str, List[str]]:
    """
    收集构建参数
    使用智能推断 + 交互式确认的方式

    Args:
        project: Jenkins 项目配置
        git_info: Git 信息
        provided_params: 用户提供的参数
        non_interactive: 是否跳过交互式确认
    """
    properties = {}
    provided_params = provided_params or {}

    # 1. 智能推断所有参数
    inferred = smart_infer_parameters(project, git_info)

    # 2. 显示推断结果
    print(f"\n项目: {project['name']} ({project['full_name']})")
    print("=" * 60)
    print("智能推断的参数:")

    for param in project.get('parameters', []):
        name = param['name']
        if name in inferred and inferred[name]:
            param_type = param['type']
            # 只显示非只读参数
            if param_type != 'WReadonlyStringParameterDefinition':
                print(f"  ✓ {name}: {inferred[name]}")

    print("=" * 60)

    if non_interactive:
        print("\n使用非交互式模式，自动应用推断/提供的参数\n")
    else:
        print("\n请确认或修改参数 (直接回车使用推断值):\n")

    # 3. 逐个收集参数
    for param in project.get('parameters', []):
        name = param['name']
        param_type = param['type']
        desc = param.get('description', '')
        choices = param.get('choices', [])

        # 优先使用用户提供的参数
        if name in provided_params:
            properties[name] = [provided_params[name]]
            continue

        # 获取推断值
        inferred_value = inferred.get(name, '')

        # 只读参数直接使用，不询问
        if param_type == 'WReadonlyStringParameterDefinition':
            if inferred_value:
                properties[name] = [inferred_value]
            continue

        # 非交互模式：直接使用推断值或默认值
        if non_interactive:
            if inferred_value:
                properties[name] = [inferred_value]
            # Choice 类型如果没有推断值，使用第一个选项
            elif param_type == 'ChoiceParameterDefinition' and choices:
                properties[name] = [choices[0]]
            continue

        # 交互式模式：逐个确认
        # 根据参数类型收集输入
        if param_type == 'StringParameterDefinition':
            value = input_string_with_default(name, inferred_value, desc)
            if value:
                properties[name] = [value]

        elif param_type == 'ChoiceParameterDefinition':
            # 如果推断值在选项中，默认选中
            default_index = 0
            if inferred_value in choices:
                default_index = choices.index(inferred_value)
            value = input_choice_with_default(name, choices, default_index, desc)
            if value:
                properties[name] = [value]

        elif param_type == 'PT_CHECKBOX':
            # 复选框：解析默认值
            default_selected = []
            if inferred_value:
                default_selected = inferred_value.split(',') if inferred_value else []
            value = input_checkbox_with_default(name, choices, default_selected, desc)
            if value:
                properties[name] = value

        elif param_type == 'PT_BOOLEAN' or param_type == 'BooleanParameterDefinition':
            value = input_boolean_with_default(name, inferred_value == 'true', desc)
            if value:
                properties[name] = [value]

        else:
            # 其他类型：使用推断值
            if inferred_value:
                properties[name] = [inferred_value]

    # 4. 最终确认所有参数
    if not non_interactive:
        print("\n" + "=" * 60)
        print("请确认以下构建参数:")
        print("=" * 60)

        for name, values in properties.items():
            value_str = ', '.join(values) if isinstance(values, list) else str(values)
            print(f"  {name}: {value_str}")

        print("=" * 60)

        while True:
            confirm = input("\n确认并触发构建？(y/n): ").strip().lower()
            if confirm in ['y', 'yes', '是']:
                print("✓ 开始触发构建...\n")
                return properties
            elif confirm in ['n', 'no', '否']:
                print("✗ 已取消构建")
                return {}
            else:
                print("请输入 y 或 n")
    else:
        # 非交互模式：显示最终参数并直接返回
        print("\n" + "=" * 60)
        print("即将使用的构建参数:")
        print("=" * 60)

        for name, values in properties.items():
            value_str = ', '.join(values) if isinstance(values, list) else str(values)
            print(f"  {name}: {value_str}")

        print("=" * 60)
        print("\n✓ 开始触发构建...\n")
        return properties


def input_string_with_default(name: str, default: str = '', desc: str = '') -> str:
    """文本输入（带默认值）"""
    prompt = f"  {name}"
    if desc:
        prompt += f" - {desc}"
    if default:
        prompt += f" [默认: {default}]"
    prompt += ": "

    value = input(prompt).strip()
    return value if value else default


def input_string(name: str, default: str = '', desc: str = '') -> str:
    """文本输入（兼容旧接口）"""
    return input_string_with_default(name, default, desc)


def input_choice_with_default(name: str, choices: List[str], default_index: int = 0, desc: str = '') -> str:
    """下拉选择（带默认选中）"""
    print(f"  {name}:")
    if desc:
        print(f"    描述: {desc}")

    for i, choice in enumerate(choices, 1):
        marker = "→" if i - 1 == default_index else " "
        print(f"    {marker} {i}. {choice}")

    while True:
        try:
            prompt = f"    请输入选项 (1-{len(choices)}, 默认: {default_index + 1}): "
            selection = input(prompt).strip()
            if not selection:
                return choices[default_index]

            index = int(selection) - 1
            if 0 <= index < len(choices):
                return choices[index]
            print(f"    请输入 1-{len(choices)} 之间的数字")
        except ValueError:
            print("    请输入有效的数字")


def input_choice(name: str, choices: List[str], desc: str = '') -> str:
    """下拉选择（兼容旧接口）"""
    return input_choice_with_default(name, choices, 0, desc)


def input_checkbox_with_default(name: str, choices: List[str], default_selected: List[str] = None, desc: str = '') -> List[str]:
    """复选框选择（带默认选中）"""
    if default_selected is None:
        default_selected = []

    print(f"  {name}:")
    if desc:
        print(f"    描述: {desc}")

    # 显示选项
    for i, choice in enumerate(choices, 1):
        checked = "✓" if choice in default_selected else " "
        print(f"    [{checked}] {i}. {choice}")

    # 获取输入
    prompt = f"    请输入选项编号，用逗号分隔 (默认: {','.join([str(choices.index(c)+1) for c in default_selected])}): "
    selection = input(prompt).strip()

    if not selection:
        return default_selected

    # 解析选择
    selected = []
    for s in selection.split(','):
        try:
            index = int(s.strip()) - 1
            if 0 <= index < len(choices):
                selected.append(choices[index])
        except ValueError:
            pass

    return selected if selected else default_selected


def input_boolean_with_default(name: str, default: bool = False, desc: str = '') -> str:
    """布尔值输入（带默认值）"""
    prompt = f"  {name}"
    if desc:
        prompt += f" - {desc}"
    prompt += f" [y/n, 默认: {'y' if default else 'n'}]: "

    while True:
        value = input(prompt).strip().lower()
        if not value:
            return 'true' if default else 'false'
        if value in ['y', 'yes', '是', 'true']:
            return 'true'
        elif value in ['n', 'no', '否', 'false']:
            return 'false'
        print("    请输入 y/n")


def input_boolean(name: str, default: bool = False, desc: str = '') -> str:
    """布尔值输入（兼容旧接口）"""
    return input_boolean_with_default(name, default, desc)


# ============================================================================
# 构建 API
# ============================================================================

def trigger_build(auth: Tuple[str, str], project: Dict, properties: Dict) -> Optional[int]:
    """触发 Jenkins 构建，返回队列 ID"""
    user, token = auth

    full_name = project.get('full_name', '')
    # full_name 格式: abc-his/test/PcFeatureDev
    parts = full_name.split('/')
    if len(parts) < 3:
        raise Exception(f"无效的项目全名: {full_name}")

    # 每个 part 前都要加 /job/
    build_url = JENKINS_URL + '/'.join([f'job/{p}' for p in parts]) + '/buildWithParameters'

    # 发送请求
    print(f"\n正在触发构建: {project.get('name')}")
    print(f"构建 URL: {build_url}")

    response = requests.post(build_url, auth=(user, token), data=properties, timeout=30)

    # 尝试从响应头获取队列位置（Jenkins 可能返回 201、302 等状态码）
    queue_id = None
    queue_url = response.headers.get('Location', '')

    if queue_url:
        match = re.search(r'/queue/item/(\d+)', queue_url)
        if match:
            queue_id = int(match.group(1))

    # 如果响应头没有队列 URL，尝试从响应体中解析（某些 Jenkins 版本）
    if not queue_id and response.text:
        # 尝试从响应体中提取队列项 URL
        match = re.search(r'/queue/item/(\d+)', response.text)
        if match:
            queue_id = int(match.group(1))

    if queue_id:
        print(f"构建已加入队列 (Queue ID: {queue_id})")
        return queue_id

    # 提供更详细的错误信息
    print(f"响应状态码: {response.status_code}")
    # 过滤敏感头信息
    safe_headers = {k: v for k, v in response.headers.items()
                    if k.lower() not in ['authorization', 'cookie', 'set-cookie']}
    print(f"响应头: {safe_headers}")
    print(f"响应内容: {response.text[:500] if response.text else '无内容'}")
    raise Exception(f"触发构建失败: 无法获取队列 ID (HTTP {response.status_code})")


def monitor_build(auth: Tuple[str, str], project: Dict, queue_id: int):
    """监控构建状态"""
    user, token = auth
    full_name = project.get('full_name', '')
    parts = full_name.split('/')
    job_path = '/'.join(parts[:-1])
    job_name = parts[-1]

    print("\n开始监控构建状态...")

    # 阶段1: 等待任务出队列
    build_number = wait_for_build_start(auth, queue_id)

    if build_number is None:
        print("构建已取消或失败")
        return

    # 阶段2: 监控构建状态
    build_result = monitor_build_progress(auth, job_path, job_name, build_number)

    # 显示结果
    print(f"\n{'='*60}")
    if build_result == 'SUCCESS':
        print(f"✓ 构建成功!")
    elif build_result == 'FAILURE':
        print(f"✗ 构建失败")
    elif build_result == 'ABORTED':
        print(f"⚠ 构建已取消")
    else:
        print(f"构建状态: {build_result}")

    # 显示构建 URL
    build_url = f"{JENKINS_URL}job/{job_path}/job/{job_name}/{build_number}/"
    print(f"构建 URL: {build_url}")
    print(f"{'='*60}\n")


def signal_handler(signum, frame):
    """处理终止信号，取消 Jenkins 构建"""
    global _monitor_should_stop
    _monitor_should_stop = True

    info = _cancel_info
    if info['auth'] and info['job_path'] and info['job_name'] and info['build_number']:
        try:
            user, token = info['auth']
            # 调用 Jenkins API 停止构建
            stop_url = f"{JENKINS_URL}job/{info['job_path']}/job/{info['job_name']}/{info['build_number']}/stop"
            response = requests.post(stop_url, auth=(user, token), timeout=10)

            if response.status_code == 200 or response.status_code == 302:
                print(f"\n\n⚠️ 已发送停止构建请求: Build #{info['build_number']}")
            else:
                print(f"\n\n⚠️ 停止构建失败: HTTP {response.status_code}")
        except Exception as e:
            print(f"\n\n⚠️ 停止构建时出错: {e}")
    else:
        print("\n\n⚠️ 监控已停止，但构建信息不完整，无法自动取消")


def cancel_jenkins_build(auth: Tuple[str, str], job_path: str, job_name: str, build_number: int) -> bool:
    """取消 Jenkins 构建"""
    try:
        user, token = auth
        stop_url = f"{JENKINS_URL}job/{job_path}/job/{job_name}/{build_number}/stop"
        response = requests.post(stop_url, auth=(user, token), timeout=10)
        return response.status_code in [200, 302]
    except Exception:
        return False


def get_terminal_app():
    """根据环境变量判断当前终端应用"""
    term_program = os.environ.get("TERM_PROGRAM", "")
    if term_program == "vscode":
        return "com.microsoft.VSCode"
    elif term_program == "iTerm.app":
        return "com.googlecode.iterm2"
    elif term_program == "Apple_Terminal":
        return "com.apple.Terminal"
    else:
        # 默认返回 iTerm2
        return "com.googlecode.iterm2"


def is_app_frontmost(bundle_id):
    """检查指定应用是否在前台"""
    try:
        script = f'''
        tell application "System Events"
            set frontApp to bundle identifier of first application process whose frontmost is true
            return frontApp
        end tell
        '''
        result = subprocess.run(
            ["/usr/bin/osascript", "-e", script],
            capture_output=True,
            text=True,
            timeout=2
        )
        return result.stdout.strip() == bundle_id
    except Exception:
        return False


def send_notification(title: str, message: str):
    """发送系统通知（使用 terminal-notifier，参考 notification_handler.py）"""
    try:
        import platform
        system = platform.system()

        if system == 'Darwin':  # macOS
            terminal_app = get_terminal_app()

            # 构建基本参数
            cmd = [
                "/opt/homebrew/bin/terminal-notifier",
                "-title", title,
                "-message", message,
                "-sound", "Glass",
                "-group", "jenkins-build"
            ]

            # 如果目标应用不在前台，添加 -activate 参数
            if not is_app_frontmost(terminal_app):
                cmd.extend(["-activate", terminal_app])

            subprocess.run(cmd, check=False, capture_output=True, timeout=5)
        elif system == 'Linux':
            subprocess.run([
                'notify-send', title, message
            ], check=False, capture_output=True)
    except Exception:
        pass  # 静默失败，不影响主流程


def monitor_build_with_notification(auth: Tuple[str, str], project: Dict, queue_id: int, project_name: str):
    """后台监控构建状态，完成后发送通知"""
    global _monitor_should_stop, _cancel_info
    _monitor_should_stop = False  # 重置停止标志

    # 初始化构建信息文件变量（用于 finally 块中清理）
    build_info_file = None
    stop_marker_file = None

    # 注册信号处理器
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        user, token = auth
        full_name = project.get('full_name', '')
        parts = full_name.split('/')
        # 正确构建 Jenkins URL 路径
        job_url_path = '/job/'.join(parts)

        print(f"📊 开始监控构建: {project_name}", flush=True)
        print(f"   Queue ID: {queue_id}", flush=True)
        print(f"   项目: {full_name}", flush=True)
        print(flush=True)

        # 等待任务出队列（显示进度）
        build_number = wait_for_build_start(auth, queue_id, timeout=300, silent=False)

        if _monitor_should_stop:
            print("\n⚠️ 监控已在队列阶段停止")
            return

        if build_number is None:
            send_notification("Jenkins 构建失败", f"{project_name}: 构建已取消或超时")
            return

        # 读取构建参数（如果存在）
        build_params = {}
        params_file = CACHE_DIR / f"build_params_{queue_id}.json"
        try:
            if params_file.exists():
                with open(params_file, 'r') as f:
                    params_data = json.load(f)
                    build_params = params_data.get('params', {})
        except Exception as e:
            pass  # 参数文件可选，读取失败不影响监控

        # 如果返回 -1，说明队列项已被清理，尝试获取最新构建
        if build_number == -1:
            try:
                url = f"{JENKINS_URL}job/{job_url_path}/api/json?tree=builds[number,result,building,timestamp]"
                response = requests.get(url, auth=(user, token), timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    builds = data.get('builds', [])
                    if builds:
                        latest = builds[0]
                        build_number = latest['number']
                        build_timestamp = latest.get('timestamp', 0)  # 毫秒时间戳

                        # 检查构建是否在最近 3 分钟内开始（认为是我们触发的）
                        current_time = time.time() * 1000  # 转换为毫秒
                        time_diff = (current_time - build_timestamp) / 1000  # 秒

                        if time_diff > 180:  # 超过 3 分钟，可能不是我们触发的
                            send_notification("Jenkins 监控错误", f"{project_name}: 无法找到对应的构建")
                            print(f"❌ 最新构建时间过久（{int(time_diff)}秒前），可能不是当前触发的构建")
                            return

                        # 检查构建状态
                        result = latest.get('result')
                        building = latest.get('building', False)

                        if result and not building:
                            # 构建已完成，直接发送通知
                            build_url = f"{JENKINS_URL}job/{job_url_path}/{build_number}/"
                            if result == 'SUCCESS':
                                send_notification("✓ Jenkins 构建成功", f"{project_name} (Build #{build_number})")
                                print(f"\n✓ {project_name} 构建成功!")
                                print(f"构建 URL: {build_url}")
                            elif result == 'FAILURE':
                                send_notification("✗ Jenkins 构建失败", f"{project_name} (Build #{build_number})")
                                print(f"\n✗ {project_name} 构建失败")
                                print(f"构建 URL: {build_url}")
                            else:
                                send_notification(f"Jenkins 构建: {result}", f"{project_name} (Build #{build_number})")
                                print(f"\n⚠ {project_name} 构建状态: {result}")
                                print(f"构建 URL: {build_url}")
                            return
                        # 构建还在进行中，继续监控
                        print(f"✓ 找到最新构建 #{build_number}（{int(time_diff)}秒前开始）")
            except Exception as e:
                send_notification("Jenkins 监控错误", f"{project_name}: 无法获取构建信息")
                print(f"❌ 获取构建信息失败: {e}")
                return

        # 需要继续监控，计算正确的 job_path 和 job_name
        # job_path 需要用 /job/ 连接（除了最后一个是 job_name）
        if len(parts) > 2:
            job_path = '/job/'.join(parts[:-1])
        else:
            job_path = parts[0]
        job_name = parts[-1]

        # 设置取消信息（用于信号处理）
        _cancel_info = {
            'auth': auth,
            'job_path': job_path,
            'job_name': job_name,
            'build_number': build_number
        }

        # 保存构建信息到文件（用于 --stop 命令）
        build_info_file = CACHE_DIR / f"build_info_{build_number}.json"
        build_info_data = {
            'job_path': job_path,
            'job_name': job_name,
            'build_number': build_number,
            'project_name': project_name,
            'timestamp': time.time()
        }
        try:
            with open(build_info_file, 'w') as f:
                json.dump(build_info_data, f, indent=2)
        except Exception as e:
            print(f"警告: 无法保存构建信息: {e}")

        # 创建停止标记文件
        stop_marker_file = CACHE_DIR / f"stop_build_{build_number}.marker"

        print(f"📦 构建号: #{build_number}", flush=True)
        print(f"⏳ 监控构建进度...", flush=True)
        print(f"   需要取消时，请告诉我: \"取消构建 #{build_number}\"", flush=True)
        print(flush=True)

        # 监控构建状态（显示进度）
        build_result = monitor_build_progress(auth, job_path, job_name, build_number, timeout=3600, silent=False, stop_marker_file=stop_marker_file)

        # 清理停止标记文件
        if stop_marker_file.exists():
            try:
                stop_marker_file.unlink()
            except:
                pass

        # 检查是否被用户停止
        if _monitor_should_stop or build_result == 'STOPPED':
            # 尝试取消 Jenkins 构建
            if cancel_jenkins_build(auth, job_path, job_name, build_number):
                send_notification("Jenkins 构建已停止", f"{project_name} (Build #{build_number})")
                print(f"⚠️ {project_name} 构建已停止", flush=True)
            else:
                print(f"⚠️ 构建停止请求已发送，请手动确认", flush=True)
            print(f"构建 URL: {JENKINS_URL}job/{job_url_path}/{build_number}/", flush=True)
            return

        # 构建完成，发送通知
        build_url = f"{JENKINS_URL}job/{job_url_path}/{build_number}/"

        # 格式化通知消息（包含 featureNo/envNo）
        def format_notification_message(base_msg: str) -> str:
            parts = [base_msg]
            if build_params.get('featureNo'):
                parts.append(f"功能编号: {build_params['featureNo']}")
            if build_params.get('envNo'):
                parts.append(f"环境编号: {build_params['envNo']}")
            return '\n'.join(parts)

        if build_result == 'SUCCESS':
            send_notification(
                "✓ Jenkins 构建成功",
                format_notification_message(f"{project_name} (Build #{build_number})")
            )
            print(f"\n✅ {project_name} 构建成功!", flush=True)
            if build_params.get('featureNo'):
                print(f"   功能编号: {build_params['featureNo']}", flush=True)
            if build_params.get('envNo'):
                print(f"   环境编号: {build_params['envNo']}", flush=True)
            print(f"构建 URL: {build_url}", flush=True)
        elif build_result == 'FAILURE':
            send_notification(
                "✗ Jenkins 构建失败",
                format_notification_message(f"{project_name} (Build #{build_number})")
            )
            print(f"\n❌ {project_name} 构建失败", flush=True)
            if build_params.get('featureNo'):
                print(f"   功能编号: {build_params['featureNo']}", flush=True)
            print(f"构建 URL: {build_url}", flush=True)
        elif build_result == 'ABORTED':
            send_notification(
                "⚠️ Jenkins 构建已中止",
                format_notification_message(f"{project_name} (Build #{build_number})")
            )
            print(f"\n⚠️ {project_name} 构建已中止", flush=True)
            print(f"构建 URL: {build_url}", flush=True)
        else:
            send_notification(
                f"Jenkins 构建: {build_result}",
                format_notification_message(f"{project_name} (Build #{build_number})")
            )
            print(f"\n⚠️ {project_name} 构建状态: {build_result}")
            print(f"构建 URL: {build_url}")

    except KeyboardInterrupt:
        print("\n⚠️ 监控已中断")
    except Exception as e:
        send_notification("Jenkins 监控错误", f"{project_name}: {str(e)}")
        print(f"❌ 监控出错: {e}")
    finally:
        # 清理信号处理器
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        signal.signal(signal.SIGTERM, signal.SIG_DFL)
        # 清理取消信息
        _cancel_info = {'auth': None, 'job_path': '', 'job_name': '', 'build_number': None}

        # 清理构建信息文件
        if build_info_file is not None and build_info_file.exists():
            try:
                build_info_file.unlink()
            except:
                pass

        # 清理停止标记文件
        if stop_marker_file is not None and stop_marker_file.exists():
            try:
                stop_marker_file.unlink()
            except:
                pass

        # 清理构建参数文件
        if 'params_file' in locals() and params_file.exists():
            try:
                params_file.unlink()
            except:
                pass


def wait_for_build_start(auth: Tuple[str, str], queue_id: int, timeout: int = 300, silent: bool = False) -> Optional[int]:
    """等待任务出队列，返回构建编号"""
    user, token = auth
    start_time = time.time()
    first_forty_four_time = None  # 第一次 404 的时间

    while time.time() - start_time < timeout:
        try:
            url = f"{JENKINS_URL}queue/item/{queue_id}/api/json"
            response = requests.get(url, auth=(user, token), timeout=10)

            if response.status_code == 200:
                data = response.json()

                # 检查是否被取消
                if data.get('cancelled', False):
                    if not silent:
                        print("任务已在队列中取消")
                    return None

                # 显示等待原因
                why = data.get('why')
                if why and not silent:
                    print(f"等待中: {why}", flush=True)

                # 检查是否开始执行
                executable = data.get('executable')
                if executable:
                    build_number = executable.get('number')
                    if build_number:
                        if not silent:
                            print(f"任务开始执行 (Build #{build_number})", flush=True)
                        return build_number
            elif response.status_code == 404:
                # 队列项已不存在（构建已开始）
                if first_forty_four_time is None:
                    first_forty_four_time = time.time()
                    if not silent:
                        print("队列项已清理，等待获取构建信息...")
                elif time.time() - first_forty_four_time > 5:
                    # 连续 404 超过 5 秒，认为构建确实已经开始
                    if not silent:
                        print("队列已清理，尝试从项目获取构建信息")
                    return -1  # 返回特殊值，让调用者获取最新构建
            else:
                first_forty_four_time = None  # 重置

        except Exception as e:
            if not silent:
                print(f"查询队列状态失败: {e}")

        time.sleep(2)

    if not silent:
        print("等待任务超时")
    return None


def monitor_build_progress(auth: Tuple[str, str], job_path: str, job_name: str, build_number: int, timeout: int = 3600, silent: bool = False, stop_marker_file: Optional[Path] = None) -> str:
    """监控构建进度，返回最终结果"""
    global _monitor_should_stop
    user, token = auth
    start_time = time.time()
    check_count = 0

    while time.time() - start_time < timeout:
        # 检查是否应该停止（多种方式）
        if _monitor_should_stop:
            return "STOPPED"

        # 检查停止标记文件
        if stop_marker_file and stop_marker_file.exists():
            _monitor_should_stop = True
            # 删除标记文件
            try:
                stop_marker_file.unlink()
            except:
                pass
            return "STOPPED"

        try:
            url = f"{JENKINS_URL}job/{job_path}/job/{job_name}/{build_number}/api/json"
            response = requests.get(url, auth=(user, token), timeout=10)

            if response.status_code == 200:
                data = response.json()

                # 检查构建结果
                result = data.get('result')
                if result:
                    return result

                # 显示进度
                if not silent:
                    check_count += 1
                    elapsed = int(time.time() - start_time)
                    estimated_duration = data.get('estimatedDuration', 0)

                    if estimated_duration > 0:
                        progress = min(elapsed * 1000 / estimated_duration, 0.99)
                        bar_length = 30
                        filled = int(bar_length * progress)
                        bar = '█' * filled + '░' * (bar_length - filled)
                        pct = int(progress * 100)
                        # 每次更新换行，适合文件输出
                        print(f"⏳ [{bar}] {pct}% ({elapsed}s)", flush=True)
                    else:
                        # 如果没有预计时间，显示等待状态
                        dots = '.' * (check_count % 4)
                        print(f"⏳ 构建中{dots} ({elapsed}s)", flush=True)

        except Exception:
            pass

        time.sleep(2)

    if not silent:
        print("⏱️ 监控超时", flush=True)
    return "UNKNOWN"


# ============================================================================
# 主函数
# ============================================================================

def select_project_interactively(projects: List[Dict], prompt_msg: str = "请选择要发布的项目") -> Optional[Dict]:
    """交互式选择项目"""
    if not projects:
        print("没有可用的项目")
        return None

    print(f"\n{prompt_msg}:\n")

    # 按环境和名称排序
    sorted_projects = sorted(projects, key=lambda p: (p.get('env', ''), p.get('name', '')))

    # 显示项目列表
    for i, project in enumerate(sorted_projects, 1):
        env = project.get('env', '')
        name = project.get('name', '')
        full_name = project.get('full_name', '')
        print(f"  {i}. [{env}] {name} ({full_name})")

    # 获取用户选择
    while True:
        try:
            selection = input(f"\n请输入选项 (1-{len(sorted_projects)}, 或 q 退出): ").strip()
            if selection.lower() == 'q':
                print("已取消")
                return None

            index = int(selection) - 1
            if 0 <= index < len(sorted_projects):
                selected = sorted_projects[index]
                print(f"✓ 已选择: {selected['name']} ({selected['full_name']})")
                return selected
            else:
                print(f"请输入 1-{len(sorted_projects)} 之间的数字")
        except ValueError:
            print("请输入有效的数字")
        except KeyboardInterrupt:
            print("\n\n已取消")
            return None


def main():
    parser = argparse.ArgumentParser(description='ABC Jenkins 发布工具')
    parser.add_argument('project', nargs='?', help='Jenkins 项目名称')
    parser.add_argument('--branch', help='Git 分支名')
    parser.add_argument('--tag', help='Git 标签')
    parser.add_argument('--list', '-l', action='store_true', help='列出可用的 Jenkins 项目')
    parser.add_argument('--all', '-a', action='store_true', help='列出所有 Jenkins 项目（不根据 Git 仓库过滤）')
    parser.add_argument('--refresh', '-r', action='store_true', help='强制刷新缓存，重新从 Jenkins 获取数据')
    parser.add_argument('--params', help='JSON 格式的构建参数')
    parser.add_argument('--yes', '-y', action='store_true', help='跳过所有交互式确认，自动使用推断/提供的参数')
    parser.add_argument('--trigger-only-no-monitor', action='store_true', help='仅触发构建模式：直接使用提供的参数触发构建，返回 JSON')
    parser.add_argument('--monitor-only', action='store_true', help='后台监控模式')
    parser.add_argument('--full-name', help='项目完整路径（监控模式使用）')
    parser.add_argument('--queue-id', type=int, help='队列 ID（监控模式使用）')
    parser.add_argument('--display-name', help='项目显示名称（监控模式使用）')
    parser.add_argument('--stop', type=int, metavar='BUILD_NUMBER', help='停止指定构建号')
    parser.add_argument('--dry-run', action='store_true', help='模拟运行：显示将要执行的参数，但不实际触发构建')
    parser.add_argument('--validate', action='store_true', help='验证模式：检查参数格式和必填项，不触发构建')

    args = parser.parse_args()

    # 停止构建模式
    if args.stop:
        try:
            auth = get_jenkins_auth()
            job_path = None
            job_name = None
            project_name = None

            # 优先从构建信息文件读取（更快）
            build_info_file = CACHE_DIR / f"build_info_{args.stop}.json"
            if build_info_file.exists():
                try:
                    with open(build_info_file, 'r') as f:
                        build_info = json.load(f)
                    job_path = build_info['job_path']
                    job_name = build_info['job_name']
                    project_name = build_info.get('project_name', job_name)
                    print(f"✓ 从缓存读取构建信息")
                except Exception as e:
                    print(f"警告: 读取构建信息文件失败: {e}")

            # 如果没有构建信息文件，则遍历所有项目查找
            if not job_path:
                print(f"未找到构建信息缓存，正在搜索项目...")
                all_projects = get_jenkins_projects(auth, None, False)
                target_project = None
                for project in all_projects:
                    # 检查是否包含该构建号
                    job_url = f"{JENKINS_URL}job/{project['full_name'].replace('/', '/job/')}/{args.stop}/api/json"
                    response = requests.get(job_url, auth=(auth[0], auth[1]), timeout=5)
                    if response.status_code == 200:
                        target_project = project
                        break

                if not target_project:
                    print(f"错误: 未找到构建 #{args.stop} 对应的项目")
                    sys.exit(1)

                # 计算正确的 job_path 和 job_name
                parts = target_project['full_name'].split('/')
                if len(parts) > 2:
                    job_path = '/job/'.join(parts[:-1])
                else:
                    job_path = parts[0]
                job_name = parts[-1]
                project_name = target_project['name']

            print(f"停止构建: {project_name} Build #{args.stop}")
            print(f"项目: {job_path}/{job_name}")

            # 尝试停止构建
            if cancel_jenkins_build(auth, job_path, job_name, args.stop):
                print(f"✓ 已发送停止请求")
                # job_path 已经是正确格式（如 abc-his/job/test），直接使用
                print(f"构建 URL: {JENKINS_URL}job/{job_path}/{job_name}/{args.stop}/")

                # 删除停止标记文件（如果存在）
                stop_marker_file = CACHE_DIR / f"stop_build_{args.stop}.marker"
                if stop_marker_file.exists():
                    stop_marker_file.unlink()
                    print(f"✓ 已清理停止标记")

                # 删除构建信息文件（如果存在）
                build_info_file = CACHE_DIR / f"build_info_{args.stop}.json"
                if build_info_file.exists():
                    try:
                        build_info_file.unlink()
                        print(f"✓ 已清理构建信息缓存")
                    except:
                        pass
            else:
                print(f"✗ 停止请求失败")
            sys.exit(0)
        except Exception as e:
            print(f"错误: {e}")
            sys.exit(1)

    # 后台监控模式：用于子进程监控构建状态
    if args.monitor_only:
        if not args.full_name or not args.queue_id or not args.display_name:
            print("错误: --monitor-only 模式需要提供: --full-name <full_name> --queue-id <queue_id> --display-name <project_name>")
            sys.exit(1)

        try:
            auth = get_jenkins_auth()

            # 获取项目配置
            all_projects = get_jenkins_projects(auth, None, False)
            target_project = None
            for project in all_projects:
                if project['full_name'] == args.full_name:
                    target_project = project
                    break

            if not target_project:
                print(f"错误: 未找到项目 {args.full_name}")
                sys.exit(1)

            # 运行监控
            monitor_build_with_notification(auth, target_project, args.queue_id, args.display_name)
            sys.exit(0)
        except Exception as e:
            print(f"监控错误: {e}")
            sys.exit(1)

    # 仅触发构建模式：用于 Claude Code 技能
    if args.trigger_only_no_monitor:
        if not args.project:
            print("错误: --trigger-only 模式需要指定项目名称")
            sys.exit(1)

        # 解析提供的参数
        provided_params = {}
        if args.params:
            try:
                provided_params = json.loads(args.params)
            except json.JSONDecodeError:
                print("错误: 参数 JSON 格式错误")
                sys.exit(1)

        try:
            # 获取认证信息
            auth = get_jenkins_auth()

            # 获取项目配置
            all_projects = get_jenkins_projects(auth, None, args.refresh)
            target_project = None
            for project in all_projects:
                if project['name'] == args.project or project['full_name'] == args.project:
                    target_project = project
                    break

            if not target_project:
                print(f"错误: 未找到项目 {args.project}")
                sys.exit(1)

            # 获取项目参数定义（用于验证和显示）
            project_params = target_project.get('parameters', [])

            # 验证模式：检查参数格式和必填项
            if args.validate:
                import json as json_mod
                print_colored("[验证模式] 检查参数格式和必填项", 'yellow')
                print(f"\n项目: {target_project['name']} ({target_project['full_name']})")

                # 检查必填参数
                missing_required = []
                for param in project_params:
                    if param.get('required') and param['name'] not in provided_params:
                        missing_required.append(param['name'])

                # 检查未知参数
                param_names = {p['name'] for p in project_params}
                unknown_params = set(provided_params.keys()) - param_names

                # 验证结果
                print(f"\n✓ 项目找到: {target_project['full_name']}")
                print(f"✓ 参数定义: {len(project_params)} 个")
                print(f"✓ 提供的参数: {len(provided_params)} 个")

                if missing_required:
                    print_colored(f"\n✗ 缺少必填参数: {', '.join(missing_required)}", 'red')
                    for param in project_params:
                        if param.get('required') and param['name'] in missing_required:
                            print(f"  - {param['name']}: {param.get('description', '无描述')}")

                if unknown_params:
                    print_colored(f"\n⚠ 未知参数: {', '.join(unknown_params)}", 'yellow')

                if not missing_required and not unknown_params:
                    print_colored("\n✓ 所有参数验证通过", 'green')
                    sys.exit(0)
                else:
                    sys.exit(1)

            # Dry-run 模式：模拟触发构建
            if args.dry_run:
                import json as json_mod
                print_colored("[DRY RUN] 模拟运行，不会实际触发构建", 'yellow')
                print(f"\n项目: {target_project['name']} ({target_project['full_name']})")
                print(f"构建 URL: {JENKINS_URL}job/{target_project['full_name'].replace('/', '/job/')}/")
                print(f"\n构建参数:")

                if provided_params:
                    for key, value in provided_params.items():
                        # 找到参数定义获取类型和描述
                        param_def = next((p for p in project_params if p['name'] == key), None)
                        param_type = param_def.get('type', 'Unknown') if param_def else 'Unknown'
                        print(f"  {key}: {value}  [{param_type}]")
                else:
                    print("  (无参数)")

                # 模拟返回 JSON
                result = {
                    'dry_run': True,
                    'full_name': target_project['full_name'],
                    'project_name': target_project['name'],
                    'build_url': f"{JENKINS_URL}job/{target_project['full_name'].replace('/', '/job/')}/",
                    'params': provided_params,
                    'message': 'DRY RUN - 未实际触发构建'
                }
                print(f"\n{json_mod.dumps(result, indent=2, ensure_ascii=False)}")
                sys.exit(0)

            # 直接触发构建
            print(f"触发构建: {target_project['name']} ({target_project['full_name']})")
            print(f"参数: {provided_params}")

            # 清理旧的缓存文件（在触发新构建前）
            try:
                current_time = time.time()
                # 清理超过 1 小时的构建参数文件
                for f in CACHE_DIR.glob('build_params_*.json'):
                    if f.stat().st_mtime < current_time - 3600:
                        f.unlink()
                # 清理超过 1 小时的构建信息文件
                for f in CACHE_DIR.glob('build_info_*.json'):
                    if f.stat().st_mtime < current_time - 3600:
                        f.unlink()
                # 清理所有停止标记文件
                for f in CACHE_DIR.glob('stop_build_*.marker'):
                    f.unlink()
            except Exception as e:
                pass  # 清理失败不影响构建

            queue_id = trigger_build(auth, target_project, provided_params)

            if queue_id:
                # 保存构建参数到缓存文件（供监控任务读取）
                params_file = CACHE_DIR / f"build_params_{queue_id}.json"
                params_data = {
                    'queue_id': queue_id,
                    'full_name': target_project['full_name'],
                    'project_name': target_project['name'],
                    'params': provided_params,
                    'timestamp': time.time()
                }
                try:
                    CACHE_DIR.mkdir(parents=True, exist_ok=True)
                    with open(params_file, 'w') as f:
                        json.dump(params_data, f, indent=2)
                except Exception as e:
                    print(f"警告: 无法保存构建参数: {e}", file=sys.stderr)

                # 仅触发构建，不启动监控（由调用方启动监控）
                # 输出 JSON 格式，方便 Claude Code 解析
                import json as json_mod
                result = {
                    'queue_id': queue_id,
                    'full_name': target_project['full_name'],
                    'project_name': target_project['name'],
                    'build_url': f"{JENKINS_URL}job/{target_project['full_name'].replace('/', '/job/')}/"
                }
                print(json_mod.dumps(result))
                sys.exit(0)
            else:
                print("错误: 构建触发失败")
                sys.exit(1)

        except Exception as e:
            print(f"错误: {e}")
            sys.exit(1)

    try:
        # 获取认证信息
        print("正在获取 Jenkins 认证信息...")
        auth = get_jenkins_auth()
        print("✓ 认证信息已获取\n")

        # 获取 Git 信息（用于过滤项目）
        git_info = get_git_info()

        # 列出项目
        if args.list:
            if args.all:
                # 列出所有项目
                projects = get_jenkins_projects(auth, None, args.refresh)
            else:
                # 根据 Git 仓库过滤
                projects = get_jenkins_projects(auth, git_info.get('remote_url'), args.refresh)

            if not projects:
                if args.all:
                    print("未找到任何 Jenkins 项目")
                else:
                    print("未找到与当前 Git 仓库相关的 Jenkins 项目")
                    print("提示：使用 --all 参数可以列出所有 Jenkins 项目")
                return

            print("可用的 Jenkins 项目:")
            for project in projects:
                env = project.get('env', '')
                name = project.get('name', '')
                full_name = project.get('full_name', '')
                print(f"  - {name} ({full_name})")
            return

        # 根据 Git 仓库过滤项目
        filtered_projects = get_jenkins_projects(auth, git_info.get('remote_url'), args.refresh)

        target_project = None

        # 情况1: 用户没有指定项目名称 -> 交互式选择
        if not args.project:
            if not filtered_projects:
                print("未找到与当前 Git 仓库相关的 Jenkins 项目")
                print("提示：使用 --list --all 查看所有可用项目")
                return
            target_project = select_project_interactively(filtered_projects, "请选择要发布的项目")
            if not target_project:
                return

        # 情况2: 用户指定了项目名称 -> 验证是否存在
        else:
            # 先在过滤后的项目中查找
            for project in filtered_projects:
                if project['name'] == args.project or project['full_name'] == args.project:
                    target_project = project
                    break

            # 如果在过滤后的项目中没找到，在所有项目中查找
            if not target_project:
                all_projects = get_jenkins_projects(auth, None, args.refresh)
                for project in all_projects:
                    if project['name'] == args.project or project['full_name'] == args.project:
                        target_project = project
                        break

            # 找到了，直接使用
            if target_project:
                print(f"✓ 找到项目: {target_project['name']} ({target_project['full_name']})")
            else:
                # 没找到，让用户选择
                print(f"⚠ 未找到项目: {args.project}")
                if filtered_projects:
                    target_project = select_project_interactively(filtered_projects, "请从相关项目中选择")
                else:
                    target_project = select_project_interactively(all_projects, "请从所有项目中选择")

                if not target_project:
                    return

        # 解析用户提供的参数
        provided_params = {}
        if args.params:
            try:
                provided_params = json.loads(args.params)
            except json.JSONDecodeError:
                print("参数 JSON 格式错误")
                return

        if args.branch:
            provided_params['repoBranch'] = args.branch
            # 从分支名解析 TAPD ID
            parts = args.branch.split('-')
            if parts:
                last_part = parts[-1]
                if last_part.isdigit():
                    git_info['tapd_id'] = last_part
                    git_info['branch'] = args.branch

        if args.tag:
            provided_params['repoTag'] = args.tag
            # 更新 git_info 中的 tag
            git_info['tag'] = args.tag

        # ========== 验证模式和模拟运行模式 ==========
        # 这两种模式不需要交互式收集参数，直接使用提供的参数进行验证或模拟

        # 获取项目参数定义（用于验证和显示）
        project_params = target_project.get('parameters', [])

        # 验证模式：检查参数格式和必填项
        if args.validate:
            import json as json_mod
            print_colored("[验证模式] 检查参数格式和必填项", 'yellow')
            print(f"\n项目: {target_project['name']} ({target_project['full_name']})")

            has_error = False

            # 检查必填参数
            missing_required = []
            for param in project_params:
                if param.get('required') and param['name'] not in provided_params:
                    missing_required.append(param['name'])

            # 特殊处理：featureNo 和 envNo 如果项目有这些参数，默认为必填
            # 即使 Jenkins API 没有标记为 required
            param_names = {p['name'] for p in project_params}
            for special_param in ['featureNo', 'envNo']:
                if special_param in param_names and special_param not in provided_params:
                    if special_param not in missing_required:
                        missing_required.append(special_param)

            # 检查未知参数
            unknown_params = set(provided_params.keys()) - param_names

            # 检查 featureNo 和 envNo 的范围 (1-100)
            range_errors = []
            for key, value in provided_params.items():
                if key in ['featureNo', 'envNo']:
                    # 检查是否为数字
                    if not str(value).isdigit():
                        range_errors.append(f"{key}: '{value}' 不是有效数字 (1-100)")
                        has_error = True
                    else:
                        num = int(value)
                        if num < 1 or num > 100:
                            range_errors.append(f"{key}: {value} 超出范围 (1-100)")
                            has_error = True

            # 验证结果
            print(f"\n✓ 项目找到: {target_project['full_name']}")
            print(f"✓ 参数定义: {len(project_params)} 个")
            print(f"✓ 提供的参数: {len(provided_params)} 个")

            if missing_required:
                print_colored(f"\n✗ 缺少必填参数: {', '.join(missing_required)}", 'red')
                for param in project_params:
                    if param.get('required') and param['name'] in missing_required:
                        print(f"  - {param['name']}: {param.get('description', '无描述')}")
                has_error = True

            if unknown_params:
                print_colored(f"\n⚠ 未知参数: {', '.join(unknown_params)}", 'yellow')

            if range_errors:
                print_colored(f"\n✗ 参数范围错误:", 'red')
                for err in range_errors:
                    print(f"  - {err}")

            if not has_error and not missing_required and not unknown_params:
                print_colored("\n✓ 所有参数验证通过", 'green')
                sys.exit(0)
            else:
                sys.exit(1)

        # Dry-run 模式：模拟触发构建
        if args.dry_run:
            import json as json_mod
            print_colored("[DRY RUN] 模拟运行，不会实际触发构建", 'yellow')
            print(f"\n项目: {target_project['name']} ({target_project['full_name']})")
            print(f"构建 URL: {JENKINS_URL}job/{target_project['full_name'].replace('/', '/job/')}/")
            print(f"\n构建参数:")

            if provided_params:
                for key, value in provided_params.items():
                    # 找到参数定义获取类型和描述
                    param_def = next((p for p in project_params if p['name'] == key), None)
                    param_type = param_def.get('type', 'Unknown') if param_def else 'Unknown'
                    print(f"  {key}: {value}  [{param_type}]")
            else:
                print("  (无参数)")

            # 模拟返回 JSON
            result = {
                'dry_run': True,
                'full_name': target_project['full_name'],
                'project_name': target_project['name'],
                'build_url': f"{JENKINS_URL}job/{target_project['full_name'].replace('/', '/job/')}/",
                'params': provided_params,
                'message': 'DRY RUN - 未实际触发构建'
            }
            print(f"\n{json_mod.dumps(result, indent=2, ensure_ascii=False)}")
            sys.exit(0)

        # ========== 交互式发布模式 ==========
        # 收集构建参数
        print(f"\n项目: {target_project['name']} ({target_project['full_name']})")
        print("收集构建参数:")

        properties = collect_build_parameters(target_project, git_info, provided_params, args.yes)

        # 用户取消构建
        if not properties:
            print("构建已取消，退出")
            return

        # 触发构建
        queue_id = trigger_build(auth, target_project, properties)

        if queue_id:
            # 监控构建状态
            monitor_build(auth, target_project, queue_id)

    except KeyboardInterrupt:
        print("\n\n操作已取消")
    except Exception as e:
        print(f"\n错误: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
