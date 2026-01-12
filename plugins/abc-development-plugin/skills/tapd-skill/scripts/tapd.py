#!/usr/bin/env python3
"""
TAPD 统一命令行工具

用法: python tapd.py <command> [参数]

命令列表:
  项目相关:
    get_user_participant_projects  获取用户参与的项目列表
    get_workspace_info            获取项目信息
    get_workitem_types            获取需求类别

  需求/任务:
    get_stories_or_tasks          查询需求/任务
    create_story_or_task          创建需求/任务
    update_story_or_task          更新需求/任务
    get_story_or_task_count       获取数量
    get_stories_fields_lable      字段中英文对照
    get_stories_fields_info       字段及候选值

  缺陷:
    get_bug                       查询缺陷
    create_bug                    创建缺陷
    update_bug                    更新缺陷
    get_bug_count                 获取数量

  迭代:
    get_iterations                查询迭代
    create_iteration              创建迭代
    update_iteration              更新迭代

  评论:
    get_comments                  查询评论
    create_comments               创建评论
    update_comments               更新评论

  附件/图片:
    get_entity_attachments        获取附件
    get_image                     获取图片下载链接

  自定义字段:
    get_entity_custom_fields      获取自定义字段配置

  工作流:
    get_workflows_status_map      状态映射
    get_workflows_all_transitions 状态流转
    get_workflows_last_steps      结束状态

  测试用例:
    get_tcases                    查询测试用例
    create_or_update_tcases       创建/更新测试用例
    create_tcases_batch           批量创建

  Wiki:
    get_wiki                      查询 Wiki
    create_wiki                   创建 Wiki
    update_wiki                   更新 Wiki

  工时:
    get_timesheets                查询工时
    add_timesheets                填写工时
    update_timesheets             更新工时

  待办:
    get_todo                      获取待办

  关联:
    get_related_bugs              获取关联缺陷
    entity_relations              创建关联关系

  发布计划:
    get_release_info              获取发布计划

  源码:
    get_commit_msg                获取提交关键字

  消息:
    send_qiwei_message            发送企业微信消息

示例:
    python tapd.py get_stories_or_tasks --workspace_id 123 --entity_type stories
    python tapd.py create_story_or_task --workspace_id 123 --name "需求标题"
    python tapd.py get_bug --workspace_id 123 --title "%登录%"
"""

import sys
import re
import json
import argparse
import os
from tapd_client import TAPDClient


def get_tapd_base_url():
    """获取 TAPD 基础 URL"""
    from tapd_client import get_env_check_message
    if get_env_check_message():
        print(get_env_check_message())
        sys.exit(1)

    config_base_url = os.getenv("TAPD_BASE_URL")
    return config_base_url or os.getenv("TAPD_API_BASE_URL", "https://www.tapd.cn").replace("api.tapd.cn", "www.tapd.cn")


# ============ 项目相关 ============

def cmd_get_user_participant_projects(args):
    """获取用户参与的项目列表"""
    client = TAPDClient()
    data = {"nick": args.nick} if args.nick else {"nick": client.nick or ""}
    result = client.get_user_participant_projects(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_get_workspace_info(args):
    """获取项目信息"""
    client = TAPDClient()
    result = client.get_workspace_info({"workspace_id": args.workspace_id})
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_get_workitem_types(args):
    """获取需求类别"""
    client = TAPDClient()
    data = {"workspace_id": args.workspace_id}
    if args.id:
        data["id"] = args.id
    if args.name:
        data["name"] = args.name
    result = client.get_workitem_types(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


# ============ 需求/任务相关 ============

def cmd_get_stories_or_tasks(args):
    """查询需求/任务"""
    client = TAPDClient()
    data = {"workspace_id": args.workspace_id}

    if args.entity_type:
        data["entity_type"] = args.entity_type
    else:
        data["entity_type"] = "stories"

    if args.id:
        data["id"] = args.id
    if args.name:
        data["name"] = args.name
    if args.status:
        data["status"] = args.status
    if args.v_status:
        data["v_status"] = args.v_status
    if args.owner:
        data["owner"] = args.owner
    if args.creator:
        data["creator"] = args.creator
    if args.priority_label:
        data["priority_label"] = args.priority_label
    if args.iteration_id:
        data["iteration_id"] = args.iteration_id
    if args.limit:
        data["limit"] = args.limit
    if args.page:
        data["page"] = args.page

    # 获取详情时（指定 id）默认包含 description
    fields_param = args.fields
    if args.id:
        if not fields_param:
            fields_param = "description"
        elif "description" not in fields_param:
            fields_param = fields_param + ",description"
    data["fields"] = fields_param

    result = client.get_stories(data)
    count_result = client.get_story_count(data)

    # 过滤字段
    fields_param = data.get('fields')
    if isinstance(result, dict) and 'data' in result:
        result['data'] = client.filter_fields(result['data'], fields_param)

    # 获取详情时，自动处理图片
    if args.id and result.get('data'):
        for item in result['data']:
            story = item.get('Story', {})
            description = story.get('description', '')
            # 提取图片路径
            img_paths = re.findall(r'<img[^>]+src="([^"]+)"', description)
            if img_paths:
                images = []
                for img_path in img_paths:
                    try:
                        # 如果已经是完整 URL，直接使用
                        if img_path.startswith('http://') or img_path.startswith('https://'):
                            images.append({
                                "path": img_path,
                                "download_url": img_path,
                                "filename": ""
                            })
                        else:
                            # 相对路径，调用 get_image 获取下载链接
                            img_result = client.get_image({
                                "workspace_id": args.workspace_id,
                                "image_path": img_path
                            })
                            if img_result.get('data', {}).get('Attachment'):
                                att = img_result['data']['Attachment']
                                images.append({
                                    "path": img_path,
                                    "download_url": att.get('download_url'),
                                    "filename": att.get('filename')
                                })
                    except Exception:
                        continue
                if images:
                    item['images'] = images

    tapd_base_url = get_tapd_base_url()
    url_template = client.get_story_or_task_url_template(args.workspace_id, data["entity_type"], tapd_base_url)

    output = {
        "url_template": url_template,
        "data": result.get('data', []),
        "count": count_result
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


def cmd_create_story_or_task(args):
    """创建需求/任务"""
    client = TAPDClient()
    data = {
        "workspace_id": args.workspace_id,
        "name": args.name
    }

    if args.entity_type:
        data["entity_type"] = args.entity_type
    else:
        data["entity_type"] = "stories"

    if args.description:
        data["description"] = args.description
    if args.priority_label:
        data["priority_label"] = args.priority_label
    if args.owner:
        data["owner"] = args.owner
    if args.iteration_id:
        data["iteration_id"] = args.iteration_id
    if args.iteration_name:
        data["iteration_name"] = args.iteration_name
    if args.category_id:
        data["category_id"] = args.category_id
    if args.workitem_type_id:
        data["workitem_type_id"] = args.workitem_type_id
    if args.release_id:
        data["release_id"] = args.release_id
    if args.parent_id:
        data["parent_id"] = args.parent_id
    if args.story_id and data.get("entity_type") == "tasks":
        data["story_id"] = args.story_id
    if args.size:
        data["size"] = args.size
    if args.version:
        data["version"] = args.version
    if args.module:
        data["module"] = args.module

    result = client.create_or_update_story(data)

    tapd_base_url = get_tapd_base_url()
    entity_type = data["entity_type"]
    url_template = client.get_story_or_task_url_template(args.workspace_id, entity_type, tapd_base_url)

    output = {
        "url_template": url_template,
        "data": json.dumps(result, ensure_ascii=False, indent=2)
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


def cmd_update_story_or_task(args):
    """更新需求/任务"""
    client = TAPDClient()
    data = {
        "workspace_id": args.workspace_id,
        "id": args.id
    }

    if args.entity_type:
        data["entity_type"] = args.entity_type
    else:
        data["entity_type"] = "stories"

    if args.name:
        data["name"] = args.name
    if args.description:
        data["description"] = args.description
    if args.v_status:
        data["v_status"] = args.v_status
    if args.status:
        data["status"] = args.status
    if args.priority_label:
        data["priority_label"] = args.priority_label
    if args.owner:
        data["owner"] = args.owner

    result = client.create_or_update_story(data)

    tapd_base_url = get_tapd_base_url()
    entity_type = data["entity_type"]
    url_template = client.get_story_or_task_url_template(args.workspace_id, entity_type, tapd_base_url)

    output = {
        "url_template": url_template,
        "data": json.dumps(result, ensure_ascii=False, indent=2)
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


def cmd_get_story_or_task_count(args):
    """获取需求/任务数量"""
    client = TAPDClient()
    data = {"workspace_id": args.workspace_id}

    if args.entity_type:
        data["entity_type"] = args.entity_type
    else:
        data["entity_type"] = "stories"

    if args.id:
        data["id"] = args.id
    if args.name:
        data["name"] = args.name
    if args.status:
        data["status"] = args.status

    result = client.get_story_count(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_get_stories_fields_lable(args):
    """获取字段中英文对照"""
    client = TAPDClient()
    result = client.get_stories_fields_lable({"workspace_id": args.workspace_id})
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_get_stories_fields_info(args):
    """获取字段及候选值"""
    client = TAPDClient()
    result = client.get_stories_fields_info({"workspace_id": args.workspace_id})
    print(json.dumps(result, ensure_ascii=False, indent=2))


# ============ 缺陷相关 ============

def cmd_get_bug(args):
    """查询缺陷"""
    client = TAPDClient()
    data = {"workspace_id": args.workspace_id}

    if args.id:
        data["id"] = args.id
    if args.title:
        data["title"] = args.title
    if args.status:
        data["status"] = args.status
    if args.v_status:
        data["v_status"] = args.v_status
    if args.priority_label:
        data["priority_label"] = args.priority_label
    if args.severity:
        data["severity"] = args.severity
    if args.owner:
        data["owner"] = args.owner
    if args.limit:
        data["limit"] = args.limit
    if args.page:
        data["page"] = args.page

    # 获取详情时（指定 id）默认包含 description
    fields_param = args.fields
    if args.id:
        if not fields_param:
            fields_param = "description"
        elif "description" not in fields_param:
            fields_param = fields_param + ",description"
    data["fields"] = fields_param

    result = client.get_bug(data)
    count_result = client.get_bug_count(data)

    # 过滤字段
    fields_param = data.get('fields')
    if isinstance(result, dict) and 'data' in result:
        result['data'] = client.filter_fields(result['data'], fields_param)

    tapd_base_url = get_tapd_base_url()

    output = {
        "base_url": tapd_base_url,
        "data": result.get('data', []),
        "count": count_result
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


def cmd_create_bug(args):
    """创建缺陷"""
    client = TAPDClient()
    data = {
        "workspace_id": args.workspace_id,
        "title": args.title
    }

    if args.description:
        data["description"] = args.description
    if args.priority_label:
        data["priority_label"] = args.priority_label
    if args.severity:
        data["severity"] = args.severity
    if args.current_owner:
        data["current_owner"] = args.current_owner
    if args.cc:
        data["cc"] = args.cc
    if args.reporter:
        data["reporter"] = args.reporter
    if args.iteration_id:
        data["iteration_id"] = args.iteration_id
    if args.release_id:
        data["release_id"] = args.release_id
    if args.module:
        data["module"] = args.module
    if args.feature:
        data["feature"] = args.feature

    result = client.create_or_update_bug(data)

    tapd_base_url = get_tapd_base_url()
    bug_id = result.get("data", {}).get("Bug", {}).get("id")
    url = f"{tapd_base_url}/{args.workspace_id}/bugtrace/bugs/view/{bug_id}" if bug_id else ""

    output = {
        "url": url,
        "data": json.dumps(result, ensure_ascii=False, indent=2)
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


def cmd_update_bug(args):
    """更新缺陷"""
    client = TAPDClient()
    data = {
        "workspace_id": args.workspace_id,
        "id": args.id
    }

    if args.title:
        data["title"] = args.title
    if args.description:
        data["description"] = args.description
    if args.v_status:
        data["v_status"] = args.v_status
    if args.status:
        data["status"] = args.status
    if args.priority_label:
        data["priority_label"] = args.priority_label
    if args.severity:
        data["severity"] = args.severity
    if args.current_owner:
        data["current_owner"] = args.current_owner

    result = client.create_or_update_bug(data)

    tapd_base_url = get_tapd_base_url()

    output = {
        "base_url": tapd_base_url,
        "data": json.dumps(result, ensure_ascii=False, indent=2)
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


def cmd_get_bug_count(args):
    """获取缺陷数量"""
    client = TAPDClient()
    data = {"workspace_id": args.workspace_id}

    if args.title:
        data["title"] = args.title
    if args.status:
        data["status"] = args.status

    result = client.get_bug_count(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


# ============ 迭代相关 ============

def cmd_get_iterations(args):
    """查询迭代"""
    client = TAPDClient()
    data = {"workspace_id": args.workspace_id}

    if args.id:
        data["id"] = args.id
    if args.name:
        data["name"] = args.name
    if args.status:
        data["status"] = args.status

    result = client.get_iterations(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_create_iteration(args):
    """创建迭代"""
    client = TAPDClient()
    data = {
        "workspace_id": args.workspace_id,
        "name": args.name,
        "startdate": args.startdate,
        "enddate": args.enddate
    }

    if args.creator:
        data["creator"] = args.creator
    if args.description:
        data["description"] = args.description
    if args.status:
        data["status"] = args.status
    if args.label:
        data["label"] = args.label
    if args.parent_id:
        data["parent_id"] = args.parent_id

    result = client.create_or_update_iteration(data)

    tapd_base_url = get_tapd_base_url()
    iteration_id = result.get("data", {}).get("Iteration", {}).get("id")
    url = f"{tapd_base_url}/{args.workspace_id}/prong/iterations/card_view/{iteration_id}" if iteration_id else ""

    output = {
        "url": url,
        "data": json.dumps(result, ensure_ascii=False, indent=2)
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


def cmd_update_iteration(args):
    """更新迭代"""
    client = TAPDClient()
    data = {
        "workspace_id": args.workspace_id,
        "id": args.id,
        "current_user": args.current_user
    }

    if args.name:
        data["name"] = args.name
    if args.startdate:
        data["startdate"] = args.startdate
    if args.enddate:
        data["enddate"] = args.enddate
    if args.status:
        data["status"] = args.status

    result = client.create_or_update_iteration(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


# ============ 评论相关 ============

def cmd_get_comments(args):
    """查询评论"""
    client = TAPDClient()
    data = {"workspace_id": args.workspace_id}

    if args.id:
        data["id"] = args.id
    if args.entry_type:
        data["entry_type"] = args.entry_type
    if args.entry_id:
        data["entry_id"] = args.entry_id
    if args.author:
        data["author"] = args.author
    if args.limit:
        data["limit"] = args.limit
    if args.page:
        data["page"] = args.page

    result = client.get_comments(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_create_comments(args):
    """创建评论"""
    client = TAPDClient()
    data = {
        "workspace_id": args.workspace_id,
        "entry_type": args.entry_type,
        "entry_id": args.entry_id,
        "description": args.description
    }

    if args.author:
        data["author"] = args.author
    if args.root_id:
        data["root_id"] = args.root_id
    if args.reply_id:
        data["reply_id"] = args.reply_id

    result = client.create_comments(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_update_comments(args):
    """更新评论"""
    client = TAPDClient()
    data = {
        "workspace_id": args.workspace_id,
        "id": args.id,
        "description": args.description,
        "change_creator": args.change_creator
    }

    result = client.create_comments(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


# ============ 附件/图片相关 ============

def cmd_get_entity_attachments(args):
    """获取附件"""
    client = TAPDClient()
    data = {
        "workspace_id": args.workspace_id,
        "entry_id": args.entry_id,
        "type": args.type
    }

    result = client.get_attachments(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_get_image(args):
    """获取图片下载链接"""
    client = TAPDClient()
    data = {
        "workspace_id": args.workspace_id,
        "image_path": args.image_path
    }

    result = client.get_image(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


# ============ 自定义字段 ============

def cmd_get_entity_custom_fields(args):
    """获取自定义字段配置"""
    client = TAPDClient()
    data = {
        "workspace_id": args.workspace_id,
        "entity_type": args.entity_type
    }

    result = client.get_entity_custom_fields(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


# ============ 工作流相关 ============

def cmd_get_workflows_status_map(args):
    """获取状态映射"""
    client = TAPDClient()
    data = {
        "workspace_id": args.workspace_id,
        "system": args.system
    }
    if args.workitem_type_id:
        data["workitem_type_id"] = args.workitem_type_id

    result = client.get_workflows_status_map(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_get_workflows_all_transitions(args):
    """获取状态流转"""
    client = TAPDClient()
    data = {
        "workspace_id": args.workspace_id,
        "system": args.system
    }
    if args.workitem_type_id:
        data["workitem_type_id"] = args.workitem_type_id

    result = client.get_workflows_all_transitions(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_get_workflows_last_steps(args):
    """获取结束状态"""
    client = TAPDClient()
    data = {
        "workspace_id": args.workspace_id,
        "system": args.system
    }
    if args.workitem_type_id:
        data["workitem_type_id"] = args.workitem_type_id
    if args.type:
        data["type"] = args.type

    result = client.get_workflows_last_steps(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


# ============ 测试用例相关 ============

def cmd_get_tcases(args):
    """查询测试用例"""
    client = TAPDClient()
    data = {"workspace_id": args.workspace_id}

    if args.id:
        data["id"] = args.id
    if args.name:
        data["name"] = args.name
    if args.category_id:
        data["category_id"] = args.category_id
    if args.status:
        data["status"] = args.status
    if args.type:
        data["type"] = args.type
    if args.priority:
        data["priority"] = args.priority
    if args.limit:
        data["limit"] = args.limit
    if args.page:
        data["page"] = args.page

    result = client.get_tcases(data)
    count_result = client.get_tcases_count(data)

    tapd_base_url = get_tapd_base_url()

    output = {
        "base_url": tapd_base_url,
        "data": json.dumps(result, ensure_ascii=False, indent=2),
        "count": json.dumps(count_result, ensure_ascii=False, indent=2)
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


def cmd_create_or_update_tcases(args):
    """创建/更新测试用例"""
    client = TAPDClient()
    data = {"workspace_id": args.workspace_id}

    if args.id:
        data["id"] = args.id
    if args.name:
        data["name"] = args.name
    if args.category_id:
        data["category_id"] = args.category_id
    if args.status:
        data["status"] = args.status
    if args.precondition:
        data["precondition"] = args.precondition
    if args.steps:
        data["steps"] = args.steps
    if args.expectation:
        data["expectation"] = args.expectation
    if args.type:
        data["type"] = args.type
    if args.priority:
        data["priority"] = args.priority

    result = client.create_tcases(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_create_tcases_batch(args):
    """批量创建测试用例"""
    client = TAPDClient()

    if not args.tcases_json:
        print("错误: 需要提供 --tcases_json 参数")
        sys.exit(1)

    try:
        tcases = json.loads(args.tcases_json)
    except json.JSONDecodeError:
        print("错误: --tcases_json 必须是有效的 JSON 格式")
        sys.exit(1)

    for tcase in tcases:
        if 'workspace_id' not in tcase:
            tcase['workspace_id'] = args.workspace_id

    result = client.create_tcases_batch_save(tcases)
    print(json.dumps(result, ensure_ascii=False, indent=2))


# ============ Wiki 相关 ============

def cmd_get_wiki(args):
    """查询 Wiki"""
    client = TAPDClient()
    data = {"workspace_id": args.workspace_id}

    if args.id:
        data["id"] = args.id
    if args.name:
        data["name"] = args.name
    if args.creator:
        data["creator"] = args.creator
    if args.limit:
        data["limit"] = args.limit
    if args.page:
        data["page"] = args.page

    result = client.get_wiki(data)
    count_result = client.get_wiki_count(data)

    tapd_base_url = get_tapd_base_url()

    output = {
        "base_url": tapd_base_url,
        "data": json.dumps(result, ensure_ascii=False, indent=2),
        "count": json.dumps(count_result, ensure_ascii=False, indent=2)
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


def cmd_create_wiki(args):
    """创建 Wiki"""
    client = TAPDClient()
    data = {"workspace_id": args.workspace_id}

    if args.name:
        data["name"] = args.name
    if args.markdown_description:
        data["markdown_description"] = args.markdown_description
    if args.creator:
        data["creator"] = args.creator
    if args.note:
        data["note"] = args.note
    if args.parent_wiki_id:
        data["parent_wiki_id"] = args.parent_wiki_id

    result = client.create_wiki(data)

    tapd_base_url = get_tapd_base_url()
    wiki_id = result.get("data", {}).get("Wiki", {}).get("id")
    url = f"{tapd_base_url}/{args.workspace_id}/markdown_wikis/show/#{wiki_id}" if wiki_id else ""

    output = {
        "url": url,
        "data": json.dumps(result, ensure_ascii=False, indent=2)
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


def cmd_update_wiki(args):
    """更新 Wiki"""
    client = TAPDClient()
    data = {"workspace_id": args.workspace_id}

    if args.id:
        data["id"] = args.id
    if args.name:
        data["name"] = args.name
    if args.markdown_description:
        data["markdown_description"] = args.markdown_description
    if args.note:
        data["note"] = args.note
    if args.parent_wiki_id:
        data["parent_wiki_id"] = args.parent_wiki_id

    result = client.create_wiki(data)

    tapd_base_url = get_tapd_base_url()
    wiki_id = result.get("data", {}).get("Wiki", {}).get("id")
    url = f"{tapd_base_url}/{args.workspace_id}/markdown_wikis/show/#{wiki_id}" if wiki_id else ""

    output = {
        "url": url,
        "data": json.dumps(result, ensure_ascii=False, indent=2)
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


# ============ 工时相关 ============

def cmd_get_timesheets(args):
    """查询工时"""
    client = TAPDClient()
    data = {"workspace_id": args.workspace_id}

    if args.entity_type:
        data["entity_type"] = args.entity_type
    if args.entity_id:
        data["entity_id"] = args.entity_id
    if args.owner:
        data["owner"] = args.owner
    if args.spentdate:
        data["spentdate"] = args.spentdate
    if args.limit:
        data["limit"] = args.limit
    if args.page:
        data["page"] = args.page

    result = client.get_timesheets(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_add_timesheets(args):
    """填写工时"""
    client = TAPDClient()
    data = {
        "workspace_id": args.workspace_id,
        "entity_type": args.entity_type,
        "entity_id": args.entity_id,
        "timespent": args.timespent,
        "spentdate": args.spentdate
    }

    if args.owner:
        data["owner"] = args.owner
    if args.memo:
        data["memo"] = args.memo
    if args.timeremain:
        data["timeremain"] = args.timeremain

    result = client.update_timesheets(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_update_timesheets(args):
    """更新工时"""
    client = TAPDClient()
    data = {
        "workspace_id": args.workspace_id,
        "id": args.id,
        "timespent": args.timespent
    }

    if args.memo:
        data["memo"] = args.memo
    if args.timeremain:
        data["timeremain"] = args.timeremain

    result = client.update_timesheets(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


# ============ 待办相关 ============

def cmd_get_todo(args):
    """获取待办"""
    client = TAPDClient()
    data = {
        "entity_type": args.entity_type,
        "user_nick": args.user_nick or client.nick
    }

    result = client.get_todo(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


# ============ 关联相关 ============

def cmd_get_related_bugs(args):
    """获取关联缺陷"""
    client = TAPDClient()
    data = {
        "workspace_id": args.workspace_id,
        "story_id": args.story_id
    }

    result = client.get_related_bugs(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_entity_relations(args):
    """创建关联关系"""
    client = TAPDClient()
    data = {
        "workspace_id": args.workspace_id,
        "source_type": args.source_type,
        "target_type": args.target_type,
        "source_id": args.source_id,
        "target_id": args.target_id
    }

    result = client.add_entity_relations(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


# ============ 发布计划 ============

def cmd_get_release_info(args):
    """获取发布计划"""
    client = TAPDClient()
    data = {"workspace_id": args.workspace_id}

    if args.id:
        data["id"] = args.id
    if args.name:
        data["name"] = args.name
    if args.status:
        data["status"] = args.status
    if args.limit:
        data["limit"] = args.limit

    result = client.get_release_info(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


# ============ 源码提交关键字 ============

def cmd_get_commit_msg(args):
    """获取提交关键字"""
    client = TAPDClient()
    data = {
        "workspace_id": args.workspace_id,
        "object_id": args.object_id,
        "type": args.type
    }

    result = client.get_scm_copy_keywords(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


# ============ 企业微信消息 ============

def cmd_send_qiwei_message(args):
    """发送企业微信消息"""
    client = TAPDClient()
    result = client.send_message({"msg": args.msg})
    print(result)


# ============ 主程序 ============

def build_parser():
    """构建命令行解析器"""
    parser = argparse.ArgumentParser(
        description="TAPD 统一命令行工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        add_help=False
    )
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")

    subparsers = parser.add_subparsers(dest="command", title="命令")

    # ============ 项目相关 ============
    p = subparsers.add_parser("get_user_participant_projects", help="获取用户参与的项目列表")
    p.add_argument("--nick", help="用户昵称")

    p = subparsers.add_parser("get_workspace_info", help="获取项目信息")
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")

    p = subparsers.add_parser("get_workitem_types", help="获取需求类别")
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--id", help="ID")
    p.add_argument("--name", help="需求类别名称")

    # ============ 需求/任务 ============
    p = subparsers.add_parser("get_stories_or_tasks", help="查询需求/任务")
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--entity_type", choices=["stories", "tasks"], help="类型")
    p.add_argument("--id", help="ID")
    p.add_argument("--name", help="标题（模糊匹配）")
    p.add_argument("--status", help="状态")
    p.add_argument("--v_status", help="状态（中文）")
    p.add_argument("--owner", help="处理人")
    p.add_argument("--creator", help="创建人")
    p.add_argument("--priority_label", help="优先级")
    p.add_argument("--iteration_id", help="迭代ID")
    p.add_argument("--limit", type=int, default=10, help="返回数量限制")
    p.add_argument("--page", type=int, default=1, help="页码")
    p.add_argument("--fields", help="字段列表")

    p = subparsers.add_parser("create_story_or_task", help="创建需求/任务")
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--name", required=True, help="标题")
    p.add_argument("--entity_type", choices=["stories", "tasks"], help="类型")
    p.add_argument("--description", help="描述")
    p.add_argument("--priority_label", help="优先级")
    p.add_argument("--owner", help="处理人")
    p.add_argument("--iteration_id", help="迭代ID")
    p.add_argument("--iteration_name", help="迭代名称")
    p.add_argument("--category_id", help="需求分类ID")
    p.add_argument("--workitem_type_id", help="需求类别ID")
    p.add_argument("--release_id", help="发布计划ID")
    p.add_argument("--parent_id", help="父需求ID")
    p.add_argument("--story_id", help="关联需求ID（任务）")
    p.add_argument("--size", help="规模点")
    p.add_argument("--version", help="版本")
    p.add_argument("--module", help="模块")

    p = subparsers.add_parser("update_story_or_task", help="更新需求/任务")
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--id", required=True, help="需求/任务ID")
    p.add_argument("--entity_type", choices=["stories", "tasks"], help="类型")
    p.add_argument("--name", help="标题")
    p.add_argument("--description", help="描述")
    p.add_argument("--v_status", help="状态（中文）")
    p.add_argument("--status", help="状态")
    p.add_argument("--priority_label", help="优先级")
    p.add_argument("--owner", help="处理人")

    p = subparsers.add_parser("get_story_or_task_count", help="获取需求/任务数量")
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--entity_type", choices=["stories", "tasks"], help="类型")
    p.add_argument("--id", help="ID")
    p.add_argument("--name", help="标题")
    p.add_argument("--status", help="状态")

    p = subparsers.add_parser("get_stories_fields_lable", help="获取字段中英文对照")
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")

    p = subparsers.add_parser("get_stories_fields_info", help="获取字段及候选值")
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")

    # ============ 缺陷 ============
    p = subparsers.add_parser("get_bug", help="查询缺陷")
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--id", help="ID")
    p.add_argument("--title", help="标题（模糊匹配）")
    p.add_argument("--status", help="状态")
    p.add_argument("--v_status", help="状态（中文）")
    p.add_argument("--priority_label", help="优先级")
    p.add_argument("--severity", help="严重程度")
    p.add_argument("--owner", help="处理人")
    p.add_argument("--limit", type=int, default=10, help="返回数量限制")
    p.add_argument("--page", type=int, default=1, help="页码")
    p.add_argument("--fields", help="字段列表")

    p = subparsers.add_parser("create_bug", help="创建缺陷")
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--title", required=True, help="标题")
    p.add_argument("--description", help="描述")
    p.add_argument("--priority_label", help="优先级")
    p.add_argument("--severity", help="严重程度")
    p.add_argument("--current_owner", help="处理人")
    p.add_argument("--cc", help="抄送人")
    p.add_argument("--reporter", help="创建人")
    p.add_argument("--iteration_id", help="迭代ID")
    p.add_argument("--release_id", help="发布计划ID")
    p.add_argument("--module", help="模块")
    p.add_argument("--feature", help="特性")

    p = subparsers.add_parser("update_bug", help="更新缺陷")
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--id", required=True, help="缺陷ID")
    p.add_argument("--title", help="标题")
    p.add_argument("--description", help="描述")
    p.add_argument("--v_status", help="状态（中文）")
    p.add_argument("--status", help="状态")
    p.add_argument("--priority_label", help="优先级")
    p.add_argument("--severity", help="严重程度")
    p.add_argument("--current_owner", help="处理人")

    p = subparsers.add_parser("get_bug_count", help="获取缺陷数量")
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--title", help="标题")
    p.add_argument("--status", help="状态")

    # ============ 迭代 ============
    p = subparsers.add_parser("get_iterations", help="查询迭代")
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--id", help="ID")
    p.add_argument("--name", help="名称")
    p.add_argument("--status", help="状态")

    p = subparsers.add_parser("create_iteration", help="创建迭代")
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--name", required=True, help="名称")
    p.add_argument("--startdate", required=True, help="开始日期")
    p.add_argument("--enddate", required=True, help="结束日期")
    p.add_argument("--creator", help="创建人")
    p.add_argument("--description", help="描述")
    p.add_argument("--status", help="状态")
    p.add_argument("--label", help="标签")
    p.add_argument("--parent_id", help="父迭代ID")

    p = subparsers.add_parser("update_iteration", help="更新迭代")
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--id", required=True, help="迭代ID")
    p.add_argument("--current_user", required=True, help="变更人")
    p.add_argument("--name", help="名称")
    p.add_argument("--startdate", help="开始日期")
    p.add_argument("--enddate", help="结束日期")
    p.add_argument("--status", help="状态")

    # ============ 评论 ============
    p = subparsers.add_parser("get_comments", help="查询评论")
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--id", help="评论ID")
    p.add_argument("--entry_type", help="评论类型")
    p.add_argument("--entry_id", help="业务对象ID")
    p.add_argument("--author", help="评论人")
    p.add_argument("--limit", type=int, default=30, help="返回数量限制")
    p.add_argument("--page", type=int, default=1, help="页码")

    p = subparsers.add_parser("create_comments", help="创建评论")
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--entry_type", required=True, help="评论类型")
    p.add_argument("--entry_id", required=True, help="业务对象ID")
    p.add_argument("--description", required=True, help="内容")
    p.add_argument("--author", help="评论人")
    p.add_argument("--root_id", help="根评论ID")
    p.add_argument("--reply_id", help="回复ID")

    p = subparsers.add_parser("update_comments", help="更新评论")
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--id", required=True, help="评论ID")
    p.add_argument("--description", required=True, help="内容")
    p.add_argument("--change_creator", required=True, help="变更人")

    # ============ 附件/图片 ============
    p = subparsers.add_parser("get_entity_attachments", help="获取附件")
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--entry_id", required=True, help="业务对象ID")
    p.add_argument("--type", required=True, help="业务对象类型")

    p = subparsers.add_parser("get_image", help="获取图片下载链接")
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--image_path", required=True, help="图片路径")

    # ============ 自定义字段 ============
    p = subparsers.add_parser("get_entity_custom_fields", help="获取自定义字段配置")
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--entity_type", required=True, help="实体类型")

    # ============ 工作流 ============
    p = subparsers.add_parser("get_workflows_status_map", help="获取状态映射")
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--system", required=True, help="系统名 (bug/story)")
    p.add_argument("--workitem_type_id", help="需求类别ID")

    p = subparsers.add_parser("get_workflows_all_transitions", help="获取状态流转")
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--system", required=True, help="系统名 (bug/story)")
    p.add_argument("--workitem_type_id", help="需求类别ID")

    p = subparsers.add_parser("get_workflows_last_steps", help="获取结束状态")
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--system", required=True, help="系统名 (bug/story)")
    p.add_argument("--workitem_type_id", help="需求类别ID")
    p.add_argument("--type", help="节点类型")

    # ============ 测试用例 ============
    p = subparsers.add_parser("get_tcases", help="查询测试用例")
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--id", help="ID")
    p.add_argument("--name", help="名称")
    p.add_argument("--category_id", help="用例目录ID")
    p.add_argument("--status", help="状态")
    p.add_argument("--type", help="用例类型")
    p.add_argument("--priority", help="用例等级")
    p.add_argument("--limit", type=int, default=30, help="返回数量限制")
    p.add_argument("--page", type=int, default=1, help="页码")

    p = subparsers.add_parser("create_or_update_tcases", help="创建/更新测试用例")
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--id", help="测试用例ID")
    p.add_argument("--name", help="名称")
    p.add_argument("--category_id", help="用例目录ID")
    p.add_argument("--status", help="状态")
    p.add_argument("--precondition", help="前置条件")
    p.add_argument("--steps", help="用例步骤")
    p.add_argument("--expectation", help="预期结果")
    p.add_argument("--type", help="用例类型")
    p.add_argument("--priority", help="用例等级")

    p = subparsers.add_parser("create_tcases_batch", help="批量创建测试用例")
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--tcases_json", required=True, help="测试用例列表 (JSON格式)")

    # ============ Wiki ============
    p = subparsers.add_parser("get_wiki", help="查询 Wiki")
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--id", help="ID")
    p.add_argument("--name", help="标题")
    p.add_argument("--creator", help="创建人")
    p.add_argument("--limit", type=int, default=30, help="返回数量限制")
    p.add_argument("--page", type=int, default=1, help="页码")

    p = subparsers.add_parser("create_wiki", help="创建 Wiki")
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--name", required=True, help="标题")
    p.add_argument("--markdown_description", help="内容")
    p.add_argument("--creator", help="创建人")
    p.add_argument("--note", help="备注")
    p.add_argument("--parent_wiki_id", help="父Wiki ID")

    p = subparsers.add_parser("update_wiki", help="更新 Wiki")
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--id", required=True, help="Wiki ID")
    p.add_argument("--name", help="标题")
    p.add_argument("--markdown_description", help="内容")
    p.add_argument("--note", help="备注")
    p.add_argument("--parent_wiki_id", help="父Wiki ID")

    # ============ 工时 ============
    p = subparsers.add_parser("get_timesheets", help="查询工时")
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--entity_type", help="对象类型")
    p.add_argument("--entity_id", help="对象ID")
    p.add_argument("--owner", help="创建人")
    p.add_argument("--spentdate", help="日期")
    p.add_argument("--limit", type=int, default=30, help="返回数量限制")
    p.add_argument("--page", type=int, default=1, help="页码")

    p = subparsers.add_parser("add_timesheets", help="填写工时")
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--entity_type", required=True, help="对象类型")
    p.add_argument("--entity_id", required=True, help="对象ID")
    p.add_argument("--timespent", required=True, help="花费工时")
    p.add_argument("--spentdate", required=True, help="日期")
    p.add_argument("--owner", help="创建人")
    p.add_argument("--memo", help="备注")
    p.add_argument("--timeremain", help="剩余工时")

    p = subparsers.add_parser("update_timesheets", help="更新工时")
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--id", required=True, help="工时ID")
    p.add_argument("--timespent", required=True, help="花费工时")
    p.add_argument("--memo", help="备注")
    p.add_argument("--timeremain", help="剩余工时")

    # ============ 待办 ============
    p = subparsers.add_parser("get_todo", help="获取待办")
    p.add_argument("--entity_type", required=True, help="对象类型 (story/bug/task)")
    p.add_argument("--user_nick", help="用户昵称")

    # ============ 关联 ============
    p = subparsers.add_parser("get_related_bugs", help="获取关联缺陷")
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--story_id", required=True, help="需求ID")

    p = subparsers.add_parser("entity_relations", help="创建关联关系")
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--source_type", required=True, help="源对象类型")
    p.add_argument("--target_type", required=True, help="目标对象类型")
    p.add_argument("--source_id", required=True, help="源对象ID")
    p.add_argument("--target_id", required=True, help="目标对象ID")

    # ============ 发布计划 ============
    p = subparsers.add_parser("get_release_info", help="获取发布计划")
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--id", help="发布计划ID")
    p.add_argument("--name", help="名称")
    p.add_argument("--status", help="状态")
    p.add_argument("--limit", type=int, default=30, help="返回数量限制")

    # ============ 源码 ============
    p = subparsers.add_parser("get_commit_msg", help="获取提交关键字")
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--object_id", required=True, help="对象ID")
    p.add_argument("--type", required=True, help="对象类型 (story/task/bug)")

    # ============ 消息 ============
    p = subparsers.add_parser("send_qiwei_message", help="发送企业微信消息")
    p.add_argument("--msg", required=True, help="消息内容 (Markdown格式)")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if not args.command:
        print(__doc__)
        sys.exit(0)

    cmd = args.command

    # 根据命令分发
    if cmd == "get_user_participant_projects":
        cmd_get_user_participant_projects(args)
    elif cmd == "get_workspace_info":
        cmd_get_workspace_info(args)
    elif cmd == "get_workitem_types":
        cmd_get_workitem_types(args)
    elif cmd == "get_stories_or_tasks":
        cmd_get_stories_or_tasks(args)
    elif cmd == "create_story_or_task":
        cmd_create_story_or_task(args)
    elif cmd == "update_story_or_task":
        cmd_update_story_or_task(args)
    elif cmd == "get_story_or_task_count":
        cmd_get_story_or_task_count(args)
    elif cmd == "get_stories_fields_lable":
        cmd_get_stories_fields_lable(args)
    elif cmd == "get_stories_fields_info":
        cmd_get_stories_fields_info(args)
    elif cmd == "get_bug":
        cmd_get_bug(args)
    elif cmd == "create_bug":
        cmd_create_bug(args)
    elif cmd == "update_bug":
        cmd_update_bug(args)
    elif cmd == "get_bug_count":
        cmd_get_bug_count(args)
    elif cmd == "get_iterations":
        cmd_get_iterations(args)
    elif cmd == "create_iteration":
        cmd_create_iteration(args)
    elif cmd == "update_iteration":
        cmd_update_iteration(args)
    elif cmd == "get_comments":
        cmd_get_comments(args)
    elif cmd == "create_comments":
        cmd_create_comments(args)
    elif cmd == "update_comments":
        cmd_update_comments(args)
    elif cmd == "get_entity_attachments":
        cmd_get_entity_attachments(args)
    elif cmd == "get_image":
        cmd_get_image(args)
    elif cmd == "get_entity_custom_fields":
        cmd_get_entity_custom_fields(args)
    elif cmd == "get_workflows_status_map":
        cmd_get_workflows_status_map(args)
    elif cmd == "get_workflows_all_transitions":
        cmd_get_workflows_all_transitions(args)
    elif cmd == "get_workflows_last_steps":
        cmd_get_workflows_last_steps(args)
    elif cmd == "get_tcases":
        cmd_get_tcases(args)
    elif cmd == "create_or_update_tcases":
        cmd_create_or_update_tcases(args)
    elif cmd == "create_tcases_batch":
        cmd_create_tcases_batch(args)
    elif cmd == "get_wiki":
        cmd_get_wiki(args)
    elif cmd == "create_wiki":
        cmd_create_wiki(args)
    elif cmd == "update_wiki":
        cmd_update_wiki(args)
    elif cmd == "get_timesheets":
        cmd_get_timesheets(args)
    elif cmd == "add_timesheets":
        cmd_add_timesheets(args)
    elif cmd == "update_timesheets":
        cmd_update_timesheets(args)
    elif cmd == "get_todo":
        cmd_get_todo(args)
    elif cmd == "get_related_bugs":
        cmd_get_related_bugs(args)
    elif cmd == "entity_relations":
        cmd_entity_relations(args)
    elif cmd == "get_release_info":
        cmd_get_release_info(args)
    elif cmd == "get_commit_msg":
        cmd_get_commit_msg(args)
    elif cmd == "send_qiwei_message":
        cmd_send_qiwei_message(args)
    else:
        print(f"未知命令: {cmd}")
        print("使用 'python tapd.py --help' 查看帮助")
        sys.exit(1)


if __name__ == "__main__":
    main()
