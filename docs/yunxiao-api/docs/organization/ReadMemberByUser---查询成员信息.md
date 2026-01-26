# ReadMemberByUser - 查询成员信息

---
source: https://help.aliyun.com/zh/yunxiao/developer-reference/readmemberbyuser-query-organization-member-information-user-id
category: organization
downloaded_at: 2026-01-26T14:48:06.272740
---

# ReadMemberByUser - 查询成员信息

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
| 基础服务 | 组织成员 | 只读   |

## 请求语法

```
GET https://{domain}/oapi/v1/platform/organizations/{organizationId}/members:readByUser
```

## 请求头

| 参数              | 类型     | 是否必填 | 描述      | 示例值                          |
|-----------------|--------|------|---------|------------------------------|
| x-yunxiao-token | string | 是    | 个人访问令牌。 | pt-0fh3****0fbG_35af****0484 |

## 请求参数

| 参数             | 类型     | 位置    | 是否必填 | 描述     | 示例值          |
|----------------|--------|-------|------|--------|--------------|
| organizationId | string | path  | 是    | 组织 ID。 | 99d1****71d4 |
| userId         | string | query | 是    | 用户 ID。 | 3ab3****b634 |

## 请求示例

```
curl -X 'GET' \
  'https://test.rdc.aliyuncs.com/oapi/v1/platform/organizations/{organizationId}/members:readByUser?userId={userId}' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'
```

## 返回参数

| 参数             | 类型            | 描述                                                                  | 示例值                      |
|----------------|---------------|---------------------------------------------------------------------|--------------------------|
| -              | object        |                                                                     |                          |
| deptIds        | array[string] | 所属组织部门列表。                                                           | [99d1****6124]           |
| id             | string        | 成员 ID。                                                              | 99d1****6124             |
| joined         | string        | 加入时间，等于数据库的创建时间。                                                    | 2023-08-31T03:59:16.201Z |
| lastUpdated    | string        | 最后更新时间，等于数据库的更新时间。                                                  | 2023-08-31T03:59:16.201Z |
| name           | string        | 成员名。                                                                | 示例名                      |
| organizationId | string        | 组织 ID。                                                              | 99d1****6124             |
| roleIds        | array[string] | 角色信息。                                                               | [99d1****6124]           |
| status         | string        | 成员状态，可选值：ENABLED,DISABLED,UNDELETED,DELETED,NORMAL_USING,UNVISITED。 | ENABLED                  |
| userId         | string        | 用户 ID。                                                              | 99d1****6124             |
| visited        | string        | 最后访问时间。                                                             | 2023-08-31T03:59:16.201Z |

## 返回示例

```
{
    "deptIds": [99d1****6124],
    "id": "99d1****6124",
    "joined": "2023-08-31T03:59:16.201Z",
    "lastUpdated": "2023-08-31T03:59:16.201Z",
    "name": "示例名",
    "organizationId": "99d1****6124",
    "roleIds": [99d1****6124],
    "status": "ENABLED",
    "userId": "99d1****6124",
    "visited": "2023-08-31T03:59:16.201Z"
}
```

## 错误码

访问错误码中心查看 API 相关错误码。
