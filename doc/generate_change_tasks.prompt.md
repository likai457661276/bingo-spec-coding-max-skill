# Change Tasks Generator

Generate `tasks.md` for an `L2` small change or a recorded change under a feature history.

## Required Inputs

- related feature spec
- change description
- confirmed classification output where `Final Level = L2`

## Rules

- keep the change minimal
- avoid architecture changes
- include verification
- if no baseline feature spec exists, do not continue as `L2`; escalate to `L1 + FULL_SPEC`

## Output Structure

```markdown
# Change Tasks: <change-name>

## Classification

Requested Level: AUTO | L1 | L2 | L3
Final Level: L2
Change Type: SMALL_CHANGE | BUG_FIX
Doc Mode: CHANGE_RECORD
Workflow: Tasks -> Code
Human Gate: Confirm after Tasks
```
