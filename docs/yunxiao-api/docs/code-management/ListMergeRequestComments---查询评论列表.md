# ListMergeRequestComments - 查询评论列表

---
source: https://help.aliyun.com/zh/yunxiao/developer-reference/listmergerequestcomments
category: code-management
downloaded_at: 2026-01-26T14:36:21.284972
---

# ListMergeRequestComments - 查询评论列表

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

| 参数              | 类型     | 是否必填 | 描述      | 示例值                          |
|-----------------|--------|------|---------|------------------------------|
| x-yunxiao-token | string | 是    | 个人访问令牌。 | pt-0fh3****0fbG_35af****0484 |

| 参数                   | 类型            | 位置   | 是否必填 | 描述                            | 示例值                                          |
|----------------------|---------------|------|------|-------------------------------|----------------------------------------------|
| organizationId       | string        | path | 是    | 组织 ID。                        | 60d54f3daccf2bbd6659f3ad                     |
| repositoryId         | string        | path | 是    | 代码库 ID 或者 URL-Encoder 编码的全路径。 | 2813489或者60de7a6852743a5162b5f957%2FDemoRepo |
| localId              | integer       | path | 是    | 局部 ID，表示代码库中第几个合并请求。          | 1                                            |
| -                    | object        | body | 否    |                               |                                              |
| comment_biz_id_list  | array[string] | body | 否    | 所需评论 ID 列表，从根评论开始返回。          |                                              |
| comment_type         | string        | body | 否    | 评论类型。                         | GLOBAL_COMMENT,INLINE_COMMENT                |
| file_path            | string        | body | 否    | 文件路径。                         | /src/main/test.java                          |
| patchset_biz_id_list | array[string] | body | 否    | 版本业务 ID 列表。                   |                                              |
| resolved             | boolean       | body |      | 是否已解决。                        | false                                        |
| state                | string        | body |      | 评论状态。                         | DRAFT,OPENED                                 |

```
curl -X 'POST' \
  'https://{domain}/oapi/v1/codeup/organizations/60d54f3daccf2bbd6659f3ad/repositories/2813489或者60de7a6852743a5162b5f957%2FDemoRepo/changeRequests/1/comments/list' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484' \
  --data '
    {
        "comment_biz_id_list": [
            
        ],
        "comment_type": "GLOBAL_COMMENT",
        "file_path": "/src/main/test.java",
        "patchset_biz_id_list": [
            
        ],
        "resolved": false,
        "state": "DRAFT"
    }'
```

| 参数                               | 类型            | 描述                                            | 示例值                                      |
|----------------------------------|---------------|-----------------------------------------------|------------------------------------------|
| -                                | array         |                                               |                                          |
| -                                | object        |                                               |                                          |
| author                           | object        | 用户信息。                                         |                                          |
| avatar                           | string        | 用户头像地址。                                       | https://example/example/w/100/h/100      |
| email                            | string        | 用户邮箱。                                         | username@example.com                     |
| name                             | string        | 用户名称。                                         | codeup-name                              |
| state                            | string        | 用户状态：active - 激活可用；blocked - 阻塞暂不可用。          | active                                   |
| userId                           | string        | 云效用户 ID。                                      | 62c795xxxb468af8                         |
| username                         | string        | 用户登录名。                                        | codeup-username                          |
| child_comments_list              | array[string] | 子评论。                                          | []                                       |
| comment_time                     | string        | 评论时间。                                         | 2023-08-21T14:30:00Z                     |
| comment_type                     | string        | 评论类型。                                         | INLINE_COMMENT                           |
| content                          | string        | 评论内容。                                         | This is a comment content.               |
| expression_reply_list            | array         | 表态回复。                                         | []                                       |
| -                                | object        |                                               |                                          |
| emoji                            | string        | emoji 表情符。                                    |                                          |
| reply_user_list                  | array         | 表态用户列表。                                       |                                          |
| -                                | object        |                                               |                                          |
| reply_biz_id                     | string        | 回复业务 ID。                                      | 1d8171cf0cc2453197fae0e0a27d5ece         |
| reply_user                       | object        | 用户信息。                                         |                                          |
| avatar                           | string        | 用户头像地址。                                       | https://example/example/w/100/h/100      |
| email                            | string        | 用户邮箱。                                         | username@example.com                     |
| name                             | string        | 用户名称。                                         | codeup-name                              |
| state                            | string        | 用户状态：active - 激活可用；blocked - 阻塞暂不可用。          | active                                   |
| userId                           | string        | 云效用户 ID。                                      | 62c795xxxb468af8                         |
| username                         | string        | 用户登录名。                                        | codeup-username                          |
| filePath                         | string        | 所在文件。                                         | /src/main/java/com/example/MyClass.java  |
| from_patchset_biz_id             | string        | from 版本 id。                                   | c341efc7fa38425eb575ad6ab6e95e76         |
| is_deleted                       | boolean       | 是否已经删除。                                       | false                                    |
| last_edit_time                   | string        | 上次编辑时间。                                       | 2023-08-21T15:00:00Z                     |
| last_edit_user                   | object        | 用户信息。                                         |                                          |
| avatar                           | string        | 用户头像地址。                                       | https://example/example/w/100/h/100      |
| email                            | string        | 用户邮箱。                                         | username@example.com                     |
| name                             | string        | 用户名称。                                         | codeup-name                              |
| state                            | string        | 用户状态：active - 激活可用；blocked - 阻塞暂不可用。          | active                                   |
| userId                           | string        | 云效用户 ID。                                      | 62c795xxxb468af8                         |
| username                         | string        | 用户登录名。                                        | codeup-username                          |
| last_resolved_status_change_time | string        | 最后解决状态更改时间。                                   | 2023-08-21T16:00:00Z                     |
| last_resolved_status_change_user | object        | 用户信息。                                         |                                          |
| avatar                           | string        | 用户头像地址。                                       | https://example/example/w/100/h/100      |
| email                            | string        | 用户邮箱。                                         | username@example.com                     |
| name                             | string        | 用户名称。                                         | codeup-name                              |
| state                            | string        | 用户状态：active - 激活可用；blocked - 阻塞暂不可用。          | active                                   |
| userId                           | string        | 云效用户 ID。                                      | 62c795xxxb468af8                         |
| username                         | string        | 用户登录名。                                        | codeup-username                          |
| line_number                      | integer       | 所在行号。                                         | 42                                       |
| location                         | object        |                                               |                                          |
| can_located                      | boolean       | 是否可以定位。                                       | true                                     |
| located_file_path                | string        | 定位的文件路径。                                      | /src/main/java/com/example/Example.java  |
| located_line_number              | integer       | 定位的行号。                                        | 100                                      |
| located_patch_set_biz_id         | string        | 定位的补丁集业务 ID。                                  | 1d8171cf0cc2453197fae0e0a27d5ece         |
| mr_biz_id                        | string        | 所属 mrBizId。                                   | bf117304dfe44d5d9b1132f348edf92e         |
| out_dated                        | boolean       | 是否过期评论。                                       | false                                    |
| parent_comment_biz_id            | string        | 父评论 bizID。                                    | 1d8171cf0cc2453197fae0e0a27d5ece         |
| project_id                       | integer       | 代码库 ID。                                       | 123456                                   |
| related_patchset                 | object        |                                               |                                          |
| commitId                         | string        | 版本对应的提交 ID。                                   | 45ede4680536406d793e0e629bc771cb9fcaa153 |
| createTime                       | string        | 版本创建时间。                                       | 2024-10-05T15:30:45Z                     |
| patchSetBizId                    | string        | 版本 ID，具有唯一性。                                  | bf117304dfe44d5d9b1132f348edf92e         |
| patchSetName                     | string        | 版本名称。                                         | 版本1                                      |
| ref                              | string        | 版本对应的 ref 信息。                                 | null                                     |
| relatedMergeItemType             | string        | 关联的类型：MERGE_SOURCE - 合并源；MERGE_TARGET - 合并目标。 | MERGE_SOURCE                             |
| shortId                          | string        | 提交 ID 对应的短 ID，通常为8位。                          | 45ede468                                 |
| versionNo                        | integer       | 版本号。                                          | 1                                        |
| resolved                         | boolean       | 是否已解决。                                        | false                                    |
| root_comment_biz_id              | string        | 根评论 bizId。                                    | 1d8171cf0cc2453197fae0e0a27d5ece         |
| state                            | string        | 评论状态。                                         | OPENED,DRAFT                             |
| to_patchset_biz_id               | string        | to 版本 id。                                     | c341efc7fa38425eb575ad6ab6e95e76         |

```
[
    {
        "author": {
            "avatar": "https://example/example/w/100/h/100",
            "email": "username@example.com",
            "name": "codeup-name",
            "state": "active",
            "userId": "62c795xxxb468af8",
            "username": "codeup-username"
        },
        "child_comments_list": [],
        "comment_biz_id": "bf117304dfe44d5d9b1132f348edf92e",
        "comment_time": "2023-08-21T14:30:00Z",
        "comment_type": "INLINE_COMMENT",
        "content": "This is a comment content.",
        "expression_reply_list": [],
        "filePath": "/src/main/java/com/example/MyClass.java",
        "from_patchset_biz_id": "c341efc7fa38425eb575ad6ab6e95e76",
        "is_deleted": false,
        "last_edit_time": "2023-08-21T15:00:00Z",
        "last_edit_user": {
            "avatar": "https://example/example/w/100/h/100",
            "email": "username@example.com",
            "name": "codeup-name",
            "state": "active",
            "userId": "62c795xxxb468af8",
            "username": "codeup-username"
        },
        "last_resolved_status_change_time": "2023-08-21T16:00:00Z",
        "last_resolved_status_change_user": {
            "avatar": "https://example/example/w/100/h/100",
            "email": "username@example.com",
            "name": "codeup-name",
            "state": "active",
            "userId": "62c795xxxb468af8",
            "username": "codeup-username"
        },
        "line_number": 42,
        "location": {
            "can_located": true,
            "located_file_path": "/src/main/java/com/example/Example.java",
            "located_line_number": 100,
            "located_patch_set_biz_id": "1d8171cf0cc2453197fae0e0a27d5ece"
        },
        "mr_biz_id": "bf117304dfe44d5d9b1132f348edf92e",
        "out_dated": false,
        "parent_comment_biz_id": "1d8171cf0cc2453197fae0e0a27d5ece",
        "project_id": 123456,
        "related_patchset": {
            "commitId": "45ede4680536406d793e0e629bc771cb9fcaa153",
            "createTime": "2024-10-05T15:30:45Z",
            "patchSetBizId": "bf117304dfe44d5d9b1132f348edf92e",
            "patchSetName": "版本1",
            "ref": "null",
            "relatedMergeItemType": "MERGE_SOURCE",
            "shortId": "45ede468",
            "versionNo": 1
        },
        "resolved": false,
        "root_comment_biz_id": "1d8171cf0cc2453197fae0e0a27d5ece",
        "state": "OPENED,DRAFT",
        "to_patchset_biz_id": "c341efc7fa38425eb575ad6ab6e95e76"
    }
]
```

访问错误码中心查看 API 相关错误码。

