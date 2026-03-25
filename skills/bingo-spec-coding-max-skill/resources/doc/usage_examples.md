# Usage Examples

## Example 0 - Analyze Why Login Keeps Failing

```text
Requested Level: AUTO
Final Level: L0
Change Type: QUESTION
Doc Mode: QUESTION_RECORD
Workflow: Context -> Investigation -> Answer
Human Gate: None; if implementation is clearly needed after analysis, escalate to L1, L2, or L3 and continue
Reason: The user is asking for diagnosis and explanation first, not an implementation change.
Scope Signals: Read-only investigation; compare possibilities; no direct code change requested
Escalation Note: Reclassify to L1, L2, or L3 and continue if the request turns into implementation work
```

## Example 1 - Add Login Feature

```text
Requested Level: AUTO
Final Level: L1
Change Type: FEATURE
Doc Mode: FULL_SPEC
Workflow: Context -> Plan -> Spec -> Tasks -> Code
Human Gate: Complete Plan, Spec, and Tasks, then confirm once after Tasks
Reason: New capability plus a new external interface requires full feature workflow.
Scope Signals: New login page; New authentication API; New JWT issuance flow
Escalation Note: None
```

## Example 2 - Password Validation Bug

```text
Requested Level: AUTO
Final Level: L2
Change Type: BUG_FIX
Doc Mode: CHANGE_RECORD
Workflow: Tasks -> Code
Human Gate: Confirm after Tasks
Reason: Local defect fix on top of an existing feature spec with no contract change.
Scope Signals: Existing feature spec; Local input normalization fix; No interface change
Escalation Note: Escalate to L1 if the fix changes interface behavior
```

## Example 3 - Production Token Failure

```text
Requested Level: AUTO
Final Level: L3
Change Type: BUG_FIX
Doc Mode: HOTFIX_RECORD
Workflow: Patch Proposal -> Code
Human Gate: Confirm after Patch Proposal
Reason: Production recovery using the smallest safe patch fits hotfix flow.
Scope Signals: Broad production failure; Rapid restoration target; Minimal patch scope
Escalation Note: Escalate to L2 or L1 if the patch stops being minimal
```
