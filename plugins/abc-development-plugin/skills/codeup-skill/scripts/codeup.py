#!/usr/bin/env python3
"""
AlibabaCloud DevOps (云效/Codeup) CLI Tool

Usage:
    python codeup.py <command> [arguments]

Commands:
    # User & Organization
    get_current_user           Get current user information
    get_current_organization   Get current organization information
    list_organizations         List organizations user belongs to
    list_departments           List departments in organization
    get_department             Get department details
    list_members               List organization members
    search_members             Search organization members
    list_roles                 List organization roles

    # Repository
    get_repository             Get repository details
    list_repositories          List repositories in organization

    # Branch
    get_branch                 Get branch details
    create_branch              Create a new branch
    delete_branch              Delete a branch
    list_branches              List branches in repository

    # File
    get_file                   Get file content
    create_file                Create a new file
    update_file                Update an existing file
    delete_file                Delete a file
    list_files                 List files in repository
    compare                    Compare code between branches

    # Merge Request
    get_merge_request          Get merge request details
    list_merge_requests        List merge requests
    create_merge_request       Create a merge request
    create_merge_request_comment   Add comment to MR
    list_merge_request_comments    List MR comments
    list_merge_request_patch_sets  List MR patch sets (commits)
"""

import os
import sys
import json
import argparse

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from codeup_client import CodeupClient, get_env_check_message


def cmd_get_current_user(args):
    """Get current user information"""
    client = CodeupClient()
    result = client.get_current_user()
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_get_current_organization(args):
    """Get current organization information"""
    client = CodeupClient()
    result = client.get_current_organization()
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_list_organizations(args):
    """List organizations user belongs to"""
    client = CodeupClient()
    result = client.list_organizations()
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_list_departments(args):
    """List departments in organization"""
    client = CodeupClient()
    result = client.list_departments(args.org_id)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_get_department(args):
    """Get department details"""
    client = CodeupClient()
    result = client.get_department(args.org_id, args.dept_id)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_list_members(args):
    """List organization members"""
    client = CodeupClient()
    result = client.list_members(args.org_id, page=args.page, limit=args.limit)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_search_members(args):
    """Search organization members"""
    client = CodeupClient()
    result = client.search_members(args.org_id, args.query)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_list_roles(args):
    """List organization roles"""
    client = CodeupClient()
    result = client.list_roles(args.org_id)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_get_repository(args):
    """Get repository details"""
    client = CodeupClient()
    result = client.get_repository(args.org_id, args.repo_id)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_list_repositories(args):
    """List repositories in organization"""
    client = CodeupClient()
    result = client.list_repositories(args.org_id, page=args.page, limit=args.limit)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_get_branch(args):
    """Get branch details"""
    client = CodeupClient()
    result = client.get_branch(args.org_id, args.repo_id, args.branch_name)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_create_branch(args):
    """Create a new branch"""
    client = CodeupClient()
    result = client.create_branch(
        args.org_id, args.repo_id, args.branch_name, args.source_branch
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_delete_branch(args):
    """Delete a branch"""
    client = CodeupClient()
    result = client.delete_branch(args.org_id, args.repo_id, args.branch_name)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_list_branches(args):
    """List branches in repository"""
    client = CodeupClient()
    result = client.list_branches(
        args.org_id, args.repo_id, page=args.page, limit=args.limit
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_get_file(args):
    """Get file content"""
    client = CodeupClient()
    result = client.get_file(args.org_id, args.repo_id, args.file_path, args.branch)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_create_file(args):
    """Create a new file"""
    client = CodeupClient()
    # Read content from file if specified, otherwise use stdin
    if args.content_file:
        with open(args.content_file, 'r', encoding='utf-8') as f:
            content = f.read()
    elif args.content:
        content = args.content
    else:
        content = sys.stdin.read()

    result = client.create_file(
        args.org_id, args.repo_id, args.file_path, content,
        branch=args.branch, message=args.message
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_update_file(args):
    """Update an existing file"""
    client = CodeupClient()
    # Read content from file if specified, otherwise use stdin
    if args.content_file:
        with open(args.content_file, 'r', encoding='utf-8') as f:
            content = f.read()
    elif args.content:
        content = args.content
    else:
        content = sys.stdin.read()

    result = client.update_file(
        args.org_id, args.repo_id, args.file_path, content,
        branch=args.branch, message=args.message
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_delete_file(args):
    """Delete a file"""
    client = CodeupClient()
    result = client.delete_file(
        args.org_id, args.repo_id, args.file_path,
        branch=args.branch, message=args.message
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_list_files(args):
    """List files in repository"""
    client = CodeupClient()
    result = client.list_files(
        args.org_id, args.repo_id, path=args.path,
        branch=args.branch, page=args.page, limit=args.limit
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_compare(args):
    """Compare code between branches"""
    client = CodeupClient()
    result = client.compare(
        args.org_id, args.repo_id, args.source, args.target
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_get_merge_request(args):
    """Get merge request details"""
    client = CodeupClient()
    result = client.get_merge_request(args.org_id, args.repo_id, args.mr_id)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_list_merge_requests(args):
    """List merge requests"""
    client = CodeupClient()
    result = client.list_merge_requests(
        args.org_id, args.repo_id, state=args.state,
        page=args.page, limit=args.limit
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_create_merge_request(args):
    """Create a merge request"""
    client = CodeupClient()
    result = client.create_merge_request(
        args.org_id, args.repo_id, args.title,
        args.source_branch, args.target_branch,
        description=args.description
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_create_merge_request_comment(args):
    """Add a comment to merge request"""
    client = CodeupClient()
    # Read content from file if specified, otherwise use stdin
    if args.content_file:
        with open(args.content_file, 'r', encoding='utf-8') as f:
            content = f.read()
    elif args.content:
        content = args.content
    else:
        content = sys.stdin.read()

    result = client.create_merge_request_comment(
        args.org_id, args.repo_id, args.mr_id, content
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_list_merge_request_comments(args):
    """List comments on merge request"""
    client = CodeupClient()
    result = client.list_merge_request_comments(
        args.org_id, args.repo_id, args.mr_id,
        page=args.page, limit=args.limit
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_list_merge_request_patch_sets(args):
    """List patch sets (commits) of merge request"""
    client = CodeupClient()
    result = client.list_merge_request_patch_sets(
        args.org_id, args.repo_id, args.mr_id
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


def build_parser():
    """Build argument parser with subcommands"""
    parser = argparse.ArgumentParser(
        description="AlibabaCloud DevOps (云效/Codeup) CLI Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # ==================== User & Organization Commands ====================

    p = subparsers.add_parser("get_current_user", help="Get current user information")
    p = subparsers.add_parser("get_current_organization", help="Get current organization information")
    p = subparsers.add_parser("list_organizations", help="List organizations user belongs to")

    p = subparsers.add_parser("list_departments", help="List departments in organization")
    p.add_argument("--org_id", required=True, help="Organization ID")

    p = subparsers.add_parser("get_department", help="Get department details")
    p.add_argument("--org_id", required=True, help="Organization ID")
    p.add_argument("--dept_id", required=True, help="Department ID")

    p = subparsers.add_parser("list_members", help="List organization members")
    p.add_argument("--org_id", required=True, help="Organization ID")
    p.add_argument("--page", type=int, default=1, help="Page number (default: 1)")
    p.add_argument("--limit", type=int, default=20, help="Items per page (default: 20)")

    p = subparsers.add_parser("search_members", help="Search organization members")
    p.add_argument("--org_id", required=True, help="Organization ID")
    p.add_argument("--query", required=True, help="Search query")

    p = subparsers.add_parser("list_roles", help="List organization roles")
    p.add_argument("--org_id", required=True, help="Organization ID")

    # ==================== Repository Commands ====================

    p = subparsers.add_parser("get_repository", help="Get repository details")
    p.add_argument("--org_id", required=True, help="Organization ID")
    p.add_argument("--repo_id", required=True, help="Repository ID")

    p = subparsers.add_parser("list_repositories", help="List repositories in organization")
    p.add_argument("--org_id", required=True, help="Organization ID")
    p.add_argument("--page", type=int, default=1, help="Page number (default: 1)")
    p.add_argument("--limit", type=int, default=20, help="Items per page (default: 20)")

    # ==================== Branch Commands ====================

    p = subparsers.add_parser("get_branch", help="Get branch details")
    p.add_argument("--org_id", required=True, help="Organization ID")
    p.add_argument("--repo_id", required=True, help="Repository ID")
    p.add_argument("--branch_name", required=True, help="Branch name")

    p = subparsers.add_parser("create_branch", help="Create a new branch")
    p.add_argument("--org_id", required=True, help="Organization ID")
    p.add_argument("--repo_id", required=True, help="Repository ID")
    p.add_argument("--branch_name", required=True, help="New branch name")
    p.add_argument("--source_branch", required=True, help="Source branch name")

    p = subparsers.add_parser("delete_branch", help="Delete a branch")
    p.add_argument("--org_id", required=True, help="Organization ID")
    p.add_argument("--repo_id", required=True, help="Repository ID")
    p.add_argument("--branch_name", required=True, help="Branch name to delete")

    p = subparsers.add_parser("list_branches", help="List branches in repository")
    p.add_argument("--org_id", required=True, help="Organization ID")
    p.add_argument("--repo_id", required=True, help="Repository ID")
    p.add_argument("--page", type=int, default=1, help="Page number (default: 1)")
    p.add_argument("--limit", type=int, default=20, help="Items per page (default: 20)")

    # ==================== File Commands ====================

    p = subparsers.add_parser("get_file", help="Get file content")
    p.add_argument("--org_id", required=True, help="Organization ID")
    p.add_argument("--repo_id", required=True, help="Repository ID")
    p.add_argument("--file_path", required=True, help="File path in repository")
    p.add_argument("--branch", default="master", help="Branch name (default: master)")

    p = subparsers.add_parser("create_file", help="Create a new file")
    p.add_argument("--org_id", required=True, help="Organization ID")
    p.add_argument("--repo_id", required=True, help="Repository ID")
    p.add_argument("--file_path", required=True, help="File path in repository")
    p.add_argument("--branch", default="master", help="Branch name (default: master)")
    p.add_argument("--message", help="Commit message")
    p.add_argument("--content", help="File content (or use --content-file or stdin)")
    p.add_argument("--content-file", help="File path to read content from")

    p = subparsers.add_parser("update_file", help="Update an existing file")
    p.add_argument("--org_id", required=True, help="Organization ID")
    p.add_argument("--repo_id", required=True, help="Repository ID")
    p.add_argument("--file_path", required=True, help="File path in repository")
    p.add_argument("--branch", default="master", help="Branch name (default: master)")
    p.add_argument("--message", help="Commit message")
    p.add_argument("--content", help="File content (or use --content-file or stdin)")
    p.add_argument("--content-file", help="File path to read content from")

    p = subparsers.add_parser("delete_file", help="Delete a file")
    p.add_argument("--org_id", required=True, help="Organization ID")
    p.add_argument("--repo_id", required=True, help="Repository ID")
    p.add_argument("--file_path", required=True, help="File path in repository")
    p.add_argument("--branch", default="master", help="Branch name (default: master)")
    p.add_argument("--message", help="Commit message")

    p = subparsers.add_parser("list_files", help="List files in repository")
    p.add_argument("--org_id", required=True, help="Organization ID")
    p.add_argument("--repo_id", required=True, help="Repository ID")
    p.add_argument("--path", default="", help="Directory path (default: root)")
    p.add_argument("--branch", default="master", help="Branch name (default: master)")
    p.add_argument("--page", type=int, default=1, help="Page number (default: 1)")
    p.add_argument("--limit", type=int, default=100, help="Items per page (default: 100)")

    p = subparsers.add_parser("compare", help="Compare code between branches")
    p.add_argument("--org_id", required=True, help="Organization ID")
    p.add_argument("--repo_id", required=True, help="Repository ID")
    p.add_argument("--source", required=True, help="Source branch/tag")
    p.add_argument("--target", required=True, help="Target branch/tag")

    # ==================== Merge Request Commands ====================

    p = subparsers.add_parser("get_merge_request", help="Get merge request details")
    p.add_argument("--org_id", required=True, help="Organization ID")
    p.add_argument("--repo_id", required=True, help="Repository ID")
    p.add_argument("--mr_id", required=True, help="Merge request ID")

    p = subparsers.add_parser("list_merge_requests", help="List merge requests")
    p.add_argument("--org_id", required=True, help="Organization ID")
    p.add_argument("--repo_id", required=True, help="Repository ID")
    p.add_argument("--state", choices=["open", "closed", "merged"], help="MR state filter")
    p.add_argument("--page", type=int, default=1, help="Page number (default: 1)")
    p.add_argument("--limit", type=int, default=20, help="Items per page (default: 20)")

    p = subparsers.add_parser("create_merge_request", help="Create a merge request")
    p.add_argument("--org_id", required=True, help="Organization ID")
    p.add_argument("--repo_id", required=True, help="Repository ID")
    p.add_argument("--title", required=True, help="MR title")
    p.add_argument("--source_branch", required=True, help="Source branch")
    p.add_argument("--target_branch", required=True, help="Target branch")
    p.add_argument("--description", help="MR description")

    p = subparsers.add_parser("create_merge_request_comment", help="Add comment to merge request")
    p.add_argument("--org_id", required=True, help="Organization ID")
    p.add_argument("--repo_id", required=True, help="Repository ID")
    p.add_argument("--mr_id", required=True, help="Merge request ID")
    p.add_argument("--content", help="Comment content (or use --content-file or stdin)")
    p.add_argument("--content-file", help="File path to read content from")

    p = subparsers.add_parser("list_merge_request_comments", help="List comments on merge request")
    p.add_argument("--org_id", required=True, help="Organization ID")
    p.add_argument("--repo_id", required=True, help="Repository ID")
    p.add_argument("--mr_id", required=True, help="Merge request ID")
    p.add_argument("--page", type=int, default=1, help="Page number (default: 1)")
    p.add_argument("--limit", type=int, default=20, help="Items per page (default: 20)")

    p = subparsers.add_parser("list_merge_request_patch_sets", help="List MR patch sets (commits)")
    p.add_argument("--org_id", required=True, help="Organization ID")
    p.add_argument("--repo_id", required=True, help="Repository ID")
    p.add_argument("--mr_id", required=True, help="Merge request ID")

    return parser


def main():
    """Main entry point"""
    # Check environment variables first
    env_msg = get_env_check_message()
    if env_msg:
        print(env_msg, file=sys.stderr)
        sys.exit(1)

    parser = build_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Command dispatch
    cmd_map = {
        "get_current_user": cmd_get_current_user,
        "get_current_organization": cmd_get_current_organization,
        "list_organizations": cmd_list_organizations,
        "list_departments": cmd_list_departments,
        "get_department": cmd_get_department,
        "list_members": cmd_list_members,
        "search_members": cmd_search_members,
        "list_roles": cmd_list_roles,
        "get_repository": cmd_get_repository,
        "list_repositories": cmd_list_repositories,
        "get_branch": cmd_get_branch,
        "create_branch": cmd_create_branch,
        "delete_branch": cmd_delete_branch,
        "list_branches": cmd_list_branches,
        "get_file": cmd_get_file,
        "create_file": cmd_create_file,
        "update_file": cmd_update_file,
        "delete_file": cmd_delete_file,
        "list_files": cmd_list_files,
        "compare": cmd_compare,
        "get_merge_request": cmd_get_merge_request,
        "list_merge_requests": cmd_list_merge_requests,
        "create_merge_request": cmd_create_merge_request,
        "create_merge_request_comment": cmd_create_merge_request_comment,
        "list_merge_request_comments": cmd_list_merge_request_comments,
        "list_merge_request_patch_sets": cmd_list_merge_request_patch_sets,
    }

    cmd_func = cmd_map.get(args.command)
    if cmd_func:
        try:
            cmd_func(args)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(f"Unknown command: {args.command}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
