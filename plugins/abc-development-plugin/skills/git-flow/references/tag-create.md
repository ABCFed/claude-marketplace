# Tag 创建详细指南

## Tag 类型说明

| 类型 | 名称 | 可部署 | 可提测 | 允许分支 | 说明 |
|-----|------|--------|--------|----------|------|
| f | 需求提测 | ❌ | ✅ | 所有分支 | 需求开发完成，提测给测试同学 |
| t | 测试环境 | ❌ | ✅ | 所有分支 | 测试环境 tag |
| p | 预发布 | ✅ | ❌ | **rc** | 预发布环境 tag |
| g | 灰度 | ✅ | ❌ | **gray** | 灰度环境 tag |
| v | 正式 | ✅ | ❌ | **master** | 正式环境 tag，需要 CR 审核 |
| pgv | 一键发布正式 | ✅ | ❌ | 自动切换 | 同时创建 p→g→v，需要 CR 审核 |
| pg | 一键发布预发布 | ✅ | ❌ | 自动切换 | 同时创建 p→g |

## 分支约束（重要）

```
v tag  → 只能在 master 分支创建
g tag  → 只能在 gray 分支创建
p tag  → 只能在 rc 分支创建
f/t tag → 任意分支
```

**违反分支约束会报错并拒绝创建。**

## Tag 命名格式

```
{prefix}-{tagType}{year}.{week}.{build}
```

- `prefix`: tag 前缀（如 pc, charge 等），首次使用时需要配置
- `tagType`: tag 类型（f/t/v/g/p）
- `year`: 年份（如 2025）
- `week`: 周数（自动计算）
- `build`: 构建号（自动递增，从 01 开始）

**示例：**
- `pc-v2025.05.01` - pc 项目的正式环境 tag
- `charge-g2025.05.03` - charge 项目的灰度环境 tag

## 使用命令

### 命令行参数 vs 交互式选择

| Tag 类型 | 命令行指定 | 交互式选择 | 说明 |
|---------|-----------|-----------|------|
| f | ✅ `git abc tag create f` | ✅ | 需求提测 |
| t | ✅ `git abc tag create t` | ✅ | 测试环境 |
| v | ✅ `git abc tag create v` | ✅ | 正式环境（仅 master） |
| g | ✅ `git abc tag create g` | ✅ | 灰度环境（仅 gray） |
| p | ✅ `git abc tag create p` | ✅ | 预发布（仅 rc） |
| pgv | ❌ | ✅ | 一键发布正式（自动切换分支） |
| pg | ❌ | ✅ | 一键发布预发布（自动切换分支） |

> **注意**：`pgv` 和 `pg` 不支持命令行直接指定，必须通过交互式选择。

### 基本用法

```bash
# 交互式选择 tag 类型（推荐用于 pgv/pg）
git abc tag create

# 直接指定单个 tag 类型（f/t/v/g/p）
git abc tag create f
git abc tag create t
git abc tag create v
git abc tag create g
git abc tag create p

# 指定业务线
git abc tag create -b abc-oa v
git abc tag create -b abc-global v
git abc tag create -b abc-bis v

# hotfix 模式（上班车时会检查未发布的 tag）
git abc tag create --hotfix v

# 组合使用
git abc tag create -b abc-global --hotfix g
```

## 创建流程

1. **验证环境**：检查 tag 配置和 git 用户名
2. **选择类型**：交互式选择或命令行指定 tag 类型
3. **分支检查**：验证当前分支是否允许创建该类型 tag
4. **更新分支**：fetch + pull (rebase) 更新代码
5. **生成版本**：基于最新 tag 自动递增 build 号
6. **创建推送**：创建本地 tag 并推送到远程
7. **后续处理**：
   - 可部署类型（v/g/p/pgv/pg）→ 填写信息并上班车
   - 可提测类型（f/t）→ 填写信息并提测
   - 其他 → 复制到剪贴板供测试使用

## 上班车信息（可部署 tag）

创建 v/g/p/pgv/pg tag 时需要填写：

| 字段 | 说明 | 是否必填 |
|-----|------|----------|
| 依赖的服务 | 描述该次发布需要依赖的服务 | ✅ |
| 需要的操作 | 描述需要进行的操作（如刷数据、建字段） | ✅ |
| CR审核人 | v/pgv 需要，两人及以上（Leader+其他成员） | 条件必填 |
| CR链接 | v/pgv 需要，必须是 http 开头的链接 | 条件必填 |
| 紧急预案 | v/pgv 需要，发布后出现紧急情况的预案 | 条件必填 |
| 备注 | 发布备注说明 | ✅ |

## 提测信息（f/t tag）

创建 f/t tag 时需要填写：

| 字段 | 说明 |
|-----|------|
| 配合提测的服务 | 涉及其他服务 TAG 配合提测 |
| 影响面评估 | 可能影响到的功能点逻辑 |
| 需求/BUG | TAPD 标题或其他描述 |
| 关联的需求ID | pc 项目的 f tag 可填写，触发自动化测试 |

## 配置 Tag 前缀

首次使用时需要配置 tag 前缀：

```bash
# 交互式配置
git abc tag config

# 命令行配置
git abc tag config charge
git abc tag config pc
```

配置后，tag 格式如：`{prefix}-v2025.xx.xx`

## 业务线前缀

使用 `-b` 参数指定业务线时，会自动添加业务前缀：

| 业务线 | 前缀 |
|--------|------|
| abc-his | （无前缀） |
| abc-global | global- |
| abc-oa | oa- |
| abc-bis | bis- |
| mira | mira- |

**示例：** `-b abc-oa` + prefix `pc` → 最终 tag 前缀为 `oa-pc`

## 常见问题

### Q: 为什么报错"禁止在非master分支打v tag"？
A: v tag 只能在 master 分支创建，请先切换到 master 分支。

### Q: 为什么 `git abc tag create pgv` 无效？
A: `pgv` 和 `pg` 不支持命令行直接指定，请使用 `git abc tag create` 进入交互式选择。

### Q: 如何查看最新的 tag？
A: 使用 `git abc tag show [类型]` 命令。

### Q: hotfix 模式有什么用？
A: hotfix 模式会在上班车时检查是否存在未发布的 tag，提示确认后继续。

### Q: 一键发布（pgv/pg）如何工作？
A: 会自动切换分支并依次创建多个 tag：
- pgv: 在 rc 创建 p → 切到 gray 创建 g → 切到 master 创建 v
- pg: 在 rc 创建 p → 切到 gray 创建 g
