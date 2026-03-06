# Change Tasks Generator

Generate `tasks.md` for an `L2` small change or a recorded change under a feature history.

## Required Inputs

- related feature spec
- change description

Optional but recommended:

- current bug context
- affected files or modules

## Task Generation Rules

- keep the change minimal
- avoid architecture change
- modify the smallest safe scope
- include at least one verification step
- include a rollback or fallback note when behavior could regress
- preserve alignment with the related feature spec

## Escalation Rules

- if the task list requires major redesign, new APIs, or broad cross-module work, do not continue as `L2`
- if the change expands beyond a local fix, state that it must be escalated to `L1`

## Required Output Structure

Return exactly this structure:

```markdown
# Change Tasks: <change-name>

## Change Type

L2
Quality Gate: SMALL_CHANGE | BUG_FIX

## Context

Describe the problem, affected behavior, and why this remains a small change.

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

## Additional Rules

- keep tasks implementation-ready
- prefer local edits over broad rewrites
- include test updates for bug fixes or validation changes
- if the change is urgent production repair, stop and say it should be handled as `L3`
