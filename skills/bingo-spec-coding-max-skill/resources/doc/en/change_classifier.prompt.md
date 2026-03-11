# Change Classification Prompt

Before planning, task decomposition, or coding, classify the current request.

Classify on three axes:

1. `Workflow Level`
2. `Change Type`
3. `Doc Mode`

## Required Output Fields

Return exactly:

```text
Requested Level: AUTO | L0 | L1 | L2 | L3
Final Level: L0 | L1 | L2 | L3
Change Type: QUESTION | FEATURE | SMALL_CHANGE | BUG_FIX
Doc Mode: QUESTION_RECORD | FULL_SPEC | CHANGE_RECORD | HOTFIX_RECORD
Workflow: Context -> Investigation -> Answer | Context -> Plan -> Spec -> Tasks -> Code | Tasks -> Code | Patch Proposal -> Code
Human Gate:
Reason:
Scope Signals:
Escalation Note:
```

## Decision Rules

1. If the request is explanation, analysis, investigation, or option comparison without a direct implementation ask, prefer `L0 + QUESTION_RECORD`.
2. External contract changes must be at least `L1`, and `Doc Mode` must be `FULL_SPEC`.
3. Do not use `L2` unless an existing feature spec can be reused.
4. Use `L3` only for the smallest safe patch to a production incident, security issue, or critical failure.
5. Explicitly requested levels may raise conservatism, but may not bypass hard rules.

## Decision Order

1. Check whether the request is analysis-only.
2. Check whether a level was explicitly requested.
3. Check whether the request changes an external contract.
4. Check whether the request is a production or security emergency fix.
5. Check whether an existing spec can be reused.
6. Then finalize `Change Type` and `Doc Mode`.

When information is incomplete, choose the more conservative and slower level.

## Human Gate Rules

- `L0`: confirmation required after `Answer` only if implementation should continue
- `L1`: confirmation required after `Plan`, `Spec`, and `Tasks`
- `L2`: confirmation required after `Tasks`
- `L3`: confirmation required after `Patch Proposal`

## Path Rules

- `L0`: `spec/questions/<date>-<topic>.md`
- `L1`: `spec/features/<feature-name>/plan.md`, `spec.md`, `tasks.md`
- `L2`: `spec/features/<feature-name>/smallchange/<date>-<change-name>.md`
- `L3`: `spec/features/<feature-name>/hotfix/<date>-<hotfix-name>.md`

If an `L0` investigation turns into a concrete implementation ask, reclassify into `L1`, `L2`, or `L3`.

## Final Execution Requirement

Return only the required output fields in the required order.
