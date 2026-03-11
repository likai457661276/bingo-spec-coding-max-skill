# Change Tasks Generator

Generate `tasks.md` for an `L2` small change or a recorded change under a feature history.

## Required Inputs

- related feature spec
- change description
- confirmed classification output where `Final Level = L2`

Optional but recommended:

- current defect context
- impacted files or modules

## Task Generation Rules

- keep the change minimal
- avoid architecture changes
- modify the smallest safe scope
- include at least one verification step
- add rollback or fallback notes when behavior may regress
- stay aligned with the related feature spec
- if no baseline feature spec exists, do not continue as `L2`; escalate to `L1 + FULL_SPEC`

## Path Rules

- save the output to `spec/features/<feature-name>/smallchange/<date>-<change-name>.md`
- only write under the related feature folder's `smallchange/`
- do not place change records directly under the `spec/` root

## Required Output Structure

Return exactly this structure:

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
