#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查环境变量和 API 连接
"""
import os
import sys

print("=" * 60)
print("ABC Apifox 环境检查")
print("=" * 60)

# 检查环境变量
token = os.environ.get('APIFOX_ACCESS_TOKEN')
project_id = os.environ.get('APIFOX_PROJECT_ID', '4105462')

print(f"\n1. 环境变量:")
print(f"   APIFOX_ACCESS_TOKEN: {'✓ 已设置' if token else '✗ 未设置'}")
if token:
    print(f"   Token 长度: {len(token)} 字符")
    print(f"   Token 前缀: {token[:15]}...")
    print(f"   APIFOX_PROJECT_ID: {project_id}")

# 检查 Python 依赖
print(f"\n2. Python 依赖:")
try:
    import requests
    print(f"   ✓ requests 模块已安装 (版本: {requests.__version__})")
except ImportError:
    print(f"   ✗ requests 模块未安装")
    print(f"   安装方法: pip3 install requests")

# 检查缓存状态
print(f"\n3. 缓存状态:")
script_dir = os.path.dirname(os.path.abspath(__file__))
cache_dir = os.path.join(os.path.dirname(script_dir), "cache")
meta_file = os.path.join(cache_dir, "meta.json")

if os.path.exists(meta_file):
    try:
        import json
        with open(meta_file, 'r') as f:
            meta = json.load(f)
        print(f"   ✓ 缓存存在")
        print(f"   版本: {meta.get('version', 'unknown')}")
        print(f"   接口数: {meta.get('total_paths', 0)}")
        print(f"   模块数: {len(meta.get('modules', {}))}")
        print(f"   缓存目录: {cache_dir}")
    except Exception as e:
        print(f"   ✗ 缓存读取失败: {e}")
else:
    print(f"   ✗ 缓存不存在")
    print(f"   运行以下命令初始化: ./scripts/apifox refresh_oas")

# 测试 API 连接
if token:
    print(f"\n4. API 连接测试:")
    try:
        import requests
        url = f"https://api.apifox.com/v1/projects/{project_id}/export-openapi"
        params = {"locale": "zh-CN"}
        headers = {
            "Authorization": f"Bearer {token}",
            "X-Apifox-Api-Version": "2024-03-28",
            "Content-Type": "application/json"
        }
        body = {
            "scope": {"type": "ALL"},
            "options": {
                "includeApifoxExtensionProperties": False,
                "addFoldersToTags": False
            },
            "oasVersion": "3.1",
            "exportFormat": "JSON"
        }

        print(f"   请求 URL: {url}")
        response = requests.post(url, params=params, json=body, headers=headers, timeout=120)
        print(f"   状态码: {response.status_code}")

        if response.status_code == 200:
            try:
                data = response.json()
                print(f"   ✓ API 连接成功!")
                print(f"   OpenAPI 版本: {data.get('openapi')}")
                print(f"   接口数量: {len(data.get('paths', {}))}")
            except:
                print(f"   ✗ 响应不是 JSON 格式")
                print(f"   响应: {response.text[:100]}")
        else:
            print(f"   ✗ API 请求失败")
            print(f"   响应: {response.text[:200]}")

    except Exception as e:
        print(f"   ✗ 请求异常: {e}")
else:
    print(f"\n4. API 连接测试: 跳过（未设置 Token）")

print(f"\n" + "=" * 60)
print("配置方法:")
print("export APIFOX_ACCESS_TOKEN=\"你的 Apifox Access Token\"")
print("export APIFOX_PROJECT_ID=\"4105462\"  # 可选")
print("=" * 60)
