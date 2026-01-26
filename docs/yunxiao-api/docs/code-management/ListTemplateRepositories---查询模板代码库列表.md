# ListTemplateRepositories - 查询模板代码库列表

---
source: https://help.aliyun.com/zh/yunxiao/developer-reference/listtemplaterepositories-query-the-list-of-template-code-libraries
category: code-management
downloaded_at: 2026-01-26T14:33:18.707052
---

# ListTemplateRepositories - 查询模板代码库列表

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
| 代码管理 | 代码仓库 | 只读   |

## 请求语法

```
GET https://{domain}/oapi/v1/codeup/organizations/{organizationId}/repositories/templates
```

## 请求头

| 参数              | 类型     | 是否必填 | 描述      | 示例值                          |
|-----------------|--------|------|---------|------------------------------|
| x-yunxiao-token | string | 是    | 个人访问令牌。 | pt-0fh3****0fbG_35af****0484 |

## 请求参数

| 参数             | 类型      | 位置    | 是否必填 | 描述                       | 示例值          |
|----------------|---------|-------|------|--------------------------|--------------|
| organizationId | string  | path  | 是    | 组织 ID。                   | 99d1****71d4 |
| page           | integer | query | 否    | 页码，默认从1开始，一般不要超过150页。    | 1            |
| perPage        | integer | query | 否    | 每页大小，默认20，取值范围【1，100】。   | 20           |
| templateType   | integer | query | 是    | 模板类型，1-自定义模板库，2-系统内置模板库。 | 1            |

## 请求示例

```
curl -X 'GET' \
  'https://{domain}/oapi/v1/codeup/organizations/{organizationId}/repositories/templates?page=<page>&perPage=<perPage>&templateType=<templateType>' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'
```

## 返回参数

| 参数          | 类型      | 描述                            | 示例值                                 |
|-------------|---------|-------------------------------|-------------------------------------|
| -           | array   |                               |                                     |
| -           | object  |                               |                                     |
| avatarUrl   | string  | 代码库头像链接。                      | https://example/example/w/100/h/100 |
| description | string  | 代码库描述内容。                      | 描述信息的具体内容                           |
| name        | string  | 代码库名称。                        | template-repo                       |
| path        | string  | 代码库全路径，但若是系统预置模板库，则该属性为 null。 | null                                |
| projectId   | integer | 模板仓库 ID。                      | 1                                   |

## 返回示例

```
[
    {
        "avatarUrl": "https://example/example/w/100/h/100",
        "description": "模板库的描述内容",
        "name": "template-repo",
        "path": "null",
        "projectId": 1
    }
]
```

## 错误码

访问错误码中心查看 API 相关错误码。

