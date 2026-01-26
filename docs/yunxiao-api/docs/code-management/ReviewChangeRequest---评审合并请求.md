# ReviewChangeRequest - 评审合并请求

---
source: https://help.aliyun.com/zh/yunxiao/developer-reference/reviewchangerequest-review-merge-request
category: code-management
downloaded_at: 2026-01-26T14:35:44.694835
---

# ReviewChangeRequest - 评审合并请求

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

## 请求语法

```
POST https://{domain}/oapi/v1/codeup/organizations/{organizationId}/repositories/{repositoryId}/changeRequests/{localId}/review
```

## 请求头

| 参数              | 类型     | 是否必填 | 描述      | 示例值                          |
|-----------------|--------|------|---------|------------------------------|
| x-yunxiao-token | string | 是    | 个人访问令牌。 | pt-0fh3****0fbG_35af****0484 |

## 请求参数

| 参数                    | 类型            | 位置   | 是否必填 | 描述                             | 示例值                                          |
|-----------------------|---------------|------|------|--------------------------------|----------------------------------------------|
| organizationId        | string        | path | 是    | 组织 ID。                         | 60d54f3daccf2bbd6659f3ad                     |
| repositoryId          | string        | path | 是    | 代码库 ID 或者 URL-Encoder 编码的全路径。  | 2813489或者60de7a6852743a5162b5f957%2FDemoRepo |
| localId               | integer       | path | 是    | 局部 ID。                         | 1                                            |
| -                     | object        | body | 否    |                                |                                              |
| reviewComment         | string        | body | 否    | 评论内容。                          | change request comment content               |
| reviewOpinion         | string        | body | 否    | 评审意见：PASS - 通过；NOT_PASS - 不通过。 | PASS                                         |
| submitDraftCommentIds | array[string] | body | 否    | 提交的草稿评论 ID 列表。                 | [“4ff23jj62c795xxxb468af8”]                  |

## 请求示例

```
curl -X 'POST' \
  'https://test.rdc.aliyuncs.com/oapi/v1/codeup/organizations/60d54f3daccf2bbd6659f3ad/repositories/2813489或者60de7a6852743a5162b5f957%2FDemoRepo/changeRequests/1/review' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484' \
  --data '
    {
        "reviewComment": "change request comment content",
        "reviewOpinion": "PASS",
        "submitDraftCommentIds": ["4ff23jj62c795xxxb468af8"]
    }'
```

## 返回参数

| 参数     | 类型      | 描述      | 示例值   |
|--------|---------|---------|-------|
| -      | object  |         |       |
| result | boolean | 是否执行成功。 | false |

## 返回示例

```
{
    "result": true
}
```

## 错误码

访问错误码中心查看 API 相关错误码。

