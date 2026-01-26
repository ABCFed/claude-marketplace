# GetChangeRequest - 查询合并请求

---
source: https://help.aliyun.com/zh/yunxiao/developer-reference/getchangerequest-query-merge-request
category: code-management
downloaded_at: 2026-01-26T14:35:22.406113
---

# GetChangeRequest - 查询合并请求

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
GET https://{domain}/oapi/v1/codeup/organizations/{organizationId}/repositories/{repositoryId}/changeRequests/{localId}
```

## 请求头

| 参数              | 类型     | 是否必填 | 描述      | 示例值                          |
|-----------------|--------|------|---------|------------------------------|
| x-yunxiao-token | string | 是    | 个人访问令牌。 | pt-0fh3****0fbG_35af****0484 |

## 请求参数

| 参数             | 类型      | 位置   | 是否必填 | 描述                            | 示例值                                   |
|----------------|---------|------|------|-------------------------------|---------------------------------------|
| organizationId | string  | path | 是    | 组织 ID。                        | 99d1****71d4                          |
| repositoryId   | string  | path | 是    | 代码库 ID 或者 URL-Encoder 编码的全路径。 | 2835387 或 codeup-org-id%2Fcodeup-demo |
| localId        | integer | path | 是    | 局部 ID，表示代码库中第几个合并请求。          | 1                                     |

## 请求示例

```
curl -X 'GET' \
  'https://test.rdc.aliyuncs.com/oapi/v1/codeup/organizations/{organizationId}/repositories/{repositoryId}/changeRequests/{localId}' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'
```

## 返回参数

| 参数                             | 类型      | 描述                                                                                                             | 示例值                                                                                |
|--------------------------------|---------|----------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------|
| -                              | object  |                                                                                                                |                                                                                    |
| ahead                          | integer | 源分支领先目标分支的 commit 数量。                                                                                          | 1                                                                                  |
| allRequirementsPass            | boolean | 是否所有卡点项通过。                                                                                                     | true                                                                               |
| author                         | object  | 用户信息。                                                                                                          |                                                                                    |
| avatar                         | string  | 用户头像地址。                                                                                                        | https://tcs-devops.aliyuncs.com/thumbnail/112afcb7a6a35c3f67f1bea827c4/w/100/h/100 |
| email                          | string  | 用户邮箱。                                                                                                          | username@example.com                                                               |
| name                           | string  | 用户名称。                                                                                                          | test-codeup                                                                        |
| state                          | string  | 用户状态：active - 激活可用；blocked - 阻塞暂不可用。                                                                           | active                                                                             |
| userId                         | string  | 云效用户 ID。                                                                                                       | 62c795c9cf*****b468af8                                                             |
| username                       | string  | 用户登录名。                                                                                                         | root-test-codeup                                                                   |
| behind                         | integer | 目标分支领先源分支的 commit 数量。                                                                                          | 1                                                                                  |
| canRevertOrCherryPick          | boolean | 是否能 Revert 或者 CherryPick。                                                                                      | false                                                                              |
| checkList                      | object  | 卡点列表。                                                                                                          |                                                                                    |
| requirementRuleItems           | array   | 卡点规则。                                                                                                          |                                                                                    |
| -                              | object  |                                                                                                                |                                                                                    |
| itemType                       | string  | 卡点规则项类型：MERGE_CONFLICT_CHECK - 冲突检查；REVIEWER_APPROVED_CHECK - 评审通过检查；COMMENTS_CHECK - 评论解决检查；CI_CHECK - 自动化检查。 | MERGE_CONFLICT_CHECK                                                               |
| pass                           | boolean | 检查项是否通过。                                                                                                       | true                                                                               |
| createFrom                     | string  | 创建来源：WEB - 页面创建；COMMAND_LINE - 命令行创建。                                                                          | WEB                                                                                |
| createTime                     | string  | 创建时间。                                                                                                          | 2023-05-30T02:53:36Z                                                               |
| description                    | string  | 描述。                                                                                                            | 描述信息的具体内容                                                                          |
| detailUrl                      | string  | 合并请求详情地址。                                                                                                      | xxx                                                                                |
| hasReverted                    | boolean | 是否 Revert 过。                                                                                                   | false                                                                              |
| localId                        | integer | 局部 ID。                                                                                                         | 1                                                                                  |
| mergedRevision                 | string  | 合并版本（提交 ID），仅已合并状态才有值。                                                                                         | 1a072f5367c21f9de3464b8c0ee8546e47764d2d                                           |
| mrType                         | string  | 合并请求类型：CODE_REVIEW - 代码评审；REF_REVIEW - 分支标签评审。                                                                 | CODE_REVIEW                                                                        |
| projectId                      | integer | 代码库 ID。                                                                                                        | 2369234                                                                            |
| reviewers                      | array   | 评审人列表。                                                                                                         |                                                                                    |
| -                              | object  |                                                                                                                |                                                                                    |
| avatar                         | string  | 用户头像地址。                                                                                                        | https://tcs-devops.aliyuncs.com/thumbnail/112afcb7a6a35c3f67f1bea827c4/w/100/h/100 |
| email                          | string  | 用户邮箱。                                                                                                          | username@example.com                                                               |
| hasCommented                   | boolean | 是否已经评论过。                                                                                                       | true                                                                               |
| hasReviewed                    | boolean | 是否评审过。                                                                                                         | false                                                                              |
| name                           | string  | 用户名称。                                                                                                          | test-codeup                                                                        |
| reviewOpinionStatus            | string  | 评审意见：PASS - 通过；NOT_PASS - 不通过。                                                                                 | NOT_PASS                                                                           |
| reviewTime                     | string  | 评审时间。                                                                                                          | 2023-05-30T02:53:36Z                                                               |
| state                          | string  | 用户状态：active - 激活可用；blocked - 阻塞暂不可用。                                                                           | active                                                                             |
| userId                         | string  | 云效用户 ID。                                                                                                       | 62c795c9cf*****b468af8                                                             |
| username                       | string  | 用户登录名。                                                                                                         | root-test-codeup                                                                   |
| sourceBranch                   | string  | 源分支。                                                                                                           | test-merge-request                                                                 |
| sourceCommitId                 | string  | 源提交 ID，当 createFrom=COMMAND_LINE 时，有值。                                                                         |                                                                                    |
| sourceProjectId                | integer | 源库 ID。                                                                                                         | 2369234                                                                            |
| sourceRef                      | string  | 源提交引用，当 createFrom=COMMAND_LINE 时，有值。                                                                          |                                                                                    |
| status                         | string  | 合并请求状态：UNDER_DEV - 开发中；UNDER_REVIEW - 评审中；TO_BE_MERGED - 待合并；CLOSED - 已关闭；MERGED - 已合并。                        | UNDER_REVIEW                                                                       |
| subscribers                    | array   | 订阅人列表。                                                                                                         |                                                                                    |
| -                              | object  | 用户信息。                                                                                                          |                                                                                    |
| avatar                         | string  | 用户头像地址。                                                                                                        | https://tcs-devops.aliyuncs.com/thumbnail/112afcb7a6a35c3f67f1bea827c4/w/100/h/100 |
| email                          | string  | 用户邮箱。                                                                                                          | username@example.com                                                               |
| name                           | string  | 用户名称。                                                                                                          | test-codeup                                                                        |
| state                          | string  | 用户状态：active - 激活可用；blocked - 阻塞暂不可用。                                                                           | active                                                                             |
| userId                         | string  | 云效用户 ID。                                                                                                       | 62c795c9cf*****b468af8                                                             |
| username                       | string  | 用户登录名。                                                                                                         | root-test-codeup                                                                   |
| supportMergeFastForwardOnly    | boolean | 是否支持 fast-forward-only。                                                                                        | true                                                                               |
| targetBranch                   | string  | 目标分支。                                                                                                          | master                                                                             |
| targetProjectId                | integer | 目标库 ID。                                                                                                        | 2369234                                                                            |
| targetProjectNameWithNamespace | string  | 目标库名称（含完整父路径）。                                                                                                 | orgId / test-group / test-target-repo（斜杠两侧有空格）                                     |
| targetProjectPathWithNamespace | string  | 目标库路径（含完整父路径）。                                                                                                 | orgId/test-group/test-target-repo                                                  |
| title                          | string  | 标题。                                                                                                            | test-合并请求标题                                                                        |
| totalCommentCount              | integer | 总评论数。                                                                                                          | 2                                                                                  |
| unResolvedCommentCount         | integer | 未解决评论数。                                                                                                        | 1                                                                                  |
| updateTime                     | string  | 更新时间。                                                                                                          | 2023-05-30T02:53:36Z                                                               |
| webUrl                         | string  | 页面地址。                                                                                                          | xxx                                                                                |

## 返回示例

```
{
    "ahead": 1,
    "allRequirementsPass": true,
    "author": {
        "avatar": "https://example/example/w/100/h/100",
        "email": "username@example.com",
        "name": "codeup-name",
        "state": "active",
        "userId": "62c795xxxb468af8",
        "username": "codeup-username"
    },
    "behind": 1,
    "canRevertOrCherryPick": true,
    "checkList": {
        "requirementRuleItems": [
            {
                "itemType": "MERGE_CONFLICT_CHECK",
                "pass": true
            }
        ]
    },
    "createFrom": "WEB",
    "createTime": "2024-10-05T15:30:45Z",
    "description": "mr description",
    "detailUrl": "https://example.com/example/example_demo/change/1",
    "hasReverted": false,
    "localId": 1,
    "mergedRevision": "6da8c14b5a9102998148b7ea35f96507d5304f74",
    "mrType": "CODE_REVIEW",
    "projectId": 2813489,
    "reviewers": [
        {
            "avatar": "https://example/example/w/100/h/100",
            "email": "username@example.com",
            "hasCommented": true,
            "hasReviewed": true,
            "name": "codeup-name",
            "reviewOpinionStatus": "PASS",
            "reviewTime": "2024-10-05T15:30:45Z",
            "state": "active",
            "userId": "62c795xxxb468af8",
            "username": "codeup-username"
        }
    ],
    "sourceBranch": "demo-branch",
    "sourceCommitId": "6da8c14b5a9102998148b7ea35f96507d5304f74",
    "sourceProjectId": 2813489,
    "sourceRef": "null",
    "status": "UNDER_REVIEW",
    "subscribers": [
        {
            "avatar": "https://example/example/w/100/h/100",
            "email": "username@example.com",
            "name": "codeup-name",
            "state": "active",
            "userId": "62c795xxxb468af8",
            "username": "codeup-username"
        }
    ],
    "supportMergeFastForwardOnly": true,
    "targetBranch": "master",
    "targetProjectId": 2813489,
    "targetProjectNameWithNamespace": "60de7a6852743a5162b5f957 / DemoRepo（斜杠两侧有空格）",
    "targetProjectPathWithNamespace": "60de7a6852743a5162b5f957/DemoRepo",
    "title": "mr title",
    "totalCommentCount": 1,
    "unResolvedCommentCount": 1,
    "updateTime": "2024-10-05T15:30:45Z",
    "webUrl": "https://example.com/example/example_demo/change/1"
}
```

## 错误码

访问错误码中心查看 API 相关错误码。

