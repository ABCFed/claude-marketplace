# ListOrganizations - 查询组织列表

---
source: https://help.aliyun.com/zh/yunxiao/developer-reference/listorganizations
category: organization
downloaded_at: 2026-01-26T14:42:09.856006
---

# ListOrganizations - 查询组织列表

## 前提条件

获取服务接入点，替换 API 请求语法中的 <domain> 。关于如何获取domain，请参见服务接入点（domain）。

获取个人访问令牌，具体操作，请参见获取个人访问令牌。

获取organizationId，请前往组织管理后台的基本信息页面获取组织 ID 。

- 获取服务接入点，替换 API 请求语法中的 <domain> 。关于如何获取domain，请参见服务接入点（domain）。
- 获取个人访问令牌，具体操作，请参见获取个人访问令牌。
- 获取organizationId，请前往组织管理后台的基本信息页面获取组织 ID 。

## 授权信息

| 产品   | 资源  | 所需权限 |
|------|-----|------|
| 组织管理 | 组织  | 只读   |

## 请求语法

```
GET https://{domain}/oapi/v1/platform/organizations
```

## 请求头

| 参数              | 类型     | 是否必填 | 描述      | 示例值                          |
|-----------------|--------|------|---------|------------------------------|
| x-yunxiao-token | string | 是    | 个人访问令牌。 | pt-0fh3****0fbG_35af****0484 |

## 请求参数

| 参数      | 类型      | 位置    | 是否必填 | 描述                                                               | 示例值          |
|---------|---------|-------|------|------------------------------------------------------------------|--------------|
| userId  | string  | query | 否    | 用户 ID，标准版：返回个人访问令牌对应用户加入的组织列表，此参数无效；专属版：为空返回所有组织列表，不为空返回加入的组织列表。 | 99d1****6124 |
| page    | integer | query | 否    | [仅专属版适用]当前页，默认1。                                                 | 1            |
| perPage | integer | query | 否    | [仅专属版适用]每页数据条数，1<=perPage<=100，默认100。                            | 100          |

## 请求示例

```
curl -X 'GET' \
  'https://{domain}/oapi/v1/platform/organizations?userId={userId}&page={page}&perPage={perPage}' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'
```

## 返回参数

| 参数          | 类型     | 描述     | 示例值                      |
|-------------|--------|--------|--------------------------|
| -           | array  |        |                          |
| -           | object |        |                          |
| createdAt   | string | 创建时间。  | 2023-08-31T03:59:16.201Z |
| creatorId   | string | 组织创建者。 | 99d1****6124             |
| defaultRole | string | 默认角色。  | 99d1****6124             |
| description | string | 组织描述。  | 示例描述                     |
| id          | string | 组织 ID。 | 99d1****6124             |
| name        | string | 组织名称。  | 示例名                      |
| updateAt    | string | 更新时间。  | 2023-08-31T03:59:16.201Z |

## 返回示例

```
[
    {
        "createdAt": "2023-08-31T03:59:16.201Z",
        "creatorId": "99d1****6124",
        "defaultRole": "99d1****6124",
        "description": "示例描述",
        "id": "99d1****6124",
        "name": "示例名",
        "updateAt": "2023-08-31T03:59:16.201Z"
    }
]
```

## 响应头

| 参数            | 描述      | 示例值 |
|---------------|---------|-----|
| x-next-page   | 下一页。    | 2   |
| x-page        | 当前页。    | 1   |
| x-per-page    | 每页数据条数。 | 100 |
| x-prev-page   | 上一页。    | 1   |
| x-total       | 总数据量。   | 2   |
| x-total-pages | 总分页数。   | 1   |

## 错误码

访问错误码中心查看 API 相关错误码。

