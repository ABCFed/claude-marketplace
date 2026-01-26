"""
AlibabaCloud DevOps (云效/Codeup) API Client
"""

import os
import json
import requests


# Environment variable names
ENV_ACCESS_TOKEN = "YUNXIAO_ACCESS_TOKEN"

# API Base URL
BASE_URL = "https://openapi-rdc.aliyuncs.com"


def check_env_vars():
    """Check if required environment variables are set"""
    missing = []
    if not os.environ.get(ENV_ACCESS_TOKEN):
        missing.append(ENV_ACCESS_TOKEN)
    return missing


def get_env_check_message():
    """Get environment check message"""
    missing = check_env_vars()
    if missing:
        return f"Error: Missing environment variables: {', '.join(missing)}"
    return None


class CodeupClient:
    """AlibabaCloud DevOps API Client"""

    def __init__(self):
        """Initialize client with access token from environment"""
        self.access_token = os.environ.get(ENV_ACCESS_TOKEN)
        if not self.access_token:
            raise ValueError(f"Environment variable {ENV_ACCESS_TOKEN} is not set")
        self.headers = {
            "x-yunxiao-token": self.access_token,
            "Content-Type": "application/json"
        }

    def _make_request(self, method: str, endpoint: str, params: dict = None, data: dict = None) -> dict:
        """Make HTTP request to API"""
        url = f"{BASE_URL}{endpoint}"
        response = requests.request(
            method=method,
            url=url,
            headers=self.headers,
            params=params,
            json=data
        )
        response.raise_for_status()
        return response.json()

    # ==================== User & Organization ====================

    def get_current_user(self) -> dict:
        """Get current user information"""
        return self._make_request("GET", "/oapi/v1/platform/user")

    def list_organizations(self) -> dict:
        """List organizations the user belongs to"""
        return self._make_request("GET", "/oapi/v1/platform/organizations")

    def list_departments(self, org_id: str, parent_id: str = None) -> dict:
        """List departments in organization

        Args:
            org_id: Organization ID
            parent_id: Parent department ID (optional)
        """
        params = {}
        if parent_id:
            params["parentId"] = parent_id
        return self._make_request(
            "GET",
            f"/oapi/v1/platform/organizations/{org_id}/departments",
            params=params if params else None
        )

    def get_department(self, org_id: str, dept_id: str) -> dict:
        """Get department details"""
        return self._make_request("GET", f"/oapi/v1/platform/organizations/{org_id}/departments/{dept_id}")

    def list_members(
        self,
        org_id: str,
        page: int = 1,
        per_page: int = 100,
    ) -> list:
        """List organization members

        Args:
            org_id: Organization ID
            page: Current page (default: 1)
            per_page: Items per page, 1-100 (default: 100)
        """
        return self._make_request(
            "GET",
            f"/oapi/v1/platform/organizations/{org_id}/members",
            params={"page": page, "perPage": per_page}
        )

    def get_organization_member(self, org_id: str, member_id: str) -> dict:
        """Get organization member details

        Args:
            org_id: Organization ID
            member_id: Member ID
        """
        return self._make_request(
            "GET",
            f"/oapi/v1/platform/organizations/{org_id}/members/{member_id}"
        )

    def search_members(self, org_id: str, query: str, page: int = 1, per_page: int = 100) -> dict:
        """Search organization members

        Args:
            org_id: Organization ID
            query: Search query
            page: Page number (default: 1)
            per_page: Items per page (default: 100)
        """
        return self._make_request(
            "POST",
            f"/oapi/v1/platform/organizations/{org_id}/members:search",
            data={"query": query, "page": page, "perPage": per_page}
        )

    def list_roles(self, org_id: str) -> dict:
        """List organization roles"""
        return self._make_request("GET", f"/oapi/v1/platform/organizations/{org_id}/roles")

    # ==================== Repository ====================

    def get_repository(self, org_id: str, repo_id: str) -> dict:
        """Get repository details"""
        return self._make_request(
            "GET",
            f"/oapi/v1/codeup/organizations/{org_id}/repositories/{repo_id}"
        )

    def list_repositories(self, org_id: str, page: int = 1, per_page: int = 20,
                          order_by: str = None, sort: str = None,
                          search: str = None, archived: bool = None) -> dict:
        """List repositories in organization

        Args:
            org_id: Organization ID
            page: Page number (default: 1)
            per_page: Items per page, 1-100 (default: 20)
            order_by: Sort field - created_at, name, path, last_activity_at
            sort: Sort order - asc, desc (default: desc)
            search: Search keyword for repository path
            archived: Filter by archived status
        """
        params = {"page": page, "perPage": per_page}
        if order_by:
            params["orderBy"] = order_by
        if sort:
            params["sort"] = sort
        if search:
            params["search"] = search
        if archived is not None:
            params["archived"] = archived
        return self._make_request(
            "GET",
            f"/oapi/v1/codeup/organizations/{org_id}/repositories",
            params=params
        )

    # ==================== Branch ====================

    def get_branch(self, org_id: str, repo_id: str, branch_name: str) -> dict:
        """Get branch details"""
        return self._make_request(
            "GET",
            f"/oapi/v1/codeup/organizations/{org_id}/repositories/{repo_id}/branches/{branch_name}"
        )

    def create_branch(self, org_id: str, repo_id: str, branch_name: str, source_branch: str) -> dict:
        """Create a new branch

        Args:
            org_id: Organization ID
            repo_id: Repository ID
            branch_name: New branch name
            source_branch: Source branch/tag/commit (e.g., 'master' or 'refs/tags/v1.0')
        """
        return self._make_request(
            "POST",
            f"/oapi/v1/codeup/organizations/{org_id}/repositories/{repo_id}/branches",
            params={"branch": branch_name, "ref": source_branch}
        )

    def delete_branch(self, org_id: str, repo_id: str, branch_name: str) -> dict:
        """Delete a branch"""
        return self._make_request(
            "DELETE",
            f"/oapi/v1/codeup/organizations/{org_id}/repositories/{repo_id}/branches/{branch_name}"
        )

    def list_branches(self, org_id: str, repo_id: str, page: int = 1, per_page: int = 20) -> dict:
        """List branches in repository"""
        return self._make_request(
            "GET",
            f"/oapi/v1/codeup/organizations/{org_id}/repositories/{repo_id}/branches",
            params={"page": page, "perPage": per_page}
        )

    # ==================== File ====================

    def get_file(self, org_id: str, repo_id: str, file_path: str, branch: str = "master") -> dict:
        """Get file content

        Args:
            org_id: Organization ID
            repo_id: Repository ID
            file_path: File path in repository
            branch: Branch name (default: master)
        """
        # URL encode the file path
        encoded_path = requests.utils.quote(file_path, safe="")
        return self._make_request(
            "GET",
            f"/oapi/v1/codeup/organizations/{org_id}/repositories/{repo_id}/files/{encoded_path}",
            params={"ref": branch}
        )

    def create_file(self, org_id: str, repo_id: str, file_path: str, content: str,
                    branch: str = "master", message: str = None, encoding: str = "text") -> dict:
        """Create a new file

        Args:
            org_id: Organization ID
            repo_id: Repository ID
            file_path: File path in repository
            content: File content
            branch: Branch name (default: master)
            message: Commit message
            encoding: Content encoding (default: text, can be base64)
        """
        # URL encode the file path
        encoded_path = requests.utils.quote(file_path, safe="")
        data = {
            "filePath": encoded_path,
            "branch": branch,
            "content": content,
            "encoding": encoding
        }
        if message:
            data["commitMessage"] = message
        return self._make_request(
            "POST",
            f"/oapi/v1/codeup/organizations/{org_id}/repositories/{repo_id}/files",
            data=data
        )

    def update_file(self, org_id: str, repo_id: str, file_path: str, content: str,
                    branch: str = "master", message: str = None, encoding: str = "text") -> dict:
        """Update an existing file

        Args:
            org_id: Organization ID
            repo_id: Repository ID
            file_path: File path in repository
            content: File content
            branch: Branch name (default: master)
            message: Commit message
            encoding: Content encoding (default: text, can be base64)
        """
        # URL encode the file path
        encoded_path = requests.utils.quote(file_path, safe="")
        data = {
            "branch": branch,
            "content": content,
            "encoding": encoding
        }
        if message:
            data["commitMessage"] = message
        return self._make_request(
            "PUT",
            f"/oapi/v1/codeup/organizations/{org_id}/repositories/{repo_id}/files/{encoded_path}",
            data=data
        )

    def delete_file(self, org_id: str, repo_id: str, file_path: str,
                    branch: str = "master", message: str = None) -> dict:
        """Delete a file

        Args:
            org_id: Organization ID
            repo_id: Repository ID
            file_path: File path in repository
            branch: Branch name (default: master)
            message: Commit message (required)
        """
        if not message:
            raise ValueError("commitMessage is required for deleting a file")
        # URL encode the file path
        encoded_path = requests.utils.quote(file_path, safe="")
        params = {"branch": branch, "commitMessage": message}
        return self._make_request(
            "DELETE",
            f"/oapi/v1/codeup/organizations/{org_id}/repositories/{repo_id}/files/{encoded_path}",
            params=params
        )

    def list_files(self, org_id: str, repo_id: str, path: str = "",
                   branch: str = "master",
                   type: str = "RECURSIVE") -> dict:
        """List files in repository

        Args:
            org_id: Organization ID
            repo_id: Repository ID
            path: Directory path (default: "")
            branch: Branch name (default: master)
            type: Tree type - DIRECT, RECURSIVE, or FLATTEN (default: RECURSIVE)
        """
        return self._make_request(
            "GET",
            f"/oapi/v1/codeup/organizations/{org_id}/repositories/{repo_id}/files/tree",
            params={"path": path, "ref": branch, "type": type}
        )

    def compare(self, org_id: str, repo_id: str, from_ref: str, to_ref: str,
                source_type: str = None, target_type: str = None,
                straight: str = None) -> dict:
        """Compare code between branches, tags, or commits

        Args:
            org_id: Organization ID
            repo_id: Repository ID
            from_ref: Source reference (branch name, tag, or commit SHA)
            to_ref: Target reference (branch name, tag, or commit SHA)
            source_type: Type of source reference (branch/tag/None for commit)
            target_type: Type of target reference (branch/tag/None for commit)
            straight: Use merge-base (false) or not (true). Default: false
        """
        params = {"from": from_ref, "to": to_ref}
        if source_type:
            params["sourceType"] = source_type
        if target_type:
            params["targetType"] = target_type
        if straight is not None:
            params["straight"] = straight
        return self._make_request(
            "GET",
            f"/oapi/v1/codeup/organizations/{org_id}/repositories/{repo_id}/compares",
            params=params
        )

    # ==================== Merge Request ====================

    def get_change_request(self, org_id: str, repo_id: str, local_id: int) -> dict:
        """Get merge request details

        Args:
            org_id: Organization ID
            repo_id: Repository ID
            local_id: Local MR ID (the sequence number in the repository)
        """
        return self._make_request(
            "GET",
            f"/oapi/v1/codeup/organizations/{org_id}/repositories/{repo_id}/changeRequests/{local_id}"
        )

    def list_merge_requests(self, org_id: str, repo_id: str = None, state: str = None,
                            page: int = 1, per_page: int = 20,
                            author_ids: str = None, reviewer_ids: str = None,
                            search: str = None, order_by: str = None, sort: str = None,
                            created_before: str = None, created_after: str = None) -> dict:
        """List merge requests in organization

        Args:
            org_id: Organization ID
            repo_id: Repository ID (optional)
            state: MR state - opened, merged, closed
            page: Page number (default: 1)
            per_page: Items per page (default: 20)
            author_ids: Author user IDs (comma-separated)
            reviewer_ids: Reviewer user IDs (comma-separated)
            search: Title keyword search
            order_by: Sort field - created_at, updated_at
            sort: Sort order - asc, desc
            created_before: Start creation time (ISO 8601)
            created_after: End creation time (ISO 8601)
        """
        params = {"page": page, "perPage": per_page}
        if state:
            params["state"] = state
        if repo_id:
            params["projectIds"] = repo_id
        if author_ids:
            params["authorIds"] = author_ids
        if reviewer_ids:
            params["reviewerIds"] = reviewer_ids
        if search:
            params["search"] = search
        if order_by:
            params["orderBy"] = order_by
        if sort:
            params["sort"] = sort
        if created_before:
            params["createdBefore"] = created_before
        if created_after:
            params["createdAfter"] = created_after
        return self._make_request(
            "GET",
            f"/oapi/v1/codeup/organizations/{org_id}/changeRequests",
            params=params
        )

    def create_merge_request(self, org_id: str, repo_id: str, title: str,
                             source_branch: str, target_branch: str,
                             description: str = None,
                             reviewer_user_ids: list = None) -> dict:
        """Create a merge request

        Args:
            org_id: Organization ID
            repo_id: Repository ID
            title: MR title
            source_branch: Source branch
            target_branch: Target branch
            description: MR description
            reviewer_user_ids: List of reviewer user IDs
        """
        data = {
            "title": title,
            "sourceBranch": source_branch,
            "targetBranch": target_branch,
            "sourceProjectId": int(repo_id),
            "targetProjectId": int(repo_id)
        }
        if description:
            data["description"] = description
        if reviewer_user_ids:
            data["reviewerUserIds"] = reviewer_user_ids
        return self._make_request(
            "POST",
            f"/oapi/v1/codeup/organizations/{org_id}/repositories/{repo_id}/changeRequests",
            data=data
        )

    def close_merge_request(self, org_id: str, repo_id: str, local_id: int) -> dict:
        """Close a merge request

        Args:
            org_id: Organization ID
            repo_id: Repository ID
            local_id: Local MR ID (sequence number)
        """
        return self._make_request(
            "POST",
            f"/oapi/v1/codeup/organizations/{org_id}/repositories/{repo_id}/changeRequests/{local_id}/close"
        )

    def create_merge_request_comment(self, org_id: str, repo_id: str, local_id: int,
                                     content: str, comment_type: str = "GLOBAL_COMMENT",
                                     draft: bool = False, patchset_biz_id: str = None,
                                     file_path: str = None, line_number: int = None,
                                     parent_comment_biz_id: str = None,
                                     from_patchset_biz_id: str = None,
                                     to_patchset_biz_id: str = None,
                                     resolved: bool = False) -> dict:
        """Add a comment to merge request

        Args:
            org_id: Organization ID
            repo_id: Repository ID
            local_id: Local MR ID
            content: Comment content
            comment_type: Comment type - GLOBAL_COMMENT or INLINE_COMMENT
            draft: Is draft comment (default: False)
            patchset_biz_id: Patch set biz ID (required for INLINE_COMMENT)
            file_path: File path for inline comment
            line_number: Line number for inline comment
            parent_comment_biz_id: Parent comment biz ID
            from_patchset_biz_id: From patch set biz ID
            to_patchset_biz_id: To patch set biz ID (required for INLINE_COMMENT)
            resolved: Is resolved (default: False)
        """
        data = {
            "content": content,
            "comment_type": comment_type,
            "draft": draft,
            "resolved": resolved
        }
        if patchset_biz_id:
            data["patchset_biz_id"] = patchset_biz_id
        if file_path:
            data["file_path"] = file_path
        if line_number:
            data["line_number"] = line_number
        if parent_comment_biz_id:
            data["parent_comment_biz_id"] = parent_comment_biz_id
        if from_patchset_biz_id:
            data["from_patchset_biz_id"] = from_patchset_biz_id
        if to_patchset_biz_id:
            data["to_patchset_biz_id"] = to_patchset_biz_id
        return self._make_request(
            "POST",
            f"/oapi/v1/codeup/organizations/{org_id}/repositories/{repo_id}/changeRequests/{local_id}/comments",
            data=data
        )

    def list_merge_request_comments(self, org_id: str, repo_id: str, local_id: int,
                                    page: int = 1, per_page: int = 20) -> list:
        """List comments on merge request

        Args:
            org_id: Organization ID
            repo_id: Repository ID
            local_id: Local MR ID
            page: Page number (default: 1)
            per_page: Items per page (default: 20)
        """
        return self._make_request(
            "POST",
            f"/oapi/v1/codeup/organizations/{org_id}/repositories/{repo_id}/changeRequests/{local_id}/comments/list",
            data={"page": page, "perPage": per_page}
        )

    def list_merge_request_patch_sets(self, org_id: str, repo_id: str, local_id: int) -> dict:
        """List patch sets (commits) of merge request

        Args:
            org_id: Organization ID
            repo_id: Repository ID
            local_id: Local MR ID
        """
        return self._make_request(
            "GET",
            f"/oapi/v1/codeup/organizations/{org_id}/repositories/{repo_id}/changeRequests/{local_id}/diffs/patches"
        )

    def merge_change_request(self, org_id: str, repo_id: str, local_id: int) -> dict:
        """Merge a merge request

        Args:
            org_id: Organization ID
            repo_id: Repository ID
            local_id: Local MR ID
        """
        return self._make_request(
            "POST",
            f"/oapi/v1/codeup/organizations/{org_id}/repositories/{repo_id}/changeRequests/{local_id}/merge"
        )

    def reopen_change_request(self, org_id: str, repo_id: str, local_id: int) -> dict:
        """Reopen a closed merge request

        Args:
            org_id: Organization ID
            repo_id: Repository ID
            local_id: Local MR ID
        """
        return self._make_request(
            "POST",
            f"/oapi/v1/codeup/organizations/{org_id}/repositories/{repo_id}/changeRequests/{local_id}/reopen"
        )

    def review_change_request(self, org_id: str, repo_id: str, local_id: int,
                              decision: str, comment: str = None) -> dict:
        """Review (approve/reject) a merge request

        Args:
            org_id: Organization ID
            repo_id: Repository ID
            local_id: Local MR ID
            decision: Review decision - APPROVE, REJECT, or ABSTAIN
            comment: Review comment (optional)
        """
        data = {"decision": decision}
        if comment:
            data["comment"] = comment
        return self._make_request(
            "POST",
            f"/oapi/v1/codeup/organizations/{org_id}/repositories/{repo_id}/changeRequests/{local_id}/review",
            data=data
        )

    def update_change_request(self, org_id: str, repo_id: str, local_id: int,
                              title: str = None, description: str = None) -> dict:
        """Update a merge request

        Args:
            org_id: Organization ID
            repo_id: Repository ID
            local_id: Local MR ID
            title: New title (optional)
            description: New description (optional)
        """
        data = {}
        if title:
            data["title"] = title
        if description:
            data["description"] = description
        return self._make_request(
            "PUT",
            f"/oapi/v1/codeup/organizations/{org_id}/repositories/{repo_id}/changeRequests/{local_id}",
            data=data
        )

    def get_change_request_tree(self, org_id: str, repo_id: str, local_id: int,
                                 page: int = 1, per_page: int = 50) -> dict:
        """Get changed files tree of a merge request

        Args:
            org_id: Organization ID
            repo_id: Repository ID
            local_id: Local MR ID
            page: Page number (default: 1)
            per_page: Items per page (default: 50)
        """
        return self._make_request(
            "GET",
            f"/oapi/v1/codeup/organizations/{org_id}/repositories/{repo_id}/changeRequests/{local_id}/tree",
            params={"page": page, "perPage": per_page}
        )

    def delete_change_request_comment(self, org_id: str, repo_id: str,
                                      comment_biz_id: str) -> dict:
        """Delete a comment on merge request

        Args:
            org_id: Organization ID
            repo_id: Repository ID
            comment_biz_id: Comment biz ID
        """
        return self._make_request(
            "DELETE",
            f"/oapi/v1/codeup/organizations/{org_id}/repositories/{repo_id}/comments/{comment_biz_id}"
        )

    def update_change_request_comment(self, org_id: str, repo_id: str,
                                      comment_biz_id: str, content: str) -> dict:
        """Update a comment on merge request

        Args:
            org_id: Organization ID
            repo_id: Repository ID
            comment_biz_id: Comment biz ID
            content: New comment content
        """
        return self._make_request(
            "PUT",
            f"/oapi/v1/codeup/organizations/{org_id}/repositories/{repo_id}/comments/{comment_biz_id}",
            data={"content": content}
        )
