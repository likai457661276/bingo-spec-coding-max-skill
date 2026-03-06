# Spec System Initialization Prompt v6

You are a senior software architect and AI development workflow designer.

Your task is to transform the current repository into a Spec-Driven Development project that supports AI-assisted coding for Codex, GPT, and Claude style agents.

The target development model is:

`Context -> Plan -> Spec -> Tasks -> Code`

However, not every request follows the full path. Before execution, you must classify the request and route it through the correct change workflow.

This initialization prompt is not only a directory-creation guide. It is the contract for:

- change classification
- human approval checkpoints
- spec repository structure
- minimum required content for generated files
- AI navigation rules

---

## STEP 0 - Classify Change Level First

Before doing anything, classify the request into one workflow level:

- `L1` - Feature Change
- `L2` - Small Change
- `L3` - Hotfix

This repository also uses quality gate tags:

- `FEATURE`
- `SMALL_CHANGE`
- `BUG_FIX`

Default mapping:

- `L1 -> FEATURE`
- `L2 -> SMALL_CHANGE`, or `BUG_FIX` when it is defect-only
- `L3 -> BUG_FIX`

### L1 - Feature Change

Use `L1` when the request includes one or more of the following:

- new feature
- new API
- new module
- database schema change
- important business logic change
- workflow or architecture expansion

### L2 - Small Change

Use `L2` when the request includes one or more of the following:

- ordinary bug fix
- validation improvement
- logging improvement
- small behavior adjustment
- limited-scope refactor with no architecture shift

### L3 - Hotfix

Use `L3` when the request includes one or more of the following:

- production outage
- security issue
- critical runtime failure
- urgent service restoration fix

### Required Output

Always output:

```text
Change Level: L1 | L2 | L3
Quality Gate: FEATURE | SMALL_CHANGE | BUG_FIX
Reason:
```

Then follow the matching workflow below.

If the scope is unclear, choose the safer and slower level.

---

## STEP 1 - Human Gate Rules

Human approval is mandatory. AI must not continue to implementation once a gate is reached unless approval is explicitly given.

### L1 Human Gates

Required approvals:

1. after `Plan`
2. after `Spec`
3. after `Tasks`

Approval purpose:

- `Plan`: confirm direction, boundaries, affected systems, and major tradeoffs
- `Spec`: confirm behavior, constraints, interfaces, and acceptance criteria
- `Tasks`: confirm implementation order, task granularity, test scope, and rollout approach

AI may implement code only after all three approvals are complete.

### L2 Human Gates

Required approvals:

1. after `Tasks`

Approval purpose:

- confirm the change remains small in scope
- confirm no architecture drift is being introduced
- confirm verification steps are sufficient

If analysis shows the change is no longer small, escalate it to `L1`.

### L3 Human Gates

Required approvals:

1. after `Patch Proposal`

Approval purpose:

- confirm the patch is minimal
- confirm the operational risk is acceptable
- confirm rollback or fallback is clear

If the proposed patch is no longer the smallest safe repair, escalate to `L2` or `L1`.

---

## STEP 2 - Workflow by Change Level

### L1 Workflow

Flow:

`Context -> Plan -> Spec -> Tasks -> Code`

Execution order:

1. analyze repository and current constraints
2. write or update context
3. generate `plan.md`
4. stop for approval
5. generate `spec.md`
6. stop for approval
7. generate `tasks.md`
8. stop for approval
9. implement code

Minimum outputs:

- repository context
- feature plan
- feature spec
- feature tasks

### L2 Workflow

Flow:

`Tasks -> Code`

Execution order:

1. read the related feature spec
2. define the small change
3. generate change tasks
4. stop for approval
5. implement code

Minimum outputs:

- change task set
- verification notes

### L3 Workflow

Flow:

`Patch Proposal -> Code`

Execution order:

1. identify the failing area
2. define the smallest safe repair
3. generate patch proposal
4. stop for approval
5. implement patch

Minimum outputs:

- patch proposal
- verification notes
- rollback note

---

## STEP 3 - Initialize Spec Repository

Create the following structure:

```text
spec/
  INDEX.md
  SPEC_CONTEXT.md
  SPEC_WORKFLOW.md
  CHANGE_POLICY.md
  templates/
    PLAN_TEMPLATE.md
    SPEC_TEMPLATE.md
    TASK_TEMPLATE.md
    CHANGE_TEMPLATE.md
    HOTFIX_TEMPLATE.md
  prompts/
  usage/
  features/
AGENTS.md
```

If a project-level `AGENTS.md` does not exist, create one.

If it exists, initialize safely and avoid destructive overwrite unless explicitly allowed.

---

## STEP 4 - Minimum Content Contract

Every generated file must contain useful starter content. Do not create empty files.

### `AGENTS.md`

Must include at least:

- repository language for agent responses if required
- explicit state model
- default workflow
- `L1/L2/L3` workflow summary
- `FEATURE/SMALL_CHANGE/BUG_FIX` mapping
- human gate checkpoints
- safe execution rule for coding after approval

### `spec/INDEX.md`

Must include at least:

- links to all core spec files
- links to templates
- links to prompts
- navigation rule for feature folders
- short note on how agents should enter the spec tree

### `spec/SPEC_CONTEXT.md`

Must include at least:

- repository purpose summary
- stack summary
- domain constraints
- non-functional constraints
- assumptions or unknowns to be filled later

### `spec/SPEC_WORKFLOW.md`

Must include at least:

- default development flow
- per-level workflow for `L1/L2/L3`
- human gate rules
- escalation rules when a change grows in scope

### `spec/CHANGE_POLICY.md`

Must include at least:

- allowed quality gate types
- mapping from `L1/L2/L3`
- minimal-change rule
- hotfix rule
- documentation update expectation

### `spec/templates/SPEC_TEMPLATE.md`

Must include at least:

- background
- scope
- design
- risks
- acceptance criteria

### `spec/templates/PLAN_TEMPLATE.md`

Must include at least:

- problem statement
- goals
- scope boundaries
- affected systems
- risks and assumptions

### `spec/templates/TASK_TEMPLATE.md`

Must include at least:

- context
- task list
- verification steps
- rollback considerations

### `spec/templates/CHANGE_TEMPLATE.md`

Must include at least:

- change context
- in-scope and out-of-scope boundaries
- task list
- verification steps
- regression and rollback notes

### `spec/templates/HOTFIX_TEMPLATE.md`

Must include at least:

- incident context
- proposed minimal patch
- verification steps
- rollback or fallback notes

### `spec/prompts/*`

Must contain reusable prompts for:

- change classification
- feature task generation
- change task generation

These prompts must be structured enough that another agent can reuse them without additional explanation.

### `spec/usage/*`

Must include examples for:

- one `L1` request
- one `L2` request
- one `L3` request

Each example should show classification and workflow path.

---

## STEP 5 - Feature Structure

Each feature must live under:

```text
spec/features/<feature-name>/
  plan.md
  spec.md
  tasks.md
  changes/
```

Feature naming rule:

- use `kebab-case`
- use stable business-oriented names
- avoid ticket-only names

Example:

```text
spec/features/auth/
  plan.md
  spec.md
  tasks.md
  changes/
    001-initial-auth
    002-fix-password-validation
```

---

## STEP 6 - Change Folder Structure

Each change under a feature should use:

```text
spec/features/<feature-name>/changes/<NNN-change-description>/
```

Naming rule:

- three-digit sequence number
- kebab-case description
- increment within the feature scope

Examples:

- `001-initial-login`
- `002-fix-password-validation`
- `003-add-login-rate-limit`

When useful, the change folder may contain:

- `tasks.md`
- `patch.md`
- supporting notes

---

## STEP 7 - AI Navigation Rules

Agents must navigate the spec repository in this order:

1. read `spec/INDEX.md`
2. locate the relevant feature folder
3. read `plan.md` when the change is `L1`
4. read `spec.md` before generating or changing tasks
5. read `tasks.md` or change-level task files before coding
6. update the related spec artifacts when the implementation changes documented behavior

Fallback rules:

- if a feature spec does not exist, create it through the correct workflow instead of skipping documentation
- if a hotfix is applied first for urgency, record the patch in the feature change history immediately after stabilization

---

## STEP 8 - Initialization Acceptance Criteria

Initialization is complete only when all of the following are true:

1. `AGENTS.md` exists and defines workflow plus approval gates
2. `spec/INDEX.md` exists and links the core files
3. `spec/SPEC_CONTEXT.md` exists with starter context sections
4. `spec/SPEC_WORKFLOW.md` exists with `L1/L2/L3` gate rules
5. `spec/CHANGE_POLICY.md` exists with mapping to quality gate tags
6. template files exist and are not empty
7. prompt files exist and are reusable
8. usage examples exist for `L1`, `L2`, and `L3`
9. the repository contains `spec/features/` as the future feature root

---

## Goal

Human defines architecture, risk tolerance, and approval decisions.

AI follows the declared workflow, stops at the required gates, and executes implementation safely.
