#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SLS Log Query Script
用于查询阿里云日志服务中指定 traceId 的日志
"""

import argparse
import hashlib
import hmac
import base64
import json
import os
import sys
import time
from datetime import datetime, timedelta, timezone
from urllib.parse import quote, urlparse, parse_qs

try:
    import requests
except ImportError:
    print("Error: requests library not found. Install with: pip3 install requests")
    sys.exit(1)


# 预设配置
CONFIGS = {
    "shanghai": {
        "endpoint": "cn-shanghai.log.aliyuncs.com",
        "project": "abc-cis-log",
    },
    "hangzhou": {
        "endpoint": "cn-hangzhou.log.aliyuncs.com",
        "project": "abc-cis-log-hangzhou",
    }
}

# 域名到环境映射
DOMAIN_MAPPING = {
    "dev.abczs.cn": {"env": "dev", "region": "shanghai"},
    "test.abczs.cn": {"env": "test", "region": "shanghai"},
    "abcyun.cn": {"env": "prod", "region": "shanghai"},
    "region2.abcyun.cn": {"env": "prod", "region": "hangzhou"},
}

CREDENTIALS_PATHS = [
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "credentials.json"),
    os.path.expanduser("~/.cc-switch/skills/sls-trace-analyzer/credentials.json"),
    os.path.expanduser("~/.config/sls-query/credentials.json"),
]


def load_credentials():
    """Load SLS credentials from config file or environment variables."""
    # Try config files first (multiple candidate paths)
    for cred_path in CREDENTIALS_PATHS:
        if os.path.exists(cred_path):
            with open(cred_path, "r") as f:
                creds = json.load(f)
            ak_id = creds.get("sls_access_key_id")
            ak_secret = creds.get("sls_access_key_secret")
            if ak_id and ak_secret:
                return ak_id, ak_secret

    # Fall back to environment variables
    ak_id = os.environ.get("SLS_ACCESS_KEY_ID")
    ak_secret = os.environ.get("SLS_ACCESS_KEY_SECRET")
    if ak_id and ak_secret:
        return ak_id, ak_secret

    # Neither configured — print setup instructions and exit
    print(
        "Error: SLS credentials not configured.\n"
        "\n"
        "Option 1 — config file (recommended):\n"
        "  mkdir -p ~/.config/sls-query\n"
        '  cat > ~/.config/sls-query/credentials.json << \'EOF\'\n'
        "  {\n"
        '    "sls_access_key_id": "YOUR_ACCESS_KEY_ID",\n'
        '    "sls_access_key_secret": "YOUR_ACCESS_KEY_SECRET"\n'
        "  }\n"
        "  EOF\n"
        "  chmod 600 ~/.config/sls-query/credentials.json\n"
        "\n"
        "Option 2 — environment variables:\n"
        "  export SLS_ACCESS_KEY_ID=YOUR_ACCESS_KEY_ID\n"
        "  export SLS_ACCESS_KEY_SECRET=YOUR_ACCESS_KEY_SECRET",
        file=sys.stderr,
    )
    sys.exit(1)


def parse_url_input(url):
    """解析 URL 输入，提取环境、地域、路径和时间戳"""
    parsed = urlparse(url)
    domain = parsed.netloc
    path = parsed.path
    query = parsed.query

    # 提取时间戳
    timestamp = None
    if query:
        if '=' in query:
            params = parse_qs(query)
            timestamp = params.get('t', [None])[0]
        else:
            timestamp = query

    # 从域名获取环境和地域
    config = DOMAIN_MAPPING.get(domain, {"env": "prod", "region": "shanghai"})

    return {
        "domain": domain,
        "path": path,
        "timestamp": timestamp,
        "env": config["env"],
        "region": config["region"]
    }


def sign(method, resource, params, headers, access_key_secret):
    """计算 SLS API 签名"""
    content_md5 = headers.get('Content-MD5', '')
    content_type = headers.get('Content-Type', '')
    date = headers.get('Date', '')

    # 构建 CanonicalizedSLSHeaders
    sls_headers = sorted([k for k in headers.keys() if k.lower().startswith('x-log-')])
    canonicalized_sls_headers = '\n'.join([f'{k.lower()}:{headers[k]}' for k in sls_headers])

    # 构建 CanonicalizedResource
    if params:
        sorted_params = sorted(params.items())
        query_string = '&'.join([f'{k}={v}' for k, v in sorted_params])
        canonicalized_resource = f'{resource}?{query_string}'
    else:
        canonicalized_resource = resource

    # 构建签名字符串
    string_to_sign = f'{method}\n{content_md5}\n{content_type}\n{date}\n{canonicalized_sls_headers}\n{canonicalized_resource}'

    # 计算 HMAC-SHA1 签名
    signature = base64.b64encode(
        hmac.new(
            access_key_secret.encode('utf-8'),
            string_to_sign.encode('utf-8'),
            hashlib.sha1
        ).digest()
    ).decode('utf-8')

    return signature


def parse_datetime(date_str):
    """解析日期字符串为时间戳"""
    if not date_str:
        return None

    formats = [
        '%Y-%m-%d %H:%M:%S',
        '%Y-%m-%d %H:%M',
        '%Y-%m-%d',
    ]

    for fmt in formats:
        try:
            dt = datetime.strptime(date_str, fmt)
            return int(dt.timestamp())
        except ValueError:
            continue

    raise ValueError(f"无法解析日期: {date_str}")


def get_logs(endpoint, project, logstore, trace_id, start_time, end_time, access_key_id, access_key_secret, limit=1000):
    """获取日志"""
    resource = f'/logstores/{logstore}'

    # 构建查询语句 - 直接使用 traceId 进行全文搜索
    query = trace_id

    params = {
        'type': 'log',
        'from': str(start_time),
        'to': str(end_time),
        'query': query,
        'line': str(limit),
        'offset': '0',
        'reverse': 'false'
    }

    # 构建请求头
    date = datetime.now(timezone.utc).strftime('%a, %d %b %Y %H:%M:%S GMT')
    headers = {
        'Content-Type': 'application/json',
        'Date': date,
        'x-log-apiversion': '0.6.0',
        'x-log-signaturemethod': 'hmac-sha1',
        'x-log-bodyrawsize': '0',
        'Host': f'{project}.{endpoint}'
    }

    # 计算签名
    signature = sign('GET', resource, params, headers, access_key_secret)
    headers['Authorization'] = f'LOG {access_key_id}:{signature}'

    # 发送请求
    url = f'https://{project}.{endpoint}{resource}'

    try:
        response = requests.get(url, params=params, headers=headers, timeout=60)

        if response.status_code == 200:
            return {
                'success': True,
                'data': response.json(),
                'count': int(response.headers.get('x-log-count', 0)),
                'progress': response.headers.get('x-log-progress', 'Complete')
            }
        else:
            return {
                'success': False,
                'error': f"HTTP {response.status_code}: {response.text}"
            }
    except requests.exceptions.RequestException as e:
        return {
            'success': False,
            'error': str(e)
        }


def get_access_logs(endpoint, project, logstore, path, timestamp_ms, access_key_id, access_key_secret, limit=100):
    """根据路径和时间戳查询 gateway access-log"""
    resource = f'/logstores/{logstore}'

    # 时间范围：直接查询最近 4 天，避免时间戳不准确导致查不到日志
    now = datetime.now()
    start_time = int((now - timedelta(days=4)).timestamp())
    end_time = int(now.timestamp())

    # 构建查询语句
    # 使用路径关键词而非完整路径，提高匹配率
    # Topic: abc-cis-gateway-service 是业务请求 API 网关入口
    # 同时匹配时间戳参数，确保找到正确的请求
    path_keyword = path.split('/')[-1] if '/' in path else path
    query = f'__topic__: abc-cis-gateway-service and {path_keyword} and {timestamp_ms}'

    params = {
        'type': 'log',
        'from': str(start_time),
        'to': str(end_time),
        'query': query,
        'line': str(limit),
        'offset': '0',
        'reverse': 'false'
    }

    date = datetime.now(timezone.utc).strftime('%a, %d %b %Y %H:%M:%S GMT')
    headers = {
        'Content-Type': 'application/json',
        'Date': date,
        'x-log-apiversion': '0.6.0',
        'x-log-signaturemethod': 'hmac-sha1',
        'x-log-bodyrawsize': '0',
        'Host': f'{project}.{endpoint}'
    }

    signature = sign('GET', resource, params, headers, access_key_secret)
    headers['Authorization'] = f'LOG {access_key_id}:{signature}'

    url = f'https://{project}.{endpoint}{resource}'

    try:
        response = requests.get(url, params=params, headers=headers, timeout=60)
        if response.status_code == 200:
            return {
                'success': True,
                'data': response.json(),
                'count': int(response.headers.get('x-log-count', 0))
            }
        else:
            return {
                'success': False,
                'error': f"HTTP {response.status_code}: {response.text}"
            }
    except requests.exceptions.RequestException as e:
        return {
            'success': False,
            'error': str(e)
        }


def format_log_entry(log):
    """格式化单条日志"""
    # 尝试提取常见字段
    timestamp = log.get('__time__', '')
    if timestamp:
        try:
            timestamp = datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')
        except:
            pass

    level = log.get('level', log.get('log_level', ''))
    message = log.get('message', log.get('msg', log.get('content', '')))
    logger = log.get('logger', log.get('class', ''))
    thread = log.get('thread', '')

    return {
        'time': timestamp,
        'level': level,
        'logger': logger,
        'thread': thread,
        'message': message,
        'raw': log
    }


def extract_target_service(logs):
    """从日志中提取目标服务名称"""
    for log in logs:
        message = log.get('message', '')
        # 从 monitor 日志中提取 targetHost
        if 'targetHost' in message:
            try:
                import re
                match = re.search(r'"targetHost"\s*:\s*"([^"]+)"', message)
                if match:
                    return match.group(1)
            except:
                pass
    return None


def has_exception_stack(logs):
    """检查日志中是否包含异常堆栈"""
    # 只检查 message 字段中的异常关键字，排除 location 字段的干扰
    exception_keywords = ['Exception', 'at cn.abcyun.', 'at java.', 'at org.springframework', 'Caused by:']
    for log in logs:
        message = log.get('message', '')
        level = log.get('level', '')
        if level == 'ERROR':
            return True
        for keyword in exception_keywords:
            if keyword in message:
                return True
    return False


def main():
    parser = argparse.ArgumentParser(description='查询阿里云 SLS 日志')
    parser.add_argument('--trace-id', '-t', help='要查询的 traceId')
    parser.add_argument('--mode', '-m', choices=['trace', 'access-log'], default='trace',
                        help='查询模式: trace(默认) 或 access-log')
    parser.add_argument('--timestamp', help='时间戳(毫秒)，access-log 模式使用')
    parser.add_argument('--path', help='API 路径，access-log 模式使用')
    parser.add_argument('--region', '-r', default='shanghai',
                        choices=['shanghai', 'hangzhou'], help='地域 (默认: shanghai)')
    parser.add_argument('--env', '-e', default='prod',
                        choices=['dev', 'test', 'prod'], help='环境 (默认: prod)')
    parser.add_argument('--longtime', '-l', action='store_true',
                        help='仅查询 longtime logstore（默认同时查询普通和 longtime 两个 logstore）')
    parser.add_argument('--logstore', help='指定单个 logstore 名称')
    parser.add_argument('--auto-expand', '-a', action='store_true',
                        help='自动扩展查询服务专属日志')
    parser.add_argument('--from', dest='from_time', help='开始时间')
    parser.add_argument('--to', dest='to_time', help='结束时间')
    parser.add_argument('--limit', type=int, default=1000, help='返回日志条数限制')
    parser.add_argument('--output', '-o', choices=['json', 'text'], default='json',
                        help='输出格式')

    args = parser.parse_args()

    # Load credentials
    access_key_id, access_key_secret = load_credentials()

    # 获取配置
    config = CONFIGS[args.region]
    endpoint = config['endpoint']
    project = config['project']

    # 确定 logstore
    if args.logstore:
        logstore = args.logstore
    elif args.longtime:
        logstore = f'{args.env}_longtime'
    else:
        logstore = args.env

    # access-log 模式
    if args.mode == 'access-log':
        if not args.timestamp or not args.path:
            print("access-log 模式需要 --timestamp 和 --path 参数", file=sys.stderr)
            sys.exit(1)

        print(f"=== Access Log 查询 ===", file=sys.stderr)
        print(f"Path: {args.path}", file=sys.stderr)
        print(f"Timestamp: {args.timestamp}", file=sys.stderr)
        print(f"Region: {args.region}, Env: {args.env}", file=sys.stderr)

        result = get_access_logs(endpoint, project, logstore,
                                  args.path, args.timestamp,
                                  access_key_id, access_key_secret)
        if not result['success']:
            print(f"查询失败: {result['error']}", file=sys.stderr)
            sys.exit(1)

        print(json.dumps(result['data'], indent=2, ensure_ascii=False))
        return

    # trace 模式需要 trace-id
    if not args.trace_id:
        print("trace 模式需要 --trace-id 参数", file=sys.stderr)
        sys.exit(1)

    # 解析时间范围（默认最近 4 天）
    now = datetime.now()
    if args.from_time:
        start_time = parse_datetime(args.from_time)
    else:
        start_time = int((now - timedelta(days=4)).timestamp())

    if args.to_time:
        end_time = parse_datetime(args.to_time)
    else:
        end_time = int(now.timestamp())

    # 确定要查询的 logstore 列表
    if args.logstore:
        # 指定了具体 logstore
        logstores_to_query = [args.logstore]
    elif args.longtime:
        # 仅查询 longtime
        logstores_to_query = [f'{args.env}_longtime']
    else:
        # 默认同时查询普通存储和长期存储
        logstores_to_query = [args.env, f'{args.env}_longtime']

    # 打印查询信息
    print(f"=== SLS 日志查询 ===", file=sys.stderr)
    print(f"TraceId: {args.trace_id}", file=sys.stderr)
    print(f"Region: {args.region}", file=sys.stderr)
    print(f"Project: {project}", file=sys.stderr)
    print(f"LogStore: {', '.join(logstores_to_query)}", file=sys.stderr)
    print(f"时间范围: {datetime.fromtimestamp(start_time)} ~ {datetime.fromtimestamp(end_time)}", file=sys.stderr)
    print(f"", file=sys.stderr)

    # 查询日志（支持多个 logstore）
    logs = []
    total_count = 0
    for ls in logstores_to_query:
        print(f"查询 {ls}...", file=sys.stderr)
        result = get_logs(endpoint, project, ls, args.trace_id, start_time, end_time, access_key_id, access_key_secret, args.limit)
        if result['success']:
            logs.extend(result['data'])
            total_count += result['count']
            print(f"  -> {result['count']} 条日志", file=sys.stderr)
        else:
            print(f"  -> 查询失败: {result['error']}", file=sys.stderr)

    if not logs:
        print(f"未查询到任何日志", file=sys.stderr)
        sys.exit(1)

    print(f"查询完成，共 {total_count} 条日志", file=sys.stderr)

    # Step 2.5: 自动扩展查询
    expanded_logs = []
    if args.auto_expand and not has_exception_stack(logs):
        print(f"\n=== Step 2.5: 未找到异常堆栈，自动扩展查询 ===", file=sys.stderr)

        # 从日志中提取目标服务
        target_service = extract_target_service(logs)
        if target_service:
            service_logstore = f'{args.env}-{target_service}'
            print(f"检测到目标服务: {target_service}", file=sys.stderr)
            print(f"查询服务专属日志: {service_logstore}", file=sys.stderr)

            expanded_result = get_logs(endpoint, project, service_logstore, args.trace_id, start_time, end_time, access_key_id, access_key_secret, args.limit)
            if expanded_result['success']:
                expanded_logs = expanded_result['data']
                print(f"扩展查询完成，共 {expanded_result['count']} 条日志", file=sys.stderr)
            else:
                print(f"扩展查询失败: {expanded_result['error']}", file=sys.stderr)
        else:
            print(f"未能从日志中提取目标服务名称", file=sys.stderr)

    # 合并结果
    all_logs = logs + expanded_logs

    if args.output == 'json':
        print(json.dumps(all_logs, indent=2, ensure_ascii=False))
    else:
        for log in all_logs:
            formatted = format_log_entry(log)
            print(f"[{formatted['time']}] [{formatted['level']}] {formatted['logger']} - {formatted['message']}")


if __name__ == '__main__':
    main()
