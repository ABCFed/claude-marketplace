#!/usr/bin/env python3
"""
检查环境变量和 API 连接
"""
import os
import sys

print("=" * 60)
print("Apifox 环境检查")
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

# 测试 API 连接
if token:
    print(f"\n2. API 连接测试:")
    try:
        import requests
        url = f"https://api.apifox.com/v1/projects/{project_id}/export-openapi"
        params = {"locale": "zh-CN"}
        headers = {
            "Authorization": f"Bearer {token}",
            "X-Apifox-Api-Version": "2024-03-28"
        }

        print(f"   请求 URL: {url}")
        response = requests.get(url, params=params, headers=headers, timeout=10)
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
    print(f"\n2. API 连接测试: 跳过（未设置 Token）")

print(f"\n" + "=" * 60)
print("配置方法:")
print("export APIFOX_ACCESS_TOKEN=\"你的 Apifox Access Token\"")
print("export APIFOX_PROJECT_ID=\"4105462\"  # 可选")
print("=" * 60)
