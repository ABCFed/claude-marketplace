# ListTags - 查询标签列表

---
source: https://help.aliyun.com/zh/yunxiao/developer-reference/listtags
category: code-management
downloaded_at: 2026-01-26T14:34:41.895224
---

# ListTags - 查询标签列表

## 服务接入点与授权信息

获取服务接入点，替换 API 请求语法中的 <domain> ：服务接入点（domain）。

获取个人访问令牌，具体操作，请参见获取个人访问令牌。

获取organizationId，请前往组织管理后台的基本信息页面获取组织 ID 。

- 获取服务接入点，替换 API 请求语法中的 <domain> ：服务接入点（domain）。
- 获取个人访问令牌，具体操作，请参见获取个人访问令牌。
- 获取organizationId，请前往组织管理后台的基本信息页面获取组织 ID 。

| 产品   | 资源  | 所需权限 |
|------|-----|------|
| 代码管理 | 标签  | 只读   |

## 请求语法

```
GET https://{domain}/oapi/v1/codeup/organizations/{organizationId}/repositories/{repositoryId}/tags
```

## 请求头

| 参数              | 类型     | 是否必填 | 描述      | 示例值                          |
|-----------------|--------|------|---------|------------------------------|
| x-yunxiao-token | string | 是    | 个人访问令牌。 | pt-0fh3****0fbG_35af****0484 |

## 请求参数

| 参数             | 类型      | 位置    | 是否必填 | 描述                                         | 示例值                      |
|----------------|---------|-------|------|--------------------------------------------|--------------------------|
| organizationId | string  | path  | 是    | 组织 ID。                                     | 611b75680fc7bf0dbe1dce55 |
| repositoryId   | string  | path  | 是    | 代码库 ID 或者 URL-Encoder 编码的全路径。              | 2709413                  |
| page           | integer | query | 否    | 页码，默认从1开始，一般不要超过150页。                      | 2                        |
| perPage        | integer | query | 否    | 每页大小，默认20，取值范围【1，100】。                     | 20                       |
| search         | string  | query | 否    | 搜索关键字。                                     | Demo                     |
| sort           | string  | query | 否    | 排序方式：desc-降序，asc-升序，默认 desc。               | desc                     |
| orderBy        | string  | query | 否    | 排序字段：name-按名称排序，create-按创建时间排序，默认为 create。 | create                   |

## 请求示例

```
curl -X 'GET' \
  'https://openapi-rdc.aliyuncs.com/oapi/v1/codeup/organizations/{organizationId}/repositories/{repositoryId}/tags?page=<page>&perPage=<perPage>&search=<search>&sort=<sort>&orderBy=<orderBy>' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'
```

## 返回参数

| 参数             | 类型            | 描述           | 示例值                                      |
|----------------|---------------|--------------|------------------------------------------|
| -              | array         |              |                                          |
| -              | object        |              |                                          |
| commit         | object        | 提交信息。        |                                          |
| authorEmail    | string        | 作者邮箱。        | username@example.com                     |
| authorName     | string        | 作者姓名。        | 阿里云云效                                    |
| authoredDate   | string        | 作者提交时间。      | 2023-01-03T15:41:26+08:00                |
| committedDate  | string        | 提交者提交时间。     | 2023-01-03T15:41:26+08:00                |
| committerEmail | string        | 提交者邮箱。       | username@example.com                     |
| committerName  | string        | 提交者姓名。       | 阿里云云效Committer                           |
| id             | string        | 提交 ID。       | de02b625ba8488f92eb204bcb3773a40c1b4ddac |
| message        | string        | 提交内容。        | ""                                       |
| parentIds      | array[string] | 父提交 ID。      | de02b                                    |
| shortId        | string        | 代码组路径。       | de02b625                                 |
| stats          | object        | 变更行数信息。      |                                          |
| additions      | integer       | 增加行数。        | 0                                        |
| deletions      | integer       | 删除行数。        | 0                                        |
| total          | integer       | 总变动行数。       | 0                                        |
| title          | string        | 标题，提交的第一行内容。 | 提交标题                                     |
| webUrl         | string        | 页面访问地址。      | ""                                       |
| id             | string        | 主键 ID。       | de02b625ba8488f92eb204bcb3773a40c1b4ddac |
| message        | string        | 标签提交信息。      | ""                                       |
| name           | string        | 标签名。         | tag v1.0                                 |
| release        | object        | 发行版本信息。      |                                          |
| description    | string        | 描述信息。        | ""                                       |
| tagName        | string        | 标签名。         | v1.0                                     |

## 返回示例

```
[
    {
        "commit": {
            "authorEmail": "username@example.com",
            "authorName": "阿里云云效",
            "authoredDate": "2023-01-03T15:41:26+08:00",
            "committedDate": "2023-01-03T15:41:26+08:00",
            "committerEmail": "username@example.com",
            "committerName": "阿里云云效Committer",
            "id": "de02b625ba8488f92eb204bcb3773a40c1b4ddac",
            "message": "",
            "parentIds": [
                "de02b"
            ],
            "shortId": "de02b625",
            "stats": {
                "additions": 0,
                "deletions": 0,
                "total": 0
            },
            "title": "提交标题",
            "webUrl": ""
        },
        "id": "de02b625ba8488f92eb204bcb3773a40c1b4ddac",
        "message": "",
        "name": "tag v1.0",
        "release": {
            "description": "",
            "tagName": "v1.0"
        }
    }
]
```

## 响应头

| 参数            | 描述     | 示例值                                  |
|---------------|--------|--------------------------------------|
| x-next-page   | 下一页。   | 2                                    |
| x-page        | 当前页。   | 1                                    |
| x-per-page    | 每页大小。  | 20                                   |
| x-prev-page   | 前一页。   | 0                                    |
| x-request-id  | 请求 ID。 | 37294673-00CA-5B8B-914F-A8B35511E90A |
| x-total       | 总数。    | 10                                   |
| x-total-pages | 总分页数。  | 1                                    |

## 错误码

访问错误码中心查看 API 相关错误码。

