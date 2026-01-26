# ListCommits - 查询提交列表

---
source: https://help.aliyun.com/zh/yunxiao/developer-reference/listcommits-query-the-submission-list
category: code-management
downloaded_at: 2026-01-26T14:33:54.901365
---

# ListCommits - 查询提交列表

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

	

提交

	

只读

| 产品   | 资源  | 所需权限 |
|------|-----|------|
| 代码管理 | 提交  | 只读   |

## 请求语法

```
GET https://{domain}/oapi/v1/codeup/organizations/{organizationId}/repositories/{repositoryId}/commits
```

## 请求头

| 参数              | 类型     | 是否必填 | 描述      | 示例值                          |
|-----------------|--------|------|---------|------------------------------|
| x-yunxiao-token | string | 是    | 个人访问令牌。 | pt-0fh3****0fbG_35af****0484 |

## 请求参数

| 参数             | 类型      | 位置    | 是否必填 | 描述                              | 示例值                      |
|----------------|---------|-------|------|---------------------------------|--------------------------|
| organizationId | string  | path  | 是    | 组织 ID。                          | 99d1****71d4             |
| repositoryId   | string  | path  | 是    | 代码库 ID 或者 URL-Encoder 编码的全路径。   | 2825387                  |
| refName        | string  | query | 是    | 分支名称、标签名称或提交版本，默认为代码库默认分支。      | master 或 tag1.0或 sjjfssa |
| since          | string  | query | 否    | 提交起始时间，格式：YYYY-MM-DDTHH:MM:SSZ。 | 2022-08-08 18:09:09      |
| until          | string  | query | 否    | 提交截止时间，格式：YYYY-MM-DDTHH:MM:SSZ。 | 2022-03-18 14:24:54      |
| page           | integer | query | 否    | 页码。                             | 1                        |
| perPage        | integer | query | 否    | 每页大小。                           | 20                       |
| path           | string  | query | 否    | 文件路径。                           | src/cpp/main.cpp         |
| search         | string  | query | 否    | 搜索关键字。                          | search                   |
| showSignature  | boolean | query | 否    | 是否展示签名。                         | false                    |
| committerIds   | string  | query | 否    | 提交人 ID 列表（多个 ID 以逗号隔开）。         | false                    |

## 请求示例

```
curl -X 'GET' \
  'https://test.rdc.aliyuncs.com/oapi/v1/codeup/organizations/{organizationId}/repositories/{repositoryId}/commits?refName=<refName>&since=<since>&until=<until>&page=<page>&perPage=<perPage>&path=<path>&search=<search>&showSignature=<showSignature>&committerIds=<committerIds>' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'
```

## 返回参数

| 参数             | 类型            | 描述           | 示例值                                      |
|----------------|---------------|--------------|------------------------------------------|
| -              | array         |              |                                          |
| -              | object        |              |                                          |
| authorEmail    | string        | 作者邮箱。        | username@example.com                     |
| authorName     | string        | 作者姓名。        | test-codeup                              |
| authoredDate   | string        | 作者提交时间。      | 2022-03-18 15:00:00                      |
| committedDate  | string        | 提交者提交时间。     | 2022-03-18 16:00:00                      |
| committerEmail | string        | 提交者邮箱。       | username@example.com                     |
| committerName  | string        | 提交者姓名。       | committer-codeup                         |
| id             | string        | 提交 ID。       | de02b625ba8488f92eb204bcb3773a40c1b4ddac |
| message        | string        | 提交内容。        | 提交的具体内容                                  |
| parentIds      | array[string] | 父提交 ID。      |                                          |
| shortId        | string        | 代码组路径。       | de02b625                                 |
| title          | string        | 标题，提交的第一行内容。 | 提交标题                                     |
| webUrl         | string        | 页面访问地址。      | ""                                       |

## 返回示例

```
[
    {
        "authorEmail": "username@example.com",
        "authorName": "test-codeup",
        "authoredDate": "2022-03-18 15:00:00",
        "committedDate": "2022-03-18 16:00:00",
        "committerEmail": "username@example.com",
        "committerName": "committer-codeup",
        "id": "de02b625ba8488f92eb204bcb3773a40c1b4ddac",
        "message": "提交的具体内容",
        "parentIds": [
            
        ],
        "shortId": "de02b625",
        "title": "提交标题",
        "webUrl": "\"\""
    }
]
```

## 响应头

| 参数            | 描述     | 示例值                                  |
|---------------|--------|--------------------------------------|
| x-next-page   | 下一页。   | 2                                    |
| x-page        | 当前页。   | 1                                    |
| x-per-page    | 每页大小。  | 20                                   |
| x-prev-page   | 前一页。   | 0                                    |
| x-request-id  | 请求 ID。 | F7B85D1B-D1C2-140F-A039-341859F130B9 |
| x-total       | 总数。    | 10                                   |
| x-total-pages | 总分页数。  | 1                                    |

## 错误码

访问错误码中心查看 API 相关错误码。

