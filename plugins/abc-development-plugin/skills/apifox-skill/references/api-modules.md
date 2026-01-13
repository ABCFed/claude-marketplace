# API 模块分类

## 模块概览

ABC 医疗云 API 共包含 **4209** 个接口，按路径前缀分为以下主要模块：

| 模块 | 接口数量 | 路径前缀 | 说明 |
|------|---------|---------|------|
| api | 2506 | `/api/*` | 标准 HTTP REST API |
| rpc | 1338 | `/rpc/*` | RPC 服务接口 |
| api-weapp | 294 | `/api-weapp/*` | 小程序专用 API |
| api-device | 29 | `/api-device/*` | 智能设备接口 |
| api-mp | 17 | `/api-mp/*` | 微信公众号接口 |
| api-external | 14 | `/api-external/*` | 外部系统集成接口 |

## 1. api 模块 (2506 个接口)

标准 HTTP REST API，涵盖大部分业务功能。

### 1.1 全局认证 (global-auth)

**路径前缀**: `/api/global-auth`

登录、认证、权限相关接口。

**主要接口**:
- `POST /api/global-auth/login/sms` - 短信验证码登录
- `POST /api/global-auth/login/password` - 密码登录
- `POST /api/global-auth/login/app` - APP 登录
- `POST /api/global-auth/logout` - 退出登录
- `POST /api/global-auth/refresh-token` - 刷新令牌
- `GET /api/global-auth/clinic/joined` - 查询加入的门店
- `POST /api/global-auth/switch-clinic/*` - 切换门店

### 1.2 内容管理 (cms)

**路径前缀**: `/api/v3/cms`

推送消息、文章、公告等内容管理。

**主要接口**:
- `GET /api/v3/cms/push/current` - 查询当前推送
- `POST /rpc/cms/push` - 新增推送
- `PUT /rpc/cms/push/{id}` - 更新推送
- `POST /rpc/cms/log` - 新增文章

### 1.3 消息服务 (message)

**路径前缀**: `/api/v2/message`, `/rpc/message`

短信、模板消息、消息配置。

**主要接口**:
- `POST /rpc/message/sms/send` - 发送短信
- `POST /rpc/message/send` - 发送消息
- `GET /api/v2/message/template` - 查询消息模板
- `POST /api/v2/message/config` - 更新消息配置

### 1.4 促销营销 (promotions)

**路径前缀**: `/api/v2/promotions`, `/rpc/promotions`

活动、卡券、会员权益管理。

**主要接口**:
- `GET /api/v2/promotions/mains` - 促销活动列表
- `POST /api/v2/promotions/mains` - 创建活动
- `GET /api/v2/promotions/card` - 卡列表
- `POST /api/v2/promotions/card/patients` - 开卡
- `POST /rpc/promotions/discount/member` - 会员折扣

## 2. rpc 模块 (1338 个接口)

RPC 风格的服务接口，通常用于内部服务调用。

### 2.1 诊所管理 (clinics)

**路径前缀**: `/rpc/v3/clinics`

诊所、门店、组织架构管理。

**主要接口**:
- 查询诊所信息
- 更新诊所配置
- 诊所员工管理

### 2.2 其他 RPC 服务

包含大量内部业务逻辑调用接口。

## 3. api-weapp 模块 (294 个接口)

微信小程序专用 API 接口。

**特点**:
- 针对小程序场景优化
- 简化的认证流程
- 小程序特有功能（如微信登录、支付等）

**主要接口**:
- 小程序登录
- 小程序用户信息
- 小程序支付
- 小程序预约

## 4. api-device 模块 (29 个接口)

智能硬件设备接口。

**应用场景**:
- 云检设备
- 智能体检设备
- 医疗物联网设备

**主要功能**:
- 设备登录认证
- 设备数据上报
- 设备状态查询

## 5. api-mp 模块 (17 个接口)

微信公众号专用接口。

**主要功能**:
- 公众号用户绑定
- 公众号消息推送
- 公众号菜单管理

## 6. api-external 模块 (14 个接口)

外部系统集成接口。

**应用场景**:
- 第三方平台对接
- 数据交换
- 系统集成

## 按业务领域分类

### 认证与授权

- 登录（短信、密码、扫码、第三方）
- 令牌刷新
- 门店切换
- 权限验证

### 患者管理

- 患者信息
- 就诊记录
- 健康档案
- 会员管理

### 预约挂号

- 医生排班
- 预约创建
- 预约查询
- 预约取消

### 诊疗服务

- 问诊记录
- 处方开具
- 检查检验
- 诊断报告

### 营销管理

- 促销活动
- 卡券管理
- 会员权益
- 积分管理

### 消息通知

- 短信发送
- 模板消息
- 推送通知
- 消息配置

### 内容管理

- 文章发布
- 推送消息
- 公告管理
- 内容审核

### 数据统计

- 业务统计
- 用户分析
- 报表生成
- 数据导出

## 版本说明

### API 版本

当前主要版本：
- `/v2/*` - 主版本
- `/v3/*` - 新版本（如 cms）
- 无版本前缀 - 早期版本

### 升级建议

- 新功能优先使用 `/v3/*` 接口
- 现有功能可继续使用 `/v2/*`
- 部分早期接口可能已废弃

## 查询模块统计

```bash
# 查看所有模块及接口数量
python apifox.py list_modules

# 查看某个模块的所有接口
python apifox.py list_paths --module api

# 查看详细统计
python apifox.py stats --detail
```
