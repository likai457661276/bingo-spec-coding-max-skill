# Feature Tasks 生成器

为 `L1` feature change 生成 `tasks.md`。

## Required Inputs

- `plan.md`
- `spec.md`

在两个输入都齐备前，不得生成任务。

## Task Generation Rules

- 任务必须有顺序
- 任务必须原子化
- 任务必须遵循已批准的 plan 和 spec
- 任务必须尊重现有项目架构
- 任务必须包含验证工作
- 任务粒度要适合 AI 独立执行
- 能局部改动时优先局部改动，但功能需要时可跨模块

## Required Output Structure

严格按以下结构返回：

```markdown
# Tasks: <feature-name>

## Change Type

L1
Quality Gate: FEATURE

## Context

总结功能目标、影响区域和实现假设。

## Preconditions

- Confirm `plan.md` approved
- Confirm `spec.md` approved

## Tasks

1. ...
2. ...
3. ...

## Verification

1. Automated tests:
2. Manual checks:
3. Observability or logs to review:

## Risks

- ...

## Rollback Notes

- ...
```
