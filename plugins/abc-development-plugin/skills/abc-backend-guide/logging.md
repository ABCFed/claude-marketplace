# 日志打印规范

## 1. 基本用法

```java
@Slf4j  // Lombok 注解，自动生成 log 对象
public class XxxService {

    public void doSomething(String id) {
        log.info("开始处理, id={}", id);

        try {
            // 业务逻辑
        } catch (Exception e) {
            log.error("处理失败, id={}", id, e);  // 最后一个参数是异常对象
            throw e;
        }
    }
}
```

## 2. 日志级别

| 级别 | 用途 | 示例 |
|------|------|------|
| `ERROR` | 需要立即关注的错误 | 数据库连接失败、NPE |
| `WARN` | 潜在问题但不影响主流程 | 降级处理、重试 |
| `INFO` | 关键业务节点 | 接口调用、状态变更 |
| `DEBUG` | 调试信息（生产环境通常关闭） | 变量值、SQL 参数 |

## 3. AbcLogMarker 日志标记

通过 `AbcLogMarker`（`cn.abcyun.common.log.marker.AbcLogMarker`）可以控制日志写入的目标字段和存储桶：

| 常量 | Marker 值 | 有索引 | 用途 |
|------|----------|--------|------|
| `MARKER_MESSAGE_INDEX` | `message-index` | 是 | 写入正常桶的有索引字段 |
| `MARKER_MESSAGE_NO_INDEX` | `message-no-index` | 否 | 写入正常桶的无索引字段（默认行为） |
| `MARKER_LONG_TIME` | `longtime` | 是 | 写入长日志桶（长期存储约半年，带索引） |
| `MARKER_MESSAGE_AMQP` | `message-amqp` | - | AMQP 消息日志 |

```java
import cn.abcyun.common.log.marker.AbcLogMarker;

// 写入有索引字段（可搜索）
log.info(AbcLogMarker.MARKER_MESSAGE_INDEX, "关键业务信息: {}", args);

// 写入长日志桶（长期存储）
log.info(AbcLogMarker.MARKER_LONG_TIME, "需要长期保留的日志: {}", args);

// 默认行为：写入无索引字段
log.info("普通日志: {}", args);
```

> **何时使用**：
> - `MARKER_MESSAGE_INDEX`：需要在 SLS 中通过关键词搜索定位的关键业务日志
> - `MARKER_LONG_TIME`：需要长期追溯的关键操作记录（正常日志桶仅保留约 3 天）

## 4. @LogReqAndRsp 注解

`@LogReqAndRsp` 注解用于自动记录接口的请求参数和响应结果，日志打印到 `message-index`（有索引）。

```java
@LogReqAndRsp                        // 自动记录请求和响应
@LogReqAndRsp(longTimeLog = true)    // 同时写入长期存储日志桶（保留约半年）
```

使用建议：
- **前期新接口一般都会加上**，方便问题定位和排查
- 后续接口稳定、访问量起来以后可以再删掉（减少日志成本）
- Controller 层的写操作接口（创建、更新、删除）
- RPC Controller 的接口方法

## 5. 日志存储：正常日志 vs 长日志

SLS 中存在两种日志存储桶：

| 类型 | 保留时间 | Logstore 命名 | 说明 |
|------|---------|---------------|------|
| 正常日志 | 短期（约 3 天） | `dev` / `test` / `prod` | 默认写入 |
| 长日志 | 长期（约半年） | `dev_longtime` / `test_longtime` / `prod_longtime` | 需要通过 `longTimeLog = true` 写入 |

### 各环境长日志桶

| 环境 | Logstore |
|------|----------|
| 开发 | `dev_longtime` |
| 测试 | `test_longtime` |
| 正式（上海） | `prod_longtime` |
| 正式（杭州） | `prod_longtime` |

> 使用 `@LogReqAndRsp(longTimeLog = true)` 的接口日志会同时写入正常桶和长日志桶。**长日志只有重要逻辑才会加上**，开发过程中一般不会主动增加，只有后续发现业务逻辑经常需要排查问题且非常关键时才增加。

## 6. 日志规范

- **一般不主动打印 INFO 以上等级的日志**，避免日志量过大导致成本问题
- 使用 `{}` 占位符，不要用字符串拼接
- ERROR 日志必须带上异常对象 `e`（打印堆栈）
- 不要在循环中打大量日志
- 需要在 SLS 中搜索的关键日志使用 `AbcLogMarker.MARKER_MESSAGE_INDEX`
- **DEBUG 日志需要构建对象时**，必须先判断是否开启了 DEBUG 级别：

```java
// 需要构建打印对象时，先判断 debug 是否开启
if (log.isDebugEnabled()) {
    log.debug("详细信息: {}", buildExpensiveDebugInfo());
}
```
