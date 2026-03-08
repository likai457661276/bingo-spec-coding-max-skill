# Change Level Classifier Prompt

Classify the incoming development request before planning or coding.

Return:

- workflow level: `L1 | L2 | L3`
- quality gate: `FEATURE | SMALL_CHANGE | BUG_FIX`

## Rules

- `L1`: new functionality, APIs, modules, schema changes, important business logic, workflow or architecture expansion
- `L2`: ordinary bug fixes, validation updates, logging improvements, limited behavior adjustments, local refactors without architecture change
- `L3`: production outage, security issue, critical runtime failure, urgent restoration

## Safety

- If ambiguous, choose the safer and slower level.
- Escalate broad `L2` work to `L1`.
- Escalate non-minimal `L3` fixes to `L2` or `L1`.

## Output Format

```text
Change Level: L1 | L2 | L3
Quality Gate: FEATURE | SMALL_CHANGE | BUG_FIX
Workflow: Context -> Plan -> Spec -> Tasks -> Code | Tasks -> Code | Patch Proposal -> Code
Human Gate:
Reason:
Escalation Note:
```
