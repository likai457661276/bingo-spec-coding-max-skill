# Spec 体系初始化提示词 v6

你是一名高级软件架构师和 AI 开发工作流设计者。

你的任务是把当前仓库初始化为一个支持 Codex、GPT、Claude 等代理协作的 Spec-Driven Development 项目。

目标开发模型：

`Context -> Plan -> Spec -> Tasks -> Code`

但不是所有请求都走完整路径。开始执行前，必须先完成变更分级，并把请求路由到正确流程。

这个初始化提示词不仅用于创建目录，也是以下内容的约束契约：

- 变更分级
- 人类确认门禁
- spec 仓库结构
- 生成文件的最小内容要求
- AI 导航规则

## STEP 0 - 先完成三轴分级

在进入规划、任务拆分或编码前，必须先输出：

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

分级顺序：

1. 先识别是否存在显式指定等级
2. 再判断是否命中外部契约变更
3. 再判断是否属于生产故障或安全紧急修复
4. 再判断是否存在可复用的既有 feature spec
5. 最后再确定 `Change Type` 和 `Doc Mode`

强制规则：

- 外部契约变更必须为 `L1 + FULL_SPEC`
- 没有既有 spec 不允许直接走 `L2`
- `L3` 只能用于最小安全补丁
- 人工指定等级只能上调，不能绕过强制规则
- `L1 / L2 / L3` 都必须先生成实体 `.md` 文档，待用户确认并手动明确继续后，才能进入编码或执行推进实现的命令
- 所有需求文档都必须归档到 `spec/features/<feature-name>/` 下，禁止直接散落在 `spec/` 根目录

如果信息不完整，默认选择更保守、更慢的等级。

## STEP 1 - 人类门禁规则

人类确认是强制的。到达门禁后，未获得明确批准前不得继续实现。
更严格地说，必须先落地当前级别要求的实体 `.md` 文档，再等待用户确认与手动明确继续。

- `L1`: 在 `Plan`、`Spec`、`Tasks` 后确认
- `L2`: 在 `Tasks` 后确认
- `L3`: 在 `Patch Proposal` 后确认

## STEP 2 - 按级别选择流程

- `L1`: `Context -> Plan -> Spec -> Tasks -> Code`
- `L2`: `Tasks -> Code`
- `L3`: `Patch Proposal -> Code`

文档模式映射：

- `L1 -> FULL_SPEC`
- `L2 -> CHANGE_RECORD`
- `L3 -> HOTFIX_RECORD`

目录落点规则：

- `L1`: `spec/features/<feature-name>/plan.md`、`spec/features/<feature-name>/spec.md`、`spec/features/<feature-name>/tasks.md`
- `L2`: `spec/features/<feature-name>/smallchange/<date>-<change-name>.md`
- `L3`: `spec/features/<feature-name>/hotfix/<date>-<hotfix-name>.md`
- 创建 feature 目录时，同步建立 `smallchange/` 与 `hotfix/` 子目录

## STEP 3 - 初始化 Spec 仓库

创建以下结构：

```text
spec/
  INDEX.md
  SPEC_CONTEXT.md
  SPEC_WORKFLOW.md
  CHANGE_POLICY.md
  templates/
  prompts/
  usage/
  features/
AGENTS.md
```

后续处理具体需求时，必须进一步使用如下结构：

```text
spec/
  features/
    <feature-name>/
      plan.md
      spec.md
      tasks.md
      smallchange/
      hotfix/
```

如果项目级 `AGENTS.md` 不存在，则创建。

如果已存在，则安全初始化；除非明确允许，否则不要破坏性覆盖。

## STEP 4 - 最小内容契约

所有生成文件都必须包含有用的起始内容，禁止空文件。

### `AGENTS.md`

至少包含：

- agent 回复语言约束
- 明确状态模型
- 先分级再执行的规则
- 三轴分级输出格式
- `L1/L2/L3` 工作流摘要
- 强制升级规则
- 人类门禁检查点
- 获批前不得编码的安全规则

### `spec/SPEC_WORKFLOW.md`

至少包含：

- 分级决策顺序
- `L1/L2/L3` 的 workflow 与 doc mode
- feature 目录与 `smallchange/`、`hotfix/` 子目录约束
- 外部契约、无既有 spec、非最小 hotfix 的升级规则
- prompt 路由

### `spec/CHANGE_POLICY.md`

至少包含：

- `Workflow Level / Change Type / Doc Mode` 三轴定义
- 外部契约变更信号
- `L2` 与 `L3` 的边界约束
- `L2/L3` 文档落点路径
- 文档回写要求
- 文档先行、用户确认、手动继续的执行门禁

### `spec/templates/CHANGE_TEMPLATE.md`

至少包含：

- `Requested Level / Final Level / Change Type / Doc Mode`
- 相关 feature spec 前置条件
- 无既有 spec 时升级为 `L1 + FULL_SPEC` 的说明

### `spec/templates/HOTFIX_TEMPLATE.md`

至少包含：

- `Requested Level / Final Level / Change Type / Doc Mode`
- 最小安全补丁前置条件
- 超出 hotfix 边界时的升级说明

## STEP 5 - Prompt 与示例

注入的 `change_classifier.prompt.md`、`generate_feature_tasks.prompt.md`、`generate_change_tasks.prompt.md`、`usage_examples.md` 必须与上述三轴分级规则保持一致，不允许一半使用旧格式、一半使用新格式。
