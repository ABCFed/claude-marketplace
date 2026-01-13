# 贡献指南

感谢您对 ABC Claude Code Plugin Marketplace 项目的关注！我们欢迎并感谢社区贡献，包括新插件开发、文档改进、Bug 修复等功能增强。

## 目录

- [贡献方式](#贡献方式)
- [新建插件](#新建插件)
- [扩展现有插件](#扩展现有插件)
- [提交规范](#提交规范)
- [本地测试](#本地测试)
- [行为准则](#行为准则)
- [许可证](#许可证)

## 贡献方式

### 报告问题
- 使用 GitHub Issues 报告 Bug 或提出功能建议
- 描述问题时请提供详细的重现步骤和环境信息
- 搜索现有问题，避免重复提交

### 提交代码
- Fork 本仓库并创建分支进行开发
- 遵循项目代码规范
- 确保所有测试通过后提交 Pull Request

### 完善文档
- 改进现有文档的清晰度和完整性
- 添加新功能的使用示例
- 翻译文档到其他语言

---

## 新建插件

本项目使用 `plugin-development` 插件辅助开发，按照以下步骤创建新插件。

### 步骤 1：安装开发工具

```bash
# 在 Claude Code 中添加插件市场
/plugin marketplace add https://github.com/ABCFed/claude-marketplace

# 安装插件开发工具
/plugin install plugin-development@abc-claude-plugin-marketplace
```

### 步骤 2：初始化插件

```bash
# 创建新插件（替换 your-plugin-name 为你的插件名）
/plugin-development:init your-plugin-name
```

这将在 `plugins/` 目录下创建插件基础结构：

```
plugins/your-plugin-name/
├── .claude-plugin/
│   └── plugin.json          # 插件清单文件
├── README.md                 # 插件说明文档
├── commands/                 # 斜杠命令（可選）
├── agents/                   # 子代理（可選）
├── skills/                   # 技能模块（可選）
└── hooks/                    # 事件钩子（可選）
```

### 步骤 3：编辑插件清单

编辑 `.claude-plugin/plugin.json`，配置插件元数据：

```json
{
  "name": "your-plugin-name",
  "version": "0.0.1",
  "description": "插件简短描述",
  "author": {
    "name": "Your Name",
    "email": "your@email.com"
  },
  "license": "MIT",
  "keywords": ["keyword1", "keyword2"]
}
```

### 步骤 4：添加组件

根据需要添加组件：

```bash
# 添加斜杠命令
/plugin-development:add-command your-command "命令描述"

/plugin-development:add-skill your-skill "技能描述"

/plugin-development:add-agent your-agent "子代理描述"

/plugin-development:add-hook "pre-commit" "*.py"
```

### 步骤 5：验证结构

```bash
/plugin-development:validate
```

此命令会检查插件结构是否符合规范。

### 步骤 6：本地测试

```bash
/plugin-development:test-local
```

---

## 扩展现有插件

以在 `abc-development-plugin` 中添加新 Skill 为例。

### 步骤 1：进入插件目录

```bash
cd plugins/abc-development-plugin
```

### 步骤 2：添加新 Skill

```bash
/plugin-development:add-skill your-skill "Skill 描述"
```

这将创建以下结构：

```
skills/your-skill/
├── SKILL.md                  # Skill 说明文档
└── references/               # 参考文档目录（可选）
    └── features.md
```

### 步骤 3：编写 Skill 文档

编辑 `skills/your-skill/SKILL.md`，添加 Skill 的使用说明：

```markdown
---
name: your-skill
description: 简短的 Skill 描述，说明做什么以及何时使用
---

# Your Skill

此处填写 Skill 的详细使用说明...
```

### 步骤 4：验证并测试

插件会自动发现 `skills/` 目录下的技能，无需在 `plugin.json` 中额外配置。

```bash
/plugin-development:validate
```

---

## 提交规范

### Git 提交信息格式

```
<type>(<scope>): <subject>
```

**类型说明**：
- `feat` - 新功能
- `fix` - Bug 修复
- `docs` - 文档更新
- `style` - 代码格式调整
- `refactor` - 重构
- `test` - 测试相关
- `chore` - 构建或辅助工具更新

**示例**：

```
feat(skill): 添加 API 文档查询功能

- 支持按路径搜索接口
- 支持方法筛选
- 返回完整的接口定义

Closes #123
```

### Pull Request

1. 确保代码通过所有检查
2. 填写 PR 模板中的所有必填项
3. 保持 PR 专注于单一功能
4. 及时响应审查意见

---

## 本地测试

### 方式一：使用开发命令

```bash
/plugin marketplace add ./plugins/your-plugin-name
/plugin install your-plugin-name
```

### 方式二：使用 test-local 命令

```bash
/plugin-development:test-local
```

---

## 行为准则

请尊重所有贡献者，创建一个包容、友好的社区环境。

- 使用友好和包容性的语言
- 尊重不同的观点和经验
- 接受建设性批评
- 关注对社区最有利的事情

---

## 许可证

通过贡献您的代码，您同意根据 MIT 许可证分发您的贡献。

---

## 联系方式

- GitHub Issues: 问题反馈和功能建议
- GitHub Discussions: 讨论和交流

感谢您的贡献！
