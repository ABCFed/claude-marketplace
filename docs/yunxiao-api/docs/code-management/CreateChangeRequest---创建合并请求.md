# CreateChangeRequest - 创建合并请求

---
source: https://help.aliyun.com/zh/yunxiao/developer-reference/createchangerequest-create-merge-request
category: code-management
downloaded_at: 2026-01-26T14:35:15.306850
---

# CreateChangeRequest - 创建合并请求

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

	

读写

| 产品   | 资源   | 所需权限 |
|------|------|------|
| 代码管理 | 合并请求 | 读写   |

## 请求语法

```
POST https://{domain}/oapi/v1/codeup/organizations/{organizationId}/repositories/{repositoryId}/changeRequests
```

## 请求头

| 参数              | 类型     | 是否必填 | 描述      | 示例值                          |
|-----------------|--------|------|---------|------------------------------|
| x-yunxiao-token | string | 是    | 个人访问令牌。 | pt-0fh3****0fbG_35af****0484 |

## 请求参数

| 参数                 | 类型            | 位置   | 是否必填 | 描述                            | 示例值                                   |
|--------------------|---------------|------|------|-------------------------------|---------------------------------------|
| organizationId     | string        | path | 是    | 组织 ID。                        | 5ebbc0228123212b59xxxxx               |
| repositoryId       | string        | path | 是    | 代码库 ID 或者 URL-Encoder 编码的全路径。 | 2835387 或 codeup-org-id%2Fcodeup-demo |
| -                  | object        | body | 否    |                               |                                       |
| description        | string        | body | 否    | 描述，不超过10000个字符。               | 描述信息的具体内容                             |
| reviewerUserIds    | array[string] | body | 否    | 评审人用户 ID 列表。                  |                                       |
| sourceBranch       | string        | body | 是    | 源分支。                          | sourceBranch                          |
| sourceProjectId    | integer       | body | 是    | 源库 ID。                        | 2369234                               |
| targetBranch       | string        | body | 是    | 目标分支。                         | targetBranch                          |
| targetProjectId    | integer       | body | 是    | 目标库 ID。                       | 2369234                               |
| title              | string        | body | 是    | 标题，不超过256个字符。                 | 测试合并请求的标题                             |
| triggerAIReviewRun | boolean       | body | 否    | 是否触发 AI 评审，默认 false。          | false                                 |
| workItemIds        | array[string] | body | 否    | 关联工作项 ID 列表。                  | 722200214032b6b31e6f1434ab            |

## 请求示例

```
curl -X 'POST' \
  'https://test.rdc.aliyuncs.com/oapi/v1/codeup/organizations/{organizationId}/repositories/{repositoryId}/changeRequests' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484' \
  --data '
    {
        "description": "描述信息的具体内容",
        "reviewerUserIds": [
            
        ],
        "sourceBranch": "sourceBranch",
        "sourceProjectId": 2369234,
        "targetBranch": "targetBranch",
        "targetProjectId": 2369234,
        "title": "测试合并请求的标题",
        "triggerAIReviewRun": false,
        "workItemIds": [
            "722200214032b6b31e6f1434ab",
            "xxx"
        ]
    }'
```

## 返回参数

| 参数                             | 类型      | 描述                                                                                      | 示例值                                                                                |
|--------------------------------|---------|-----------------------------------------------------------------------------------------|------------------------------------------------------------------------------------|
| -                              | object  |                                                                                         |                                                                                    |
| ahead                          | integer | 源分支领先目标分支的 commit 数量。                                                                   | 2                                                                                  |
| allRequirementsPass            | boolean | 是否所有卡点项通过。                                                                              | true                                                                               |
| author                         | object  | 用户信息。                                                                                   |                                                                                    |
| avatar                         | string  | 用户头像地址。                                                                                 | https://tcs-devops.aliyuncs.com/thumbnail/112afcb7a6a35c3f67f1bea827c4/w/100/h/100 |
| email                          | string  | 用户邮箱。                                                                                   | username@example.com                                                               |
| name                           | string  | 用户名称。                                                                                   | test-codeup                                                                        |
| state                          | string  | 用户状态：active - 激活可用；blocked - 阻塞暂不可用。                                                    | active                                                                             |
| userId                         | string  | 云效用户 ID。                                                                                | 62c795c9cf*****b468af8                                                             |
| username                       | string  | 用户登录名。                                                                                  | test-codeup-nickname                                                               |
| behind                         | integer | 目标分支领先源分支的 commit 数量。                                                                   | 0                                                                                  |
| canRevertOrCherryPick          | boolean | 是否能 Revert 或者 CherryPick。                                                               | true                                                                               |
| createFrom                     | string  | 创建来源：WEB - 页面创建；COMMAND_LINE - 命令行创建。                                                   | WEB                                                                                |
| createTime                     | string  | 创建时间。                                                                                   | 2023-06-02T03:41:22Z                                                               |
| description                    | string  | 描述。                                                                                     | 测试合并请求                                                                             |
| detailUrl                      | string  | 合并请求详情地址。                                                                               | xxx                                                                                |
| hasReverted                    | boolean | 是否 Revert 过。                                                                            | false                                                                              |
| localId                        | integer | 局部 ID。                                                                                  | 1                                                                                  |
| mergedRevision                 | string  | 合并版本（提交 ID），仅已合并状态才有值。                                                                  |                                                                                    |
| mrType                         | string  | 合并请求类型：CODE_REVIEW - 代码评审；REF_REVIEW - 分支标签评审。                                          | CODE_REVIEW                                                                        |
| projectId                      | integer | 代码库 ID。                                                                                 | 2369234                                                                            |
| reviewers                      | array   | 评审人列表。                                                                                  |                                                                                    |
| -                              | object  |                                                                                         |                                                                                    |
| avatar                         | string  | 用户头像地址。                                                                                 | https://tcs-devops.aliyuncs.com/thumbnail/112afcb7a6a35c3f67f1bea827c4/w/100/h/100 |
| email                          | string  | 用户邮箱。                                                                                   | username@example.com                                                               |
| hasCommented                   | boolean | 是否已经评论过。                                                                                | false                                                                              |
| hasReviewed                    | boolean | 是否评审过。                                                                                  | false                                                                              |
| name                           | string  | 用户名称。                                                                                   | test-codeup                                                                        |
| reviewOpinionStatus            | string  | 评审意见：PASS - 通过；NOT_PASS - 不通过。                                                          | PASS                                                                               |
| reviewTime                     | string  | 评审时间。                                                                                   |                                                                                    |
| state                          | string  | 用户状态：active - 激活可用；blocked - 阻塞暂不可用。                                                    | active                                                                             |
| userId                         | string  | 云效用户 ID。                                                                                | 62c795c9cf*****b468af8                                                             |
| username                       | string  | 用户登录名。                                                                                  | root-codeup                                                                        |
| sourceBranch                   | string  | 源分支。                                                                                    | sourceBranch                                                                       |
| sourceCommitId                 | string  | 源提交 ID，当 createFrom=COMMAND_LINE 时，有值。                                                  |                                                                                    |
| sourceProjectId                | integer | 源库 ID。                                                                                  | 2369234                                                                            |
| sourceRef                      | string  | 源提交引用，当 createFrom=COMMAND_LINE 时，有值。                                                   |                                                                                    |
| status                         | string  | 合并请求状态：UNDER_DEV - 开发中；UNDER_REVIEW - 评审中；TO_BE_MERGED - 待合并；CLOSED - 已关闭；MERGED - 已合并。 | UNDER_DEV                                                                          |
| subscribers                    | array   | 订阅人列表。                                                                                  |                                                                                    |
| -                              | object  | 用户信息。                                                                                   |                                                                                    |
| avatar                         | string  | 用户头像地址。                                                                                 | https://tcs-devops.aliyuncs.com/thumbnail/112afcb7a6a35c3f67f1bea827c4/w/100/h/100 |
| email                          | string  | 用户邮箱。                                                                                   | username@example.com                                                               |
| name                           | string  | 用户名称。                                                                                   | test-codeup-nickname                                                               |
| state                          | string  | 用户状态：active - 激活可用；blocked - 阻塞暂不可用。                                                    | active                                                                             |
| userId                         | string  | 云效用户 ID。                                                                                | 62c795c9cf*****b468af8                                                             |
| username                       | string  | 用户登录名。                                                                                  | test-codeup-nickname                                                               |
| supportMergeFastForwardOnly    | boolean | 是否支持 fast-forward-only。                                                                 | true                                                                               |
| targetBranch                   | string  | 目标分支。                                                                                   | targetBranch                                                                       |
| targetProjectId                | integer | 目标库 ID。                                                                                 | 2369234                                                                            |
| targetProjectNameWithNamespace | string  | 目标库名称（含完整父路径）。                                                                          | orgId / test-group / test-target-repo（斜杠两侧有空格）                                     |
| targetProjectPathWithNamespace | string  | 目标库路径（含完整父路径）。                                                                          | orgId/test-group/test-target-repo                                                  |
| title                          | string  | 标题。                                                                                     | test-合并请求标题                                                                        |
| totalCommentCount              | integer | 总评论数。                                                                                   | 2                                                                                  |
| unResolvedCommentCount         | integer | 未解决评论数。                                                                                 | 1                                                                                  |
| updateTime                     | string  | 更新时间。                                                                                   | 023-05-30T02:53:36Z                                                                |
| webUrl                         | string  | 页面地址。                                                                                   | ""                                                                                 |

## 返回示例

```
{
    "ahead": 0,
    "allRequirementsPass": false,
    "author": {
        "avatar": "https://tcs-devops.aliyuncs.com/thumbnail/112afcb7a6a35c3f67f1bea827c4/w/100/h/100",
        "email": "username@example.com",
        "name": "test-codeup",
        "state": "active",
        "userId": "62c795c9cf*****b468af8",
        "username": "root-test-codeup"
    },
    "behind": 0,
    "canRevertOrCherryPick": false,
    "createFrom": "WEB",
    "createTime": "2023-05-30T02:53:36Z",
    "description": "描述信息的具体内容",
    "detailUrl": "xxx",
    "hasReverted": false,
    "localId": 0,
    "mergedRevision": "1a072f5367c21f9de3464b8c0ee8546e47764d2d",
    "mrType": "CODE_REVIEW",
    "projectId": 0,
    "reviewers": [
        {
            "avatar": "https://tcs-devops.aliyuncs.com/thumbnail/112afcb7a6a35c3f67f1bea827c4/w/100/h/100",
            "email": "username@example.com",
            "hasCommented": false,
            "hasReviewed": false,
            "name": "test-codeup",
            "reviewOpinionStatus": "NOT_PASS",
            "reviewTime": "2023-05-30T02:53:36Z",
            "state": "active",
            "userId": "62c795c9cf*****b468af8",
            "username": "root-test-codeup"
        }
    ],
    "sourceBranch": "test-merge-request",
    "sourceCommitId": "",
    "sourceProjectId": 0,
    "sourceRef": "",
    "status": "UNDER_REVIEW",
    "subscribers": [
        {
            "avatar": "https://tcs-devops.aliyuncs.com/thumbnail/112afcb7a6a35c3f67f1bea827c4/w/100/h/100",
            "email": "username@example.com",
            "name": "test-codeup",
            "state": "active",
            "userId": "62c795c9cf*****b468af8",
            "username": "root-test-codeup"
        }
    ],
    "supportMergeFastForwardOnly": false,
    "targetBranch": "master",
    "targetProjectId": 0,
    "targetProjectNameWithNamespace": "orgId / test-group / test-target-repo（斜杠两侧有空格）",
    "targetProjectPathWithNamespace": "orgId/test-group/test-target-repo",
    "title": "test-合并请求标题",
    "totalCommentCount": 2,
    "unResolvedCommentCount": 1,
    "updateTime": "2023-05-30T02:53:36Z",
    "webUrl": "\"\""
}
```

## 错误码

访问错误码中心查看 API 相关错误码。

