# 后端 Git 分支管理补充

> 后端项目有特殊的**联合分支**机制。本文档仅描述后端特有部分。如果安装了 `abc-git-flow` SKILL，可参考其中的通用 git-flow 流程。

## 为什么后端需要联合分支？

```
前端：每个 feature 分支可以独立部署到自己的泳道环境，互不影响
后端：只有一套 dev 环境和一套 test 环境，多个 feature 必须合到一起才能部署
```

**核心问题**：后端没有泳道，多个需求要同时在 dev/test 环境验证时，需要一个"集合点"把各个 feature 分支汇聚到一起。

这就是 `dev-join/dev-joint` 和 `test-join/test-joint` 的作用。

## 联合分支概览

| 联合分支 | 对应环境 | 发布方式 | 用途 |
|---------|---------|---------|------|
| `dev-join` / `dev-joint` | dev 开发环境 | 直接构建发布 | 多个 feature 合并后部署到 dev 环境联调 |
| `test-join` / `test-joint` | test 测试环境 | 打 tag 后发布 | 多个 feature 合并后部署到 test 环境测试 |

> `dev-join` 和 `dev-joint` 是同一个概念，不同项目可能用不同的名字，以实际项目为准。`test-join` / `test-joint` 同理。

## 开发环境发布流程（dev-join）

```
feature/A ──┐
feature/B ──┼──→ dev-join ──→ 直接构建发布到 dev 环境
feature/C ──┘
```

### 操作步骤

```bash
# 1. 切换到 dev-join 分支并拉取最新
git checkout dev-join
git pull origin dev-join

# 2. 将你的 feature 分支合并进来
git merge feature/your-feature-name

# 3. 解决冲突（如有），然后推送
git push origin dev-join

# 4. 推送后，通过 CI/CD 手动触发构建发布到 dev 环境
```

**要点**：
- dev 环境是**直接用 dev-join 分支构建**，不需要打 tag
- 推送后需要手动触发 CI/CD 构建发布
- 如果 dev-join 分支太"脏"了（积累了太多已完成/废弃的 feature），需要**人工手动**基于 develop 重建

## 测试环境发布流程（test-join）

```
feature/A ──┐
feature/B ──┼──→ test-join ──→ 打 tag ──→ 发布到 test 环境
feature/C ──┘
```

### 操作步骤

```bash
# 1. 切换到 test-join 分支并拉取最新
git checkout test-joint
git pull origin test-joint

# 2. 将你的 feature 分支合并进来
git merge feature/your-feature-name

# 3. 解决冲突（如有），然后推送
git push origin test-joint

# 4. 在 test-joint 分支上打 tag 触发发布
git abc tag create   # 选择 "测试环境(t)"
```

**要点**：
- test 环境**必须打 tag 才能发布**，不像 dev 环境推送即发布
- tag 命名遵循 `abc-git-flow` 的 t-tag 规范
- 打 tag 前确保所有需要的 feature 都已合并进来

## 前端 vs 后端发布流程对比

```
前端（有泳道）:
  feature/A → 独立泳道A → 独立验证 → develop → rc → gray → master

后端（无泳道）:
  feature/A ──┐
  feature/B ──┼→ dev-join → test-join(打tag) → develop → rc → gray → master
  feature/C ──┘
```

| 阶段 | 前端 | 后端 |
|------|------|------|
| 开发联调 | 泳道环境，独立部署 | 合并到 `dev-join`，共享 dev 环境 |
| 提测 | feature 分支打 f-tag | 合并到 `test-join`，打 t-tag |
| 预发布及之后 | develop → rc → gray → master | 同前端，走标准 abc-git-flow |

## 注意事项

1. **联合分支是临时集合点，不是长期分支**：不要在 dev-join/test-join 上直接开发，只用来合并 feature
2. **不要 rebase 联合分支**：联合分支是多人共用的，禁止 rebase
3. **定期清理**：联合分支积累太多废弃代码时，需要**人工手动**基于 develop 重建
4. **先确认再合并**：合并前在群里知会一声，避免覆盖别人正在验证的内容
5. **feature 分支才是你的"主阵地"**：所有开发工作在 feature 分支完成，联合分支只是发布的中转站
