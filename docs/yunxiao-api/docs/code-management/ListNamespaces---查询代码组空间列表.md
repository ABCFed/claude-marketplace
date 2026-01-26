# ListNamespaces - 查询代码组空间列表

---
source: https://help.aliyun.com/zh/yunxiao/developer-reference/listnamespaces-query-the-code-group-space-list
category: code-management
downloaded_at: 2026-01-26T14:33:29.299747
---

# ListNamespaces - 查询代码组空间列表

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
| 代码管理 | 代码组 | 只读   |

## 请求语法

```
GET https://{domain}/oapi/v1/codeup/organizations/{organizationId}/namespaces
```

## 请求头

| 参数              | 类型     | 是否必填 | 描述      | 示例值                          |
|-----------------|--------|------|---------|------------------------------|
| x-yunxiao-token | string | 是    | 个人访问令牌。 | pt-0fh3****0fbG_35af****0484 |

## 请求参数

| 参数             | 类型      | 位置    | 是否必填 | 描述                                                   | 示例值          |
|----------------|---------|-------|------|------------------------------------------------------|--------------|
| organizationId | string  | path  | 是    | 组织 ID。                                               | 99d1****71d4 |
| parentId       | integer | query | 否    | 父组 ID，若是查询组织下当前用户的组列表，可设置为空。                         | 26842        |
| page           | integer | query | 否    | 页码，默认从1开始，一般不要超过150页。                                | 1            |
| perPage        | integer | query | 否    | 每页大小，默认20，取值范围【1，100】。                               | 20           |
| search         | string  | query | 否    | 搜索关键字。                                               |              |
| orderBy        | string  | query | 否    | 排序字段，可选值包括 {created_at, updated_at}，默认值为 updated_at。 | updated_at   |
| sort           | string  | query | 否    | 排序方式，可选值包括{asc, desc}，默认值为 desc。                     | desc         |

## 请求示例

```
curl -X 'GET' \
  'https://{domain}/oapi/v1/codeup/organizations/{organizationId}/namespaces?parentId={parentId}&page={page}&perPage={perPage}&search={search}&orderBy={orderBy}&sort={sort}' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'
```

## 返回参数

| 参数                | 类型      | 描述                                           | 示例值                                                                                |
|-------------------|---------|----------------------------------------------|------------------------------------------------------------------------------------|
| -                 | array   |                                              |                                                                                    |
| -                 | object  |                                              |                                                                                    |
| avatarUrl         | string  | 头像地址。                                        | https://tcs-devops.aliyuncs.com/thumbnail/112afcb7a6a35c3f67f1bea827c4/w/100/h/100 |
| fullPath          | string  | 空间完整路径。                                      | org/test-group                                                                     |
| id                | integer | ID。                                          | 36932                                                                              |
| kind              | string  | 默认取值为 group。                                 | group                                                                              |
| name              | string  | 名称。                                          | test-group-name                                                                    |
| nameWithNamespace | string  | 完整名称。                                        | org/test-group-name                                                                |
| parentId          | integer | 上级路径的 ID。                                    | 20966                                                                              |
| path              | string  | 路径。                                          | test-group                                                                         |
| pathWithNamespace | string  | 完整路径。                                        | org/test-group                                                                     |
| visibility        | string  | 可见性，包括{private-私有，internal-组织内公开，public-公开}。 | private                                                                            |
| webUrl            | string  | 页面访问时的 URL。                                  | ""                                                                                 |

## 返回示例

```
[
    {
        "avatarUrl": "https://tcs-devops.aliyuncs.com/thumbnail/112afcb7a6a35c3f67f1bea827c4/w/100/h/100",
        "fullPath": "org/test-group",
        "id": 0,
        "kind": "group",
        "name": "test-group-name",
        "nameWithNamespace": "org/test-group-name",
        "parentId": 0,
        "path": "test-create-group",
        "pathWithNamespace": "codeup-test-org/test-create-group",
        "visibility": "private",
        "webUrl": "\"\""
    }
]
```

## 响应头

| 参数            | 描述     | 示例值                                  |
|---------------|--------|--------------------------------------|
| x-next-page   | 下一页。   | 2                                    |
| x-page        | 当前页。   | 1                                    |
| x-per-page    | 每页大小。  | 20                                   |
| x-prev-page   | 前一页。   | 0                                    |
| x-request-id  | 请求 ID。 | F7B85D1B-D1C2-140F-A039-341859F130B9 |
| x-total       | 总数。    | 10                                   |
| x-total-pages | 总分页数。  | 1                                    |

## 错误码

访问错误码中心查看 API 相关错误码。

