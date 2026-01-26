# CreateProtectedBranch - 创建保护分支

---
source: https://help.aliyun.com/zh/yunxiao/developer-reference/createprotectedbranch
category: code-management
downloaded_at: 2026-01-26T14:55:26.889851
---

# CreateProtectedBranch - 创建保护分支

通过OpenAPI创建保护分支。

## 适用版本

企业标准版

## 服务接入点与授权信息

获取服务接入点，替换 API 请求语法中的 <domain> ：服务接入点（domain）。

获取个人访问令牌，具体操作，请参见获取个人访问令牌。

获取organizationId，请前往组织管理后台的基本信息页面获取组织 ID 。

| 产品   | 资源   | 所需权限 |
|------|------|------|
| 代码管理 | 保护分支 | 读写   |

## 请求语法

```
POST https://{domain}/oapi/v1/codeup/organizations/{organizationId}/repositories/{repositoryId}/protectedBranches
```

## 请求头

| 参数              | 类型     | 是否必填 | 描述      | 示例值                          |
|-----------------|--------|------|---------|------------------------------|
| x-yunxiao-token | string | 是    | 个人访问令牌。 | pt-0fh3****0fbG_35af****0484 |

## 请求参数

| 参数                                  | 类型             | 位置   | 是否必填 | 描述                                             | 示例值                                          |
|-------------------------------------|----------------|------|------|------------------------------------------------|----------------------------------------------|
| organizationId                      | string         | path | 是    | 组织 ID。                                         | 60d54f3daccf2bbd6659f3ad                     |
| repositoryId                        | string         | path | 是    | 代码库 ID 或者 URL-Encoder 编码的全路径。                  | 2813489或者60de7a6852743a5162b5f957%2FDemoRepo |
| -                                   | object         | body | 否    |                                                |                                              |
| allowMergeRoles                     | array[integer] | body | 否    | 允许合并的角色列表：40-管理员，30-开发者。                         | [40, 30]                                     |
| allowMergeUserIds                   | array[string]  | body | 否    | 允许合并的用户 ID 列表。                                 | ["62c795xxxb468af8"]                         |
| allowPushRoles                      | array[integer] | body | 否    | 允许推送的角色列表：40-管理员，30-开发者。                         | [40, 30]                                     |
| allowPushUserIds                    | array[string]  | body | 否    | 允许推送用户 ID 列表。                                  | ["62c795xxxb468af8"]                         |
| branch                              | string         | body | 是    | 被保护分支名称。                                       | master                                       |
| mergeRequestSetting                 | object         | body | 否    | 要求合并前通过代码评审。                                   |                                              |
| allowMergeRequestRoles              | array[integer] | body | 否    | 允许合并请求的角色列表。                                   | [40, 30]                                     |
| defaultAssignees                    | array[string]  | body | 否    | 默认评审人 ID 列表。                                   | ["62c795xxxb468af8"]                         |
| isAllowSelfApproval                 | boolean        | body | 否    | 是否允许创建者通过代码评审。                                 | false                                        |
| isAllowSourceBranchPushUserApproval | boolean        | body | 否    | 是否允许源分支的提交者通过合并请求。                             | false                                        |
| isRequireDiscussionProcessed        | boolean        | body | 否    | 是否要求评审全部已解决。                                   | true                                         |
| isRequired                          | boolean        | body | 否    | 是否开启【要求合并前通过代码评审】。                             | true                                         |
| isResetApprovalWhenNewPush          | boolean        | body | 否    | 是否在有推送时重置评审状态。                                 | true                                         |
| minimumApproval                     | integer        | body | 否    | 评审通过的最少人数，仅普通模式生效。                             | 1                                            |
| mrMode                              | string         | body | 否    | 评审模式：general - 普通模式, codeowner - CodeOwner 模式。 | general                                      |
| whiteList                           | string         | body | 否    | 评审文件白名单；输入文件路径，多行以换行符隔开，通配符请使用英文格式。            | *.java                                       |
| testSetting                         | object         | body | 否    | 要求合并前通过自动化状态检查。                                 |                                              |
| isRequired                          | boolean        | body | 否    | 是否开启【要求合并前通过自动化状态检查】。                           | true                                         |

## 请求示例

```
curl -X 'POST' \
  'https://{domain}/oapi/v1/codeup/organizations/60d54f3daccf2bbd6659f3ad/repositories/2813489或者60de7a6852743a5162b5f957%2FDemoRepo/protectedBranches' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484' \
  --data '{
      "allowMergeRoles": [40, 30],
      "allowMergeUserIds": ["62c795xxxb468af8"],
      "allowPushRoles": [40, 30],
      "allowPushUserIds": ["62c795xxxb468af8"],
      "branch": "master",
      "mergeRequestSetting": {...},
      "testSetting": {...}
  }'
```

## 返回参数

| 参数                                  | 类型             | 描述                                                   | 示例值                                 |
|-------------------------------------|----------------|------------------------------------------------------|-------------------------------------|
| -                                   | object         |                                                      |                                     |
| allowMergeRoles                     | array[integer] | 允许合并的角色列表：40-管理员，30-开发者。                             | [40, 30]                            |
| allowMergeUserIds                   | array[string]  | 允许合并的用户 ID 列表。                                       | ["62c795xxxb468af8"]                |
| allowMergeUsers                     | array          | 允许合并的用户列表。                                           |                                     |
| allowPushRoles                      | array[integer] | 允许推送的角色列表：40-管理员，30-开发者。                             | [40, 30]                            |
| allowPushUserIds                    | array[string]  | 允许推送用户 ID 列表。                                        | ["62c795xxxb468af8"]                |
| branch                              | string         | 分支名称。                                                | master                              |
| createdAt                           | string         | 创建时间。                                                | 2024-10-05T15:30:45Z                |
| id                                  | integer        | 保护分支规则 ID。                                           | 1                                   |
| mergeRequestSetting                 | object         | 合并请求设置。                                              |                                     |
| testSetting                         | object         | 测试设置。                                                 |                                     |
| updatedAt                           | string         | 更新时间。                                                | 2024-10-05T15:30:45Z                |

## 返回示例

```json
{
    "allowMergeRoles": [40, 30],
    "allowMergeUsers": [...],
    "allowPushRoles": [40, 30],
    "allowPushUserIds": ["62c795xxxb468af8"],
    "branch": "master",
    "createdAt": "2024-10-05T15:30:45Z",
    "id": 1,
    "mergeRequestSetting": {...},
    "testSetting": {...},
    "updatedAt": "2024-10-05T15:30:45Z"
}
```

## 错误码

访问错误码中心查看 API 相关错误码。
