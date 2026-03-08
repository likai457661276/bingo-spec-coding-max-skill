# 变更分级提示词

在规划或编码前，先对输入的开发请求进行分级。

必须同时输出：

- workflow level: `L1 | L2 | L3`
- quality gate: `FEATURE | SMALL_CHANGE | BUG_FIX`

## Classification Rules

### `L1` - Feature Change

满足以下任一条件时使用 `L1`：

- 新功能
- 新 API
- 新模块
- 数据库 schema 变更
- 重要业务逻辑扩展
- 工作流或架构扩展

默认质量门禁：

- `FEATURE`

### `L2` - Small Change

满足以下任一条件时使用 `L2`：

- 普通 bug 修复
- 校验更新
- 日志改进
- 小范围行为调整
- 不改变架构的局部重构

默认质量门禁：

- `SMALL_CHANGE`
- 如果是纯缺陷修复，可使用 `BUG_FIX`

### `L3` - Hotfix

满足以下任一条件时使用 `L3`：

- 生产故障
- 安全问题
- 关键运行时失败
- 紧急恢复服务

默认质量门禁：

- `BUG_FIX`

## Safety Rules

- 如果请求有歧义，选择更保守、更慢的级别。
- 若 `L2` 需要跨模块重设计，升级为 `L1`。
- 若 `L3` 不是最小安全补丁，升级为 `L2` 或 `L1`。

## Human Gate Summary

- `L1`: 在 `Plan`、`Spec`、`Tasks` 后需要人类确认
- `L2`: 在 `Tasks` 后需要人类确认
- `L3`: 在 `Patch Proposal` 后需要人类确认

## Output Format

严格按以下结构返回：

```text
Change Level: L1 | L2 | L3
Quality Gate: FEATURE | SMALL_CHANGE | BUG_FIX
Workflow: Context -> Plan -> Spec -> Tasks -> Code | Tasks -> Code | Patch Proposal -> Code
Human Gate:
Reason:
Escalation Note:
```
