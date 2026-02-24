---
name: abc-apifox
description: ABC 医疗云 API 文档查询工具。读取和查询 ABC API 的 OpenAPI 规范文档（5000+ 接口），支持按模块、路径、方法搜索，自动解析 $ref 引用。采用按模块拆分的缓存结构，查询速度快。使用场景：(1) 查询 API 接口定义 (2) 搜索特定功能接口 (3) 查询 Schema 定义 (4) 查看接口统计信息
---

# ABC Apifox Skill

本 skill 提供 ABC 医疗云 API 文档查询功能。

## 环境配置

### 必需的环境变量

使用前需要配置 Apifox Access Token：

```bash
# 设置 Apifox Access Token（必需）
export APIFOX_ACCESS_TOKEN="你的 Apifox Access Token"

# 设置项目 ID（可选，默认为 4105462）
export APIFOX_PROJECT_ID="4105462"
```

### 获取 Apifox Access Token

1. 登录 [Apifox](https://apifox.com)
2. 进入账号设置 > API 访问令牌
3. 创建新的访问令牌
4. 复制 Token 并配置到环境变量

### 依赖安装

```bash
# 安装 Python 依赖
pip3 install requests
```

### 工作原理

**缓存架构**：按模块拆分的缓存结构

1. **首次使用**：从 Apifox API 获取 OpenAPI 文档
2. **智能拆分**：
   - 接口按模块拆分（api.stocks、rpc.advice 等）
   - Schema 按首字母分组（A-Z + 非字母）
3. **按需加载**：查询时只加载相关模块文件
4. **缓存持久**：缓存永久有效，需要手动刷新获取最新文档

## 使用方式

```bash
./scripts/apifox <command> [参数]
```

所有命令默认返回 JSON 格式输出。

## 命令列表

### 接口查询

| 命令 | 说明 |
|------|------|
| `get_path` | 获取接口详情（自动推断模块） |
| `get_schema` | 获取 Schema 定义 |
| `search_paths` | 搜索接口（关键词匹配） |
| `list_modules` | 列出所有模块 |
| `get_module` | 获取模块的所有接口 |

### 文档管理

| 命令 | 说明 |
|------|------|
| `refresh_oas` | 刷新 OpenAPI 文档 |
| `status` | 查看缓存状态 |
| `clear_cache` | 清除本地缓存（需要 `--force`） |

## 使用示例

### 获取接口详情

```bash
# 获取接口详情（自动推断模块）
./scripts/apifox get_path \
    --path "/api/v3/goods/stocks/check/orders" \
    --method POST

# 获取接口并解析 $ref 引用
./scripts/apifox get_path \
    --path "/api/v3/goods/stocks/check/orders" \
    --method POST \
    --include_refs true
```

### 获取 Schema 定义

```bash
# 获取 Schema 定义
./scripts/apifox get_schema --name CreateGoodsStockCheckOrderReq
```

### 搜索接口

```bash
# 搜索盘点相关接口
./scripts/apifox search_paths --keyword "盘点"

# 搜索特定模块的接口
./scripts/apifox search_paths --keyword "库存" --module api.stocks

# 按方法过滤
./scripts/apifox search_paths --keyword "order" --method POST --limit 10
```

### 模块查询

```bash
# 列出所有模块
./scripts/apifox list_modules

# 获取特定模块的所有接口
./scripts/apifox get_module --module api.stocks
```

### 文档管理

```bash
# 查看缓存状态
./scripts/apifox status

# 刷新文档（从 Apifox 获取最新数据）
./scripts/apifox refresh_oas

# 清除缓存
./scripts/apifox clear_cache --force
```

## 输出格式

所有命令返回 JSON 格式：

```json
{
  "success": true,
  "data": "返回的数据"
}
```

错误时返回：

```json
{
  "success": false,
  "error": "错误信息"
}
```

## Claude 使用方式

当用户需要查询 API 文档时：

1. **理解需求**：确定要查询的接口或 Schema
2. **构建命令**：根据需求选择合适的命令
3. **执行脚本**：使用 Bash 工具运行
4. **分析结果**：解析返回的接口/Schema 定义

示例工作流：
```
用户: "查看盘点单接口的定义"

Claude:
1. ./scripts/apifox search_paths --keyword "盘点"
2. 从结果中找到相关接口路径
3. ./scripts/apifox get_path --path "/api/v3/goods/stocks/check/orders" --method POST
4. 分析返回的请求体 CreateGoodsStockCheckOrderReq
5. 如需查看 Schema: ./scripts/apifox get_schema --name CreateGoodsStockCheckOrderReq
```

## 缓存结构

```
cache/
├── meta.json              # 元数据 + 全局索引
├── modules/               # 按模块拆分的接口数据
│   ├── api.stocks.json    # 库存相关接口
│   ├── rpc.advice.json    # 医嘱相关接口
│   └── ...
└── schemas/               # Schema 定义缓存（按首字母分组）
    ├── a.json             # A 开头的 Schema
    ├── b.json
    ├── ...
    └── _.json             # 非字母开头的 Schema（中文、数字等）
```

## 模块命名规则

| 路径格式 | 模块名 | 示例 |
|---------|-------|------|
| `/api/v3/goods/stocks/xxx` | `api.stocks` | 库存模块 |
| `/rpc/advice/xxx` | `rpc.advice` | 医嘱模块 |
| `/api/global-auth/xxx` | `api.global-auth` | 认证模块 |

## 文件结构

```
scripts/
├── apifox              # 命令行工具入口
├── apifox.py           # Python CLI 实现
├── apifox_client.py    # 客户端
└── cache_manager.py    # 缓存管理器
```

## 首次使用

```bash
# 配置环境变量后首次运行
./scripts/apifox status

# 自动从 Apifox 获取文档并建立缓存
# 正在从 Apifox 获取项目 4105462 的 OpenAPI 文档...
# 正在清空旧缓存...
# 正在按模块拆分接口...
# 正在保存 Schema（分组格式）...
# 导入完成!
```
