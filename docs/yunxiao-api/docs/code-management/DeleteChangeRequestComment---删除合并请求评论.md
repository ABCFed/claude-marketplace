# DeleteChangeRequestComment - 删除合并请求评论

---
source: https://help.aliyun.com/zh/yunxiao/developer-reference/deletechangerequestcomment
category: code-management
downloaded_at: 2026-01-26T14:36:17.583110
---

# DeleteChangeRequestComment - 删除合并请求评论

## 服务接入点与授权信息

获取服务接入点，替换 API 请求语法中的 <domain> ：服务接入点（domain）。

获取个人访问令牌，具体操作，请参见获取个人访问令牌。

获取organizationId，请前往组织管理后台的基本信息页面获取组织 ID 。

- 获取服务接入点，替换 API 请求语法中的 <domain> ：服务接入点（domain）。
- 获取个人访问令牌，具体操作，请参见获取个人访问令牌。
- 获取organizationId，请前往组织管理后台的基本信息页面获取组织 ID 。

产品

	

资源

	

所需权限




代码管理

	

合并请求

	

读写

| 产品   | 资源   | 所需权限 |
|------|------|------|
| 代码管理 | 合并请求 | 读写   |

```
DELETE https://{domain}/oapi/v1/codeup/organizations/{organizationId}/repositories/{repositoryId}/changeRequests/{localId}/comments/{commentBizId}
```

| 参数              | 类型     | 是否必填 | 描述      | 示例值                          |
|-----------------|--------|------|---------|------------------------------|
| x-yunxiao-token | string | 是    | 个人访问令牌。 | pt-0fh3****0fbG_35af****0484 |

| 参数             | 类型      | 位置   | 是否必填 | 描述                            | 示例值                                          |
|----------------|---------|------|------|-------------------------------|----------------------------------------------|
| organizationId | string  | path | 是    | 组织 ID。                        | 60d54f3daccf2bbd6659f3ad                     |
| repositoryId   | string  | path | 是    | 代码库 ID 或者 URL-Encoder 编码的全路径。 | 2813489或者60de7a6852743a5162b5f957%2FDemoRepo |
| localId        | integer | path | 是    | 局部 ID，表示代码库中第几个合并请求。          | 1                                            |
| commentBizId   | string  | path | 是    | 评论 bizId。                     | bf117304dfe44d5d9b1132f348edf92e             |

```
curl -X 'DELETE' \
  'https://{domain}/oapi/v1/codeup/organizations/60d54f3daccf2bbd6659f3ad/repositories/2813489或者60de7a6852743a5162b5f957%2FDemoRepo/changeRequests/1/comments/bf117304dfe44d5d9b1132f348edf92e' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'
```

| 参数     | 类型      | 描述    | 示例值  |
|--------|---------|-------|------|
| -      | object  |       |      |
| result | boolean | 执行结果。 | true |

```
{
    "result": true
}
```

访问错误码中心查看 API 相关错误码。

