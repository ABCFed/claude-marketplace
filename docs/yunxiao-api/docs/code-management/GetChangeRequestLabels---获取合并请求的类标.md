# GetChangeRequestLabels - 获取合并请求的类标

---
source: https://help.aliyun.com/zh/yunxiao/developer-reference/getchangerequestlabels
category: code-management
downloaded_at: 2026-01-26T14:35:30.025843
---

# GetChangeRequestLabels - 获取合并请求的类标

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
| 组织管理 | 项目类标 | 只读   |

## 请求语法

```
GET https://{domain}/oapi/v1/codeup/organizations/{organizationId}/repositories/{repositoryId}/changeRequests/{localId}/labels
```

## 请求头

| 参数              | 类型     | 是否必填 | 描述      | 示例值                          |
|-----------------|--------|------|---------|------------------------------|
| x-yunxiao-token | string | 是    | 个人访问令牌。 | pt-0fh3****0fbG_35af****0484 |

## 请求参数

| 参数             | 类型      | 位置   | 是否必填 | 描述                            | 示例值                                          |
|----------------|---------|------|------|-------------------------------|----------------------------------------------|
| organizationId | string  | path | 是    | 组织 ID。                        | 60d54f3daccf2bbd6659****                     |
| repositoryId   | string  | path | 是    | 代码库 ID 或者 URL-Encoder 编码的全路径。 | 2813489或者60de7a6852743a5162b5f957%2FDemoRepo |
| localId        | integer | path | 是    | 局部 ID，表示代码库中第几个合并请求。          | 42                                           |

## 请求示例

```
curl -X 'GET' \
  'https://{domain}/oapi/v1/codeup/organizations/60d54f3daccf2bbd6659****/repositories/2813489/changeRequests/42/labels' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'
```

## 返回参数

- #006AD4
- #2FA6A4
- #6190AC
- #4B81D0
- #4D5DBB
- #A16AD7
- #3BA630
- #95B44F
- #AA945F
- #B36A53
- #FD842F
- #EF433B

| 参数          | 类型     | 描述                                                                                                            | 示例值                              |
|-------------|--------|---------------------------------------------------------------------------------------------------------------|----------------------------------|
| -           | array  |                                                                                                               |                                  |
| -           | object |                                                                                                               |                                  |
| color       | string | 类标颜色（十六进制格式）： #006AD4 #2FA6A4 #6190AC #4B81D0 #4D5DBB #A16AD7 #3BA630 #95B44F #AA945F #B36A53 #FD842F #EF433B | #006AD4                          |
| description | string | 类标描述。                                                                                                         | 表示代码中的错误                         |
| id          | string | 类标 ID。                                                                                                        | 68c1bd9b8515477fa86fac5exxxxx941 |
| name        | string | 类标名称。                                                                                                         | Bug                              |

- #006AD4
- #2FA6A4
- #6190AC
- #4B81D0
- #4D5DBB
- #A16AD7
- #3BA630
- #95B44F
- #AA945F
- #B36A53
- #FD842F
- #EF433B

## 返回示例

```
[
    {
        "color": "#006AD4",
        "description": "表示代码中的错误",
        "id": "68c1bd9b8515477fa86fac5exxxxx941",
        "name": "Bug"
    }
]
```

## 错误码

访问错误码中心查看 API 相关错误码。

