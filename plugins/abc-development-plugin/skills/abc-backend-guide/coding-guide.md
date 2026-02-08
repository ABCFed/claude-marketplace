# 后端编码规范指南

> 后端业务代码编写规范，涵盖分层架构、各层代码模板、注解速查和注意事项。

## 1. 分层架构

```
┌─────────────────────────────────────────────┐
│  Controller 层                               │
│  接收 HTTP 请求，参数校验，调用 Service        │
├─────────────────────────────────────────────┤
│  Facade 层（可选）                            │
│  跨 Service 的业务编排                        │
├─────────────────────────────────────────────┤
│  Service 层                                  │
│  核心业务逻辑，事务管理                        │
├─────────────────────────────────────────────┤
│  Repository 层 (JPA)                         │
│  简单 CRUD、分页查询                          │
├─────────────────────────────────────────────┤
│  Mapper 层 (MyBatis)                         │
│  复杂查询、批量操作、性能优化                   │
├─────────────────────────────────────────────┤
│  Entity / Model                              │
│  数据库表映射、数据结构定义                     │
└─────────────────────────────────────────────┘
```

### JPA vs MyBatis 选择

| 场景 | 选择 | 原因 |
|------|------|------|
| 简单 CRUD | JPA Repository | 不用写 SQL，方法名即查询 |
| 分页查询 | JPA Repository | 内置 Pageable 支持 |
| 复杂多表关联 | MyBatis Mapper | 手写 SQL 更灵活 |
| 批量更新/插入 | MyBatis Mapper | 性能更好 |
| 动态条件查询 | MyBatis XML | `<if>` 标签动态拼接 SQL |
| 需要 force index | MyBatis XML | JPA 不支持 hint |

> **注意**：尽量避免在一个事务中同时使用 JPA 和 MyBatis 进行写操作，可能导致数据不一致或缓存问题。

### 各层常用注解

| 层 | 类型 | 常用注解 |
|----|------|---------|
| Controller | HTTP 控制器 | `@RestController`, `@RequestMapping`, `@Slf4j`, `@Api` |
| Service | 业务逻辑 | `@Service`, `@Slf4j`, `@Transactional` |
| JPA Repository | 数据访问 | 继承 `JpaRepository<Entity, ID>`，无需额外注解 |
| MyBatis Mapper | 数据访问 | `@Mapper` |
| 普通 Model（DTO/VO） | 数据传输 | `@Data` |
| JPA Model（Entity） | 数据库映射 | `@Data`, `@Entity`, `@Table`, `@Id` |

## 2. 请求/响应 DTO

### 请求 DTO（Req）

```java
package cn.abcyun.cis.{service}.api.xxx;

import io.swagger.annotations.ApiModelProperty;
import lombok.Data;
import javax.validation.constraints.NotBlank;

@Data
public class CreateXxxReq {

    @NotBlank(message = "名称不能为空")
    @ApiModelProperty("名称")
    private String name;

    @ApiModelProperty("描述")
    private String description;
}
```

**规范要点**：
- 请求 DTO 放在 `api/` 包下，按业务模块分子包
- 命名规则：`Create{Xxx}Req`、`Update{Xxx}Req`、`Query{Xxx}Req`
- 使用 `@NotBlank` / `@NotNull` / `@Max` 等 JSR 303 注解做参数校验
- 使用 `@ApiModelProperty` 标注 Swagger 文档

### 响应 DTO（Rsp / View / Info）

```java
@Data
public class XxxInfo implements Serializable {

    @JsonSerialize(using = ToStringSerializer.class)
    private Long id;

    private String name;
    private String description;
    private String createdBy;
    private Instant created;
}
```

**规范要点**：
- 响应 DTO 放在 `entity/` 包下
- 命名规则：`{Xxx}Info`（详情）、`{Xxx}Abstract`（摘要）、`{Xxx}View`（视图）
- 实现 `Serializable` 接口
- `@JsonInclude(NON_NULL)` 声明在**字段级别**，不要加在类上；View 对象的新字段**必须加** `@JsonInclude(NON_NULL)`，但**已有字段不能新增此注解**（会影响前端已有逻辑）
- **Long/long 类型字段必须加** `@JsonSerialize(using = ToStringSerializer.class)`，避免前端 JavaScript 精度丢失

## 3. 数据库 Entity

```java
@Data
@Entity
@Table(name = "{prefix}_xxx")
public class Xxx {

    @Id
    private Long id;

    @Column(name = "chain_id")
    private String chainId;

    private String name;
    private String description;
    private int isDeleted;        // 0=正常, 1=已删除
    private Instant created;
    private String createdBy;
    private Instant lastModified;
    private String lastModifiedBy;
}
```

**规范要点**：
- Entity 放在 `model/` 包下
- 表名前缀每个服务不同，新建时先查看当前项目已有表的前缀并保持一致
- 新表主键使用 `Long` 类型，由 `AbcIdGenerator` 生成（老表可能是 `String`）
- 必须包含审计字段：`created`、`createdBy`、`lastModified`、`lastModifiedBy`
- 软删除：使用 `isDeleted` 字段（0=正常, 1=已删除），不物理删除

## 4. Repository / Mapper 规范

**JPA Repository**：
- 放在 `repository/` 包下，继承 `JpaRepository<Entity, 主键类型>`
- 查询方法优先用方法名派生（findBy / existsBy / countBy）
- 修改操作必须加 `@Modifying` + `@Transactional`
- 查询条件通常包含 `chainId`（连锁ID）和 `isDeleted`（排除已删除）

**MyBatis Mapper**（复杂查询时使用）：
- Mapper 接口放在 `dao/` 包下，加 `@Mapper` 注解
- XML 文件放在 `src/main/resources/mapper/` 目录
- 多参数使用 `@Param` 注解
- XML 中使用 `#{param}` 防止 SQL 注入，禁止使用 `${param}`
- **优先使用 JPA**：能用 JPA 多次 `IN` 查询解决的，不要用 MyBatis 多表关联
- **IN 查询注意事项**：每批 `IN` 的大小需要控制（建议不超过 500），因为 JPA 的 `queryPlanCache` 会为不同长度的 IN 列表生成不同的查询计划，过多不同长度可能导致 OOM

## 5. Service 规范

```java
@Service
@Slf4j
public class XxxService {

    private final XxxRepository xxxRepository;
    private final AbcIdGenerator abcIdGenerator;

    public XxxService(XxxRepository xxxRepository,
                      AbcIdGenerator abcIdGenerator) {
        this.xxxRepository = xxxRepository;
        this.abcIdGenerator = abcIdGenerator;
    }

    @Transactional
    public XxxInfo create(String chainId, String employeeId,
                          CreateXxxReq req) {
        // 1. 业务校验
        if (xxxRepository.existsByChainIdAndNameAndIsDeleted(
                chainId, req.getName(), 0)) {
            throw new {Service}CustomException("名称已存在");
        }

        // 2. 构建实体并保存
        Xxx xxx = new Xxx();
        xxx.setId(abcIdGenerator.nextId());
        xxx.setChainId(chainId);
        xxx.setName(req.getName());
        xxx.setIsDeleted(0);
        xxx.setCreatedBy(employeeId);
        xxx.setLastModifiedBy(employeeId);
        xxxRepository.save(xxx);

        return convertToInfo(xxx);
    }

    @Transactional(readOnly = true)
    public XxxInfo getById(String chainId, String id) {
        Xxx xxx = xxxRepository
            .findFirstByChainIdAndIdAndIsDeleted(chainId, id, 0);
        if (xxx == null) {
            throw new NotFoundException();
        }
        return convertToInfo(xxx);
    }
}
```

**规范要点**：
- Service 放在 `service/` 包下，直接实现类，不需要接口
- 推荐构造器注入依赖
- 写操作加 `@Transactional`，只读操作加 `@Transactional(readOnly = true)`
- ID 使用 `AbcIdGenerator.nextId()` 生成
- 业务异常抛各服务的 `{Service}CustomException`（继承自 `CisCustomException`），资源不存在抛 `NotFoundException`

## 6. Controller 规范

```java
@RestController
@RequestMapping("/api/v2/{service}/xxxs")
@Api(value = "Xxx管理", description = "Xxx相关接口")
@Slf4j
public class XxxController {

    private final XxxService xxxService;

    public XxxController(XxxService xxxService) {
        this.xxxService = xxxService;
    }

    @PostMapping("")
    @ApiOperation("创建Xxx")
    @LogReqAndRsp
    public AbcServiceResponse<XxxInfo> create(
            @RequestHeader(CisJWTUtils.CIS_HEADER_CHAIN_ID) String chainId,
            @RequestHeader(CisJWTUtils.CIS_HEADER_EMPLOYEE_ID) String employeeId,
            @RequestBody @Valid CreateXxxReq req) {
        XxxInfo result = xxxService.create(chainId, employeeId, req);
        return new AbcServiceResponse<>(result);
    }

    @GetMapping("/{id}")
    @ApiOperation("获取Xxx详情")
    public AbcServiceResponse<XxxInfo> getById(
            @RequestHeader(CisJWTUtils.CIS_HEADER_CHAIN_ID) String chainId,
            @PathVariable String id) {
        XxxInfo result = xxxService.getById(chainId, id);
        return new AbcServiceResponse<>(result);
    }
}
```

**规范要点**：
- Controller 放在 `controller/` 包下
- 路径格式：`/api/v{版本号}/{service}/{资源名复数}`（如 `/api/v2/crm/patients`、`/api/v3/goods/stocks`）
- 使用 `@RestController`，不用 `@Controller`
- 统一响应包装：`AbcServiceResponse<T>`
- 通过 `@RequestHeader` 获取 chainId、clinicId、employeeId 等上下文
- 写操作加 `@LogReqAndRsp` 记录日志
- 请求体加 `@Valid` 触发参数校验

## 7. 注解速查

### 7.1 Spring 核心注解

```java
// 组件标记
@Service          // 标记业务逻辑类
@RestController   // 标记 HTTP 控制器（自动返回 JSON）
@Configuration    // 标记配置类

// 依赖注入
@Autowired        // 自动注入依赖（字段注入）
// 推荐构造器注入：
// private final XxxService xxxService;
// public MyService(XxxService xxxService) { this.xxxService = xxxService; }

// 路由映射
@RequestMapping("/api/v2/{service}/xxxs")  // 基础路径
@GetMapping("/{id}")                       // GET 请求
@PostMapping("")                           // POST 请求
@PutMapping("/{id}")                       // PUT 请求
@DeleteMapping("/{id}")                    // DELETE 请求

// 参数绑定
@PathVariable     // 路径参数：/patients/{id} → id
@RequestParam     // 查询参数：?limit=20 → limit
@RequestBody      // 请求体（JSON → Java 对象）
@RequestHeader    // 请求头
```

### 7.2 Lombok 注解

```java
@Data             // 自动生成 getter/setter/toString/equals/hashCode（最常用）
@Slf4j            // 自动生成 log 对象，可直接用 log.info("xxx")
@NoArgsConstructor // 生成无参构造函数
@AllArgsConstructor // 生成全参构造函数
@Builder          // 生成 Builder 模式：Xxx.builder().name("a").build()
@Accessors(chain = true) // 支持链式调用：obj.setName("a").setAge(18)
@FieldNameConstants // 生成字段名常量：Patient.Fields.name → "name"
```

### 7.3 JPA 注解

```java
@Entity                    // 标记为数据库实体
@Table(name = "v2_patient") // 指定表名
@Id                        // 主键字段
@Column(name = "id_card")  // 指定列名（字段名和列名不同时）
@Version                   // 乐观锁版本号
@IdClass(XxxURK.class)     // 复合主键

// JPA 生命周期回调
@PostLoad                  // 从数据库加载后执行
@PrePersist                // 插入前执行
@PreUpdate                 // 更新前执行
```

### 7.4 事务与数据注解

```java
@Transactional             // 开启事务（方法内操作要么全成功，要么全回滚）
@Transactional(readOnly = true) // 只读事务（查询用，性能更好）
@UseReadOnlyDB             // 使用只读数据源（读写分离）
@Async                     // 异步执行
@Retryable(value = {DataIntegrityViolationException.class}, maxAttempts = 5)
                           // 失败自动重试
```

**事务注解搭配**：

| 场景 | 注解搭配 | 说明 |
|------|---------|------|
| 写操作 | `@Transactional` | 默认读写事务 |
| 只读查询（需事务保证） | `@Transactional(readOnly = true)` | 只读事务，走主库 |
| 只读查询（可走从库） | `@UseReadOnlyDB` | 走只读从库，适合对实时性要求不高的查询 |
| 只读查询（事务 + 从库） | `@Transactional(readOnly = true)` + `@UseReadOnlyDB` | 只读事务 + 从库 |

### 7.5 Swagger 文档注解

```java
@Api(value = "患者管理", description = "患者相关接口")  // Controller 文档
@ApiOperation("获取患者详情")                          // 方法文档
@ApiModelProperty("姓名")                             // 字段文档
@ApiImplicitParam(name = "id", value = "患者ID")      // 参数文档
```

> 如果安装了 `swagger-springfox` SKILL，可参考其中更详细的 Swagger 注解规范和最佳实践。

### 7.6 ABC 自定义注解

```java
@LogReqAndRsp              // 自动记录请求和响应日志
@LogReqAndRsp(longTimeLog = true) // 同时写入长期存储日志桶
@ApiEncrypt                // API 响应加密
@SensitiveEntity           // 标记包含敏感字段的实体
@SensitiveField            // 标记敏感字段（手机号、身份证等）
@SensitiveParamSql(params = {...}) // MyBatis 敏感参数自动加密
```

## 8. ABC Common 公共项目

ABC 后端有一组公共基础项目，所有业务服务都依赖它们。

### 依赖关系

```
AbcBisRpcSDK                    ← 最上层，全系统公用 RPC SDK
    ↓ 依赖
AbcCisCommons + AbcCisCore      ← 中间层，工具类 + 框架核心
    ↓ 依赖
AbcCommonModel + AbcCommonLog   ← 最底层，数据模型 + 日志
```

### 各项目职责

| 项目 | 职责 | 关键类 |
|------|------|--------|
| **AbcCommonModel** | 全系统通用数据模型：响应体、分页、错误信息 | `AbcServiceResponse`、`AbcServiceResponseBody`、`AbcListPage` |
| **AbcCommonLog** | 统一日志收集，集成阿里云 SLS | `LoghubAppender`（Logback → SLS） |
| **AbcCisCommons** | CIS 公共工具类：加密、日期、JSON、拼音、价格计算 | `AESUtils`、`DateUtils`、`JsonUtils`、`PinyinUtils` |
| **AbcCisCore** | CIS 框架核心：序列化、链路追踪、RPC 调用模板 | `FeignClientRpcTemplate`、`AbcObjectMapperSupplier`、`ApiEncryptSerializer` |
| **AbcBisRpcSDK** | 全系统公用 RPC SDK：各服务的 Feign Client + DTO 定义 | 各服务的 `FeignClient`（如商品、医嘱、收费等） |

## 9. Checklist

编码前的自检清单：

- [ ] 请求/响应 DTO 是否定义完整，字段命名是否规范
- [ ] Entity 是否包含审计字段（created/createdBy/lastModified/lastModifiedBy）
- [ ] 是否使用软删除（isDeleted=1），而非物理删除
- [ ] 查询条件是否包含 chainId 做数据隔离
- [ ] 写操作是否加了 `@Transactional`
- [ ] Controller 是否加了 Swagger 注解
- [ ] 新表是否需要提交 DDL（参考 `db-migration.md`）
- [ ] 关联查询是否优先使用 JPA 多次 IN 查询，而非 MyBatis 多表关联
