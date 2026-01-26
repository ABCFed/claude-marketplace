# UpdateCheckRun - 更新运行检查

---
source: https://help.aliyun.com/zh/yunxiao/developer-reference/updatecheckrun
category: code-management
downloaded_at: 2026-01-26T14:36:39.434774
---

# UpdateCheckRun - 更新运行检查

## 服务接入点与授权信息

获取服务接入点，替换 API 请求语法中的 <domain> ：服务接入点（domain）。

获取个人访问令牌，具体操作，请参见获取个人访问令牌。

获取organizationId，请前往组织管理后台的基本信息页面获取组织 ID 。

- 获取服务接入点，替换 API 请求语法中的 <domain> ：服务接入点（domain）。
- 获取个人访问令牌，具体操作，请参见获取个人访问令牌。
- 获取organizationId，请前往组织管理后台的基本信息页面获取组织 ID 。

| 产品   | 资源   | 所需权限 |
|------|------|------|
| 代码管理 | 运行检查 | 读写   |

## 请求语法

```
POST https://{domain}/oapi/v1/codeup/organizations/{organizationId}/repositories/{repositoryId}/checkRuns/{checkRunId}
```

## 请求头

| 参数              | 类型     | 是否必填 | 描述      | 示例值                          |
|-----------------|--------|------|---------|------------------------------|
| x-yunxiao-token | string | 是    | 个人访问令牌。 | pt-0fh3****0fbG_35af****0484 |

## 请求参数

| 参数              | 类型      | 位置   | 是否必填 | 描述                                                                                                                                                | 示例值                     |
|-----------------|---------|------|------|---------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------|
| organizationId  | string  | path | 是    | 组织 ID。                                                                                                                                            | 5ebbc0228123212b59xxxxx |
| repositoryId    | string  | path | 是    | 代码库 ID 或者 URL-Encoder 编码的全路径。                                                                                                                     | 2835387                 |
| checkRunId      | integer | path | 是    | 运行检查 ID，唯一标识。                                                                                                                                     | 1                       |
| -               | object  | body | 否    |                                                                                                                                                   |                         |
| annotations     | array   | body | 否    | 注解信息。                                                                                                                                             |                         |
| -               | object  | body | 否    |                                                                                                                                                   |                         |
| annotationLevel | string  | body | 否    | 检查注解的等级：notice - 轻微；warning - 警告；failure - 严重。                                                                                                    | warning                 |
| endColumn       | integer | body | 否    | 结束列，当且仅当 startLine=endLine 时，该字段值有效。                                                                                                              | 4                       |
| endLine         | integer | body | 否    | 结束行。                                                                                                                                              | 2                       |
| message         | string  | body | 否    | 摘要信息。                                                                                                                                             | ""                      |
| path            | string  | body | 否    | 文件路径。                                                                                                                                             | demo/test.txt           |
| rawDetails      | string  | body | 否    | 详情信息，限制64KB 以内。                                                                                                                                   | ""                      |
| startColumn     | integer | body | 否    | 起始列，当且仅当 startLine=endLine 时，该字段值有效。                                                                                                              | 3                       |
| startLine       | integer | body | 否    | 起始行，需要用户自行确认文件行数的有效性，否则无法展示，其余类似。                                                                                                                 | 1                       |
| title           | string  | body | 否    | 检查注解的标题。                                                                                                                                          | ""                      |
| completedAt     | string  | body | 否    | 三方检查的完结时间，格式为 ISO 8601，如2024-03-15T08:00:00Z。                                                                                                     | 2023-03-15T08:00:00Z    |
| conclusion      | string  | body | 否    | 结论：cancelled - 已取消；failure - 失败；neutral - 中立状态，算作成功状态；success - 成功；skipped - 跳过，算作成功状态；timed_out - 超时。 当直接写入 conclusion 时，status 自动设置为 completed。 | success                 |
| detailsUrl      | string  | body | 否    | 三方交互系统的详情地址，由用户自行决定，平台仅提供跳转能力。                                                                                                                    | xxx                     |
| externalId      | string  | body | 否    | 外部系统的 ID，由用户自行决定写入的信息。                                                                                                                            | 42                      |
| name            | string  | body | 否    | check run 的名称，长度限制在50以内。                                                                                                                          | my-check-ci             |
| output          | object  | body | 否    |                                                                                                                                                   |                         |
| images          | array   | body | 否    | 可展示的图片，不超过3张。                                                                                                                                     |                         |
| -               | object  | body | 否    |                                                                                                                                                   |                         |
| alt             | string  | body | 否    | alt 文本信息。                                                                                                                                         | test-image-alt          |
| caption         | string  | body | 否    | 图片信息的简要描述。                                                                                                                                        | test                    |
| imageUrl        | string  | body | 否    | 图片地址，须确保能够有效访问，否则页面无法加载。                                                                                                                          | xxx                     |
| summary         | string  | body | 否    | 摘要信息，支持 Markdown 格式，最大字符长度为64KB，即65535个字符。                                                                                                        | ""                      |
| text            | string  | body | 否    | 详情信息，支持 Markdown 格式，最大字符长度为64KB，即65535个字符。                                                                                                        | ""                      |
| title           | string  | body | 否    | 标题。                                                                                                                                               | Mighty Readme report    |
| startedAt       | string  | body | 否    | 三方检查的开始时间，格式为 ISO 8601，如2024-03-15T08:00:00Z。                                                                                                     | 2023-03-15T08:00:00Z    |
| status          | string  | body | 否    | 状态：queued - 队列中；in_progress - 运行中；completed - 已完成。当写入 completed 时，需要同时写入 conclusion。                                                              | completed               |

## 请求示例

```
curl -X 'POST' \
  'https://test.rdc.aliyuncs.com/oapi/v1/codeup/organizations/{organizationId}/repositories/{repositoryId}/checkRuns/{checkRunId}' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484' \
  --data '
    {
        "annotations": [
            {
                "annotationLevel": "warning",
                "endColumn": 4,
                "endLine": 2,
                "message": "",
                "path": "demo/test.txt",
                "rawDetails": "",
                "startColumn": 3,
                "startLine": 1,
                "title": ""
            }
        ],
        "completedAt": "2023-03-15T08:00:00Z",
        "conclusion": "success",
        "detailsUrl": "xxx",
        "externalId": "42",
        "name": "my-check-ci",
        "output": {
            "images": [
                {
                    "alt": "test-image-alt",
                    "caption": "test",
                    "imageUrl": "xxx"
                }
            ],
            "summary": "",
            "text": "",
            "title": "Mighty Readme report"
        },
        "startedAt": "2023-03-15T08:00:00Z",
        "status": "completed"
    }'
```

## 返回参数

| 参数              | 类型      | 描述                                                                                                     | 示例值                                      |
|-----------------|---------|--------------------------------------------------------------------------------------------------------|------------------------------------------|
| -               | object  |                                                                                                        |                                          |
| annotations     | array   | 注解信息。                                                                                                  |                                          |
| -               | object  |                                                                                                        |                                          |
| annotationLevel | string  | 检查注解的等级：notice - 轻微；warning - 警告；failure - 严重。                                                         | warning                                  |
| createdAt       | string  | 创建时间。                                                                                                  | 2022-01-14T21:08:26+08:00                |
| endColumn       | integer | 结束列，当且仅当 startLine=endLine 时，该字段值有效。                                                                   | 4                                        |
| endLine         | integer | 结束行。                                                                                                   | 2                                        |
| id              | integer | 检查注解 ID，唯一标识。                                                                                          | 1                                        |
| message         | string  | 摘要信息。                                                                                                  | ""                                       |
| path            | string  | 文件路径。                                                                                                  | demo/test.txt                            |
| rawDetails      | string  | 详情信息，限制64KB 以内。                                                                                        | ""                                       |
| startColumn     | integer | 起始列，当且仅当 startLine=endLine 时，该字段值有效。                                                                   | 3                                        |
| startLine       | integer | 起始行，需要用户自行确认文件行数的有效性，否则无法展示，其余类似。                                                                      | 1                                        |
| title           | string  | 检查注解的标题。                                                                                               | ""                                       |
| updatedAt       | string  | 更新时间。                                                                                                  | 2022-01-14T21:08:26+08:00                |
| checkSuite      | object  | 检查套件信息。                                                                                                |                                          |
| id              | integer | 唯一标识。                                                                                                  | 1                                        |
| completedAt     | string  | 三方检查的完成时间。                                                                                             | 2023-03-15T08:00:00Z                     |
| conclusion      | string  | 结论：cancelled - 已取消；failure - 失败；neutral - 中立状态，算作成功状态；success - 成功；skipped - 跳过，算作成功状态；timed_out - 超时。 | success                                  |
| createdAt       | string  | 回写记录的创建时间。                                                                                             | 2023-03-15T08:00:00Z                     |
| detailsUrl      | string  | 三方交互系统的链接地址，由用户自行决定，平台仅提供跳转能力。                                                                         | xxx                                      |
| externalId      | string  | 外部系统 ID。                                                                                               | 42                                       |
| headSha         | string  | 提交 ID。                                                                                                 | 40f4ccfe019cdd4a62d4acb0c57130106fc7e1be |
| id              | integer | 唯一标识。                                                                                                  | 5240                                     |
| name            | string  | check run 的名称。                                                                                         | my-check-ci                              |
| output          | object  | 页面展示信息。                                                                                                |                                          |
| images          | array   | 可展示的图片，不超过3张。                                                                                          |                                          |
| -               | object  |                                                                                                        |                                          |
| alt             | string  | alt 文本信息。                                                                                              | test-image-alt                           |
| caption         | string  | 图片信息的简要描述。                                                                                             | test                                     |
| imageUrl        | string  | 图片地址，须确保能够有效访问，否则页面无法加载。                                                                               | xxx                                      |
| summary         | string  | 摘要信息，支持 MarkDown 格式，最大字符长度为64KB，即65535个字符。                                                             | ""                                       |
| text            | string  | 详情信息，支持 MarkDown 格式，最大字符长度为64KB，即65535个字符。                                                             | ""                                       |
| title           | string  | 标题。                                                                                                    | Mighty Readme report                     |
| startedAt       | string  | 三方检查的开始时间。                                                                                             | 2023-03-15T08:00:00Z                     |
| status          | string  | 状态：queued - 队列中；in_progress - 运行中；completed - 完成。                                                      | completed                                |
| updatedAt       | string  | 回写记录的更新时间。                                                                                             | 2022-01-14T21:08:26+08:00                |
| writer          | object  | 写入人信息。                                                                                                 | ""                                       |
| id              | string  | 用户 ID。                                                                                                 | xxx                                      |
| logoUrl         | string  | 用户头像地址。                                                                                                | xxx                                      |
| name            | string  | 用户名称。                                                                                                  | test-codeup                              |
| slug            | string  | 用户登录名。                                                                                                 | test-codeup                              |
| type            | string  | 写入人类型：User - 用户；Bot - 应用（暂无）。                                                                          | User                                     |

## 返回示例

```
{
    "annotations": [
        {
            "annotationLevel": "notice",
            "createdAt": "2022-01-14T21:08:26+08:00",
            "endColumn": 5,
            "endLine": 2,
            "id": 524836,
            "message": "",
            "path": "demo/test.txt",
            "rawDetails": "",
            "startColumn": 3,
            "startLine": 1,
            "title": "",
            "updatedAt": "2022-01-14T21:08:26+08:00"
        }
    ],
    "checkSuite": {
        "id": 1
    },
    "completedAt": "2023-03-15T08:00:00Z",
    "conclusion": "success",
    "createdAt": "2022-01-14T21:08:26+08:00",
    "detailsUrl": "xxx",
    "externalId": "42",
    "headSha": "40f4ccfe019cdd4a62d4acb0c57130106fc7e1be",
    "id": 524836,
    "name": "my-check-ci",
    "output": {
        "images": [
            {
                "alt": "test-image-alt",
                "caption": "test",
                "imageUrl": "xxx"
            }
        ],
        "summary": "",
        "text": "",
        "title": "Mighty Readme report"
    },
    "startedAt": "2023-03-15T08:00:00Z",
    "status": "completed",
    "updatedAt": "2022-01-14T21:08:26+08:00",
    "writer": {
        "id": "xxx",
        "logoUrl": "xxx",
        "name": "test-codeup",
        "slug": "test-codeup",
        "type": "User"
    }
}
```

