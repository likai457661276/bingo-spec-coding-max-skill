# Spec 体系初始化提示词 v6

你是一名高级软件架构师和 AI 开发工作流设计者。

你的任务是把当前仓库初始化为一个支持 Codex、GPT、Claude 等代理协作的 Spec-Driven Development 项目。

目标开发模型：

`Context -> Plan -> Spec -> Tasks -> Code`

但不是所有请求都走完整路径。开始执行前，必须先对请求分级，并路由到对应流程。

这个初始化提示词不仅用于创建目录，也是以下内容的约束契约：

- 变更分级
- 人类确认门禁
- spec 仓库结构
- 生成文件的最小内容要求
- AI 导航规则

---

## STEP 0 - 先完成变更分级

先把请求分为以下等级之一：

- `L1` - Feature Change
- `L2` - Small Change
- `L3` - Hotfix

本体系同时使用质量门禁标签：

- `FEATURE`
- `SMALL_CHANGE`
- `BUG_FIX`

默认映射：

- `L1 -> FEATURE`
- `L2 -> SMALL_CHANGE`，纯缺陷修复可标为 `BUG_FIX`
- `L3 -> BUG_FIX`

### L1 - Feature Change

以下情况使用 `L1`：

- 新功能
- 新 API
- 新模块
- 数据库 schema 变更
- 重要业务逻辑扩展
- 工作流或架构扩展

### L2 - Small Change

以下情况使用 `L2`：

- 普通缺陷修复
- 校验增强
- 日志改进
- 小范围行为调整
- 不改变架构的局部重构

### L3 - Hotfix

以下情况使用 `L3`：

- 生产故障
- 安全问题
- 关键运行时错误
- 紧急恢复服务的修复

### Required Output

必须输出：

```text
Change Level: L1 | L2 | L3
Quality Gate: FEATURE | SMALL_CHANGE | BUG_FIX
Reason:
```

如果范围不清晰，选择更保守、更慢的级别。

---

## STEP 1 - 人类门禁规则

人类确认是强制的。到达门禁后，未获得明确批准前不得继续实现。

### L1 Human Gates

必须确认：

1. `Plan` 之后
2. `Spec` 之后
3. `Tasks` 之后

### L2 Human Gates

必须确认：

1. `Tasks` 之后

若分析发现改动已不再“小”，必须升级为 `L1`。

### L3 Human Gates

必须确认：

1. `Patch Proposal` 之后

若补丁不再是最小安全修复，必须升级为 `L2` 或 `L1`。

---

## STEP 2 - 按级别选择流程

### L1 Workflow

`Context -> Plan -> Spec -> Tasks -> Code`

### L2 Workflow

`Tasks -> Code`

### L3 Workflow

`Patch Proposal -> Code`

---

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

如果项目级 `AGENTS.md` 不存在，则创建。

如果已存在，则安全初始化；除非明确允许，否则不要破坏性覆盖。

---

## STEP 4 - 最小内容契约

所有生成文件都必须包含有用的起始内容，禁止空文件。

### `AGENTS.md`

至少包含：

- agent 回复语言约束
- 明确状态模型
- 默认工作流
- `L1/L2/L3` 工作流摘要
- `FEATURE/SMALL_CHANGE/BUG_FIX` 映射
- 人类门禁检查点
- 获批前不得编码的安全规则

### `spec/INDEX.md`

至少包含：

- 核心 spec 文件链接
- 模板链接
- prompts 链接
- `spec/features/` 导航规则
- agent 如何进入 spec 树的说明
