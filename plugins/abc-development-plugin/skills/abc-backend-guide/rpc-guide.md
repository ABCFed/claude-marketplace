# RPC 服务指南

> 微服务间通信使用 Spring Cloud OpenFeign（HTTP/REST），本指南涵盖"提供 RPC 接口"和"调用其他服务 RPC 接口"两个场景。

## 概念说明

```
┌──────────────┐  HTTP/JSON  ┌──────────────┐
│  服务 A      │ ──────────→ │  服务 B      │
│  (消费方)     │  Feign      │  (提供方)     │
│              │ ←────────── │              │
└──────────────┘             └──────────────┘
```

- **提供方**：编写 RPC Controller，暴露 `/rpc/` 前缀的接口
- **消费方**：编写 Feign Client 接口，像调用本地方法一样调用远程服务
- **RPC SDK**：RPC 接口定义（Feign Client、DTO）统一放在 `AbcBisRpcSDK` 项目中，消费方通过引入 SDK 依赖来调用

## 场景一：提供 RPC 接口给其他服务调用

### RPC Controller

```java
package cn.abcyun.cis.{service}.rpc.controller;

import cn.abcyun.cis.commons.model.AbcServiceResponse;
import cn.abcyun.cis.core.aop.LogReqAndRsp;
import lombok.extern.slf4j.Slf4j;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/rpc/{servicePathPrefix}/xxxs")
@Slf4j
public class XxxRpcController {

    private final XxxService xxxService;

    public XxxRpcController(XxxService xxxService) {
        this.xxxService = xxxService;
    }

    @GetMapping("/{id}")
    @LogReqAndRsp
    public AbcServiceResponse<XxxInfo> getById(
            @RequestParam("chainId") String chainId,
            @PathVariable("id") String id) {
        XxxInfo result = xxxService.getById(chainId, id);
        return new AbcServiceResponse<>(result);
    }

    @PostMapping("")
    @LogReqAndRsp(longTimeLog = true)
    public AbcServiceResponse<XxxInfo> create(
            @RequestBody @Valid CreateXxxReq req) {
        XxxInfo result = xxxService.create(
            req.getChainId(), req.getEmployeeId(), req);
        return new AbcServiceResponse<>(result);
    }
}
```

**与前端 API Controller 的区别**：

| 区别点 | 前端 API Controller | RPC Controller |
|--------|-------------------|----------------|
| 路径前缀 | `/api/v{版本号}/{service}/` | `/rpc/{servicePathPrefix}/` |
| 位置 | `controller/` | `rpc/controller/` |
| 上下文获取 | `@RequestHeader` 取 JWT 信息 | `@RequestParam` 或 `@RequestBody` 传入 |
| 调用方 | 前端浏览器 | 其他微服务 |

## 场景二：调用其他服务的 RPC 接口

### RPC SDK 工作流程

RPC 接口定义统一维护在 `AbcBisRpcSDK` 项目中，不管是新增还是修改 Feign Client，都需要按以下流程操作：

```
1. 在 AbcBisRpcSDK 项目中新增/修改 Feign Client 和 DTO
2. 打包发布 SDK（gradle publish）
3. 在当前服务项目中升级 SDK 版本号
4. 重新加载依赖（gradle refresh）
5. 在 Service 中注入并调用
```

### 1. 定义 Feign Client（在 AbcBisRpcSDK 中）

```java
package cn.abcyun.bis.rpc.sdk.cis.client;

import cn.abcyun.common.model.AbcServiceResponseBody;
import cn.abcyun.bis.rpc.sdk.config.CisFeignForwardHeaderConfiguration;
import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.*;

@FeignClient(
    name = "abc-cis-xxx-service",
    url = "http://abc-cis-xxx-service",
    configuration = CisFeignForwardHeaderConfiguration.class
)
public interface AbcCisXxxFeignClient {

    @GetMapping("/rpc/xxxs/{id}")
    AbcServiceResponseBody<XxxInfo> getById(
        @RequestParam(value = "chainId") String chainId,
        @PathVariable("id") String id);

    @PostMapping("/rpc/xxxs")
    AbcServiceResponseBody<XxxInfo> create(
        @RequestBody CreateXxxReq req);
}
```

**规范要点**：
- Feign Client 包路径：`cn.abcyun.bis.rpc.sdk.{模块}.client`（如 `cis.client`、`bis.client`、`his.client`）
- 类命名格式：`Abc{模块}{功能}FeignClient`（如 `AbcCisGoodsFeignClient`、`AbcCisCrmFeignClient`、`AbcBisOrderFeignClient`）
- `name` 和 `url` 格式一致：`abc-{模块}-{功能}-service`（K8s 内部 DNS）
- Configuration 按模块选择：CIS 用 `CisFeignForwardHeaderConfiguration`，BIS 用 `BisFeignForwardHeaderConfiguration`
- **返回类型必须使用 `AbcServiceResponseBody<T>`**（`cn.abcyun.common.model.AbcServiceResponseBody`），这是 SDK 包中 Feign Client 的标准返回包装类型。`CisServiceResponseBody` 已废弃，不推荐使用
- DTO 存放路径：`cn.abcyun.bis.rpc.sdk.{模块}.model.{功能}/`（如 `cis.model.patient/`）
- **熔断降级**：调用外部 RPC 时，需根据业务场景评估是否需要增加熔断和降级策略（如非核心链路调用失败不应阻断主流程）

### 2. 注册 Feign Client（在当前服务项目中）

在主应用类的 `@EnableFeignClients` 中添加新的 Client：

```java
// {Service}Application.java
@EnableFeignClients(clients = {
    AbcCisClinicFeignClient.class,
    AbcCisChargeFeignClient.class,
    AbcCisXxxFeignClient.class,  // ← 新增
    // ...
})
```

### 3. 在 Service 中调用（在当前服务项目中）

**推荐方式：创建 RPC Service 包装层**

在 `rpc/client/service/` 下创建包装类，封装 Feign Client 调用：

```java
package cn.abcyun.cis.{service}.rpc.client.service;

import cn.abcyun.bis.rpc.sdk.cis.client.AbcCisXxxFeignClient;
import cn.abcyun.bis.rpc.sdk.cis.model.xxx.*;
import cn.abcyun.cis.core.util.FeignClientRpcTemplate;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class CisXxxFeignClient {

    private final AbcCisXxxFeignClient xxxFeignClient;

    @Autowired
    public CisXxxFeignClient(AbcCisXxxFeignClient xxxFeignClient) {
        this.xxxFeignClient = xxxFeignClient;
    }

    public XxxInfo getById(String chainId, String id) {
        return FeignClientRpcTemplate.dealRpcClientMethod(
            "getXxxById",
            () -> xxxFeignClient.getById(chainId, id),
            chainId, id);
    }

    // 需要打印请求/响应日志的场景
    public XxxInfo getByIdWithLog(String chainId, String id) {
        return FeignClientRpcTemplate.dealRpcClientMethod(
            "getXxxById",
            true,  // needLog
            () -> xxxFeignClient.getById(chainId, id),
            chainId, id);
    }

    // 非核心链路：异常时返回默认值而不是抛出异常
    public XxxInfo getByIdOrNull(String chainId, String id) {
        return FeignClientRpcTemplate.dealRpcClientMethod(
            "getXxxById",
            () -> xxxFeignClient.getById(chainId, id),
            null,  // exceptionDefault：异常时返回 null
            chainId, id);
    }
}
```

然后在业务 Service 中注入包装类使用：

```java
@Service
public class MyBusinessService {

    private final CisXxxFeignClient cisXxxFeignClient;

    public MyBusinessService(CisXxxFeignClient cisXxxFeignClient) {
        this.cisXxxFeignClient = cisXxxFeignClient;
    }

    public void doSomething(String chainId, String id) {
        XxxInfo info = cisXxxFeignClient.getById(chainId, id);
        // 业务逻辑...
    }
}
```

**`FeignClientRpcTemplate`**（优先使用 `cn.abcyun.cis.core.util.FeignClientRpcTemplate`，部分老项目可能还在用各自服务内的版本）：

| 方法 | 说明 | 适用场景 |
|------|------|---------|
| `dealRpcClientMethod(label, supplier, args)` | 默认不打印日志，异常时抛出 | 常规 RPC 调用 |
| `dealRpcClientMethod(label, needLog, supplier, args)` | 可控制是否打印请求/响应日志 | 需要排查问题时开启日志 |
| `dealRpcClientMethod(label, supplier, exceptionDefault, args)` | 异常时返回默认值而不是抛出 | 非核心链路，失败不应阻断主流程 |

## 常见错误处理

| 异常类型 | 原因 | 处理方式 |
|---------|------|---------|
| `FeignRuntimeException` | 网络超时、服务不可用 | 框架自动捕获并记录日志 |
| 返回 `null` | 目标服务返回空 | 检查 `rsp != null && rsp.getData() != null` |
| HTTP 4xx/5xx | 目标服务报错 | Feign 会抛异常，被 Template 捕获 |
