# DeleteProtectedBranch - 移除保护分支

---
source: https://help.aliyun.com/zh/yunxiao/developer-reference/deleteprotectedbranch
category: code-management
downloaded_at: 2026-01-26T14:34:52.019837
---

# DeleteProtectedBranch - 移除保护分支

## 服务接入点与授权信息

获取服务接入点，替换 API 请求语法中的 <domain> ：服务接入点（domain）。

获取个人访问令牌，具体操作，请参见获取个人访问令牌。

获取organizationId，请前往组织管理后台的基本信息页面获取组织 ID 。

- 获取服务接入点，替换 API 请求语法中的 <domain> ：服务接入点（domain）。
- 获取个人访问令牌，具体操作，请参见获取个人访问令牌。
- 获取organizationId，请前往组织管理后台的基本信息页面获取组织 ID 。

| 产品   | 资源   | 所需权限 |
|------|------|------|
| 代码管理 | 保护分支 | 读写   |

## 请求语法

```
DELETE https://{domain}/oapi/v1/codeup/organizations/{organizationId}/repositories/{repositoryId}/protectedBranches/{id}
```

## 请求头

| 参数              | 类型     | 是否必填 | 描述      | 示例值                          |
|-----------------|--------|------|---------|------------------------------|
| x-yunxiao-token | string | 是    | 个人访问令牌。 | pt-0fh3****0fbG_35af****0484 |

## 请求参数

| 参数             | 类型      | 位置   | 是否必填 | 描述                            | 示例值                      |
|----------------|---------|------|------|-------------------------------|--------------------------|
| organizationId | string  | path | 是    | 组织 ID。                        | 611b75680fc7bf0dbe1dce55 |
| repositoryId   | integer | path | 是    | 代码库 ID 或者 URL-Encoder 编码的全路径。 | 2813489                  |
| id             | integer | path | 是    | 保护分支规则主键 ID。                  | 5326                     |

## 请求示例

```
curl -X 'DELETE' \
  'https://test.rdc.aliyuncs.com/oapi/v1/codeup/organizations/{organizationId}/repositories/{repositoryId}/protectedBranches/{id}' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'
```

## 返回参数

| 参数     | 类型      | 描述      | 示例值   |
|--------|---------|---------|-------|
| -      | object  |         |       |
| result | boolean | 是否执行成功。 | false |

## 返回示例

```
{
    "result": false
}
```

## 错误码

访问错误码中心查看 API 相关错误码。

