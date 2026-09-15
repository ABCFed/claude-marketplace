# 迭代管理指南

## 创建迭代

```python
create_iteration(
    workspace_id=123,
    options={
        "name": "迭代名称",
        "startdate": "2024-01-01",  # 开始日期，必填
        "enddate": "2024-01-14",    # 结束日期，必填
        "creator": "创建人",
        "description": "迭代描述",
        "status": "open",  # open/done
        "label": "标签1|标签2"
    }
)
```

## 查询迭代

```python
get_iterations(
    workspace_id=123,
    options={
        "id": "迭代ID",
        "name": "迭代名称",
        "status": "open",  # open/done/自定义状态
        "startdate": "开始时间",
        "enddate": "结束时间",
        "limit": 30,
        "page": 1
    }
)
```

## 更新迭代

```python
update_iteration(
    workspace_id=123,
    options={
        "id": "迭代ID",
        "current_user": "变更人",
        "name": "新名称",
        "startdate": "新开始日期",
        "enddate": "新结束日期",
        "status": "done"
    }
)
```

## 字段说明

| 字段 | 说明 | 必填 |
|------|------|------|
| name | 迭代名称 | 是 |
| startdate | 开始日期 (YYYY-MM-DD) | 是 |
| enddate | 结束日期 (YYYY-MM-DD) | 是 |
| status | 状态: open/done | 否 |
| label | 标签，多个用竖线分隔 | 否 |
| parent_id | 父迭代ID | 否 |

## URL 格式

迭代链接: `{tapd_base_url}/tapd_fe/{workspace_id}/iteration/card/{19位id}`

★★ **迭代的尾段与 story/bug 不同，别按同族形式照推**：

| 实体 | 实测形态 |
|---|---|
| story / bug | `/tapd_fe/{ws}/{story\|bug}/detail/{id}` ← 尾段 `detail` |
| **iteration** | `/tapd_fe/{ws}/iteration/card/{id}` ← 尾段 **`card`** |

所以 `/iteration/detail/{id}` 这类「看着对称」的拼法是**错的**；旧格式
`/{workspace_id}/prong/iterations/card_view/{id}` 也已失效（点开报错）。

★ 通用教训：`tapd_fe` 只是「路由前缀已换代」，**每个实体的尾段各写各的** ——
拿不准就自己在浏览器里点开一次确认，或向用户要一条他点开过的链接。

## 使用迭代获取需求

查询时指定迭代ID可获取该迭代下的所有需求：

```python
get_stories_or_tasks(
    workspace_id=123,
    options={
        "entity_type": "stories",
        "iteration_id": "迭代ID"
    }
)
```
