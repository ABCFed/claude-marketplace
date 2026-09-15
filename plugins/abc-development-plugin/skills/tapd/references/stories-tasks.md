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

- 需求链接: `{tapd_base_url}/tapd_fe/{workspace_id}/story/detail/{19位id}`
- 任务链接: `{tapd_base_url}/tapd_fe/{workspace_id}/task/detail/{19位id}`

★ 旧格式 `/{workspace_id}/prong/{stories,tasks}/view/{id}` 已失效（2026-09 起 TAPD 前端换代）。
`tapd_fe` 形式的**尾段按实体各写各的**（story/bug/task 是 `detail`，迭代是 `card`），
别互相套用；id 一律 19 位长 id。

## 父子需求：改挂必须用专用接口 `update_story_parent`

| 操作 | 正确做法 |
|---|---|
| 创建时挂父需求 | `POST /stories` 带 `parent_id` ✅ **生效** |
| **给已存在需求改挂父需求** | **`POST /stories/update_story_parent`**，参数 `story_id` + `parent_id` + `workspace_id`（form 或 json body 均可）✅ **生效** —— ★ 两个 id 都必须是 19 位长 id，见下方踩坑 |
| 从父需求下移出 | 同一接口传 `parent_id=0` ✅ **生效**（回读 `path` 只剩自己，父需求 `children_id` 同步移除） |
| 删除需求 | ❌ 开放 API 不支持：`DELETE /stories` → 422 ParamError；`POST /stories/delete` → 403 |

**踩坑 1：用通用更新接口传 `parent_id` 会被静默忽略。**
`POST /stories` 或 `POST /stories/update` 传 `parent_id`、`children_id`、`ancestor_id` 都**无效** ——
返回 `status:1` 看着像成功，回读 `parent_id` 仍是 `0`。短号代替长号、`PUT /stories`（405）也全无效。

**踩坑 2（更隐蔽）：`parent_id` 传短号会「假成功」。**
把短号（如 `1000209`）传给 `update_story_parent`：返回 `status:1 success`，但回读发现
`parent_id` 被**原样写成字符串 `1000209`**、`level` 仍是 `0`、`path` 里没有父 id
—— 既没建立关系，还在字段里留了个指向不存在需求的脏值（得再传一次 `parent_id=0` 清掉）。
同一接口传 19 位长 id 则一次成功，回显 `path=<父id>:<子id>:`。

★ **报「这个接口不支持挂父单」之前，先核 id 位数**：

```bash
printf '%s' "$id" | wc -c    # 必须是 19
```

**踩坑 3：别拿真实单据当参数探针。**
为验证参数对一条已有子单试 `parent_id=0`，那次**真的把它从父需求下摘掉了**；
而后续「挂回」因 id 传错全部失败，一度无法恢复。
要试参数就先新建一条一次性需求来试，或确认参数无误再对真实单动手。

★ **回读判据走列表查询**：`parent_id == 父单id`、`level == 1`、`path` 形如 `<父id>:<子id>:`
三项都对才算挂上。单查 `--id` 拿不到 `parent_id`（见 SKILL.md 的「极简字段集」一节）。
