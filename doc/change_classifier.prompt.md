# Change Classification Prompt

Before planning, task decomposition, or coding, classify the current development request.

The goal is not only to estimate code size. You must classify across:

1. `Workflow Level`
2. `Change Type`
3. `Doc Mode`

Prioritize the following:

- external contract changes must not be downgraded by mistake
- behavior-changing work must not land without documentation
- urgent fixes must stay on the smallest safe patch path

## Required Output Fields

Return exactly these fields and do not omit any of them:

```text
Requested Level: AUTO | L1 | L2 | L3
Final Level: L1 | L2 | L3
Change Type: FEATURE | SMALL_CHANGE | BUG_FIX
Doc Mode: FULL_SPEC | CHANGE_RECORD | HOTFIX_RECORD
Workflow: Context -> Plan -> Spec -> Tasks -> Code | Tasks -> Code | Patch Proposal -> Code
Human Gate:
Reason:
Scope Signals:
Escalation Note:
```

Field notes:

- `Requested Level`: use the explicit level from user, developer, or system instructions when present; otherwise use `AUTO`
- `Final Level`: the final level after applying the rules
- `Change Type`: the type of change, not the workflow level
- `Doc Mode`: the documentation depth that must be produced for this request

## Hard Rules

1. External contract changes must be at least `L1`, and `Doc Mode` must be `FULL_SPEC`.
2. Do not use `L2` unless an existing feature spec can be reused.
3. Use `L3` only for the smallest safe patch to a production incident, security issue, or critical failure.
4. Explicitly requested levels may raise conservatism, but may not bypass hard rules.

## Decision Order

1. Check whether a level was explicitly requested.
2. Check whether the request changes an external contract.
3. Check whether the request is a production or security emergency fix.
4. Check whether an existing spec can be reused.
5. Then classify `FEATURE`, `SMALL_CHANGE`, or `BUG_FIX`.

When information is incomplete, choose the more conservative and slower level.

## Human Gate Rules

- `L1`: confirmation required after `Plan`, `Spec`, and `Tasks`
- `L2`: confirmation required after `Tasks`
- `L3`: confirmation required after `Patch Proposal`

## Final Execution Requirement

Return only the required output fields in the required order. Do not add extra sections, do not use Markdown lists, and do not omit fields.
