# Change Tasks Generator

Generate a `CHANGE_RECORD` for an `L2` request.

## Required Inputs

- related feature spec
- change description
- confirmed classification output where `Final Level = L2`

## Rules

- keep the change minimal
- avoid architecture changes
- include verification
- if no baseline feature spec exists, do not continue as `L2`; escalate to `L1 + FULL_SPEC`
- if the request is still only analysis or explanation, reclassify to `L0` instead of generating change tasks

## Output Structure

```markdown
# Change Tasks: <change-name>

## Classification

Requested Level: AUTO | L0 | L1 | L2 | L3
Final Level: L2
Change Type: SMALL_CHANGE | BUG_FIX
Doc Mode: CHANGE_RECORD
Workflow: Tasks -> Code
Human Gate: Confirm after Tasks
```
