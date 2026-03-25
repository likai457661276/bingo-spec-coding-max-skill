# Spec 体系初始化提示词 v6

将当前仓库初始化为适合 AI 协作的 Spec-Driven Development 结构。

## STEP 0 - 先分级

在进入规划、任务拆分或编码前，先输出：

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

规则：

- `L0` 用于问题澄清、分析、代码阅读、方案比较和只读调研
- 外部契约变更必须是 `L1 + FULL_SPEC`
- 没有既有 feature spec 时不得直接走 `L2`
- `L3` 仅用于最小安全补丁
- `L1`、`L2`、`L3` 在进入实现前都必须先落地实体 `.md` 文档
- `L0` 不强制落问题文档；若分析后已明确需要实现，可直接升级到 `L1`、`L2` 或 `L3`

## STEP 1 - 人类门禁

- `L0`：无需额外确认；可在 `Answer` 后结束，或直接升级并继续推进
- `L1`：先完成 `Plan`、`Spec`、`Tasks`，仅在 `Tasks` 后确认一次
- `L2`：在 `Tasks` 后确认
- `L3`：在 `Patch Proposal` 后确认

## STEP 2 - 工作流路由

- `L0`：`Context -> Investigation -> Answer`
- `L1`：`Context -> Plan -> Spec -> Tasks -> Code`
- `L2`：`Tasks -> Code`
- `L3`：`Patch Proposal -> Code`

## STEP 3 - 创建仓库结构

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

## STEP 4 - 路径约定

- `L0`：如需沉淀分析记录，可写入 `spec/questions/<date>-<topic>.md`
- `L1`：`spec/features/<feature-name>/plan.md`、`spec.md`、`tasks.md`
- `L2`：`spec/features/<feature-name>/smallchange/<date>-<change-name>.md`
- `L3`：`spec/features/<feature-name>/hotfix/<date>-<hotfix-name>.md`

## STEP 5 - Prompt 一致性

以下文件必须共享同一套分级模型：

- `change_classifier.prompt.md`
- `generate_question_answer.prompt.md`
- `generate_feature_tasks.prompt.md`
- `generate_change_tasks.prompt.md`
- `usage_examples.md`
