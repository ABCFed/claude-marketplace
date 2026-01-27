# 字段配置指南

## 获取字段信息

### 获取所有字段及候选值

```python
get_stories_fields_info(workspace_id=123)
# 返回需求所有字段及候选值
```

### 获取字段中英文对照

```python
get_stories_fields_lable(workspace_id=123)
# 返回字段中英文映射
```

### 获取自定义字段配置

```python
get_entity_custom_fields(
    workspace_id=123,
    options={
        "entity_type": "stories"  # stories/tasks/bugs/iterations/tcases
    }
)
```

## 常用字段

### 需求/任务字段

| 字段 | 说明 | 示例值 |
|------|------|--------|
| v_status | 状态(中文) | 已开始、实现中、已验收 |
| status | 状态(英文) | progress |
| priority_label | 优先级 | 高、中、低 |
| owner | 处理人 | zhangsan |
| iteration_id | 迭代ID | 12345678 |
| category_id | 需求分类ID | 12345 |
| workitem_type_id | 需求类别ID | 123 |

### 缺陷字段

| 字段 | 说明 | 示例值 |
|------|------|--------|
| priority_label | 优先级 | 紧急、高、中、低 |
| severity | 严重程度 | 致命、严重、一般 |
| current_owner | 处理人 | zhangsan |
| de | 开发人员 | lisi |

## 自定义字段使用

使用自定义字段前必须先获取字段配置：

```python
# 1. 获取配置
config = get_entity_custom_fields(
    workspace_id=123,
    options={"entity_type": "stories"}
)
# 返回 custom_field_* 格式的字段名

# 2. 使用自定义字段查询
stories = get_stories_or_tasks(
    workspace_id=123,
    options={
        "entity_type": "stories",
        "custom_field_1": "值"
    }
)

# 3. 使用自定义字段创建
create_story_or_task(
    workspace_id=123,
    name="需求",
    options={
        "custom_field_1": "值"
    }
)
```

## 工作流状态

### 获取状态映射

```python
# 获取中英文状态对照
status_map = get_workflows_status_map(
    workspace_id=123,
    options={
        "system": "story",  # 或 bug
        "workitem_type_id": "需求类别ID"
    }
)
```

### 获取可流转状态

```python
# 查询当前状态可以流转到哪些状态
transitions = get_workflows_all_transitions(
    workspace_id=123,
    options={
        "system": "story",  # 或 bug
        "workitem_type_id": "需求类别ID"
    }
)
```

### 获取结束状态

```python
# 获取工作流结束状态
last_steps = get_workflows_last_steps(
    workspace_id=123,
    options={
        "system": "story",
        "workitem_type_id": "需求类别ID"
    }
)
```
