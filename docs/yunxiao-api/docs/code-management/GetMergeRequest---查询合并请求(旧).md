# GetMergeRequest - 查询合并请求(旧)

---
source: https://help.aliyun.com/zh/yunxiao/developer-reference/getmergerequest-query-merge-request-old
category: code-management
downloaded_at: 2026-01-26T14:36:03.090553
---

# GetMergeRequest - 查询合并请求(旧)

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
GET https://{domain}/oapi/v1/codeup/organizations/{organizationId}/repositories/{repositoryId}/mergeRequests/{iid}
```

## 请求头

| 参数              | 类型     | 是否必填 | 描述      | 示例值                          |
|-----------------|--------|------|---------|------------------------------|
| x-yunxiao-token | string | 是    | 个人访问令牌。 | pt-0fh3****0fbG_35af****0484 |

## 请求参数

| 参数             | 类型      | 位置   | 是否必填 | 描述                            | 示例值                                           |
|----------------|---------|------|------|-------------------------------|-----------------------------------------------|
| organizationId | string  | path | 是    | 组织 ID。                        | 99d1****71d4                                  |
| repositoryId   | integer | path | 是    | 代码库 ID 或者 URL-Encoder 编码的全路径。 | 2835387 或 codeup-org-id%2Fcodeup-demo今天 15:29 |
| iid            | integer | path | 是    | 库内合并请求 ID。                    | 1                                             |

## 请求示例

```
curl -X 'GET' \
  'https://test.rdc.aliyuncs.com/oapi/v1/codeup/organizations/{organizationId}/repositories/{repositoryId}/mergeRequests/{iid}' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'
```

## 返回参数

| 参数                 | 类型            | 描述                                                                              | 示例值                                                                                |
|--------------------|---------------|---------------------------------------------------------------------------------|------------------------------------------------------------------------------------|
| -                  | object        |                                                                                 |                                                                                    |
| acceptedRevision   | string        | 评审通过时的版本。                                                                       |                                                                                    |
| ahead              | integer       | 源分支领先目标分支的 commit 数量。                                                           | 1                                                                                  |
| assignees          | array         | 评审人列表。                                                                          |                                                                                    |
| -                  | object        |                                                                                 |                                                                                    |
| avatar             | string        | 头像地址。                                                                           | https://tcs-devops.aliyuncs.com/thumbnail/112afcb7a6a35c3f67f1bea827c4/w/100/h/100 |
| email              | string        | 邮箱。                                                                             | username@example.com                                                               |
| id                 | integer       | 数据库主键 ID（无业务意义）。                                                                | 90452                                                                              |
| name               | string        | 用户名称。                                                                           | test-subscriber                                                                    |
| state              | string        | 用户状态，包括{active、blocked}，一般为 active。                                             | active                                                                             |
| status             | string        | 评审人的评审状态，包括：approved - 评审通过，pending - 待处理，comment - 发表过评论、点赞等。                  | approved                                                                           |
| userId             | string        | 云效用户 ID（在 codeup 的 OpenAPI 中涉及到用户 ID 之处，均应使用该用户 ID）。                            | 62c795c9cf*****b468af8                                                             |
| username           | string        | 用户名称（登录名）。                                                                      | root-test-codeup                                                                   |
| author             | object        | 用户信息。                                                                           |                                                                                    |
| avatar             | string        | 头像地址。                                                                           | https://tcs-devops.aliyuncs.com/thumbnail/112afcb7a6a35c3f67f1bea827c4/w/100/h/100 |
| email              | string        | 邮箱。                                                                             | username@example.com                                                               |
| id                 | integer       | 数据库主键 ID（无业务意义）。                                                                | 90452                                                                              |
| name               | string        | 用户名称。                                                                           | test-subscriber                                                                    |
| state              | string        | 用户状态，包括{active、blocked}，一般为 active。                                             | active                                                                             |
| userId             | string        | 云效用户 ID（在 codeup 的 OpenAPI 中涉及到用户 ID 之处，均应使用该用户 ID）。                            | 62c795c9cf*****b468af8                                                             |
| username           | string        | 用户名称（登录名）。                                                                      | root-test-codeup                                                                   |
| behind             | integer       | 目标分支领先源分支的 commit 数量。                                                           | 1                                                                                  |
| createdAt          | string        | 创建时间。                                                                           | 2023-05-30T02:53:36Z                                                               |
| creationMethod     | string        | 创建方式，包括：WEB、COMMAND，默认创建方式为 WEB。                                                | WEB                                                                                |
| description        | string        | 合并请求描述信息。                                                                       | 描述信息的具体内容                                                                          |
| detailUrl          | string        | 合并请求详情地址。                                                                       | xxx                                                                                |
| downvotes          | integer       | 不通过投票数。                                                                         | 1                                                                                  |
| id                 | integer       | 合并请求 ID。                                                                        | 123                                                                                |
| iid                | integer       | 库内合并请求 ID，表示属于代码库内的第几个合并请求 ID。                                                  |                                                                                    |
| isUsePushBlock     | boolean       | 是否开启推送拦截。                                                                       | false                                                                              |
| labels             | array[string] | 标签（label）列表。                                                                    |                                                                                    |
| mergeStatus        | string        | 合并请求合并状态，包括：unchecked-未检查，can_be_merged-待合并，cannot_be_merged-不可合并。              | unchecked                                                                          |
| mergedRevision     | string        | 合并的版本。                                                                          | 1a072f5367c21f9de3464b8c0ee8546e47764d2d                                           |
| nameWithNamespace  | string        | 代码库的全名称（包含父路径）。                                                                 | orgId / test-group / test-target-repo（斜杠两侧有空格）                                     |
| projectId          | integer       | 代码库 ID。                                                                         | 2369234                                                                            |
| sourceBranch       | string        | 源分支。                                                                            | test-merge-request                                                                 |
| sourceProjectId    | integer       | 评审分支所在的代码库 ID。                                                                  | 2369234                                                                            |
| sourceProjectName  | string        | 源库名称。                                                                           | test-codeup                                                                        |
| sourceType         | string        | 合并源类型，包括：BRANCH、COMMIT。                                                         | BRANCH                                                                             |
| sshUrlToRepo       | string        | 仓库 SSH 克隆地址。                                                                    | git@xxx:xxx/test/test.git                                                          |
| state              | string        | 合并请求状态：opened-已开启，closed-已关闭，merged-已合并，accepted-评审通过，reopened-重新打开，locked-合并中。 | opened                                                                             |
| subscribers        | array         | 订阅人列表。                                                                          |                                                                                    |
| -                  | object        | 用户信息。                                                                           |                                                                                    |
| avatar             | string        | 头像地址。                                                                           | https://tcs-devops.aliyuncs.com/thumbnail/112afcb7a6a35c3f67f1bea827c4/w/100/h/100 |
| email              | string        | 邮箱。                                                                             | username@example.com                                                               |
| id                 | integer       | 数据库主键 ID（无业务意义）。                                                                | 123                                                                                |
| name               | string        | 用户名称。                                                                           | test-subscriber                                                                    |
| state              | string        | 用户状态，包括{active、blocked}，一般为 active。                                             | active                                                                             |
| userId             | string        | 云效用户 ID（在 codeup 的 OpenAPI 中涉及到用户 ID 之处，均应使用该用户 ID）。                            | 62c795c9cf*****b468af8                                                             |
| username           | string        | 用户名称（登录名）。                                                                      | test-subscriber                                                                    |
| supportMergeFFOnly | boolean       | 是否支持 ff-only 合并方式。                                                              | false                                                                              |
| targetBranch       | string        | 目标分支。                                                                           | master                                                                             |
| targetProjectId    | integer       | 目标分支所在的代码库 ID。                                                                  | 2369234                                                                            |
| targetProjectName  | string        | 目标库名称。                                                                          | test-target-repo                                                                   |
| targetType         | string        | 合并目标类型，包括：BRANCH、COMMIT。                                                        | BRANCH                                                                             |
| title              | string        | 合并请求标题。                                                                         | test-合并请求标题                                                                        |
| updatedAt          | string        | 更新时间。                                                                           | 2023-05-30T02:53:36Z                                                               |
| upvotes            | integer       | 通过投票数。                                                                          | 1                                                                                  |
| webUrl             | string        | web 地址。                                                                         | ""                                                                                 |
| workInProgress     | boolean       | WIP 标识，即合并请求还处于开发中。                                                             | false                                                                              |

## 返回示例

```
{
    "acceptedRevision": "",
    "ahead": 1,
    "assignees": [
        {
            "avatar": "https://tcs-devops.aliyuncs.com/thumbnail/112afcb7a6a35c3f67f1bea827c4/w/100/h/100",
            "email": "username@example.com",
            "id": 90452,
            "name": "test-subscriber",
            "state": "active",
            "status": "approved",
            "userId": "62c795c9cf*****b468af8",
            "username": "root-test-codeup"
        }
    ],
    "author": {
        "avatar": "https://tcs-devops.aliyuncs.com/thumbnail/112afcb7a6a35c3f67f1bea827c4/w/100/h/100",
        "email": "username@example.com",
        "id": 90452,
        "name": "test-subscriber",
        "state": "active",
        "userId": "62c795c9cf*****b468af8",
        "username": "root-test-codeup"
    },
    "behind": 1,
    "createdAt": "2023-05-30T02:53:36Z",
    "creationMethod": "WEB",
    "description": "描述信息的具体内容",
    "detailUrl": "xxx",
    "downvotes": 1,
    "id": 123,
    "iid": 0,
    "isUsePushBlock": false,
    "labels": [
        
    ],
    "mergeStatus": "unchecked",
    "mergedRevision": "1a072f5367c21f9de3464b8c0ee8546e47764d2d",
    "nameWithNamespace": "orgId / test-group / test-target-repo（斜杠两侧有空格）",
    "projectId": 2369234,
    "sourceBranch": "test-merge-request",
    "sourceProjectId": 2369234,
    "sourceProjectName": "test-codeup",
    "sourceType": "BRANCH",
    "sshUrlToRepo": "git@xxx:xxx/test/test.git",
    "state": "opened",
    "subscribers": [
        {
            "avatar": "https://tcs-devops.aliyuncs.com/thumbnail/112afcb7a6a35c3f67f1bea827c4/w/100/h/100",
            "email": "username@example.com",
            "id": 123,
            "name": "test-subscriber",
            "state": "active",
            "userId": "62c795c9cf*****b468af8",
            "username": "test-subscriber"
        }
    ],
    "supportMergeFFOnly": false,
    "targetBranch": "master",
    "targetProjectId": 2369234,
    "targetProjectName": "test-target-repo",
    "targetType": "BRANCH",
    "title": "test-合并请求标题",
    "updatedAt": "2023-05-30T02:53:36Z",
    "upvotes": 1,
    "webUrl": "",
    "workInProgress": false
}
```

## 错误码

访问错误码中心查看 API 相关错误码。

