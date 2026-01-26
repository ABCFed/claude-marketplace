# ListFiles - 查询文件树

---
source: https://help.aliyun.com/zh/yunxiao/developer-reference/listfiles
category: code-management
downloaded_at: 2026-01-26T14:34:13.805121
---

# ListFiles - 查询文件树

## 前提条件

获取服务接入点，替换 API 请求语法中的 <domain> 。关于如何获取domain，请参见服务接入点（domain）。

获取个人访问令牌，具体操作，请参见获取个人访问令牌。

获取organizationId，请前往组织管理后台的基本信息页面获取组织 ID 。

- 获取服务接入点，替换 API 请求语法中的 <domain> 。关于如何获取domain，请参见服务接入点（domain）。
- 获取个人访问令牌，具体操作，请参见获取个人访问令牌。
- 获取organizationId，请前往组织管理后台的基本信息页面获取组织 ID 。

## 授权信息

| 产品   | 资源  | 所需权限 |
|------|-----|------|
| 代码管理 | 文件  | 只读   |

## 请求语法

```
GET https://{domain}/oapi/v1/codeup/organizations/{organizationId}/repositories/{repositoryId}/files/tree
```

## 请求头

| 参数              | 类型     | 是否必填 | 描述      | 示例值                          |
|-----------------|--------|------|---------|------------------------------|
| x-yunxiao-token | string | 是    | 个人访问令牌。 | pt-0fh3****0fbG_35af****0484 |

## 请求参数

| 参数             | 类型     | 位置    | 是否必填 | 描述                                                                                                     | 示例值                       |
|----------------|--------|-------|------|--------------------------------------------------------------------------------------------------------|---------------------------|
| organizationId | string | path  | 是    | 组织 ID。                                                                                                 | 624666bd54d036291ae13a36  |
| repositoryId   | string | path  | 是    | 代码库 ID 或者 URL-Encoder 编码的全路径。请参见查询代码库列表获取相关信息。                                                         | 2851516                   |
| path           | string | query | 否    | 指定查询的路径，例如需要查询 src/main 目录下的文件。需使用 URL-Encoder 编码进行处理。                                                 | src%2Fmain                |
| ref            | string | query | 否    | 指定引用名，一般为分支名，可为分支名、标签名和 CommitSHA，若不传值，则为当前代码库的默认分支，如 master。                                          | master / tag1.0 / sjjfssa |
| type           | string | query | 否    | 文件树获取方式：DIRECT - 仅获取当前目录，默认方式；RECURSIVE - 递归查找当前路径下的所有文件；FLATTEN - 扁平化展示（如果是目录，递归查找，直到子目录包含文件或多个目录为止）。 | RECURSIVE                 |

## 请求示例

```
curl -X 'GET' \
  'https://{domain}/oapi/v1/codeup/organizations/{organizationId}/repositories/{repositoryId}/files/tree?path={path}&ref={ref}&type={type}' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'
```

## 返回参数

| 参数    | 类型      | 描述                                              | 示例值                                      |
|-------|---------|-------------------------------------------------|------------------------------------------|
| -     | object  |                                                 |                                          |
| id    | string  | 文件的 git object id，是文件的唯一标识。                     | 76c3f251f414ac31f2e01faf6f2008a9d756a437 |
| isLFS | boolean | 是否是 LFS 文件。                                     | false                                    |
| mode  | string  | 类型、权限等信息，例如100644。                              | 100644                                   |
| name  | string  | 文件名称。                                           | condition.js                             |
| path  | string  | 文件路径。                                           | src/main/condition.js                    |
| type  | string  | 文件类型：tree - 目录；blob - 文件；commit - 使用 submodule。 | blob                                     |

## 返回示例

```
{
    "id": "76c3f251f414ac31f2e01faf6f2008a9d756a437",
    "isLFS": false,
    "mode": "100644",
    "name": "condition.js",
    "path": "src/main/condition.js",
    "type": "blob"
}
```

## 错误码

访问错误码中心查看 API 相关错误码。

