# CreateProjectLabel - 创建项目类标

---
source: https://help.aliyun.com/zh/yunxiao/developer-reference/createprojectlabel
category: code-management
downloaded_at: 2026-01-26T14:57:43.981359
---

# CreateProjectLabel - 创建项目类标

禁用部署密钥。

## 适用版本

标准版

## 服务接入点与授权信息

获取服务接入点，替换 API 请求语法中的 <domain> ：服务接入点（domain）。

获取个人访问令牌，具体操作，请参见获取个人访问令牌。

获取 organizationId，请前往组织管理后台的基本信息页面获取组织 ID 。

| 产品   | 资源   | 所需权限 |
|------|------|------|
| 代码管理 | 部署密钥 | 读写   |

## 请求语法

```
POST https://{domain}/oapi/v1/codeup/organizations/{organizationId}/repositories/{repositoryId}/keys/{keyId}/disable
```

## 请求头

| 参数              | 类型     | 是否必填 | 描述      | 示例值                          |
|-----------------|--------|------|---------|------------------------------|
| x-yunxiao-token | string | 是    | 个人访问令牌。 | pt-0fh3****0fbG_35af****0484 |

## 请求参数

| 参数             | 类型     | 位置   | 是否必填 | 描述                            | 示例值                                          |
|----------------|--------|------|------|-------------------------------|----------------------------------------------|
| organizationId | string | path | 是    | 组织 ID。                        | 60d54f3daccf2bbd6659f3ad                     |
| repositoryId   | string | path | 是    | 代码库 ID 或者 URL-Encoder 编码的全路径。 | 2813489或者60de7a6852743a5162b5f957%2FDemoRepo |
| keyId          | number | path | 是    | 部署密钥 Id。                      | 2813489                                      |

## 请求示例

```curl
curl -X 'POST' \
  'https://test.rdc.aliyuncs.com/oapi/v1/codeup/organizations/60d54f3daccf2bbd6659f3ad/repositories/2813489或者60de7a6852743a5162b5f957%2FDemoRepo/keys/2813489/disable' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'
```

## 返回参数

| 参数          | 类型      | 描述       | 示例值                  |
|-------------|---------|----------|----------------------|
| -           | object  |          |                      |
| createdAt   | string  | 创建时间。    | 2024-10-05T15:30:45Z |
| fingerPrint | string  | 部署密钥指纹。  | xxx                  |
| id          | integer | 部署密钥 ID。 | 1                    |
| key         | string  | 部署密钥。    | xxx                  |
| title       | string  | 部署密钥标题。  | username@example     |

## 返回示例

```json
{
    "createdAt": "2024-10-05T15:30:45Z",
    "fingerPrint": "xxx",
    "id": 1,
    "key": "xxx",
    "title": "username@example"
}
```

## 错误码

访问错误码中心查看 API 相关错误码。
