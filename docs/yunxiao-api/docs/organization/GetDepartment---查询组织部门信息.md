# GetDepartment - 查询组织部门信息

---
source: https://help.aliyun.com/zh/yunxiao/developer-reference/getdepartment-query-organization-department-information
category: organization
downloaded_at: 2026-01-26T14:42:20.516493
---

# GetDepartment - 查询组织部门信息

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
| 基础服务 | 组织部门 | 只读   |

## 请求语法

```
GET https://{domain}/oapi/v1/platform/organizations/{organizationId}/departments/{id}
```

## 请求头

| 参数              | 类型     | 是否必填 | 描述      | 示例值                          |
|-----------------|--------|------|---------|------------------------------|
| x-yunxiao-token | string | 是    | 个人访问令牌。 | pt-0fh3****0fbG_35af****0484 |

## 请求参数

| 参数             | 类型     | 位置   | 是否必填 | 描述     | 示例值          |
|----------------|--------|------|------|--------|--------------|
| organizationId | string | path | 是    | 组织 ID。 | 99d1****71d4 |
| id             | string | path | 是    | 部门 ID。 | 8446****ce9f |

## 请求示例

```
curl -X 'GET' \
  'https://test.rdc.aliyuncs.com/oapi/v1/platform/organizations/{organizationId}/departments/{id}' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'
```

## 返回参数

| 参数             | 类型      | 描述      | 示例值          |
|----------------|---------|---------|--------------|
| -              | object  |         |              |
| creatorId      | string  | 创建人 ID。 | 99d1****6124 |
| hasSub         | boolean | 是否有子部门。 | true         |
| id             | string  | 部门 ID。  | 99d1****6124 |
| name           | string  | 部门名称。   | 示例           |
| organizationId | string  | 组织 ID。  | 99d1****6124 |
| parentId       | string  | 父部门 ID。 | 99d1****6124 |

## 返回示例

```
{
    "creatorId": "99d1****6124",
    "hasSub": true,
    "id": "99d1****6124",
    "name": "示例",
    "organizationId": "99d1****6124",
    "parentId": "99d1****6124"
}
```

## 错误码

访问错误码中心查看 API 相关错误码。

