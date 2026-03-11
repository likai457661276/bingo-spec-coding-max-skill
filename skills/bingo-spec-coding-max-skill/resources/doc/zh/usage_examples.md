# 使用示例

## 示例 1 - 新增登录功能

需求：

添加用户登录功能，包括登录页面、认证接口、JWT 令牌签发和基础登录测试。

分类输出：

```text
Requested Level: AUTO
Final Level: L1
Change Type: FEATURE
Doc Mode: FULL_SPEC
Workflow: Context -> Plan -> Spec -> Tasks -> Code
Human Gate: Confirm after Plan, Spec, and Tasks
Reason: 请求包含新功能、新接口和新增认证流程，命中了外部契约新增，因此必须走 L1；该功能尚未有可复用 spec，因此文档模式必须为 FULL_SPEC。
Scope Signals: 新增登录页面；新增认证接口；新增 JWT 签发流程；前端与调用方接口行为会变化
Escalation Note: None
```

落地路径：

- `spec/features/auth-login/plan.md`
- `spec/features/auth-login/spec.md`
- `spec/features/auth-login/tasks.md`
- `spec/features/auth-login/smallchange/`
- `spec/features/auth-login/hotfix/`

## 示例 2 - 密码校验缺陷

需求：

包含首尾空格的密码会导致登录失败，需要在不改变架构的前提下修复。已存在 `spec/features/auth-login/spec.md`。

分类输出：

```text
Requested Level: AUTO
Final Level: L2
Change Type: BUG_FIX
Doc Mode: CHANGE_RECORD
Workflow: Tasks -> Code
Human Gate: Confirm after Tasks
Reason: 这是已有登录能力中的局部缺陷修复，未改变接口字段或语义，且相关 feature 已存在可复用 spec，因此可维持 L2，并以 CHANGE_RECORD 记录。
Scope Signals: 登录能力已存在；已有 feature spec 可复用；仅修复输入清洗缺陷；不改变接口契约
Escalation Note: 如果修复扩大到认证流程重构、字段语义调整或接口行为变化，则升级为 L1
```

落地路径：

- `spec/features/auth-login/smallchange/2026-03-09-trim-password-input.md`

## 示例 3 - 生产环境令牌故障

需求：

JWT 验证异常导致生产环境请求大面积失败，需要尽快恢复服务。

分类输出：

```text
Requested Level: AUTO
Final Level: L3
Change Type: BUG_FIX
Doc Mode: HOTFIX_RECORD
Workflow: Patch Proposal -> Code
Human Gate: Confirm after Patch Proposal
Reason: 该请求属于生产故障修复，当前目标是以最小安全补丁快速恢复服务，且尚未涉及外部契约变更，因此可使用 L3，并记录 HOTFIX_RECORD。
Scope Signals: 生产环境大面积失败；目标是快速止血；补丁范围限定在 JWT 校验入口；未引入新接口
Escalation Note: 如果补丁扩大到认证链路重设计、接口调整或大范围重构，则升级为 L2 或 L1
```

落地路径：

- `spec/features/auth-login/hotfix/2026-03-09-jwt-validation-patch.md`
