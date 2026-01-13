#!/usr/bin/env python3
"""
Apifox 统一命令行工具

ABC 医疗云 API 文档查询工具
"""

import argparse
import json
import sys
import os

# 添加当前目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from apifox_client import ApifoxClient
from cache_manager import CacheManager


def cmd_read_oas(args):
    """读取完整 OpenAPI 规范"""
    client = ApifoxClient()
    try:
        oas = client.read_project_oas()
        print(json.dumps(oas, ensure_ascii=False, indent=2))
    except Exception as e:
        print(json.dumps({'error': str(e)}, ensure_ascii=False))


def cmd_refresh_oas(args):
    """刷新最新文档"""
    client = ApifoxClient()
    try:
        status = client.refresh_project_oas()
        print(json.dumps(status, ensure_ascii=False, indent=2))
    except Exception as e:
        print(json.dumps({'error': str(e)}, ensure_ascii=False))


def cmd_list_paths(args):
    """列出接口路径"""
    client = ApifoxClient()
    try:
        paths = client.list_paths(
            module=args.module,
            method=args.method,
            limit=args.limit,
            offset=args.offset
        )
        result = {
            'success': True,
            'total': len(paths),
            'paths': paths
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(json.dumps({'success': False, 'error': str(e)}, ensure_ascii=False))


def cmd_search_paths(args):
    """搜索接口"""
    client = ApifoxClient()
    try:
        paths = client.search_paths(
            keyword=args.keyword,
            module=args.module,
            method=args.method
        )
        result = {
            'success': True,
            'keyword': args.keyword,
            'total': len(paths),
            'paths': paths
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(json.dumps({'success': False, 'error': str(e)}, ensure_ascii=False))


def cmd_get_path(args):
    """获取接口详情"""
    client = ApifoxClient()
    try:
        detail = client.get_path_detail(
            path=args.path,
            method=args.method,
            resolve_refs=args.include_refs
        )
        result = {
            'success': True,
            'data': detail
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(json.dumps({'success': False, 'error': str(e)}, ensure_ascii=False))


def cmd_list_modules(args):
    """列出所有模块"""
    client = ApifoxClient()
    try:
        modules = client.list_modules()
        result = {
            'success': True,
            'total': len(modules),
            'modules': modules
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(json.dumps({'success': False, 'error': str(e)}, ensure_ascii=False))


def cmd_stats(args):
    """统计信息"""
    client = ApifoxClient()
    try:
        stats = client.get_stats(detail=args.detail)
        result = {
            'success': True,
            'stats': stats
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(json.dumps({'success': False, 'error': str(e)}, ensure_ascii=False))


def cmd_cache_status(args):
    """缓存状态"""
    cache = CacheManager()
    try:
        status = cache.get_status()
        print(json.dumps({'success': True, 'status': status}, ensure_ascii=False, indent=2))
    except Exception as e:
        print(json.dumps({'success': False, 'error': str(e)}, ensure_ascii=False))


def cmd_clear_cache(args):
    """清除缓存"""
    cache = CacheManager()
    try:
        if args.force:
            cache.clear_all()
            print(json.dumps({'success': True, 'message': '缓存已清除'}, ensure_ascii=False))
        else:
            print(json.dumps({
                'success': False,
                'message': '请使用 --force 参数确认清除缓存'
            }, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({'success': False, 'error': str(e)}, ensure_ascii=False))


def cmd_export_summary(args):
    """导出摘要"""
    client = ApifoxClient()
    try:
        content = client.export_summary(
            module=args.module,
            format=args.format
        )

        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(content)
            print(json.dumps({
                'success': True,
                'message': f'已导出到 {args.output}',
                'format': args.format
            }, ensure_ascii=False, indent=2))
        else:
            print(content)
    except Exception as e:
        print(json.dumps({'success': False, 'error': str(e)}, ensure_ascii=False))


def build_parser():
    """构建参数解析器"""
    parser = argparse.ArgumentParser(
        description='ABC 医疗云 API 文档查询工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python apifox.py read_oas                    读取完整 OpenAPI 规范
  python apifox.py list_paths --module api      列出 api 模块接口
  python apifox.py search_paths --keyword login 搜索登录相关接口
  python apifox.py get_path --path "/api/global-auth/login/sms" --method POST
  python apifox.py stats --detail               查看详细统计
  python apifox.py export_summary --module api --output api.md
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    subparsers.required = True

    # read_oas
    p = subparsers.add_parser('read_oas', help='读取完整 OpenAPI 规范')

    # refresh_oas
    p = subparsers.add_parser('refresh_oas', help='刷新最新文档')

    # list_paths
    p = subparsers.add_parser('list_paths', help='列出接口路径')
    p.add_argument('--module', help='模块过滤 (api, rpc, api-weapp 等)')
    p.add_argument('--method', help='方法过滤 (get, post, put, delete)',
                   choices=['get', 'post', 'put', 'delete', 'patch'])
    p.add_argument('--limit', type=int, help='返回数量限制')
    p.add_argument('--offset', type=int, default=0, help='偏移量')

    # search_paths
    p = subparsers.add_parser('search_paths', help='搜索接口')
    p.add_argument('--keyword', required=True, help='搜索关键词')
    p.add_argument('--module', help='模块过滤')
    p.add_argument('--method', help='方法过滤',
                   choices=['get', 'post', 'put', 'delete', 'patch'])

    # get_path
    p = subparsers.add_parser('get_path', help='获取接口详情')
    p.add_argument('--path', required=True, help='接口路径')
    p.add_argument('--method', required=True,
                   help='请求方法', choices=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
    p.add_argument('--include_refs', type=bool, default=True,
                   help='是否解析 $ref 引用 (默认: True)')

    # list_modules
    p = subparsers.add_parser('list_modules', help='列出所有模块')

    # stats
    p = subparsers.add_parser('stats', help='统计信息')
    p.add_argument('--detail', action='store_true', help='显示详细信息')

    # cache_status
    p = subparsers.add_parser('cache_status', help='查看缓存状态')

    # clear_cache
    p = subparsers.add_parser('clear_cache', help='清除缓存')
    p.add_argument('--force', action='store_true', help='强制清除')

    # export_summary
    p = subparsers.add_parser('export_summary', help='导出接口摘要')
    p.add_argument('--module', help='模块过滤')
    p.add_argument('--format', default='json',
                   choices=['json', 'markdown'], help='输出格式')
    p.add_argument('--output', help='输出文件路径')

    return parser


def main():
    """主函数"""
    parser = build_parser()
    args = parser.parse_args()

    # 命令分发
    commands = {
        'read_oas': cmd_read_oas,
        'refresh_oas': cmd_refresh_oas,
        'list_paths': cmd_list_paths,
        'search_paths': cmd_search_paths,
        'get_path': cmd_get_path,
        'list_modules': cmd_list_modules,
        'stats': cmd_stats,
        'cache_status': cmd_cache_status,
        'clear_cache': cmd_clear_cache,
        'export_summary': cmd_export_summary,
    }

    cmd_func = commands.get(args.command)
    if cmd_func:
        cmd_func(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
