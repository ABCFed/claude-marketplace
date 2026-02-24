---
description: 初始化 abc-apifox（安装依赖并下载缓存）
---

## Context

- Skill 安装路径: skills/abc-apifox

## Your task

初始化 abc-apifox，按顺序执行以下步骤：

1. **安装 Python 依赖**（如果未安装）：
   ```bash
   pip3 install requests
   ```

2. **运行环境检查**（验证配置）：
   ```bash
   python skills/abc-apifox/scripts/check_env.py
   ```

3. **初始化缓存**（从 Apifox 下载最新文档）：
   ```bash
   python skills/abc-apifox/scripts/apifox.py refresh_oas
   ```

执行完成后，报告初始化结果（成功/失败、接口数量、模块数量等）。
