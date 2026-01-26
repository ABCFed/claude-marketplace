# CreateTag - 创建标签

---
source: https://help.aliyun.com/zh/yunxiao/developer-reference/createtag
category: code-management
downloaded_at: 2026-01-26T14:34:34.510167
---

# CreateTag - 创建标签

## 服务接入点与授权信息

获取服务接入点，替换 API 请求语法中的 <domain> ：服务接入点（domain）。

获取个人访问令牌，具体操作，请参见获取个人访问令牌。

获取organizationId，请前往组织管理后台的基本信息页面获取组织 ID 。

- 获取服务接入点，替换 API 请求语法中的 <domain> ：服务接入点（domain）。
- 获取个人访问令牌，具体操作，请参见获取个人访问令牌。
- 获取organizationId，请前往组织管理后台的基本信息页面获取组织 ID 。

| 产品   | 资源  | 所需权限 |
|------|-----|------|
| 代码管理 | 标签  | 读写   |

## 请求语法

```
POST https://{domain}/oapi/v1/codeup/organizations/{organizationId}/repositories/{repositoryId}/tags
```

## 请求头

| 参数              | 类型     | 是否必填 | 描述      | 示例值                          |
|-----------------|--------|------|---------|------------------------------|
| x-yunxiao-token | string | 是    | 个人访问令牌。 | pt-0fh3****0fbG_35af****0484 |

## 请求参数

| 参数             | 类型     | 位置    | 是否必填 | 描述                                    | 示例值                     |
|----------------|--------|-------|------|---------------------------------------|-------------------------|
| organizationId | string | path  | 是    | 组织 ID。                                | 5ebbc0228123212b59xxxxx |
| repositoryId   | string | path  | 是    | 代码库 ID 或者 URL-Encoder 编码的全路径。         | 2080972                 |
| tagName        | string | query | 是    | 标签名称（若包含特殊符号，需使用 URL-Encoder 进行编码处理）。 | v1.0                    |
| ref            | string | query | 是    | 来源，可为分支名称、另一个标签名称或者 CommitSHA。        | master                  |
| message        | string | query | 否    | 描述信息。                                 | ""                      |

## 请求示例

```
curl -X 'POST' \
  'https://test.rdc.aliyuncs.com/oapi/v1/codeup/organizations/{organizationId}/repositories/{repositoryId}/tags?tagName=<tagName>&ref=<ref>&message=<message>' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'
```

## 返回参数

| 参数             | 类型            | 描述           | 示例值                                      |
|----------------|---------------|--------------|------------------------------------------|
| -              | object        |              |                                          |
| commit         | object        | 提交信息。        |                                          |
| authorEmail    | string        | 作者邮箱。        | username@example.com                     |
| authorName     | string        | 作者姓名。        | 阿里云云效                                    |
| authoredDate   | string        | 作者提交时间。      | 2023-01-03T15:41:26+08:00                |
| committedDate  | string        | 提交者提交时间。     | 2023-01-03T15:41:26+08:00                |
| committerEmail | string        | 提交者邮箱。       | username@example.com                     |
| committerName  | string        | 提交者姓名。       | 阿里云云效committer                           |
| id             | string        | 提交 ID。       | e0297d8fb0393c833a8531e7cc8832739e3cba6d |
| message        | string        | 提交内容。        | ""                                       |
| parentIds      | array[string] | 父提交 ID。      | e0297                                    |
| shortId        | string        | 代码组路径。       | e0297d8f                                 |
| stats          | object        | 变更行数信息。      |                                          |
| additions      | integer       | 增加行数。        | 0                                        |
| deletions      | integer       | 删除行数。        | 0                                        |
| total          | integer       | 总变动行数。       | 0                                        |
| title          | string        | 标题，提交的第一行内容。 | 提交标题                                     |
| webUrl         | string        | 页面访问地址。      | ""                                       |
| id             | integer       | 主键 ID，无业务意义。 | 0                                        |
| message        | string        | 标签提交信息。      | ""                                       |
| name           | string        | 标签名。         | v1.0                                     |
| release        | object        | 发行版本信息。      |                                          |
| description    | string        | 描述信息。        | ""                                       |
| tagName        | string        | 标签名。         | v1.0                                     |

## 返回示例

```
{
    "commit": {
        "authorEmail": "username@example.com",
        "authorName": "阿里云云效",
        "authoredDate": "2023-01-03T15:41:26+08:00",
        "committedDate": "2023-01-03T15:41:26+08:00",
        "committerEmail": "username@example.com",
        "committerName": "阿里云云效committer",
        "id": "e0297d8fb0393c833a8531e7cc8832739e3cba6d",
        "message": "",
        "parentIds": [
            "e0297"
        ],
        "shortId": "e0297d8f",
        "stats": {
            "additions": 0,
            "deletions": 0,
            "total": 0
        },
        "title": "提交标题",
        "webUrl": ""
    },
    "id": 0,
    "message": "",
    "name": "v1.0",
    "release": {
        "description": "",
        "tagName": "v1.0"
    }
}
```

## 错误码

访问错误码中心查看 API 相关错误码。

