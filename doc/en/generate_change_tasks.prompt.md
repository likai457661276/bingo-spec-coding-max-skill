# Change Tasks Generator

Generate `tasks.md` for an `L2` small change or a recorded change under a feature history.

## Required Inputs

- related feature spec
- change description

## Rules

- keep the change minimal
- avoid architecture change
- modify the smallest safe scope
- include verification
- escalate to `L1` when scope expands beyond a local fix

## Output Structure

```markdown
# Change Tasks: <change-name>

## Change Type

L2
Quality Gate: SMALL_CHANGE | BUG_FIX

## Context

Describe the problem, affected behavior, and why this remains a small change.
```
