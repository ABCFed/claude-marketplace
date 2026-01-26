# GetNamespace - 查询代码组空间信息

---
source: https://help.aliyun.com/zh/yunxiao/developer-reference/getnamespace-query-code-group-space-information
category: code-management
downloaded_at: 2026-01-26T14:33:25.827112
---

# GetNamespace - 查询代码组空间信息

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
GET https://{domain}/oapi/v1/codeup/organizations/{organizationId}/namespaces/{namespaceId}
```

## 请求头

| 参数              | 类型     | 是否必填 | 描述      | 示例值                          |
|-----------------|--------|------|---------|------------------------------|
| x-yunxiao-token | string | 是    | 个人访问令牌。 | pt-0fh3****0fbG_35af****0484 |

## 请求参数

| 参数             | 类型     | 位置   | 是否必填 | 描述                                                             | 示例值                                                              |
|----------------|--------|------|------|----------------------------------------------------------------|------------------------------------------------------------------|
| organizationId | string | path | 是    | 组织 ID。                                                         | 99d1****71d4                                                     |
| namespaceId    | string | path | 是    | 代码组 ID，或者全路径（需使用 URL-Encoder 编码进行处理）。请参见查询代码组空间列表获取代码组 ID或全路径。 | 36612（代码组 ID）或99d1****71d4%2Ftest-parent-group%2Ftest-group（全路径） |

## 请求示例

```
curl -X 'GET' \
  'https://{domain}/oapi/v1/codeup/organizations/{organizationId}/namespaces/{namespaceId}' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'
```

## 返回参数

| 参数                | 类型      | 描述                                           | 示例值                                                                                |
|-------------------|---------|----------------------------------------------|------------------------------------------------------------------------------------|
| -                 | object  |                                              |                                                                                    |
| avatarUrl         | string  | 头像地址，该字段非必返回，当上传头像不为空时返回。                    | https://tcs-devops.aliyuncs.com/thumbnail/112afcb7a6a35c3f67f1bea827c4/w/100/h/100 |
| fullPath          | string  | 空间完整路径。                                      | 99d1****71d4/test-parent-group/test-group                                          |
| id                | integer | ID。                                          | 36612                                                                              |
| kind              | string  | 默认取值为 group。                                 | Group                                                                              |
| name              | string  | 名称。                                          | test-group                                                                         |
| nameWithNamespace | string  | 完整名称。                                        | 99d1****71d4 / test-parent-group / test-group（斜杠两侧有空格）                             |
| parentId          | integer | 上级路径的 ID。                                    | 26842                                                                              |
| path              | string  | 路径。                                          | test-group                                                                         |
| pathWithNamespace | string  | 完整路径。                                        | 99d1****71d4/test-parent-group/test-group                                          |
| visibility        | string  | 可见性，包括{private-私有，internal-组织内公开，public-公开}。 | private                                                                            |
| webUrl            | string  | 页面访问时的 URL。                                  | ""                                                                                 |

## 返回示例

```
{
    "avatarUrl": "https://tcs-devops.aliyuncs.com/thumbnail/112afcb7a6a35c3f67f1bea827c4/w/100/h/100",
    "fullPath": "99d1****71d4/test-parent-group/test-group",
    "id": 36612,
    "kind": "Group",
    "name": "test-group",
    "nameWithNamespace": "99d1****71d4 / test-parent-group / test-group",
    "parentId": 26842,
    "path": "test-group",
    "pathWithNamespace": "99d1****71d4/test-parent-group/test-group",
    "visibility": "private",
    "webUrl": "\"\""
}
```

## 错误码

访问错误码中心查看 API 相关错误码。

