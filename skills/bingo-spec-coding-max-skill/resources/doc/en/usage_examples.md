# Usage Examples

## Example 1 - Add Login Feature

Request:

Add a login feature including a login page, authentication API, JWT issuance, and basic login tests.

Classification output:

```text
Requested Level: AUTO
Final Level: L1
Change Type: FEATURE
Doc Mode: FULL_SPEC
Workflow: Context -> Plan -> Spec -> Tasks -> Code
Human Gate: Confirm after Plan, Spec, and Tasks
Reason: The request adds new functionality, a new API, and a new authentication flow. It changes the external contract, so it must be L1, and there is no reusable baseline spec yet, so the required doc mode is FULL_SPEC.
Scope Signals: New login page; New authentication API; New JWT issuance flow; Caller-visible interface behavior will change
Escalation Note: None
```

Suggested paths:

- `spec/features/auth-login/plan.md`
- `spec/features/auth-login/spec.md`
- `spec/features/auth-login/tasks.md`
- `spec/features/auth-login/smallchange/`
- `spec/features/auth-login/hotfix/`

## Example 2 - Password Validation Bug

Request:

Passwords with leading or trailing spaces fail validation and should be fixed without changing the architecture. `spec/features/auth-login/spec.md` already exists.

Classification output:

```text
Requested Level: AUTO
Final Level: L2
Change Type: BUG_FIX
Doc Mode: CHANGE_RECORD
Workflow: Tasks -> Code
Human Gate: Confirm after Tasks
Reason: This is a local defect fix inside an existing login capability. It does not change API fields or semantics, and a reusable feature spec already exists, so it can remain L2 with CHANGE_RECORD documentation.
Scope Signals: Existing login capability; Existing feature spec can be reused; Only input normalization bug is fixed; No interface contract change
Escalation Note: Escalate to L1 if the fix expands into authentication-flow redesign, field semantic changes, or caller-visible interface behavior changes
```

Suggested path:

- `spec/features/auth-login/smallchange/2026-03-09-trim-password-input.md`

## Example 3 - Production Token Failure

Request:

JWT validation failures are causing broad production errors and service should be restored quickly.

Classification output:

```text
Requested Level: AUTO
Final Level: L3
Change Type: BUG_FIX
Doc Mode: HOTFIX_RECORD
Workflow: Patch Proposal -> Code
Human Gate: Confirm after Patch Proposal
Reason: This is a production incident fix whose current goal is rapid restoration through the smallest safe patch. No external contract change is required yet, so L3 with HOTFIX_RECORD is appropriate.
Scope Signals: Broad production failure; Rapid mitigation goal; Patch limited to JWT validation entrypoint; No new interface introduced
Escalation Note: Escalate to L2 or L1 if the patch grows into auth-chain redesign, interface changes, or a broad refactor
```

Suggested path:

- `spec/features/auth-login/hotfix/2026-03-09-jwt-validation-patch.md`
