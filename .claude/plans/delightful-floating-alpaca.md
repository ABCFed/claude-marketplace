# Codeup API 修复计划

## 问题汇总

经过对比官方文档 `docs/yunxiao-api/docs/` 和当前 `codeup_client.py` 实现，发现以下问题需要修复：

---

### 1. `list_branches` - 参数名称错误

**位置:** `codeup_client.py:208-214`

**问题:** 参数名应为 `perPage`，当前使用了 `limit`

| 当前代码 | 官方文档要求 |
|---------|-------------|
| `{"page": page, "limit": limit}` | `{"page": page, "perPage": perPage}` |

**修复:** 将 `limit` 改为 `perPage`

---

### 2. `create_file` - filePath 未 URL 编码

**位置:** `codeup_client.py:235-260`

**问题:** `filePath` 在请求体中，但官方要求 `filePath` 需要先 URL 编码（包含特殊符号时）

**修复:** 添加 `filePath = requests.utils.quote(file_path, safe="")`

---

### 3. `delete_file` - commitMessage 位置错误

**位置:** `codeup_client.py:290-310`

**问题:** `commitMessage` 应放在 `query` 参数中，当前放在了 body 的 data 里

| 当前代码 | 官方文档要求 |
|---------|-------------|
| `data={"branch": ..., "commitMessage": ...}` | `params={"branch": ..., "commitMessage": ...}` |

**修复:** 将 `commitMessage` 从 `data` 移到 `params`

---

### 4. `list_merge_request_comments` - API Path 错误

**位置:** `codeup_client.py:486-501`

**问题:** API Path 应该是 `/comments/list`，而不是 `/comments`

| 当前代码 | 官方文档要求 |
|---------|-------------|
| `/changeRequests/{local_id}/comments` | `/changeRequests/{local_id}/comments/list` |

**修复:** 修改 endpoint 为 `/changeRequests/{local_id}/comments/list`

---

### 5. `list_merge_request_comments` - 请求方式应为 POST

**位置:** `codeup_client.py:486-501`

**问题:** 官方文档显示这个 API 使用 **POST** 请求

| 当前代码 | 官方文档要求 |
|---------|-------------|
| `"GET"` | `"POST"` |

**修复:** 将方法改为 POST

---

### 6. `list_merge_request_comments` - 返回类型应为 list

**位置:** `codeup_client.py:486-501`

**问题:** 官方文档显示返回类型是 `array`，当前返回类型是 `dict`

**修复:** 返回类型改为 `list`

---

### 7. `create_merge_request_comment` - patchset_biz_id 必填校验

**位置:** `codeup_client.py:437-484`

**问题:** 当 `comment_type` 为 `INLINE_COMMENT` 时，`patchset_biz_id` 是必填参数

**修复:** 添加参数校验，当类型为 INLINE_COMMENT 但未提供 patchset_biz_id 时抛出错误

---

### 8. `list_merge_request_patch_sets` - API Path 错误

**位置:** `codeup_client.py:503-514`

**问题:** API Path 应该是 `/diffs/patches`，而不是 `/patchsets`

| 当前代码 | 官方文档要求 |
|---------|-------------|
| `/changeRequests/{local_id}/patchsets` | `/changeRequests/{local_id}/diffs/patches` |

**修复:** 修改 endpoint 为 `/changeRequests/{local_id}/diffs/patches`

---

## 修改文件

- `plugins/abc-development-plugin/skills/codeup-skill/scripts/codeup_client.py`

## 验证方式

运行以下命令验证修复：

```bash
# 检查环境变量
export YUNXIAO_ACCESS_TOKEN="your_token"

# 测试 list_branches
python codeup.py list_branches --org_id xxx --repo_id xxx --page 1 --per_page 20

# 测试 delete_file
python codeup.py delete_file --org_id xxx --repo_id xxx --file_path xxx --branch master --message "test"

# 测试 list_merge_request_comments
python codeup.py list_merge_request_comments --org_id xxx --repo_id xxx --local_id 1

# 测试 list_merge_request_patch_sets
python codeup.py list_merge_request_patch_sets --org_id xxx --repo_id xxx --local_id 1
```
