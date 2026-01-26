# ListBranches - 查询分支列表

---
source: https://help.aliyun.com/zh/yunxiao/developer-reference/listbranches-query-the-list-of-branches
category: code-management
downloaded_at: 2026-01-26T14:33:47.652525
---

# ListBranches - 查询分支列表

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
| 代码管理 | 分支  | 只读   |

## 请求语法

```
GET https://{domain}/oapi/v1/codeup/organizations/{organizationId}/repositories/{repositoryId}/branches
```

## 请求头

| 参数              | 类型     | 是否必填 | 描述      | 示例值                          |
|-----------------|--------|------|---------|------------------------------|
| x-yunxiao-token | string | 是    | 个人访问令牌。 | pt-0fh3****0fbG_35af****0484 |

## 请求参数

| 参数             | 类型      | 位置    | 是否必填 | 描述                                                                                | 示例值          |
|----------------|---------|-------|------|-----------------------------------------------------------------------------------|--------------|
| organizationId | string  | path  | 是    | 组织 ID。                                                                            | 99d1****71d4 |
| repositoryId   | string  | path  | 是    | 代码库 ID 或者 URL-Encoder 编码的全路径。                                                     | 2334743      |
| page           | integer | query | 否    | 页码。                                                                               | 2            |
| perPage        | integer | query | 否    | 每页大小。                                                                             | 10           |
| sort           | string  | query | 否    | 排序方式：name_asc - 名称升序，name_desc - 名称降序；updated_asc - 更新时间升序；updated_desc - 更新时间降序。 | name_desc    |
| search         | string  | query | 否    | 查询条件。                                                                             | search       |

## 请求示例

```
curl -X 'GET' \
  'https://{domain}/oapi/v1/codeup/organizations/{organizationId}/repositories/{repositoryId}/branches?page=<page>&perPage=<perPage>&sort=<sort>&search=<search>' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'
```

## 返回参数

| 参数             | 类型            | 描述           | 示例值                                      |
|----------------|---------------|--------------|------------------------------------------|
| -              | array         |              |                                          |
| -              | object        |              |                                          |
| commit         | object        | 分支最近一次提交信息。  |                                          |
| authorEmail    | string        | 作者邮箱。        | username@example.com                     |
| authorName     | string        | 作者姓名。        | 阿里云云效                                    |
| authoredDate   | string        | 作者提交时间。      | 2022-03-18 08:00:00                      |
| committedDate  | string        | 提交者提交时间。     | 2022-03-18 09:00:00                      |
| committerEmail | string        | 提交者邮箱。       | username@example.com                     |
| committerName  | string        | 提交者姓名。       | 阿里云云效Committer                           |
| id             | string        | 提交 ID。       | e0297d8fb0393c833a8531e7cc8832739e3cba6d |
| message        | string        | 提交内容。        | 修改main.txt文件                             |
| parentIds      | array[string] | 父提交 ID。      | de02b625ba8488f92eb204bcb3773a40c1b4ddac |
| shortId        | string        | 代码组路径。       | e0297d8f                                 |
| stats          | object        | 提交变更行统计。     |                                          |
| additions      | integer       | 增加行数。        | 5                                        |
| deletions      | integer       | 删除行数。        | 2                                        |
| total          | integer       | 总变动行数。       | 7                                        |
| title          | string        | 标题，提交的第一行内容。 | 修改main.txt文件                             |
| webUrl         | string        | 页面访问地址。      | ""                                       |
| defaultBranch  | boolean       | 是否是默认分支。     | false                                    |
| name           | string        | 分支名称。        | master                                   |
| protected      | boolean       | 是否是保护分支。     | false                                    |
| webUrl         | string        | 页面访问 URL。    | ""                                       |

## 返回示例

```
[
    {
        "commit": {
            "authorEmail": "username@example.com",
            "authorName": "阿里云云效",
            "authoredDate": "2022-03-18 08:00:00",
            "committedDate": "2022-03-18 09:00:00",
            "committerEmail": "username@example.com",
            "committerName": "阿里云云效Committer",
            "id": "e0297d8fb0393c833a8531e7cc8832739e3cba6d",
            "message": "修改main.txt文件",
            "parentIds": [
                
            ],
            "shortId": "e0297d8f",
            "stats": {
                "additions": 0,
                "deletions": 0,
                "total": 0
            },
            "title": "修改main.txt文件",
            "webUrl": "\"\""
        },
        "defaultBranch": false,
        "name": "master",
        "protected": false,
        "webUrl": "\"\""
    }
]
```

## 错误码

访问错误码中心查看 API 相关错误码。

