# 常见项目参数参考

本文档包含常见 Jenkins 项目的完整参数列表。

**参数类型说明**：
- **只读**：自动填充，不可修改
- **字符串**：需用户输入
- **下拉选择**：从选项中选择
- **复选框**：可多选

**featureNo / envNo 规则**：
- 有效值：1-100 的数字
- 当项目有这些参数时为必填
- 以实际查询到的参数为准

---

## 测试环境项目

### PcFeatureTest

**用途**：PC 项目测试环境发布（使用标签）

| 参数 | 类型 | 默认值 | 必填 | 说明 |
|------|------|--------|------|------|
| `repoUrl` | 只读 | `git@codeup.aliyun.com:abcyun/AbcPc/AbcPc.git` | - | Git 仓库地址 |
| `dockerName` | 只读 | `abc-cis-static-pc-service` | - | Docker 镜像名称 |
| `nodeName` | 只读 | `master` | - | 构建节点 |
| `buildEnv` | 只读 | `test` | - | 构建环境 |
| `repoTag` | 字符串 | (空) | ✓ | 发布标签（如 `pc-t2025.53.19`） |
| `featureNo` | 字符串 | (空) | ✓ | 功能编号（1-100） |

**发布示例**：
```bash
python scripts/jenkins_deploy.py \
  PcFeatureTest \
  --trigger-only-no-monitor \
  --yes \
  --params '{"repoTag":"pc-t2025.53.19","featureNo":"70"}'
```

### socialPcModuleFeatureTest

**用途**：社保模块测试环境发布

| 参数 | 类型 | 默认值 | 必填 | 说明 |
|------|------|--------|------|------|
| `repoUrl` | 只读 | `git@codeup.aliyun.com:abcyun/SocialSecurityLite/...` | - | Git 仓库地址 |
| `nodeName` | 只读 | `master` | - | 构建节点 |
| `buildEnv` | 只读 | `test` | - | 构建环境 |
| `moduleName` | 只读 | `social` | - | 模块名称 |
| `repoTag` | 字符串 | (空) | ✓ | 发布标签 |
| `envNo` | 字符串 | (空) | ✓ | 环境编号（1-100） |
| `ossType` | 下拉选择 | `ali` | - | OSS 类型 |
| `execType` | 下拉选择 | (空) | - | 执行类型 |

**发布示例**：
```bash
python scripts/jenkins_deploy.py \
  socialPcModuleFeatureTest \
  --trigger-only-no-monitor \
  --yes \
  --params '{"repoTag":"social-t2025.53.19","envNo":"1"}'
```

### staticPrintFeatureTest

**用途**：打印服务测试环境发布

| 参数 | 类型 | 默认值 | 必填 | 说明 |
|------|------|--------|------|------|
| `repoUrl` | 只读 | `git@codeup.aliyun.com:abcyun/abc-fed-common/abc-print.git` | - | Git 仓库地址 |
| `nodeName` | 只读 | `master` | - | 构建节点 |
| `buildEnv` | 只读 | `test` | - | 构建环境 |
| `repoTag` | 字符串 | (空) | ✓ | 发布标签 |
| `envNo` | 字符串 | (空) | ✓ | 环境编号（1-100） |
| `ossType` | 下拉选择 | `ali` | - | OSS 类型 |

**发布示例**：
```bash
python scripts/jenkins_deploy.py \
  staticPrintFeatureTest \
  --trigger-only-no-monitor \
  --yes \
  --params '{"repoTag":"print-t2025.53.19","envNo":"50"}'
```

### static-mf-deepseek

**用途**：DeepSeek 微前端测试环境发布

| 参数 | 类型 | 默认值 | 必填 | 说明 |
|------|------|--------|------|------|
| `repoUrl` | 只读 | `git@codeup.aliyun.com:abcyun/AbcPc/AbcPc.git` | - | Git 仓库地址 |
| `nodeName` | 只读 | `master` | - | 构建节点 |
| `buildEnv` | 只读 | `test` | - | 构建环境 |
| `projectRootDir` | 字符串 | `packages/mf-deepseek` | - | 项目子目录 |
| `repoTag` | 字符串 | (空) | ✓ | 发布标签 |

**发布示例**：
```bash
python scripts/jenkins_deploy.py \
  static-mf-deepseek \
  --trigger-only-no-monitor \
  --yes \
  --params '{"repoTag":"pc-f2026.05.48"}'
```

---

## 开发环境项目

### staticPcOwn

**用途**：PC 项目开发环境发布（使用分支）

| 参数 | 类型 | 默认值 | 必填 | 说明 |
|------|------|--------|------|------|
| `repoUrl` | 只读 | `git@codeup.aliyun.com:abcyun/AbcPc/AbcPc.git` | - | Git 仓库地址 |
| `dockerName` | 只读 | `abc-cis-static-pc-service` | - | Docker 镜像名称 |
| `nodeName` | 只读 | `master` | - | 构建节点 |
| `buildEnv` | 只读 | `dev` | - | 构建环境 |
| `dockerTag` | 字符串 | `latest` | - | Docker 镜像标签 |
| `repoBranch` | 字符串 | 当前分支 | ✓ | 发布分支 |
| `featureNo` | 字符串 | (空) | ✓ | 功能编号（1-100） |

**发布示例**：
```bash
python scripts/jenkins_deploy.py \
  staticPcOwn \
  --trigger-only-no-monitor \
  --yes \
  --params '{"repoBranch":"hotfix/xxx-1167459320001118371","featureNo":"50"}'
```

### static-mf-order-cloud

**用途**：订单云微前端开发环境发布

| 参数 | 类型 | 默认值 | 必填 | 说明 |
|------|------|--------|------|------|
| `repoUrl` | 只读 | `git@codeup.aliyun.com:abcyun/AbcPc/AbcPc.git` | - | Git 仓库地址 |
| `nodeName` | 只读 | `master` | - | 构建节点 |
| `buildEnv` | 只读 | `dev` | - | 构建环境 |
| `projectRootDir` | 字符串 | `packages/mf-order-cloud` | - | 项目子目录 |
| `dockerTag` | 字符串 | `latest` | - | Docker 镜像标签 |
| `deployZone` | 复选框 | `primary` | ✓ | 部署区域（primary/standby） |
| `repoBranch` | 字符串 | 当前分支 | ✓ | 发布分支 |

**发布示例**：
```bash
python scripts/jenkins_deploy.py \
  static-mf-order-cloud \
  --trigger-only-no-monitor \
  --yes \
  --params '{"repoBranch":"develop","deployZone":"primary"}'
```

---

## 查询项目参数

使用以下命令查询任意项目的完整参数定义：

```bash
# 验证模式查看参数
python scripts/jenkins_deploy.py \
  <项目名称> \
  --validate \
  --params '{}'

# 模拟运行查看参数详情
python scripts/jenkins_deploy.py \
  <项目名称> \
  --dry-run \
  --params '{}'
```
