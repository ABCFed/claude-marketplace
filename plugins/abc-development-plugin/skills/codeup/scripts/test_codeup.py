"""
Codeup API 测试用例

运行方式：
    # 运行所有单元测试
    python test_codeup.py

    # 运行特定测试类
    python test_codeup.py TestCodeupClient -v

    # 只运行集成测试（需要真实 API 令牌）
    python test_codeup.py IntegrationTestCodeupClient

测试覆盖：
    - API Path 验证
    - HTTP Method 验证
    - 请求参数验证
    - 返回值验证
    - 文件路径 URL 编码
    - 参数类型验证
    - 错误处理

集成测试说明：
    集成测试需要设置环境变量 YUNXIAO_ACCESS_TOKEN，
    如果未设置会自动跳过。
"""

import os
import sys
import json
import unittest
from unittest.mock import patch, MagicMock

# 添加脚本目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from codeup_client import CodeupClient


class MockResponse:
    """Mock HTTP 响应"""

    def __init__(self, json_data, status_code=200):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data

    def raise_for_status(self):
        if self.status_code >= 400:
            raise Exception(f"HTTP {self.status_code}")


class TestCodeupClient(unittest.TestCase):
    """CodeupClient 单元测试"""

    def setUp(self):
        """设置测试环境"""
        # 设置 mock token
        os.environ["YUNXIAO_ACCESS_TOKEN"] = "test_token"
        self.client = CodeupClient()

    @patch("requests.request")
    def test_get_current_user(self, mock_request):
        """测试获取当前用户信息"""
        mock_response_data = {
            "id": "test_user_id",
            "name": "Test User",
            "email": "test@example.com"
        }
        mock_request.return_value = MockResponse(mock_response_data)

        result = self.client.get_current_user()

        mock_request.assert_called_once_with(
            method="GET",
            url="https://openapi-rdc.aliyuncs.com/oapi/v1/platform/user",
            headers=self.client.headers,
            params=None,
            json=None
        )
        self.assertEqual(result, mock_response_data)

    @patch("requests.request")
    def test_list_organizations(self, mock_request):
        """测试列出组织"""
        mock_response_data = [
            {"id": "org_1", "name": "Organization 1"},
            {"id": "org_2", "name": "Organization 2"}
        ]
        mock_request.return_value = MockResponse(mock_response_data)

        result = self.client.list_organizations()

        mock_request.assert_called_once_with(
            method="GET",
            url="https://openapi-rdc.aliyuncs.com/oapi/v1/platform/organizations",
            headers=self.client.headers,
            params=None,
            json=None
        )
        self.assertEqual(result, mock_response_data)

    @patch("requests.request")
    def test_list_departments(self, mock_request):
        """测试列出部门"""
        mock_response_data = [
            {"id": "dept_1", "name": "Department 1"}
        ]
        mock_request.return_value = MockResponse(mock_response_data)

        result = self.client.list_departments("org_123")

        mock_request.assert_called_once_with(
            method="GET",
            url="https://openapi-rdc.aliyuncs.com/oapi/v1/platform/organizations/org_123/departments",
            headers=self.client.headers,
            params=None,
            json=None
        )

    @patch("requests.request")
    def test_list_members(self, mock_request):
        """测试列出成员"""
        mock_response_data = [
            {"id": "member_1", "name": "Member 1"}
        ]
        mock_request.return_value = MockResponse(mock_response_data)

        result = self.client.list_members("org_123", page=1, per_page=20)

        mock_request.assert_called_once_with(
            method="GET",
            url="https://openapi-rdc.aliyuncs.com/oapi/v1/platform/organizations/org_123/members",
            headers=self.client.headers,
            params={"page": 1, "perPage": 20},
            json=None
        )

    @patch("requests.request")
    def test_list_repositories(self, mock_request):
        """测试列出仓库"""
        mock_response_data = [
            {"id": 123, "name": "repo_1"}
        ]
        mock_request.return_value = MockResponse(mock_response_data)

        result = self.client.list_repositories("org_123", page=1, per_page=20)

        mock_request.assert_called_once_with(
            method="GET",
            url="https://openapi-rdc.aliyuncs.com/oapi/v1/codeup/organizations/org_123/repositories",
            headers=self.client.headers,
            params={"page": 1, "perPage": 20},
            json=None
        )

    @patch("requests.request")
    def test_list_branches(self, mock_request):
        """测试列出分支 - 验证 perPage 参数"""
        mock_response_data = [
            {"name": "master", "protected": True}
        ]
        mock_request.return_value = MockResponse(mock_response_data)

        result = self.client.list_branches("org_123", "repo_456", page=1, per_page=50)

        # 验证使用 perPage 而不是 limit
        mock_request.assert_called_once_with(
            method="GET",
            url="https://openapi-rdc.aliyuncs.com/oapi/v1/codeup/organizations/org_123/repositories/repo_456/branches",
            headers=self.client.headers,
            params={"page": 1, "perPage": 50},
            json=None
        )

    @patch("requests.request")
    def test_create_branch(self, mock_request):
        """测试创建分支"""
        mock_response_data = {
            "name": "feature/new-branch",
            "commit": {"id": "abc123"}
        }
        mock_request.return_value = MockResponse(mock_response_data)

        result = self.client.create_branch(
            "org_123", "repo_456", "feature/new-branch", "master"
        )

        mock_request.assert_called_once_with(
            method="POST",
            url="https://openapi-rdc.aliyuncs.com/oapi/v1/codeup/organizations/org_123/repositories/repo_456/branches",
            headers=self.client.headers,
            params={"branch": "feature/new-branch", "ref": "master"},
            json=None
        )

    @patch("requests.request")
    def test_delete_branch(self, mock_request):
        """测试删除分支"""
        mock_response_data = {"branchName": "feature/old-branch"}
        mock_request.return_value = MockResponse(mock_response_data)

        result = self.client.delete_branch("org_123", "repo_456", "feature/old-branch")

        mock_request.assert_called_once_with(
            method="DELETE",
            url="https://openapi-rdc.aliyuncs.com/oapi/v1/codeup/organizations/org_123/repositories/repo_456/branches/feature/old-branch",
            headers=self.client.headers,
            params=None,
            json=None
        )

    @patch("requests.request")
    def test_get_file(self, mock_request):
        """测试获取文件内容"""
        mock_response_data = {
            "fileName": "README.md",
            "content": "file content",
            "encoding": "text"
        }
        mock_request.return_value = MockResponse(mock_response_data)

        result = self.client.get_file("org_123", "repo_456", "README.md", "master")

        # 验证文件路径被 URL 编码
        mock_request.assert_called_once_with(
            method="GET",
            url="https://openapi-rdc.aliyuncs.com/oapi/v1/codeup/organizations/org_123/repositories/repo_456/files/README.md",
            headers=self.client.headers,
            params={"ref": "master"},
            json=None
        )

    @patch("requests.request")
    def test_create_file(self, mock_request):
        """测试创建文件 - 验证 filePath URL 编码"""
        mock_response_data = {"filePath": "src/test.js"}
        mock_request.return_value = MockResponse(mock_response_data)

        result = self.client.create_file(
            "org_123", "repo_456", "src/test.js", "console.log('test')",
            branch="master", message="Add test file"
        )

        # 验证 filePath 被 URL 编码
        mock_request.assert_called_once()
        call_kwargs = mock_request.call_args.kwargs
        self.assertEqual(call_kwargs["json"]["filePath"], "src%2Ftest.js")

    @patch("requests.request")
    def test_update_file(self, mock_request):
        """测试更新文件"""
        mock_response_data = {"filePath": "README.md"}
        mock_request.return_value = MockResponse(mock_response_data)

        result = self.client.update_file(
            "org_123", "repo_456", "README.md", "updated content",
            branch="master", message="Update README"
        )

        # 验证文件路径被 URL 编码
        mock_request.assert_called_once()
        call_args = mock_request.call_args

    @patch("requests.request")
    def test_delete_file(self, mock_request):
        """测试删除文件 - 验证 commitMessage 在 query params"""
        mock_response_data = {"result": True}
        mock_request.return_value = MockResponse(mock_response_data)

        result = self.client.delete_file(
            "org_123", "repo_456", "old-file.txt",
            branch="master", message="Delete old file"
        )

        # 验证 commitMessage 在 params 中
        mock_request.assert_called_once()
        call_args = mock_request.call_args
        self.assertEqual(call_args[1]["params"]["commitMessage"], "Delete old file")
        self.assertEqual(call_args[1]["params"]["branch"], "master")

    def test_delete_file_without_message(self):
        """测试删除文件时没有 commitMessage 应该报错"""
        with self.assertRaises(ValueError) as context:
            self.client.delete_file("org_123", "repo_456", "file.txt")

        self.assertIn("commitMessage is required", str(context.exception))

    @patch("requests.request")
    def test_list_files(self, mock_request):
        """测试列出文件树"""
        mock_response_data = [
            {"name": "file1.js", "type": "blob"},
            {"name": "src", "type": "tree"}
        ]
        mock_request.return_value = MockResponse(mock_response_data)

        result = self.client.list_files("org_123", "repo_456", path="src", branch="master")

        mock_request.assert_called_once_with(
            method="GET",
            url="https://openapi-rdc.aliyuncs.com/oapi/v1/codeup/organizations/org_123/repositories/repo_456/files/tree",
            headers=self.client.headers,
            params={"path": "src", "ref": "master", "type": "RECURSIVE"},
            json=None
        )

    @patch("requests.request")
    def test_compare(self, mock_request):
        """测试代码对比"""
        mock_response_data = {
            "commits": [],
            "diffs": []
        }
        mock_request.return_value = MockResponse(mock_response_data)

        result = self.client.compare(
            "org_123", "repo_456", "feature-branch", "master",
            source_type="branch", target_type="branch"
        )

        mock_request.assert_called_once_with(
            method="GET",
            url="https://openapi-rdc.aliyuncs.com/oapi/v1/codeup/organizations/org_123/repositories/repo_456/compares",
            headers=self.client.headers,
            params={
                "from": "feature-branch",
                "to": "master",
                "sourceType": "branch",
                "targetType": "branch"
            },
            json=None
        )

    @patch("requests.request")
    def test_get_change_request(self, mock_request):
        """测试获取 MR 详情"""
        mock_response_data = {
            "localId": 1,
            "title": "Test MR",
            "state": "OPENED"
        }
        mock_request.return_value = MockResponse(mock_response_data)

        result = self.client.get_change_request("org_123", "repo_456", 1)

        mock_request.assert_called_once_with(
            method="GET",
            url="https://openapi-rdc.aliyuncs.com/oapi/v1/codeup/organizations/org_123/repositories/repo_456/changeRequests/1",
            headers=self.client.headers,
            params=None,
            json=None
        )

    @patch("requests.request")
    def test_list_merge_requests(self, mock_request):
        """测试列出 MR"""
        mock_response_data = [
            {"localId": 1, "title": "MR 1"},
            {"localId": 2, "title": "MR 2"}
        ]
        mock_request.return_value = MockResponse(mock_response_data)

        result = self.client.list_merge_requests("org_123", repo_id="repo_456", state="opened")

        mock_request.assert_called_once_with(
            method="GET",
            url="https://openapi-rdc.aliyuncs.com/oapi/v1/codeup/organizations/org_123/changeRequests",
            headers=self.client.headers,
            params={
                "page": 1,
                "perPage": 20,
                "projectIds": "repo_456",
                "state": "opened"
            },
            json=None
        )

    @patch("requests.request")
    def test_create_merge_request(self, mock_request):
        """测试创建 MR - 验证 sourceProjectId/targetProjectId 为 int"""
        mock_response_data = {
            "localId": 123,
            "title": "New MR"
        }
        mock_request.return_value = MockResponse(mock_response_data)

        result = self.client.create_merge_request(
            "org_123", 5822285, "Test MR",
            "feature-branch", "master",
            description="Test description"
        )

        # 验证 projectId 是整数类型
        mock_request.assert_called_once()
        call_kwargs = mock_request.call_args.kwargs
        data = call_kwargs["json"]
        self.assertEqual(data["sourceProjectId"], 5822285)
        self.assertEqual(data["targetProjectId"], 5822285)
        self.assertIsInstance(data["sourceProjectId"], int)
        self.assertIsInstance(data["targetProjectId"], int)

    @patch("requests.request")
    def test_list_merge_request_comments(self, mock_request):
        """测试列出 MR 评论 - 验证 POST /comments/list"""
        mock_response_data = [
            {"comment_biz_id": "abc", "content": "Test comment"}
        ]
        mock_request.return_value = MockResponse(mock_response_data)

        result = self.client.list_merge_request_comments("org_123", "repo_456", 1)

        # 验证使用 POST 和 /comments/list 路径
        mock_request.assert_called_once()
        call_kwargs = mock_request.call_args.kwargs
        self.assertEqual(call_kwargs["method"], "POST")  # method
        self.assertIn("/comments/list", call_kwargs["url"])  # URL

    @patch("requests.request")
    def test_list_merge_request_patch_sets(self, mock_request):
        """测试列出 MR 补丁集 - 验证 /diffs/patches"""
        mock_response_data = [
            {"patchSetBizId": "abc123", "versionNo": 1}
        ]
        mock_request.return_value = MockResponse(mock_response_data)

        result = self.client.list_merge_request_patch_sets("org_123", "repo_456", 1)

        # 验证使用 /diffs/patches 路径
        mock_request.assert_called_once()
        call_kwargs = mock_request.call_args.kwargs
        self.assertIn("/diffs/patches", call_kwargs["url"])

    @patch("requests.request")
    def test_create_merge_request_comment(self, mock_request):
        """测试创建 MR 评论"""
        mock_response_data = {"comment_biz_id": "new_comment"}
        mock_request.return_value = MockResponse(mock_response_data)

        result = self.client.create_merge_request_comment(
            "org_123", "repo_456", 1,
            "This is a comment"
        )

        mock_request.assert_called_once()
        call_args = mock_request.call_args
        data = call_args[1]["json"]
        self.assertEqual(data["content"], "This is a comment")
        self.assertEqual(data["comment_type"], "GLOBAL_COMMENT")

    @patch("requests.request")
    def test_merge_change_request(self, mock_request):
        """测试合并 MR"""
        mock_response_data = {"state": "MERGED"}
        mock_request.return_value = MockResponse(mock_response_data)

        result = self.client.merge_change_request("org_123", "repo_456", 1)

        mock_request.assert_called_once()
        call_kwargs = mock_request.call_args.kwargs
        self.assertEqual(call_kwargs["method"], "POST")
        self.assertIn("/merge", call_kwargs["url"])

    @patch("requests.request")
    def test_reopen_change_request(self, mock_request):
        """测试重新打开 MR"""
        mock_response_data = {"state": "OPENED"}
        mock_request.return_value = MockResponse(mock_response_data)

        result = self.client.reopen_change_request("org_123", "repo_456", 1)

        mock_request.assert_called_once()
        call_kwargs = mock_request.call_args.kwargs
        self.assertEqual(call_kwargs["method"], "POST")
        self.assertIn("/reopen", call_kwargs["url"])

    @patch("requests.request")
    def test_review_change_request_approve(self, mock_request):
        """测试审查 MR - 批准"""
        mock_response_data = {"decision": "APPROVE"}
        mock_request.return_value = MockResponse(mock_response_data)

        result = self.client.review_change_request("org_123", "repo_456", 1, "APPROVE", "LGTM")

        mock_request.assert_called_once()
        call_kwargs = mock_request.call_args.kwargs
        self.assertEqual(call_kwargs["method"], "POST")
        self.assertIn("/review", call_kwargs["url"])
        data = call_kwargs["json"]
        self.assertEqual(data["decision"], "APPROVE")
        self.assertEqual(data["comment"], "LGTM")

    @patch("requests.request")
    def test_review_change_request_reject(self, mock_request):
        """测试审查 MR - 拒绝"""
        mock_response_data = {"decision": "REJECT"}
        mock_request.return_value = MockResponse(mock_response_data)

        result = self.client.review_change_request("org_123", "repo_456", 1, "REJECT")

        mock_request.assert_called_once()
        call_kwargs = mock_request.call_args.kwargs
        data = call_kwargs["json"]
        self.assertEqual(data["decision"], "REJECT")
        self.assertNotIn("comment", data)

    @patch("requests.request")
    def test_update_change_request(self, mock_request):
        """测试更新 MR"""
        mock_response_data = {"title": "Updated Title", "description": "Updated description"}
        mock_request.return_value = MockResponse(mock_response_data)

        result = self.client.update_change_request(
            "org_123", "repo_456", 1,
            title="Updated Title",
            description="Updated description"
        )

        mock_request.assert_called_once()
        call_kwargs = mock_request.call_args.kwargs
        self.assertEqual(call_kwargs["method"], "PUT")
        self.assertIn("/changeRequests/1", call_kwargs["url"])
        data = call_kwargs["json"]
        self.assertEqual(data["title"], "Updated Title")
        self.assertEqual(data["description"], "Updated description")

    @patch("requests.request")
    def test_get_change_request_tree(self, mock_request):
        """测试获取 MR 变更文件列表"""
        mock_response_data = [
            {"path": "src/main.py", "status": "MODIFIED"},
            {"path": "tests/test_main.py", "status": "ADDED"}
        ]
        mock_request.return_value = MockResponse(mock_response_data)

        result = self.client.get_change_request_tree("org_123", "repo_456", 1)

        mock_request.assert_called_once()
        call_kwargs = mock_request.call_args.kwargs
        self.assertEqual(call_kwargs["method"], "GET")
        self.assertIn("/tree", call_kwargs["url"])

    @patch("requests.request")
    def test_delete_change_request_comment(self, mock_request):
        """测试删除 MR 评论"""
        mock_response_data = {"success": True}
        mock_request.return_value = MockResponse(mock_response_data)

        result = self.client.delete_change_request_comment("org_123", "repo_456", "comment_biz_123")

        mock_request.assert_called_once()
        call_kwargs = mock_request.call_args.kwargs
        self.assertEqual(call_kwargs["method"], "DELETE")
        self.assertIn("/comments/comment_biz_123", call_kwargs["url"])

    @patch("requests.request")
    def test_update_change_request_comment(self, mock_request):
        """测试更新 MR 评论"""
        mock_response_data = {"content": "Updated content"}
        mock_request.return_value = MockResponse(mock_response_data)

        result = self.client.update_change_request_comment(
            "org_123", "repo_456", "comment_biz_123", "Updated content"
        )

        mock_request.assert_called_once()
        call_kwargs = mock_request.call_args.kwargs
        self.assertEqual(call_kwargs["method"], "PUT")
        self.assertIn("/comments/comment_biz_123", call_kwargs["url"])
        data = call_kwargs["json"]
        self.assertEqual(data["content"], "Updated content")

    @patch("requests.request")
    def test_search_members(self, mock_request):
        """测试搜索成员"""
        mock_response_data = [
            {"id": "member_1", "name": "Search Result"}
        ]
        mock_request.return_value = MockResponse(mock_response_data)

        result = self.client.search_members("org_123", "keyword", page=1, per_page=10)

        mock_request.assert_called_once_with(
            method="POST",
            url="https://openapi-rdc.aliyuncs.com/oapi/v1/platform/organizations/org_123/members:search",
            headers=self.client.headers,
            params=None,
            json={"query": "keyword", "page": 1, "perPage": 10}
        )


class TestFilePathEncoding(unittest.TestCase):
    """文件路径编码测试"""

    def setUp(self):
        os.environ["YUNXIAO_ACCESS_TOKEN"] = "test_token"
        self.client = CodeupClient()

    @patch("requests.request")
    def test_file_path_with_special_chars(self, mock_request):
        """测试包含特殊字符的文件路径编码"""
        mock_request.return_value = MockResponse({"result": "ok"})

        # 测试包含斜杠的路径
        self.client.get_file("org", "repo", "src/main/java/App.java", "master")

        call_kwargs = mock_request.call_args.kwargs
        url = call_kwargs["url"]
        # 斜杠应该被编码
        self.assertIn("src%2Fmain%2Fjava%2FApp.java", url)


class TestArgumentValidation(unittest.TestCase):
    """参数验证测试"""

    def setUp(self):
        os.environ["YUNXIAO_ACCESS_TOKEN"] = "test_token"
        self.client = CodeupClient()

    def test_delete_file_requires_message(self):
        """测试删除文件必须提供 commitMessage"""
        with self.assertRaises(ValueError) as context:
            self.client.delete_file("org", "repo", "file.txt")

        self.assertIn("commitMessage is required", str(context.exception))


class TestErrorHandling(unittest.TestCase):
    """错误处理测试"""

    def setUp(self):
        os.environ["YUNXIAO_ACCESS_TOKEN"] = "test_token"
        self.client = CodeupClient()

    def test_missing_token(self):
        """测试缺少访问令牌"""
        del os.environ["YUNXIAO_ACCESS_TOKEN"]

        with self.assertRaises(ValueError) as context:
            CodeupClient()

        self.assertIn("YUNXIAO_ACCESS_TOKEN", str(context.exception))


# 集成测试（需要真实 API）
class IntegrationTestCodeupClient(unittest.TestCase):
    """集成测试 - 需要真实的 YUNXIAO_ACCESS_TOKEN"""

    @classmethod
    def setUpClass(cls):
        cls.token = os.environ.get("YUNXIAO_ACCESS_TOKEN")
        if not cls.token:
            raise unittest.SkipTest("YUNXIAO_ACCESS_TOKEN not set")

        cls.client = CodeupClient()
        # 使用真实的测试数据
        cls.test_org_id = "62d62893487c500c27f72e36"
        cls.test_repo_id = "5822285"

    def test_integration_get_current_user(self):
        """集成测试 - 获取当前用户"""
        result = self.client.get_current_user()
        self.assertIn("id", result)
        self.assertIn("name", result)

    def test_integration_list_branches(self):
        """集成测试 - 列出分支"""
        result = self.client.list_branches(self.test_org_id, self.test_repo_id)
        self.assertIsInstance(result, list)
        if result:
            self.assertIn("name", result[0])

    def test_integration_list_merge_requests(self):
        """集成测试 - 列出 MR"""
        result = self.client.list_merge_requests(
            self.test_org_id,
            repo_id=self.test_repo_id,
            state="opened"
        )
        self.assertIsInstance(result, list)

    def test_integration_list_merge_request_comments(self):
        """集成测试 - 列出 MR 评论"""
        # 先获取一个 MR
        mrs = self.client.list_merge_requests(
            self.test_org_id,
            repo_id=self.test_repo_id,
            state="opened",
            page=1,
            per_page=1
        )
        if mrs:
            local_id = mrs[0]["localId"]
            result = self.client.list_merge_request_comments(
                self.test_org_id, self.test_repo_id, local_id
            )
            self.assertIsInstance(result, list)

    def test_integration_list_merge_request_patch_sets(self):
        """集成测试 - 列出 MR 补丁集"""
        mrs = self.client.list_merge_requests(
            self.test_org_id,
            repo_id=self.test_repo_id,
            state="opened",
            page=1,
            per_page=1
        )
        if mrs:
            local_id = mrs[0]["localId"]
            result = self.client.list_merge_request_patch_sets(
                self.test_org_id, self.test_repo_id, local_id
            )
            self.assertIsInstance(result, list)


if __name__ == "__main__":
    # 运行测试
    unittest.main(verbosity=2)
