# Change Tasks 生成器

为 `L2` small change 或 feature 历史中的局部变更生成 `tasks.md`。

## Required Inputs

- 相关 feature spec
- 变更描述

可选但推荐：

- 当前缺陷上下文
- 受影响的文件或模块

## Task Generation Rules

- 保持改动最小
- 避免架构变化
- 修改最小安全范围
- 至少包含一个验证步骤
- 若行为可能回归，补充 rollback 或 fallback 说明
- 与相关 feature spec 保持一致

## Escalation Rules

- 如果任务列表需要重大重设计、新 API 或大范围跨模块改动，则不要继续按 `L2`
- 如果变更超出局部修复范围，应明确升级为 `L1`

## Required Output Structure

严格按以下结构返回：

```markdown
# Change Tasks: <change-name>

## Change Type

L2
Quality Gate: SMALL_CHANGE | BUG_FIX

## Context

描述问题、受影响行为，以及为什么它仍然是小改动。

## Scope

In scope:
- ...

Out of scope:
- ...

## Tasks

1. ...
2. ...
3. ...

## Verification

1. Automated tests:
2. Manual checks:
3. Regression focus:

## Risks

- ...

## Rollback Notes

- ...
```
