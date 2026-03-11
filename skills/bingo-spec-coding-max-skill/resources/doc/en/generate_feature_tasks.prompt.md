# Feature Tasks Generator

Generate `tasks.md` for an `L1` feature change.

## Required Inputs

- `spec/features/<feature-name>/plan.md`
- `spec/features/<feature-name>/spec.md`
- confirmed classification output where `Final Level = L1`

Do not generate tasks until these inputs are available.

## Path Rules

- save the output to `spec/features/<feature-name>/tasks.md`
- when the feature folder is created, also create `spec/features/<feature-name>/smallchange/` and `spec/features/<feature-name>/hotfix/`
- do not write requirement documents directly under the `spec/` root

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
