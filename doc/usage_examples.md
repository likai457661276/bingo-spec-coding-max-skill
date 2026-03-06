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

人类介入时机：

- `Plan` 完成后确认范围和影响面
- `Spec` 完成后确认接口、约束和验收标准
- `Tasks` 完成后确认实施顺序和测试范围

示例任务结构：

```markdown
# Tasks: auth-login

## Change Type

L1
Quality Gate: FEATURE

## Context

新增登录能力，影响 Web 登录入口、认证服务和令牌发放逻辑。

## Preconditions

- Confirm `plan.md` approved
- Confirm `spec.md` approved

## Tasks

1. 创建登录页面和表单提交流程
2. 实现认证控制器和服务层认证逻辑
3. 增加密码校验与 JWT 签发
4. 更新 API 文档或接口说明
5. 增加自动化测试和基本手工验证
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
Reason: 问题是局部缺陷修复，影响范围有限，可通过小范围改动完成。
Escalation Note: 如果修复涉及认证流程重构，则应升级为 L1
```

人类介入时机：

- `Tasks` 完成后确认修改范围足够小

示例任务结构：

```markdown
# Change Tasks: trim-password-input

## Change Type

L2
Quality Gate: BUG_FIX

## Context

登录时密码输入包含首尾空格会导致校验失败，此问题应通过局部修复解决。

## Scope

In scope:
- 输入清洗
- 认证前校验
- 回归测试

Out of scope:
- 认证模块重构
- 登录协议变更

## Tasks

1. 定位密码校验与标准化逻辑
2. 在认证入口统一去除首尾空格
3. 增加缺陷回归测试
4. 验证现有登录路径未被破坏
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

人类介入时机：

- `Patch Proposal` 完成后确认补丁足够小且可回滚

示例补丁提案：

```markdown
# Patch Proposal: jwt-validation-guard

## Context

JWT 解析异常在生产环境未被正确捕获，导致请求链路中断。

## Proposed Patch

1. 在令牌校验入口补充异常捕获
2. 返回受控错误而不是让进程崩溃
3. 增加一条针对异常输入的验证测试

## Verification

1. 复现异常令牌输入
2. 确认服务不再崩溃
3. 检查日志中是否记录受控错误

## Rollback Notes

- 若补丁引发认证误判，回滚到上一稳定版本并切换到临时保护策略
```
