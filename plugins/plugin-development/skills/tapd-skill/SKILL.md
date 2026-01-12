---
name: tapd-skill
description: TAPD 敏捷研发管理平台集成。使用脚本调用 TAPD API，实现需求、缺陷、任务、迭代、测试用例、Wiki 等实体管理。使用场景包括：(1) 查询/创建/更新需求、缺陷、任务、迭代 (2) 管理测试用例和 Wiki (3) 管理评论和工时 (4) 关联需求与缺陷 (5) 获取源码提交关键字
---

# tapd-skill Skill

TAPD 敏捷研发管理平台集成 Skill，通过调用 TAPD API 实现研发管理全流程操作。

## When to Activate

This Skill activates when:
- 用户提及 TAPD 相关操作（需求、缺陷、任务、迭代等）
- 用户提到查询、创建、更新研发管理实体
- 用户需要管理与 TAPD 相关的工时、评论、Wiki
- 用户需要获取源码提交关键字关联需求

## Capabilities

What this Skill can help with:

1. **需求管理**：查询、创建、更新需求（Stories）
2. **缺陷管理**：查询、创建、更新缺陷（Bugs）
3. **任务管理**：查询、创建、更新任务（Tasks）
4. **迭代管理**：查询、创建、更新迭代（Iterations）
5. **测试用例管理**：查询、创建、更新测试用例（Test Cases）
6. **Wiki 管理**：查询、创建、更新 Wiki 文档
7. **评论管理**：添加、更新、查询评论
8. **工时管理**：记录、更新工时
9. **关联关系**：创建需求与缺陷的关联
10. **源码提交**：获取需求的提交关键字

## Quick Links (Progressive Disclosure)

- [Schemas](./schemas/)
- [Templates](./templates/)
- [Examples](./examples/)
- [Best Practices](./best-practices/)

## Workflow

How this Skill operates:

1. **识别需求**：理解用户对 TAPD 操作的意图
2. **选择工具**：根据操作类型选择合适的 TAPD 工具
3. **执行操作**：调用 TAPD API 完成操作
4. **返回结果**：返回操作结果和相关信息链接

## Common Patterns

### Pattern 1: 查询需求

```bash
# 查询特定项目下的需求
/plugin tapd get-stories --workspace_id=项目ID --options='{"entity_type": "stories"}'
```

### Pattern 2: 创建缺陷

```bash
# 创建缺陷
/plugin tapd create-bug --workspace_id=项目ID --title="缺陷标题"
```

### Pattern 3: 记录工时

```bash
# 为需求记录工时
/plugin tapd add-timesheets --workspace_id=项目ID --options='{"entity_type": "story", "entity_id": 需求ID, "timespent": "2h"}'
```

## Notes

- 需要提供正确的 workspace_id（项目 ID）
- 自定义字段查询前需先获取字段配置
- 工时记录需要指定正确的日期格式（YYYY-MM-DD）
- 所有操作链接均为可点击链接格式
