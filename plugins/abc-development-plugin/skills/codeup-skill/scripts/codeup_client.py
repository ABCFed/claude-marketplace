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

    def get_current_user(self, organization_id: str = None) -> dict:
        """Get current user information

        Args:
            organization_id: Optional organization ID. Returns personal name if not provided,
                           returns organization name if provided.
        """
        params = {}
        if organization_id:
            params["organizationId"] = organization_id
        return self._make_request("GET", "/users/current", params=params if params else None)

    def list_organizations(self) -> dict:
        """List organizations the user belongs to"""
        return self._make_request("GET", "/users/joinedOrgs")

    def list_departments(self, org_id: str) -> dict:
        """List departments in organization"""
        return self._make_request("GET", f"/oapi/v1/organization/{org_id}/departments")

    def get_department(self, org_id: str, dept_id: str) -> dict:
        """Get department details"""
        return self._make_request("GET", f"/oapi/v1/organization/{org_id}/departments/{dept_id}")

    def list_members(
        self,
        org_id: str,
        organization_member_name: str = None,
        provider: str = None,
        extern_uid: str = None,
        state: str = None,
        next_token: str = None,
        max_results: int = 20,
        join_time_from: int = None,
        join_time_to: int = None,
        contains_extern_info: bool = None,
    ) -> dict:
        """List organization members

        Args:
            org_id: Organization ID
            organization_member_name: Member name filter
            provider: Third-party system (used with externUid)
            extern_uid: Third-party user ID
            state: User state (normal/blocked/deleted), default normal
            next_token: Pagination token
            max_results: Max results (0-50, default 20)
            join_time_from: Join time from (milliseconds timestamp)
            join_time_to: Join time to (milliseconds timestamp)
            contains_extern_info: Include third-party info, default false
        """
        params = {"maxResults": max_results}
        if organization_member_name:
            params["organizationMemberName"] = organization_member_name
        if provider:
            params["provider"] = provider
        if extern_uid:
            params["externUid"] = extern_uid
        if state:
            params["state"] = state
        if next_token:
            params["nextToken"] = next_token
        if join_time_from:
            params["joinTimeFrom"] = join_time_from
        if join_time_to:
            params["joinTimeTo"] = join_time_to
        if contains_extern_info is not None:
            params["containsExternInfo"] = contains_extern_info

        return self._make_request(
            "GET",
            f"/organization/{org_id}/members",
            params=params
        )

    def get_organization_member(self, org_id: str, account_id: str) -> dict:
        """Get organization member details

        Args:
            org_id: Organization ID
            account_id: Alibaba Cloud user UID
        """
        return self._make_request(
            "GET",
            f"/organization/{org_id}/members/{account_id}"
        )

    def search_members(self, org_id: str, query: str) -> dict:
        """Search organization members"""
        return self._make_request(
            "GET",
            f"/oapi/v1/organization/{org_id}/members",
            params={"query": query}
        )

    def list_roles(self, org_id: str) -> dict:
        """List organization roles"""
        return self._make_request("GET", f"/oapi/v1/organization/{org_id}/roles")

    # ==================== Repository ====================

    def get_repository(self, org_id: str, repo_id: str) -> dict:
        """Get repository details"""
        return self._make_request(
            "GET",
            f"/oapi/v1/codeup/organizations/{org_id}/repositories/{repo_id}"
        )

    def list_repositories(self, org_id: str, page: int = 1, limit: int = 20) -> dict:
        """List repositories in organization"""
        return self._make_request(
            "GET",
            f"/oapi/v1/codeup/organizations/{org_id}/repositories",
            params={"page": page, "limit": limit}
        )

    # ==================== Branch ====================

    def get_branch(self, org_id: str, repo_id: str, branch_name: str) -> dict:
        """Get branch details"""
        return self._make_request(
            "GET",
            f"/oapi/v1/codeup/organizations/{org_id}/repositories/{repo_id}/branches/{branch_name}"
        )

    def create_branch(self, org_id: str, repo_id: str, branch_name: str, source_branch: str) -> dict:
        """Create a new branch"""
        return self._make_request(
            "POST",
            f"/oapi/v1/codeup/organizations/{org_id}/repositories/{repo_id}/branches",
            data={"branchName": branch_name, "sourceBranch": source_branch}
        )

    def delete_branch(self, org_id: str, repo_id: str, branch_name: str) -> dict:
        """Delete a branch"""
        return self._make_request(
            "DELETE",
            f"/oapi/v1/codeup/organizations/{org_id}/repositories/{repo_id}/branches/{branch_name}"
        )

    def list_branches(self, org_id: str, repo_id: str, page: int = 1, limit: int = 20) -> dict:
        """List branches in repository"""
        return self._make_request(
            "GET",
            f"/oapi/v1/codeup/organizations/{org_id}/repositories/{repo_id}/branches",
            params={"page": page, "limit": limit}
        )

    # ==================== File ====================

    def get_file(self, org_id: str, repo_id: str, file_path: str, branch: str = "master") -> dict:
        """Get file content"""
        return self._make_request(
            "GET",
            f"/oapi/v1/codeup/organizations/{org_id}/repositories/{repo_id}/files",
            params={"filePath": file_path, "ref": branch}
        )

    def create_file(self, org_id: str, repo_id: str, file_path: str, content: str,
                    branch: str = "master", message: str = None) -> dict:
        """Create a new file"""
        data = {
            "filePath": file_path,
            "branchName": branch,
            "content": content
        }
        if message:
            data["commitMessage"] = message
        return self._make_request(
            "POST",
            f"/oapi/v1/codeup/organizations/{org_id}/repositories/{repo_id}/files",
            data=data
        )

    def update_file(self, org_id: str, repo_id: str, file_path: str, content: str,
                    branch: str = "master", message: str = None) -> dict:
        """Update an existing file"""
        data = {
            "filePath": file_path,
            "branchName": branch,
            "content": content
        }
        if message:
            data["commitMessage"] = message
        return self._make_request(
            "PUT",
            f"/oapi/v1/codeup/organizations/{org_id}/repositories/{repo_id}/files",
            data=data
        )

    def delete_file(self, org_id: str, repo_id: str, file_path: str,
                    branch: str = "master", message: str = None) -> dict:
        """Delete a file"""
        params = {
            "filePath": file_path,
            "branchName": branch
        }
        if message:
            params["commitMessage"] = message
        return self._make_request(
            "DELETE",
            f"/oapi/v1/codeup/organizations/{org_id}/repositories/{repo_id}/files",
            params=params
        )

    def list_files(self, org_id: str, repo_id: str, path: str = "",
                   branch: str = "master", page: int = 1, limit: int = 100) -> dict:
        """List files in repository"""
        return self._make_request(
            "GET",
            f"/oapi/v1/codeup/organizations/{org_id}/repositories/{repo_id}/repositoryTree",
            params={"path": path, "ref": branch, "page": page, "limit": limit}
        )

    def compare(self, org_id: str, repo_id: str, source: str, target: str) -> dict:
        """Compare code between two branches/tags"""
        return self._make_request(
            "GET",
            f"/oapi/v1/codeup/organizations/{org_id}/repositories/{repo_id}/compare",
            params={"from": source, "to": target}
        )

    # ==================== Merge Request ====================

    def get_merge_request(self, org_id: str, repo_id: str, mr_id: str) -> dict:
        """Get merge request details"""
        return self._make_request(
            "GET",
            f"/oapi/v1/codeup/organizations/{org_id}/repositories/{repo_id}/changeRequests/{mr_id}",
            params={"projectIds": repo_id}
        )

    def list_merge_requests(self, org_id: str, repo_id: str = None, state: str = None,
                            page: int = 1, limit: int = 20) -> dict:
        """List merge requests in repository"""
        params = {"page": page, "limit": limit}
        if state:
            params["state"] = state
        if repo_id:
            params["projectIds"] = repo_id
        return self._make_request(
            "GET",
            f"/oapi/v1/codeup/organizations/{org_id}/changeRequests",
            params=params
        )

    def create_merge_request(self, org_id: str, repo_id: str, title: str,
                             source_branch: str, target_branch: str,
                             description: str = None) -> dict:
        """Create a merge request"""
        data = {
            "title": title,
            "sourceBranch": source_branch,
            "targetBranch": target_branch,
            "sourceProjectId": str(repo_id),
            "targetProjectId": str(repo_id)
        }
        if description:
            data["description"] = description
        return self._make_request(
            "POST",
            f"/oapi/v1/codeup/organizations/{org_id}/repositories/{repo_id}/changeRequests",
            data=data
        )

    def create_merge_request_comment(self, org_id: str, repo_id: str, mr_id: str,
                                     content: str) -> dict:
        """Add a comment to merge request"""
        return self._make_request(
            "POST",
            f"/oapi/v1/codeup/organizations/{org_id}/repositories/{repo_id}/changeRequests/{mr_id}/comments",
            data={"content": content}
        )

    def list_merge_request_comments(self, org_id: str, repo_id: str, mr_id: str,
                                    page: int = 1, limit: int = 20) -> dict:
        """List comments on merge request"""
        return self._make_request(
            "GET",
            f"/oapi/v1/codeup/organizations/{org_id}/repositories/{repo_id}/changeRequests/{mr_id}/comments",
            params={"page": page, "limit": limit}
        )

    def list_merge_request_patch_sets(self, org_id: str, repo_id: str, mr_id: str) -> dict:
        """List patch sets (commits) of merge request"""
        return self._make_request(
            "GET",
            f"/oapi/v1/codeup/organizations/{org_id}/repositories/{repo_id}/changeRequests/{mr_id}/patchsets"
        )
