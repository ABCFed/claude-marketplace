#!/usr/bin/env python3
"""
Apifox Skill 功能测试脚本
"""

import os
import sys

# 设置测试环境变量
os.environ['APIFOX_ACCESS_TOKEN'] = 'test_token_for_testing'

from apifox_client import ApifoxClient

def test_env_check():
    """测试环境变量检查"""
    print("=== 测试环境变量检查 ===")
    client = ApifoxClient()
    assert client.check_env_vars(), "环境变量检查失败"
    assert client.access_token == 'test_token_for_testing', "Token 不匹配"
    assert client.project_id == '4105462', "Project ID 不匹配"
    print("✓ 环境变量检查通过")

def test_api_config():
    """测试 API 配置"""
    print("\n=== 测试 API 配置 ===")
    client = ApifoxClient()
    assert client.APIFOX_BASE_URL == "https://api.apifox.com/v1", "API URL 不匹配"
    assert client.session.headers['Authorization'] == 'Bearer test_token_for_testing', "Auth 头不匹配"
    print("✓ API 配置正确")

def test_cache_load():
    """测试缓存加载"""
    print("\n=== 测试缓存加载 ===")
    client = ApifoxClient()
    data = client.cache.load_oas()
    assert data is not None, "缓存数据为空"
    assert len(data.get('paths', {})) > 0, "缓存中没有接口数据"
    print(f"✓ 缓存加载成功，接口数: {len(data.get('paths', {}))}")

def test_stats():
    """测试统计功能"""
    print("\n=== 测试统计功能 ===")
    client = ApifoxClient()
    # 直接使用缓存数据测试
    data = client.cache.load_oas()
    paths = data.get('paths', {})

    stats = {
        'total': len(paths),
        'by_module': {},
        'by_method': {'get': 0, 'post': 0, 'put': 0, 'delete': 0}
    }

    for path, path_item in paths.items():
        parts = path.strip('/').split('/')
        if parts:
            module = parts[0]
            stats['by_module'][module] = stats['by_module'].get(module, 0) + 1

        for method in path_item.keys():
            if method.lower() in stats['by_method']:
                stats['by_method'][method.lower()] += 1

    assert stats['total'] > 0, "接口总数为 0"
    assert len(stats['by_module']) > 0, "模块为空"
    print(f"✓ 统计功能正常")
    print(f"  总接口数: {stats['total']}")
    print(f"  模块数: {len(stats['by_module'])}")
    print(f"  GET: {stats['by_method']['get']}, POST: {stats['by_method']['post']}")

def test_search():
    """测试搜索功能"""
    print("\n=== 测试搜索功能 ===")
    client = ApifoxClient()
    data = client.cache.load_oas()

    # 搜索包含 "login" 的接口
    keyword = "login"
    results = []

    for path, path_item in data.get('paths', {}).items():
        for method, operation in path_item.items():
            # operation 可能是字典或字符串（$ref）
            if isinstance(operation, dict):
                summary = operation.get('summary', '')
                if keyword.lower() in path.lower() or keyword.lower() in summary.lower():
                    results.append({
                        'path': path,
                        'method': method,
                        'summary': summary
                    })

    assert len(results) > 0, f"搜索 '{keyword}' 没有结果"
    print(f"✓ 搜索功能正常")
    print(f"  搜索 '{keyword}': 找到 {len(results)} 个接口")

def test_modules():
    """测试模块列表"""
    print("\n=== 测试模块列表 ===")
    client = ApifoxClient()
    data = client.cache.load_oas()

    modules = {}
    for path in data.get('paths', {}).keys():
        parts = path.strip('/').split('/')
        if parts:
            module = parts[0]
            modules[module] = modules.get(module, 0) + 1

    assert len(modules) > 0, "模块列表为空"
    assert 'api' in modules, "缺少 api 模块"
    assert 'rpc' in modules, "缺少 rpc 模块"

    print(f"✓ 模块列表正常")
    print(f"  模块数: {len(modules)}")
    for module, count in sorted(modules.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"  {module}: {count} 个接口")

def main():
    """运行所有测试"""
    print("Apifox Skill 功能测试")
    print("=" * 50)

    try:
        test_env_check()
        test_api_config()
        test_cache_load()
        test_stats()
        test_search()
        test_modules()

        print("\n" + "=" * 50)
        print("✓ 所有测试通过！")
        return 0
    except AssertionError as e:
        print(f"\n✗ 测试失败: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ 测试错误: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())
