---
name: tapd
description: TAPD 敏捷研发管理平台集成。使用脚本调用 TAPD API，实现需求、缺陷、任务、迭代、测试用例、Wiki 等实体管理。使用场景包括：(1) 查询/创建/更新需求、缺陷、任务、迭代 (2) 管理测试用例和 Wiki (3) 管理评论和工时 (4) 关联需求与缺陷 (5) 获取源码提交关键字
---

# TAPD Skill

本 skill 提供与 TAPD 平台交互的 Python 脚本工具，统一通过 `tapd.py` 调用。

## 环境配置

使用前需要配置以下环境变量：
```bash
export TAPD_ACCESS_TOKEN="你的个人访问令牌"  # 推荐
# 或
export TAPD_API_USER="API账号"
export TAPD_API_PASSWORD="API密钥"

export TAPD_API_BASE_URL="https://api.tapd.cn"  # 可选，默认
export TAPD_BASE_URL="https://www.tapd.cn"      # 可选，默认
export CURRENT_USER_NICK="你的昵称"               # 可选
```

## 使用方式

```bash
python scripts/tapd.py <command> [参数]
```

所有命令默认输出 JSON 格式结果。

## 命令列表

### 项目与用户
| 命令 | 说明 |
|------|------|
| `get_user_participant_projects` | 获取用户参与的项目列表 |
| `get_workspace_info` | 获取项目信息 |
| `get_workitem_types` | 获取需求类别 |

### 需求/任务
| 命令 | 说明 |
|------|------|
| `get_stories_or_tasks` | 查询需求/任务 |
| `create_story_or_task` | 创建需求/任务 |
| `update_story_or_task` | 更新需求/任务 |
| `get_story_or_task_count` | 获取数量 |
| `get_stories_fields_lable` | 字段中英文对照 |
| `get_stories_fields_info` | 字段及候选值 |

### 缺陷
| 命令 | 说明 |
|------|------|
| `get_bug` | 查询缺陷 |
| `create_bug` | 创建缺陷 |
| `update_bug` | 更新缺陷 |
| `get_bug_count` | 获取数量 |

### 迭代
| 命令 | 说明 |
|------|------|
| `get_iterations` | 查询迭代 |
| `create_iteration` | 创建迭代 |
| `update_iteration` | 更新迭代 |

### 评论
| 命令 | 说明 |
|------|------|
| `get_comments` | 查询评论 |
| `create_comments` | 创建评论 |
| `update_comments` | 更新评论 |

### 附件/图片
| 命令 | 说明 |
|------|------|
| `get_entity_attachments` | 获取附件 |
| `get_image` | 获取图片下载链接 |

### 自定义字段
| 命令 | 说明 |
|------|------|
| `get_entity_custom_fields` | 获取自定义字段配置 |

### 工作流
| 命令 | 说明 |
|------|------|
| `get_workflows_status_map` | 状态映射 |
| `get_workflows_all_transitions` | 状态流转 |
| `get_workflows_last_steps` | 结束状态 |

### 测试用例
| 命令 | 说明 |
|------|------|
| `get_tcases` | 查询测试用例 |
| `create_or_update_tcases` | 创建/更新测试用例 |
| `create_tcases_batch` | 批量创建测试用例 |

### Wiki
| 命令 | 说明 |
|------|------|
| `get_wiki` | 查询 Wiki |
| `create_wiki` | 创建 Wiki |
| `update_wiki` | 更新 Wiki |

### 工时
| 命令 | 说明 |
|------|------|
| `get_timesheets` | 查询工时 |
| `add_timesheets` | 填写工时 |
| `update_timesheets` | 更新工时 |

### 待办
| 命令 | 说明 |
|------|------|
| `get_todo` | 获取待办 |

### 关联
| 命令 | 说明 |
|------|------|
| `get_related_bugs` | 获取关联缺陷 |
| `entity_relations` | 创建关联关系 |

### 发布计划
| 命令 | 说明 |
|------|------|
| `get_release_info` | 获取发布计划 |

### 源码
| 命令 | 说明 |
|------|------|
| `get_commit_msg` | 获取提交关键字 |

### 消息
| 命令 | 说明 |
|------|------|
| `send_qiwei_message` | 发送企业微信消息 |

## 源码提交关键字（把提交关联到需求）

TAPD 项目与代码仓库建立关联后，**提交信息里带上关键字即可自动关联**到对应需求
（提交会出现在该需求的「源码」页）。

```bash
# 取关键字（用真实的需求短号与类型）
python scripts/tapd.py get_commit_msg --workspace_id 12345678 \
  --object_id 1000197 --type story
# → "--story=1000197@tapd-12345678 --user=someone 【需求标题】 https://www.tapd.cn/12345678/s/1000377"
```

- 关键字形式：`--story=<需求短号>@tapd-<workspace_id>`（bug / task 换成 `--bug=` / `--task=`）。
- ★ **`--object_id` 必须传短号**（如 `1000197`）；传 19 位长 id 会 `422 ParamError`。
- 把**整行**放进 commit message（放末尾一行最稳）；**一条提交只带一条关键字**
  （一次带多条是否能同时关联多张单据**未验证**，别假设一定生效）。
- 括注写法（如「（TAPD 1112345678001000215）」）**TAPD 不认**，不会建立关联 ——
  必须是上面那种 `--story=...@tapd-...` 整行。
- `get_commit_msg` 返回的尾链（`/s/1000551`）**每次调用都新生成**，不可当稳定 ID 去比对；
  真正起关联作用的是前缀 `--story=<短号>@tapd-<workspace_id>`。

★ **回读关联用 `svn_commits`，不要用 `stories/get_commits`**（后者 403 无权限，
但**不代表这件事查不到** —— 换接口即可）：

```bash
curl -s -H "Authorization: Bearer $TAPD_ACCESS_TOKEN" \
  "https://api.tapd.cn/svn_commits?workspace_id=12345678&type=story&object_id=<19位长id>&limit=50"
# → {"status":1,"data":[{"repository":"...","user":"...","comment":"<提交信息全文>"}]}
# data 的条数 = 该需求关联的提交数；comment 即提交信息全文
```

- ★ 这里的 `object_id` 反而**必须传 19 位长 id**（与取关键字时相反）；`type` 必传
  （缺 → `422 type is required.`）。
- ★ **传错的表现是「静默空」不是报错**：自己用字符串拼成 16 位会得到 `status:1` + `data:[]`，
  看着就是「没关联任何提交」，会把「id 拼错」误判成「关联失败」。
  ⇒ 取 id 一律从工具返回里复制，并断言 `len(id) == 19`。
- ★ **关联是 TAPD 侧异步同步，有时滞**：实测同一仓库里早推的提交已挂上、晚推的隔 50 分钟仍未出现。
  ⇒ **「刚推完就查」得到空列表属于正常现象**，不要在推完几分钟内就判定「关联失败」。
- ★ 「关联数为 0」要分三种原因查：① 关键字没带或写成括注式；② 同步时滞；③ 代码库未与 TAPD 绑定。

## 创建/查询的返回结构（写脚本前先看，两个坑都实测过）

- ★★ **`create_story_or_task` 的返回是「两层 data」**：外层是 `{"data": "<json 字符串>"}`，
  `json.loads` 之后才是 `{"status":1,"data":{"Story":{...}},"info":"success"}` ——
  取 id 要写 `json.loads(resp["data"])["data"]["Story"]["id"]`。直接 `resp["data"]["Story"]`
  会报 `TypeError: string indices must be integers`（看着像接口出错，其实是没拆第二层）。
- ★★ **`get_stories_or_tasks --id <单个id>` 返回的 Story 是「极简字段集」**：实测只有
  `description` / `secret_workitem`，**没有 `name`、没有 `parent_id`** ——
  用它核对标题或父子关系会得到 `None`，误判成「没写进去」。核对父子关系要用**列表查询**（不带 `--id`）。
- ★★ **反向也成立：列表查询（含 `--name` 搜索）不下发 `description`** —— 用列表查回读刚写入的描述
  会看到空串，**误判成「没写进去、白改了」**。
  ⇒ 一句话分工：**单查 `--id` 取 `description`，列表查取 `status` / `iteration_id` / `parent_id`**。
  要核对两样就得查两次，别图省事只跑一次。
  同理，写描述前的「先备份原文」也必须用单查 —— 列表查拿到的是空串，备份出来等于没备。
- 顶层 `data` 的形状有两种：列表查询是 `list[{Story:{...}}]`，创建响应是 json 字符串（见上）。
- **TAPD 对空字段返回 `null` 而不是空串**：取值一律写 `x.get('k') or 默认值`，
  别用 `x.get('k', 默认值)` —— 后者只在「键不存在」时兜底，值为 null 时仍返回 None，
  后续字符串/正则操作会抛 `TypeError: expected string or bytes-like object, got 'NoneType'`。

## 使用示例

### 查询需求

```bash
# 查询指定需求
python scripts/tapd.py get_stories_or_tasks --workspace_id 123 --entity_type stories --id 1167459320001114969

# 模糊搜索需求
python scripts/tapd.py get_stories_or_tasks --workspace_id 123 --entity_type stories --name "%登录%" --limit 20

# 查询指定状态的需求
python scripts/tapd.py get_stories_or_tasks --workspace_id 123 --entity_type stories --v_status "已验收"
```

### 创建需求

```bash
# ★ description 必须是 HTML（TAPD 该字段是富文本 "rich_edit"），不能写 markdown 或纯文本换行 ——
#   纯文本里的 \n 会被前端丢掉，所有段落挤成一坨。详见「已知坑 → 富文本」。
python scripts/tapd.py create_story_or_task --workspace_id 123 \
    --name "用户登录功能" \
    --description "<p><strong>需求描述</strong></p><p>用户可以通过账号密码登录系统</p>" \
    --priority_label "高" \
    --owner "zhangsan" \
    --iteration_name "Sprint 1"

# 改描述同样用 HTML；长内容先写进文件再读入，可免去 shell 转义麻烦
python scripts/tapd.py update_story_or_task --workspace_id 123 \
    --id 1167459320001114969 --description "$(cat desc.html)"
```

### 更新需求状态

```bash
python scripts/tapd.py update_story_or_task --workspace_id 123 \
    --id 1167459320001114969 \
    --v_status "实现中"
```

### 查询缺陷

```bash
python scripts/tapd.py get_bug --workspace_id 123 --title "%登录失败%" --priority_label "高"
```

### 创建缺陷

```bash
python scripts/tapd.py create_bug --workspace_id 123 \
    --title "登录页面显示异常" \
    --description "输入正确密码后提示错误" \
    --priority_label "高" \
    --severity "严重"
```

### 迭代管理

```bash
# 查询迭代
python scripts/tapd.py get_iterations --workspace_id 123

# 创建迭代
python scripts/tapd.py create_iteration --workspace_id 123 \
    --name "Sprint 1" \
    --startdate "2024-01-01" \
    --enddate "2024-01-14" \
    --creator "zhangsan"
```

### 工时管理

```bash
# 查询工时
python scripts/tapd.py get_timesheets --workspace_id 123 --entity_type story --entity_id 1167459320001114969

# 填写工时
python scripts/tapd.py add_timesheets --workspace_id 123 \
    --entity_type story \
    --entity_id 1167459320001114969 \
    --timespent "4" \
    --spentdate "2024-01-08" \
    --memo "开发登录功能"
```

### 评论管理

```bash
# 查询评论
python scripts/tapd.py get_comments --workspace_id 123 \
    --entry_type stories \
    --entry_id 1167459320001114969

# 创建评论
python scripts/tapd.py create_comments --workspace_id 123 \
    --entry_type stories \
    --entry_id 1167459320001114969 \
    --description "看起来不错，可以继续完善"
```

### 关联需求与缺陷（★ 写入侧实测靠不住，详见 references/bugs.md）

```bash
# 查询需求关联的缺陷
python scripts/tapd.py get_related_bugs --workspace_id 123 --story_id 1167459320001114969

# 创建关联 —— ★ 实测可能返回 success 但关联并未建立（GET relations 查回来是空数组）；
# 也不要指望 update_bug 写 story_id（回读仍是 null）。
# 跨单据互链请改用评论：create_comments 在需求单下发带缺陷链接的说明，并回读验证。
python scripts/tapd.py entity_relations --workspace_id 123 \
    --source_type story \
    --target_type bug \
    --source_id 1167459320001114969 \
    --target_id 1167459320001114970
```

### 工作流

```bash
# 获取状态映射
python scripts/tapd.py get_workflows_status_map --workspace_id 123 --system story

# 获取可流转状态
python scripts/tapd.py get_workflows_all_transitions --workspace_id 123 --system story
```

## 已知坑（实测集合，动手前扫一遍）

### id 一律用 19 位长 id

★★ 需求 / 缺陷 / 迭代的 id 都是 19 位；写成 16 位短号（漏掉中间的 `001`）会
「**读静默空、写却成功**」—— 最坏的组合。实测：`get_bug --id <短号>`、`GET /bugs?id=<短号>`、
`get_comments --entry_id <短号>` **全部返回 `status:1` + `data:[]`**（不报错，看着像
「单子不存在 / 评论没发出去」）；而**写**接口（`POST /comments` 的 `entry_id`）会把短号
规范化后**真写进正确的那张单**。⇒ 于是「写成功了、读却说没有」，极易误判成「关单失败、评论没落库」。

**规矩：id 一律从列表查询返回里原样复制，并在脚本里 `assert len(id) == 19`** ——
比事后对着空结果怀疑权限省事得多。

### 字段名在两侧不对称

- ★★ **建缺陷的标题字段是 `title`，不是 `name`**：传 `name` 报 `422 title is required.`
  —— 提示语只提 title，不告诉你字段名错了，容易往「标题内容不合法」方向查。
  **需求侧用 `name`、缺陷侧用 `title`**，写脚本时按类型分支，别用一个 body 打天下。
- ★★ **评论的 `entry_type`：需求是 `stories`（复数）、缺陷是 `bug`（单数）**，写错直接 422。
  实测给缺陷传 `bugs` → `422 invalid entry_type bugs`，再试 `bugtrace_bugs` / `bugtrace` /
  `b` / `defect` **全部 422，只有 `bug` 通过**；给需求传 `story` 也被拒。
  ★ **探针发出去就是一条真评论**（TAPD 没有删除评论的 API）—— 别拿真单试探；
  已发错可用 `update_comments` 改写成正式内容（实测可改写，`modified` 会更新）。

### 关联类接口的行为与直觉不符

- ★★ **`entity_relations` 可能返回 success 但关联并未建立**（详见 `references/bugs.md`）；
  `update_bug` / `POST /bugs` 写 `story_id` 回读仍是 `null`。
  ⇒ 跨单据互链优先用**评论 + 回读评论**做判据。
- ★★ **缺陷挂不了父需求**：`POST /bugs` 传 `parent_id`（19 位父需求 id）**被静默忽略**，
  响应与回读的 `parent_id` 都是 `None`，而同一 body 里的 `iteration_id` 正常写入。
  这不是 id 位数问题 —— TAPD 的「父子」是**需求**体系的概念，缺陷只归迭代、不参与需求父子树。
- ★★ **父需求（下面挂了子单的）不允许设置 `iteration_id`**：报 422
  `the parent story <id> was not allowed set iteration_id value`。迭代归属只能由子需求体现；
  批量挂迭代前先滤掉父单，否则每轮刷一堆失败噪音，容易被当成「接口坏了」。
- ★ **清空迭代归属要传 `iteration_id: "0"`**（传空字符串语义不明），实测可把单子从迭代里摘出。

### 更新类子命令覆盖不全，缺参数就直接发请求

- ★ **`update_story_or_task` / `update_bug` 都没有 `--iteration_id` 参数**
  （只有 description/status/priority/owner/severity）。要挂迭代得直接发请求：
  `POST https://api.tapd.cn/stories`（或 `/bugs`），`Content-Type: application/json` +
  `Authorization: Bearer <token>`，body 带 `{workspace_id, id, iteration_id, current_user}`。
  顺带一个好处：JSON body **一条请求能同时改多个字段**，长 HTML 描述也不受 shell 转义折磨 ——
  批量整理单据时比逐条调 CLI 稳得多。
- ★★ **父子需求改挂必须用专用接口 `POST /stories/update_story_parent`**
  （用通用更新接口传 `parent_id` 会静默忽略）—— 详见 `references/stories-tasks.md`。
- ★★ **缺陷要一次落「迭代 + 优先级 + 严重程度」时别用 `create_bug` 子命令**（它没有 `--iteration_id`）。
  直接 `POST https://api.tapd.cn/bugs` + JSON body：
  `{workspace_id, title, description(HTML), priority_label, severity, iteration_id, reporter}`，
  实测一条请求全部写入并在响应里回显 `iteration_id`（可直接核对）。
  取值实测被接受：`priority_label` = `high`/`medium`/`low`；`severity` = `serious`/`normal`/`prompt`
  （**英文，不是中文**「严重」）。
- **TAPD 没有「删除需求」的 API**（`tapd.py` 里无 delete，只有状态流转）。
  要「清理」重复单/作废单，手段是置状态为「已拒绝」并补一条**作废说明评论**
  （写明「以哪条为准、不要再据此开发」）。真要物理删除只能走 TAPD 网页端（回收站语义）。

### 状态相关的两个反直觉点

- ★★ **需求（story）没有「已关闭」这一档 —— 它只有两个终态：`resolved`（已实现）、`rejected`（已拒绝）**。
  `get_workflows_status_map --system story` 返回的就是 planning / developing / resolved / rejected
  （+ 项目自定义的 status_2 / status_3）；**「已关闭」是缺陷（bug）才有的状态**。
  ⇒ 用户说「关需求单」时，先去查状态映射与项目惯例（`get_stories_or_tasks` 看别单怎么收尾），
  需求侧置 `resolved` 即可；不要自己造一个 `closed` 值发过去。
- ★★ **状态可以用接口一步设到目标值（可能绕过工作流），但页面点不动**。
  `workflows/all_transitions` 给的是**工作流允许的**流转（例：从 `planning` 只允许去
  `developing` / `rejected`，没有直达 `resolved` 的路径），但 `update_story_or_task --status resolved`
  实测**直接成功**并写回 `completed` 时间。两个后果要知道：
  ① 接口改完状态后状态历史里没有中间流转记录（组织若要求轨迹完整，需与 TAPD 管理员确认工作流）；
  ② 用户之后在页面上手动点状态会被工作流拦住，**这不是权限坏了**。
  ⇒ **收尾就一条动作**：设目标状态，然后**回读** `status` + `completed` 确认真的落库
  （别只看接口返回成功）。流转表的用途只有一个：解释「为什么页面上点不动」这类现象。
- ★★ **评论报 422「the stories `<id>` not in workspace `<ws>`」不等于参数写错**。
  报错文本看着像「id / workspace 不对」，但往往参数**完全正确**：
  用 `get_stories_or_tasks --workspace_id <ws>` 列一遍就能看到那条 story 就在列表里。
  **正确姿势（按序）**：① 先做**存在性取证**（列表里能看到 → 参数没问题，**不要再改参数**）；
  ② **原样重试**（实测同一条完全相同的请求隔几分钟就返回 200）；③ 还不行再查 token 权限，
  别一上来就怀疑 token。评论的 `author` / `change_creator` 要填**工作区里的真实昵称**。

### 富文本（描述与评论）—— 发完必须回读自检

- ★ **description 是富文本，必须传 HTML；传纯文本会「挤成一坨」**。
  TAPD 官方字段元数据接口（`get_stories_fields_info`）对 description 返回
  `"html_type": "rich_edit"`，网页端按 HTML 渲染 —— 纯文本里的 `\n` **全部丢失**。
  正确写法：

  ```html
  <p><strong>需求背景</strong></p>
  <p>正文段落</p>
  <ul><li>要点一</li><li>要点二</li></ul>
  ```

  排版约定：段落用 `<p>`；小节标题用 `<p><strong>标题</strong></p>`（不依赖 h1-h6）；
  列表用 `<ul><li>` / `<ol><li>`；**不要**用 markdown 语法。
  传入时避免 ASCII 双引号，可免去 shell 转义麻烦。
- ★★ **这条对「评论」一样成立** —— `create_comments` / `update_comments` 的 `--description`
  是同一个富文本字段。评论是「给人读」的交付物，比需求描述更容易被忽略这一条。
- ★★ **描述/评论的 HTML 会被 TAPD 规范化：`<br/>` 变成 `<br  />`（两个空格）**。
  后果：拿「上次写进去的富文本」做锚点去二次修改时，**锚点命中 0 次**（看着像内容丢了）。
  稳妥做法：改前先 `desc.replace("<br  />", "<br/>").replace("<br />", "<br/>")` 归一化再匹配；
  回读判据也别用「逐字节相等」，用 **`re.sub(r"\s+", "", s)` 忽略空白后相等**。
- ★ **改描述前先「单查取原文 → 落盘备份」**（`--id` 单查才有 description），再做定点替换，
  并断言每个锚点**恰好命中 1 次**；命中 0 次或多于 1 次就中止不提交 ——
  长描述整段重写迟早会把别处的更新覆盖掉。
- **回读自检的判据用「标签个数」，不要用「有没有换行」**：

  ```python
  rc, out, _ = run("get_comments", "--workspace_id", WS, "--entry_type", "stories", "--entry_id", ID)
  desc = <从返回里取 description>
  assert desc.count("<p>") >= 3, "仍是纯文本 → 前端会挤成一坨"
  # HTML 源码里标签之间本来就有 \n，所以不能拿 desc 里有没有 \n 判断（那会永远通过）
  ```

  ★ `get_comments` 的 `data` 是 `[{'Comment': {...}}]` 而**不是裸 list** ——
  直接取 `c.get('description')` 会拿到 `None`，于是自检**假红**（看着像没发出去）。
  正确取法：`for it in d['data']: c = it.get('Comment') or {}`。
- **TAPD 没有删除评论的 API**。若先发了一条「连通自测」或发成了纯文本，
  用 `update_comments --workspace_id <ws> --id <评论id> --change_creator <昵称> --description <HTML>`
  把它**改写成正式内容**（实测可行，`modified` 会更新）；改完必须回读自检 HTML 形态。

### 附件与图片

- ★ **附件（非图片：PDF/Excel/zip/代码包）走 `files/upload_attachment`**，挂到工作项的附件区。
  multipart 字段名是 **`file`**；参数为 `workspace_id` + `type=story`（或 `task`/`bug`）+ `entry_id`。

  ```bash
  curl -H "Authorization: Bearer $TAPD_ACCESS_TOKEN" \
    -F 'workspace_id=12345678' -F 'type=story' -F 'entry_id=<19位id>' \
    -F 'file=@/tmp/文档.pdf' https://api.tapd.cn/files/upload_attachment
  # → {"data":{"Attachment":{"id":"...","type":"story","filename":"文档.pdf", ...}}}
  ```

  - **不要传 `custom_field`**：那是给「自定义字段附件」用的。传了但字段英文名不是真实自定义字段，
    会 422 `custom_field parameters only apply to story, task and bug`（官方文档的示例就是这么写的，
    容易让人误以为必须传）。
  - 上传后可用 `attachments?workspace_id=&entry_id=&type=story` 回读确认。
- ★ **取回附件（机器人读别人上传的文件）：`attachments/down`**。

  ```bash
  curl -H "Authorization: Bearer $TAPD_ACCESS_TOKEN" \
    'https://api.tapd.cn/attachments/down?workspace_id=12345678&id=<附件id>'
  # → Attachment.download_url（可直接下载原文）
  ```

  下载链接**只 300 秒有效**，取到就立即用，别存别外发。
- ★ **描述里插图用 `files/upload_image`**（multipart 字段名 = `image`），
  把返回的 `html_code` 原样插进描述。这是 TAPD 自家图床，**不要用外部图床**。

  ```bash
  curl -H "Authorization: Bearer $TAPD_ACCESS_TOKEN" \
    -F 'workspace_id=12345678' -F 'type=story' -F 'image=@/tmp/pic.jpg' \
    https://api.tapd.cn/files/upload_image
  # → {"data":{"image_src":"/tfl/pictures/202609/api_12345678_....jpg",
  #           "html_code":"<img src=\"/tfl/pictures/202609/....jpg\"/>"}}
  ```

  - 路径形如 `/tfl/pictures/YYYYMM/api_{workspace_id}_{ts}{rand}.{ext}`，**是相对路径**，
    前端会解析（外部直接访问不可达）—— 所以描述里就写相对路径，不要改写成绝对域名。
  - `image_src` 为空（`/tfl/`）= **字段名传错**；表单字段必须叫 `image`（multipart 文件），
    其余名字（image_data/base64_data/data/content）都会被当空值**静默成功**。
  - 错误示范：`files/upload_image_base64` 的 `type` 只能是 `story_custom_field`（给自定义字段用的），
    传 `type=story_description` 直接 422。
- **验证图片路径归属**：`get_image`（`files/get_image`，传 `image_path`）返回 `type: tfl_image`
  + `filename` + 300 秒临时 `download_url` 即路径有效；报 `image X not belong request workspace`
  则路径/空间不对。该 `download_url` 有时效，**不能**写进 description（过期即裂图）。
- ★ **附件无法在 description 里做持久链接，只有图片可以**。
  想「在正文里看到文件内容」只能把内容转成图片插进描述，真文件走附件区。
- ★ **缺陷描述里 `<pre>` / `<code>` 实测能原样保留**（贴代码片段与生产日志很有用），
  `<p>/<strong>/<ul>/<ol>` 一如既往可用。多行日志用 `<pre>`，行内标识用 `<code>`；
  HTML 里的 `&` 必须写成 `&amp;`（否则富文本解析会吞字符）。
- ★ **建单时正文里写「用户提供/报告的原始信息」（原始 URL、复现时间、报错原文）时要标出来源**，
  方便后续人区分「用户实测」与「排查者推断」——同一份描述里这两类证据可信度不同，
  混在一起会被当成全都实测过。
- ★★ **「缺陷转需求」：网页端有，开放 API 没有**。
  TAPD 官方更新日志（<https://www.tapd.cn/official/release_note>）写明缺陷支持**批量转需求**
  并可选择需求类别，但**官方 API 文档的缺陷章节里没有转需求接口**。
  ⇒ 遇到「本质是需求、不是坏了」的缺陷：标「已拒绝」+ 加说明评论，**转需求这一步留给用户
  在平台上点**（网页端支持批量转 + 选类别，比逐条 API 建单快）。
  回答这类「平台有没有某能力」的问题前，**先去官方更新日志搜关键词**验证，比凭记忆断言可靠。

## 常用命令速查

```bash
# 需求
python scripts/tapd.py get_stories_or_tasks --workspace_id $WS_ID --entity_type stories
python scripts/tapd.py create_story_or_task --workspace_id $WS_ID --name "标题"
python scripts/tapd.py update_story_or_task --workspace_id $WS_ID --id $ID --v_status "状态"

# 缺陷
python scripts/tapd.py get_bug --workspace_id $WS_ID
python scripts/tapd.py create_bug --workspace_id $WS_ID --title "标题"

# 迭代
python scripts/tapd.py get_iterations --workspace_id $WS_ID
python scripts/tapd.py create_iteration --workspace_id $WS_ID --name "Sprint X" --startdate "2024-01-01" --enddate "2024-01-14"

# 工时
python scripts/tapd.py add_timesheets --workspace_id $WS_ID --entity_type story --entity_id $ID --timespent 4 --spentdate "2024-01-08"

# 评论
python scripts/tapd.py create_comments --workspace_id $WS_ID --entry_type stories --entry_id $ID --description "评论内容"
```

## 状态值说明

| 类型 | 字段 | 可用值 |
|------|------|--------|
| 需求优先级 | `priority_label` | High / Middle / Low / Nice To Have |
| 缺陷优先级 | `priority_label` | urgent / high / medium / low / insignificant |
| 缺陷严重程度 | `severity` | fatal / serious / normal / prompt / advice |
| 任务状态 | `status` | open / progressing / done |
| 迭代状态 | `status` | open / done |

## Claude 使用方式

当用户需要与 TAPD 交互时：

1. **读取脚本**：了解命令用法
2. **构建命令**：根据需求构建参数
3. **执行脚本**：使用 Bash 工具运行
4. **处理结果**：解析输出，分析数据

示例工作流：
```
用户: "查看需求 1167459320001114969 的详情"

Claude:
1. python scripts/tapd.py get_stories_or_tasks --workspace_id 67459320 --entity_type stories --id 1167459320001114969
2. 分析返回的需求信息
```

### 图片处理

当获取需求详情时，`get_stories_or_tasks` 命令会自动解析 description 中的图片并获取下载链接。

**返回结果包含 `images` 字段**：
```json
{
  "data": [
    {
      "Story": { "id": "1167459320001114969", "name": "需求标题", ... },
      "images": [
        {
          "path": "/tfl/captures/2026-01/tapd_67459320_base64_1767668922_121.png",
          "download_url": "https://file.tapd.cn/attachments/tmp_download/...?salt=...&time=...",
          "filename": "tapd_67459320_base64_1767668922_121.png"
        }
      ]
    }
  ]
}
```

**处理步骤**：
1. 从返回结果中读取 `images` 数组
2. 使用 `download_url` 访问或下载图片
3. 图片链接有效期约 300 秒

**手动获取图片**（备用方式）：
```bash
# 如果需要单独获取某张图片
python scripts/tapd.py get_image --workspace_id 67459320 --image_path "/tfl/captures/2026-01/tapd_xxx.png"
```

## 文件结构

```
scripts/
├── tapd.py           # 统一入口脚本（43个子命令）
├── tapd_client.py    # TAPD API 客户端
└── requirements.txt
```
