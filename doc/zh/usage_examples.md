# 使用示例

## 示例 1 - 新增登录功能

需求：

添加用户登录功能，包括登录页面、认证接口、JWT 令牌签发和基础登录测试。

分类输出：

```text
Change Level: L1
Quality Gate: FEATURE
Workflow: Context -> Plan -> Spec -> Tasks -> Code
Human Gate: Approvals required after Plan, Spec, and Tasks
Reason: 请求包含新功能、新接口和新增认证流程，属于完整特性开发。
Escalation Note: None
```

## 示例 2 - 密码校验缺陷

需求：

包含首尾空格的密码会导致登录失败，需要在不改变架构的前提下修复。

分类输出：

```text
Change Level: L2
Quality Gate: BUG_FIX
Workflow: Tasks -> Code
Human Gate: Approval required after Tasks
Reason: 问题是局部缺陷修复，影响范围有限。
Escalation Note: 如果修复涉及认证流程重构，则应升级为 L1
```

## 示例 3 - 生产环境令牌故障

需求：

JWT 验证异常导致生产环境请求大面积失败，需要尽快恢复服务。

分类输出：

```text
Change Level: L3
Quality Gate: BUG_FIX
Workflow: Patch Proposal -> Code
Human Gate: Approval required after Patch Proposal
Reason: 该请求属于生产故障修复，目标是以最小补丁恢复可用性。
Escalation Note: 如果修复不再是最小安全补丁，应升级为 L2 或 L1
```
