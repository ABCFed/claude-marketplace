---
name: codeup
description: 阿里云云效 Codeup 代码仓库管理工具集。使用场景包括：(1) 代码仓库操作 - 分支管理、文件操作、代码对比、合并请求/MR管理 (2) 组织管理 - 部门管理、成员查询、角色管理 (3) 操作 codeup 仓库、分支、MR、合并请求 (4) 查询云效组织成员、部门列表
---

# Codeup Skill

本 skill 提供与云效（Codeup）平台交互的 Python 脚本工具，统一通过 `codeup.py` 调用。

## 环境配置

使用前需要配置以下环境变量：
```bash
export YUNXIAO_ACCESS_TOKEN="你的个人访问令牌"
```

获取访问令牌：
1. 登录阿里云控制台
2. 进入云效（Codeup）
3. 设置 -> 访问令牌管理 -> 创建个人访问令牌

## 使用方式

```bash
cd ~/.claude/skills/codeup-skill/scripts
python codeup.py <command> [参数]
```

所有命令默认输出 JSON 格式结果。

## 命令列表

### 用户与组织
| 命令 | 说明 |
|------|------|
| `get_current_user` | 获取当前用户信息 |
| `list_organizations` | 列出用户所属组织（获取 org_id） |

### 部门与成员
| 命令 | 说明 |
|------|------|
| `list_departments` | 列出部门 |
| `get_department` | 获取部门详情 |
| `list_members` | 列出组织成员 |
| `get_organization_member` | 获取成员详情 |
| `search_members` | 搜索成员 |
| `list_roles` | 列出角色 |

### 仓库操作
| 命令 | 说明 |
|------|------|
| `get_repository` | 获取仓库详情 |
| `list_repositories` | 列出仓库 |

### 分支操作
| 命令 | 说明 |
|------|------|
| `get_branch` | 获取分支详情 |
| `create_branch` | 创建分支 |
| `delete_branch` | 删除分支 |
| `list_branches` | 列出分支 |

### 文件操作
| 命令 | 说明 |
|------|------|
| `get_file` | 获取文件内容 |
| `create_file` | 创建文件 |
| `update_file` | 更新文件 |
| `delete_file` | 删除文件 |
| `list_files` | 列出文件树 |
| `compare` | 对比代码差异 |

### 合并请求
| 命令 | 说明 |
|------|------|
| `get_merge_request` | 获取 MR 详情 |
| `list_merge_requests` | 列出 MR |
| `create_merge_request` | 创建 MR |
| `close_merge_request` | 关闭 MR |
| `create_merge_request_comment` | 添加 MR 评论 |
| `list_merge_request_comments` | 列出 MR 评论 |
| `list_merge_request_patch_sets` | 列出 MR 补丁集 |

## 使用示例

### 查询组织信息

```bash
# 获取当前用户
python codeup.py get_current_user

# 列出用户所属组织（获取 org_id）
python codeup.py list_organizations
```

### 组织成员管理

```bash
# 列出部门
python codeup.py list_departments --org_id 62d62893487c500c27f72e36

# 获取部门详情
python codeup.py get_department --org_id 62d62893487c500c27f72e36 --dept_id 68d910db15dfc6c8604fccb4

# 列出所有成员
python codeup.py list_members --org_id 62d62893487c500c27f72e36

# 获取成员详情
python codeup.py get_organization_member --org_id 62d62893487c500c27f72e36 --member_id 639fe0e38d9a873a30aad3df

# 搜索成员
python codeup.py search_members --org_id 62d62893487c500c27f72e36 --query "姓名"

# 列出角色
python codeup.py list_roles --org_id 62d62893487c500c27f72e36
```

### 仓库与分支管理

```bash
# 列出仓库
python codeup.py list_repositories --org_id 62d62893487c500c27f72e36

# 获取仓库详情
python codeup.py get_repository --org_id 62d62893487c500c27f72e36 --repo_id 5822285

# 列出分支
python codeup.py list_branches --org_id 62d62893487c500c27f72e36 --repo_id 5822285

# 创建分支
python codeup.py create_branch \
    --org_id 62d62893487c500c27f72e36 \
    --repo_id 5822285 \
    --branch_name feature/new-feature \
    --source_branch master

# 删除分支
python codeup.py delete_branch \
    --org_id 62d62893487c500c27f72e36 \
    --repo_id 5822285 \
    --branch_name feature/old-feature
```

### 文件操作

```bash
# 获取文件内容
python codeup.py get_file \
    --org_id 62d62893487c500c27f72e36 \
    --repo_id 5822285 \
    --file_path README.md \
    --branch master

# 创建文件
python codeup.py create_file \
    --org_id 62d62893487c500c27f72e36 \
    --repo_id 5822285 \
    --file_path docs/new-doc.md \
    --content "# 新文档\n\n这是内容" \
    --branch feature/new-feature \
    --message "Add new documentation"

# 更新文件
python codeup.py update_file \
    --org_id 62d62893487c500c27f72e36 \
    --repo_id 5822285 \
    --file_path README.md \
    --content "# 更新后的内容" \
    --message "Update README"

# 列出文件
python codeup.py list_files \
    --org_id 62d62893487c500c27f72e36 \
    --repo_id 5822285 \
    --path src \
    --branch master

# 对比代码
python codeup.py compare \
    --org_id 62d62893487c500c27f72e36 \
    --repo_id 5822285 \
    --from feature/new-feature \
    --to master
```

### 合并请求管理

```bash
# 列出 MR
python codeup.py list_merge_requests \
    --org_id 62d62893487c500c27f72e36 \
    --repo_id 5822285

# 列出打开的 MR
python codeup.py list_merge_requests \
    --org_id 62d62893487c500c27f72e36 \
    --repo_id 5822285 \
    --state opened

# 获取 MR 详情
python codeup.py get_merge_request \
    --org_id 62d62893487c500c27f72e36 \
    --repo_id 5822285 \
    --local_id 584

# 创建 MR
python codeup.py create_merge_request \
    --org_id 62d62893487c500c27f72e36 \
    --repo_id 5822285 \
    --title "Feature: 新功能" \
    --source_branch feature/new-feature \
    --target_branch master \
    --description "实现用户登录功能"

# 关闭 MR
python codeup.py close_merge_request \
    --org_id 62d62893487c500c27f72e36 \
    --repo_id 5822285 \
    --local_id 584

# 添加 MR 评论
python codeup.py create_merge_request_comment \
    --org_id 62d62893487c500c27f72e36 \
    --repo_id 5822285 \
    --local_id 584 \
    --content "代码审查通过"

# 列出 MR 评论
python codeup.py list_merge_request_comments \
    --org_id 62d62893487c500c27f72e36 \
    --repo_id 5822285 \
    --local_id 584

# 列出 MR 补丁集（提交）
python codeup.py list_merge_request_patch_sets \
    --org_id 62d62893487c500c27f72e36 \
    --repo_id 5822285 \
    --local_id 584
```

## 常用命令速查

```bash
# 组织成员
python codeup.py list_members --org_id 62d62893487c500c27f72e36
python codeup.py search_members --org_id 62d62893487c500c27f72e36 --query "姓名"

# 仓库操作
python codeup.py list_repositories --org_id 62d62893487c500c27f72e36
python codeup.py list_branches --org_id 62d62893487c500c27f72e36 --repo_id 5822285

# 文件操作
python codeup.py get_file --org_id 62d62893487c500c27f72e36 --repo_id 5822285 --file_path README.md

# MR 操作
python codeup.py list_merge_requests --org_id 62d62893487c500c27f72e36 --repo_id 5822285 --state opened
python codeup.py get_merge_request --org_id 62d62893487c500c27f72e36 --repo_id 5822285 --local_id 584
```

## Claude 使用方式

当用户需要与云效交互时：

1. **获取 org_id**：先调用 `list_organizations` 获取组织列表，选择目标组织
2. **获取 repo_id**：调用 `list_repositories` 列出仓库，选择目标仓库
3. **构建命令**：根据需求构建相应参数
4. **执行脚本**：使用 Bash 工具运行
5. **处理结果**：解析输出，分析数据

示例工作流：
```
用户: "查看当前组织的成员列表"

Claude:
1. cd ~/.claude/skills/codeup-skill/scripts
2. python codeup.py list_organizations  # 获取 org_id
3. python codeup.py list_members --org_id $ORG_ID  # 列出成员
4. 分析返回结果并展示
```

## 常见问题

### 1. 如何获取 org_id 和 repo_id？

```bash
# 列出用户所属组织（包含 org_id）
python codeup.py list_organizations

# 列出仓库（包含 repo_id）
python codeup.py list_repositories --org_id 62d62893487c500c27f72e36
```

### 2. 权限不足怎么办？

确保访问令牌有相应权限：
- 仓库读取权限：查看仓库、分支、文件
- 仓库写入权限：创建/更新/删除文件、创建分支
- MR 管理权限：创建/更新 MR、添加评论

### 3. 合并请求状态值

| 状态 | 说明 |
|------|------|
| `opened` | 打开中 |
| `closed` | 已关闭 |
| `merged` | 已合并 |

## 文件结构

```
codeup-skill/
├── SKILL.md
├── references/
│   ├── code-management.md          # 代码管理 API 参考
│   └── organization-management.md  # 组织管理 API 参考
└── scripts/
    ├── codeup.py              # 统一入口脚本（27个子命令）
    ├── codeup_client.py       # Codeup API 客户端
    └── requirements.txt       # 依赖：requests>=2.28.0
```
