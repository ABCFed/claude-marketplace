# ListChangeRequests - 查询合并请求列表

---
source: https://help.aliyun.com/zh/yunxiao/developer-reference/listchangerequests-query-the-list-of-merge-requests
category: code-management
downloaded_at: 2026-01-26T14:35:33.573208
---

# ListChangeRequests - 查询合并请求列表

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

	

合并请求

	

只读

| 产品   | 资源   | 所需权限 |
|------|------|------|
| 代码管理 | 合并请求 | 只读   |

## 请求语法

```
GET https://{domain}/oapi/v1/codeup/organizations/{organizationId}/changeRequests
```

## 请求头

| 参数              | 类型     | 是否必填 | 描述      | 示例值                          |
|-----------------|--------|------|---------|------------------------------|
| x-yunxiao-token | string | 是    | 个人访问令牌。 | pt-0fh3****0fbG_35af****0484 |

## 请求参数

| 参数             | 类型      | 位置    | 是否必填 | 描述                                                   | 示例值                  |
|----------------|---------|-------|------|------------------------------------------------------|----------------------|
| organizationId | string  | path  | 是    | 组织 ID。                                               | 99d1****71d4         |
| page           | integer | query | 否    | 页码。                                                  | 1                    |
| perPage        | integer | query | 否    | 每页大小。                                                | 10                   |
| projectIds     | string  | query | 否    | 代码库 ID 或者路径列表，多个以逗号分隔。                               | 2308912, 2308913     |
| authorIds      | string  | query | 否    | 创建者用户 ID 列表，多个以逗号分隔。                                 | 1234567890           |
| reviewerIds    | string  | query | 否    | 评审人用户 ID 列表，多个以逗号分隔。                                 | 1234567890123        |
| state          | string  | query | 否    | 合并请求筛选状态：opened，merged，closed，默认为 null，即查询全部状态。      | opened               |
| search         | string  | query | 否    | 标题关键字搜索。                                             | test-search          |
| orderBy        | string  | query | 否    | 排序字段，仅支持：created_at - 创建时间；updated_at - 更新时间，默认排序字段。 | updated_at           |
| sort           | string  | query | 否    | 排序方式：asc - 升序；desc - 降序，默认排序方式。                      | desc                 |
| createdBefore  | string  | query | 否    | 起始创建时间，时间格式为 ISO 8601。                               | 2019-03-15T08:00:00Z |
| createdAfter   | string  | query | 否    | 截止创建时间，时间格式为 ISO 8601。                               | 2019-03-15T08:00:00Z |

## 请求示例

```
curl -X 'GET' \
  'https://test.rdc.aliyuncs.com/oapi/v1/codeup/organizations/{organizationId}/changeRequests?page=<page>&perPage=<perPage>&projectIds=<projectIds>&authorIds=<authorIds>&reviewerIds=<reviewerIds>&state=<state>&search=<search>&orderBy=<orderBy>&sort=<sort>&createdBefore=<createdBefore>&createdAfter=<createdAfter>' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'
```

## 返回参数

| 参数                     | 类型      | 描述                                                                                      | 示例值                                                                                |
|------------------------|---------|-----------------------------------------------------------------------------------------|------------------------------------------------------------------------------------|
| -                      | array   |                                                                                         |                                                                                    |
| -                      | object  |                                                                                         |                                                                                    |
| author                 | object  | 用户信息。                                                                                   |                                                                                    |
| avatar                 | string  | 用户头像地址。                                                                                 | https://tcs-devops.aliyuncs.com/thumbnail/112afcb7a6a35c3f67f1bea827c4/w/100/h/100 |
| email                  | string  | 用户邮箱。                                                                                   | username@example.com                                                               |
| name                   | string  | 用户名称。                                                                                   | test-review-user                                                                   |
| state                  | string  | 用户状态：active - 激活可用；blocked - 阻塞暂不可用。                                                    | active                                                                             |
| userId                 | string  | 云效用户 ID。                                                                                | 62c795c9cf*****b468af8                                                             |
| username               | string  | 用户登录名。                                                                                  | root-test-review-user                                                              |
| createdAt              | string  | 创建时间。                                                                                   | 2023-05-30T02:53:36Z                                                               |
| creationMethod         | string  | 合并请求的创建方式：WEB - 页面创建；COMMAND_LINE - 命令行创建。                                              | WEB                                                                                |
| description            | string  | 描述。                                                                                     | 新的特性或需求                                                                            |
| detailUrl              | string  | 合并请求详情地址。                                                                               | xxx                                                                                |
| hasConflict            | boolean | 是否有冲突。                                                                                  | false                                                                              |
| localId                | integer | 合并请求局部 ID，表示当前代码库中第几个合并请求 ID。                                                           | 1                                                                                  |
| mergedRevision         | string  | 合并版本（提交 ID），仅已合并状态才有值。                                                                  | 1a072f5367c21f9de3464b8c0ee8546e47764d2d                                           |
| projectId              | integer | 代码库 ID。                                                                                 | 2369234                                                                            |
| reviewers              | array   | 评审人列表。                                                                                  |                                                                                    |
| -                      | object  |                                                                                         |                                                                                    |
| avatar                 | string  | 用户头像地址。                                                                                 | https://tcs-devops.aliyuncs.com/thumbnail/112afcb7a6a35c3f67f1bea827c4/w/100/h/100 |
| email                  | string  | 用户邮箱。                                                                                   | username@example.com                                                               |
| hasCommented           | boolean | 是否已经评论过。                                                                                | false                                                                              |
| hasReviewed            | boolean | 是否评审过。                                                                                  | false                                                                              |
| name                   | string  | 用户名称。                                                                                   | test-codeup                                                                        |
| reviewOpinionStatus    | string  | 评审意见：PASS - 通过；NOT_PASS - 不通过。                                                          | PASS                                                                               |
| reviewTime             | string  | 评审时间。                                                                                   | 2023-05-30T02:53:36Z                                                               |
| state                  | string  | 用户状态：active - 激活可用；blocked - 阻塞暂不可用。                                                    | active                                                                             |
| userId                 | string  | 云效用户 ID。                                                                                | 62c795c9cf*****b468af8                                                             |
| username               | string  | 用户登录名。                                                                                  | root-test-codeup                                                                   |
| sourceBranch           | string  | 源分支。                                                                                    | test-merge-source-branch                                                           |
| sourceProjectId        | integer | 评审分支所在的代码库 ID。                                                                          | 2876119                                                                            |
| sourceType             | string  | 评审分支类型：BRANCH、COMMIT。                                                                   | BRANCH                                                                             |
| sshUrl                 | string  | 仓库 SSH 克隆地址。                                                                            | git@xxx:xxx/test/test.git                                                          |
| state                  | string  | 合并请求状态：UNDER_DEV - 开发中；UNDER_REVIEW - 评审中；TO_BE_MERGED - 待合并；CLOSED - 已关闭；MERGED - 已合并。 | UNDER_DEV                                                                          |
| supportMergeFFOnly     | boolean | 是否支持 fast-forward-only 合并方式。                                                            | false                                                                              |
| targetBranch           | string  | 目标分支。                                                                                   | test-merge-target-branch                                                           |
| targetProjectId        | integer | 目标分支所在的代码库 ID。                                                                          | 2876119                                                                            |
| targetType             | string  | 目标分支类型：BRANCH、COMMIT。                                                                   | BRANCH                                                                             |
| title                  | string  | 标题。                                                                                     | 测试标题                                                                               |
| totalCommentCount      | integer | 总评论数。                                                                                   | 10                                                                                 |
| unResolvedCommentCount | integer | 未解决评论数。                                                                                 | 1                                                                                  |
| updatedAt              | string  | 更新时间。                                                                                   | 2023-05-30T02:53:36Z                                                               |
| webUrl                 | string  | Web 地址。                                                                                 | ""                                                                                 |
| workInProgress         | boolean | WIP 标识，即是否在开发中。                                                                         | false                                                                              |

## 返回示例

```
[
    {
        "author": {
            "avatar": "https://tcs-devops.aliyuncs.com/thumbnail/112afcb7a6a35c3f67f1bea827c4/w/100/h/100",
            "email": "username@example.com",
            "name": "test-codeup",
            "state": "active",
            "userId": "62c795c9cf*****b468af8",
            "username": "root-test-codeup"
        },
        "createdAt": "2023-05-30T02:53:36Z",
        "creationMethod": "WEB",
        "description": "新的特性或需求",
        "detailUrl": "xxx",
        "hasConflict": false,
        "localId": 1,
        "mergedRevision": "1a072f5367c21f9de3464b8c0ee8546e47764d2d",
        "projectId": 2876119,
        "reviewers": [
            {
                "avatar": "https://tcs-devops.aliyuncs.com/thumbnail/112afcb7a6a35c3f67f1bea827c4/w/100/h/100",
                "email": "username@example.com",
                "hasCommented": false,
                "hasReviewed": false,
                "name": "test-review-user",
                "reviewOpinionStatus": "PASS",
                "reviewTime": "2023-05-30T02:53:36Z",
                "state": "active",
                "userId": "62c795c9cf*****b468af8",
                "username": "root-test-review-user"
            }
        ],
        "sourceBranch": "test-merge-source-branch",
        "sourceProjectId": 2876119,
        "sourceType": "BRANCH",
        "sshUrl": "git@xxx:xxx/test/test.git",
        "state": "UNDER_DEV",
        "supportMergeFFOnly": false,
        "targetBranch": "test-merge-source-branch",
        "targetProjectId": 2876119,
        "targetType": "BRANCH",
        "title": "test-合并请求标题",
        "totalCommentCount": 10,
        "unResolvedCommentCount": 1,
        "updatedAt": "2023-05-30T02:53:36Z",
        "webUrl": "xxx",
        "workInProgress": false
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

