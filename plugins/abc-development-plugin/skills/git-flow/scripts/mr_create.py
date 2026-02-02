#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
ABC Git MR 创建脚本
支持非交互式创建 Merge Request，直接调用 Codeup API
"""

import argparse
import os
import sys
import subprocess
import json
from pathlib import Path
from typing import Optional, Tuple
import requests


# ============================================================================
# 配置常量
# ============================================================================

CODEUP_BASE_URL = 'https://openapi-rdc.aliyuncs.com/oapi/v1'
ORGANIZATION_ID = '62d62893487c500c27f72e36'
OA_RPC_BASE_URL = 'http://oa.rpc.abczs.cn'

CONFIG_DIR = Path.home() / '.abc-fed-config'
CONFIG_FILE = CONFIG_DIR / 'mr.json'

TARGET_BRANCHES = ['master', 'gray', 'rc', 'develop']


# ============================================================================
# 工具函数
# ============================================================================

def print_colored(message: str, color: str = 'white') -> None:
    """打印彩色输出"""
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


def get_remote_url() -> str:
    """获取远程仓库 URL"""
    try:
        return run_git_command(['git', 'config', '--get', 'remote.origin.url'])
    except:
        raise Exception("无法获取远程仓库 URL")


# ============================================================================
# 配置管理
# ============================================================================

def load_config() -> dict:
    """加载 MR 配置"""
    if not CONFIG_FILE.exists():
        raise Exception(
            "MR 配置文件不存在。请先运行: git abc mr config\n"
            f"或手动创建配置文件: {CONFIG_FILE}\n"
            f"格式: {{\"yunxiaoToken\": \"xxx\", \"webhookUrl\": \"xxx\"}}"
        )

    try:
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
            if not config.get('yunxiaoToken') or not config.get('webhookUrl'):
                raise Exception("配置文件缺少必要字段")
            return config
    except json.JSONDecodeError:
        raise Exception("配置文件格式错误")


# ============================================================================
# Codeup API
# ============================================================================

def create_default_options(token: str) -> dict:
    """创建 API 请求选项"""
    return {
        'headers': {
            'Content-Type': 'application/json',
            'x-yunxiao-token': token,
        }
    }


def get_current_user(token: str) -> dict:
    """获取当前用户信息"""
    response = requests.get(
        f"{CODEUP_BASE_URL}/platform/user",
        **create_default_options(token)
    )
    if response.status_code != 200:
        raise Exception("获取用户信息失败，请检查 yunxiaoToken 是否正确")
    return response.json()


def get_current_repo(url: str, token: str) -> dict:
    """获取当前仓库信息"""
    # 处理 ssh 和 https
    url = url.replace('git@codeup.aliyun.com:', '').replace('https://codeup.aliyun.com/', '')
    final_path = url.replace('.git', '')
    search = final_path.split('/').pop()

    response = requests.get(
        f"{CODEUP_BASE_URL}/codeup/organizations/{ORGANIZATION_ID}/repositories",
        params={'search': search},
        **create_default_options(token)
    )

    if response.status_code != 200:
        raise Exception("获取仓库信息失败")

    repos = response.json()
    if not repos:
        raise Exception(f"未找到仓库: {final_path}")

    result = next((r for r in repos if r.get('pathWithNamespace') == final_path), None)
    if not result:
        raise Exception(f"未找到仓库: {final_path}")

    return result


def get_repo_members(repo_id: str, token: str) -> list:
    """获取仓库成员列表"""
    response = requests.get(
        f"{CODEUP_BASE_URL}/codeup/organizations/{ORGANIZATION_ID}/repositories/{repo_id}/members",
        **create_default_options(token)
    )

    if response.status_code != 200:
        raise Exception("获取项目成员列表失败")

    return response.json()


def get_reviewer_ids(names: list, members: list) -> list:
    """根据姓名获取评审者 ID 列表"""
    member_map = {m['name']: m['userId'] for m in members}
    reviewer_ids = []

    for name in names:
        if name in member_map:
            reviewer_ids.append(member_map[name])
        else:
            print(f"⚠️  未找到评审者: {name}")

    return reviewer_ids


def create_merge_request(
    repo_id: str,
    source_branch: str,
    target_branch: str,
    title: str,
    description: str,
    reviewer_ids: list,
    token: str
) -> dict:
    """创建合并请求"""
    response = requests.post(
        f"{CODEUP_BASE_URL}/codeup/organizations/{ORGANIZATION_ID}/repositories/{repo_id}/changeRequests",
        **create_default_options(token),
        json={
            'title': title,
            'description': description,
            'sourceBranch': source_branch,
            'targetBranch': target_branch,
            'reviewerUserIds': reviewer_ids,
            'targetProjectId': repo_id,
            'sourceProjectId': repo_id
        }
    )

    if response.status_code != 200:
        raise Exception(f"创建合并请求失败: {response.text}")

    result = response.json()
    if not result.get('detailUrl'):
        raise Exception("创建合并请求失败")

    return result


def send_wechat_notification(webhook_url: str, merge_url: str, title: str, reviewer_names: list, current_user_name: str) -> bool:
    """发送企业微信通知"""
    try:
        # 获取企业微信用户列表
        response = requests.get(
            f"{OA_RPC_BASE_URL}/rpc/monitor/users",
            headers={'Content-Type': 'application/json', 'x-app-env': 'v'}
        )

        if response.status_code != 200:
            print("⚠️  获取企业微信用户失败，跳过通知")
            return False

        wechat_users = response.json()

        # 查找匹配的用户
        user_ids = [
            u['user_id'] for u in wechat_users
            if u['name'] in reviewer_names
        ]

        if not user_ids:
            print("⚠️  未找到企业微信用户，跳过通知")
            return False

        # 发送通知
        requests.post(webhook_url, json={
            'msgtype': 'text',
            'text': {
                'content': f"{current_user_name}发起合并请求：【{title}】, 请帮忙review \n  {merge_url} \n",
                'mentioned_list': user_ids
            }
        })

        return True
    except Exception as e:
        print(f"⚠️  企业微信通知失败: {e}")
        return False


# ============================================================================
# 主流程
# ============================================================================

def create_mr(
    target_branch: str,
    title: str,
    reviewers: list,
    description: str = "",
    skip_notify: bool = False
) -> None:
    """创建 MR 主流程"""

    # 加载配置
    print("加载配置...")
    config = load_config()
    token = config['yunxiaoToken']
    webhook_url = config['webhookUrl']

    # 获取当前信息
    print("获取仓库信息...")
    current_branch = get_current_branch()
    remote_url = get_remote_url()

    current_user = get_current_user(token)
    current_repo = get_current_repo(remote_url, token)
    members = get_repo_members(current_repo['id'], token)

    # 获取评审者 IDs
    reviewer_ids = get_reviewer_ids(reviewers, members)
    if not reviewer_ids:
        raise Exception("未找到有效的评审者")

    print(f"准备创建 MR: {current_branch} -> {target_branch}")
    print(f"评审者: {', '.join(reviewers)}")

    # 创建 MR
    print("创建合并请求...")
    result = create_merge_request(
        repo_id=current_repo['id'],
        source_branch=current_branch,
        target_branch=target_branch,
        title=title,
        description=description,
        reviewer_ids=reviewer_ids,
        token=token
    )

    detail_url = result['detailUrl']
    conflict_status = result.get('conflictCheckStatus', '')

    print(f"✅ MR 创建成功!")
    print(f"🔗 {detail_url}")

    # 复制到剪贴板
    try:
        subprocess.run(['pbcopy'], input=detail_url.encode(), check=True)
        print("📋 MR 地址已复制到剪贴板")
    except:
        pass

    # 冲突检查
    if conflict_status == 'HAS_CONFLICT':
        print("⚠️  合并请求存在冲突，请手动解决冲突")

    # 发送通知
    if not skip_notify:
        print("发送企业微信通知...")
        send_wechat_notification(
            webhook_url, detail_url, title, reviewers, current_user['name']
        )


# ============================================================================
# 命令行入口
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='ABC Git MR 非交互式创建工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 创建 MR
  %(prog)s -t develop -T "feat: 新功能" -r 张三 李四

  # 指定描述
  %(prog)s -t develop -T "fix: 修复bug" -r 张三 -d "修复了xxx问题"

  # 跳过企业微信通知
  %(prog)s -t develop -T "feat: xxx" -r 张三 --skip-notify

评审者说明:
  - 评审者姓名必须是 Codeup 仓库成员的真实姓名
  - 多个评审者用空格分隔
  - 可以使用 --reviewers 参数或 -r 简写
        """
    )

    parser.add_argument('-t', '--target', required=True,
                       help='目标分支 (master/gray/rc/develop 或自定义分支)')

    parser.add_argument('-T', '--title', required=True,
                       help='MR 标题')

    parser.add_argument('-r', '--reviewers', nargs='+', required=True,
                       help='评审者姓名（多个用空格分隔）')

    parser.add_argument('-d', '--description', default='',
                       help='MR 描述（默认为空）')

    parser.add_argument('--skip-notify', action='store_true',
                       help='跳过企业微信通知')

    args = parser.parse_args()

    try:
        create_mr(
            target_branch=args.target,
            title=args.title,
            reviewers=args.reviewers,
            description=args.description,
            skip_notify=args.skip_notify
        )
    except Exception as e:
        print_colored(f"❌ 错误: {e}", 'red')
        sys.exit(1)


if __name__ == '__main__':
    main()
