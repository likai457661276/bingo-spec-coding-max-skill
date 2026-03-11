# Feature Tasks Generator

Generate `tasks.md` for an `L1` feature change.

## Required Inputs

- `plan.md`
- `spec.md`
- confirmed classification output where `Final Level = L1`

Do not generate tasks until these inputs are available.

## Output Structure

```markdown
# Tasks: <feature-name>

## Classification

Final Level: L1
Change Type: FEATURE
Doc Mode: FULL_SPEC

## Context

Summarize the feature goal, affected area, and implementation assumptions.
```
