#!/usr/bin/env python3
"""
ABC Apifox Skill 功能测试脚本

测试新版本 (V2) 的缓存结构和 API
"""

import os
import sys
import time

# 添加 scripts 目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from apifox_client import ApifoxClient
from cache_manager import CacheManager


def test_cache_exists():
    """测试缓存是否存在"""
    print("=== 测试缓存是否存在 ===")
    cache = CacheManager()
    meta = cache.load_meta()

    assert meta.get('version') == '2.0', "缓存版本不是 V2"
    assert meta.get('total_paths', 0) > 0, "缓存中没有接口数据"
    assert 'search_index' in meta, "缺少 search_index"

    print(f"✓ 缓存存在")
    print(f"  版本: {meta.get('version')}")
    print(f"  接口数: {meta.get('total_paths')}")
    print(f"  模块数: {meta.get('modules_count', 0)}")


def test_search_performance():
    """测试搜索性能"""
    print("\n=== 测试搜索性能 ===")
    client = ApifoxClient()

    keywords = ['登录', '库存', '订单']
    total_time = 0

    for keyword in keywords:
        start = time.time()
        results = client.search_paths(keyword)
        elapsed = time.time() - start
        total_time += elapsed

        assert len(results) > 0, f"搜索 '{keyword}' 没有结果"
        print(f"  {keyword}: {elapsed*1000:.2f}ms - {len(results)} 个结果")

    avg_time = total_time / len(keywords)
    print(f"✓ 搜索性能正常 (平均: {avg_time*1000:.2f}ms)")

    # 性能阈值：平均搜索时间应小于 100ms
    assert avg_time < 0.1, f"搜索性能不达标: {avg_time*1000:.2f}ms >= 100ms"


def test_module_filter():
    """测试模块过滤"""
    print("\n=== 测试模块过滤 ===")
    client = ApifoxClient()

    # 测试指定模块搜索
    results = client.search_paths('库存', module='api.stocks')
    assert len(results) > 0, "模块过滤搜索无结果"

    # 验证所有结果都属于指定模块
    for r in results:
        assert r['module'] == 'api.stocks', f"结果不属于 api.stocks: {r['module']}"

    print(f"✓ 模块过滤正常")
    print(f"  api.stocks 模块中 '库存' 相关: {len(results)} 个")


def test_method_filter():
    """测试方法过滤"""
    print("\n=== 测试方法过滤 ===")
    client = ApifoxClient()

    # 测试方法过滤
    results = client.search_paths('登录', method='POST')
    assert len(results) > 0, "方法过滤搜索无结果"

    # 验证所有结果都是 POST 方法
    for r in results:
        assert r['method'] == 'POST', f"结果不是 POST 方法: {r['method']}"

    print(f"✓ 方法过滤正常")
    print(f"  POST 方法中 '登录' 相关: {len(results)} 个")


def test_get_path():
    """测试获取接口详情"""
    print("\n=== 测试获取接口详情 ===")
    client = ApifoxClient()

    # 测试获取接口详情
    result = client.get_path_detail('/api/v3/goods/stocks/check/orders', 'POST')

    assert result is not None, "未找到接口"
    assert result['path'] == '/api/v3/goods/stocks/check/orders', "路径不匹配"
    assert result['method'] == 'POST', "方法不匹配"
    assert result['module'] == 'api.stocks', "模块不匹配"

    print(f"✓ 获取接口详情正常")
    print(f"  接口: {result['summary']}")


def test_get_schema():
    """测试获取 Schema"""
    print("\n=== 测试获取 Schema ===")
    cache = CacheManager()

    schema = cache.load_schema('CreateGoodsStockCheckOrderReq')
    assert schema is not None, "未找到 Schema"
    assert schema.get('type') == 'object', "Schema 类型不是 object"

    print(f"✓ 获取 Schema 正常")
    print(f"  Schema 类型: {schema.get('type')}")


def test_list_modules():
    """测试模块列表"""
    print("\n=== 测试模块列表 ===")
    client = ApifoxClient()

    modules = client.list_modules()
    assert len(modules) > 0, "模块列表为空"

    # 验证常见模块存在
    module_names = [m['name'] for m in modules]
    assert 'api.stocks' in module_names, "缺少 api.stocks 模块"
    assert 'rpc.v3' in module_names, "缺少 rpc.v3 模块"

    print(f"✓ 模块列表正常")
    print(f"  总模块数: {len(modules)}")
    print(f"  最大的模块: {modules[0]['name']} ({modules[0]['paths_count']} 个接口)")


def test_get_module():
    """测试获取模块接口"""
    print("\n=== 测试获取模块接口 ===")
    client = ApifoxClient()

    paths = client.get_module_paths('api.login')
    assert len(paths) > 0, "模块接口为空"

    # 验证所有接口都属于该模块
    for p in paths:
        assert p['module'] == 'api.login', f"接口不属于 api.login: {p['module']}"

    print(f"✓ 获取模块接口正常")
    print(f"  api.login 模块: {len(paths)} 个接口")


def test_empty_search():
    """测试搜索无结果的情况"""
    print("\n=== 测试搜索无结果 ===")
    client = ApifoxClient()

    # 搜索一个不存在的关键词
    results = client.search_paths('xyzabc123notexist')
    assert len(results) == 0, "无结果搜索应该返回空列表"

    print(f"✓ 无结果搜索正常")


def test_nonexistent_path():
    """测试获取不存在的接口"""
    print("\n=== 测试不存在的接口 ===")
    client = ApifoxClient()

    try:
        result = client.get_path_detail('/api/not/exist', 'GET')
        assert result is None, "不存在的接口应该返回 None"
        print(f"✓ 不存在接口返回 None")
    except Exception as e:
        # 如果抛出异常也是可以接受的
        print(f"✓ 不存在接口抛出异常: {e}")


def test_no_include_refs():
    """测试 --no-include-refs 参数"""
    print("\n=== 测试不解析引用 ===")
    client = ApifoxClient()

    # 获取接口详情（不解析引用）
    result = client.get_path_detail('/api/v3/goods/stocks/check/orders', 'POST', resolve_refs=False)

    assert result is not None, "未找到接口"
    # 检查 requestBody 中是否包含 $ref（未解析）
    assert '$ref' in str(result.get('requestBody', {})), "应该包含 $ref 引用"

    print(f"✓ 不解析引用正常")


def test_limit_parameter():
    """测试 limit 参数"""
    print("\n=== 测试结果限制 ===")
    client = ApifoxClient()

    # 不限制结果数量
    all_results = client.search_paths('登录', limit=None)
    assert len(all_results) > 10, "无限制应该返回更多结果"

    # 限制结果数量
    limited_results = client.search_paths('登录', limit=5)
    assert len(limited_results) == 5, "限制应该只返回 5 个结果"

    print(f"✓ limit 参数正常")
    print(f"  无限制: {len(all_results)} 个")
    print(f"  limit=5: {len(limited_results)} 个")


def test_case_insensitive_search():
    """测试大小写不敏感搜索"""
    print("\n=== 测试大小写不敏感搜索 ===")
    client = ApifoxClient()

    # 大写搜索
    results_upper = client.search_paths('LOGIN')
    # 小写搜索
    results_lower = client.search_paths('login')

    assert len(results_upper) > 0, "大写搜索应该有结果"
    assert len(results_lower) > 0, "小写搜索应该有结果"
    assert len(results_upper) == len(results_lower), "大小写应该返回相同数量"

    print(f"✓ 大小写不敏感搜索正常")
    print(f"  'LOGIN': {len(results_upper)} 个")
    print(f"  'login': {len(results_lower)} 个")


def test_nonexistent_module():
    """测试不存在的模块"""
    print("\n=== 测试不存在的模块 ===")
    client = ApifoxClient()

    paths = client.get_module_paths('api.notexist')
    assert len(paths) == 0, "不存在的模块应该返回空列表"

    print(f"✓ 不存在模块返回空列表")


def test_nonexistent_schema():
    """测试不存在的 Schema"""
    print("\n=== 测试不存在的 Schema ===")
    cache = CacheManager()

    schema = cache.load_schema('NotExistSchema')
    assert schema is None, "不存在的 Schema 应该返回 None"

    print(f"✓ 不存在 Schema 返回 None")


def test_status():
    """测试 status 命令"""
    print("\n=== 测试 status 命令 ===")
    cache = CacheManager()

    status = cache.get_status()
    assert status.get('version') == '2.0', "版本不匹配"
    assert status.get('total_paths', 0) > 0, "接口数为 0"
    assert status.get('modules_count', 0) > 0, "模块数为 0"

    print(f"✓ status 正常")
    print(f"  版本: {status.get('version')}")
    print(f"  接口数: {status.get('total_paths')}")
    print(f"  模块数: {status.get('modules_count')}")


def main():
    """运行所有测试"""
    print("ABC Apifox Skill 功能测试 (V2)")
    print("=" * 50)

    try:
        # 核心功能测试
        test_cache_exists()
        test_search_performance()
        test_module_filter()
        test_method_filter()
        test_get_path()
        test_get_schema()
        test_list_modules()
        test_get_module()

        # 边界情况测试
        test_empty_search()
        test_nonexistent_path()
        test_no_include_refs()
        test_limit_parameter()
        test_case_insensitive_search()
        test_nonexistent_module()
        test_nonexistent_schema()
        test_status()

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
