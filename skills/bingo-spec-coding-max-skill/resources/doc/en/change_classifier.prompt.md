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

## Three Axes

### 1. Workflow Level

- `L1`
  - Full feature flow
  - Requires `Context -> Plan -> Spec -> Tasks -> Code`
  - Use for new capabilities, external contract changes, cross-module design changes, and important business expansions

- `L2`
  - Small-change flow
  - Requires `Tasks -> Code`
  - Use for local adjustments, small fixes, and local refactors on top of an existing capability
  - A reusable feature spec must already exist; otherwise escalate to `L1`

- `L3`
  - Urgent-fix flow
  - Requires `Patch Proposal -> Code`
  - Only use for the smallest safe patch to a production incident, security issue, or critical online failure

### 2. Change Type

- `FEATURE`
  - new capability, significant business expansion, or new/changed external contract
- `SMALL_CHANGE`
  - limited behavior adjustment, local refactor, or local non-defect optimization
- `BUG_FIX`
  - defect fix, regression fix, or incident fix

### 3. Doc Mode

- `FULL_SPEC`
  - must produce full `plan/spec/tasks`
- `CHANGE_RECORD`
  - must record a change under an existing feature
- `HOTFIX_RECORD`
  - must record the hotfix approach and backfill spec history after stabilization

## Hard Rules

### Rule A: External contract changes must be at least L1

If any of the following is true, `Final Level` must be `L1` and `Doc Mode` must be `FULL_SPEC`:

- new API
- changed API path, method, auth, status code, or error code
- changed request fields, response fields, field semantics, or requiredness
- changed database schema
- changed message contract, event shape, WebSocket payload shape
- changed import/export file format
- changed permission points or role boundaries
- changed interface behavior visible to other systems, frontend apps, mobile clients, or scripts

### Rule B: No direct L2 without an existing spec

If the work looks like a small change but the related feature has no reusable `spec.md` or baseline spec record:

- do not use `L2`
- escalate to at least `L1`
- `Doc Mode` must be `FULL_SPEC`

### Rule C: L3 is only for the smallest safe patch

Only use `L3` when the goal is rapid service restoration and the patch scope is minimal.

Do not keep `L3` if the fix already involves any of the following:

- cross-module redesign
- a new interface or new flow
- an external contract change
- broad refactoring
- full validation of new business logic

Escalate to `L2` or `L1` instead.

### Rule D: Explicitly requested levels may only raise, not violate hard rules

If a developer or user explicitly requests a level:

- you may accept a more conservative, higher level
- you may not accept a lower level that conflicts with hard rules

## Decision Order

Evaluate in this order and do not skip steps:

1. Detect whether a level was explicitly requested
2. Detect whether the request changes an external contract
3. Detect whether the request is a production or security emergency fix
4. Detect whether an existing spec can be reused
5. Then classify `FEATURE`, `SMALL_CHANGE`, or `BUG_FIX`

When information is incomplete, choose the more conservative and slower level.

## Stack-Specific Signals

### Java / Spring Boot

Prefer `L1` when the request touches any of the following:

- add or modify a `Controller` endpoint
- add or modify request/response DTO, VO, Query, or Form objects
- change Feign, OpenAPI, or Swagger-exposed structures
- change database tables, fields, indexes, constraints, or migration scripts
- change WebSocket payloads, OnlyOffice integration protocol, or export format
- change authentication, authorization, role permissions, or tenant isolation boundaries

Usually safe for `L2`:

- local null-check fix
- logging improvements
- local validation fix
- SQL optimization without interface contract changes
- internal refactor without caller-visible behavior changes

### Python

Prefer `L1` when the request touches any of the following:

- add or modify FastAPI / Flask / Django APIs
- change Pydantic schemas, serializers, or request/response models
- change Celery or message-queue input/output contracts
- change database migrations or ORM model structure
- change public SDKs, CLI argument protocol, or export format
- change auth, middleware, or tenant/permission boundaries

Usually safe for `L2`:

- local exception-handling fix
- parameter validation bug fix
- internal function refactor
- performance optimization without interface changes
- added tests, logs, or monitoring

### Frontend

Prefer `L1` when the request touches any of the following:

- new page, core business flow, or key route
- new or changed dependency on an external API contract
- changed form fields, submission flow, or user-visible business rules
- changed state transitions, permission visibility, or critical submission / review / payment paths
- changed public component API affecting multiple pages
- changed import/export format, file protocol, or realtime message structure

Usually safe for `L2`:

- style fix
- local interaction fix
- copy update
- internal component refactor without business meaning changes
- non-contract analytics, logs, or small performance tuning

## Recommended Mapping Between Level And Change Type

- `L1` usually maps to `FEATURE`
- `L2` usually maps to `SMALL_CHANGE`
- defect-only `L2` may map to `BUG_FIX`
- `L3` maps to `BUG_FIX`

Notes:

- `Change Type` does not determine `Final Level`
- even a small code change must be `L1` if it changes an external contract

## Doc Mode Rules

- if `Final Level = L1`, then `Doc Mode = FULL_SPEC`
- if `Final Level = L2`, then `Doc Mode = CHANGE_RECORD`
- if `Final Level = L3`, then `Doc Mode = HOTFIX_RECORD`

Additional requirements:

- `L2` must attach to an existing feature spec
- if no feature spec exists, escalate to `L1 + FULL_SPEC`
- after service recovery, `L3` still needs spec history backfill
- all requirement documents must be written under `spec/features/<feature-name>/`, never directly under the `spec/` root

## Human Gate Rules

- `L1`: confirmation required after `Plan`, `Spec`, and `Tasks`
- `L2`: confirmation required after `Tasks`
- `L3`: confirmation required after `Patch Proposal`

Additional hard requirement:

- `L1` must first create `spec/features/<feature-name>/`, then save `plan.md`, `spec.md`, and `tasks.md`
- `L2` must first generate and save `<date>-<change-name>.md` under `spec/features/<feature-name>/smallchange/`
- `L3` must first generate and save `<date>-<hotfix-name>.md` under `spec/features/<feature-name>/hotfix/`
- when a feature folder is created, create `smallchange/` and `hotfix/` under it too
- for every level, wait for user confirmation and a manual go-ahead before coding or running implementation-driving commands

## Reason Requirements

`Reason` must explicitly explain:

- why this is the chosen `Final Level`
- whether an external contract change was detected
- whether an existing spec exists
- why this `Doc Mode` was chosen

## Scope Signals Requirements

`Scope Signals` must list the concrete signals you used, separated by semicolons.

Example:

```text
Scope Signals: Added teacher enrollment API; Added request DTO and response VO; Frontend calling pattern will change; External contract is newly introduced
```

## Escalation Note Requirements

- use `None` when there is no escalation risk
- otherwise state the exact condition that would force escalation

## Final Execution Requirement

Return only the required output fields in the required order. Do not add extra sections, do not use Markdown lists, and do not omit fields.
