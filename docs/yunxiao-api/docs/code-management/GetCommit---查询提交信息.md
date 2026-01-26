# GetCommit - 查询提交信息

---
source: https://help.aliyun.com/zh/yunxiao/developer-reference/getcommit-query-commit-information
category: code-management
downloaded_at: 2026-01-26T14:33:51.166157
---

# GetCommit - 查询提交信息

## 服务接入点与授权信息

获取服务接入点，替换 API 请求语法中的 <domain> ：服务接入点（domain）。

获取个人访问令牌，具体操作，请参见获取个人访问令牌。

获取organizationId，请前往组织管理后台的基本信息页面获取组织 ID 。

- 获取服务接入点，替换 API 请求语法中的 <domain> ：服务接入点（domain）。
- 获取个人访问令牌，具体操作，请参见获取个人访问令牌。
- 获取organizationId，请前往组织管理后台的基本信息页面获取组织 ID 。

产品

	

资源

	

所需权限




代码管理

	

提交

	

只读

| 产品   | 资源  | 所需权限 |
|------|-----|------|
| 代码管理 | 提交  | 只读   |

## 请求语法

```
GET https://{domain}/oapi/v1/codeup/organizations/{organizationId}/repositories/{repositoryId}/commits/{sha}
```

## 请求头

| 参数              | 类型     | 是否必填 | 描述      | 示例值                          |
|-----------------|--------|------|---------|------------------------------|
| x-yunxiao-token | string | 是    | 个人访问令牌。 | pt-0fh3****0fbG_35af****0484 |

## 请求参数

| 参数             | 类型     | 位置   | 是否必填 | 描述                            | 示例值                                      |
|----------------|--------|------|------|-------------------------------|------------------------------------------|
| organizationId | string | path | 是    | 组织 ID。                        | 99d1****71d4                             |
| repositoryId   | string | path | 是    | 代码库 ID 或者 URL-Encoder 编码的全路径。 | 2825387                                  |
| sha            | string | path | 是    | 提交 ID，即 Commit SHA 值。         | ff4fb5ac6d1f44f452654336d2dba468ae6c8d04 |

## 请求示例

```
curl -X 'GET' \
  'https://test.rdc.aliyuncs.com/oapi/v1/codeup/organizations/{organizationId}/repositories/{repositoryId}/commits/{sha}' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'
```

## 返回参数

| 参数             | 类型            | 描述           | 示例值                                      |
|----------------|---------------|--------------|------------------------------------------|
| -              | object        |              |                                          |
| authorEmail    | string        | 作者邮箱。        | username@example.com                     |
| authorName     | string        | 作者姓名。        | committer-codeup                         |
| authoredDate   | string        | 作者提交时间。      | 2022-08-08 18:09:09                      |
| committedDate  | string        | 提交者提交时间。     | 2022-03-18 15:00:02                      |
| committerEmail | string        | 提交者邮箱。       | username@example.com                     |
| committerName  | string        | 提交者姓名。       | committer-codeup                         |
| id             | string        | 提交 ID。       | ff4fb5ac6d1f44f452654336d2dba468ae6c8d04 |
| message        | string        | 提交内容。        | 提交的具体内容                                  |
| parentIds      | array[string] | 父提交 ID。      |                                          |
| shortId        | string        | 代码组路径。       | ff4fb5ac                                 |
| stats          | object        | 变更行数统计。      | false                                    |
| additions      | integer       | 增加行数。        | 5                                        |
| deletions      | integer       | 删除行数。        | 2                                        |
| total          | integer       | 总变动行数。       | 10                                       |
| title          | string        | 标题，提交的第一行内容。 | 提交标题                                     |
| webUrl         | string        | 页面访问地址。      | ""                                       |

## 返回示例

```
{
    "authorEmail": "username@example.com",
    "authorName": "committer-codeup",
    "authoredDate": "2022-08-08 18:09:09",
    "committedDate": "2022-03-18 15:00:02",
    "committerEmail": "username@example.com",
    "committerName": "committer-codeup",
    "id": "ff4fb5ac6d1f44f452654336d2dba468ae6c8d04 ",
    "message": "提交的具体内容",
    "parentIds": [
        
    ],
    "shortId": "ff4fb5ac",
    "stats": {
        "additions": 5,
        "deletions": 2,
        "total": 10
    },
    "title": "提交的具体内容",
    "webUrl": "\"\""
}
```

## 错误码

访问错误码中心查看 API 相关错误码。

