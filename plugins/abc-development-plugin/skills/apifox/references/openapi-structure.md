# OpenAPI 文档结构说明

## 概述

ABC 医疗云 API 文档采用 OpenAPI 3.1.0 规范，包含 4209 个接口定义。

## 文档结构

```json
{
  "openapi": "3.1.0",
  "info": {
    "title": "默认模块",
    "version": "1.0.0",
    "x-download-time": "2025-12-30T08:33:20.634Z"
  },
  "paths": {
    "/api/global-auth/login/sms": {
      "post": {
        "summary": "短信验证码登录",
        "parameters": [...],
        "requestBody": {...},
        "responses": {...}
      }
    }
  },
  "components": {
    "schemas": {...},
    "securitySchemes": {...}
  }
}
```

## $ref 引用机制

OpenAPI 规范使用 `$ref` 引用来组织文档结构：

```json
{
  "paths": {
    "/api/endpoint": {
      "$ref": "/paths/_api_endpoint.json"
    }
  }
}
```

引用文件包含完整的接口定义，包括：
- 请求参数（路径参数、查询参数、请求头）
- 请求体（requestBody）结构和 schema
- 响应定义（responses）和状态码
- 安全认证要求（security）

## 接口分类

### 按路径前缀分类

- `/api/*` - 标准 HTTP API（2506 个）
- `/rpc/*` - RPC 服务接口（1338 个）
- `/api-weapp/*` - 小程序专用接口（294 个）
- `/api-device/*` - 设备接口（29 个）
- `/api-mp/*` - 公众号接口（17 个）
- `/api-external/*` - 外部接口（14 个）

### 按业务模块分类

主要业务模块包括：

| 模块 | 路径前缀 | 说明 |
|------|---------|------|
| global-auth | /api/global-auth | 全局认证登录 |
| cms | /api/v3/cms | 内容管理系统 |
| message | /api/v2/message | 消息服务 |
| promotions | /api/v2/promotions | 促销营销 |
| clinics | /rpc/v3/clinics | 诊所管理 |
| patients | /api/v2/patients | 患者管理 |
| ... | ... | 更多业务模块 |

## 请求方法

支持的 HTTP 方法：

| 方法 | 说明 | 接口数量 |
|------|------|---------|
| GET | 查询资源 | ~1850 |
| POST | 创建资源 | ~1530 |
| PUT | 更新资源 | ~420 |
| DELETE | 删除资源 | ~409 |
| PATCH | 部分更新 | 少量 |

## 数据类型

### Schema 类型

OpenAPI 支持的数据类型：

- `string` - 字符串
- `integer` - 整数
- `number` - 数字（整数或浮点数）
- `boolean` - 布尔值
- `array` - 数组
- `object` - 对象

### 格式约束

常见格式修饰符：

- `format: date` - 日期 YYYY-MM-DD
- `format: date-time` - 日期时间 ISO 8601
- `format: email` - 邮箱地址
- `format: uri` - URI 地址
- `format: binary` - 二进制数据
- `format: byte` - Base64 编码字符串

## 认证方式

### Bearer Token

```http
Authorization: Bearer {token}
```

### API Key

```http
X-API-Key: {api_key}
```

## 分页和过滤

### 分页参数

```json
{
  "page": 1,
  "page_size": 20,
  "total": 100
}
```

### 排序

```json
{
  "sort_by": "created_at",
  "sort_order": "desc"
}
```

## 错误响应

### 标准错误格式

```json
{
  "code": "ERROR_CODE",
  "message": "错误描述",
  "details": {...}
}
```

### HTTP 状态码

| 状态码 | 说明 |
|--------|------|
| 200 | 成功 |
| 201 | 创建成功 |
| 400 | 请求参数错误 |
| 401 | 未认证 |
| 403 | 无权限 |
| 404 | 资源不存在 |
| 500 | 服务器错误 |
