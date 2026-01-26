# GetChangeRequestTree - 查询合并请求的变更文件树

---
source: https://help.aliyun.com/zh/yunxiao/developer-reference/getchangerequesttree-queries-the-change-file-tree-for-merge-requests
category: code-management
downloaded_at: 2026-01-26T14:35:37.153471
---

# GetChangeRequestTree - 查询合并请求的变更文件树

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
GET https://{domain}/oapi/v1/codeup/organizations/{organizationId}/repositories/{repositoryId}/changeRequests/{localId}/diffs/changeTree
```

## 请求头

| 参数              | 类型     | 是否必填 | 描述      | 示例值                          |
|-----------------|--------|------|---------|------------------------------|
| x-yunxiao-token | string | 是    | 个人访问令牌。 | pt-0fh3****0fbG_35af****0484 |

## 请求参数

| 参数             | 类型      | 位置    | 是否必填 | 描述                                                       | 示例值                                   |
|----------------|---------|-------|------|----------------------------------------------------------|---------------------------------------|
| organizationId | string  | path  | 是    | 组织 ID。                                                   | 6270e731cfea268afc21ccac              |
| repositoryId   | string  | path  | 是    | 代码库 ID 或者 URL-Encoder 编码的全路径。                            | 2835387 或 codeup-org-id%2Fcodeup-demo |
| localId        | integer | path  | 是    | 局部 ID。                                                   | 1                                     |
| fromPatchSetId | string  | query | 是    | 合并目标对应的版本唯一 ID（from 和 to，是 Git 的对比顺序，与通常的源分支和目标分支的顺序相反）。 | 5e733xxxxxxxxb04a6aa0e23d4ff72b8      |
| toPatchSetId   | string  | query | 是    | 合并源对应的版本唯一 ID（from 和 to，是 Git 的对比顺序，与通常的源分支和目标分支的顺序相反）。  | 513fcxxxxxxxx2d2bb0db4f72c0aa15b      |

## 请求示例

```
curl -X 'GET' \
  'https://test.rdc.aliyuncs.com/oapi/v1/codeup/organizations/{organizationId}/repositories/{repositoryId}/changeRequests/{localId}/diffs/changeTree?fromPatchSetId=<fromPatchSetId>&toPatchSetId=<toPatchSetId>' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'
```

## 返回参数

| 参数               | 类型      | 描述                 | 示例值      |
|------------------|---------|--------------------|----------|
| -                | object  |                    |          |
| changedTreeItems | array   | 变更文件列表。            |          |
| -                | object  |                    |          |
| addLines         | integer | 新增行数。              | 10       |
| delLines         | integer | 删除行数。              | 0        |
| deletedFile      | boolean | 是否是删除文件。           | false    |
| isBinary         | boolean | 是否是二进制文件。          | false    |
| newFile          | boolean | 是否是新建文件。           | true     |
| newObjectId      | string  | 新文件 git object id。 |          |
| newPath          | string  | 新文件路径。             | test.txt |
| oldObjectId      | string  | 旧文件 git object id。 |          |
| oldPath          | string  | 旧文件路径。             | test.txt |
| renamedFile      | boolean | 是否是重命名文件。          | false    |
| count            | integer | 总变更文件数。            | 20       |
| totalAddLines    | integer | 总增加行数。             | 100      |
| totalDelLines    | integer | 总删除行数。             | 50       |

## 返回示例

```
{
    "changedTreeItems": [
        {
            "addLines": 10,
            "delLines": 0,
            "deletedFile": false,
            "isBinary": false,
            "newFile": false,
            "newObjectId": "",
            "newPath": "test.txt",
            "oldObjectId": "",
            "oldPath": "test.txt",
            "renamedFile": false
        }
    ],
    "count": 20,
    "totalAddLines": 100,
    "totalDelLines": 50
}
```

## 错误码

访问错误码中心查看 API 相关错误码。

