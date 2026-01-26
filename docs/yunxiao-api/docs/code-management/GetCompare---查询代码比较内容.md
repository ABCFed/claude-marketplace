# GetCompare - 查询代码比较内容

---
source: https://help.aliyun.com/zh/yunxiao/developer-reference/getcompare
category: code-management
downloaded_at: 2026-01-26T14:36:24.875505
---

# GetCompare - 查询代码比较内容

## 服务接入点与授权信息

获取服务接入点，替换 API 请求语法中的 <domain> ：服务接入点（domain）。

获取个人访问令牌，具体操作，请参见获取个人访问令牌。

获取organizationId，请前往组织管理后台的基本信息页面获取组织 ID 。

- 获取服务接入点，替换 API 请求语法中的 <domain> ：服务接入点（domain）。
- 获取个人访问令牌，具体操作，请参见获取个人访问令牌。
- 获取organizationId，请前往组织管理后台的基本信息页面获取组织 ID 。

| 产品   | 资源   | 所需权限 |
|------|------|------|
| 代码管理 | 代码比较 | 只读   |

## 请求语法

```
GET https://{domain}/oapi/v1/codeup/organizations/{organizationId}/repositories/{repositoryId}/compares
```

## 请求头

| 参数              | 类型     | 是否必填 | 描述      | 示例值                          |
|-----------------|--------|------|---------|------------------------------|
| x-yunxiao-token | string | 是    | 个人访问令牌。 | pt-0fh3****0fbG_35af****0484 |

## 请求参数

| 参数             | 类型     | 位置    | 是否必填 | 描述                                                                                                                                     | 示例值                                      |
|----------------|--------|-------|------|----------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------|
| organizationId | string | path  | 是    | 组织 ID。                                                                                                                                 | 5ebbc0228123212b59xxxxx                  |
| repositoryId   | string | path  | 是    | 代码库 ID 或者 URL-Encoder 编码的全路径。                                                                                                          | 2369234                                  |
| from           | string | query | 是    | 可为 CommitSHA、分支名或者标签名。                                                                                                                 | c9fb781f3d66ef6ee60bdd5c414f5106454b1426 |
| to             | string | query | 是    | 可为 CommitSHA、分支名或者标签名。                                                                                                                 | b8f6f28520b1936aafe2e638373e19ccafa42b02 |
| sourceType     | string | query | 否    | 可选值：branch、tag；若是 commit 比较，可不传；若是分支比较，则需传入：branch，亦可不传，但需要确保不存在分支或 tag 重名的情况；若是 tag 比较，则需传入：tag；若是存在分支和标签同名的情况，则需要严格传入 branch 或者 tag。 | branch                                   |
| targetType     | string | query | 否    | 可选值：branch、tag；若是 commit 比较，可不传；若是分支比较，则需传入：branch，亦可不传，但需要确保不存在分支或 Tag 重名的情况；若是 tag 比较，则需传入：tag；若是存在分支和标签同名的情况，则需要严格传入 branch 或者 tag。 | branch                                   |
| straight       | string | query | 否    | 是否使用 Merge-Base：straight=false，表示使用 Merge-Base；straight=true，表示不使用 Merge-Base；默认为 false，即使用 Merge-Base。                                | false                                    |

## 请求示例

```
curl -X 'GET' \
  'https://test.rdc.aliyuncs.com/oapi/v1/codeup/organizations/{organizationId}/repositories/{repositoryId}/compares?from=<from>&to=<to>&sourceType=<sourceType>&targetType=<targetType>&straight=<straight>' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'
```

## 返回参数

| 参数             | 类型            | 描述                     | 示例值                                                                            |
|----------------|---------------|------------------------|--------------------------------------------------------------------------------|
| -              | object        |                        |                                                                                |
| commits        | array         | 差异提交列表。                |                                                                                |
| -              | object        |                        |                                                                                |
| authorEmail    | string        | 作者邮箱。                  | username@example.com                                                           |
| authorName     | string        | 作者姓名。                  | codeup-name                                                                    |
| authoredDate   | string        | 作者提交时间。                | 2024-10-05T15:30:45Z                                                           |
| committedDate  | string        | 提交者提交时间。               | 2024-10-05T15:30:45Z                                                           |
| committerEmail | string        | 提交者邮箱。                 | username@example.com                                                           |
| committerName  | string        | 提交者姓名。                 | codeup-name                                                                    |
| id             | string        | 提交 ID。                 | 6da8c14b5a9102998148b7ea35f96507d5304f74                                       |
| message        | string        | 提交内容。                  | commit message detail                                                          |
| parentIds      | array[string] | 父提交 ID。                | [“3fdaf119cf76539c1a47de0074ac02927ef4c8e1”]                                   |
| shortId        | string        | 提交短 ID。                | 6da8c14b                                                                       |
| stats          | object        | 变更行数。                  |                                                                                |
| additions      | integer       | 增加行数。                  | 1                                                                              |
| deletions      | integer       | 删除行数。                  | 1                                                                              |
| total          | integer       | 总变动行数。                 | 2                                                                              |
| title          | string        | 标题，提交的第一行内容。           | commit msg title                                                               |
| webUrl         | string        | 页面访问地址。                | http://exmaple.com/example_repo/commit/commit_sha                              |
| diffs          | array         | 差异内容。                  |                                                                                |
| -              | object        |                        |                                                                                |
| aMode          | string        | 旧文件的模式标识，包含文件类型、权限等信息。 | 0                                                                              |
| bMode          | string        | 新文件的模式标识，包含文件类型、权限等信息。 | 100644                                                                         |
| deletedFile    | boolean       | 是否是删除文件。               | false                                                                          |
| diff           | string        | 比较内容。                  | — /dev/null\n+++ b/asda\n@@ -0,0 +1 @@\n+asdasd\n\ No newline at end of file\n |
| isBinary       | boolean       | 是否是二进制文件。              | false                                                                          |
| newFile        | boolean       | 是否是新增文件。               | true                                                                           |
| newId          | string        | 新文件的 git object id。    | 911***********660d7b                                                           |
| newPath        | string        | 新文件路径。                 | src/test/main.java                                                             |
| oldId          | string        | 旧文件的 git object id。    | 8a9***********fdd82a2c1                                                        |
| oldPath        | string        | 旧文件路径。                 | src/test/main.java                                                             |
| renamedFile    | boolean       | 是否是重命名文件。              | false                                                                          |

## 返回示例

```
{
    "commits": [
        {
            "authorEmail": "username@example.com",
            "authorName": "云效Codeup",
            "authoredDate": "2023-01-03T15:41:26+08:00",
            "committedDate": "2023-01-03T15:41:26+08:00",
            "committerEmail": "username@example.com",
            "committerName": "云效CodeupCommitter",
            "id": "b8f6f28520b1936aafe2e638373e19ccafa42b02",
            "message": "",
            "parentIds": [
                "b8f6f"
            ],
            "shortId": "b8f6f285",
            "stats": {
                "additions": 0,
                "deletions": 0,
                "total": 0
            },
            "title": "提交标题",
            "webUrl": ""
        }
    ],
    "diffs": [
        {
            "aMode": "0",
            "bMode": "100644",
            "deletedFile": false,
            "diff": "--- /dev/null\n+++ b/asda\n@@ -0,0 +1 @@\n+asdasd\n\\ No newline at end of file\n",
            "isBinary": false,
            "newFile": true,
            "newId": "9118d6c90d********4a50ff660d7b",
            "newPath": "new_test.txt",
            "oldId": "8a9***********fdd82a2c1",
            "oldPath": "test.txt",
            "renamedFile": false
        }
    ]
}
```

## 错误码

访问错误码中心查看 API 相关错误码。

