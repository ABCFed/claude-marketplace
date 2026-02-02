# 测试用例

本文档包含 jenkins-deploy 技能的完整测试用例。

## 重要参数说明

**featureNo / envNo 参数规则**：
- 有效值：1-100 的数字
- 当项目有这些参数时为必填
- 不仅限于 FeatureTest 后缀项目，Own、Module 等后缀也可能有
- 以实际查询到的项目参数为准

---

## FeatureTest 项目测试用例

### PcFeatureTest

| 用例 | 命令 | 预期结果 |
|------|------|----------|
| 正确参数 | `--validate --params '{"repoTag":"pc-t2025.53.19","featureNo":"70"}'` | ✓ 通过 |
| 缺少 featureNo | `--validate --params '{"repoTag":"pc-t2025.53.19"}'` | ✗ 失败 |
| featureNo=101 | `--validate --params '{"repoTag":"pc-t2025.53.19","featureNo":"101"}'` | ✗ 超出范围 |
| featureNo=0 | `--validate --params '{"repoTag":"pc-t2025.53.19","featureNo":"0"}'` | ✗ 超出范围 |
| featureNo=abc | `--validate --params '{"repoTag":"pc-t2025.53.19","featureNo":"abc"}'` | ✗ 非数字 |
| 模拟运行 | `--dry-run --params '{"repoTag":"pc-t2025.53.19","featureNo":"70"}'` | 显示 JSON |

### socialPcModuleFeatureTest

| 用例 | 命令 | 预期结果 |
|------|------|----------|
| 正确参数 | `--validate --params '{"repoTag":"social-t2025.53.19","envNo":"1"}'` | ✓ 通过 |
| 缺少 envNo | `--validate --params '{"repoTag":"social-t2025.53.19"}'` | ✗ 失败 |
| envNo=0 | `--validate --params '{"repoTag":"social-t2025.53.19","envNo":"0"}'` | ✗ 超出范围 |
| envNo=100 | `--validate --params '{"repoTag":"social-t2025.53.19","envNo":"100"}'` | ✓ 边界值通过 |
| 模拟运行 | `--dry-run --params '{"repoTag":"social-t2025.53.19","envNo":"1"}'` | 显示 JSON |

### staticPrintFeatureTest

| 用例 | 命令 | 预期结果 |
|------|------|----------|
| 正确参数 | `--validate --params '{"repoTag":"print-t2025.53.19","envNo":"50"}'` | ✓ 通过 |
| 缺少 envNo | `--validate --params '{"repoTag":"print-t2025.53.19"}'` | ✗ 失败 |
| 模拟运行 | `--dry-run --params '{"repoTag":"print-t2025.53.19","envNo":"50"}'` | 显示 JSON |

---

## 开发环境项目测试用例

### staticPcOwn

| 用例 | 命令 | 预期结果 |
|------|------|----------|
| 正确参数 | `--validate --params '{"repoBranch":"hotfix/xxx-1167459320001118371","featureNo":"50"}'` | ✓ 通过 |
| 缺少 featureNo | `--validate --params '{"repoBranch":"hotfix/xxx-1167459320001118371"}'` | ✗ 失败 |
| featureNo 超出范围 | `--validate --params '{"repoBranch":"hotfix/xxx","featureNo":"101"}'` | ✗ 超出范围 |
| 模拟运行 | `--dry-run --params '{"repoBranch":"hotfix/xxx-1167459320001118371","featureNo":"50"}'` | 显示 JSON |

---

## 微前端项目测试用例

### static-mf-order-cloud

| 用例 | 命令 | 预期结果 |
|------|------|----------|
| 正确参数 | `--validate --params '{"repoBranch":"develop"}'` | ✓ 通过 |
| 缺少 repoBranch | `--validate --params '{}'` | ✗ 失败 |
| 模拟运行 | `--dry-run --params '{"repoBranch":"develop","deployZone":"primary"}'` | 显示 JSON |

### static-mf-deepseek

| 用例 | 命令 | 预期结果 |
|------|------|----------|
| 正确参数 | `--validate --params '{"repoTag":"pc-f2026.05.48"}'` | ✓ 通过 |
| 缺少 repoTag | `--validate --params '{}'` | ✗ 失败 |
| 模拟运行 | `--dry-run --params '{"repoTag":"pc-f2026.05.48"}'` | 显示 JSON |

---

## 基础功能测试

| 检查项 | 命令 | 预期结果 |
|--------|------|----------|
| 项目列表 | `--list` | 显示相关项目 |
| 全部项目 | `--list --all` | 显示所有项目 |
| 停止构建 | `--stop <build_number>` | 成功停止 |
| 缓存刷新 | `--list --refresh` | 缓存时间更新 |

---

## 运行测试

### 快速测试（不触发构建）

```bash
# 1. 验证参数
python scripts/jenkins_deploy.py \
  PcFeatureTest \
  --validate \
  --params '{"repoTag":"pc-t2025.53.19","featureNo":"70"}'

# 2. 模拟运行
python scripts/jenkins_deploy.py \
  PcFeatureTest \
  --dry-run \
  --params '{"repoTag":"pc-t2025.53.19","featureNo":"70"}'
```

### 完整测试（触发构建）

```bash
# 1. 触发构建
python scripts/jenkins_deploy.py \
  PcFeatureTest \
  --trigger-only-no-monitor \
  --yes \
  --params '{"repoTag":"pc-t2025.53.19","featureNo":"70"}'

# 2. 启动监控（使用返回的 queue_id）
python scripts/jenkins_deploy.py \
  --monitor-only \
  --full-name abc-his/test/PcFeatureTest \
  --queue-id <queue_id> \
  --display-name PcFeatureTest
```
