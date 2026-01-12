# ABC Claude Code Plugin Marketplace

中文 | [English](./README_EN.md)

本仓库托管了 ABC 团队的 Claude Code 插件市场。

## abc-development-plugin

ABC 敏捷研发管理平台集成插件，通过 TAPD API 实现研发全流程管理。

### 功能特性

- **需求管理** - 查询、创建、更新需求
- **缺陷管理** - 管理缺陷生命周期
- **任务管理** - 任务 CRUD 操作
- **迭代管理** - Sprint/迭代管理
- **测试用例** - 测试用例管理
- **Wiki 管理** - 创建和更新 Wiki 文档
- **评论和工时** - 管理评论、记录工时
- **关联关系** - 需求与缺陷关联

## 快速开始

### 安装插件市场

```bash
# 启动 Claude Code
claude

# 添加本地插件市场
/plugin marketplace add https://github.com/ABCFed/claude-marketplace

# 安装 abc-development-plugin
/plugin install abc-development-plugin@abc-claude-plugin-marketplace
```

### 使用插件

安装后，tapd-skill 会自动激活。当您提到 TAPD、需求、缺陷、任务、迭代等关键词时，Claude 将自动使用该技能。

## 配置环境变量

使用 TAPD API 需要配置 `TAPD_ACCESS_TOKEN` 环境变量。

### 获取 Access Token

1. 登录 [TAPD](https://www.tapd.cn/)
2. 进入「个人设置」→「个人令牌」
3. 点击「创建个人令牌」
4. 复制生成的 Token

### 配置环境变量

编辑 `~/.zshrc` 或 `~/.bashrc`：

```bash
export TAPD_ACCESS_TOKEN="your_token_here"
```

使配置生效：

```bash
source ~/.zshrc  # 或 source ~/.bashrc
```

### 验证配置

```bash
echo $TAPD_ACCESS_TOKEN
# 应该显示您的 Token
```

## 目录结构

```
├── .claude-plugin/
│   └── marketplace.json          # 市场配置
├── plugins/
│   └── abc-development-plugin/   # ABC 开发插件
└── docs/                         # 文档
```

## 许可证

MIT License - 详见 [LICENSE](LICENSE)
