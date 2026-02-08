# 数据库变更流程

> 涵盖建表、加字段、加索引等 DDL 操作，以及对应的 Java 代码配套修改。

## 变更流程概览

```
1. 编写 DDL SQL 脚本
2. 提交 SQL 到 sql/ 目录
3. 修改 Java 代码（Entity / Repository / Mapper）
4. 本地验证
5. 提交代码，DBA 审核 SQL 后执行
```

## 1. 建表

### DDL 模板

```sql
CREATE TABLE `{prefix}_xxx` (
    `id`                BIGINT        NOT NULL COMMENT '主键ID',
    `chain_id`          VARCHAR(32)   NOT NULL COMMENT '连锁ID',
    `clinic_id`         VARCHAR(32)   DEFAULT NULL COMMENT '门店ID',
    `name`              VARCHAR(128)  NOT NULL COMMENT '名称',
    `description`       TEXT          DEFAULT NULL COMMENT '描述',
    `is_deleted`        int       NOT NULL DEFAULT 0 COMMENT '状态: 0-正常, 1-已删除',
    `created`           DATETIME  NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `created_by`        VARCHAR(32)   DEFAULT NULL COMMENT '创建人',
    `last_modified`     DATETIME  NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后修改时间',
    `last_modified_by`  VARCHAR(32)   DEFAULT NULL COMMENT '最后修改人',
    PRIMARY KEY (`id`),
    KEY `ix_chain_id` (`chain_id`)
) COMMENT='Xxx表';
```

**建表规范**：
- 表名小写下划线命名，**每个服务有自己的表名前缀**（如 `v2_goods_`、`v2_`、`crm_` 等），新建表时先查看当前项目已有表的前缀并保持一致
- 新表主键用 `BIGINT`，由 `AbcIdGenerator` 生成（老表可能是 `VARCHAR(32)`，同样由 `AbcIdGenerator` 生成）
- 必须包含 `chain_id` 字段做数据隔离
- 必须包含审计字段：`created`、`created_by`、`last_modified`、`last_modified_by`
- 软删除用 `is_deleted` 字段（0=正常, 1=已删除）
- 每个字段必须有 `COMMENT`
- `chain_id` 必须建索引
- **跨服务字段**：如果存储的是其他服务的字段（如 `goods_id`、`patient_id` 等），数据类型和长度必须与对应服务的表结构保持一致
- **数据清理**：新表创建后需评估是否需要纳入数据清理脚本（如过期数据定期清理）

## 2. 加字段

```sql
-- 优先 NOT NULL + 默认值
ALTER TABLE `xxx`
    ADD COLUMN `new_field` VARCHAR(64) NOT NULL DEFAULT '' COMMENT '新字段说明';

-- 确实允许为空的场景才用 NULL
ALTER TABLE `xxx`
    ADD COLUMN `new_field` VARCHAR(64) DEFAULT NULL COMMENT '新字段说明';
```

**加字段规范**：
- 新增字段**优先使用 `NOT NULL` + 默认值**，只有确实需要区分"未填写"和"空值"时才用 `NULL`
- 新字段必须有 `COMMENT`
- **禁止变更已有字段的类型**（如 `VARCHAR` 改 `INT`），可能导致兼容性问题
- **禁止将已有字段从 `NULL` 改为 `NOT NULL`**，可能导致历史数据写入失败
- 新增的 SQL 需要确保能**走到业务库索引**，避免全表扫描
- 同步修改 JPA Entity，添加对应的 Java 字段
- 如果 MyBatis XML 中有 `SELECT *`，无需改 XML；如果是显式列名，需要补上新字段

## 3. 加索引

```sql
-- 普通索引
ALTER TABLE `xxx`
    ADD INDEX `ix_chain_id_status` (`chain_id`, `status`);
```

**索引规范**：
- 普通索引：`ix_` 前缀，如 `ix_chain_id_status`
- **禁止添加唯一索引**：业务唯一性由应用层保证，不在数据库层加唯一约束
- 索引字段顺序：高区分度字段在前

## 4. SQL 脚本存放

SQL 文件放在项目根目录的 `sql/` 目录下，命名格式：

```
sql/
└── YYMMDD_描述.sql    # 如 260208_add_xxx_table.sql
```

## 5. Java 代码配套修改

数据库变更后，需要同步修改以下 Java 文件：

| 变更类型 | 需要修改的文件 |
|---------|-------------|
| 新建表 | Entity (`model/`)、Repository (`repository/`)、可能需要 Mapper (`dao/`) |
| 加字段 | Entity 加字段、相关 DTO 加字段、MyBatis XML 中显式列名补上 |
| 加索引 | 无需改 Java 代码 |
| 改字段类型 | Entity 字段类型同步修改 |

## 6. 常用类型映射

| MySQL 类型 | Java 类型 | 说明 |
|-----------|----------|------|
| `VARCHAR` | `String` | 字符串 |
| `INT` | `int` / `Integer` | 整数（不使用 `TINYINT`，一般不考虑 `UNSIGNED`） |
| `BIGINT` | `long` / `Long` | 长整数（新表主键类型） |
| `DECIMAL` | `BigDecimal` | 金额等精确数值 |
| `DATETIME` | `Instant` | 时间戳（推荐） |
| `DATE` | `LocalDate` | 日期 |
| `TEXT` | `String` | 长文本 |
