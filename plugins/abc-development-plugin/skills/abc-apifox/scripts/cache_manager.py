#!/usr/bin/env python3
"""
ABC Apifox 缓存管理器

缓存结构:
cache/
├── meta.json              # 元数据 + 全局索引
├── modules/               # 按模块拆分的接口数据
│   ├── api.stocks.json
│   ├── rpc.advice.json
│   └── ...
└── schemas/               # Schema 定义缓存（按首字母分组）
    ├── a.json
    ├── b.json
    └── ...
"""

import os
import json
import time
from typing import Dict, Any, Optional, List
from pathlib import Path
from collections import defaultdict


class CacheManager:
    """ABC Apifox 缓存管理器"""

    @staticmethod
    def _default_cache_dir() -> str:
        """获取默认缓存目录"""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(os.path.dirname(script_dir), "cache")

    CACHE_DIR = _default_cache_dir.__func__()

    def __init__(self, cache_dir: str = None):
        self.cache_dir = cache_dir or self.CACHE_DIR
        self._ensure_cache_dirs()

    def _ensure_cache_dirs(self):
        """确保缓存目录存在"""
        os.makedirs(self.cache_dir, exist_ok=True)
        os.makedirs(os.path.join(self.cache_dir, "modules"), exist_ok=True)
        os.makedirs(os.path.join(self.cache_dir, "schemas"), exist_ok=True)

    # ========== 元数据 ==========

    def get_meta_file(self) -> str:
        """获取元数据文件路径"""
        return os.path.join(self.cache_dir, "meta.json")

    def load_meta(self) -> Dict[str, Any]:
        """加载元数据"""
        meta_file = self.get_meta_file()
        if not os.path.exists(meta_file):
            return {
                "version": "2.0",
                "created_at": None,
                "updated_at": None,
                "total_paths": 0,
                "total_schemas": 0,
                "modules": {},
                "path_to_module": {},
                "schema_storage": "grouped",
                "schema_groups": []
            }
        try:
            with open(meta_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}

    def save_meta(self, meta: Dict[str, Any]):
        """保存元数据"""
        meta_file = self.get_meta_file()
        with open(meta_file, 'w', encoding='utf-8') as f:
            json.dump(meta, f, ensure_ascii=False, indent=2)

    # ========== 模块管理 ==========

    @staticmethod
    def extract_module(path: str) -> str:
        """
        从路径提取模块名

        规则:
        - /api/v3/goods/stocks/xxx -> api.stocks
        - /rpc/advice/xxx -> rpc.advice
        """
        parts = path.strip('/').split('/')
        if len(parts) < 2:
            return 'other'

        if parts[0] == 'api':
            if len(parts) >= 4 and parts[1] == 'v3':
                return f"api.{parts[3]}"
            elif len(parts) >= 3:
                return f"api.{parts[2]}"
            return 'api'
        elif parts[0] == 'rpc':
            if len(parts) >= 2:
                return f"rpc.{parts[1]}"
            return 'rpc'
        return 'other'

    def get_module_file(self, module: str) -> str:
        """获取模块文件路径"""
        safe_name = module.replace('.', '_')
        return os.path.join(self.cache_dir, "modules", f"{safe_name}.json")

    def load_module(self, module: str) -> Optional[Dict[str, Any]]:
        """加载单个模块数据"""
        module_file = self.get_module_file(module)
        if not os.path.exists(module_file):
            return None
        try:
            with open(module_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return None

    def save_module(self, module: str, data: Dict[str, Any]):
        """保存单个模块数据"""
        module_file = self.get_module_file(module)
        with open(module_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    # ========== Schema 管理 ==========

    def _get_schema_group_file(self, schema_name: str) -> str:
        """获取 schema 分组文件路径（按首字母分组）"""
        if schema_name:
            first_char = schema_name[0].upper()
            # 只对 A-Z 字母分组，其他全部放到 _
            if not ('A' <= first_char <= 'Z'):
                first_char = '_'
        else:
            first_char = '_'
        return os.path.join(self.cache_dir, "schemas", f"{first_char.lower()}.json")

    def get_schema_file(self, schema_name: str) -> str:
        """获取 schema 文件路径（单文件格式，兼容）"""
        safe_name = schema_name.replace('/', '_').replace('{', '').replace('}', '')
        return os.path.join(self.cache_dir, "schemas", f"{safe_name}.json")

    def load_schema(self, schema_name: str) -> Optional[Dict[str, Any]]:
        """
        加载单个 schema（支持分组格式）
        """
        group_file = self._get_schema_group_file(schema_name)
        if not os.path.exists(group_file):
            return None
        try:
            with open(group_file, 'r', encoding='utf-8') as f:
                group = json.load(f)
                return group.get(schema_name)
        except Exception:
            return None

    def save_schema(self, schema_name: str, data: Dict[str, Any]):
        """保存单个 schema（单文件格式，兼容）"""
        schema_file = self.get_schema_file(schema_name)
        with open(schema_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    # ========== 查询接口 ==========

    def get_path_detail(self, path: str, method: str) -> Optional[Dict[str, Any]]:
        """
        获取接口详情（从对应的模块文件中加载）

        Args:
            path: 接口路径
            method: 请求方法

        Returns:
            接口详情，如果不存在返回 None
        """
        module = self.extract_module(path)
        module_data = self.load_module(module)

        if not module_data:
            return None

        path_item = module_data.get('paths', {}).get(path)
        if not path_item:
            return None

        operation = path_item.get(method.lower())
        if not operation:
            return None

        return {
            'path': path,
            'method': method.upper(),
            'module': module,
            'summary': operation.get('summary', ''),
            'description': operation.get('description', ''),
            'parameters': operation.get('parameters', []),
            'requestBody': operation.get('requestBody'),
            'responses': operation.get('responses', {}),
            'tags': operation.get('tags', []),
            'security': operation.get('security', [])
        }

    def search_paths(self, keyword: str, module: str = None,
                    method: str = None, limit: int = None) -> List[Dict[str, Any]]:
        """搜索接口路径"""
        meta = self.load_meta()
        keyword_lower = keyword.lower()
        results = []

        path_to_module = meta.get('path_to_module', {})

        for path, modules in path_to_module.items():
            for mod in modules:
                if module and mod != module:
                    continue

                module_data = self.load_module(mod)
                if not module_data:
                    continue

                for m, operation in module_data.get('paths', {}).get(path, {}).items():
                    if method and m.lower() != method.lower():
                        continue

                    summary = operation.get('summary', '')
                    if keyword_lower in path.lower() or keyword_lower in summary.lower():
                        results.append({
                            'path': path,
                            'method': m.upper(),
                            'module': mod,
                            'summary': summary
                        })
                        if limit and len(results) >= limit:
                            return results
        return results

    def list_modules(self) -> List[Dict[str, Any]]:
        """列出所有模块"""
        meta = self.load_meta()
        modules = []
        for name, info in meta.get('modules', {}).items():
            modules.append({
                'name': name,
                'paths_count': info.get('paths_count', 0)
            })
        return sorted(modules, key=lambda x: -x['paths_count'])

    # ========== 缓存管理 ==========

    def clear_all(self):
        """清除所有缓存"""
        import shutil
        if os.path.exists(self.cache_dir):
            shutil.rmtree(self.cache_dir)
            self._ensure_cache_dirs()
            print("缓存已清除")
        else:
            print("缓存目录不存在")

    def get_status(self) -> Dict[str, Any]:
        """获取缓存状态"""
        meta = self.load_meta()
        return {
            'version': meta.get('version', 'unknown'),
            'cache_dir': self.cache_dir,
            'total_paths': meta.get('total_paths', 0),
            'total_schemas': meta.get('total_schemas', 0),
            'modules_count': len(meta.get('modules', {})),
            'schema_storage': meta.get('schema_storage', 'unknown')
        }

    # ========== 数据导入（从 Apifox API） ==========

    def _clear_cache_dirs(self):
        """清空缓存目录（保留目录结构）"""
        modules_dir = os.path.join(self.cache_dir, "modules")
        schemas_dir = os.path.join(self.cache_dir, "schemas")

        if os.path.exists(modules_dir):
            for filename in os.listdir(modules_dir):
                filepath = os.path.join(modules_dir, filename)
                os.remove(filepath)

        if os.path.exists(schemas_dir):
            for filename in os.listdir(schemas_dir):
                filepath = os.path.join(schemas_dir, filename)
                os.remove(filepath)

    def _save_schemas_grouped(self, schemas: Dict[str, Any]):
        """保存 schemas（分组格式）"""
        schema_groups = {}
        for name, schema in schemas.items():
            if name:
                first_char = name[0].upper()
                if not ('A' <= first_char <= 'Z'):
                    first_char = '_'
            else:
                first_char = '_'

            if first_char not in schema_groups:
                schema_groups[first_char] = {}
            schema_groups[first_char][name] = schema

        schemas_dir = os.path.join(self.cache_dir, "schemas")
        for first_char, group in sorted(schema_groups.items()):
            group_file = os.path.join(schemas_dir, f"{first_char.lower()}.json")
            with open(group_file, 'w', encoding='utf-8') as f:
                json.dump(group, f, ensure_ascii=False)

    def import_oas_data(self, oas_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        导入 OpenAPI 数据

        Args:
            oas_data: OpenAPI 数据

        Returns:
            导入统计
        """
        paths = oas_data.get('paths', {})
        schemas = oas_data.get('components', {}).get('schemas', {})

        print(f"  接口数量: {len(paths)}")
        print(f"  Schema 数量: {len(schemas)}")

        # 清空旧缓存
        print("\n正在清空旧缓存...")
        self._clear_cache_dirs()

        # 初始化元数据
        meta = {
            "version": "2.0",
            "created_at": time.time(),
            "updated_at": time.time(),
            "total_paths": len(paths),
            "total_schemas": len(schemas),
            "modules": {},
            "path_to_module": {},
            "schema_storage": "grouped",
            "schema_groups": []
        }

        # 按模块组织接口
        module_paths = defaultdict(lambda: {'paths': {}, 'count': 0})

        print("\n正在按模块拆分接口...")
        for path, path_item in paths.items():
            for method, operation in path_item.items():
                if method.lower() not in ['get', 'post', 'put', 'delete', 'patch']:
                    continue

                module = self.extract_module(path)

                if path not in module_paths[module]['paths']:
                    module_paths[module]['paths'][path] = {}
                module_paths[module]['paths'][path][method] = operation
                module_paths[module]['count'] += 1

                if path not in meta['path_to_module']:
                    meta['path_to_module'][path] = []
                if module not in meta['path_to_module'][path]:
                    meta['path_to_module'][path].append(module)

        # 保存模块文件
        print("正在保存模块文件...")
        for module, data in module_paths.items():
            print(f"  {module}: {data['count']} 个接口")
            self.save_module(module, {'paths': data['paths']})
            meta['modules'][module] = {
                'paths_count': data['count']
            }

        # 保存 schemas（分组格式）
        print(f"\n正在保存 {len(schemas)} 个 Schema（分组格式）...")
        self._save_schemas_grouped(schemas)

        # 记录 schema 分组信息
        schema_groups = set()
        for name in schemas.keys():
            if name:
                first_char = name[0].upper()
                if not ('A' <= first_char <= 'Z'):
                    first_char = '_'
            else:
                first_char = '_'
            schema_groups.add(first_char)
        meta['schema_groups'] = sorted(list(schema_groups))

        # 保存元数据
        self.save_meta(meta)

        print(f"\n导入完成!")
        print(f"  模块数量: {len(module_paths)}")
        print(f"  Schema 分组数: {len(schema_groups)}")
        print(f"  Schema 总数: {len(schemas)}")

        return {
            'success': True,
            'modules_count': len(module_paths),
            'schema_groups_count': len(schema_groups),
            'schemas_count': len(schemas),
            'paths_count': len(paths)
        }
