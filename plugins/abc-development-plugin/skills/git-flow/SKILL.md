---
name: git-flow
description: ABC Git Flow 工作流助手。帮助你在开发需求或修复 bug 时使用 abc-git-flow 工具管理 git 分支。当用户请求"拉分支"、"创建分支"、"git flow"、"分支管理"或类似操作时触发此技能。
---

# ABC Git Flow 工作流助手

帮助你在开发需求或修复 bug 时使用 abc-git-flow 工具管理 git 分支。

> **⚠️ Claude Code 用户注意**：部分 `git abc` 命令需要交互式输入，在 Claude Code 中无法正常工作。**推荐使用提供的 Python 脚本**（见下方非交互式命令部分），避免终端阻塞。

## 安装

```bash
npx add-skill https://github.com/ABCFed/claude-marketplace/tree/main/skills/git-flow
```

## 安装 abc-git-flow

### macOS
```bash
sudo curl https://cis-static-common.oss-cn-shanghai.aliyuncs.com/assets/abc-git-flow/git-abc-flow-install.sh
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

### 安装 Python 依赖

```bash
pip install requests
```

## 初始化

首次使用需要在工程目录下执行：
```bash
git abc init
git abc tag config <前缀>  # 配置 tag 前缀，如 pc、charge
```

## 常用命令

> **分支命名规范**：参见 [分支命名规则](references/branch-naming.md)，了解 feature、hotfix、hotfix-g 分支的正确命名格式。

### 需求开发 (Feature)

```bash
# 开始需求开发 - 从 develop 拉取分支
git abc feature start <feature-name>

# 完成需求开发 - 合并到 develop
git abc feature finish <feature-name>
```

### 正式环境紧急修复 (Hotfix)

```bash
# 开始修复 - 从 master 拉取分支
git abc hotfix start <hotfix-name>

# 完成修复 - 合并到 master/gray/rc/develop
git abc hotfix finish <hotfix-name>
```

### 灰度环境紧急修复 (Hotfix-g)

```bash
# 开始修复 - 从 gray 拉取分支
git abc hotfix-g start <hotfix-name>

# 完成修复 - 合并到 gray/rc/develop
git abc hotfix-g finish <hotfix-name>
```

### RC 分支管理

```bash
# 将 develop 合入 rc（上线前）
git abc rc start

# 将 rc 合入 gray
git abc rc finish
```

### 灰度发布

```bash
# 将 gray 合入 master（灰度到全量）
git abc gray publish
```

### Tag 管理

**交互式命令（需要填写信息）：**
```bash
# 创建 tag（会提示选择类型并填写信息）
git abc tag create

# 直接指定 tag 类型（但仍需填写上车/提测信息）
git abc tag create v
git abc tag create g
git abc tag create f

# 查看最近 tag
git abc tag show [类型]

# 配置 tag 前缀
git abc tag config [前缀]
```

**非交互式脚本（推荐用于 Claude Code）：**
```bash
# 创建正式环境 tag
~/.claude/skills/git-flow/scripts/tag_create.py v --deps "abc-auth" --operation "无"

# 创建需求提测 tag
~/.claude/skills/git-flow/scripts/tag_create.py f \
  --deps "无" \
  --operation "无" \
  --remark "feat: 实现新功能" \
  --tapd-id "1122044681001112866"

# 创建灰度环境 tag
~/.claude/skills/git-flow/scripts/tag_create.py g \
  --deps "abc-auth" \
  --operation "无"
```

> **详细说明**：参见 [tag-create 详细指南](references/tag-create.md)，包含 tag 类型、分支约束、命令用法等完整说明。

### Merge Request 管理

**交互式命令（不推荐）：**
```bash
git abc mr create  # 会进入交互式选择
git abc mr config  # 配置云效 Token
```

**非交互式脚本（推荐用于 Claude Code）：**
```bash
# 创建 MR（需要先配置 git abc mr config）
~/.claude/skills/git-flow/scripts/mr_create.py \
  -t develop \
  -T "feat: 新功能开发" \
  -r 张三 李四

# 指定描述
~/.claude/skills/git-flow/scripts/mr_create.py \
  -t develop \
  -T "fix: 修复bug" \
  -r 张三 \
  -d "修复了xxx问题"
```

## 非交互式命令（Claude Code 推荐）

由于部分命令需要交互式输入，提供了 Python 脚本替代方案：

### Tag 创建脚本 (`scripts/tag_create.py`)

| 命令 | 说明 |
|-----|------|
| `tag_create.py v --deps "xxx" --operation "xxx"` | 创建正式环境 tag |
| `tag_create.py g --deps "xxx" --operation "xxx"` | 创建灰度环境 tag |
| `tag_create.py p --deps "xxx" --operation "xxx"` | 创建预发布 tag |
| `tag_create.py f --deps "xxx" --operation "xxx" --remark "xxx"` | 创建需求提测 tag |
| `tag_create.py t --deps "xxx" --operation "xxx" --remark "xxx"` | 创建测试环境 tag |

**完整参数：**
- `tag_type` - Tag 类型 (f/t/v/g/p)，必填
- `--deps` - 依赖的服务
- `--operation` - 需要的操作
- `--remark` - 备注/说明
- `--tapd-id` - 关联的 TAPD ID (f tag 可选)
- `-b, --business` - 业务线 (默认 abc-his)
- `--prefix` - Tag 前缀 (从 git config 读取)
- `--hotfix` - Hotfix 模式
- `--skipdeploy` - 跳过上车/提测，仅创建 tag

### MR 创建脚本 (`scripts/mr_create.py`)

| 参数 | 说明 | 必填 |
|-----|------|-----|
| `-t, --target` | 目标分支 | ✅ |
| `-T, --title` | MR 标题 | ✅ |
| `-r, --reviewers` | 评审者姓名 | ✅ |
| `-d, --description` | MR 描述 | ❌ |
| `--skip-notify` | 跳过企业微信通知 | ❌ |

> **非交互式使用指南**：参见 [非交互式命令使用指南](references/non-interactive-usage.md)

## 典型工作流程（Claude Code 优化版）

### 需求开发流程

1. **从 develop 拉开发分支：**
   ```bash
   git abc feature start <feature-name>
   ```

2. **进行需求开发、编码**

3. **开发完成后，rebase develop 的代码，创建 f-tag：**
   ```bash
   git rebase develop
   ~/.claude/skills/git-flow/scripts/tag_create.py f \
     --deps "无" \
     --operation "无" \
     --remark "feat: 实现新功能" \
     --tapd-id "1122044681001112866"
   ```

4. **提测完成，合并到 develop：**
   ```bash
   git abc feature finish <feature-name>
   ```

5. **等待集成测试，创建 t-tag：**
   ```bash
   ~/.claude/skills/git-flow/scripts/tag_create.py t \
     --deps "无" \
     --operation "无" \
     --remark "集成测试"
   ```

6. **集成测试完毕，将 develop 合入 rc，创建 p-tag：**
   ```bash
   git abc rc start
   ~/.claude/skills/git-flow/scripts/tag_create.py p \
     --deps "abc-auth" \
     --operation "无"
   ```

### 正式环境 Bug 修复流程

1. **从 master 拉 hotfix 分支：**
   ```bash
   git abc hotfix start <hotfix-name>
   ```

2. **修复后创建 t-tag 给测试同学：**
   ```bash
   ~/.claude/skills/git-flow/scripts/tag_create.py t \
     --deps "无" \
     --operation "无" \
     --remark "hotfix: 修复xxx问题"
   ```

3. **测试完毕后合并到 master/gray/rc/develop：**
   ```bash
   git abc hotfix finish <hotfix-name>
   ```
   注意：需要将 master、gray、rc 和 develop push 到远程

### 灰度环境 Bug 修复流程

1. **从 gray 拉 hotfix-g 分支：**
   ```bash
   git abc hotfix-g start <hotfix-name>
   ```

2. **修复后创建 t-tag 给测试同学：**
   ```bash
   ~/.claude/skills/git-flow/scripts/tag_create.py t \
     --deps "无" \
     --operation "无" \
     --remark "hotfix: 修复xxx问题"
   ```

3. **测试完毕后合并到 gray/rc/develop：**
   ```bash
   git abc hotfix-g finish <hotfix-name>
   ```
   注意：需要将 gray、rc 和 develop push 到远程

## 分支说明

### 长期分支

| 分支 | 说明 |
|------|------|
| **master** | 正式环境稳定代码，不能直接开发 |
| **gray** | 灰度环境稳定代码，不能直接开发 |
| **rc** | 预发布环境分支，完成后合入 gray |
| **develop** | 新需求开发基础分支，汇集已完成功能 |
| **experience** | 体验分支，不保证稳定性，用于体验最新特性 |

### 临时分支

| 分支 | 来源 | 说明 |
|------|------|------|
| **feature** | develop | 新功能开发分支 |
| **hotfix** | master | 正式环境紧急问题修复 |
| **hotfix-g** | gray | 灰度环境紧急问题修复 |

## Tag 命名规范

格式：`<前缀><年份>.<周数>.<构建号>`

| 前缀 | 说明 |
|------|------|
| `pc-f` | feature 功能提测 |
| `pc-t` | release 集成测试 |
| `pc-g` | gray 灰度发布 |
| `pc-v` | master 全量发布 |

示例：`pc-g2021.09.03` 表示 pc 工程的 2021 年第 9 周第三次构建

## Rebase 使用原则

**推荐使用场景：**
- 独立开发的分支，将源分支合并到该分支
- 本地分支同步远程分支修改

**禁止使用场景：**
- 多人协作的需求分支

示例：
```bash
# 自己的需求分支，同步 develop
git rebase develop

# 本地 develop 同步远程
git pull --rebase
```

## 其他命令

```bash
# 查看 abc-flow 版本
git abc -v

# 查看帮助
git abc -h

# 更新 git-abc
git abc update
```

## 命令支持情况对照

| 操作 | 交互式命令 | 非交互式脚本 | Claude Code 推荐 |
|-----|-----------|------------|----------------|
| Feature 操作 | `git abc feature start/finish` | - | ✅ 交互式 |
| Hotfix 操作 | `git abc hotfix start/finish` | - | ✅ 交互式 |
| RC 操作 | `git abc rc start/finish` | - | ✅ 交互式 |
| Tag 配置 | `git abc tag config <前缀>` | - | ✅ 交互式 |
| Tag 创建 | `git abc tag create v` | `tag_create.py v --deps xxx` | ✅ **非交互式** |
| MR 创建 | `git abc mr create` | `mr_create.py -t xxx -T xxx -r xxx` | ✅ **非交互式** |

> **提示**：在 Claude Code 中，优先使用非交互式脚本创建 Tag 和 MR，避免终端阻塞。
