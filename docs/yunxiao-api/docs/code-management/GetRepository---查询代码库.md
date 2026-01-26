# GetRepository - 查询代码库

---
source: https://help.aliyun.com/zh/yunxiao/developer-reference/getrepository-query-the-code-base
category: code-management
downloaded_at: 2026-01-26T14:33:10.895569
---

# GetRepository - 查询代码库

## 前提条件

获取服务接入点，替换 API 请求语法中的 <domain> 。关于如何获取domain，请参见服务接入点（domain）。

获取个人访问令牌，具体操作，请参见获取个人访问令牌。

获取organizationId，请前往组织管理后台的基本信息页面获取组织 ID 。

- 获取服务接入点，替换 API 请求语法中的 <domain> 。关于如何获取domain，请参见服务接入点（domain）。
- 获取个人访问令牌，具体操作，请参见获取个人访问令牌。
- 获取organizationId，请前往组织管理后台的基本信息页面获取组织 ID 。

## 授权信息

| 产品   | 资源   | 所需权限 |
|------|------|------|
| 代码管理 | 代码仓库 | 只读   |

## 请求语法

```
GET https://{domain}/oapi/v1/codeup/organizations/{organizationId}/repositories/{repositoryId}
```

## 请求头

| 参数              | 类型     | 是否必填 | 描述      | 示例值                          |
|-----------------|--------|------|---------|------------------------------|
| x-yunxiao-token | string | 是    | 个人访问令牌。 | pt-0fh3****0fbG_35af****0484 |

## 请求参数

| 参数             | 类型     | 位置   | 是否必填 | 描述                            | 示例值                                   |
|----------------|--------|------|------|-------------------------------|---------------------------------------|
| organizationId | string | path | 是    | 组织 ID。                        | 99d1****71d4                          |
| repositoryId   | string | path | 是    | 代码库 ID 或者 URL-Encoder 编码的全路径。 | 2835387 或 codeup-org-id%2Fcodeup-demo |

## 请求示例

```
curl -X 'GET' \
  'https://{domain}/oapi/v1/codeup/organizations/{organizationId}/repositories/{repositoryId}' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'
```

## 返回参数

| 参数                         | 类型      | 描述                                          | 示例值                                         |
|----------------------------|---------|---------------------------------------------|---------------------------------------------|
| -                          | object  |                                             |                                             |
| accessLevel                | string  | 当前用户在该代码库上的权限类型，可能的值：[20 30 40]。            | 40                                          |
| adminSettingLanguage       | string  | 仓库主要编程语言。                                   | Java                                        |
| allowPush                  | boolean | 是否允许推送。                                     | true                                        |
| archived                   | boolean | 是否归档。                                       | false                                       |
| avatarUrl                  | string  | 代码库头像地址。                                    | https://example/example/w/100/h/100         |
| cloneDownloadControlGray   | boolean | 克隆/下载控制组织维度灰度开关。                            | false                                       |
| createdAt                  | string  | 创建时间。                                       | 2024-10-05T15:30:45Z                        |
| creatorId                  | integer | 创建者 user id。                                | 无业务实际意义                                     |
| defaultBranch              | string  | 代码库默认分支。                                    | master                                      |
| demoProject                | boolean | 是否是 demo 库。                                 | false                                       |
| description                | string  | 代码库描述。                                      | 代码库的描述内容                                    |
| enableCloneDownloadControl | boolean | 是否开启代码克隆下载管控。                               | false                                       |
| forkCount                  | integer | fork 数量。                                    | 1                                           |
| httpUrlToRepo              | string  | HTTP 地址。                                    | https://example.com/example_org/example.git |
| id                         | integer | 代码库 ID。                                     | 1                                           |
| lastActivityAt             | string  | 最后活跃时间。                                     | 2024-10-05T15:30:45Z                        |
| name                       | string  | 代码库名称。                                      | demo-repo                                   |
| nameWithNamespace          | string  | 代码库完整名称（含完整组名称）。                            | 60de7a6852743a5162b5f957 / DemoRepo         |
| namespace                  | object  |                                             |                                             |
| avatar                     | string  | 头像地址。                                       | https://example/example/w/100/h/100         |
| createdAt                  | string  | 创建时间。                                       | 2024-10-05T15:30:45Z                        |
| description                | string  | 描述。                                         | 描述内容                                        |
| id                         | integer | ID。                                         | 1                                           |
| name                       | string  | 名称。                                         | demo-namespace                              |
| ownerId                    | integer | 归属者 ID。                                     | 无业务实际意义                                     |
| path                       | string  | 路径。                                         | demo-namespace                              |
| updatedAt                  | string  | 更新时间。                                       | 2024-10-05T15:30:45Z                        |
| visibility                 | string  | 可见性。private：私有, internal：内部公开; public: 公开。  | private                                     |
| openCloneDownloadControl   | boolean | 是否开启克隆下载控制。                                 | false                                       |
| owner                      | object  |                                             |                                             |
| avatarUrl                  | string  | 用户头像地址。                                     | https://example/example/w/100/h/100         |
| email                      | string  | 用户邮箱。                                       | username@example.com                        |
| id                         | integer | 无业务意义主键 ID。                                 | 1                                           |
| name                       | string  | 用户名称。                                       | codeup-name                                 |
| state                      | string  | 用户状态，可为{active, blocked}。                   | active                                      |
| userId                     | string  | 云效用户 ID。                                    | 62c795xxxb468af8                            |
| username                   | string  | 用户登录名。                                      | codeup-username                             |
| webUrl                     | string  | 页面访问地址。                                     | xxx                                         |
| path                       | string  | 代码库路径。                                      | demo-repo                                   |
| pathWithNamespace          | string  | 代码库完整路径（含完整组路径）。                            | 60de7a6852743a5162b5f957/DemoRepo           |
| permissions                | object  | 权限简介。                                       |                                             |
| groupAccess                | object  |                                             |                                             |
| accessLevel                | string  | 组权限，可选{20-浏览者，30-开发者，40-管理员}。               | 30                                          |
| notificationLevel          | integer | 保留信息。                                       | xxx                                         |
| projectAccess              | object  |                                             |                                             |
| accessLevel                | string  | 库权限，可选{20-浏览者，30-开发者，40-管理员}。               | 30                                          |
| notificationLevel          | integer | 保留信息。                                       | xxx                                         |
| projectType                | integer | 代码库类型，默认为空或者0。                              | 0                                           |
| sshUrlToRepo               | string  | 仓库 ssh 克隆地址。                                | git@example:example_org/example.git         |
| starCount                  | integer | 收藏数量。                                       | 1                                           |
| updatedAt                  | string  | 更新时间。                                       | 2024-10-05T15:30:45Z                        |
| visibility                 | string  | 可见性，包括{private-私有, internal-内部公开，public-公开。 | private                                     |
| webUrl                     | string  | 页面访问时的 URL。                                 | https://example.com/example/example_demo    |

## 返回示例

```
{
    "accessLevel": "40",
    "adminSettingLanguage": "Java",
    "allowPush": true,
    "archived": false,
    "avatarUrl": "https://example/example/w/100/h/100",
    "cloneDownloadControlGray": false,
    "createdAt": "2024-10-05T15:30:45Z",
    "creatorId": 无业务实际意义,
    "defaultBranch": "master",
    "demoProject": false,
    "description": "代码库的描述内容",
    "enableCloneDownloadControl": false,
    "forkCount": 1,
    "httpUrlToRepo": "https://example.com/example_org/example.git",
    "id": 1,
    "lastActivityAt": "2024-10-05T15:30:45Z",
    "name": "demo-repo",
    "nameWithNamespace": "60de7a6852743a5162b5f957 / DemoRepo",
    "namespace": {
        "avatar": "https://example/example/w/100/h/100",
        "createdAt": "2024-10-05T15:30:45Z",
        "description": "描述内容",
        "id": 1,
        "name": "demo-namespace",
        "ownerId": 无业务实际意义,
        "path": "demo-namespace",
        "updatedAt": "2024-10-05T15:30:45Z",
        "visibility": "private"
    },
    "openCloneDownloadControl": false,
    "owner": {
        "avatarUrl": "https://example/example/w/100/h/100",
        "email": "username@example.com",
        "id": 1,
        "name": "codeup-name",
        "state": "active",
        "userId": "62c795xxxb468af8",
        "username": "codeup-username",
        "webUrl": "xxx"
    },
    "path": "demo-repo",
    "pathWithNamespace": "60de7a6852743a5162b5f957/DemoRepo",
    "permissions": {
        "groupAccess": {
            "accessLevel": "30",
            "notificationLevel": xxx
        },
        "projectAccess": {
            "accessLevel": "30",
            "notificationLevel": xxx
        }
    },
    "projectType": 0,
    "sshUrlToRepo": "git@example:example_org/example.git",
    "starCount": 1,
    "updatedAt": "2024-10-05T15:30:45Z",
    "visibility": "private",
    "webUrl": "https://example.com/example/example_demo"
}
```

## 错误码

访问错误码中心查看 API 相关错误码。

