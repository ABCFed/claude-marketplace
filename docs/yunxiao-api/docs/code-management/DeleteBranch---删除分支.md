# DeleteBranch - 删除分支

---
source: https://help.aliyun.com/zh/yunxiao/developer-reference/deletebranch-delete-branch
category: code-management
downloaded_at: 2026-01-26T14:33:40.204799
---

# DeleteBranch - 删除分支

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
| 代码管理 | 分支  | 读写   |

## 请求语法

```
DELETE https://{domain}/oapi/v1/codeup/organizations/{organizationId}/repositories/{repositoryId}/branches/{branchName}
```

## 请求头

| 参数              | 类型     | 是否必填 | 描述      | 示例值                          |
|-----------------|--------|------|---------|------------------------------|
| x-yunxiao-token | string | 是    | 个人访问令牌。 | pt-0fh3****0fbG_35af****0484 |

## 请求参数

| 参数             | 类型     | 位置   | 是否必填 | 描述                                   | 示例值             |
|----------------|--------|------|------|--------------------------------------|-----------------|
| organizationId | string | path | 是    | 组织 ID。                               | 99d1****71d4    |
| repositoryId   | string | path | 是    | 代码库 ID 或者 URL-Encoder 编码的全路径。        | 2813489         |
| branchName     | string | path | 是    | 分支名称（若有特殊符号，可使用 URL-Encoder 进行编码处理）。 | feature/cd-flow |

## 请求示例

```
curl -X 'DELETE' \
  'https://{domain}/oapi/v1/codeup/organizations/{organizationId}/repositories/{repositoryId}/branches/{branchName}' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'
```

## 返回参数

| 参数         | 类型     | 描述        | 示例值             |
|------------|--------|-----------|-----------------|
| -          | object |           |                 |
| branchName | string | 被删除的分支名称。 | feature/cd-flow |

## 返回示例

```
{
    "branchName": "feature/cd-flow"
}
```

## 错误码

访问错误码中心查看 API 相关错误码。

