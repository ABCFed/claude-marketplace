# GetFileBlame - 获取文件 blame 信息

---
source: https://help.aliyun.com/zh/yunxiao/developer-reference/getfileblame-get-file-blame-information
category: code-management
downloaded_at: 2026-01-26T14:56:56.580754
---

# GetFileBlame - 获取文件 blame 信息

获取文件 blame 信息。

## 适用版本

企业标准版

## 服务接入点与授权信息

获取服务接入点，替换 API 请求语法中的 <domain> ：服务接入点（domain）。

获取个人访问令牌，具体操作，请参见获取个人访问令牌。

获取organizationId，请前往组织管理后台的基本信息页面获取组织 ID 。

| 产品   | 资源  | 所需权限 |
|------|-----|------|
| 代码管理 | 文件  | 只读   |

## 请求语法

```
GET https://{domain}/oapi/v1/codeup/organizations/{organizationId}/repositories/{repositoryId}/files/{filePath}/blame
```

## 请求头

| 参数              | 类型     | 是否必填 | 描述      | 示例值                          |
|-----------------|--------|------|---------|------------------------------|
| x-yunxiao-token | string | 是    | 个人访问令牌。 | pt-0fh3****0fbG_35af****0484 |

## 请求参数

| 参数             | 类型     | 位置    | 是否必填 | 描述                                 | 示例值                                          |
|----------------|--------|-------|------|------------------------------------|----------------------------------------------|
| organizationId | string | path  | 是    | 组织 ID。                             | 60d54f3daccf2bbd6659f3ad                     |
| repositoryId   | string | path  | 是    | 代码库 ID 或者 URL-Encoder 编码的全路径。      | 2813489或者60de7a6852743a5162b5f957%2FDemoRepo |
| filePath       | string | path  | 是    | 文件路径，需使用 URL-Encoder 编码进行处理。       | test.txt 或者 src%2Fmain.java                  |
| ref            | string | query | 是    | 指定引用名，一般为分支名，可为分支名、标签名和 CommitSHA。 | master                                       |

## 请求示例

```curl
curl -X 'GET' \
  'https://{domain}/oapi/v1/codeup/organizations/60d54f3daccf2bbd6659f3ad/repositories/2813489或者60de7a6852743a5162b5f957%2FDemoRepo/files/test.txt或者src%2Fmain.java/blame?ref=master' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'
```

## 返回参数

| 参数          | 类型            | 描述                                                      | 示例值                                      |
|-------------|---------------|---------------------------------------------------------|------------------------------------------|
| -           | array         |                                                         |                                          |
| -           | object        |                                                         |                                          |
| commit      | object        |                                                         |                                          |
| authorEmail | string        | 作者邮箱。                                                   | username@example.com                     |
| authorName  | string        | 作者姓名。                                                   | commiter-codeup                          |
| createdAt   | string        | 提交时间。                                                   | 2025-01-01T01:01:01+08:00                |
| id          | string        | 提交 ID。                                                  | ff4fb5ac6d1f44f452654336d2dba468ae6c8d04 |
| shortId     | string        | 短提交 ID。                                                 | ff4fb5ac                                 |
| title       | string        | 标题，提交的第一行内容。                                            | 提交标题                                     |
| userId      | string        | 云效用户 ID（在 Codeup 提交的 OpenAPI 中涉及到用户 ID 之处，均应该使用该用户 ID）。 | 62c795c9cf*****b468af8                   |
| contents    | array[string] |                                                         |                                          |
| start       | integer       | 起始行号。                                                   | 1                                        |

## 返回示例

```json
[
    {
        "commit": {
            "authorEmail": "username@example.com",
            "authorName": "commiter-codeup",
            "createdAt": "2025-01-01T01:01:01+08:00",
            "id": "ff4fb5ac6d1f44f452654336d2dba468ae6c8d04",
            "shortId": "ff4fb5ac",
            "title": "提交标题",
            "userId": "62c795c9cf*****b468af8"
        },
        "contents": [
        ],
        "start": 1
    }
]
```

## 错误码

访问错误码中心查看 API 相关错误码。
