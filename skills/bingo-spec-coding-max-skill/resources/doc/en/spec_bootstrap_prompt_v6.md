# Spec System Initialization Prompt v6

Initialize the repository into a Spec-Driven Development structure for AI-assisted work.

## STEP 0 - Classify First

Before planning, task generation, or coding, output:

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

Rules:

- `L0` is for clarification, analysis, code reading, option comparison, and read-only investigation
- external contract changes must be `L1 + FULL_SPEC`
- no direct `L2` without an existing feature spec
- `L3` is only for the smallest safe patch
- all levels require concrete `.md` files before implementation-driving commands

## STEP 1 - Human Gates

- `L0`: after `Answer` only if implementation should continue
- `L1`: after `Plan`, `Spec`, and `Tasks`
- `L2`: after `Tasks`
- `L3`: after `Patch Proposal`

## STEP 2 - Workflow Routing

- `L0`: `Context -> Investigation -> Answer`
- `L1`: `Context -> Plan -> Spec -> Tasks -> Code`
- `L2`: `Tasks -> Code`
- `L3`: `Patch Proposal -> Code`

## STEP 3 - Create Repository Structure

```text
spec/
  INDEX.md
  SPEC_CONTEXT.md
  SPEC_WORKFLOW.md
  CHANGE_POLICY.md
  templates/
  prompts/
  usage/
  questions/
  features/
AGENTS.md
```

## STEP 4 - Path Contract

- `L0`: `spec/questions/<date>-<topic>.md`
- `L1`: `spec/features/<feature-name>/plan.md`, `spec.md`, `tasks.md`
- `L2`: `spec/features/<feature-name>/smallchange/<date>-<change-name>.md`
- `L3`: `spec/features/<feature-name>/hotfix/<date>-<hotfix-name>.md`

## STEP 5 - Prompt Contract

Keep these files consistent with the same classification model:

- `change_classifier.prompt.md`
- `generate_question_answer.prompt.md`
- `generate_feature_tasks.prompt.md`
- `generate_change_tasks.prompt.md`
- `usage_examples.md`
