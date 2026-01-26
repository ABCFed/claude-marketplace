# CommitMultipleFiles - 多文件变更提交

---
source: https://help.aliyun.com/zh/yunxiao/developer-reference/commitmultiplefiles-multi-file-change-commit
category: code-management
downloaded_at: 2026-01-26T14:34:27.782227
---

# CommitMultipleFiles - 多文件变更提交

## 服务接入点与授权信息

获取服务接入点，替换 API 请求语法中的{domain} ：服务接入点（domain）。

获取个人访问令牌，具体操作，请参见获取个人访问令牌。

获取organizationId，请前往组织管理后台的基本信息页面获取组织 ID 。

访问错误码中心查看 API 相关错误码。

- 获取服务接入点，替换 API 请求语法中的{domain} ：服务接入点（domain）。
- 获取个人访问令牌，具体操作，请参见获取个人访问令牌。
- 获取organizationId，请前往组织管理后台的基本信息页面获取组织 ID 。

- create：创建文件
- delete：删除文件
- move：移动文件
- update：更新文件

| 适用版本 | 企业标准版 |
|------|-------|

| 产品   | 资源  | 所需权限 |
|------|-----|------|
| 代码管理 | 文件  | 读写   |

| 参数              | 类型     | 是否必填 | 描述      | 示例值                          |
|-----------------|--------|------|---------|------------------------------|
| x-yunxiao-token | string | 是    | 个人访问令牌。 | pt-0fh3****0fbG_35af****0484 |

| 参数             | 类型     | 位置   | 是否必填 | 描述                                                                    | 示例值                                          |
|----------------|--------|------|------|-----------------------------------------------------------------------|----------------------------------------------|
| organizationId | string | path | 是    | 组织 ID。                                                                | 60d54f3daccf2bbd6659f3ad                     |
| repositoryId   | string | path | 是    | 代码库 ID 或者 URL-Encoder 编码的全路径。                                         | 2813489或者60de7a6852743a5162b5f957%2FDemoRepo |
| -              | object | body | 是    |                                                                       |                                              |
| actions        | array  | body | 是    |                                                                       |                                              |
| -              | object | body | 是    |                                                                       |                                              |
| action         | string | body | 是    | 操作类型 create：创建文件 delete：删除文件 move：移动文件 update：更新文件                    | create                                       |
| content        | string | body | 否    | 文件内容。create 和 update 必填。 注意：若是更新操作，则是完全覆盖，即传入的content内容，会直接覆盖原有的文件内容。 |                                              |
| file_path      | string | body | 是    | 文件路径。                                                                 | src/test.java                                |
| previous_path  | string | body | 否    | 变更前的文件路径。move 必填。                                                     | src/main/test.java                           |
| branch         | string | body | 是    | 分支名称。                                                                 | demo-branch                                  |
| commit_message | string | body | 是    | 提交信息，非空，不超过102400个字符。                                                 | create a file with content                   |

| 参数             | 类型            | 描述           | 示例值                                               |
|----------------|---------------|--------------|---------------------------------------------------|
| -              | object        |              |                                                   |
| authorEmail    | string        | 作者邮箱。        | username@example.com                              |
| authorName     | string        | 作者姓名。        | codeup-name                                       |
| authoredDate   | string        | 作者提交时间。      | 2024-10-05T15:30:45Z                              |
| committedDate  | string        | 提交者提交时间。     | 2024-10-05T15:30:45Z                              |
| committerEmail | string        | 提交者邮箱。       | username@example.com                              |
| committerName  | string        | 提交者姓名。       | codeup-name                                       |
| id             | string        | 提交 ID。       | 6da8c14b5a9102998148b7ea35f96507d5304f74          |
| message        | string        | 提交内容。        | commit message detail                             |
| parentIds      | array[string] | 父提交 ID。      | [“3fdaf119cf76539c1a47de0074ac02927ef4c8e1”]      |
| shortId        | string        | 代码组路径。       | 6da8c14b                                          |
| stats          | object        |              |                                                   |
| additions      | integer       | 新增行数。        | 5                                                 |
| deletions      | integer       | 删除行数。        | 5                                                 |
| total          | integer       | 总行数。         | 10                                                |
| title          | string        | 标题，提交的第一行内容。 | commit msg title                                  |
| webUrl         | string        | 页面访问地址。      | http://exmaple.com/example_repo/commit/commit_sha |

```
POST https://{domain}/oapi/v1/codeup/organizations/{organizationId}/repositories/{repositoryId}/multipleFiles
```

```
curl -X 'POST' \
  'https://{domain}/oapi/v1/codeup/organizations/60d54f3daccf2bbd6659f3ad/repositories/2813489或者60de7a6852743a5162b5f957%2FDemoRepo/multipleFiles' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484' \
  --data '
    {
        "actions": [
            {
                "action": "create",
                "content": "xxx",
                "file_path": "src/test.java"
            },
            {
                "action": "create",
                "content": "xxx",
                "file_path": "test.java"
            },
            {
                "action": "update",
                "content": "xxx",
                "file_path": "test1.java"
            },
            {
                "action": "delete",
                "file_path": "test2.java"
            },
            {
                "action": "move",
                "file_path": "src/test3.java",
                "previous_path": "test3.java"
            }
        ],
        "branch": "demo-branch",
        "commit_message": "commit message detail"
    }'
```

```
{
    "authorEmail": "username@example.com",
    "authorName": "codeup-name",
    "authoredDate": "2024-10-05T15:30:45Z",
    "committedDate": "2024-10-05T15:30:45Z",
    "committerEmail": "username@example.com",
    "committerName": "codeup-name",
    "id": "6da8c14b5a9102998148b7ea35f96507d5304f74",
    "message": "commit message detail",
    "parentIds": ["3fdaf119cf76539c1a47de0074ac02927ef4c8e1"],
    "shortId": "6da8c14b",
    "stats": {
        "additions": 5,
        "deletions": 5,
        "total": 10
    },
    "title": "commit msg title",
    "webUrl": "http://exmaple.com/example_repo/commit/commit_sha"
}
```

## 服务接入点与授权信息

获取服务接入点，替换 API 请求语法中的{domain} ：服务接入点（domain）。

获取个人访问令牌，具体操作，请参见获取个人访问令牌。

获取organizationId，请前往组织管理后台的基本信息页面获取组织 ID 。

访问错误码中心查看 API 相关错误码。

- 获取服务接入点，替换 API 请求语法中的{domain} ：服务接入点（domain）。
- 获取个人访问令牌，具体操作，请参见获取个人访问令牌。
- 获取organizationId，请前往组织管理后台的基本信息页面获取组织 ID 。

- create：创建文件
- delete：删除文件
- move：移动文件
- update：更新文件

| 适用版本 | 企业标准版 |
|------|-------|

| 产品   | 资源  | 所需权限 |
|------|-----|------|
| 代码管理 | 文件  | 读写   |

| 参数              | 类型     | 是否必填 | 描述      | 示例值                          |
|-----------------|--------|------|---------|------------------------------|
| x-yunxiao-token | string | 是    | 个人访问令牌。 | pt-0fh3****0fbG_35af****0484 |

| 参数             | 类型     | 位置   | 是否必填 | 描述                                                                    | 示例值                                          |
|----------------|--------|------|------|-----------------------------------------------------------------------|----------------------------------------------|
| organizationId | string | path | 是    | 组织 ID。                                                                | 60d54f3daccf2bbd6659f3ad                     |
| repositoryId   | string | path | 是    | 代码库 ID 或者 URL-Encoder 编码的全路径。                                         | 2813489或者60de7a6852743a5162b5f957%2FDemoRepo |
| -              | object | body | 是    |                                                                       |                                              |
| actions        | array  | body | 是    |                                                                       |                                              |
| -              | object | body | 是    |                                                                       |                                              |
| action         | string | body | 是    | 操作类型 create：创建文件 delete：删除文件 move：移动文件 update：更新文件                    | create                                       |
| content        | string | body | 否    | 文件内容。create 和 update 必填。 注意：若是更新操作，则是完全覆盖，即传入的content内容，会直接覆盖原有的文件内容。 |                                              |
| file_path      | string | body | 是    | 文件路径。                                                                 | src/test.java                                |
| previous_path  | string | body | 否    | 变更前的文件路径。move 必填。                                                     | src/main/test.java                           |
| branch         | string | body | 是    | 分支名称。                                                                 | demo-branch                                  |
| commit_message | string | body | 是    | 提交信息，非空，不超过102400个字符。                                                 | create a file with content                   |

| 参数             | 类型            | 描述           | 示例值                                               |
|----------------|---------------|--------------|---------------------------------------------------|
| -              | object        |              |                                                   |
| authorEmail    | string        | 作者邮箱。        | username@example.com                              |
| authorName     | string        | 作者姓名。        | codeup-name                                       |
| authoredDate   | string        | 作者提交时间。      | 2024-10-05T15:30:45Z                              |
| committedDate  | string        | 提交者提交时间。     | 2024-10-05T15:30:45Z                              |
| committerEmail | string        | 提交者邮箱。       | username@example.com                              |
| committerName  | string        | 提交者姓名。       | codeup-name                                       |
| id             | string        | 提交 ID。       | 6da8c14b5a9102998148b7ea35f96507d5304f74          |
| message        | string        | 提交内容。        | commit message detail                             |
| parentIds      | array[string] | 父提交 ID。      | [“3fdaf119cf76539c1a47de0074ac02927ef4c8e1”]      |
| shortId        | string        | 代码组路径。       | 6da8c14b                                          |
| stats          | object        |              |                                                   |
| additions      | integer       | 新增行数。        | 5                                                 |
| deletions      | integer       | 删除行数。        | 5                                                 |
| total          | integer       | 总行数。         | 10                                                |
| title          | string        | 标题，提交的第一行内容。 | commit msg title                                  |
| webUrl         | string        | 页面访问地址。      | http://exmaple.com/example_repo/commit/commit_sha |

```
POST https://{domain}/oapi/v1/codeup/organizations/{organizationId}/repositories/{repositoryId}/multipleFiles
```

```
curl -X 'POST' \
  'https://{domain}/oapi/v1/codeup/organizations/60d54f3daccf2bbd6659f3ad/repositories/2813489或者60de7a6852743a5162b5f957%2FDemoRepo/multipleFiles' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484' \
  --data '
    {
        "actions": [
            {
                "action": "create",
                "content": "xxx",
                "file_path": "src/test.java"
            },
            {
                "action": "create",
                "content": "xxx",
                "file_path": "test.java"
            },
            {
                "action": "update",
                "content": "xxx",
                "file_path": "test1.java"
            },
            {
                "action": "delete",
                "file_path": "test2.java"
            },
            {
                "action": "move",
                "file_path": "src/test3.java",
                "previous_path": "test3.java"
            }
        ],
        "branch": "demo-branch",
        "commit_message": "commit message detail"
    }'
```

```
{
    "authorEmail": "username@example.com",
    "authorName": "codeup-name",
    "authoredDate": "2024-10-05T15:30:45Z",
    "committedDate": "2024-10-05T15:30:45Z",
    "committerEmail": "username@example.com",
    "committerName": "codeup-name",
    "id": "6da8c14b5a9102998148b7ea35f96507d5304f74",
    "message": "commit message detail",
    "parentIds": ["3fdaf119cf76539c1a47de0074ac02927ef4c8e1"],
    "shortId": "6da8c14b",
    "stats": {
        "additions": 5,
        "deletions": 5,
        "total": 10
    },
    "title": "commit msg title",
    "webUrl": "http://exmaple.com/example_repo/commit/commit_sha"
}
```

## 服务接入点与授权信息

获取服务接入点，替换 API 请求语法中的{domain} ：服务接入点（domain）。

获取个人访问令牌，具体操作，请参见获取个人访问令牌。

获取organizationId，请前往组织管理后台的基本信息页面获取组织 ID 。

访问错误码中心查看 API 相关错误码。

- 获取服务接入点，替换 API 请求语法中的{domain} ：服务接入点（domain）。
- 获取个人访问令牌，具体操作，请参见获取个人访问令牌。
- 获取organizationId，请前往组织管理后台的基本信息页面获取组织 ID 。

- create：创建文件
- delete：删除文件
- move：移动文件
- update：更新文件

| 适用版本 | 企业标准版 |
|------|-------|

| 产品   | 资源  | 所需权限 |
|------|-----|------|
| 代码管理 | 文件  | 读写   |

| 参数              | 类型     | 是否必填 | 描述      | 示例值                          |
|-----------------|--------|------|---------|------------------------------|
| x-yunxiao-token | string | 是    | 个人访问令牌。 | pt-0fh3****0fbG_35af****0484 |

| 参数             | 类型     | 位置   | 是否必填 | 描述                                                                    | 示例值                                          |
|----------------|--------|------|------|-----------------------------------------------------------------------|----------------------------------------------|
| organizationId | string | path | 是    | 组织 ID。                                                                | 60d54f3daccf2bbd6659f3ad                     |
| repositoryId   | string | path | 是    | 代码库 ID 或者 URL-Encoder 编码的全路径。                                         | 2813489或者60de7a6852743a5162b5f957%2FDemoRepo |
| -              | object | body | 是    |                                                                       |                                              |
| actions        | array  | body | 是    |                                                                       |                                              |
| -              | object | body | 是    |                                                                       |                                              |
| action         | string | body | 是    | 操作类型 create：创建文件 delete：删除文件 move：移动文件 update：更新文件                    | create                                       |
| content        | string | body | 否    | 文件内容。create 和 update 必填。 注意：若是更新操作，则是完全覆盖，即传入的content内容，会直接覆盖原有的文件内容。 |                                              |
| file_path      | string | body | 是    | 文件路径。                                                                 | src/test.java                                |
| previous_path  | string | body | 否    | 变更前的文件路径。move 必填。                                                     | src/main/test.java                           |
| branch         | string | body | 是    | 分支名称。                                                                 | demo-branch                                  |
| commit_message | string | body | 是    | 提交信息，非空，不超过102400个字符。                                                 | create a file with content                   |

| 参数             | 类型            | 描述           | 示例值                                               |
|----------------|---------------|--------------|---------------------------------------------------|
| -              | object        |              |                                                   |
| authorEmail    | string        | 作者邮箱。        | username@example.com                              |
| authorName     | string        | 作者姓名。        | codeup-name                                       |
| authoredDate   | string        | 作者提交时间。      | 2024-10-05T15:30:45Z                              |
| committedDate  | string        | 提交者提交时间。     | 2024-10-05T15:30:45Z                              |
| committerEmail | string        | 提交者邮箱。       | username@example.com                              |
| committerName  | string        | 提交者姓名。       | codeup-name                                       |
| id             | string        | 提交 ID。       | 6da8c14b5a9102998148b7ea35f96507d5304f74          |
| message        | string        | 提交内容。        | commit message detail                             |
| parentIds      | array[string] | 父提交 ID。      | [“3fdaf119cf76539c1a47de0074ac02927ef4c8e1”]      |
| shortId        | string        | 代码组路径。       | 6da8c14b                                          |
| stats          | object        |              |                                                   |
| additions      | integer       | 新增行数。        | 5                                                 |
| deletions      | integer       | 删除行数。        | 5                                                 |
| total          | integer       | 总行数。         | 10                                                |
| title          | string        | 标题，提交的第一行内容。 | commit msg title                                  |
| webUrl         | string        | 页面访问地址。      | http://exmaple.com/example_repo/commit/commit_sha |

```
POST https://{domain}/oapi/v1/codeup/organizations/{organizationId}/repositories/{repositoryId}/multipleFiles
```

```
curl -X 'POST' \
  'https://{domain}/oapi/v1/codeup/organizations/60d54f3daccf2bbd6659f3ad/repositories/2813489或者60de7a6852743a5162b5f957%2FDemoRepo/multipleFiles' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484' \
  --data '
    {
        "actions": [
            {
                "action": "create",
                "content": "xxx",
                "file_path": "src/test.java"
            },
            {
                "action": "create",
                "content": "xxx",
                "file_path": "test.java"
            },
            {
                "action": "update",
                "content": "xxx",
                "file_path": "test1.java"
            },
            {
                "action": "delete",
                "file_path": "test2.java"
            },
            {
                "action": "move",
                "file_path": "src/test3.java",
                "previous_path": "test3.java"
            }
        ],
        "branch": "demo-branch",
        "commit_message": "commit message detail"
    }'
```

```
{
    "authorEmail": "username@example.com",
    "authorName": "codeup-name",
    "authoredDate": "2024-10-05T15:30:45Z",
    "committedDate": "2024-10-05T15:30:45Z",
    "committerEmail": "username@example.com",
    "committerName": "codeup-name",
    "id": "6da8c14b5a9102998148b7ea35f96507d5304f74",
    "message": "commit message detail",
    "parentIds": ["3fdaf119cf76539c1a47de0074ac02927ef4c8e1"],
    "shortId": "6da8c14b",
    "stats": {
        "additions": 5,
        "deletions": 5,
        "total": 10
    },
    "title": "commit msg title",
    "webUrl": "http://exmaple.com/example_repo/commit/commit_sha"
}
```

