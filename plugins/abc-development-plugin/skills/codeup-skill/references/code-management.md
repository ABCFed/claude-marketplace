# Code Management API 参考

## 仓库操作

### 获取仓库详情

```bash
python codeup.py get_repository --org_id <org_id> --repo_id <repo_id>
```

### 列出仓库

```bash
python codeup.py list_repositories --org_id <org_id> [--page 1] [--limit 20]
```

## 分支操作

### 获取分支详情

```bash
python codeup.py get_branch --org_id <org_id> --repo_id <repo_id> --branch_name <branch>
```

### 创建分支

```bash
python codeup.py create_branch --org_id <org_id> --repo_id <repo_id> --branch_name <new_branch> --source_branch <source>
```

### 删除分支

```bash
python codeup.py delete_branch --org_id <org_id> --repo_id <repo_id> --branch_name <branch>
```

### 列出分支

```bash
python codeup.py list_branches --org_id <org_id> --repo_id <repo_id> [--page 1] [--limit 20]
```

## 文件操作

### 获取文件内容

```bash
python codeup.py get_file --org_id <org_id> --repo_id <repo_id> --file_path <path> [--branch master]
```

### 创建文件

```bash
python codeup.py create_file --org_id <org_id> --repo_id <repo_id> --file_path <path> --content <content> [--branch master] [--message "commit message"]
```

### 更新文件

```bash
python codeup.py update_file --org_id <org_id> --repo_id <repo_id> --file_path <path> --content <content> [--branch master] [--message "commit message"]
```

### 删除文件

```bash
python codeup.py delete_file --org_id <org_id> --repo_id <repo_id> --file_path <path> [--branch master] [--message "commit message"]
```

### 列出文件

```bash
python codeup.py list_files --org_id <org_id> --repo_id <repo_id> [--path ""] [--branch master] [--page 1] [--limit 100]
```

### 对比代码

```bash
python codeup.py compare --org_id <org_id> --repo_id <repo_id> --source <source_branch> --target <target_branch>
```

## 合并请求操作

### 获取 MR 详情

```bash
python codeup.py get_merge_request --org_id <org_id> --repo_id <repo_id> --mr_id <mr_id>
```

### 列出 MR

```bash
python codeup.py list_merge_requests --org_id <org_id> --repo_id <repo_id> [--state open|closed|merged] [--page 1] [--limit 20]
```

### 创建 MR

```bash
python codeup.py create_merge_request --org_id <org_id> --repo_id <repo_id> --title <title> --source_branch <source> --target_branch <target> [--description <desc>]
```

### 添加 MR 评论

```bash
python codeup.py create_merge_request_comment --org_id <org_id> --repo_id <repo_id> --mr_id <mr_id> --content <content>
```

### 列出 MR 评论

```bash
python codeup.py list_merge_request_comments --org_id <org_id> --repo_id <repo_id> --mr_id <mr_id> [--page 1] [--limit 20]
```

### 列出 MR 补丁集

```bash
python codeup.py list_merge_request_patch_sets --org_id <org_id> --repo_id <repo_id> --mr_id <mr_id>
```
