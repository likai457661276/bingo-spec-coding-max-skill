# Change Tasks 生成器

为 `L2` 请求生成 `CHANGE_RECORD`。

## Required Inputs

- 相关 feature spec
- 变更描述
- 已确认的分级输出，其中 `Final Level = L2`

## Rules

- 保持改动最小
- 避免架构变化
- 必须包含验证
- 若不存在既有 feature spec，不得继续按 `L2` 生成，必须升级为 `L1 + FULL_SPEC`
- 如果请求仍只是分析或解释，应回退为 `L0`，而不是继续生成 change tasks

## Output Structure

```markdown
# Change Tasks: <change-name>

## Classification

Requested Level: AUTO | L0 | L1 | L2 | L3
Final Level: L2
Change Type: SMALL_CHANGE | BUG_FIX
Doc Mode: CHANGE_RECORD
Workflow: Tasks -> Code
Human Gate: Confirm after Tasks
```
