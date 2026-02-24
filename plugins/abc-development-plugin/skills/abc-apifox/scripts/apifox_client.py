#!/usr/bin/env python3
"""
ABC Apifox 客户端

提供 ABC 医疗云 API 文档的查询功能
使用按模块拆分的缓存结构，查询速度提升 100+ 倍
"""

import json
import os
import sys
from typing import Dict, Any, List, Optional
from cache_manager import CacheManager

try:
    import requests
except ImportError:
    print("错误: 缺少 requests 库")
    print("请运行: pip3 install requests")
    sys.exit(1)


class ApifoxClient:
    """ABC API 文档客户端"""

    APIFOX_BASE_URL = "https://api.apifox.com/v1"
    DEFAULT_PROJECT_ID = "4105462"

    def __init__(self, cache_dir: str = None):
        self.cache = CacheManager(cache_dir)

        self.access_token = os.getenv("APIFOX_ACCESS_TOKEN")
        self.project_id = os.getenv("APIFOX_PROJECT_ID", self.DEFAULT_PROJECT_ID)

        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.access_token}",
            "X-Apifox-Api-Version": "2024-03-28",
            "Content-Type": "application/json"
        })

    def check_env_vars(self) -> bool:
        """检查环境变量"""
        return bool(self.access_token)

    def _fetch_oas_from_api(self) -> Dict[str, Any]:
        """从 Apifox API 获取 OpenAPI 规范"""
        print(f"正在从 Apifox 获取项目 {self.project_id} 的 OpenAPI 文档...")
        print(f"API 端点: {self.APIFOX_BASE_URL}/projects/{self.project_id}/export-openapi")

        url = f"{self.APIFOX_BASE_URL}/projects/{self.project_id}/export-openapi"
        params = {"locale": "zh-CN"}
        body = {
            "scope": {"type": "ALL"},
            "options": {
                "includeApifoxExtensionProperties": False,
                "addFoldersToTags": False
            },
            "oasVersion": "3.1",
            "exportFormat": "JSON"
        }

        response = self.session.request("POST", url, params=params, json=body, timeout=30)
        response.raise_for_status()
        data = response.json()

        print(f"✓ 成功获取 OpenAPI 文档")
        print(f"  OpenAPI 版本: {data.get('openapi')}")
        print(f"  接口数量: {len(data.get('paths', {}))}")

        return data

    def refresh_project_oas(self) -> Dict[str, Any]:
        """刷新 OpenAPI 规范"""
        if not self.check_env_vars():
            return {'success': False, 'error': '未配置 APIFOX_ACCESS_TOKEN'}

        try:
            print("正在刷新 OpenAPI 文档...")
            oas_data = self._fetch_oas_from_api()

            # 直接导入数据
            result = self.cache.import_oas_data(oas_data)

            return {'success': True, 'message': 'OpenAPI 文档已刷新', **result}
        except Exception as e:
            return {'success': False, 'error': str(e)}

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
        result = self.cache.get_path_detail(path, method)
        if not result:
            raise Exception(f"未找到接口: {method} {path}")

        # 解析 $ref
        if resolve_refs:
            result = self._resolve_refs(result)

        return result

    def _resolve_refs(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """解析 $ref 引用"""
        if 'requestBody' in data and data['requestBody']:
            content = data['requestBody'].get('content', {}).get('application/json', {})
            if '$ref' in content.get('schema', {}):
                ref_path = content['schema']['$ref']
                schema_name = ref_path.split('/')[-1]
                schema = self.cache.load_schema(schema_name)
                if schema:
                    data['requestBody'] = {
                        'content': {
                            'application/json': {
                                'schema': schema
                            }
                        }
                    }

        if 'responses' in data:
            for response in data['responses'].values():
                content = response.get('content', {}).get('application/json', {})
                if '$ref' in content.get('schema', {}):
                    ref_path = content['schema']['$ref']
                    schema_name = ref_path.split('/')[-1]
                    schema = self.cache.load_schema(schema_name)
                    if schema:
                        response['content'] = {
                            'application/json': {
                                'schema': schema
                            }
                        }

        # 解析 parameters 中的引用
        if 'parameters' in data:
            for param in data['parameters']:
                if '$ref' in param.get('schema', {}):
                    ref_path = param['schema']['$ref']
                    schema_name = ref_path.split('/')[-1]
                    schema = self.cache.load_schema(schema_name)
                    if schema:
                        param['schema'] = schema

        return data

    def search_paths(self, keyword: str, module: str = None,
                    method: str = None, limit: int = None) -> List[Dict[str, Any]]:
        """搜索接口路径"""
        return self.cache.search_paths(keyword, module, method, limit)

    def list_modules(self) -> List[Dict[str, Any]]:
        """列出所有模块"""
        return self.cache.list_modules()

    def get_module_paths(self, module: str) -> List[Dict[str, Any]]:
        """
        列出指定模块的所有接口

        Args:
            module: 模块名，如 api.stocks

        Returns:
            接口列表
        """
        module_data = self.cache.load_module(module)
        if not module_data:
            return []

        results = []
        for path, path_item in module_data.get('paths', {}).items():
            for method, operation in path_item.items():
                results.append({
                    'path': path,
                    'method': method.upper(),
                    'module': module,
                    'summary': operation.get('summary', '')
                })
        return results

    def get_schema(self, schema_name: str) -> Optional[Dict[str, Any]]:
        """获取 Schema 定义"""
        return self.cache.load_schema(schema_name)

    def get_stats(self, detail: bool = False) -> Dict[str, Any]:
        """获取统计信息"""
        meta = self.cache.load_meta()

        stats = {
            'version': meta.get('version'),
            'total_paths': meta.get('total_paths', 0),
            'total_schemas': meta.get('total_schemas', 0),
            'modules_count': len(meta.get('modules', {})),
            'modules': meta.get('modules', {})
        }

        return stats

    def export_summary(self, module: str = None, format: str = 'json') -> str:
        """导出接口摘要"""
        if module:
            paths = self.get_module_paths(module)
        else:
            paths = []
            for mod_info in self.list_modules():
                paths.extend(self.get_module_paths(mod_info['name']))

        if format == 'markdown':
            lines = ["# ABC API 接口摘要", f"\n共 {len(paths)} 个接口\n"]
            lines.append("| 路径 | 方法 | 模块 | 描述 |")
            lines.append("|------|------|------|------|")
            for item in paths:
                lines.append(f"| {item['path']} | {item['method']} | {item['module']} | {item['summary']} |")
            return '\n'.join(lines)
        else:
            return json.dumps({'total': len(paths), 'paths': paths},
                           ensure_ascii=False, indent=2)
