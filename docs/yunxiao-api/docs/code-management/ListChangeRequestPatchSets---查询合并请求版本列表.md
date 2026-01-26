# ListChangeRequestPatchSets - 查询合并请求版本列表

---
source: https://help.aliyun.com/zh/yunxiao/developer-reference/listchangerequestpatchsets-query-the-list-of-merge-request-versions
category: code-management
downloaded_at: 2026-01-26T14:35:41.087389
---

# ListChangeRequestPatchSets - 查询合并请求版本列表

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

	

只读

| 产品   | 资源   | 所需权限 |
|------|------|------|
| 代码管理 | 合并请求 | 只读   |

## 请求语法

```
GET https://{domain}/oapi/v1/codeup/organizations/{organizationId}/repositories/{repositoryId}/changeRequests/{localId}/diffs/patches
```

## 请求头

| 参数              | 类型     | 是否必填 | 描述      | 示例值                          |
|-----------------|--------|------|---------|------------------------------|
| x-yunxiao-token | string | 是    | 个人访问令牌。 | pt-0fh3****0fbG_35af****0484 |

## 请求参数

| 参数             | 类型      | 位置   | 是否必填 | 描述                            | 示例值                                   |
|----------------|---------|------|------|-------------------------------|---------------------------------------|
| organizationId | string  | path | 是    | 组织 ID。                        | 99d1****71d4                          |
| repositoryId   | string  | path | 是    | 代码库 ID 或者 URL-Encoder 编码的全路径。 | 2835387 或 codeup-org-id%2Fcodeup-demo |
| localId        | integer | path | 是    | 局部 ID。                        | 1                                     |

## 请求示例

```
curl -X 'GET' \
  'https://test.rdc.aliyuncs.com/oapi/v1/codeup/organizations/{organizationId}/repositories/{repositoryId}/changeRequests/{localId}/diffs/patches' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'
```

## 返回参数

| 参数                   | 类型      | 描述                                            | 示例值                                      |
|----------------------|---------|-----------------------------------------------|------------------------------------------|
| -                    | array   |                                               |                                          |
| -                    | object  |                                               |                                          |
| commitId             | string  | 版本对应的提交 ID。                                   | 1a072f5367c21f9de3464b8c0ee8546e47764d2d |
| createTime           | string  | 版本创建时间。                                       | 2023-05-30T02:53:36Z                     |
| patchSetBizId        | string  | 版本 ID，具有唯一性。                                  | 513fcfd81a9142d2bb0db4f72c0aa15b         |
| patchSetName         | string  | 版本名称。                                         | 版本1                                      |
| ref                  | string  | 版本对应的 ref 信息。                                 |                                          |
| relatedMergeItemType | string  | 关联的类型：MERGE_SOURCE - 合并源；MERGE_TARGET - 合并目标。 | MERGE_SOURCE                             |
| shortId              | string  | 提交 ID 对应的短 ID，通常为8位。                          | abcd1234                                 |
| versionNo            | integer | 版本号。                                          | 234                                      |

## 返回示例

```
[
    {
        "commitId": "1a072f5367c21f9de3464b8c0ee8546e47764d2d",
        "createTime": "2023-05-30T02:53:36Z",
        "patchSetBizId": "513fcfd81a9142d2bb0db4f72c0aa15b",
        "patchSetName": "版本1",
        "ref": "",
        "relatedMergeItemType": "MERGE_SOURCE",
        "shortId": "abcd1234",
        "versionNo": 234
    }
]
```

## 错误码

访问错误码中心查看 API 相关错误码。

