# ListGroupRepositories - 查询代码组下的代码库列表

---
source: https://help.aliyun.com/zh/yunxiao/developer-reference/listgrouprepostions-query-the-list-of-code-libraries-under-a-code-group
category: code-management
downloaded_at: 2026-01-26T14:33:32.834233
---

# ListGroupRepositories - 查询代码组下的代码库列表

## 服务接入点与授权信息

获取服务接入点（domain），替换 API 请求语法中的 <domain>

获取个人访问令牌

获取organizationId，请前往组织管理后台的基本信息页面获取组织 ID

- 获取服务接入点（domain），替换 API 请求语法中的 <domain>
- 获取个人访问令牌
- 获取organizationId，请前往组织管理后台的基本信息页面获取组织 ID

| 产品   | 资源  | 所需权限 |
|------|-----|------|
| 代码管理 | 代码组 | 只读   |

## 请求语法

```
GET https://{domain}/oapi/v1/codeup/organizations/{organizationId}/groups/{groupId}/repositories
```

## 请求头

| 参数              | 类型     | 是否必填 | 描述      | 示例值                          |
|-----------------|--------|------|---------|------------------------------|
| x-yunxiao-token | string | 是    | 个人访问令牌。 | pt-0fh3****0fbG_35af****0484 |

## 请求参数

| 参数               | 类型      | 位置    | 是否必填 | 描述                      | 示例值                      |
|------------------|---------|-------|------|-------------------------|--------------------------|
| organizationId   | string  | path  | 是    | 企业 ID。                  | 60d54f3daccf2bbd6659f3ad |
| groupId          | integer | path  | 是    | 代码组 ID。                 | 1                        |
| page             | integer | query | 否    | 页码，默认值为1。               | 1                        |
| perPage          | integer | query | 否    | 每页大小，默认值为20。            | 20                       |
| search           | string  | query | 否    | 搜索关键字，用于搜索代码库名称。        | TestRepo                 |
| includeSubgroups | boolean | query | 否    | 是否包含子组下的代码库，默认值为 false。 | false                    |

## 请求示例

```
curl -X 'GET' \
  'https://{domain}/oapi/v1/codeup/organizations/60d54f3daccf2bbd6659f3ad/groups/1/repositories?page=1&perPage=20&search=TestRepo&includeSubgroups=false' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'
```

## 返回参数

| 参数                | 类型      | 描述                                                                                | 示例值                                      |
|-------------------|---------|-----------------------------------------------------------------------------------|------------------------------------------|
| -                 | array   |                                                                                   |                                          |
| -                 | object  |                                                                                   |                                          |
| accessLevel       | integer | 当前用户在该代码库上的权限类型，可能的值：[20 30 40]。                                                  | 40                                       |
| archived          | boolean | 代码库是否归档。                                                                          | false                                    |
| avatarUrl         | string  | 头像地址。                                                                             | https://example/example/w/100/h/100      |
| createdAt         | string  | 创建时间。                                                                             | 2024-10-05T15:30:45Z                     |
| creatorId         | integer | 代码库创建者。                                                                           | 1                                        |
| demoProject       | boolean | 是否是 demo 库。                                                                       | false                                    |
| description       | string  | 代码库描述。                                                                            | demo repo                                |
| encrypted         | boolean | 是否加密。                                                                             | false                                    |
| id                | integer | 代码库 ID。                                                                           | 2813489                                  |
| lastActivityAt    | string  | 最后活跃时间。                                                                           | 2024-10-05T15:30:45Z                     |
| name              | string  | 代码库名称。                                                                            | demo-repo                                |
| nameWithNamespace | string  | 代码库完整名称（含完整组名称）。                                                                  | 60de7a6852743a5162b5f957 / DemoRepo      |
| namespaceId       | integer | 上级路径的 ID。                                                                         | 2813489                                  |
| path              | string  | 代码库路径。                                                                            | demo-repo                                |
| pathWithNamespace | string  | 代码库完整路径（含完整组路径）。                                                                  | 60de7a6852743a5162b5f957/DemoRepo        |
| repositorySize    | string  | 代码库大小(MB)。                                                                        | 1                                        |
| starCount         | integer | 被收藏的数量。                                                                           | 1                                        |
| starred           | boolean | 是否被当前用户收藏。                                                                        | false                                    |
| updatedAt         | string  | 最近更新时间。                                                                           | 2024-10-05T15:30:45Z                     |
| visibility        | string  | 可见性，private 标识私有的，internal 标识组织内公开，public 表示全平台公开，可能的值：[private internal public]。 | private                                  |
| webUrl            | string  | 页面访问时的 URL。                                                                       | http://example.com/org-demo/example-repo |

## 返回示例

```
[
    {
        "accessLevel": 40,
        "archived": false,
        "avatarUrl": "https://example/example/w/100/h/100",
        "createdAt": "2024-10-05T15:30:45Z",
        "creatorId": 1,
        "demoProject": false,
        "description": "demo repo",
        "encrypted": false,
        "id": 2813489,
        "lastActivityAt": "2024-10-05T15:30:45Z",
        "name": "demo-repo",
        "nameWithNamespace": "60de7a6852743a5162b5f957 / DemoRepo",
        "namespaceId": 2813489,
        "path": "demo-repo",
        "pathWithNamespace": "60de7a6852743a5162b5f957/DemoRepo",
        "repositorySize": "1",
        "starCount": 1,
        "starred": false,
        "updatedAt": "2024-10-05T15:30:45Z",
        "visibility": "private",
        "webUrl": "http://example.com/org-demo/example-repo"
    }
]
```

## 响应头

| 参数            | 描述     | 示例值                                  |
|---------------|--------|--------------------------------------|
| x-next-page   | 下一页。   | 3                                    |
| x-page        | 当前页。   | 2                                    |
| x-per-page    | 每页大小。  | 20                                   |
| x-prev-page   | 前一页。   | 1                                    |
| x-request-id  | 请求 ID。 | 37294673-00CA-5B8B-914F-A8B35511E90A |
| x-total       | 总数。    | 50                                   |
| x-total-pages | 总分页数。  | 3                                    |

## 错误码

访问错误码中心查看 API 相关错误码。

