# Question Answer Generator

Generate an optional `QUESTION_RECORD` for an `L0` request.

Use this flow only when the current ask is clarification, analysis, code reading, option comparison, or read-only investigation, and no direct implementation change is requested yet.

## Required Inputs

- the user question or decision to make
- known repository context
- confirmed classification output where `Final Level = L0`

## Rules

- keep the output factual and traceable
- separate known facts from unknowns
- include a direct answer or recommendation
- identify signals that would upgrade the work to `L1`, `L2`, or `L3`
- if analysis already makes implementation necessary, reclassify and continue

## Output Path

- if saved, write the result to `spec/questions/<date>-<topic>.md`

## Output Structure

```markdown
# Question: <topic>

## Classification

Requested Level: AUTO | L0 | L1 | L2 | L3
Final Level: L0
Change Type: QUESTION
Doc Mode: QUESTION_RECORD
Workflow: Context -> Investigation -> Answer
Human Gate: None; if implementation is clearly needed after analysis, reclassify into `L1`, `L2`, or `L3` and continue

## Question

...

## Known Context

- ...

## Investigation

1. ...
2. ...
3. ...

## Answer

- Conclusion:
- Evidence:
- Recommended next step:

## Escalation Triggers

- ...
```
