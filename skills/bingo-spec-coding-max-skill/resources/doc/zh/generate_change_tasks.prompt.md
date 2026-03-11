# Change Tasks 生成器

为 `L2` small change 或 feature 历史中的局部变更生成 `tasks.md`。

## Required Inputs

- 相关 feature spec
- 变更描述
- 已确认的分级输出，其中 `Final Level = L2`

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
- 若不存在既有 feature spec，不得继续按 `L2` 生成任务，必须升级为 `L1 + FULL_SPEC`

## Path Rules

- 输出内容保存到 `spec/features/<feature-name>/smallchange/<date>-<change-name>.md`
- 仅可写入相关 feature 目录下的 `smallchange/`
- 不得把变更记录直接写到 `spec/` 根目录

## Required Output Structure

严格按以下结构返回：

```markdown
# Change Tasks: <change-name>

## Classification

Requested Level: AUTO | L1 | L2 | L3
Final Level: L2
Change Type: SMALL_CHANGE | BUG_FIX
Doc Mode: CHANGE_RECORD
Workflow: Tasks -> Code
Human Gate: Confirm after `spec/features/<feature-name>/smallchange/<date>-<change-name>.md`

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
