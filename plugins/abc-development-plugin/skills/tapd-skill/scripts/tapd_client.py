"""
TAPD API 客户端封装

使用前请设置环境变量：
- TAPD_ACCESS_TOKEN: 个人访问令牌（推荐）
- TAPD_API_USER: API 账号
- TAPD_API_PASSWORD: API 密钥
- TAPD_API_BASE_URL: API 地址（默认 https://api.tapd.cn）
- TAPD_BASE_URL: TAPD Web 地址（默认 https://www.tapd.cn）
- CURRENT_USER_NICK: 当前用户昵称
"""

import os
import base64
import json
from typing import Optional, Dict, Any, List
import requests


def check_env_vars():
    """检查环境变量是否已设置"""
    access_token = os.getenv("TAPD_ACCESS_TOKEN")
    api_user = os.getenv("TAPD_API_USER")
    api_password = os.getenv("TAPD_API_PASSWORD")
    return access_token or (api_user and api_password)


def get_env_check_message():
    """获取环境变量检查消息"""
    access_token = os.getenv("TAPD_ACCESS_TOKEN")
    api_user = os.getenv("TAPD_API_USER")

    if access_token or api_user:
        return None

    return """
错误: TAPD 访问凭证未设置

请先设置以下环境变量之一：

方案 1：使用个人访问令牌（推荐）
  export TAPD_ACCESS_TOKEN="你的个人访问令牌"
  获取方式：https://www.tapd.cn/personal_settings/index?tab=personal_token

方案 2：使用 API 账号密码
  export TAPD_API_USER="你的API账号"
  export TAPD_API_PASSWORD="你的API密钥"

设置后重新运行脚本。
"""


class TAPDClient:
    """TAPD API 客户端"""

    def __init__(self):
        # 检查环境变量
        env_msg = get_env_check_message()
        if env_msg:
            print(env_msg)
            raise ValueError("TAPD 访问凭证未设置")

        self.access_token = os.getenv("TAPD_ACCESS_TOKEN")
        self.api_user = os.getenv("TAPD_API_USER")
        self.api_password = os.getenv("TAPD_API_PASSWORD")
        self.base_url = os.getenv("TAPD_API_BASE_URL", "https://api.tapd.cn")
        self.nick = os.getenv("CURRENT_USER_NICK")

        if self.access_token:
            self.headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json",
                "Via": "mcp"
            }
            self.nick = self.get_user_info() or self.nick
        elif self.api_user and self.api_password:
            auth_str = f"{self.api_user}:{self.api_password}"
            self.headers = {
                "Authorization": f"Basic {base64.b64encode(auth_str.encode()).decode()}",
                "Content-Type": "application/json",
                "Via": "mcp"
            }

    def _make_request(self, method: str, endpoint: str,
                      params: Optional[Dict] = None,
                      data: Optional[Dict] = None) -> Dict:
        """发送 API 请求"""
        url = f"{self.base_url}/{endpoint}"
        separator = '&' if '?' in url else '?'
        url = f"{url}{separator}s=mcp"

        response = requests.request(
            method=method,
            url=url,
            headers=self.headers,
            params=params,
            json=data,
            timeout=30
        )
        response.raise_for_status()
        return response.json()

    def is_cloud_env(self) -> bool:
        """判断是否为 CLOUD 环境"""
        return 'api.tapd.cn' in self.base_url

    def _to_long_id(self, single_id: str, workspace_id: str) -> str:
        """将短 ID 转换为长 ID"""
        single_id = single_id.strip()
        if single_id.isdigit() and len(single_id) <= 9:
            padded_id = single_id.zfill(9)
            pre_id = "11" if self.is_cloud_env() else "10"
            return f"{pre_id}{workspace_id}{padded_id}"
        return single_id

    def _convert_id(self, params: Dict, key: str, workspace_id: str):
        """转换 ID 为长 ID"""
        if key in params and workspace_id:
            id_val = str(params[key])
            if "," in id_val:
                id_list = id_val.split(",")
                params[key] = ",".join([self._to_long_id(i, workspace_id) for i in id_list])
            else:
                params[key] = self._to_long_id(id_val, workspace_id)

    # ============ 用户相关 ============

    def get_user_info(self) -> Optional[str]:
        """获取用户信息"""
        try:
            response = self._make_request("GET", "users/info")
            return response.get("data", {}).get("nick")
        except:
            return None

    def get_user_participant_projects(self, data: Dict) -> Dict:
        """获取用户参与的项目列表"""
        return self._make_request("GET", "workspaces/user_participant_projects", params=data)

    # ============ 项目相关 ============

    def get_workspace_info(self, data: Dict) -> Dict:
        """获取项目信息"""
        workspace_id = data.get("workspace_id")
        return self._make_request("GET", f"workspaces/get_workspace_info?workspace_id={workspace_id}")

    def get_workitem_types(self, data: Dict) -> Dict:
        """获取需求类别"""
        workspace_id = data.get("workspace_id")
        return self._make_request("GET", f"workitem_types?workspace_id={workspace_id}", params=data)

    # ============ 需求/任务相关 ============

    def get_stories(self, params: Dict) -> Dict:
        """获取需求或任务"""
        entity_type = params.get("entity_type", "stories")
        workspace_id = str(params.get("workspace_id", ""))

        self._convert_id(params, "id", workspace_id)

        default_params = {"page": 1, "limit": 10}
        default_params.update(params)
        return self._make_request("GET", entity_type, params=default_params)

    def get_story_count(self, params: Dict) -> Dict:
        """获取需求数量"""
        entity_type = params.get("entity_type", "stories")
        return self._make_request("GET", f"{entity_type}/count", params=params)

    def create_or_update_story(self, data: Dict) -> Dict:
        """创建/更新需求或任务"""
        entity_type = data.get("entity_type", "stories")
        workspace_id = str(data.get("workspace_id", ""))

        self._convert_id(data, "id", workspace_id)

        if self.nick:
            if 'id' in data:
                data['current_user'] = self.nick
            else:
                data['creator'] = self.nick

        return self._make_request("POST", entity_type, data=data)

    def get_stories_fields_lable(self, data: Dict) -> Dict:
        """获取字段中英文对照"""
        workspace_id = data.get("workspace_id")
        return self._make_request("GET", f"stories/get_fields_lable?workspace_id={workspace_id}")

    def get_stories_fields_info(self, data: Dict) -> Dict:
        """获取字段及候选值"""
        workspace_id = data.get("workspace_id")
        return self._make_request("GET", f"stories/get_fields_info?workspace_id={workspace_id}")

    # ============ 缺陷相关 ============

    def get_bug(self, params: Dict) -> Dict:
        """获取缺陷"""
        workspace_id = str(params.get("workspace_id", ""))
        self._convert_id(params, "id", workspace_id)

        default_params = {"page": 1, "limit": 10}
        default_params.update(params)
        return self._make_request("GET", "bugs", params=default_params)

    def get_bug_count(self, params: Dict) -> Dict:
        """获取缺陷数量"""
        return self._make_request("GET", "bugs/count", params=params)

    def create_or_update_bug(self, data: Dict) -> Dict:
        """创建或更新缺陷"""
        workspace_id = str(data.get("workspace_id", ""))
        self._convert_id(data, "id", workspace_id)

        if self.nick:
            if 'id' in data:
                data['current_user'] = self.nick
            else:
                data['reporter'] = self.nick

        return self._make_request("POST", "bugs", data=data)

    # ============ 迭代相关 ============

    def get_iterations(self, data: Dict) -> Dict:
        """获取迭代"""
        workspace_id = data.get("workspace_id")
        params = f"?workspace_id={workspace_id}"
        if 'id' in data:
            params += f"&id={data['id']}"
        if 'name' in data:
            params += f"&name={data['name']}"
        return self._make_request("GET", f"iterations{params}", params=data)

    def create_or_update_iteration(self, data: Dict) -> Dict:
        """创建/更新迭代"""
        if self.nick:
            if 'id' in data:
                data['current_user'] = self.nick
            else:
                data['creator'] = self.nick
        return self._make_request("POST", "iterations", data=data)

    # ============ 评论相关 ============

    def get_comments(self, params: Dict) -> Dict:
        """获取评论"""
        default_params = {"page": 1, "limit": 10}
        default_params.update(params)
        return self._make_request("GET", "comments", params=default_params)

    def create_comments(self, data: Dict) -> Dict:
        """创建评论"""
        workspace_id = str(data.get("workspace_id", ""))
        self._convert_id(data, "entry_id", workspace_id)

        if self.nick:
            if 'id' in data:
                data['change_creator'] = self.nick
            else:
                data['author'] = self.nick

        return self._make_request("POST", "comments", data=data)

    # ============ 附件相关 ============

    def get_attachments(self, params: Dict) -> Dict:
        """获取附件"""
        return self._make_request("GET", "attachments", params=params)

    def get_attachment_download_url(self, params: Dict) -> Dict:
        """获取附件下载链接"""
        return self._make_request("GET", "attachments/down", params=params)

    def get_image(self, params: Dict) -> Dict:
        """获取图片下载链接"""
        return self._make_request("GET", "files/get_image", params=params)

    # ============ 自定义字段 ============

    def get_entity_custom_fields(self, data: Dict) -> Dict:
        """获取自定义字段配置"""
        workspace_id = data.get("workspace_id")
        entity_type = data.get("entity_type", "stories")
        return self._make_request("GET", f"{entity_type}/custom_fields_settings?workspace_id={workspace_id}")

    # ============ 工作流相关 ============

    def get_workflows_status_map(self, data: Dict) -> Dict:
        """获取状态映射"""
        workspace_id = data.get("workspace_id")
        system = data.get("system")
        params = f"?workspace_id={workspace_id}&system={system}"
        if 'workitem_type_id' in data:
            params += f"&workitem_type_id={data['workitem_type_id']}"
        return self._make_request("GET", f"workflows/status_map{params}")

    def get_workflows_all_transitions(self, data: Dict) -> Dict:
        """获取状态流转"""
        workspace_id = data.get("workspace_id")
        system = data.get("system")
        params = f"?workspace_id={workspace_id}&system={system}"
        if 'workitem_type_id' in data:
            params += f"&workitem_type_id={data['workitem_type_id']}"
        return self._make_request("GET", f"workflows/all_transitions{params}")

    def get_workflows_last_steps(self, data: Dict) -> Dict:
        """获取结束状态"""
        workspace_id = data.get("workspace_id")
        system = data.get("system")
        params = f"?workspace_id={workspace_id}&system={system}"
        if 'workitem_type_id' in data:
            params += f"&workitem_type_id={data['workitem_type_id']}"
        if 'type' in data:
            params += f"&type={data['type']}"
        return self._make_request("GET", f"workflows/last_steps{params}")

    # ============ 测试用例相关 ============

    def get_tcases(self, params: Dict) -> Dict:
        """获取测试用例"""
        default_params = {"page": 1, "limit": 30}
        default_params.update(params)
        return self._make_request("GET", "tcases", params=default_params)

    def get_tcases_count(self, params: Dict) -> Dict:
        """获取测试用例数量"""
        return self._make_request("GET", "tcases/count", params=params)

    def create_tcases(self, data: Dict) -> Dict:
        """创建测试用例"""
        if self.nick:
            if 'id' in data:
                data['modifier'] = self.nick
            else:
                data['creator'] = self.nick
        return self._make_request("POST", "tcases", data=data)

    def create_tcases_batch_save(self, data: List[Dict]) -> Dict:
        """批量创建测试用例"""
        if self.nick:
            for tcase in data:
                tcase.setdefault('creator', self.nick)
        return self._make_request("POST", "tcases/batch_save", data=data)

    # ============ Wiki 相关 ============

    def get_wiki(self, params: Dict) -> Dict:
        """获取 Wiki"""
        default_params = {"page": 1, "limit": 30}
        default_params.update(params)
        return self._make_request("GET", "tapd_wikis", params=default_params)

    def get_wiki_count(self, params: Dict) -> Dict:
        """获取 Wiki 数量"""
        return self._make_request("GET", "tapd_wikis/count", params=params)

    def create_wiki(self, data: Dict) -> Dict:
        """创建/更新 Wiki"""
        if self.nick:
            if 'id' in data:
                data['modifier'] = self.nick
            else:
                data['creator'] = self.nick
        return self._make_request("POST", "tapd_wikis", data=data)

    # ============ 工时相关 ============

    def get_timesheets(self, params: Dict) -> Dict:
        """获取工时"""
        return self._make_request("GET", "timesheets", params=params)

    def update_timesheets(self, data: Dict) -> Dict:
        """创建/更新工时"""
        if self.nick:
            data['owner'] = self.nick
        return self._make_request("POST", "timesheets", data=data)

    # ============ 待办相关 ============

    def get_todo(self, data: Dict) -> Dict:
        """获取待办"""
        entity_type = data.get("entity_type")
        user_nick = data.get("user_nick", self.nick)
        return self._make_request("GET", f"users/todo/{user_nick}/{entity_type}")

    # ============ 关联相关 ============

    def get_related_bugs(self, data: Dict) -> Dict:
        """获取关联缺陷"""
        return self._make_request("GET", "stories/get_related_bugs", params=data)

    def add_entity_relations(self, data: Dict) -> Dict:
        """创建关联关系"""
        return self._make_request("POST", "relations", data=data)

    # ============ 发布计划 ============

    def get_release_info(self, params: Dict) -> Dict:
        """获取发布计划"""
        return self._make_request("GET", "releases", params=params)

    # ============ 源码提交关键字 ============

    def get_scm_copy_keywords(self, data: Dict) -> Dict:
        """获取提交关键字"""
        workspace_id = str(data.get("workspace_id", ""))
        self._convert_id(data, "object_id", workspace_id)
        return self._make_request("GET", "svn_commits/get_scm_copy_keywords", params=data)

    # ============ 企业微信消息 ============

    def send_message(self, data: Dict) -> str:
        """发送企业微信消息"""
        import requests as req
        bot_url = os.getenv("BOT_URL")
        msg = data.get("msg", "")

        if '@' in msg:
            chat_data = {
                'msgtype': 'markdown',
                'markdown': {'content': msg}
            }
        else:
            chat_data = {
                'msgtype': 'markdown_v2',
                'markdown_v2': {'content': msg}
            }

        response = req.post(
            url=bot_url,
            headers={'Content-Type': 'application/json'},
            json=chat_data,
            timeout=500
        )
        return response.text

    # ============ 分类相关 ============

    def get_category_id(self, data: Dict) -> Dict:
        """获取需求分类 ID"""
        return self._make_request("GET", "story_categories", params=data)

    # ============ 工具方法 ============

    def filter_fields(self, data_list: List, fields_param: Optional[str] = None) -> List:
        """过滤字段"""
        if not data_list:
            return data_list

        if isinstance(fields_param, str):
            fields = [f.strip() for f in fields_param.split(',') if f.strip()]
        elif isinstance(fields_param, list):
            fields = fields_param
        else:
            fields = []

        filtered = []
        for item in data_list:
            if isinstance(item, dict):
                if 'Story' in item and isinstance(item['Story'], dict):
                    obj = item['Story']
                elif 'Bug' in item and isinstance(item['Bug'], dict):
                    obj = item['Bug']
                elif 'Task' in item and isinstance(item['Task'], dict):
                    obj = item['Task']
                elif 'Iteration' in item and isinstance(item['Iteration'], dict):
                    obj = item['Iteration']
                else:
                    obj = item

                new_obj = {}
                for k, v in obj.items():
                    if k.startswith('custom_field_') and (v is None or v == '') and (not fields_param or k not in fields):
                        continue
                    if k.startswith('description') and 'Iteration' not in item and (not fields_param or k not in fields):
                        continue
                    if k.startswith('custom_plan_field_') and v == '0':
                        continue
                    new_obj[k] = v

                if 'Story' in item:
                    filtered.append({'Story': new_obj})
                elif 'Bug' in item:
                    filtered.append({'Bug': new_obj})
                elif 'Task' in item:
                    filtered.append({'Task': new_obj})
                elif 'Iteration' in item:
                    filtered.append({'Iteration': new_obj})
                else:
                    filtered.append(new_obj)
            else:
                filtered.append(item)
        return filtered

    def filter_fields_for_create_or_update(self, item: Dict) -> Dict:
        """过滤创建/更新的字段"""
        if not item:
            return item

        if 'Story' in item and isinstance(item['Story'], dict):
            obj = item['Story']
        elif 'Bug' in item and isinstance(item['Bug'], dict):
            obj = item['Bug']
        elif 'Task' in item and isinstance(item['Task'], dict):
            obj = item['Task']
        elif 'Iteration' in item and isinstance(item['Iteration'], dict):
            obj = item['Iteration']
        else:
            obj = item

        new_obj = {}
        for k, v in obj.items():
            if k.startswith('custom_field_') and (v is None or v == ''):
                continue
            if k.startswith('description') and 'Iteration' not in item:
                continue
            if k.startswith('custom_plan_field_') and v == '0':
                continue
            new_obj[k] = v

        if 'Story' in item:
            return {'Story': new_obj}
        elif 'Bug' in item:
            return {'Bug': new_obj}
        elif 'Task' in item:
            return {'Task': new_obj}
        elif 'Iteration' in item:
            return {'Iteration': new_obj}
        return new_obj

    def get_story_or_task_url_template(self, workspace_id: int, entity_type: str, tapd_base_url: str) -> str:
        """获取 URL 模板"""
        is_mini = self.check_mini_project(workspace_id)
        if entity_type == 'tasks':
            return f'{tapd_base_url}/{workspace_id}/prong/tasks/view/{{id}}'
        else:
            if is_mini:
                return f'{tapd_base_url}/tapd_fe/t/index/{workspace_id}?workitemId={{id}}'
            else:
                return f'{tapd_base_url}/{workspace_id}/prong/stories/view/{{id}}'

    def check_mini_project(self, workspace_id: int) -> bool:
        """判断是否轻协作项目"""
        data = {"workspace_id": workspace_id}
        ret = self.get_workspace_info(data)
        return ret.get('data', {}).get('Workspace', {}).get('category') == 'mini_project'
