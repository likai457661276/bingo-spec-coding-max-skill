# 变更分级提示词

在进入规划、任务拆分或编码前，先对当前请求做分级判断。

需要同时判断三条轴线：

1. `Workflow Level`
2. `Change Type`
3. `Doc Mode`

## 必须输出的字段

严格输出：

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

## 决策规则

1. 如果请求只是解释、分析、排查、代码阅读或方案比较，且没有直接要求改实现，优先归类为 `L0 + QUESTION_RECORD`。
2. 外部契约变更必须至少为 `L1`，且 `Doc Mode` 必须为 `FULL_SPEC`。
3. 没有可复用的既有 feature spec 时，不得直接走 `L2`。
4. `L3` 只能用于生产故障、安全问题或线上关键失败的最小安全补丁。
5. 显式指定等级只能上调，不能绕过硬规则。

## 决策顺序

1. 先判断请求是否仅为分析类问题。
2. 再判断是否存在显式指定等级。
3. 再判断是否命中外部契约变更。
4. 再判断是否属于生产故障或安全紧急修复。
5. 再判断是否存在可复用的既有 spec。
6. 最后确定 `Change Type` 和 `Doc Mode`。

信息不完整时，默认选择更保守、更慢的等级。

## Human Gate 规则

- `L0`：无需额外确认；可在 `Answer` 后结束，或直接升级并继续推进
- `L1`：先完成 `Plan`、`Spec`、`Tasks`，仅在 `Tasks` 后确认一次
- `L2`：在 `Tasks` 后确认
- `L3`：在 `Patch Proposal` 后确认

## 路径规则

- `L0`：如需沉淀分析记录，可写入 `spec/questions/<date>-<topic>.md`
- `L1`：`spec/features/<feature-name>/plan.md`、`spec.md`、`tasks.md`
- `L2`：`spec/features/<feature-name>/smallchange/<date>-<change-name>.md`
- `L3`：`spec/features/<feature-name>/hotfix/<date>-<hotfix-name>.md`

如果 `L0` 分析在过程中转成明确实现请求，应直接重新分级到 `L1`、`L2` 或 `L3` 并继续推进。

## 最终执行要求

只输出要求的字段，且顺序不能变。
