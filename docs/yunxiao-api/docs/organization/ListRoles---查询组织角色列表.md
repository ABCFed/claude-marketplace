# ListRoles - 查询组织角色列表

---
source: https://help.aliyun.com/zh/yunxiao/developer-reference/lists-query-the-list-of-organization-roles
category: organization
downloaded_at: 2026-01-26T14:49:31.756750
---

# ListRoles - 查询组织角色列表

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
| 基础服务 | 组织角色 | 只读   |

## 请求语法

```
GET https://{domain}/oapi/v1/platform/organizations/{organizationId}/roles
```

## 请求头

| 参数              | 类型     | 是否必填 | 描述      | 示例值                          |
|-----------------|--------|------|---------|------------------------------|
| x-yunxiao-token | string | 是    | 个人访问令牌。 | pt-0fh3****0fbG_35af****0484 |

## 请求参数

| 参数             | 类型     | 位置   | 是否必填 | 描述       | 示例值          |
|----------------|--------|------|------|----------|--------------|
| organizationId | string | path | 是    | 所属组织 ID。 | 99d1****71d4 |

## 请求示例

```
curl -X 'GET' \
  'https://test.rdc.aliyuncs.com/oapi/v1/platform/organizations/{organizationId}/roles' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'
```

## 返回参数

| 参数             | 类型            | 描述      | 示例值          |
|----------------|---------------|---------|--------------|
| -              | array         |         |              |
| -              | object        |         |              |
| id             | string        | 角色 ID。  | 99d1****6124 |
| name           | string        | 角色名称。   | 示例名          |
| organizationId | string        | 组织 ID。  | 99d1****6124 |
| permissions    | array[string] | 角色权限列表。 | [base******] |

## 返回示例

```
[
    {
        "id": "99d1****6124",
        "name": "示例名",
        "organizationId": "99d1****6124",
        "permissions": [base******]
    }
]
```

## 错误码

访问错误码中心查看 API 相关错误码。
