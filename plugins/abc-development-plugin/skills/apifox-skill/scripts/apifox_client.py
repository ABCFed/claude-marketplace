#!/usr/bin/env python3
"""
Apifox API 文档客户端

提供 ABC 医疗云 API 文档的查询功能
通过 Apifox API 获取 OpenAPI 文档数据
"""

import json
import os
import sys
from typing import Dict, Any, List, Optional
from cache_manager import CacheManager

# 尝试导入 requests，如果不存在则提示安装
try:
    import requests
except ImportError:
    print("错误: 缺少 requests 库")
    print("请运行: pip3 install requests")
    sys.exit(1)


class ApifoxClient:
    """ABC API 文档客户端"""

    # Apifox API 配置
    APIFOX_BASE_URL = "https://api.apifox.com/v1"
    DEFAULT_PROJECT_ID = "4105462"  # ABC 医疗云项目 ID

    def __init__(self, cache_dir: str = None):
        """
        初始化客户端

        Args:
            cache_dir: 缓存目录
        """
        self.cache = CacheManager(cache_dir)
        self._oas_data: Optional[Dict[str, Any]] = None
        self._index: Optional[Dict[str, Any]] = None

        # 检查环境变量
        self.access_token = os.getenv("APIFOX_ACCESS_TOKEN")
        self.project_id = os.getenv("APIFOX_PROJECT_ID", self.DEFAULT_PROJECT_ID)

        # 会话
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.access_token}",
            "X-Apifox-Api-Version": "2024-03-28",
            "Content-Type": "application/json"
        })

    def check_env_vars(self) -> bool:
        """
        检查环境变量是否已配置

        Returns:
            环境变量是否有效
        """
        if not self.access_token:
            return False
        return True

    def _make_request(self, endpoint: str, method: str = "GET",
                      params: dict = None, data: dict = None) -> Dict[str, Any]:
        """
        发送 HTTP 请求到 Apifox API

        Args:
            endpoint: API 端点
            method: HTTP 方法
            params: 查询参数
            data: 请求体数据

        Returns:
            响应 JSON 数据
        """
        url = f"{self.APIFOX_BASE_URL}{endpoint}"

        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                json=data,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Apifox API 请求失败: {e}")

    def read_project_oas(self) -> Dict[str, Any]:
        """
        读取 OpenAPI 规范

        优先从缓存读取，如果缓存无效则从 Apifox API 获取

        Returns:
            OAS 数据
        """
        # 检查环境变量
        if not self.check_env_vars():
            raise Exception(
                "未配置环境变量 APIFOX_ACCESS_TOKEN\n"
                "请设置: export APIFOX_ACCESS_TOKEN='你的 Apifox Access Token'\n"
                "可选: export APIFOX_PROJECT_ID='4105462' (默认值)"
            )

        # 尝试从缓存加载
        if self._oas_data is None:
            if self.cache.is_cache_valid():
                print("从本地缓存加载 OpenAPI 数据...")
                self._oas_data = self.cache.load_oas()
            else:
                print("缓存无效或不存在，从 Apifox API 获取...")
                self._oas_data = self._fetch_oas_from_api()
                # 保存到缓存
                self.cache.save_oas(self._oas_data)

        return self._oas_data

    def _fetch_oas_from_api(self) -> Dict[str, Any]:
        """
        从 Apifox API 获取 OpenAPI 规范

        Returns:
            OAS 数据
        """
        try:
            print(f"正在从 Apifox 获取项目 {self.project_id} 的 OpenAPI 文档...")
            print(f"API 端点: {self.APIFOX_BASE_URL}/projects/{self.project_id}/export-openapi")
            print(f"Token: {self.access_token[:20]}..." if self.access_token else "Token: (未设置)")

            # Apifox API 需要 POST 请求
            url = f"{self.APIFOX_BASE_URL}/projects/{self.project_id}/export-openapi"
            params = {"locale": "zh-CN"}

            # 请求体
            body = {
                "scope": {
                    "type": "ALL"
                },
                "options": {
                    "includeApifoxExtensionProperties": False,
                    "addFoldersToTags": False
                },
                "oasVersion": "3.1",
                "exportFormat": "JSON"
            }

            response = self.session.request(
                "POST",
                url,
                params=params,
                json=body,
                timeout=30
            )

            print(f"HTTP 状态码: {response.status_code}")
            print(f"Content-Type: {response.headers.get('Content-Type')}")

            response.raise_for_status()

            # 解析 JSON
            data = response.json()

            print(f"✓ 成功获取 OpenAPI 文档")
            print(f"  OpenAPI 版本: {data.get('openapi')}")
            print(f"  接口数量: {len(data.get('paths', {}))}")

            return data

        except Exception as e:
            raise Exception(f"从 Apifox API 获取数据失败: {e}")

    def fetch_ref_from_api(self, ref_path: str) -> Optional[Dict[str, Any]]:
        """
        从 Apifox API 获取 $ref 引用资源

        Args:
            ref_path: $ref 路径，如 /paths/_api_login.json

        Returns:
            引用数据
        """
        try:
            # Apifox API 可能不支持单个 ref 获取，这里作为占位
            # 实际可能需要从完整的 OAS 数据中提取
            print(f"获取引用: {ref_path}")
            # TODO: 实现 Apifox API 的 ref 获取逻辑
            return None
        except Exception:
            return None

    def refresh_project_oas(self) -> Dict[str, Any]:
        """
        刷新 OpenAPI 规范

        强制从 Apifox API 重新获取最新文档

        Returns:
            刷新状态
        """
        if not self.check_env_vars():
            return {
                'success': False,
                'error': '未配置 APIFOX_ACCESS_TOKEN'
            }

        try:
            print("正在刷新 OpenAPI 文档...")
            # 清除内存缓存
            self._oas_data = None
            self._index = None

            # 从 API 获取
            oas_data = self._fetch_oas_from_api()

            # 保存到缓存
            self.cache.save_oas(oas_data)

            return {
                'success': True,
                'message': 'OpenAPI 文档已刷新',
                'paths_count': len(oas_data.get('paths', {})),
                'version': oas_data.get('info', {}).get('version')
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def _load_oas(self) -> Optional[Dict[str, Any]]:
        """
        加载 OAS 数据

        Returns:
            OAS 数据
        """
        if self._oas_data is None:
            self._oas_data = self.read_project_oas()
        return self._oas_data

    def _build_index(self) -> Dict[str, Any]:
        """
        构建搜索索引

        Returns:
            索引数据
        """
        if self._index is not None:
            return self._index

        oas = self._load_oas()
        if not oas:
            return {}

        index = {
            'by_module': {},
            'by_method': {'get': [], 'post': [], 'put': [], 'delete': [], 'patch': []},
            'paths': {}
        }

        paths = oas.get('paths', {})
        for path, path_item in paths.items():
            # 提取模块名
            module = self._extract_module(path)

            if module not in index['by_module']:
                index['by_module'][module] = []

            index['by_module'][module].append(path)
            index['paths'][path] = {}

            # 遍历方法
            for method, operation in path_item.items():
                if method.lower() in index['by_method']:
                    index['by_method'][method.lower()].append({
                        'path': path,
                        'module': module,
                        'summary': operation.get('summary', '')
                    })
                    index['paths'][path][method.lower()] = {
                        'summary': operation.get('summary', ''),
                        'description': operation.get('description', ''),
                        'operation': operation
                    }

        self._index = index
        return index

    def _extract_module(self, path: str) -> str:
        """
        从路径提取模块名

        Args:
            path: API 路径

        Returns:
            模块名
        """
        parts = path.strip('/').split('/')
        if len(parts) > 0:
            return parts[0]
        return 'unknown'

    def list_paths(self, module: str = None, method: str = None,
                   limit: int = None, offset: int = 0) -> List[Dict[str, Any]]:
        """
        列出接口路径

        Args:
            module: 模块过滤 (api, rpc, api-weapp 等)
            method: 方法过滤 (get, post, put, delete)
            limit: 返回数量限制
            offset: 偏移量

        Returns:
            接口列表
        """
        index = self._build_index()
        if not index:
            raise Exception("无法加载索引数据")

        results = []

        if module:
            # 按模块过滤
            paths = index['by_module'].get(module, [])
            for path in paths:
                path_methods = index['paths'].get(path, {})
                for m, info in path_methods.items():
                    if method is None or m == method.lower():
                        results.append({
                            'path': path,
                            'method': m,
                            'module': module,
                            'summary': info.get('summary', '')
                        })
        elif method:
            # 按方法过滤
            for item in index['by_method'].get(method.lower(), []):
                results.append({
                    'path': item['path'],
                    'method': method.lower(),
                    'module': item['module'],
                    'summary': item['summary']
                })
        else:
            # 返回所有
            for path, path_methods in index['paths'].items():
                module = self._extract_module(path)
                for m, info in path_methods.items():
                    results.append({
                        'path': path,
                        'method': m,
                        'module': module,
                        'summary': info.get('summary', '')
                    })

        # 分页
        if offset > 0:
            results = results[offset:]
        if limit is not None:
            results = results[:limit]

        return results

    def search_paths(self, keyword: str, module: str = None,
                     method: str = None) -> List[Dict[str, Any]]:
        """
        搜索接口路径

        Args:
            keyword: 搜索关键词（匹配路径或描述）
            module: 模块过滤
            method: 方法过滤

        Returns:
            匹配的接口列表
        """
        index = self._build_index()
        if not index:
            raise Exception("无法加载索引数据")

        keyword_lower = keyword.lower()
        results = []

        for path, path_methods in index['paths'].items():
            path_module = self._extract_module(path)

            # 模块过滤
            if module and path_module != module:
                continue

            for m, info in path_methods.items():
                # 方法过滤
                if method and m != method.lower():
                    continue

                # 关键词匹配
                summary = info.get('summary', '')
                if (keyword_lower in path.lower() or
                    keyword_lower in summary.lower()):
                    results.append({
                        'path': path,
                        'method': m,
                        'module': path_module,
                        'summary': summary
                    })

        return results

    def get_path_detail(self, path: str, method: str,
                        resolve_refs: bool = True) -> Dict[str, Any]:
        """
        获取接口详情

        Args:
            path: 接口路径
            method: 请求方法
            resolve_refs: 是否解析 $ref 引用

        Returns:
            接口详情
        """
        oas = self._load_oas()
        if not oas:
            raise Exception("缓存数据不可用")

        paths = oas.get('paths', {})
        path_item = paths.get(path)

        if not path_item:
            raise Exception(f"未找到路径: {path}")

        method_lower = method.lower()
        operation = path_item.get(method_lower)

        if not operation:
            # 检查是否有 $ref
            if '$ref' in path_item:
                ref_path = path_item['$ref']
                return {
                    'path': path,
                    'method': method.upper(),
                    'has_ref': True,
                    'ref': ref_path,
                    'note': '此接口通过 $ref 引用定义'
                }
            raise Exception(f"未找到方法: {method} {path}")

        result = {
            'path': path,
            'method': method.upper(),
            'summary': operation.get('summary', ''),
            'description': operation.get('description', ''),
            'parameters': operation.get('parameters', []),
            'requestBody': operation.get('requestBody'),
            'responses': operation.get('responses', {}),
            'tags': operation.get('tags', []),
            'security': operation.get('security', [])
        }

        # $ref 解析暂不实现，因为 Apifox API 可能不直接支持
        # 如果需要，可以从完整的 OAS 数据中提取

        return result

    def list_modules(self) -> List[Dict[str, Any]]:
        """
        列出所有模块

        Returns:
            模块列表
        """
        index = self._build_index()
        if not index:
            raise Exception("无法加载索引数据")

        modules = []
        for module, paths in index['by_module'].items():
            # 统计该模块各方法的数量
            method_count = {'get': 0, 'post': 0, 'put': 0, 'delete': 0, 'patch': 0}
            for path in paths:
                path_methods = index['paths'].get(path, {})
                for m in path_methods.keys():
                    if m in method_count:
                        method_count[m] += 1

            modules.append({
                'name': module,
                'paths_count': len(paths),
                'method_count': method_count
            })

        # 按接口数量排序
        modules.sort(key=lambda x: x['paths_count'], reverse=True)
        return modules

    def get_stats(self, detail: bool = False) -> Dict[str, Any]:
        """
        获取统计信息

        Args:
            detail: 是否包含详细信息

        Returns:
            统计信息
        """
        oas = self._load_oas()
        if not oas:
            raise Exception("缓存数据不可用")

        paths = oas.get('paths', {})

        stats = {
            'total_paths': len(paths),
            'by_module': {},
            'by_method': {'get': 0, 'post': 0, 'put': 0, 'delete': 0, 'patch': 0}
        }

        # 统计
        for path, path_item in paths.items():
            module = self._extract_module(path)
            stats['by_module'][module] = stats['by_module'].get(module, 0) + 1

            for method in path_item.keys():
                if method.lower() in stats['by_method']:
                    stats['by_method'][method.lower()] += 1

        if detail:
            stats['info'] = oas.get('info', {})
            stats['modules_detail'] = self.list_modules()

        return stats

    def export_summary(self, module: str = None, format: str = 'json') -> str:
        """
        导出接口摘要

        Args:
            module: 模块过滤
            format: 输出格式 (json, markdown)

        Returns:
            摘要内容
        """
        paths = self.list_paths(module=module)

        if format == 'markdown':
            lines = []
            lines.append(f"# ABC API 接口摘要")
            lines.append(f"\n共 {len(paths)} 个接口\n")
            lines.append("| 路径 | 方法 | 模块 | 描述 |")
            lines.append("|------|------|------|------|")

            for item in paths:
                lines.append(f"| {item['path']} | {item['method']} | {item['module']} | {item['summary']} |")

            return '\n'.join(lines)
        else:
            return json.dumps({
                'total': len(paths),
                'paths': paths
            }, ensure_ascii=False, indent=2)
