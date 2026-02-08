# 后端调试排查指南

## 排查思路总览

### 有 traceId 的情况
1. 直接用 `X-B3-TraceId` 查询全链路日志
2. 按 `__topic__` 过滤关注的服务
3. 按 `level` 过滤查看 ERROR/WARN

### 无 traceId 的情况
1. 获取大致时间范围
2. 用 `chainId` + 接口关键字定位网关日志
3. 从网关日志获取 `X-B3-TraceId`
4. 用 traceId 追踪完整链路

### 线上问题排查
1. 确认环境：上海 prod 还是杭州 prod
2. **两个区域都要查看**，避免遗漏
3. 优先查网关日志定位 traceId
4. 再查具体业务服务的详细日志

## 1. 从哪里获取 traceId

| 方式 | 说明 |
|------|------|
| 通过网关日志 | 前端请求一定会携带时间戳，用时间范围 + `chainId` + 接口关键字在 gateway 日志中定位到具体请求，即可获得 traceId |
| 直接查看日志 | 后端每行日志都包含 `[traceId]`，通过关键字、异常堆栈等搜索日志即可获得 |

## 2. 使用 SLS 查询日志

ABC 后端日志统一存储在阿里云 SLS（日志服务）中。

> 如果安装了 `abc-be-sls` SKILL，可以通过 MCP 工具直接查询 SLS 日志，包含更详细的环境配置、查询语法和日志解析工具。

### SLS 环境配置

| 环境 | Endpoint | Project | Logstore | 说明 |
|------|----------|---------|----------|------|
| 开发 | cn-shanghai.log.aliyuncs.com | abc-cis-log | dev | 正常日志（短期约 3 天） |
| 开发 | cn-shanghai.log.aliyuncs.com | abc-cis-log | dev_longtime | 长日志（长期约半年） |
| 测试 | cn-shanghai.log.aliyuncs.com | abc-cis-log | test | 正常日志 |
| 测试 | cn-shanghai.log.aliyuncs.com | abc-cis-log | test_longtime | 长日志 |
| 正式（上海） | cn-shanghai.log.aliyuncs.com | abc-cis-log | prod | 正常日志 |
| 正式（上海） | cn-shanghai.log.aliyuncs.com | abc-cis-log | prod_longtime | 长日志 |
| 正式（杭州） | cn-hangzhou.log.aliyuncs.com | abc-cis-log-hangzhou | prod | 正常日志 |
| 正式（杭州） | cn-hangzhou.log.aliyuncs.com | abc-cis-log-hangzhou | prod_longtime | 长日志 |

> **注意**：排查线上问题时，上海和杭州的 prod 都需要查看，避免遗漏。

### 关键字段

| 字段 | 有索引 | 说明 |
|------|--------|------|
| `X-B3-TraceId` | 是 | 链路追踪 ID，贯穿整个请求链路，排查问题的核心线索 |
| `__topic__` | 是 | 服务名，格式为 `abc-{业务线}-{业务名}-service` |
| `level` | 是 | 日志级别：INFO、WARN、ERROR |
| `location` | 是 | 代码位置：`类名.方法名(文件:行号)` |
| `throwable` | 是 | 完整的 Java 异常堆栈信息 |
| `message-index` | 是 | 有索引的消息内容，网关日志默认打印到此字段 |
| `message-no-index` | 否 | 无索引的消息内容，业务服务日志默认打印到此字段 |

### 常用查询场景

```
# 通过 traceId 查全链路
X-B3-TraceId: 882f6c2aa504c5ef

# 按服务名过滤（替换为实际服务名）
__topic__: abc-cis-{service}-service

# 查某个服务的 ERROR 日志
__topic__: abc-cis-{service}-service and level: ERROR

# 通过异常堆栈搜索
throwable: NullPointerException

# 按代码位置过滤
location: PatientService.getById
```

### 排查流程

**有 traceId**：直接用 `X-B3-TraceId` 查询 → 按 `__topic__` 过滤服务 → 按 `level` 过滤 ERROR/WARN

**无 traceId**：获取时间范围 → 用 `__topic__` + 关键字定位网关日志 → 从网关日志获取 traceId → 追踪完整链路

