# GetFileBlobs - 查询文件内容

---
source: https://help.aliyun.com/zh/yunxiao/developer-reference/getfileblobs
category: code-management
downloaded_at: 2026-01-26T14:34:10.204231
---

# GetFileBlobs - 查询文件内容

## 前提条件

获取服务接入点，替换 API 请求语法中的 <domain> 。关于如何获取domain，请参见服务接入点（domain）。

获取个人访问令牌，具体操作，请参见获取个人访问令牌。

获取organizationId，请前往组织管理后台的基本信息页面获取组织 ID 。

- 获取服务接入点，替换 API 请求语法中的 <domain> 。关于如何获取domain，请参见服务接入点（domain）。
- 获取个人访问令牌，具体操作，请参见获取个人访问令牌。
- 获取organizationId，请前往组织管理后台的基本信息页面获取组织 ID 。

## 与授权信息

| 产品   | 资源  | 所需权限 |
|------|-----|------|
| 代码管理 | 文件  | 只读   |

## 请求语法

```
GET https://{domain}/oapi/v1/codeup/organizations/{organizationId}/repositories/{repositoryId}/files/{filePath}
```

## 请求头

| 参数              | 类型     | 是否必填 | 描述      | 示例值                          |
|-----------------|--------|------|---------|------------------------------|
| x-yunxiao-token | string | 是    | 个人访问令牌。 | pt-0fh3****0fbG_35af****0484 |

## 请求参数

| 参数             | 类型     | 位置    | 是否必填 | 描述                                             | 示例值                       |
|----------------|--------|-------|------|------------------------------------------------|---------------------------|
| organizationId | string | path  | 是    | 组织 ID。                                         | 60de7a6852743a5162b5f957  |
| repositoryId   | string | path  | 是    | 代码库 ID 或者 URL-Encoder 编码的全路径。请参见查询代码库列表获取相关信息。 | 2744800                   |
| filePath       | string | path  | 是    | 文件路径，需使用 URL-Encoder 编码进行处理。                   | src%2Fmain%2Ftest.java    |
| ref            | string | query | 是    | 指定引用名，一般为分支名，可为分支名、标签名和 CommitSHA。             | master / tag1.0 / ecykhdd |

## 请求示例

```
curl -X 'GET' \
  'https://{domain}/oapi/v1/codeup/organizations/{organizationId}/repositories/{repositoryId}/files/{filePath}?ref={ref}' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'
```

## 返回参数

| 参数           | 类型      | 描述                            | 示例值                                      |
|--------------|---------|-------------------------------|------------------------------------------|
| -            | object  |                               |                                          |
| blobId       | string  | 文件 git object id。             | 76c3f251f414ac31f2e01faf6f2008a9d756a437 |
| commitId     | string  | 提交 ID。                        | ""                                       |
| content      | string  | 文件内容。                         | ""                                       |
| encoding     | string  | 编码规则，可为{text, base64}。        | text                                     |
| fileName     | string  | 文件名称。                         | test.java                                |
| filePath     | string  | 文件路径。                         | src/main/test.java                       |
| lastCommitId | string  | 文件最后提交的 CommitID。             | ""                                       |
| ref          | string  | 一般为分支名，可为分支名、标签名或者 CommitSHA。 | master / tag1.0 / ecykhdd                |
| size         | integer | 文件内容大小。                       | 10                                       |

## 返回示例

```
{
    "blobId": "76c3f251f414ac31f2e01faf6f2008a9d756a437",
    "commitId": "",
    "content": "",
    "encoding": "text",
    "fileName": "test.java",
    "filePath": "src/main/test.java",
    "lastCommitId": "",
    "ref": "master",
    "size": 10
}
```

## 错误码

访问错误码中心查看 API 相关错误码。

