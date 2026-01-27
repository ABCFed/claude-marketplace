# 缺陷管理指南

## 创建缺陷

```python
create_bug(
    workspace_id=123,
    title="缺陷标题",
    options={
        "description": "## 缺陷描述\n支持 Markdown 格式",
        "current_owner": "处理人",
        "cc": "抄送人",
        "reporter": "创建人",
        "priority_label": "高",  # urgent/high/medium/low/insignificant
        "severity": "严重程度",  # fatal/serious/normal/prompt/advice
        "module": "模块",
        "feature": "特性",
        "iteration_id": "迭代ID",
        "release_id": "发布计划ID",
        "custom_field_*": "自定义字段值"
    }
)
```

## 查询缺陷

```python
get_bug(
    workspace_id=123,
    options={
        "id": "缺陷ID，支持多ID逗号分隔",
        "title": "标题",
        "status": "status1|status2",  # 枚举查询
        "priority_label": "高",
        "severity": "fatal",  # fatal/serious/normal/prompt/advice
        "owner": "处理人",
        "developer": "开发人员",
        "limit": 10,
        "page": 1,
        "fields": "id,title,status,priority_label,severity,current_owner"
    }
)
```

## 更新缺陷

```python
update_bug(
    workspace_id=123,
    options={
        "id": "缺陷ID",
        "title": "新标题",
        "v_status": "新状态",
        "priority_label": "高",
        "severity": "严重程度",
        "description": "新描述",
        "current_owner": "新处理人"
    }
)
```

## 优先级/严重程度

### priority_label (优先级)
- `urgent`: 紧急
- `high`: 高
- `medium`: 中
- `low`: 低
- `insignificant`: 无关紧要

### severity (严重程度)
- `fatal`: 致命
- `serious`: 严重
- `normal`: 一般
- `prompt`: 提示
- `advice`: 建议

## URL 格式

缺陷链接: `{tapd_base_url}/{workspace_id}/bugtrace/bugs/view/{id}`

## 关联需求与缺陷

```python
# 创建关联
entity_relations(
    workspace_id=123,
    options={
        "source_type": "story",
        "target_type": "bug",
        "source_id": "需求ID",
        "target_id": "缺陷ID"
    }
)

# 查询需求关联的缺陷
get_related_bugs(
    workspace_id=123,
    options={
        "story_id": "需求ID"
    }
)
```
