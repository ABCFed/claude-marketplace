# 异常处理规范

## 1. 异常继承体系

```
RuntimeException
├── NotFoundException                    → 404
├── ParamRequiredException               → 400
├── ParamNotValidException               → 400
├── ServiceInternalException             → 500
├── FeignRuntimeException                → 动态（由调用方状态码决定）
└── CisCustomException                   → 400（业务异常基类）
    └── {Service}CustomException         → 400（各服务自定义业务异常）
```

> 各服务会继承 `CisCustomException` 创建自己的业务异常类，如 `CisGoodsServiceException`、`CrmCustomException` 等，命名格式为 `{Service}CustomException`。

## 2. 什么场景抛什么异常

| 场景 | 异常类型 | 说明 |
|------|---------|------|
| 资源不存在 | `NotFoundException` | 查询单个资源返回 null 时 |
| 缺少必需参数 | `ParamRequiredException` | 必填参数为空 |
| 参数格式/值不合法 | `ParamNotValidException` | 参数校验不通过（非 @Valid 场景） |
| 业务规则校验不通过 | `CisCustomException` 或其子类 | 如名称重复、状态不允许操作等 |
| 服务内部不可恢复错误 | `ServiceInternalException` | 系统级异常，不应暴露细节给调用方 |

## 3. 全局异常处理机制

框架通过 `ExceptionTranslator`（`@ControllerAdvice`）统一拦截异常并转换为 HTTP 响应，**不需要在 Controller 中手动 try/catch**。

各服务可继承 `ExceptionTranslator` 扩展自己的异常处理，如 `CrmExceptionTranslator`、`GoodsExceptionTranslator` 等。

## 4. 异常类所在包

| 异常类 | 包路径 |
|--------|--------|
| `NotFoundException` | `cn.abcyun.cis.commons.exception` |
| `ParamRequiredException` | `cn.abcyun.cis.commons.exception` |
| `ParamNotValidException` | `cn.abcyun.cis.commons.exception` |
| `ServiceInternalException` | `cn.abcyun.cis.commons.exception` |
| `CisCustomException` | `cn.abcyun.cis.commons.exception` |
| `FeignRuntimeException` | `cn.abcyun.cis.commons.exception` |
| `ExceptionTranslator` | `cn.abcyun.cis.core.base` |

## 5. 使用示例

```java
import cn.abcyun.cis.commons.exception.NotFoundException;
import cn.abcyun.cis.commons.exception.ParamRequiredException;

// 资源不存在
Xxx xxx = xxxRepository.findFirstByChainIdAndIdAndIsDeleted(chainId, id, 0);
if (xxx == null) {
    throw new NotFoundException();
}

// 业务校验不通过（使用各服务的 CustomException）
if (xxxRepository.existsByChainIdAndNameAndIsDeleted(chainId, name, 0)) {
    throw new {Service}CustomException({Service}ServiceError.NAME_ALREADY_EXISTS);
}

// 缺少必需参数
if (StringUtils.isEmpty(chainId)) {
    throw new ParamRequiredException("chainId");
}
```

## 6. 业务错误码

各服务通常定义一个 `ServiceError` 枚举类（如 `GoodsServiceError`、`CrmServiceError`），集中管理错误码和错误消息：

```java
public enum {Service}ServiceError implements CisServiceError {
    NAME_ALREADY_EXISTS(40001, "名称已存在"),
    PATIENT_NOT_FOUND(40002, "患者不存在"),
    // ...
    ;

    private final int code;
    private final String message;
}
```

使用时传入枚举值：`throw new {Service}CustomException({Service}ServiceError.NAME_ALREADY_EXISTS);`
