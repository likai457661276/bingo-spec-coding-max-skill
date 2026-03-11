# 使用示例

## 示例 0 - 分析登录为什么持续失败

```text
Requested Level: AUTO
Final Level: L0
Change Type: QUESTION
Doc Mode: QUESTION_RECORD
Workflow: Context -> Investigation -> Answer
Human Gate: 仅当后续要进入实现时，在 Answer 后确认
Reason: 用户当前先要诊断和解释，不是直接要求改实现。
Scope Signals: 只读分析；比较可能原因；未要求直接改代码
Escalation Note: 如果后续转为实现工作，重新分级到 L1、L2 或 L3
```

## 示例 1 - 新增登录功能

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

## 示例 2 - 密码校验缺陷

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

## 示例 3 - 生产环境令牌故障

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
