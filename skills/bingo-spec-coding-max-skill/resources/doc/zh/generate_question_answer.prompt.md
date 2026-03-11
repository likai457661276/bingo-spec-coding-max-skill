# 问题答复生成器

为 `L0` 请求生成 `QUESTION_RECORD` 文档。

仅当当前请求属于问题澄清、原因分析、代码阅读、方案比较或只读调研，且尚未要求直接修改实现时使用本流程。

## Required Inputs

- 用户问题或待判断事项
- 已知仓库上下文
- 已确认的分级输出，其中 `Final Level = L0`

## Rules

- 输出必须基于事实并可追溯
- 已知事实与未知点要分开写
- 必须给出明确结论或建议
- 明确哪些信号会把当前工作升级为 `L1`、`L2` 或 `L3`
- 未重新分级前，不得输出推进实现的执行步骤

## Output Path

- 保存到 `spec/questions/<date>-<topic>.md`

## Output Structure

```markdown
# Question: <topic>

## Classification

Requested Level: AUTO | L0 | L1 | L2 | L3
Final Level: L0
Change Type: QUESTION
Doc Mode: QUESTION_RECORD
Workflow: Context -> Investigation -> Answer
Human Gate: 先保存 `spec/questions/<date>-<topic>.md`；若后续要进入实现，需升级为 `L1`、`L2` 或 `L3`

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
