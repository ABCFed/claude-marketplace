# CreateBranch - 创建分支

---
source: https://help.aliyun.com/zh/yunxiao/developer-reference/createbranch-create-branch
category: code-management
downloaded_at: 2026-01-26T14:33:36.407765
---

# CreateBranch - 创建分支

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
| 代码管理 | 分支  | 读写   |

## 请求语法

```
POST https://{domain}/oapi/v1/codeup/organizations/{organizationId}/repositories/{repositoryId}/branches
```

## 请求头

| 参数              | 类型     | 是否必填 | 描述      | 示例值                          |
|-----------------|--------|------|---------|------------------------------|
| x-yunxiao-token | string | 是    | 个人访问令牌。 | pt-0fh3****0fbG_35af****0484 |

## 请求参数

| 参数             | 类型     | 位置    | 是否必填 | 描述                                                                         | 示例值                                                                |
|----------------|--------|-------|------|----------------------------------------------------------------------------|--------------------------------------------------------------------|
| organizationId | string | path  | 是    | 组织 ID。                                                                     | 99d1****71d4                                                       |
| repositoryId   | string | path  | 是    | 代码库 ID 或者 URL-Encoder 编码的全路径。                                              | 2334815                                                            |
| branch         | string | query | 是    | 创建的分支名称。                                                                   | createBranch                                                       |
| ref            | string | query | 是    | 分支创建的来源，可以为分支名称、标签名称（需使用完整的 git ref 路径，如 refs/tags/v1.0）或提交版本（commit SHA）。 | master 或 refs/tags/v1.0 或 45ede4680536406d793e0e629bc771cb9fcaa153 |

## 请求示例

示例一：从分支创建分支

示例二：从标签创建分支

- 示例一：从分支创建分支

 
curl -X 'POST' \
  'https://{domain}/oapi/v1/codeup/organizations/{organizationId}/repositories/{repositoryId}/branches?branch=demo-branch&ref=master' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'
- 示例二：从标签创建分支

 
curl -X 'POST' \
  'https://{domain}/oapi/v1/codeup/organizations/60d54f3daccf2bbd6659f3ad/repositories/2813489或者60de7a6852743a5162b5f957%2FDemoRepo/branches?branch=demo-branch&ref=refs%2Ftags%2Fv1.0' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'

```
curl -X 'POST' \
  'https://{domain}/oapi/v1/codeup/organizations/{organizationId}/repositories/{repositoryId}/branches?branch=demo-branch&ref=master' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'
```

```
curl -X 'POST' \
  'https://{domain}/oapi/v1/codeup/organizations/60d54f3daccf2bbd6659f3ad/repositories/2813489或者60de7a6852743a5162b5f957%2FDemoRepo/branches?branch=demo-branch&ref=refs%2Ftags%2Fv1.0' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'
```

示例一：从分支创建分支

示例二：从标签创建分支

- 示例一：从分支创建分支

 
curl -X 'POST' \
  'https://{domain}/oapi/v1/codeup/organizations/{organizationId}/repositories/{repositoryId}/branches?branch=demo-branch&ref=master' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'
- 示例二：从标签创建分支

 
curl -X 'POST' \
  'https://{domain}/oapi/v1/codeup/organizations/60d54f3daccf2bbd6659f3ad/repositories/2813489或者60de7a6852743a5162b5f957%2FDemoRepo/branches?branch=demo-branch&ref=refs%2Ftags%2Fv1.0' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'

```
curl -X 'POST' \
  'https://{domain}/oapi/v1/codeup/organizations/{organizationId}/repositories/{repositoryId}/branches?branch=demo-branch&ref=master' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'
```

```
curl -X 'POST' \
  'https://{domain}/oapi/v1/codeup/organizations/60d54f3daccf2bbd6659f3ad/repositories/2813489或者60de7a6852743a5162b5f957%2FDemoRepo/branches?branch=demo-branch&ref=refs%2Ftags%2Fv1.0' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'
```

```
curl -X 'POST' \
  'https://{domain}/oapi/v1/codeup/organizations/{organizationId}/repositories/{repositoryId}/branches?branch=demo-branch&ref=master' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'
```

```
curl -X 'POST' \
  'https://{domain}/oapi/v1/codeup/organizations/60d54f3daccf2bbd6659f3ad/repositories/2813489或者60de7a6852743a5162b5f957%2FDemoRepo/branches?branch=demo-branch&ref=refs%2Ftags%2Fv1.0' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'
```

```
curl -X 'POST' \
  'https://{domain}/oapi/v1/codeup/organizations/60d54f3daccf2bbd6659f3ad/repositories/2813489或者60de7a6852743a5162b5f957%2FDemoRepo/branches?branch=demo-branch&ref=refs%2Ftags%2Fv1.0' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'
```

## 返回参数

| 参数             | 类型            | 描述           | 示例值                                      |
|----------------|---------------|--------------|------------------------------------------|
| -              | object        |              |                                          |
| commit         | object        | 分支最近一次提交信息。  |                                          |
| authorEmail    | string        | 作者邮箱。        | username@example.com                     |
| authorName     | string        | 作者姓名。        | 阿里云云效                                    |
| authoredDate   | string        | 作者提交时间。      | 2022-03-18 09:00:00                      |
| committedDate  | string        | 提交者提交时间。     | 2022-03-18 10:00:00                      |
| committerEmail | string        | 提交者邮箱。       | username@example.com                     |
| committerName  | string        | 提交者姓名。       | 阿里云云效committer                           |
| id             | string        | 提交 ID。       | ff4fb5ac6d1f44f452654336d2dba468ae6c8d04 |
| message        | string        | 提交内容。        | create branch                            |
| parentIds      | array[string] | 父提交 ID。      |                                          |
| shortId        | string        | 代码组路径。       | ff4fb5ac                                 |
| stats          | object        | 提交变更行统计。     |                                          |
| additions      | integer       | 增加行数。        | 5                                        |
| deletions      | integer       | 删除行数。        | 2                                        |
| total          | integer       | 总变动行数。       | 10                                       |
| title          | string        | 标题，提交的第一行内容。 | 创建代码库分支                                  |
| webUrl         | string        | 页面访问地址。      | ""                                       |
| defaultBranch  | boolean       | 是否是默认分支。     | true                                     |
| name           | string        | 分支名称。        | createBranch                             |
| protected      | boolean       | 是否是保护分支。     | false                                    |
| webUrl         | string        | 页面访问 URL。    | ""                                       |

## 返回示例

```
{
    "commit": {
        "authorEmail": "username@example.com",
        "authorName": "阿里云云效",
        "authoredDate": "2022-03-18 09:00:00",
        "committedDate": "2022-03-18 10:00:00",
        "committerEmail": "username@example.com",
        "committerName": "阿里云云效committer",
        "id": "ff4fb5ac6d1f44f452654336d2dba468ae6c8d04",
        "message": "create branch",
        "parentIds": [
            
        ],
        "shortId": "ff4fb5ac",
        "stats": {
            "additions": 5,
            "deletions": 2,
            "total": 10
        },
        "title": "创建代码库分支",
        "webUrl": "\"\""
    },
    "defaultBranch": false,
    "name": "createBranch",
    "protected": false,
    "webUrl": "\"\""
}
```

## 错误码

访问错误码中心查看 API 相关错误码。

