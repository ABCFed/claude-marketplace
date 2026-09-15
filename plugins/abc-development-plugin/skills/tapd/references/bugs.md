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

缺陷链接: `{tapd_base_url}/tapd_fe/{workspace_id}/bug/detail/{19位id}`

★ **旧格式 `/{workspace_id}/bugtrace/bugs/view/{id}` 已失效**（2026-09 起 TAPD 前端换代，
点开会报错或落到错页）。给用户发链接一律用上面的 `tapd_fe` 形式。

★★ **两个容易踩的点**：

1. **`{id}` 必须是 19 位长 id**；写成 16 位短号（漏掉中间的 `001`）同样打不开。
2. **路径段别多拼**：写成 `/{workspace_id}/tapd_fe/{workspace_id}/bug/detail/{id}`
   （workspace 号重复两段）会 404，而「含 `tapd_fe` + id 19 位」两条自检**都会通过**。

**发链接前自检三点**（缺一不可）：

- ① 路径含 `tapd_fe`；② id 长度 19；③ **域名后第一段就是 `tapd_fe`**（前面不能再有别的路径段）。

★★ 查验方式：**按 `/` 切段逐段核对结构**，不要只查「关键词在不在」，也不要改成
「数关键词出现几次」—— **workspace_id 是单据 id 的子串**（19 位 id 的结构是
`11` + workspace_id + 9 位序号），计数法会把合法链接判成非法（假红）。

```bash
# 判据示例：第 4 段是 tapd_fe、共 8 段、末段 19 位
echo "$U" | awk -F/ '{print (($4=="tapd_fe" && NF==8 && length($NF)==19) ? "✓" : "✗")}'
```

★ 别用 HTTP 状态码验证 TAPD 链接是否有效：新旧路径都可能返回 200（SPA 外壳）
或 302 到登录页，**那是假绿**。

## 关联需求与缺陷（★ 实测有坑：写入侧别只看 success）

```python
# 查：需求关联的缺陷（读的是需求-缺陷标准关联）
get_related_bugs(
    workspace_id=123,
    options={"story_id": "需求ID"}
)
```

★ **两种写入做法都不可靠，必须回读验证**：

| 做法 | 实测表现 |
|---|---|
| `entity_relations`（`POST /relations`，`source_type=story&target_type=bug`） | 返回 `status:1` 与一个 relation id，**但第二次调用返回同一个 id，`GET /relations` 查回来是空数组** —— 关联并未建立 |
| `update_bug` / `POST /bugs` 带 `story_id` | 返回体里带着 title/description 看着像成功，**回读 `story_id` 仍是 `null`** —— 该字段不接受 API 写入 |

★ 结论：**跨单据互链用评论**（`create_comments` 在需求单下发一条带缺陷链接的说明），
并以**回读评论**（`get_comments`）为判据。「提交成功」与「东西真的在了」是两件事。

★ 另：`get_comments` 返回的**顺序不可依赖**（实测最新一条不一定在末尾）；
要断言「我那条在不在」就按 id 或关键词遍历全部条目，不要取 `[-1]`。

★ 建缺陷时：`iteration_id` 要挂到**当前迭代**（验收标准往往是「后续在迭代里查得到」），
`reporter` / `current_owner` 填真实处理人；影响面要在描述里写准
（「不影响主流程、只影响报表类数据」这种分辨必须写清，否则接手的人无法定优先级）。
