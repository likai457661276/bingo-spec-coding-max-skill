# Feature Tasks Generator

Generate `tasks.md` for an `L1` feature change.

## Required Inputs

- `plan.md`
- `spec.md`

Do not generate tasks until both inputs are available.

## Task Generation Rules

- tasks must be sequential
- tasks must be atomic
- tasks must follow the approved plan and feature spec
- tasks must respect the existing project architecture
- tasks must include verification work
- tasks must be small enough for AI execution without mixing unrelated goals
- tasks should prefer minimal necessary file changes, but may span multiple modules if the feature requires it

## Required Output Structure

Return exactly this structure:

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

## Verification

1. Automated tests:
2. Manual checks:
3. Observability or logs to review:

## Risks

- ...

## Rollback Notes

- ...
```

## Additional Rules

- Include test creation or test update tasks when behavior changes
- Include documentation or API update tasks when external behavior changes
- Do not include coding work that conflicts with the approved spec
- If the requested work no longer matches `L1`, stop and say the change must be reclassified
