# ListProtectedBranches - 查询保护分支列表

---
source: https://help.aliyun.com/zh/yunxiao/developer-reference/listprotectedbranches
category: code-management
downloaded_at: 2026-01-26T14:35:01.501125
---

# ListProtectedBranches - 查询保护分支列表

## 服务接入点与授权信息

获取服务接入点，替换 API 请求语法中的 <domain> ：服务接入点（domain）。

获取个人访问令牌，具体操作，请参见获取个人访问令牌。

获取organizationId，请前往组织管理后台的基本信息页面获取组织 ID 。

- 获取服务接入点，替换 API 请求语法中的 <domain> ：服务接入点（domain）。
- 获取个人访问令牌，具体操作，请参见获取个人访问令牌。
- 获取organizationId，请前往组织管理后台的基本信息页面获取组织 ID 。

| 产品   | 资源   | 所需权限 |
|------|------|------|
| 代码管理 | 保护分支 | 只读   |

```
GET https://{domain}/oapi/v1/codeup/organizations/{organizationId}/repositories/{repositoryId}/protectedBranches
```

| 参数              | 类型     | 是否必填 | 描述      | 示例值                          |
|-----------------|--------|------|---------|------------------------------|
| x-yunxiao-token | string | 是    | 个人访问令牌。 | pt-0fh3****0fbG_35af****0484 |

## 请求参数

| 参数             | 类型     | 位置   | 是否必填 | 描述                            | 示例值                      |
|----------------|--------|------|------|-------------------------------|--------------------------|
| organizationId | string | path | 是    | 组织 ID。                        | 60de7a6852743a5162b5f957 |
| repositoryId   | string | path | 是    | 代码库 ID 或者 URL-Encoder 编码的全路径。 | 2813489                  |

## 请求示例

```
curl -X 'GET' \
  'https://test.rdc.aliyuncs.com/oapi/v1/codeup/organizations/{organizationId}/repositories/{repositoryId}/protectedBranches' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'
```

## 返回参数

| 参数                                  | 类型             | 描述                                                   | 示例值                                                                                |
|-------------------------------------|----------------|------------------------------------------------------|------------------------------------------------------------------------------------|
| -                                   | object         |                                                      |                                                                                    |
| allowMergeRoles                     | array[integer] | 允许合并的角色列表：40-管理员，30-开发者。                             | 40, 30                                                                             |
| allowMergeUserIds                   | array[string]  | 允许合并的用户 ID 列表。                                       | 62c795c*****468af8                                                                 |
| allowMergeUsers                     | array          | 允许合并的用户列表。                                           |                                                                                    |
| -                                   | object         |                                                      |                                                                                    |
| avatarUrl                           | string         | 头像地址。                                                | https://tcs-devops.aliyuncs.com/thumbnail/112afcb7a6a35c3f67f1bea827c4/w/100/h/100 |
| email                               | string         | 邮箱。                                                  | username@example.com                                                               |
| id                                  | integer        | 数据库主键 ID（无业务意义）。                                     | 1938                                                                               |
| name                                | string         | 用户名称。                                                | 阿里云云效                                                                              |
| userId                              | string         | 云效用户 ID（在 codeup 的 OpenAPI 中涉及到用户 ID 之处，均应使用该用户 ID）。 | 62c795c*****468af8                                                                 |
| username                            | string         | 用户名称（登录名）。                                           | codeup-test                                                                        |
| allowPushRoles                      | array[integer] | 允许推送的角色列表：40-管理员，30-开发者。                             | 40                                                                                 |
| allowPushUserIds                    | array[string]  | 允许推送用户 ID 列表。                                        | 62c795c*****468af8                                                                 |
| allowPushUsers                      | array          | 允许推送的用户列表。                                           |                                                                                    |
| -                                   | object         |                                                      |                                                                                    |
| avatarUrl                           | string         | 头像地址。                                                | https://tcs-devops.aliyuncs.com/thumbnail/112afcb7a6a35c3f67f1bea827c4/w/100/h/100 |
| email                               | string         | 邮箱。                                                  | username@example.com                                                               |
| id                                  | integer        | 数据库主键 ID（无业务意义）。                                     | 1938                                                                               |
| name                                | string         | 用户名称。                                                | 阿里云云效                                                                              |
| userId                              | string         | 云效用户 ID（在 Codeup 的 OpenAPI 中涉及到用户 ID 之处，均应使用该用户 ID）。 | 62c795c*****468af8                                                                 |
| username                            | string         | 用户名称（登录名）。                                           | codeup-test                                                                        |
| branch                              | string         | 分支名称。                                                | protectedBranch                                                                    |
| createdAt                           | string         | 创建时间。                                                | 2023-01-03T15:41:26+08:00                                                          |
| id                                  | integer        | 保护分支规则 ID。                                           | 19285                                                                              |
| matches                             | array[string]  | 匹配的分支列表。                                             | [\"pb\"]                                                                           |
| mergeRequestSetting                 | object         |                                                      |                                                                                    |
| allowMergeRequestRoles              | array[integer] | 允许合并请求的角色列表。                                         | 30                                                                                 |
| defaultAssignees                    | array          | 默认评审人列表。                                             |                                                                                    |
| -                                   | object         |                                                      |                                                                                    |
| avatarUrl                           | string         | 头像地址。                                                | https://tcs-devops.aliyuncs.com/thumbnail/112afcb7a6a35c3f67f1bea827c4/w/100/h/100 |
| email                               | string         | 邮箱。                                                  | username@example.com                                                               |
| id                                  | integer        | 数据库主键 ID（无业务意义）。                                     | 19238                                                                              |
| name                                | string         | 用户名称。                                                | 阿里云云效                                                                              |
| userId                              | string         | 云效用户 ID（在 Codeup 的 OpenAPI 中涉及到用户 ID 之处，均应使用该用户 ID）。 | 62c795c*****468af8                                                                 |
| username                            | string         | 用户名称（登录名）。                                           | codeup-test                                                                        |
| isAllowSelfApproval                 | boolean        | 是否允许创建者通过代码评审。                                       | true                                                                               |
| isAllowSourceBranchPushUserApproval | boolean        | 是否允许源分支的提交者通过合并请求。                                   | true                                                                               |
| isRequireDiscussionProcessed        | boolean        | 是否要求评审全部已解决。                                         | true                                                                               |
| isRequired                          | boolean        | 是否开启。                                                | true                                                                               |
| isResetApprovalWhenNewPush          | boolean        | 是否在有推送时重置评审状态。                                       | true                                                                               |
| minimumApproval                     | integer        | 评审通过的最少人数，仅普通模式生效。                                   | 1                                                                                  |
| mrMode                              | string         | 评审模式：general - 普通模式, codeowner - CodeOwner 模式。       | general                                                                            |
| whiteList                           | string         | 评审文件白名单；输入文件路径，多行以换行符隔开，通配符请使用英文格式。                  | **.java                                                                            |
| testSetting                         | object         |                                                      |                                                                                    |
| checkCheckRunConfig                 | object         | 运行检查。                                                |                                                                                    |
| checkRunCheckItems                  | array          | 配置项列表。                                               |                                                                                    |
| -                                   | object         |                                                      |                                                                                    |
| id                                  | string         | 写入人的 ID。                                             | 62c795c*****468af8                                                                 |
| name                                | string         | check run 的名称。                                       | 测试流水线                                                                              |
| required                            | boolean        | 是否作为卡点。                                              | true                                                                               |
| type                                | string         | 写入人类型：User。                                          | User                                                                               |
| checkCommitStatusConfig             | object         | 提交状态。                                                |                                                                                    |
| commitStatusCheckItems              | array          | 配置项列表。                                               |                                                                                    |
| -                                   | object         |                                                      |                                                                                    |
| context                             | string         | 三方提交状态的名称（以名称作为卡点的匹配项）。                              | ""                                                                                 |
| required                            | boolean        | 是否作为卡点。                                              | false                                                                              |
| checkConfig                         | object         | 流水线检查。                                               |                                                                                    |
| checkItems                          | array          | 配置项列表。                                               |                                                                                    |
| -                                   | object         |                                                      |                                                                                    |
| isRequired                          | boolean        | 是否是卡点项。                                              | false                                                                              |
| pipelineId                          | integer        | 流水线 ID。                                              | 0                                                                                  |
| pipelineName                        | string         | 流水线名称。                                               | ""                                                                                 |
| checkTaskQualityConfig              | object         | 代码检测任务。                                              |                                                                                    |
| bizNo                               | string         | 检测任务流水线号。                                            | 123456                                                                             |
| enabled                             | boolean        | 是否开启。                                                | false                                                                              |
| message                             | string         | 描述信息。                                                | test_task_quality                                                                  |
| taskName                            | string         | 检测任务名称。                                              | biz-task-quality                                                                   |
| isRequired                          | boolean        | 是否开启。                                                | false                                                                              |
| updatedAt                           | string         | 更新时间。                                                | 2023-01-03T15:41:26+08:00                                                          |

## 返回示例

```
{
    "allowMergeRoles": [
        40,
        30
    ],
    "allowMergeUserIds": [
        "62c795c*****468af8"
    ],
    "allowMergeUsers": [
        {
            "avatarUrl": "https://tcs-devops.aliyuncs.com/thumbnail/112afcb7a6a35c3f67f1bea827c4/w/100/h/100",
            "email": "username@example.com",
            "id": 1938,
            "name": "阿里云云效",
            "userId": "62c795c*****468af8",
            "username": "codeup-test"
        }
    ],
    "allowPushRoles": [
        40
    ],
    "allowPushUserIds": [
        "62c795c*****468af8"
    ],
    "allowPushUsers": [
        {
            "avatarUrl": "https://tcs-devops.aliyuncs.com/thumbnail/112afcb7a6a35c3f67f1bea827c4/w/100/h/100",
            "email": "username@example.com",
            "id": 1938,
            "name": "阿里云云效",
            "userId": "62c795c*****468af8",
            "username": "codeup-test"
        }
    ],
    "branch": "protectedBranch",
    "createdAt": "2023-01-03T15:41:26+08:00",
    "id": 19285,
    "matches": [
        "[\"pb\"]"
    ],
    "mergeRequestSetting": {
        "allowMergeRequestRoles": [
            30
        ],
        "defaultAssignees": [
            {
                "avatarUrl": "https://tcs-devops.aliyuncs.com/thumbnail/112afcb7a6a35c3f67f1bea827c4/w/100/h/100",
                "email": "username@example.com",
                "id": 1938,
                "name": "阿里云云效",
                "userId": "62c795c*****468af8",
                "username": "codeup-test"
            }
        ],
        "isAllowSelfApproval": false,
        "isAllowSourceBranchPushUserApproval": false,
        "isRequireDiscussionProcessed": false,
        "isRequired": false,
        "isResetApprovalWhenNewPush": false,
        "minimumApproval": 0,
        "mrMode": "general",
        "whiteList": "**.java"
    },
    "testSetting": {
        "checkCheckRunConfig": {
            "checkRunCheckItems": [
                {
                    "id": "62c795c*****468af8",
                    "name": "测试流水线",
                    "required": false,
                    "type": "User"
                }
            ]
        },
        "checkCommitStatusConfig": {
            "commitStatusCheckItems": [
                {
                    "context": "",
                    "required": false
                }
            ]
        },
        "checkConfig": {
            "checkItems": [
                {
                    "isRequired": false,
                    "pipelineId": 0,
                    "pipelineName": ""
                }
            ]
        },
        "checkTaskQualityConfig": {
            "bizNo": "123456",
            "enabled": false,
            "message": "test_task_quality",
            "taskName": "biz-task-quality"
        },
        "isRequired": false
    },
    "updatedAt": "2023-01-03T15:41:26+08:00"
}
```

## 错误码

访问错误码中心查看 API 相关错误码。

