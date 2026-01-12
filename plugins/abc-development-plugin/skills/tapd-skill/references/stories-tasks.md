# 需求/任务操作指南

## 创建需求

```python
create_story_or_task(
    workspace_id=123,
    name="需求标题",
    options={
        "description": "## 详细描述\n支持 Markdown 格式",
        "priority_label": "高",  # High/Middle/Low/Nice To Have
        "owner": "处理人",
        "cc": "抄送人",
        "developer": "开发人员",
        "iteration_name": "迭代名称",  # 或使用 iteration_id
        "category_name": "需求分类名称",  # 或使用 category_id
        "workitem_type_name": "需求类别名称",  # 或使用 workitem_type_id
        "parent_id": "父需求ID",
        "release_id": "发布计划ID",
        "version": "版本",
        "module": "模块",
        "size": 1,  # 规模点
        "custom_field_*": "自定义字段值"
    }
)
```

## 查询需求

```python
get_stories_or_tasks(
    workspace_id=123,
    options={
        "entity_type": "stories",  # 或 tasks
        "id": "需求ID，支持多ID逗号分隔",
        "name": "%搜索词%",  # 模糊匹配
        "v_status": "状态中文名",
        "status": "status1|status2|status3",  # 枚举查询
        "priority_label": "高",
        "owner": "处理人",
        "iteration_id": "迭代ID",
        "iteration_name": "迭代名称",
        "category_id": "需求分类ID",
        "creator": "创建人",
        "parent_id": "父需求ID",
        "children_id": "",  # 查子需求传:|
        "ancestor_id": "祖先需求ID",
        "limit": 10,
        "page": 1,
        "fields": "id,name,status,v_status,priority_label,owner"
    }
)
```

## 更新需求

```python
update_story_or_task(
    workspace_id=123,
    options={
        "entity_type": "stories",  # 或 tasks
        "id": "需求ID",
        "name": "新标题",
        "v_status": "新状态",
        "priority_label": "高",
        "description": "新描述",
        "owner": "新处理人"
    }
)
```

## 字段说明

| 字段 | 说明 |
|------|------|
| priority_label | 优先级：High(高)/Middle(中)/Low(低)/Nice To Have(无关紧要) |
| size | 规模点，整数类型 |
| parent_id | 父需求ID，为0表示是根需求 |
| children_id | 子需求查询，\| 表示空，查所有父需求用 != \| |

## URL 格式

- 需求链接: `{tapd_base_url}/{workspace_id}/prong/stories/view/{id}`
- 任务链接: `{tapd_base_url}/{workspace_id}/prong/tasks/view/{id}`
