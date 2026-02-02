# 非交互式命令使用指南

由于 `git abc` 命令使用交互式输入（inquirer），在 Claude Code 中无法直接执行。以下是替代方案。

## 问题说明

以下命令会进入交互式等待，无法在 Claude Code 中直接使用：
- `git abc tag create` - 需要选择 tag 类型、填写信息
- `git abc mr create` - 需要选择目标分支、填写标题、选择评审者

## 解决方案：使用 Python 脚本

提供了两个 Python 脚本，直接调用 API，避免交互式输入：

### Tag 创建 (`scripts/tag_create.py`)

直接调用 API 创建 tag，无需交互式输入。

#### 安装依赖

```bash
pip install requests
```

#### 使用方法

```bash
# 基本用法
~/.claude/skills/git-flow/scripts/tag_create.py v --deps "无" --operation "无"

# 需求提测
~/.claude/skills/git-flow/scripts/tag_create.py f \
  --deps "无" \
  --operation "无" \
  --remark "feat: 实现新功能" \
  --tapd-id "1122044681001112866"

# 指定业务线和前缀
~/.claude/skills/git-flow/scripts/tag_create.py v \
  -b abc-oa \
  --prefix pc \
  --deps "abc-auth" \
  --operation "无"

# Hotfix 模式
~/.claude/skills/git-flow/scripts/tag_create.py v \
  --hotfix \
  --deps "abc-auth" \
  --operation "刷数据"

# 仅创建 tag，跳过上车/提测
~/.claude/skills/git-flow/scripts/tag_create.py v --skipdeploy
```

#### 参数说明

| 参数 | 说明 | 必填 |
|-----|------|-----|
| `tag_type` | Tag 类型 (f/t/v/g/p) | ✅ |
| `--deps` | 依赖的服务 | ✅ (可部署/提测) |
| `--operation` | 需要的操作 | ✅ (可部署/提测) |
| `--remark` | 备注/说明 | ✅ (提测时) |
| `--tapd-id` | 关联的 TAPD ID | ❌ (f tag) |
| `-b, --business` | 业务线 | ❌ (默认 abc-his) |
| `--prefix` | Tag 前缀 | ❌ (从 git config 读取) |
| `--hotfix` | Hotfix 模式 | ❌ |
| `--skipdeploy` | 跳过上车/提测 | ❌ |

### MR 创建 (`scripts/mr_create.py`)

直接调用 Codeup API 创建 MR，无需交互式输入。

#### 配置

首次使用需要配置：

```bash
# 运行配置命令
git abc mr config
```

或手动创建配置文件 `~/.abc-fed-config/mr.json`：

```json
{
  "yunxiaoToken": "你的云效 Token",
  "webhookUrl": "企业微信 Webhook URL"
}
```

#### 使用方法

```bash
# 基本用法
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

# 跳过企业微信通知
~/.claude/skills/git-flow/scripts/mr_create.py \
  -t develop \
  -T "feat: xxx" \
  -r 张三 \
  --skip-notify
```

#### 参数说明

| 参数 | 说明 | 必填 |
|-----|------|-----|
| `-t, --target` | 目标分支 | ✅ |
| `-T, --title` | MR 标题 | ✅ |
| `-r, --reviewers` | 评审者姓名（多个用空格分隔） | ✅ |
| `-d, --description` | MR 描述 | ❌ |
| `--skip-notify` | 跳过企业微信通知 | ❌ |

## Claude Code 中的使用流程

### Tag 创建流程

1. 检查当前分支
2. 询问 tag 类型
3. 验证分支约束
4. 询问上车/提测信息
5. 执行 Python 脚本

```bash
# 示例命令
~/.claude/skills/git-flow/scripts/tag_create.py v \
  --deps "abc-auth" \
  --operation "无"
```

### MR 创建流程

1. 收集必要信息：
   - 目标分支
   - MR 标题
   - MR 描述
   - 评审者

2. 执行 Python 脚本：

```bash
~/.claude/skills/git-flow/scripts/mr_create.py \
  -t develop \
  -T "feat: 新功能开发" \
  -r 张三 李四
```

## 与原命令的对比

| 操作 | 原命令 | 新脚本 |
|-----|--------|--------|
| 创建 v tag | `git abc tag create v`（交互式填写信息） | `tag_create.py v --deps xxx --operation xxx` |
| 创建 f tag | `git abc tag create f`（交互式填写信息） | `tag_create.py f --deps xxx --operation xxx --remark xxx` |
| 创建 MR | `git abc mr create`（交互式） | `mr_create.py -t develop -T xxx -r xxx` |

## 优势

1. **无需交互式输入** - 所有参数通过命令行传递
2. **可直接在 Claude Code 中执行** - 不会阻塞等待输入
3. **功能完整** - 支持所有原命令的功能
4. **更好的错误处理** - 清晰的错误提示

## 注意事项

1. **Python 依赖** - 需要安装 `requests` 库
2. **Git 配置** - Tag 创建需要配置 `abcflow.prefix.tag`
3. **MR 配置** - MR 创建需要配置云效 Token 和 Webhook

## 当前推荐做法

**对于 Tag 创建：**
- ✅ 使用 `tag_create.py` 脚本
- 或直接指定类型 `git abc tag create <类型>`（但后续仍需交互式填写信息）

**对于 MR 创建：**
- ✅ 使用 `mr_create.py` 脚本
- 或使用 `git abc mr create` 手动在终端执行

**对于 Tag 配置：**
- ✅ 使用 `git abc tag config <前缀>` 直接指定
