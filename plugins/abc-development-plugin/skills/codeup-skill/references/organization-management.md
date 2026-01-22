# Organization Management API 参考

## 用户信息

### 获取当前用户

```bash
# 获取当前用户（个人姓名）
python codeup.py get_current_user

# 获取当前用户（指定组织，返回企业姓名）
python codeup.py get_current_user --org_id <org_id>
```

### 列出用户所属组织

```bash
python codeup.py list_organizations
```

## 部门管理

### 列出部门

```bash
python codeup.py list_departments --org_id <org_id>
```

### 获取部门详情

```bash
python codeup.py get_department --org_id <org_id> --dept_id <dept_id>
```

## 成员管理

### 列出组织成员

```bash
python codeup.py list_members --org_id <org_id> \
    [--name <member_name>] \
    [--provider <third_party>] \
    [--extern_uid <uid>] \
    [--state normal|blocked|deleted] \
    [--max_results 20]
```

### 获取成员详情

```bash
python codeup.py get_organization_member --org_id <org_id> --account_id <uid>
```

### 搜索成员

```bash
python codeup.py search_members --org_id <org_id> --query <keyword>
```

### 列出角色

```bash
python codeup.py list_roles --org_id <org_id>
```

## 环境变量

| 变量名 | 说明 |
|--------|------|
| `YUNXIAO_ACCESS_TOKEN` | 访问令牌 (必填) |

## 常见工作流

### 1. 获取组织信息和成员列表

```bash
# 获取组织列表
python codeup.py list_organizations

# 列出所有成员
python codeup.py list_members --org_id <org_id>
```

### 2. 搜索特定成员

```bash
python codeup.py search_members --org_id <org_id> --query "张三"
```

### 3. 查看成员详情

```bash
# 获取特定成员信息
python codeup.py get_organization_member --org_id <org_id> --account_id 123456789
```

### 4. 查看组织架构

```bash
# 列出部门
python codeup.py list_departments --org_id <org_id>

# 查看各部门成员
python codeup.py list_members --org_id <org_id>
```
