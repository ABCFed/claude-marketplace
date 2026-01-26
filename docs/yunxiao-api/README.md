# 云效 API 文档批量下载

批量下载云效官方 API 文档为 Markdown 格式。

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

```bash
# 下载所有文档
python scripts/download_docs.py

# 显示浏览器窗口（非无头模式）
python scripts/download_docs.py --headless false

# 指定输出目录
python scripts/download_docs.py --output ./api-docs

# 只下载组织管理文档
python scripts/download_docs.py --category organization

# 只下载代码管理文档
python scripts/download_docs.py --category code-management
```

## 输出目录结构

```
docs/
├── organization/       # 组织管理 API 文档
│   ├── 获取组织列表.md
│   └── ...
└── code-management/    # 代码管理 API 文档
    ├── 获取仓库列表.md
    └── ...
```

## 支持的 API 分类

### 组织管理 (Organization)
- 获取组织列表
- 获取组织详情
- 创建组织
- 更新组织
- 删除组织

### 代码管理 (Codeup)
- 代码仓库管理
- 分支管理
- 合并请求 (MR)
- 提交记录
- 文件操作
- 代码审查
- 流水线

## 依赖

- `playwright` - 浏览器自动化
- `python >= 3.8`
