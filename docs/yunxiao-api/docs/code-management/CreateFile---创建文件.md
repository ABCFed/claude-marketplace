# CreateFile - 创建文件

---
source: https://help.aliyun.com/zh/yunxiao/developer-reference/createfile
category: code-management
downloaded_at: 2026-01-26T14:34:02.376723
---

# CreateFile - 创建文件

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
| 代码管理 | 文件  | 读写   |

## 请求语法

```
POST https://{domain}/oapi/v1/codeup/organizations/{organizationId}/repositories/{repositoryId}/files
```

## 请求头

| 参数              | 类型     | 是否必填 | 描述      | 示例值                          |
|-----------------|--------|------|---------|------------------------------|
| x-yunxiao-token | string | 是    | 个人访问令牌。 | pt-0fh3****0fbG_35af****0484 |

## 请求参数

| 参数             | 类型     | 位置   | 是否必填 | 描述                                                | 示例值                      |
|----------------|--------|------|------|---------------------------------------------------|--------------------------|
| organizationId | string | path | 是    | 组织 ID。                                            | 60de7a6852743a5162b5f957 |
| repositoryId   | string | path | 是    | 代码库 ID 或者 URL-Encoder 编码的全路径。请参见查询代码库列表获取相关信息。    | 2080972                  |
| -              | object | body | 否    |                                                   |                          |
| branch         | string | body | 是    | 分支名称。                                             | master                   |
| commitMessage  | string | body | 是    | 提交信息，非空，不超过102400个字符。                             | 创建xxx文件                  |
| content        | string | body | 是    | 文件内容。                                             | file content             |
| encoding       | string | body | 是    | 编码规则，可选值{text, base64}，默认为 text。                  | text                     |
| filePath       | string | body | 是    | 文件路径，非空，一般不要使用包含特殊符号的文件路径。需使用 URL-Encoder 编码进行处理。 | src%2Fmain%2Ftest.java   |

## 请求示例

```
curl -X 'POST' \
  'https://{domain}/oapi/v1/codeup/organizations/{organizationId}/repositories/{repositoryId}/files' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484' \
  --data '
    {
        "branch": "master",
        "commitMessage": "创建xxx文件",
        "content": "file content",
        "encoding": "text",
        "filePath": "src%2Fmain%2Ftest1.java"
    }'
```

## 返回参数

| 参数       | 类型     | 描述    | 示例值                 |
|----------|--------|-------|---------------------|
| -        | object |       |                     |
| branch   | string | 分支名称。 | master              |
| filePath | string | 文件路径。 | /src/main/test.java |

## 返回示例

```
{
    "branch": "master",
    "filePath": "/src/main/test.java"
}
```

## 错误码

访问错误码中心查看 API 相关错误码。

