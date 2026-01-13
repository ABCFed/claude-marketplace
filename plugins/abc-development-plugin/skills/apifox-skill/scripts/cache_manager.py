#!/usr/bin/env python3
"""
缓存管理器

管理 ABC API OpenAPI 文档的本地缓存
"""

import os
import json
import time
from typing import Dict, Any, Optional
from pathlib import Path


class CacheManager:
    """缓存管理器"""

    CACHE_DIR = os.path.expanduser("~/.claude/skills/apifox-skill/cache")
    CACHE_EXPIRY = 24 * 3600  # 24 小时

    def __init__(self, cache_dir: str = None):
        """
        初始化缓存管理器

        Args:
            cache_dir: 缓存目录，默认为 ~/.claude/skills/apifox-skill/cache
        """
        self.cache_dir = cache_dir or self.CACHE_DIR
        self._ensure_cache_dir()

    def _ensure_cache_dir(self):
        """确保缓存目录存在"""
        os.makedirs(self.cache_dir, exist_ok=True)
        os.makedirs(os.path.join(self.cache_dir, "refs"), exist_ok=True)

    def is_cache_valid(self) -> bool:
        """
        检查 OAS 缓存是否有效

        Returns:
            缓存是否存在且未过期
        """
        oas_file = os.path.join(self.cache_dir, "oas.json")
        meta_file = os.path.join(self.cache_dir, "oas_meta.json")

        if not os.path.exists(oas_file) or not os.path.exists(meta_file):
            return False

        try:
            with open(meta_file, 'r', encoding='utf-8') as f:
                meta = json.load(f)

            cached_at = meta.get('cached_at', 0)
            return (time.time() - cached_at) < self.CACHE_EXPIRY
        except Exception:
            return False

    def load_oas(self) -> Optional[Dict[str, Any]]:
        """
        加载 OAS 缓存

        Returns:
            OAS 数据，如果缓存不存在或无效则返回 None
        """
        oas_file = os.path.join(self.cache_dir, "oas.json")

        if not os.path.exists(oas_file):
            return None

        try:
            with open(oas_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"加载缓存失败: {e}")
            return None

    def save_oas(self, oas_data: Dict[str, Any]):
        """
        保存 OAS 缓存

        Args:
            oas_data: OAS 数据
        """
        oas_file = os.path.join(self.cache_dir, "oas.json")
        meta_file = os.path.join(self.cache_dir, "oas_meta.json")

        try:
            with open(oas_file, 'w', encoding='utf-8') as f:
                json.dump(oas_data, f, ensure_ascii=False, indent=2)

            meta = {
                'cached_at': time.time(),
                'version': oas_data.get('info', {}).get('version', 'unknown'),
                'title': oas_data.get('info', {}).get('title', 'unknown'),
                'paths_count': len(oas_data.get('paths', {}))
            }

            with open(meta_file, 'w', encoding='utf-8') as f:
                json.dump(meta, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存缓存失败: {e}")

    def load_ref(self, ref_path: str) -> Optional[Dict[str, Any]]:
        """
        加载单个 $ref 缓存

        Args:
            ref_path: $ref 路径，如 /paths/_api_login.json

        Returns:
            引用数据，如果不存在则返回 None
        """
        # 将路径转换为安全的文件名
        safe_name = ref_path.replace('/', '_').replace('{', '').replace('}', '')
        ref_file = os.path.join(self.cache_dir, "refs", f"{safe_name}.json")

        if not os.path.exists(ref_file):
            return None

        try:
            with open(ref_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return None

    def save_ref(self, ref_path: str, data: Dict[str, Any]):
        """
        保存单个 $ref 缓存

        Args:
            ref_path: $ref 路径
            data: 引用数据
        """
        safe_name = ref_path.replace('/', '_').replace('{', '').replace('}', '')
        ref_file = os.path.join(self.cache_dir, "refs", f"{safe_name}.json")

        try:
            with open(ref_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存 ref 缓存失败: {e}")

    def clear_all(self):
        """清除所有缓存"""
        import shutil

        if os.path.exists(self.cache_dir):
            shutil.rmtree(self.cache_dir)
            self._ensure_cache_dir()
            print("缓存已清除")
        else:
            print("缓存目录不存在")

    def get_status(self) -> Dict[str, Any]:
        """
        获取缓存状态

        Returns:
            缓存状态信息
        """
        oas_file = os.path.join(self.cache_dir, "oas.json")
        meta_file = os.path.join(self.cache_dir, "oas_meta.json")
        refs_dir = os.path.join(self.cache_dir, "refs")

        status = {
            'cache_dir': self.cache_dir,
            'oas_exists': os.path.exists(oas_file),
            'meta_exists': os.path.exists(meta_file),
            'is_valid': self.is_cache_valid(),
        }

        if os.path.exists(meta_file):
            try:
                with open(meta_file, 'r', encoding='utf-8') as f:
                    meta = json.load(f)
                    status['meta'] = meta
                    cached_at = meta.get('cached_at', 0)
                    age_seconds = time.time() - cached_at
                    status['age_hours'] = age_seconds / 3600
            except Exception:
                pass

        if os.path.exists(refs_dir):
            ref_files = [f for f in os.listdir(refs_dir) if f.endswith('.json')]
            status['refs_count'] = len(ref_files)

        return status
