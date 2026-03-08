# Feature Tasks Generator

Generate `tasks.md` for an `L1` feature change.

## Required Inputs

- `plan.md`
- `spec.md`

Do not generate tasks until both inputs are available.

## Rules

- tasks must be sequential
- tasks must be atomic
- tasks must follow the approved plan and spec
- tasks must respect existing architecture
- tasks must include verification

## Output Structure

```markdown
# Tasks: <feature-name>

## Change Type

L1
Quality Gate: FEATURE

## Context

Summarize the feature goal, affected area, and implementation assumptions.

## Preconditions

- Confirm `plan.md` approved
- Confirm `spec.md` approved

## Tasks

1. ...
2. ...
3. ...
```
