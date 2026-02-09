≥# ABC Claude Code Plugin Marketplace

中文 | [English](./README_EN.md)

本仓库托管了 ABC 团队的 Claude Code 插件市场。

## 快速开始

### 通过 skills CLI 安装（适用于所有 AI 代理）

![skills 安装示例](docs/install_screenshot.png)

```bash
# 安装单个 skill
npx skills add https://github.com/ABCFed/claude-marketplace/tree/main/skills/tapd
npx skills add https://github.com/ABCFed/claude-marketplace/tree/main/skills/apifox
npx skills add https://github.com/ABCFed/claude-marketplace/tree/main/skills/codeup
npx skills add https://github.com/ABCFed/claude-marketplace/tree/main/skills/jenkins-deploy
npx skills add https://github.com/ABCFed/claude-marketplace/tree/main/skills/git-flow
npx skills add https://github.com/ABCFed/claude-marketplace/tree/main/skills/modao-capture
npx skills add https://github.com/ABCFed/claude-marketplace/tree/main/skills/sls-trace-analyzer
npx skills add https://github.com/ABCFed/claude-marketplace/tree/main/skills/tapd-bug-analyzer
```

**常用选项**：

| 选项 | 说明 |
|------|------|
| `-g, --global` | 安装到用户目录而非项目目录 |
| `-a, --agent <agents...>` | 指定目标 agent（如 claude-code, codex） |
| `-s, --skill <skills...>` | 按名称安装指定 skills（多选用空格分隔） |
| `-l, --list` | 列出可用 skills但不安装 |
| `-y, --yes` | 跳过所有确认提示 |

**示例**：

```bash
# 安装到用户目录
npx skills add https://github.com/ABCFed/claude-marketplace/tree/main/skills/tapd --global

# 指定 agent 安装
npx skills add https://github.com/ABCFed/claude-marketplace/tree/main/skills/tapd --agent codex

# 跳过确认提示
npx skills add https://github.com/ABCFed/claude-marketplace/tree/main/skills/tapd --yes

# 列出仓库中所有可用 skills
npx skills add ABCFed/claude-marketplace --list
```

### 通过插件市场安装（仅 Claude Code）

```bash
# 启动 Claude Code
claude

# 添加本地插件市场
/plugin marketplace add https://github.com/ABCFed/claude-marketplace

# 安装 abc-development-plugin
/plugin install abc-development-plugin@abc-claude-plugin-marketplace
```

## 技能详情

### tapd

TAPD 敏捷研发管理平台集成，通过 TAPD API 实现研发全流程管理。

**安装**：
```bash
npx skills add https://github.com/ABCFed/claude-marketplace/tree/main/skills/tapd
```

**准备**：
```bash
# 编辑 ~/.zshrc 或 ~/.bashrc
export TAPD_ACCESS_TOKEN="your_token_here"
source ~/.zshrc
```

**触发关键词**：TAPD、需求、缺陷、任务、迭代、测试用例、Wiki、工时

**功能特性**：
- 需求管理 - 查询、创建、更新需求
- 缺陷管理 - 管理缺陷生命周期
- 任务管理 - 任务 CRUD 操作
- 迭代管理 - Sprint/迭代管理
- 测试用例 - 测试用例管理
- Wiki 管理 - 创建和更新 Wiki 文档
- 评论和工时 - 管理评论、记录工时
- 关联关系 - 需求与缺陷关联

---

### apifox

ABC 医疗云 API 文档查询工具，读取和查询 ABC API 的 OpenAPI 规范文档（4,000+ 接口）。

**安装**：
```bash
npx skills add https://github.com/ABCFed/claude-marketplace/tree/main/skills/apifox
```

**准备**：
```bash
# 编辑 ~/.zshrc 或 ~/.bashrc
export APIFOX_ACCESS_TOKEN="your_apifox_token_here"
export APIFOX_PROJECT_ID="4105462"  # 可选，默认为 4105462
source ~/.zshrc
```

**触发关键词**：API、接口、Apifox、OpenAPI、接口文档

**功能特性**：
- 接口查询 - 按路径、方法、模块搜索接口
- 接口详情 - 获取完整定义（自动解析 $ref）
- 统计分析 - 接口总数、模块分布、方法统计
- 文档导出 - 导出 JSON/Markdown 摘要

---

### codeup

阿里云云效 Codeup 代码仓库管理工具集，通过 Codeup API 管理代码仓库、分支、文件和合并请求。

**安装**：
```bash
npx skills add https://github.com/ABCFed/claude-marketplace/tree/main/skills/codeup
```

**准备**：
```bash
# 编辑 ~/.zshrc 或 ~/.bashrc
export YUNXIAO_ACCESS_TOKEN="your_codeup_token_here"
source ~/.zshrc
```

**触发关键词**：Codeup、代码仓库、分支、MR、合并请求、阿里云、云效

**功能特性**：
- 仓库管理 - 查询仓库详情、列出仓库
- 分支操作 - 创建、删除、列出分支
- 文件操作 - 读取、创建、更新、删除文件，对比代码差异
- MR 管理 - 创建合并请求、添加评论、列出 MR 和补丁集
- 组织管理 - 查询组织、部门、成员、角色信息

---

### jenkins-deploy

ABC Jenkins 项目发布技能，支持智能参数推断和交互式触发 Jenkins 构建。

**安装**：
```bash
npx skills add https://github.com/ABCFed/claude-marketplace/tree/main/skills/jenkins-deploy
```

**准备**：
```bash
# 编辑 ~/.zshrc 或 ~/.bashrc
export JENKINS_USER="your_jenkins_username"
export JENKINS_TOKEN="your_jenkins_api_token"
source ~/.zshrc
```

**触发关键词**：Jenkins、发布、部署、构建、Deploy、Build、CI/CD

**功能特性**：
- 智能参数推断 - 自动解析分支名、标签、TAPD ID
- 两阶段部署 - 触发构建后返回 JSON，支持后台监控
- 实时状态监控 - 构建进度可视化，完成后发送通知
- 项目过滤 - 根据 Git 仓库自动过滤相关项目
- 缓存机制 - 项目列表缓存，提高响应速度

---

### git-flow

ABC Git Flow 工作流助手，帮助使用 abc-git-flow 工具管理 git 分支。

**安装**：
```bash
npx skills add https://github.com/ABCFed/claude-marketplace/tree/main/skills/git-flow
```

**准备**：
```bash
# 安装 abc-git-flow
sudo curl https://cis-static-common.oss-cn-shanghai.aliyuncs.com/assets/abc-git-flow/git-abc-flow-install.sh

# 安装 Python 依赖
pip install requests
```

**触发关键词**：拉分支、创建分支、git flow、分支管理、feature、hotfix、tag

**功能特性**：
- 需求开发 - feature 分支管理（start/finish）
- 紧急修复 - hotfix（正式环境）/hotfix-g（灰度环境）管理
- Tag 管理 - 非交互式创建 tag（f/t/v/g/p 类型）
- MR 管理 - 非交互式创建 Merge Request
- RC 分支 - rc 分支管理（start/finish）
- 灰度发布 - gray 分支发布到 master

---

### modao-capture

墨刀原型稿抓取工具。自动从墨刀原型稿链接抓取所有页面、截图和批注，生成 Markdown 文档。

**安装**：
```bash
npx skills add https://github.com/ABCFed/claude-marketplace/tree/main/skills/modao-capture
```

**准备**：
```bash
# 编辑 ~/.zshrc 或 ~/.bashrc
export MODAO_CAPTURE_CHROME_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
source ~/.zshrc
```

**触发关键词**：墨刀、modao、原型稿、PRD、页面截图、批注

**功能特性**：
- 页面抓取 - 自动抓取原型稿所有页面
- 截图生成 - 生成高清页面截图
- 批注提取 - 提取页面批注内容
- Markdown 导出 - 生成结构化文档

---

### sls-trace-analyzer

SLS 日志追踪分析工具，根据 traceId 或 URL 查询阿里云日志服务 (SLS)，自动分析日志内容并定位代码问题。

**安装**：
```bash
npx skills add https://github.com/ABCFed/claude-marketplace/tree/main/skills/sls-trace-analyzer
```

**准备**：
```bash
# 方式一：配置 credentials 文件（安装时自动创建）
# 编辑 ~/.claude/skills/sls-trace-analyzer/credentials.json
{
  "sls_access_key_id": "your_access_key_id",
  "sls_access_key_secret": "your_access_key_secret"
}

# 方式二：使用环境变量
export SLS_ACCESS_KEY_ID="your_access_key_id"
export SLS_ACCESS_KEY_SECRET="your_access_key_secret"
```

> **注意**: skill 目录下已内置 `.venv` Python 虚拟环境（含 `requests` 等依赖），无需额外安装 Python 包。

**触发关键词**：traceId、SLS、日志查询、日志分析、链路追踪

**功能特性**：
- TraceId 查询 - 根据 traceId 查询完整调用链日志
- URL 模式 - 从请求 URL 自动解析环境、地域、时间戳，查询网关日志获取 traceId
- 多 Region 支持 - 上海/杭州双 Region，自动跨 Region 追踪
- 双 LogStore 查询 - 同时查询普通存储和长期存储，获取完整日志
- 根因分析 - 自动识别异常堆栈，结合代码定位问题根因
- 分析报告 - 生成结构化的日志分析报告，包含调用链路和修复建议

---

### tapd-bug-analyzer

TAPD Bug 单自动分析工具，从 Bug 链接出发，自动获取 Bug 详情并选择最优分析策略定位问题。

**安装**：
```bash
npx skills add https://github.com/ABCFed/claude-marketplace/tree/main/skills/tapd-bug-analyzer
```

**准备**：
```bash
# 需要 TAPD MCP Server 和 SLS 凭证（用于日志分析）
# 1. 确保 TAPD MCP Server 已配置
# 2. 确保 sls-trace-analyzer 已安装并配置凭证
```

**触发关键词**：TAPD Bug、Bug 分析、缺陷分析、Bug 定位

**功能特性**：
- Bug 详情获取 - 通过 TAPD MCP 自动获取 Bug 单详细信息
- 智能策略选择 - 根据 Bug 描述内容自动选择最优分析策略：
  - 策略 A：检测到 traceId，直接查询 SLS 日志分析
  - 策略 B：检测到请求 URL（含时间戳），通过网关日志反查 traceId
  - 策略 C：纯文字描述，基于关键词搜索代码定位问题
- 日志联动 - 与 sls-trace-analyzer 联动，自动完成日志查询和分析
- 代码定位 - 从异常堆栈或业务描述定位到具体代码位置
- 分析报告 - 生成包含 Bug 信息、调用链路、根因分析和修复建议的完整报告

## 目录结构

```
├── .claude-plugin/
│   └── marketplace.json          # 市场配置
├── skills/                       # 独立技能
│   ├── jenkins-deploy/           # Jenkins 发布技能
│   ├── git-flow/                 # Git Flow 工作流助手
│   ├── tapd/                     # TAPD 集成（从 plugins 迁移）
│   ├── apifox/                   # API 文档查询（从 plugins 迁移）
│   ├── codeup/                   # Codeup 仓库管理（从 plugins 迁移）
│   ├── modao-capture/            # 墨刀原型稿抓取
│   ├── sls-trace-analyzer/       # SLS 日志追踪分析
│   └── tapd-bug-analyzer/        # TAPD Bug 单自动分析
├── plugins/
│   └── abc-development-plugin/   # ABC 开发插件
└── docs/                         # 文档
```

## 贡献指南

欢迎贡献代码、文档或新插件！请参阅 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详情。

## 许可证

MIT License - 详见 [LICENSE](LICENSE)
