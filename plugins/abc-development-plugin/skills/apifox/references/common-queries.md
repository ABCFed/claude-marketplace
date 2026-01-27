# 常见查询示例

## 认证相关

### 查询所有登录接口

```bash
python apifox.py search_paths --keyword "login"
```

### 获取短信登录接口详情

```bash
python apifox.py get_path \
    --path "/api/global-auth/login/sms" \
    --method POST
```

### 查询小程序登录接口

```bash
python apifox.py search_paths --keyword "login weapp"
```

## 用户管理

### 查询用户相关接口

```bash
python apifox.py search_paths --keyword "user" --module api
```

### 查询患者管理接口

```bash
python apifox.py search_paths --keyword "patient"
```

## 诊所管理

### 查询诊所相关 RPC 接口

```bash
python apifox.py list_paths --module rpc --limit 50 | grep -i clinic
```

### 查询诊所切换接口

```bash
python apifox.py search_paths --keyword "switch-clinic"
```

## 消息服务

### 查询短信发送接口

```bash
python apifox.py search_paths --keyword "sms send"
```

### 查询消息模板接口

```bash
python apifox.py search_paths --keyword "template"
```

## 营销促销

### 查询卡券管理接口

```bash
python apifox.py search_paths --keyword "card"
```

### 查询促销活动接口

```bash
python apifox.py search_paths --keyword "promotions"
```

## 按方法查询

### 列出所有 POST 接口

```bash
python apifox.py list_paths --method post --limit 50
```

### 列出所有 GET 接口

```bash
python apifox.py list_paths --method get --limit 50
```

## 按模块查询

### 列出小程序接口

```bash
python apifox.py list_paths --module api-weapp --limit 50
```

### 列出 RPC 接口

```bash
python apifox.py list_paths --module rpc --limit 50
```

### 列出设备接口

```bash
python apifox.py list_paths --module api-device
```

## 统计分析

### 查看接口统计

```bash
python apifox.py stats --detail
```

### 查看各模块分布

```bash
python apifox.py list_modules
```

## 导出文档

### 导出 API 模块摘要为 Markdown

```bash
python apifox.py export_summary \
    --module api \
    --output api_summary.md \
    --format markdown
```

### 导出所有接口摘要为 JSON

```bash
python apifox.py export_summary \
    --output full_summary.json \
    --format json
```

## 缓存管理

### 查看缓存状态

```bash
python apifox.py cache_status
```

### 刷新 API 文档缓存

```bash
# 步骤 1: 检查缓存状态
python apifox.py cache_status

# 步骤 2: 如果需要刷新，由 Claude 调用 MCP 工具
# mcp__ABC____-_API_____read_project_oas_ivgmlc

# 步骤 3: 验证刷新结果
python apifox.py cache_status
```

### 清除缓存

```bash
python apifox.py clear_cache --force
```

## 实用组合命令

### 查找特定功能的所有接口

```bash
# 1. 先搜索关键词
python apifox.py search_paths --keyword "appointment"

# 2. 对找到的接口获取详情
python apifox.py get_path --path "/api/v2/appointments" --method GET
```

### 分析某个模块的所有接口

```bash
# 1. 列出模块所有接口
python apifox.py list_paths --module api --limit 1000

# 2. 导出为文件
python apifox.py export_summary --module api --output api_full.md
```

### 查找特定业务的所有 POST 接口

```bash
python apifox.py search_paths --keyword "order" --method post
```

## Claude 工作流示例

### 场景：查找用户注册相关接口

```bash
# Step 1: 搜索注册相关接口
python apifox.py search_paths --keyword "register"

# Step 2: 获取具体接口详情
python apifox.py get_path --path "/api/global-auth/login/sms-register" --method POST

# Step 3: 分析请求参数和响应结构
# 从返回的 JSON 中提取：
# - requestBody: 请求参数结构
# - responses: 响应状态码和数据结构
# - parameters: URL 参数
```

### 场景：导出小程序完整文档

```bash
# Step 1: 获取所有小程序接口
python apifox.py list_paths --module api-weapp --limit 500 > weapp_paths.json

# Step 2: 导出为 Markdown 文档
python apifox.py export_summary \
    --module api-weapp \
    --output weapp_api.md \
    --format markdown
```

### 场景：分析某个接口的完整定义

```bash
# 获取完整接口定义（解析所有 $ref）
python apifox.py get_path \
    --path "/api/v2/patients" \
    --method POST \
    --include_refs true > patient_create_full.json

# 使用 jq 格式化输出
python apifox.py get_path \
    --path "/api/v2/patients" \
    --method POST | jq '.data.requestBody'
```
