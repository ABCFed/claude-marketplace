# CreateGroup - 创建代码组

---
source: https://help.aliyun.com/zh/yunxiao/developer-reference/creategroup-creates-a-code-group
category: code-management
downloaded_at: 2026-01-26T14:33:22.310343
---

# CreateGroup - 创建代码组

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
| 代码管理 | 代码组 | 读写   |

## 请求语法

```
POST https://{domain}/oapi/v1/codeup/organizations/{organizationId}/groups
```

## 请求头

| 参数              | 类型     | 是否必填 | 描述      | 示例值                          |
|-----------------|--------|------|---------|------------------------------|
| x-yunxiao-token | string | 是    | 个人访问令牌。 | pt-0fh3****0fbG_35af****0484 |

## 请求参数

| 参数             | 类型      | 位置   | 是否必填 | 描述                                               | 示例值                                                                                |
|----------------|---------|------|------|--------------------------------------------------|------------------------------------------------------------------------------------|
| organizationId | string  | path | 是    | 组织 ID。                                           | 60de7a6852743a5162b5f957                                                           |
| -              | object  | body | 否    |                                                  |                                                                                    |
| avatar         | string  | body | 否    | 代码组头像地址。                                         | https://tcs-devops.aliyuncs.com/thumbnail/112afcb7a6a35c3f67f1bea827c4/w/100/h/100 |
| description    | string  | body | 否    | 代码组描述内容，最长不超过65535个字符。                           | 描述信息的具体内容"                                                                         |
| name           | string  | body | 否    | 代码组名称。                                           | test-create-group                                                                  |
| parentId       | integer | body | 否    | 代码组父路径 ID，若为空，则创建在组织路径下。                         | 26842                                                                              |
| path           | string  | body | 否    | 代码组路径。                                           | test-create-group                                                                  |
| visibility     | string  | body | 否    | 代码组的可见性，包括{private-私有，internal-组织内公开，public-公开}。 | private                                                                            |

## 请求参数

| 参数             | 类型      | 位置   | 是否必填 | 描述                                               | 示例值                                                                                |
|----------------|---------|------|------|--------------------------------------------------|------------------------------------------------------------------------------------|
| organizationId | string  | path | 是    | 组织 ID。                                           | 60de7a6852743a5162b5f957                                                           |
| -              | object  | body | 否    |                                                  |                                                                                    |
| avatar         | string  | body | 否    | 代码组头像地址。                                         | https://tcs-devops.aliyuncs.com/thumbnail/112afcb7a6a35c3f67f1bea827c4/w/100/h/100 |
| description    | string  | body | 否    | 代码组描述内容，最长不超过65535个字符。                           | 描述信息的具体内容"                                                                         |
| name           | string  | body | 否    | 代码组名称。                                           | test-create-group                                                                  |
| parentId       | integer | body | 否    | 代码组父路径 ID，若为空，则创建在组织路径下。                         | 26842                                                                              |
| path           | string  | body | 否    | 代码组路径。                                           | test-create-group                                                                  |
| visibility     | string  | body | 否    | 代码组的可见性，包括{private-私有，internal-组织内公开，public-公开}。 | private                                                                            |

## 请求示例

```
curl -X 'POST' \
  'https://{domain}/oapi/v1/codeup/organizations/{organizationId}/groups' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484' \
  --data '
    {
        "avatar": "https://tcs-devops.aliyuncs.com/thumbnail/112afcb7a6a35c3f67f1bea827c4/w/100/h/100",
        "description": "测试验证",
        "name": "test-create-group",
        "parentId": 0,
        "path": "test-create-group",
        "visibility": "private"
    }'
```

## 返回参数

| 参数                | 类型      | 描述                                                 | 示例值                                                                                |
|-------------------|---------|----------------------------------------------------|------------------------------------------------------------------------------------|
| -                 | object  |                                                    |                                                                                    |
| avatarUrl         | string  | 头像地址。                                              | https://tcs-devops.aliyuncs.com/thumbnail/112afcb7a6a35c3f67f1bea827c4/w/100/h/100 |
| description       | string  | 代码组描述信息。                                           | 描述信息的具体内容"                                                                         |
| id                | integer | 代码组 ID，也可作为代码空间 ID 使用。                             | 18685                                                                              |
| name              | string  | 代码组名称。                                             | test-create-group                                                                  |
| nameWithNamespace | string  | 代码组完整名称。                                           | codeup-test-org / test-create-group （斜杠两侧有空格）                                      |
| ownerId           | integer | 代码组创建者。                                            | 19230                                                                              |
| parentId          | integer | 上级路径的 ID。                                          | 26842                                                                              |
| path              | string  | 代码组路径。                                             | test-create-group                                                                  |
| pathWithNamespace | string  | 代码组完整路径。                                           | codeup-test-org/test-create-group                                                  |
| visibility        | string  | 可见性：private 表示私有的，internal 表示组织内公开，public 表示全平台公开。 | private                                                                            |
| webUrl            | string  | 页面访问时的 URL。                                        | ""                                                                                 |

## 返回示例

```
{
    "avatarUrl": "https://tcs-devops.aliyuncs.com/thumbnail/112afcb7a6a35c3f67f1bea827c4/w/100/h/100",
    "description": "描述信息的具体内容",
    "id": 0,
    "name": "test-create-group",
    "nameWithNamespace": "codeup-test-org / test-create-group",
    "ownerId": 0,
    "parentId": 0,
    "path": "test-create-group",
    "pathWithNamespace": "codeup-test-org/test-create-group",
    "visibility": "private",
    "webUrl": "\"\""
}
```

## 错误码

访问错误码中心查看 API 相关错误码。

