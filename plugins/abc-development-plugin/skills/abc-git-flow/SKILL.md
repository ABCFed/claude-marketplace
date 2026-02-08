---
name: abc-git-flow
description: ABC 后台 Git 分支管理工作流辅助。用于执行 git abc 命令进行分支操作、提供开发流程指导。当用户提到"开新分支"、"feature"、"hotfix"、"发布"、"提测"、"合并"、"灰度"、"全量"、"rc"、"tag" 等关键词时使用此技能。
---

# ABC GIT FLOW 分支管理

ABC 定制化的 Git 工作流，基于 git-flow 扩展，支持 灰度发布 流程。

## 分支结构

### 长期分支（禁止直接开发）

| 分支 | 用途 | 对应环境 |
|------|------|----------|
| `master` | 稳定的生产代码 | 正式环境 |
| `gray` | 灰度环境代码 | 灰度环境 |
| `rc` | 预发布测试 | 预发布环境 |
| `develop` | 开发基础分支 | 测试环境 |

### 临时分支

| 分支前缀 | 来源 | 用途 |
|----------|------|------|
| `feature/*` | develop | 新功能开发 |
| `hotfix/*` | master | 正式环境紧急修复 |
| `hotfix-g/*` | gray | 灰度环境紧急修复 |

## 场景判断指南

根据用户描述判断场景，并提供对应指导：

### 场景1: 新需求开发

**触发关键词**: 开新分支、新功能、feature、需求开发、迭代

**流程**:
```bash
# 1. 创建 feature 分支
git abc feature start <name>

# 2. 开发完成后，rebase develop（单人开发时）
git fetch origin develop
git rebase origin/develop

# 3. 创建提测 tag (f-tag)
git abc tag create   # 选择 "需求提测(f)"

# 4. 测试通过后，合回 develop
git abc feature finish <name>
```

**注意事项**:
- 多人协作同一 feature 时禁用 rebase，改用 merge
- finish 后记得 push develop 分支

### 场景2: 正式环境 Bug 修复

**触发关键词**: 线上bug、正式环境问题、hotfix、紧急修复、生产问题

**流程**:
```bash
# 1. 从 master 创建 hotfix 分支
git abc hotfix start <name>

# 2. 修复后创建测试 tag
git abc tag create   # 选择 "测试环境(t)"

# 3. 测试通过后，合入所有分支
git abc hotfix finish <name>

# 4. 推送所有受影响的分支
git push origin master gray rc develop

# 5. 删除 hotfix 分支
git branch -d hotfix/<name>
git push origin --delete hotfix/<name>
```

**关键提醒**: hotfix finish 会自动合入 master、gray、rc、develop 四个分支，务必全部 push！

### 场景3: 灰度环境 Bug 修复

**触发关键词**: 灰度问题、灰度bug、hotfix-g、gray环境问题

**流程**:
```bash
# 1. 从 gray 创建 hotfix-g 分支
git abc hotfix-g start <name>

# 2. 修复后创建测试 tag
git abc tag create   # 选择 "测试环境(t)"

# 3. 测试通过后，合入相关分支
git abc hotfix-g finish <name>

# 4. 推送所有受影响的分支
git push origin gray rc develop

# 5. 删除 hotfix-g 分支
git branch -d hotfix-g/<name>
git push origin --delete hotfix-g/<name>
```

**关键提醒**: hotfix-g finish 会合入 gray、rc、develop 三个分支（不包含 master）

### 场景4: 发布流程

**触发关键词**: 发布、上线、发灰度、发全量、提测、集成测试

**集成测试 (t-tag)**:
```bash
# 在 develop 分支打 t-tag
git checkout develop
git abc tag create   # 选择 "测试环境(t)"
```

**发预发布 (p-tag)**:
```bash
# 将 develop 合入 rc
git abc rc start

# 打预发布 tag
git abc tag create   # 选择 "预发布环境(p)"
git push origin rc
```

**发灰度 (g-tag)**:
```bash
# 将 rc 合入 gray
git abc rc finish
git push origin gray

# 打灰度 tag
git checkout gray
git abc tag create   # 选择 "灰度环境(g)"
```

**发全量 (v-tag)**:
```bash
# 将 gray 合入 master
git abc gray publish
git push origin master

# 打全量 tag
git checkout master
git abc tag create   # 选择 "正式环境(v)"
```

## Tag 命名规范

通过 `git abc tag create` 交互式创建的 tag 自动符合规范。

格式: `前缀年份.周数.构建号`

| 前缀 | 用途 | 示例 |
|------|------|------|
| `xxx-f` | feature 功能提测 | pc-f2021.09.01 |
| `xxx-t` | 集成测试 | pc-t2021.09.02 |
| `xxx-p` | 预发布 | pc-p2021.09.01 |
| `xxx-g` | 灰度发布 | pc-g2021.09.01 |
| `xxx-v` | 正式发布 | pc-v2021.09.01 |

## Rebase 使用原则

**推荐使用 rebase 的场景**:
- 独立开发的 feature 分支，合入 develop 最新代码
- 独立开发的 hotfix 分支，合入 master 最新代码
- 本地分支同步远程: `git pull --rebase`

**禁止使用 rebase 的场景**:
- 多人协作的分支（会导致历史混乱）

## 命令速查

```bash
# 初始化仓库
git abc init

# Feature 管理
git abc feature start <name>     # 从 develop 创建
git abc feature finish <name>    # 合回 develop

# Hotfix 管理（正式环境）
git abc hotfix start <name>      # 从 master 创建
git abc hotfix finish <name>     # 合入 master/gray/rc/develop

# Hotfix-g 管理（灰度环境）
git abc hotfix-g start <name>    # 从 gray 创建
git abc hotfix-g finish <name>   # 合入 gray/rc/develop

# RC 管理
git abc rc start                 # develop → rc
git abc rc finish                # rc → gray

# Gray 管理
git abc gray publish             # gray → master

# Tag 管理
git abc tag create               # 交互式创建 tag
git abc tag show                 # 查看最近 tag
git abc tag config               # 配置 tag 前缀

# 更新工具
git abc update
```

## 操作指导原则

1. **执行前确认**: 执行 git abc 命令前，先用 `git status` 确认工作区干净
2. **及时推送**: finish 操作后，立即推送所有受影响的分支
3. **清理分支**: 合并完成后删除已废弃的临时分支
4. **冲突处理**: 遇到合并冲突时，仔细解决后再继续操作
5. **观察提示**: 注意命令执行过程中的提示信息，按提示操作
