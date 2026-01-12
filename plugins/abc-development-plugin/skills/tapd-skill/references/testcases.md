# 测试用例管理指南

## 创建测试用例

```python
create_or_update_tcases(
    workspace_id=123,
    options={
        "name": "用例名称",
        "category_id": "用例目录ID",
        "precondition": "前置条件（支持Markdown）",
        "steps": "测试步骤（支持Markdown）",
        "expectation": "预期结果（支持Markdown）",
        "type": "用例类型",
        "priority": "用例等级",
        "status": "normal",  # updating/abandon/normal
        "creator": "创建人"
    }
)
```

## 批量创建测试用例

```python
create_tcases_batch(
    workspace_id=123,
    options={
        "tcases": [
            {
                "name": "用例1名称",
                "precondition": "前置条件",
                "steps": "步骤1\n步骤2",
                "expectation": "预期结果",
                "type": "功能测试",
                "priority": "P1"
            },
            {
                "name": "用例2名称",
                "precondition": "前置条件",
                "steps": "步骤1\n步骤2",
                "expectation": "预期结果"
            }
            # 最多200条
        ]
    }
)
```

## 查询测试用例

```python
get_tcases(
    workspace_id=123,
    options={
        "id": "用例ID",
        "name": "用例名称",
        "category_id": "用例目录ID",
        "status": "normal",  # updating/abandon/normal
        "type": "用例类型",
        "priority": "用例等级",
        "creator": "创建人",
        "limit": 30,
        "page": 1,
        "order": "created desc",
        "fields": "id,name,status,priority,type"
    }
)
```

## 字段说明

| 字段 | 说明 |
|------|------|
| status | 用例状态: updating/abandon/normal |
| priority | 用例等级 |
| type | 用例类型 |
| is_automated | 是否自动化 |
| automation_type | 自动化类型 |
| automation_platform | 自动化平台 |
| is_serving | 是否上架 |

## URL 格式

测试用例链接: `{tapd_base_url}/{workspace_id}/sparrow/tcase/view/{id}`
