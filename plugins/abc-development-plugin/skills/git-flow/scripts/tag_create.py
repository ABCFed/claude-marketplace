#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
ABC Git Tag 创建脚本
支持非交互式创建 tag，直接调用 API
"""

import argparse
import os
import sys
import subprocess
import re
from datetime import datetime
from typing import Optional, Tuple
import requests


# ============================================================================
# 配置常量
# ============================================================================

BASE_URL = 'http://oa.rpc.abczs.cn'
BUSINESS_PREFIX_MAP = {
    'abc-global': 'global-',
    'abc-his': '',
    'abc-oa': 'oa-',
    'abc-bis': 'bis-',
    'mira': 'mira-',
}

TAG_TYPE_CONFIG = {
    'f': {'name': '需求提测', 'deployable': False, 'qa': True, 'branch_restriction': None},
    't': {'name': '测试环境', 'deployable': False, 'qa': True, 'branch_restriction': None},
    'v': {'name': '正式环境', 'deployable': True, 'qa': False, 'branch_restriction': 'master'},
    'g': {'name': '灰度环境', 'deployable': True, 'qa': False, 'branch_restriction': 'gray'},
    'p': {'name': '预发布', 'deployable': True, 'qa': False, 'branch_restriction': 'rc'},
}


# ============================================================================
# Git 操作
# ============================================================================

def run_git_command(cmd: list) -> str:
    """执行 git 命令并返回输出"""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        raise Exception(f"Git 命令执行失败: {' '.join(cmd)}\n{e.stderr}")


def get_current_branch() -> str:
    """获取当前分支名"""
    return run_git_command(['git', 'rev-parse', '--abbrev-ref', 'HEAD'])


def get_git_config(key: str) -> Optional[str]:
    """获取 git 配置"""
    try:
        return run_git_command(['git', 'config', '--get', key])
    except:
        return None


def get_tag_prefix() -> str:
    """获取 tag 前缀"""
    prefix = get_git_config('abcflow.prefix.tag')
    if not prefix:
        raise Exception(
            "未配置 tag 前缀。请先执行: git abc tag config <前缀>\n"
            "或使用 --prefix 参数指定前缀"
        )
    return prefix


def get_latest_tag(tag_type: str, prefix: str) -> str:
    """获取最新的 tag"""
    try:
        # 获取当前年份
        year = datetime.now().year
        pattern = f"{prefix}-{tag_type}{year}.*"
        tags = run_git_command([
            'git', 'tag', '-l', pattern, '--sort=-v:refname'
        ]).split('\n')
        return tags[0] if tags and tags[0] else f"{prefix}-{tag_type}{year}.0.0"
    except:
        return f"{prefix}-{tag_type}{datetime.now().year}.0.0"


def generate_new_tag(tag_type: str, prefix: str) -> str:
    """生成新 tag"""
    latest = get_latest_tag(tag_type, prefix)
    # 解析: prefix-v2025.05.01 -> extract week and build
    match = re.search(rf'{re.escape(prefix)}-{re.escape(tag_type)}(\d+)\.(\d+)\.(\d+)', latest)
    if match:
        year, week, build = match.groups()
        # 这里简化处理，实际需要根据当前日期计算周数
        new_build = str(int(build) + 1).zfill(2)
        return f"{prefix}-{tag_type}{year}.{week}.{new_build}"
    # 默认格式
    return f"{prefix}-{tag_type}{datetime.now().year}.1.01"


def create_and_push_tag(tag_name: str) -> None:
    """创建并推送 tag"""
    # 更新分支
    print(f"更新当前分支...")
    try:
        run_git_command(['git', 'fetch', '--tags'])
        run_git_command(['git', 'pull', '--rebase'])
    except:
        print("警告: 分支更新失败，继续创建 tag")

    # 创建 tag
    print(f"创建 tag: {tag_name}")
    run_git_command(['git', 'tag', tag_name])

    # 推送 tag
    print(f"推送 tag 到远程...")
    run_git_command(['git', 'push', 'origin', tag_name])
    print(f"✅ Tag 创建成功: {tag_name}")


# ============================================================================
# API 调用
# ============================================================================

def get_opened_deploy_task(task_type: int = 0) -> Optional[dict]:
    """获取开放的班车/提测任务"""
    try:
        response = requests.get(f"{BASE_URL}/rpc/low-code/deployment/deploy-task/opened?type={task_type}")
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print(f"警告: 获取班车任务失败 - {e}")
        return None


def post_deploy_tag(
    tag_name: str,
    prefix: str,
    deps: str,
    operation: str,
    remark: str,
    created_by: str,
    tapd_id: str = "",
    is_hotfix: int = 0
) -> bool:
    """提交 tag 上车/提测信息"""
    try:
        response = requests.post(
            f"{BASE_URL}/rpc/low-code/deployment/deploy-tag",
            json={
                'name': tag_name,
                'prefix': prefix,
                'type': is_hotfix,
                'deps': deps,
                'operation': operation,
                'remark': remark,
                'tapdId': tapd_id,
                'createdBy': created_by
            }
        )
        if response.status_code == 200:
            print(f"✅ Tag 已上车/提测")
            return True
        else:
            print(f"⚠️  API 调用失败: {response.text}")
            return False
    except Exception as e:
        print(f"⚠️  上车/提测失败: {e}")
        return False


# ============================================================================
# 主流程
# ============================================================================

def create_tag(
    tag_type: str,
    business: str = 'abc-his',
    prefix: Optional[str] = None,
    hotfix: bool = False,
    deps: Optional[str] = None,
    operation: Optional[str] = None,
    remark: Optional[str] = None,
    tapd_id: Optional[str] = None,
    skip_deploy: bool = False
) -> None:
    """创建 tag 主流程"""

    # 验证 tag 类型
    if tag_type not in TAG_TYPE_CONFIG:
        raise Exception(f"无效的 tag 类型: {tag_type}。支持的类型: {', '.join(TAG_TYPE_CONFIG.keys())}")

    # 获取配置
    if not prefix:
        prefix = get_tag_prefix()

    # 添加业务前缀
    full_prefix = BUSINESS_PREFIX_MAP.get(business, '') + prefix
    created_by = get_git_config('user.name') or 'Unknown'

    # 验证分支约束
    current_branch = get_current_branch()
    required_branch = TAG_TYPE_CONFIG[tag_type]['branch_restriction']
    if required_branch and current_branch != required_branch:
        raise Exception(
            f"❌ {tag_type} tag 只能在 {required_branch} 分支创建\n"
            f"当前分支: {current_branch}"
        )

    # 生成 tag 名
    tag_name = generate_new_tag(tag_type, full_prefix)
    print(f"准备创建 tag: {tag_name}")

    # 创建并推送 tag
    create_and_push_tag(tag_name)

    # 处理后续（上车/提测）
    if skip_deploy:
        print("⏭️  跳过上车/提测")
        return

    config = TAG_TYPE_CONFIG[tag_type]

    # 可部署类型
    if config['deployable']:
        if not deps or not operation:
            print("⚠️  可部署 tag 需要填写上车信息")
            print("使用 --deps 和 --operation 参数指定，或使用 --skipdeploy 跳过")
            return

        # 检查班车
        task = get_opened_deploy_task(0)
        if not task:
            print("⚠️  当前没有班车，请联系测试同学开车")
            return

        print(f"🚀 上班车: {task.get('name', 'N/A')}")

        # 提交上车信息
        post_deploy_tag(
            tag_name, full_prefix, deps, operation, remark or '无',
            created_by, is_hotfix=int(hotfix)
        )

    # 可提测类型
    elif config['qa']:
        if not deps or not operation or not remark:
            print("⚠️  提测 tag 需要填写提测信息")
            print("使用 --deps --operation --remark 参数指定，或使用 --skipdeploy 跳过")
            return

        # 检查提测任务
        task = get_opened_deploy_task(1)
        if not task:
            print("⚠️  当前没有测试任务，请联系测试同学开车")
            return

        print(f"🧪 提测任务: {task.get('name', 'N/A')}")

        # 提交提测信息
        post_deploy_tag(
            tag_name, full_prefix, deps, operation, remark,
            created_by, tapd_id=tapd_id or ''
        )
    else:
        # 复制到剪贴板
        print(f"📋 Tag 已复制到剪贴板，粘贴给测试同学即可")


# ============================================================================
# 命令行入口
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='ABC Git Tag 非交互式创建工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 创建正式环境 tag
  %(prog)s v --deps "abc-auth" --operation "无"

  # 创建需求提测 tag
  %(prog)s f --deps "无" --operation "无" --remark "feat: 新功能" --tapd-id "1122044681001112866"

  # 指定业务线和前缀
  %(prog)s v -b abc-oa --prefix pc --deps "abc-auth" --operation "无"

  # Hotfix 模式
  %(prog)s v --hotfix --deps "abc-auth" --operation "刷数据"
        """
    )

    parser.add_argument('tag_type', choices=['f', 't', 'v', 'g', 'p'],
                       help='Tag 类型: f=需求提测, t=测试环境, v=正式环境, g=灰度环境, p=预发布')

    parser.add_argument('-b', '--business', default='abc-his',
                       choices=['abc-global', 'abc-his', 'abc-oa', 'abc-bis', 'mira'],
                       help='业务线 (默认: abc-his)')

    parser.add_argument('--prefix', help='Tag 前缀 (默认从 git config 读取)')

    parser.add_argument('--hotfix', action='store_true', help='Hotfix 模式')

    parser.add_argument('--deps', default='无', help='依赖的服务 (默认: 无)')
    parser.add_argument('--operation', default='无', help='需要的操作 (默认: 无)')
    parser.add_argument('--remark', help='备注/说明 (提测时必填)')
    parser.add_argument('--tapd-id', help='关联的 TAPD ID (f tag 可选)')

    parser.add_argument('--skipdeploy', action='store_true',
                       help='跳过上车/提测，仅创建 tag')

    args = parser.parse_args()

    try:
        create_tag(
            tag_type=args.tag_type,
            business=args.business,
            prefix=args.prefix,
            hotfix=args.hotfix,
            deps=args.deps,
            operation=args.operation,
            remark=args.remark,
            tapd_id=args.tapd_id,
            skip_deploy=args.skipdeploy
        )
    except Exception as e:
        print(f"❌ 错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
