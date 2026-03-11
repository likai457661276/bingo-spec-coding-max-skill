# Feature Tasks 生成器

为 `L1` feature change 生成 `tasks.md`。

## Required Inputs

- `spec/features/<feature-name>/plan.md`
- `spec/features/<feature-name>/spec.md`
- 已确认的分级输出，其中 `Final Level = L1`

在上述输入齐备前，不得生成任务。

## Path Rules

- 输出内容保存到 `spec/features/<feature-name>/tasks.md`
- 创建 feature 目录时，同步建立 `spec/features/<feature-name>/smallchange/` 与 `spec/features/<feature-name>/hotfix/`
- 不得把需求文档直接写到 `spec/` 根目录

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

## Classification

Final Level: L1
Change Type: FEATURE
Doc Mode: FULL_SPEC

## Context

总结功能目标、影响区域和实现假设。

## Preconditions

- Confirm `spec/features/<feature-name>/plan.md` approved
- Confirm `spec/features/<feature-name>/spec.md` approved

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
