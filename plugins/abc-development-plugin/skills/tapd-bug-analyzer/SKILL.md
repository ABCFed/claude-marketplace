# TAPD Bug Analyzer Skill

自动化分析和定位 TAPD Bug 单中的问题，支持多种分析策略。

## Usage

```
/tapd-bug <bug_url> [--env <environment>] [--region <region>]
```

### Parameters
- `bug_url`: 必填，TAPD Bug 单链接（如：https://www.tapd.cn/xxxxx/bugtrace/bugs/view/xxxxxx）
- `--env`: 可选，环境名称：dev/test/prod（默认根据 URL 自动判断）
- `--region`: 可选，地域：shanghai/hangzhou（默认 shanghai）

## Instructions

当用户调用此 skill 时，按以下步骤执行：

### Step 1: 解析 TAPD Bug 链接

从 Bug 链接中提取 workspace_id 和 bug_id：

```
URL 格式: https://www.tapd.cn/{workspace_id}/bugtrace/bugs/view/{bug_id}
示例: https://www.tapd.cn/12345678/bugtrace/bugs/view/1012345678001234567
```

### Step 2: 获取 Bug 详情

使用 TAPD MCP 工具获取 Bug 单详细信息：

```
调用 mcp__mcp-server-tapd__get_bug 工具：
- workspace_id: 从 URL 解析得到
- options: {"id": "<bug_id>", "fields": "id,title,description,status,severity,priority,reporter,current_owner,created,modified"}
```

### Step 3: 分析 Bug 描述，选择分析策略

仔细阅读 Bug 描述（description 字段），按优先级选择分析策略：

#### 策略 A: 包含 traceId
检测 Bug 描述中是否包含 traceId（通常是 16 位十六进制字符串）：
- 正则匹配: `[a-f0-9]{16}`
- 常见格式: `traceId: xxx`, `trace_id=xxx`, `X-B3-TraceId: xxx`

如果找到 traceId，直接调用 sls-trace-analyzer：
```bash
~/.claude/skills/sls-trace-analyzer/.venv/bin/python \
  ~/.claude/skills/sls-trace-analyzer/sls-query.py \
  --trace-id "<traceId>" \
  --region "<region>" \
  --env "<env>"
```

> **说明**: 脚本默认同时查询普通存储和长期存储两个 logstore，以获取完整日志。

#### 策略 B: 包含请求 URL（带时间戳）
检测 Bug 描述中是否包含 API 请求 URL：
- URL 模式: `http(s)://xxx.abczs.cn/api/...`
- 时间戳参数: URL 末尾的 13 位数字（毫秒时间戳）

示例 URL:
```
http://32.ftest.abczs.cn/api/v2/patientorders/his/ffffffff0000000035246dd0adec0000/hospital?1768198926187
```

如果找到带时间戳的 URL，直接调用 sls-trace-analyzer（URL 模式）：
```bash
~/.claude/skills/sls-trace-analyzer/.venv/bin/python \
  ~/.claude/skills/sls-trace-analyzer/sls-query.py \
  --url "<完整URL含时间戳>"
```

sls-trace-analyzer 会自动：
1. 解析 URL 中的域名、路径、时间戳
2. 根据域名判断环境（dev/test/prod）和地域
3. 查询网关日志获取 traceId
4. 使用 traceId 查询完整调用链日志
5. 输出日志分析结果

#### 策略 C: 无 traceId 也无时间戳
基于 Bug 描述进行代码分析：
1. 提取关键信息（错误消息、功能模块、操作步骤）
2. 使用 codebase-retrieval 搜索相关代码
3. 分析业务逻辑，推断问题原因

### Step 4: 日志分析与问题定位

获取到 traceId 后，调用 sls-trace-analyzer 进行深度分析：

1. **识别错误和异常**
   - 查找 ERROR、WARN 级别的日志
   - 识别 Java 异常堆栈（Exception、Caused by）
   - 提取错误消息和错误码

2. **追踪请求链路**
   - 按时间排序日志条目
   - 识别请求入口（Controller）和出口
   - 标记 RPC/Feign 调用和响应

3. **定位代码问题**
   - 从异常堆栈提取类名和行号
   - 优先关注 `cn.abcyun` 包下的代码
   - 使用 codebase-retrieval 查找对应代码

### Step 5: 输出分析报告

生成结构化的分析报告：

```markdown
## TAPD Bug 分析报告

### Bug 基本信息
- **Bug ID**: xxx
- **标题**: xxx
- **状态**: xxx
- **严重程度**: xxx
- **报告人**: xxx
- **处理人**: xxx

### 分析策略
- 使用策略: A/B/C
- TraceId: xxx（如有）
- 请求时间: xxx（如有）

### 错误摘要
- **错误类型**: xxx
- **错误消息**: xxx
- **发生位置**: `文件路径:行号`

### 调用链路
1. [入口] POST /api/xxx
2. [Service] XxxService.method()
3. [RPC] 调用 xxx 服务
4. [Error] 发生异常

### 问题定位
- **根因分析**: xxx
- **相关代码**:
  ```java
  // 问题代码片段
  ```

### 修复建议
1. xxx
2. xxx
```

## Examples

### 示例 1: Bug 描述中包含 traceId

```bash
/tapd-bug https://www.tapd.cn/12345678/bugtrace/bugs/view/1012345678001234567
```

Bug 描述内容：
```
用户反馈下单失败，错误信息：系统繁忙，请稍后重试
traceId: 8989a698c36e5189
```

执行流程：
1. 解析 URL 获取 workspace_id=12345678, bug_id=1012345678001234567
2. 调用 TAPD MCP 获取 Bug 详情
3. 从描述中提取 traceId: 8989a698c36e5189
4. 调用 sls-trace-analyzer 分析日志
5. 输出分析报告

### 示例 2: Bug 描述中包含请求 URL

```bash
/tapd-bug https://www.tapd.cn/12345678/bugtrace/bugs/view/1012345678001234568 --env test
```

Bug 描述内容：
```
测试环境下单接口报错 500
请求地址：http://32.ftest.abczs.cn/api/v2/patientorders/his/ffffffff0000000035246dd0adec0000/hospital?1768198926187
```

执行流程：
1. 解析 URL 获取 workspace_id 和 bug_id
2. 调用 TAPD MCP 获取 Bug 详情
3. 从描述中提取请求 URL（含时间戳）
4. 调用 sls-trace-analyzer（URL 模式）进行日志分析
5. 输出分析报告

### 示例 3: 纯文字描述的 Bug

```bash
/tapd-bug https://www.tapd.cn/12345678/bugtrace/bugs/view/1012345678001234569
```

Bug 描述内容：
```
患者在门诊缴费时，选择医保支付后点击确认，页面提示"医保结算失败"，
但实际上 HIS 系统显示已经结算成功。
复现步骤：
1. 登录患者端 APP
2. 选择待缴费订单
3. 选择医保支付
4. 点击确认支付
预期结果：支付成功，跳转到支付成功页面
实际结果：提示"医保结算失败"
```

执行流程：
1. 解析 URL 获取 workspace_id 和 bug_id
2. 调用 TAPD MCP 获取 Bug 详情
3. 未找到 traceId 或时间戳
4. 分析描述提取关键词：门诊缴费、医保支付、医保结算
5. 使用 codebase-retrieval 搜索相关代码
6. 分析业务逻辑，推断可能原因
7. 输出分析报告

### 示例 4: 实际案例 - 处方不展示规格

**输入**:
```bash
/tapd-bug https://www.tapd.cn/43780818/bugtrace/bugs/view/1143780818001109821
```

**Bug 描述内容**:
```
问题概述：处方不展示规格
门店id: ffffffff000000003526121e726a0004
收费单id：ffffffff000000003526dc97b673c003
补充说明：后台没返回药品档案的规格
```

**执行流程**:
1. 解析 URL: workspace_id=43780818, bug_id=1143780818001109821
2. 调用 TAPD MCP 获取 Bug 详情
3. 分析描述：无 traceId，无时间戳 URL → 使用策略 C
4. 提取关键词：处方、规格、药品档案
5. 使用 codebase-retrieval 搜索相关代码
6. 定位到 PrescriptionService.java:678-680

**问题定位结果**:
```java
// PrescriptionService.java:678-680
if (goodsItem.getType() == 2) {
    prescriptionFormItem.setSpecification(...);
}
```

**根因分析**:
西药处方的 specification 字段只在 type==2（材料）时设置，普通西药（type=1）未设置规格。

**修复建议**:
为所有类型药品设置规格，优先使用 GoodsItem.displaySpec 字段。
