# 变更分级提示词

在进入规划、任务拆分或编码前，先对当前开发请求做分级判断。

你的目标不是只判断“代码改动大小”，而是同时判断：

1. 工作流等级 `Workflow Level`
2. 变更类型 `Change Type`
3. 文档模式 `Doc Mode`

必须优先保证：

- 外部契约变更不会被误降级
- 有行为变化的需求不会无文档落地
- 紧急修复只走最小安全补丁

## 必须输出的字段

严格输出以下字段，不要省略：

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

说明：

- `Requested Level`：如果用户、开发者、系统提示中明确指定了等级，则填该值；否则填 `AUTO`
- `Final Level`：你结合规则后最终采用的等级
- `Change Type`：表示改动性质，不等同于工作流等级
- `Doc Mode`：表示本次必须沉淀的文档深度

## 三轴定义

### 1. Workflow Level

- `L1`
  - 完整特性流程
  - 需要 `Context -> Plan -> Spec -> Tasks -> Code`
  - 适用于新增能力、外部契约变化、跨模块设计变化、重要业务扩展

- `L2`
  - 小改动流程
  - 需要 `Tasks -> Code`
  - 适用于已有能力上的局部调整、小范围修复、局部重构
  - 前提是相关 feature 已有可依赖的 spec；若没有，则至少升级为 `L1`

- `L3`
  - 紧急修复流程
  - 需要 `Patch Proposal -> Code`
  - 仅适用于生产故障、安全问题、线上关键失败的最小安全补丁

### 2. Change Type

- `FEATURE`
  - 新增能力、显著业务扩展、外部契约新增或变更
- `SMALL_CHANGE`
  - 小范围行为调整、局部重构、非缺陷类局部优化
- `BUG_FIX`
  - 缺陷修复、回归修复、线上故障修复

### 3. Doc Mode

- `FULL_SPEC`
  - 需要完整沉淀 `plan/spec/tasks`
- `CHANGE_RECORD`
  - 需要在既有 feature 下记录 change
- `HOTFIX_RECORD`
  - 需要记录 hotfix 方案，并在稳定后补回规格历史

## 强制规则

### 规则 A：外部契约变更必须至少为 L1

若满足任一条件，`Final Level` 必须为 `L1`，且 `Doc Mode` 必须为 `FULL_SPEC`：

- 新增 API
- 修改 API 路径、方法、鉴权、状态码、错误码
- 修改请求字段、响应字段、字段语义、字段必填性
- 修改数据库 schema
- 修改消息体契约、事件结构、WebSocket 消息结构
- 修改导入导出文件格式
- 修改权限点、角色能力边界
- 修改会影响其他系统、前端、客户端、脚本调用方的接口行为

### 规则 B：没有既有 spec，不允许直接走 L2

如果任务看起来像小改动，但相关 feature 没有可依赖的 `spec.md` 或基础规格记录，则：

- 不允许直接走 `L2`
- 至少升级为 `L1`
- `Doc Mode` 必须为 `FULL_SPEC`

### 规则 C：L3 只能用于最小安全补丁

只有在“目标是尽快恢复服务且补丁范围最小”时才能使用 `L3`。

若修复已经涉及以下任一情况，则不能继续使用 `L3`：

- 跨模块重设计
- 引入新接口或新流程
- 修改外部契约
- 较大范围重构
- 需要完整验证新业务逻辑

此时应升级为 `L2` 或 `L1`。

### 规则 D：人工指定只能上调，不能违背硬规则下调

如果开发者或用户显式指定了等级：

- 可以接受更保守、更高等级的指定
- 不能接受与强制规则冲突的降级指定

## 分类决策顺序

按以下顺序判断，不要跳步：

1. 先识别是否存在显式指定等级
2. 再判断是否命中“外部契约变更”
3. 再判断是否属于生产故障或安全紧急修复
4. 再判断是否存在既有 spec 可复用
5. 最后再判断是 `FEATURE`、`SMALL_CHANGE` 还是 `BUG_FIX`

如果信息不完整，默认选择更保守、更慢的等级。

## 技术栈识别信号

### Java / Spring Boot

以下信号优先判断为 `L1`：

- 新增或修改 `Controller` 接口
- 新增或修改请求/响应 DTO、VO、Query、Form
- 修改 `Feign`、OpenAPI、Swagger 暴露的接口结构
- 修改数据库表、字段、索引、约束、迁移脚本
- 修改 WebSocket 消息体、OnlyOffice 协议、文件导出格式
- 修改认证鉴权、角色权限、租户隔离逻辑

通常可归为 `L2`：

- 局部判空修复
- 日志补充
- 局部校验修正
- 不改变接口契约的 SQL 优化
- 不改变对外行为的内部重构

### Python

以下信号优先判断为 `L1`：

- 新增或修改 FastAPI / Flask / Django API
- 修改 Pydantic schema、Serializer、请求响应模型
- 修改 Celery / 消息队列任务的输入输出契约
- 修改数据库 migration、ORM model 结构
- 修改公共 SDK、CLI 参数协议、导出文件结构
- 修改鉴权、中间件、租户/权限边界

通常可归为 `L2`：

- 局部异常处理修复
- 参数校验 bug 修复
- 内部函数重构
- 不改变接口的性能优化
- 补测试、补日志、补监控

### 前端

以下信号优先判断为 `L1`：

- 新增页面、核心业务流程、关键路由
- 新增或修改对外接口契约依赖
- 修改表单字段、提交流程、用户可见业务规则
- 修改状态流转、权限可见性、支付/提交/审核等关键路径
- 修改公共组件 API，影响多个页面使用方式
- 修改导入导出格式、文件协议、实时消息结构

通常可归为 `L2`：

- 样式修复
- 局部交互修复
- 文案修正
- 不改变业务含义的组件内部重构
- 非契约型埋点、日志、性能微调

## Level 与 Change Type 的推荐映射

- `L1` 通常对应 `FEATURE`
- `L2` 通常对应 `SMALL_CHANGE`
- `L2` 若是纯缺陷修复，可对应 `BUG_FIX`
- `L3` 对应 `BUG_FIX`

注意：

- `Change Type` 不能反向决定 `Final Level`
- 即使代码量很小，只要命中外部契约变更，也必须是 `L1`

## 文档模式判定规则

- 若 `Final Level = L1`，则 `Doc Mode = FULL_SPEC`
- 若 `Final Level = L2`，则 `Doc Mode = CHANGE_RECORD`
- 若 `Final Level = L3`，则 `Doc Mode = HOTFIX_RECORD`

补充要求：

- `L2` 必须依附已有 feature spec
- 若无 feature spec，则升级为 `L1 + FULL_SPEC`
- `L3` 在服务恢复后，仍需补回规格历史
- 所有需求文档都必须写入 `spec/features/<feature-name>/`，禁止直接写到 `spec/` 根目录

## Human Gate 规则

- `L1`: 在 `Plan`、`Spec`、`Tasks` 后需要确认
- `L2`: 在 `Tasks` 后需要确认
- `L3`: 在 `Patch Proposal` 后需要确认

补充强制要求：

- `L1` 必须先创建 `spec/features/<feature-name>/`，并保存 `plan.md`、`spec.md`、`tasks.md`
- `L2` 必须先在 `spec/features/<feature-name>/smallchange/` 下生成并保存 `<date>-<change-name>.md`
- `L3` 必须先在 `spec/features/<feature-name>/hotfix/` 下生成并保存 `<date>-<hotfix-name>.md`
- 创建 feature 目录时，同步建立 `smallchange/` 与 `hotfix/` 子目录
- 所有级别都必须等待用户确认，并由用户手动明确继续后，才能进入编码或执行推进实现的命令

## Reason 要求

`Reason` 必须明确说明：

- 为什么是这个 `Final Level`
- 是否命中了外部契约变更
- 是否存在既有 spec
- 为什么选择该 `Doc Mode`

## Scope Signals 要求

`Scope Signals` 必须列出判断依据，使用中文短句并用分号分隔。

示例：

```text
Scope Signals: 新增教师培训报名接口；新增请求 DTO 和响应 VO；前端调用方式将发生变化；属于外部契约新增
```

## Escalation Note 要求

- 若无升级风险，写 `None`
- 若存在可能升级条件，明确写出触发条件

## 最终执行要求

严格按输出格式返回，不要添加额外章节，不要输出 Markdown 列表，不要省略字段。
