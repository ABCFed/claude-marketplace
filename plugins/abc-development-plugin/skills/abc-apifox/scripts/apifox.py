#!/usr/bin/env python3
"""
ABC Apifox CLI - ABC 医疗云 API 文档查询工具

查询命令:
    get_path      - 获取接口详情
    get_schema    - 获取 Schema 定义
    search_paths  - 搜索接口
    list_modules  - 列出所有模块
    get_module    - 获取模块的所有接口

管理命令:
    refresh_oas   - 刷新 OpenAPI 文档
    status        - 查看缓存状态
    clear_cache   - 清除缓存
"""

import sys
import os
import json
import argparse

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from apifox_client import ApifoxClient
from cache_manager import CacheManager


def print_json(data):
    """打印 JSON 格式输出"""
    print(json.dumps(data, ensure_ascii=False, indent=2))


def cmd_get_path(args):
    """获取接口详情"""
    client = ApifoxClient()
    result = client.get_path_detail(args.path, args.method, resolve_refs=args.include_refs)
    print_json({'success': True, 'data': result})


def cmd_get_schema(args):
    """获取 Schema 定义"""
    cache = CacheManager()
    schema = cache.load_schema(args.name)
    if schema:
        print_json({'success': True, 'data': schema})
    else:
        print_json({'success': False, 'error': f'Schema not found: {args.name}'})


def cmd_search_paths(args):
    """搜索接口"""
    client = ApifoxClient()
    results = client.search_paths(
        keyword=args.keyword,
        module=args.module,
        method=args.method,
        limit=args.limit
    )
    print_json({
        'success': True,
        'keyword': args.keyword,
        'total': len(results),
        'paths': results
    })


def cmd_list_modules(args):
    """列出所有模块"""
    client = ApifoxClient()
    modules = client.list_modules()
    print_json({
        'success': True,
        'total': len(modules),
        'modules': modules
    })


def cmd_get_module(args):
    """获取模块的所有接口"""
    client = ApifoxClient()
    paths = client.get_module_paths(args.module)
    print_json({
        'success': True,
        'module': args.module,
        'total': len(paths),
        'paths': paths
    })


def cmd_refresh_oas(args):
    """刷新 OpenAPI 文档"""
    client = ApifoxClient()
    result = client.refresh_project_oas()
    print_json(result)


def cmd_status(args):
    """查看缓存状态"""
    cache = CacheManager()
    status = cache.get_status()
    print_json(status)


def cmd_clear_cache(args):
    """清除缓存"""
    if not args.force:
        print("错误: 请使用 --force 参数确认清除缓存")
        sys.exit(1)
    cache = CacheManager()
    cache.clear_all()


def main():
    parser = argparse.ArgumentParser(description='ABC Apifox CLI')
    subparsers = parser.add_subparsers(dest='command', help='可用命令')

    # get_path
    p = subparsers.add_parser('get_path', help='获取接口详情')
    p.add_argument('--path', required=True, help='接口路径')
    p.add_argument('--method', required=True,
                   choices=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'],
                   help='请求方法')
    p.add_argument('--include_refs', default='true',
                   help='是否解析 $ref 引用')

    # get_schema
    p = subparsers.add_parser('get_schema', help='获取 Schema 定义')
    p.add_argument('--name', required=True, help='Schema 名称')

    # search_paths
    p = subparsers.add_parser('search_paths', help='搜索接口')
    p.add_argument('--keyword', required=True, help='搜索关键词')
    p.add_argument('--module', help='模块过滤')
    p.add_argument('--method', help='方法过滤')
    p.add_argument('--limit', type=int, help='返回数量限制')

    # list_modules
    subparsers.add_parser('list_modules', help='列出所有模块')

    # get_module
    p = subparsers.add_parser('get_module', help='获取模块的所有接口')
    p.add_argument('--module', required=True, help='模块名，如 api.stocks')

    # refresh_oas
    subparsers.add_parser('refresh_oas', help='刷新 OpenAPI 文档')

    # status
    subparsers.add_parser('status', help='查看缓存状态')

    # clear_cache
    p = subparsers.add_parser('clear_cache', help='清除缓存')
    p.add_argument('--force', action='store_true', help='确认清除')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # 执行命令
    commands = {
        'get_path': cmd_get_path,
        'get_schema': cmd_get_schema,
        'search_paths': cmd_search_paths,
        'list_modules': cmd_list_modules,
        'get_module': cmd_get_module,
        'refresh_oas': cmd_refresh_oas,
        'status': cmd_status,
        'clear_cache': cmd_clear_cache,
    }

    cmd_func = commands.get(args.command)
    if cmd_func:
        cmd_func(args)
    else:
        print(f"未知命令: {args.command}")
        sys.exit(1)


if __name__ == '__main__':
    main()
