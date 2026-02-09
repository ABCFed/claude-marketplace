---
name: abc-git-flow
description: ABC 后台 Git 分支管理工作流辅助。用于执行 git abc 命令进行分支操作、提供开发流程指导。当用户提到"开新分支"、"feature"、"hotfix"、"发布"、"提测"、"合并"、"灰度"、"全量"、"rc"、"tag"、"MR"、"merge request" 等关键词时使用此技能。
---

# ABC GIT FLOW 分支管理

ABC 定制化的 Git 工作流，基于 git-flow 扩展，支持灰度发布流程。

## 安装 abc-git-flow

### macOS
```bash
sudo curl https://cis-static-common.oss-cn-shanghai.aliyuncs.com/assets/abc-git-flow/git-abc-flow-install.sh | sh
```
如果报错 `Bad CPU type`，需要执行：
```bash
/usr/sbin/softwareupdate --install-rosetta --agree-to-license
```

### Windows
```cmd
curl -# -O https://static-common-cdn.abcyun.cn/assets/abc-git-flow/install.bat && call install.bat
```

### Linux
```bash
curl https://static-common-cdn.abcyun.cn/assets/abc-git-flow/install-linux.sh | sh
```

## 初始化

首次使用需要在工程目录下执行：
```bash
git abc init
git abc tag config <前缀>  # 配置 tag 前缀，如 pc、charge
```

## 分支结构

### 长期分支（禁止直接开发）

| 分支 | 用途 | 对应环境 |
|------|------|----------|
| `master` | 稳定的生产代码 | 正式环境 |
| `gray` | 灰度环境代码 | 灰度环境 |
| `rc` | 预发布测试 | 预发布环境 |
| `develop` | 开发基础分支 | 测试环境 |
| `experience` | 体验分支，不保证稳定性 | 体验环境 |

### 临时分支

| 分支前缀 | 来源 | 用途 |
|----------|------|------|
| `feature/*` | develop | 新功能开发 |
| `hotfix/*` | master | 正式环境紧急修复 |
| `hotfix-g/*` | gray | 灰度环境紧急修复 |

> **分支命名规范**：参见 [分支命名规则](references/branch-naming.md)

## 典型工作流程

### 新需求开发

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

### 正式环境 Bug 修复

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

### 灰度环境 Bug 修复

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

### 发布流程

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

> **详细说明**：参见 [Tag 创建详细指南](references/tag-create.md)，包含 tag 类型、分支约束、上车/提测信息等完整说明。

## Rebase 使用原则

**推荐使用 rebase 的场景**:
- 独立开发的 feature 分支，合入 develop 最新代码
- 独立开发的 hotfix 分支，合入 master 最新代码
- 本地分支同步远程: `git pull --rebase`

**禁止使用 rebase 的场景**:
- 多人协作的分支（会导致历史混乱）

## Merge Request 管理

```bash
# 创建 MR（交互式选择目标分支和评审者）
git abc mr create

# 配置云效 Token
git abc mr config
```

## 非交互式脚本

`git abc` 部分命令（如 tag create、mr create）需要交互式输入，在自动化场景（CI/CD、脚本批处理、IDE 集成等）中不方便使用。提供了 Python 脚本作为非交互式替代方案。

**安装依赖：**
```bash
pip install requests
```

### Tag 创建脚本 (`scripts/tag_create.py`)

```bash
# 创建正式环境 tag
scripts/tag_create.py v --deps "abc-auth" --operation "无"

# 创建需求提测 tag
scripts/tag_create.py f \
  --deps "无" \
  --operation "无" \
  --remark "feat: 实现新功能" \
  --tapd-id "1122044681001112866"

# 创建灰度环境 tag
scripts/tag_create.py g --deps "abc-auth" --operation "无"

# 仅创建 tag，跳过上车/提测
scripts/tag_create.py v --skipdeploy
```

**参数说明：**

| 参数 | 说明 | 必填 |
|-----|------|-----|
| `tag_type` | Tag 类型 (f/t/v/g/p) | 是 |
| `--deps` | 依赖的服务 | 上车/提测时必填 |
| `--operation` | 需要的操作 | 上车/提测时必填 |
| `--remark` | 备注/说明 | 提测时必填 |
| `--tapd-id` | 关联的 TAPD ID | 否 (f tag 可选) |
| `-b, --business` | 业务线 (默认 abc-his) | 否 |
| `--prefix` | Tag 前缀 (默认从 git config 读取) | 否 |
| `--hotfix` | Hotfix 模式 | 否 |
| `--skipdeploy` | 跳过上车/提测，仅创建 tag | 否 |

### MR 创建脚本 (`scripts/mr_create.py`)

```bash
# 创建 MR
scripts/mr_create.py \
  -t develop \
  -T "feat: 新功能开发" \
  -r 张三 李四

# 指定描述
scripts/mr_create.py \
  -t develop \
  -T "fix: 修复bug" \
  -r 张三 \
  -d "修复了xxx问题"

# 跳过企业微信通知
scripts/mr_create.py \
  -t develop \
  -T "feat: xxx" \
  -r 张三 \
  --skip-notify
```

**参数说明：**

| 参数 | 说明 | 必填 |
|-----|------|-----|
| `-t, --target` | 目标分支 | 是 |
| `-T, --title` | MR 标题 | 是 |
| `-r, --reviewers` | 评审者姓名（多个用空格分隔） | 是 |
| `-d, --description` | MR 描述 | 否 |
| `--skip-notify` | 跳过企业微信通知 | 否 |

> **前置条件**：MR 创建需要先配置云效 Token，运行 `git abc mr config` 或手动创建 `~/.abc-fed-config/mr.json`。

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
git abc tag create <类型>        # 直接指定 tag 类型 (v/g/p/f/t)
git abc tag show [类型]          # 查看最近 tag
git abc tag config [前缀]        # 配置 tag 前缀

# MR 管理
git abc mr create                # 创建 Merge Request
git abc mr config                # 配置云效 Token

# 其他
git abc -v                       # 查看版本
git abc -h                       # 查看帮助
git abc update                   # 更新工具
```

## 命令支持情况对照

| 操作 | 交互式命令 | 非交互式脚本 | 推荐方式 |
|-----|-----------|------------|---------|
| Feature 操作 | `git abc feature start/finish` | - | 交互式 |
| Hotfix 操作 | `git abc hotfix start/finish` | - | 交互式 |
| RC 操作 | `git abc rc start/finish` | - | 交互式 |
| Tag 配置 | `git abc tag config <前缀>` | - | 交互式 |
| Tag 创建 | `git abc tag create [类型]` | `tag_create.py [类型] --deps xxx` | 自动化场景用非交互式 |
| MR 创建 | `git abc mr create` | `mr_create.py -t xxx -T xxx -r xxx` | 自动化场景用非交互式 |

> **提示**：在非交互式终端环境（CI/CD、脚本批处理、IDE 集成等）中，优先使用非交互式脚本创建 Tag 和 MR，避免终端阻塞。

## 操作指导原则

1. **执行前确认**: 执行 git abc 命令前，先用 `git status` 确认工作区干净
2. **及时推送**: finish 操作后，立即推送所有受影响的分支
3. **清理分支**: 合并完成后删除已废弃的临时分支
4. **冲突处理**: 遇到合并冲突时，仔细解决后再继续操作
5. **观察提示**: 注意命令执行过程中的提示信息，按提示操作
