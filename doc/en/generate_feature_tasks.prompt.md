# Feature Tasks Generator

Generate `tasks.md` for an `L1` feature change.

## Required Inputs

- `plan.md`
- `spec.md`
- confirmed classification output where `Final Level = L1`

Do not generate tasks until these inputs are available.

## Task Generation Rules

- tasks must be sequential
- tasks must be atomic
- tasks must follow the approved plan and spec
- tasks must respect the existing architecture
- tasks must include verification work
- task granularity should fit independent AI execution
- prefer local edits when possible, but allow cross-module work when the feature truly requires it

## Required Output Structure

Return exactly this structure:

```markdown
# Tasks: <feature-name>

## Classification

Final Level: L1
Change Type: FEATURE
Doc Mode: FULL_SPEC

## Context

Summarize the feature goal, affected area, and implementation assumptions.

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
