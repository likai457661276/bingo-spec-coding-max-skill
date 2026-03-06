# Change Level Classifier Prompt

Classify the incoming development request before planning or coding.

You must output both:

- workflow level: `L1 | L2 | L3`
- quality gate: `FEATURE | SMALL_CHANGE | BUG_FIX`

## Classification Rules

### `L1` - Feature Change

Use `L1` when the request includes one or more of the following:

- new functionality
- new API
- new module
- database schema change
- important business logic expansion
- workflow or architecture expansion

Default quality gate:

- `FEATURE`

### `L2` - Small Change

Use `L2` when the request includes one or more of the following:

- ordinary bug fix
- validation update
- logging improvement
- limited behavior adjustment
- local refactor without architecture change

Default quality gate:

- `SMALL_CHANGE`
- use `BUG_FIX` if the request is defect-only

### `L3` - Hotfix

Use `L3` when the request includes one or more of the following:

- production outage
- security issue
- critical runtime failure
- urgent operational restoration

Default quality gate:

- `BUG_FIX`

## Safety Rules

- If the request is ambiguous, choose the safer and slower level.
- If a proposed `L2` change needs cross-module redesign, escalate to `L1`.
- If a proposed `L3` fix is not the smallest safe patch, escalate to `L2` or `L1`.

## Human Gate Summary

- `L1`: human approval required after `Plan`, `Spec`, and `Tasks`
- `L2`: human approval required after `Tasks`
- `L3`: human approval required after `Patch Proposal`

## Output Format

Return exactly this structure:

```text
Change Level: L1 | L2 | L3
Quality Gate: FEATURE | SMALL_CHANGE | BUG_FIX
Workflow: Context -> Plan -> Spec -> Tasks -> Code | Tasks -> Code | Patch Proposal -> Code
Human Gate:
Reason:
Escalation Note:
```

Output guidance:

- `Workflow` must match the classified level
- `Human Gate` must state the exact approval checkpoint
- `Escalation Note` should say `None` if no escalation concern exists
