#!/usr/bin/env python3
"""
云效 API 文档批量下载脚本

使用方法:
    python download_docs.py [--output-dir OUTPUT_DIR] [--headless]

功能:
    批量下载云效官方 API 文档为 Markdown 格式
    - 组织管理 API (organization)
    - 代码管理 API (codeup/code management)
"""

import argparse
import os
import re
import sys
import time
from pathlib import Path
from datetime import datetime

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("错误: 未安装 playwright。请运行: pip install playwright && playwright install")
    sys.exit(1)


# 云效文档基础 URL
DOC_BASE_URL = "https://help.aliyun.com/zh/yunxiao/developer-reference"

# 组织管理相关文档（基于云效官方文档目录 - 从菜单 DOM 提取）
ORGANIZATION_DOCS = [
    ("listorganizations", "ListOrganizations - 查询组织列表"),
    ("getuserbytoken", "GetUserByToken - 根据个人访问令牌查询对应用户信息"),
    ("query-the-list-of-organization-departments", "ListDepartments - 查询组织部门列表"),
    ("getdepartment-query-organization-department-information", "GetDepartment - 查询组织部门信息"),
    ("listdepartmentancestors-query-the-list-of-all-parent-departments-of-a-department-in-an-organization", "ListDepartmentAncestors - 查询组织内部门的所有父部门列表"),
    ("listmembers-query-the-list-of-organization-members", "ListMembers - 查询成员列表"),
    ("getmember-query-member-information", "GetMember - 查询成员信息"),
    ("readmemberbyuser-query-organization-member-information-user-id", "ReadMemberByUser - 查询成员信息"),
    ("searchmembers-search-for-a-list-of-organization-members", "SearchMembers - 搜索成员列表"),
    ("lists-query-the-list-of-organization-roles", "ListRoles - 查询组织角色列表"),
    ("getrole", "GetRole - 查询角色信息"),
]

# 代码管理相关文档（基于云效官方文档目录）
CODEUP_DOCS = [
    ("createreposition-creates-a-code-base", "CreateRepository - 创建代码库"),
    ("deletereposition-delete-code-base", "DeleteRepository - 删除代码库"),
    ("getrepository-query-the-code-base", "GetRepository - 查询代码库"),
    ("listrepositories-query-code-base-list", "ListRepositories - 查询代码库列表"),
    ("listtemplaterepositories-query-the-list-of-template-code-libraries", "ListTemplateRepositories - 查询模板代码库列表"),
    ("creategroup-creates-a-code-group", "CreateGroup - 创建代码组"),
    ("getnamespace-query-code-group-space-information", "GetNamespace - 查询代码组空间信息"),
    ("listnamespaces-query-the-code-group-space-list", "ListNamespaces - 查询代码组空间列表"),
    ("listgrouprepostions-query-the-list-of-code-libraries-under-a-code-group", "ListGroupRepositories - 查询代码组下的代码库列表"),
    ("createbranch-create-branch", "CreateBranch - 创建分支"),
    ("deletebranch-delete-branch", "DeleteBranch - 删除分支"),
    ("getbranch-query-branch-information", "GetBranch - 查询分支信息"),
    ("listbranches-query-the-list-of-branches", "ListBranches - 查询分支列表"),
    ("getcommit-query-commit-information", "GetCommit - 查询提交信息"),
    ("listcommits-query-the-submission-list", "ListCommits - 查询提交列表"),
    ("createcommitcomment", "CreateCommitComment - 给单个提交添加评论"),
    ("createfile", "CreateFile - 创建文件"),
    ("deletefile", "DeleteFile - 删除文件"),
    ("getfileblobs", "GetFileBlobs - 查询文件内容"),
    ("listfiles", "ListFiles - 查询文件树"),
    ("updatefile", "UpdateFile - 更新文件内容"),
    ("getfileblame-get-file-blame-information", "GetFileBlame - 获取文件 blame 信息"),
    ("commitmultiplefiles-multi-file-change-commit", "CommitMultipleFiles - 多文件变更提交"),
    ("createtag", "CreateTag - 创建标签"),
    ("deletetag", "DeleteTag - 删除标签"),
    ("listtags", "ListTags - 查询标签列表"),
    ("createprotectedbranch", "CreateProtectedBranch - 创建保护分支"),
    ("deleteprotectedbranch", "DeleteProtectedBranch - 移除保护分支"),
    ("getprotectedbranch", "GetProtectedBranch - 查询保护分支"),
    ("listprotectedbranches", "ListProtectedBranches - 查询保护分支列表"),
    ("updateprotectedbranch", "UpdateProtectedBranch - 更新保护分支"),
    ("createchangerequest-create-merge-request", "CreateChangeRequest - 创建合并请求"),
    ("closechangerequest-close-merge-request", "CloseChangeRequest - 关闭合并请求"),
    ("getchangerequest-query-merge-request", "GetChangeRequest - 查询合并请求"),
    ("attachlabelstochangerquest", "AttachLabelsToChangeRequest - 关联类标到合并请求"),
    ("getchangerequestlabels", "GetChangeRequestLabels - 获取合并请求的类标"),
    ("listchangerequests-query-the-list-of-merge-requests", "ListChangeRequests - 查询合并请求列表"),
    ("getchangerequesttree-queries-the-change-file-tree-for-merge-requests", "GetChangeRequestTree - 查询合并请求的变更文件树"),
    ("listchangerequestpatchsets-query-the-list-of-merge-request-versions", "ListChangeRequestPatchSets - 查询合并请求版本列表"),
    ("reviewchangerequest-review-merge-request", "ReviewChangeRequest - 评审合并请求"),
    ("updatechangerequest-update-merge-request-basic-information", "UpdateChangeRequest - 更新合并请求基本信息"),
    ("update-merge-request-stakeholders", "UpdateChangeRequestRelatedPerson - 更新合并请求干系人"),
    ("mergechangerequest-merge-merge-request", "MergeChangeRequest - 合并合并请求"),
    ("reopenchangerequest-reopen-merge-request", "ReopenChangeRequest - 重新打开合并请求"),
    ("getmergerequest-query-merge-request-old", "GetMergeRequest - 查询合并请求(旧)"),
    ("listmergerequests-query-the-list-of-merge-requests-old", "ListMergeRequests - 查询合并请求列表(旧)"),
    ("createchangerequestcomment", "CreateChangeRequestComment - 创建合并请求评论"),
    ("updatechangerequestcomment", "UpdateChangeRequestComment - 更新合并请求评论"),
    ("deletechangerequestcomment", "DeleteChangeRequestComment - 删除合并请求评论"),
    ("listmergerequestcomments", "ListMergeRequestComments - 查询评论列表"),
    ("getcompare", "GetCompare - 查询代码比较内容"),
    ("createcheckrun", "CreateCheckRun - 创建运行检查"),
    ("getcheckrun", "GetCheckRun - 查询运行检查"),
    ("listcheckruns", "ListCheckRuns - 查询运行检查列表"),
    ("updatecheckrun", "UpdateCheckRun - 更新运行检查"),
    ("createdeploykey", "CreateDeployKey - 创建部署密钥"),
    ("disabledeploykey", "DisableDeployKey - 禁用部署密钥"),
    ("enabledeploykey", "EnableDeployKey - 启动部署密钥"),
    ("createprojectlabel", "CreateProjectLabel - 创建项目类标"),
    ("getprojectlabels", "GetProjectLabels - 获取项目类标列表"),
    ("updateprojectlabel", "UpdateProjectLabel - 更新项目类标"),
    ("deleteprojectlabel", "DeleteProjectLabel - 删除项目类标"),
]


class YunxiaoDocDownloader:
    """云效 API 文档下载器"""

    def __init__(self, output_dir: str = "docs", headless: bool = True):
        self.output_dir = Path(output_dir)
        self.headless = headless
        self.browser = None
        self.context = None
        self._playwright = None

    def __enter__(self):
        """上下文管理器入口"""
        self._playwright = sync_playwright().start()
        self.browser = self._playwright.chromium.launch(headless=self.headless)
        self.context = self.browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器退出"""
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if self._playwright:
            self._playwright.stop()

    def extract_content_js(self, page) -> str:
        """使用 JavaScript 提取页面内容"""
        return page.evaluate("""
            () => {
                function extractTable(table) {
                    if (table.classList.contains('fixed-table')) return '';

                    const rows = [];
                    table.querySelectorAll('tr').forEach(tr => {
                        const cells = [];
                        tr.querySelectorAll('th, td').forEach(cell => {
                            const text = cell.innerText.trim().replace(/\\s+/g, ' ');
                            cells.push(text);
                        });
                        if (cells.length > 0) rows.push(cells);
                    });

                    if (rows.length === 0) return '';

                    let md = '';
                    const colCount = Math.max(...rows.map(r => r.length));
                    const widths = [];

                    for (let i = 0; i < colCount; i++) {
                        widths[i] = Math.max(3, ...rows.map(r => r[i]?.length || 0));
                    }

                    md += '| ' + rows[0].map((c, i) => c.padEnd(widths[i])).join(' | ') + ' |\\n';
                    md += '|-' + widths.map(w => '-'.repeat(w)).join('-|-') + '-|\\n';
                    for (let i = 1; i < rows.length; i++) {
                        const row = rows[i];
                        md += '| ' + row.map((c, j) => (c || '').padEnd(widths[j])).join(' | ') + ' |\\n';
                    }

                    return md + '\\n';
                }

                const content = document.querySelector('.aliyun-docs-content');
                if (!content) return '';

                let md = '';

                // 标题
                const h1 = content.querySelector('h1');
                if (h1) md += '# ' + h1.innerText.trim() + '\\n\\n';

                // 更新时间
                const updateTime = content.querySelector('.aliyun-docs-update-time');
                if (updateTime) md += '*更新时间：' + updateTime.innerText.trim() + '*\\n\\n';

                // 处理每个 section
                const sections = content.querySelectorAll('section');
                sections.forEach(section => {
                    const h2 = section.querySelector('h2');
                    if (h2) md += '## ' + h2.innerText.trim() + '\\n\\n';

                    // 段落（排除表格内的 p）
                    section.querySelectorAll('p').forEach(p => {
                        if (p.closest('table')) return;
                        const text = p.innerText.trim();
                        if (text && text.length > 5) md += text + '\\n\\n';
                    });

                    // 列表
                    section.querySelectorAll('ul').forEach(ul => {
                        ul.querySelectorAll('li').forEach(li => {
                            const text = li.innerText.trim();
                            if (text) md += '- ' + text + '\\n';
                        });
                        md += '\\n';
                    });

                    // 表格
                    section.querySelectorAll('table.table').forEach(table => {
                        md += extractTable(table);
                    });

                    // 代码块
                    section.querySelectorAll('pre').forEach(pre => {
                        const code = pre.innerText.trim();
                        if (code) md += '```\\n' + code + '\\n```\\n\\n';
                    });
                });

                return md;
            }
        """)

    def download_doc(self, url_path: str, title: str, category: str) -> dict:
        """下载单个文档页面"""
        url = f"{DOC_BASE_URL}/{url_path}"
        print(f"  {title}")

        page = self.context.new_page()

        try:
            response = page.goto(url, wait_until="domcontentloaded", timeout=60000)

            # 检查是否 404
            if response.status == 404 or "404" in page.title():
                return {"error": "404 Not Found", "url": url, "title": title}

            # 等待页面完全加载（包括内容渲染）
            page.wait_for_timeout(3000)

            # 检查内容是否存在
            content_check = page.evaluate("""
                () => {
                    const content = document.querySelector('.aliyun-docs-content');
                    if (!content) return { exists: false };
                    const text = content.innerText || '';
                    return { exists: true, length: text.length, hasH1: !!content.querySelector('h1') };
                }
            """)

            if not content_check.get("exists") or content_check.get("length", 0) < 100:
                return {"error": f"页面内容为空或过短 ({content_check.get('length', 0)} 字符)", "url": url, "title": title}

            # 提取内容
            content = self.extract_content_js(page)

            if content and len(content) > 100:
                return {
                    "url": url,
                    "category": category,
                    "title": title,
                    "content": content,
                    "downloaded_at": datetime.now().isoformat()
                }
            else:
                return {"error": f"无法提取有效内容 (提取了 {len(content)} 字符)", "url": url, "title": title}

        except Exception as e:
            return {"error": str(e), "url": url, "title": title}
        finally:
            page.close()

    def save_document(self, doc_data: dict) -> Path:
        """保存文档到文件"""
        category = doc_data.get("category", "unknown")
        title = doc_data.get("title", "unknown")

        # 生成文件名
        safe_title = re.sub(r'[<>:"/\\|?*]', "_", title)
        safe_title = re.sub(r'\s+', "-", safe_title)
        safe_title = safe_title[:100]

        # 创建分类目录
        category_dir = self.output_dir / category
        category_dir.mkdir(parents=True, exist_ok=True)

        # 保存文件
        file_path = category_dir / f"{safe_title}.md"
        content = doc_data.get("content", "")

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"# {title}\n\n")
            f.write(f"---\n")
            f.write(f"source: {doc_data.get('url', '')}\n")
            f.write(f"category: {category}\n")
            f.write(f"downloaded_at: {doc_data.get('downloaded_at', '')}\n")
            f.write(f"---\n\n")
            f.write(content)

        return file_path

    def download_all(self, docs: list, category: str) -> list:
        """下载所有文档"""
        results = []
        total = len(docs)

        for idx, (url_path, title) in enumerate(docs, 1):
            print(f"  [{idx}/{total}] ", end="", flush=True)

            try:
                doc_data = self.download_doc(url_path, title, category)

                if "error" not in doc_data:
                    file_path = self.save_document(doc_data)
                    print(f"✓ {file_path.name}")
                    results.append({
                        "status": "success",
                        "file": str(file_path),
                        "title": title
                    })
                else:
                    print(f"✗ {doc_data['error']}")
                    results.append({
                        "status": "failed",
                        "url": doc_data.get("url", ""),
                        "title": title,
                        "error": doc_data["error"]
                    })

            except Exception as e:
                print(f"✗ 错误: {e}")
                results.append({
                    "status": "error",
                    "title": title,
                    "error": str(e)
                })

            time.sleep(0.8)

        return results


def build_parser() -> argparse.ArgumentParser:
    """构建命令行参数解析器"""
    parser = argparse.ArgumentParser(
        description="云效 API 文档批量下载工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
    python download_docs.py                     # 下载所有文档
    python download_docs.py --headless false    # 显示浏览器窗口
    python download_docs.py --output ./docs     # 指定输出目录
    python download_docs.py --category organization
    python download_docs.py --category code-management
        """
    )

    parser.add_argument(
        "--output-dir", "-o",
        default="docs",
        help="输出目录 (默认: docs)"
    )

    parser.add_argument(
        "--headless",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="是否使用无头模式 (默认: True)"
    )

    parser.add_argument(
        "--category",
        choices=["organization", "code-management", "all"],
        default="all",
        help="选择要下载的文档分类"
    )

    return parser


def cmd_download(args):
    """下载命令处理"""
    output_dir = Path(args.output_dir)
    headless = args.headless
    category = args.category

    if category == "organization":
        docs = ORGANIZATION_DOCS
    elif category == "code-management":
        docs = CODEUP_DOCS
    else:
        docs = ORGANIZATION_DOCS + CODEUP_DOCS

    print(f"准备下载 {len(docs)} 个文档...")
    print(f"输出目录: {output_dir}")
    print(f"分类: {category}")
    print("-" * 60)

    with YunxiaoDocDownloader(output_dir=str(output_dir), headless=headless) as downloader:
        if category == "all":
            print(f"\n=== 组织管理 API ({len(ORGANIZATION_DOCS)}个) ===")
            org_results = downloader.download_all(ORGANIZATION_DOCS, "organization")

            print(f"\n=== 代码管理 API ({len(CODEUP_DOCS)}个) ===")
            code_results = downloader.download_all(CODEUP_DOCS, "code-management")

            results = org_results + code_results
        else:
            cat_name = "organization" if category == "organization" else "code-management"
            print(f"\n=== {cat_name} API ===")
            results = downloader.download_all(docs, cat_name)

    success = sum(1 for r in results if r["status"] == "success")
    failed = sum(1 for r in results if r["status"] != "success")

    print("\n" + "=" * 60)
    print(f"下载完成! 成功: {success}, 失败: {failed}")

    if failed > 0:
        print("\n失败的文档:")
        for r in results:
            if r["status"] != "success":
                print(f"  - {r.get('title', 'Unknown')}")

    return 0 if failed == 0 else 1


def main():
    """主入口"""
    parser = build_parser()
    args = parser.parse_args()
    sys.exit(cmd_download(args))


if __name__ == "__main__":
    main()
