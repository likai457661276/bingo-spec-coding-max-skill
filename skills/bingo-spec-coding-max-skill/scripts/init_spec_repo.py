#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
import sys
from typing import Any

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python 3.11+ should provide tomllib
    tomllib = None


DEFAULT_PROJECT_SUMMARY = "Fill in project goals and architecture summary."
DEFAULT_STACK = "Unknown stack. Fill in runtime, framework, database, and deployment details."
DEFAULT_TEST_COMMAND = "No common test command detected."
DEFAULT_RUN_COMMAND = "No common run command detected."
DEFAULT_SOURCE_ROOTS = "No common source roots detected."
DEFAULT_LANGUAGE = "zh"
SUPPORTED_LANGUAGES = ("zh", "en")
COMMON_ROOT_CANDIDATES = (
    "src",
    "src/main",
    "src/main/java",
    "src/main/resources",
    "src/test",
    "src/test/java",
    "app",
    "pages",
    "components",
    "public",
    "tests",
    "backend",
    "frontend",
    "packages",
    "services",
    "lib",
)
COMMON_CONTAINER_DIRS = ("backend", "frontend", "packages", "services", "apps")
PLAYWRIGHT_CONFIGS = (
    "playwright.config.js",
    "playwright.config.cjs",
    "playwright.config.mjs",
    "playwright.config.ts",
)
CYPRESS_CONFIGS = (
    "cypress.config.js",
    "cypress.config.cjs",
    "cypress.config.mjs",
    "cypress.config.ts",
)
ESLINT_CONFIGS = (
    ".eslintrc",
    ".eslintrc.js",
    ".eslintrc.cjs",
    ".eslintrc.json",
    ".eslintrc.yaml",
    ".eslintrc.yml",
    "eslint.config.js",
    "eslint.config.cjs",
    "eslint.config.mjs",
    "eslint.config.ts",
)
PRETTIER_CONFIGS = (
    ".prettierrc",
    ".prettierrc.js",
    ".prettierrc.cjs",
    ".prettierrc.json",
    ".prettierrc.yaml",
    ".prettierrc.yml",
    "prettier.config.js",
    "prettier.config.cjs",
    "prettier.config.mjs",
    "prettier.config.ts",
)
STYLELINT_CONFIGS = (
    ".stylelintrc",
    ".stylelintrc.js",
    ".stylelintrc.cjs",
    ".stylelintrc.json",
    ".stylelintrc.yaml",
    ".stylelintrc.yml",
    "stylelint.config.js",
    "stylelint.config.cjs",
    "stylelint.config.mjs",
)
TASKFILE_CONFIGS = ("Taskfile.yml", "Taskfile.yaml")


DOC_TO_TARGET = {
    "spec_bootstrap_prompt_v6.md": "spec/prompts/spec_bootstrap_prompt_v6.md",
    "change_classifier.prompt.md": "spec/prompts/change_classifier.prompt.md",
    "generate_question_answer.prompt.md": "spec/prompts/generate_question_answer.prompt.md",
    "generate_feature_tasks.prompt.md": "spec/prompts/generate_feature_tasks.prompt.md",
    "generate_change_tasks.prompt.md": "spec/prompts/generate_change_tasks.prompt.md",
    "usage_examples.md": "spec/usage/usage_examples.md",
}


GENERATED_FILES_BY_LANGUAGE = {
    "zh": {
        "AGENTS.md": """Always respond in Chinese-simplified

# Project Agent Policy

## Repository Snapshot

- Project Summary: {{PROJECT_SUMMARY}}
- Detected Stack: {{DETECTED_STACK}}
- Suggested Test Command: {{TEST_COMMAND}}
- Suggested Source Roots: {{SOURCE_ROOTS}}
- Spec Language: Chinese

## State Model

INIT -> ANALYSIS -> EXECUTION -> COMPLETED | FAILED | ABORTED

## Classification First

在进入规划、任务拆分或编码前，先完成三轴分级，并严格输出：

Requested Level: AUTO | L0 | L1 | L2 | L3
Final Level: L0 | L1 | L2 | L3
Change Type: QUESTION | FEATURE | SMALL_CHANGE | BUG_FIX
Doc Mode: QUESTION_RECORD | FULL_SPEC | CHANGE_RECORD | HOTFIX_RECORD
Workflow: Context -> Investigation -> Answer | Context -> Plan -> Spec -> Tasks -> Code | Tasks -> Code | Patch Proposal -> Code
Human Gate:
Reason:
Scope Signals:
Escalation Note:

## Workflow Levels

默认工作流：Context -> Plan -> Spec -> Tasks -> Code

L0（Question）: Context -> Investigation -> Answer
L1（Feature）: Context -> Plan -> Spec -> Tasks -> Code
L2（Small Change）: Tasks -> Code
L3（Hotfix）: Patch Proposal -> Code

## Hard Rules

1. 若请求只是解释、分析、排查、方案比较，且未要求直接改动实现，优先归类为 `L0 + QUESTION_RECORD`。
2. 外部契约变更至少为 L1，且 Doc Mode 必须为 FULL_SPEC。
3. L2 必须依附已有 feature spec；若无 spec，升级为 L1。
4. L3 只能用于最小安全补丁；范围扩大即升级为 L2 或 L1。
5. 用户或开发者显式指定等级只能上调，不能绕过强制规则。
6. `L1` / `L2` / `L3` 都必须先生成实体 `.md` 文档并遵守对应的人类门禁；`L0` 不强制落 `QUESTION_RECORD`，分析后若已明确需要实现，可直接升级到 `L1` / `L2` / `L3` 继续推进。

## Human Gates

L0 无需额外确认：

1. 完成 `Answer` 后可直接结束
2. 若分析结论已明确需要实现，可直接升级到 `L1`、`L2` 或 `L3`

L1 需要在以下阶段后获得确认：

1. 完成 `Plan`、`Spec`、`Tasks`
2. 在 `Tasks` 后统一确认一次

L2 需要在以下阶段后获得确认：

1. Tasks

L3 需要在以下阶段后获得确认：

1. Patch Proposal

## Safe Execution Rule

未完成分级输出前，不得进入代码实现阶段，也不得执行会推进实现的命令。若后续工作进入 `L1`、`L2` 或 `L3`，仍须满足对应级别的文档门禁与人类门禁；`L0` 分析本身不要求先落文档或等待额外确认。

## Spec Entry Binding

1. `AGENTS.md` 负责请求分级、文档门禁与执行边界。
2. 完成分级输出后，必须先读取 `spec/INDEX.md`，再决定进入 `spec/questions/` 或 `spec/features/<feature-name>/`。
3. `spec/INDEX.md` 是规格树唯一导航入口；不得跳过索引直接假设文档路径。
""",
        "spec/INDEX.md": """# 规格索引

## 核心文档

1. [SPEC_CONTEXT.md](./SPEC_CONTEXT.md)
2. [SPEC_WORKFLOW.md](./SPEC_WORKFLOW.md)
3. [CHANGE_POLICY.md](./CHANGE_POLICY.md)

## Agent 入口

Agent 应从本文件进入规格树，再根据请求类型定位到 `spec/questions/` 或 `spec/features/<feature-name>/`。

## 与 AGENTS.md 的挂接

1. `AGENTS.md` 负责请求分级、Doc Mode、人类门禁与执行边界。
2. 本文件负责把 `AGENTS.md` 的分级结果映射到具体 spec 路径与文档集合。
3. Agent 在完成分级输出后，必须回到本索引，并按 `Doc Mode` 进入对应文档目录。
4. 未读取本索引前，不得开始撰写 `plan/spec/tasks/question/change/hotfix` 文档。

## Prompt 来源

1. [spec_bootstrap_prompt_v6.md](./prompts/spec_bootstrap_prompt_v6.md)
2. [change_classifier.prompt.md](./prompts/change_classifier.prompt.md)
3. [generate_question_answer.prompt.md](./prompts/generate_question_answer.prompt.md)
4. [generate_feature_tasks.prompt.md](./prompts/generate_feature_tasks.prompt.md)
5. [generate_change_tasks.prompt.md](./prompts/generate_change_tasks.prompt.md)

## 模板

1. [PLAN_TEMPLATE.md](./templates/PLAN_TEMPLATE.md)
2. [SPEC_TEMPLATE.md](./templates/SPEC_TEMPLATE.md)
3. [QUESTION_TEMPLATE.md](./templates/QUESTION_TEMPLATE.md)
4. [TASK_TEMPLATE.md](./templates/TASK_TEMPLATE.md)
5. [CHANGE_TEMPLATE.md](./templates/CHANGE_TEMPLATE.md)
6. [HOTFIX_TEMPLATE.md](./templates/HOTFIX_TEMPLATE.md)

## 使用示例

1. [usage_examples.md](./usage/usage_examples.md)
2. 特性目录：`spec/features/<feature-name>/`
3. 问题记录：`spec/questions/<date>-<topic>.md`

## 文档目录约定

1. 如需沉淀 `L0` 问题记录，保存在 `spec/questions/<date>-<topic>.md`
2. `L1` 主文档保存在 `spec/features/<feature-name>/plan.md`、`spec/features/<feature-name>/spec.md`、`spec/features/<feature-name>/tasks.md`
3. `L2` 变更记录保存在 `spec/features/<feature-name>/smallchange/<date>-<change-name>.md`
4. `L3` 热修复记录保存在 `spec/features/<feature-name>/hotfix/<date>-<hotfix-name>.md`
5. 创建 feature 目录时，同步建立 `smallchange/` 与 `hotfix/` 子目录

## 导航规则

1. 先阅读本索引。
2. 如果是问题分析，先检查 `spec/questions/` 下是否已有相关记录。
3. 如果是变更请求，再定位到相关特性目录。
4. L1 先读 `plan.md`。
5. 编写任务或代码前先读 `spec.md`。
6. 编码前读取 `tasks.md` 或变更任务说明。
""",
        "spec/SPEC_CONTEXT.md": """# SPEC_CONTEXT

## 仓库摘要

- Project: {{PROJECT_SUMMARY}}
- Stack: {{DETECTED_STACK}}
- Source roots: {{SOURCE_ROOTS}}
- Suggested test command: {{TEST_COMMAND}}

## 领域约束

- 业务约束：
- 合规/安全约束：

## 项目规则与协作约束

- CI / 自动化流程：
- 代码质量 / 格式化规则：
- 本地提交门禁：

## 非功能约束

- 性能：
- 可靠性：
- 可观测性：

## 假设与未知项

- 待确认问题：
- 待决策事项：
- 当前仓库上下文中的已知缺口：
""",
        "spec/SPEC_WORKFLOW.md": """# SPEC_WORKFLOW

## 全局流程

Context -> Plan -> Spec -> Tasks -> Code

## 分级决策顺序

1. 先识别该请求是否只是问题、分析、排查、解释或方案比较。
2. 再识别 `Requested Level` 是否被显式指定。
3. 再判断是否命中外部契约变更。
4. 再判断是否属于生产故障或安全紧急修复。
5. 再判断是否存在可复用的既有 feature spec。
6. 最后确定 `Change Type` 与 `Doc Mode`。

## 变更分级

### L0 Question

- Workflow: `Context -> Investigation -> Answer`
- Doc Mode: `QUESTION_RECORD`
- 适用：问题澄清、代码阅读结论、原因分析、方案比较、只读调研、是否值得做需求的前置判断
- 执行要求：可选在 `spec/questions/` 下生成 `<date>-<topic>.md` 记录分析结论；若分析后已明确需要实现，可直接升级到 `L1/L2/L3` 并继续推进，无需等待额外确认

### L1 Feature Change

- Workflow: `Context -> Plan -> Spec -> Tasks -> Code`
- Doc Mode: `FULL_SPEC`
- 适用：新增能力、外部契约变更、跨模块设计变化、没有既有 spec 的行为变更
- 强制门禁：必须先创建 `spec/features/<feature-name>/`，并在其中生成 `plan.md`、`spec.md`、`tasks.md`；同时建立 `smallchange/` 与 `hotfix/` 子目录，等待用户确认后才可进入编码

### L2 Small Change

- Workflow: `Tasks -> Code`
- Doc Mode: `CHANGE_RECORD`
- 前提：必须已有相关 feature spec；若无 spec，不得直接走 L2
- 强制门禁：必须先在 `spec/features/<feature-name>/smallchange/` 下生成实体 `<date>-<change-name>.md` 变更记录并等待用户确认，之后仅在用户手动明确继续时进入编码

### L3 Hotfix

- Workflow: `Patch Proposal -> Code`
- Doc Mode: `HOTFIX_RECORD`
- 前提：目标是尽快恢复服务，且补丁范围必须保持最小安全补丁
- 强制门禁：必须先在 `spec/features/<feature-name>/hotfix/` 下生成实体 `<date>-<hotfix-name>.md` 补丁方案并等待用户确认，之后仅在用户手动明确继续时进入编码

## 强制升级规则

- 若涉及 API、数据库 schema、消息体、文件格式、权限边界等外部契约变化，必须升级为 `L1 + FULL_SPEC`。
- 若相关 feature 不存在 `spec.md` 或基础规格记录，不得直接走 L2，必须升级为 `L1 + FULL_SPEC`。
- 若 hotfix 已超出最小安全补丁，必须升级为 `L2` 或 `L1`。
- 若问题分析过程中出现明确实现请求、接口调整或行为变更，必须从 `L0` 升级到 `L1/L2/L3`。
- 若实现改变了既有行为，必须同步回写规格文档。

## Human Gate Rules

- `L0`: none; 完成 `Answer` 后可直接结束，或直接升级到 `L1`、`L2`、`L3`
- `L1`: 完成 `Plan`、`Spec`、`Tasks` 后，仅在 `Tasks` 后确认一次
- `L2`: after `Tasks`
- `L3`: after `Patch Proposal`

## 文档先行规则

- `L0`: 可选落地 `spec/questions/<date>-<topic>.md`，但这不是继续实现的前置条件
- `L1`: 先创建 `spec/features/<feature-name>/`，再落地 `plan.md`、`spec.md`、`tasks.md`
- `L2`: 先确认相关 feature 目录存在，再落地 `spec/features/<feature-name>/smallchange/<date>-<change-name>.md`
- `L3`: 先确认相关 feature 目录存在，再落地 `spec/features/<feature-name>/hotfix/<date>-<hotfix-name>.md`
- 仅 `L1` / `L2` / `L3` 需要在文档落地并获得用户确认后，由用户手动明确继续，才可进入代码实现或执行推进实现的命令

## Prompt 路由

- 分级判断：`spec/prompts/change_classifier.prompt.md`
- L0 答复生成：`spec/prompts/generate_question_answer.prompt.md`
- L1 任务生成：`spec/prompts/generate_feature_tasks.prompt.md`
- L2 任务生成：`spec/prompts/generate_change_tasks.prompt.md`
""",
        "spec/CHANGE_POLICY.md": """# CHANGE_POLICY

## 分类三轴

1. Workflow Level：`L0 | L1 | L2 | L3`
2. Change Type：`QUESTION | FEATURE | SMALL_CHANGE | BUG_FIX`
3. Doc Mode：`QUESTION_RECORD | FULL_SPEC | CHANGE_RECORD | HOTFIX_RECORD`

## L0 问题分析约束

1. 仅适用于问题澄清、原因分析、代码阅读、只读调研、方案比较和需求前置判断。
2. 如需保留分析记录，可使用 `QUESTION_RECORD` 写入 `spec/questions/<date>-<topic>.md`，但这不是实现前置条件。
3. 若分析过程中已经明确进入实现设计、接口调整或行为变更，应直接升级到 `L1`、`L2` 或 `L3` 并继续推进。

## 外部契约变更

命中以下任一信号，必须为 `L1 + FULL_SPEC`：

1. API 路径、方法、鉴权、状态码、错误码变化
2. 请求字段、响应字段、字段语义、字段必填性变化
3. 数据库 schema、迁移、索引、约束变化
4. 消息体契约、事件结构、WebSocket 消息或导入导出文件格式变化
5. 权限点、角色能力边界变化
6. 任何会影响其他系统、前端、客户端或脚本调用方的接口行为变化

## L2 约束

1. 必须已有可复用的 feature `spec.md` 或基础规格记录。
2. 若无既有 spec，不得直接走 `L2`，必须升级为 `L1 + FULL_SPEC`。
3. 文档沉淀使用 `CHANGE_RECORD`，写入 `spec/features/<feature-name>/smallchange/` 下的历史记录。

## L3 约束

1. 仅用于生产故障、安全问题、线上关键失败的最小安全补丁。
2. 若修复涉及跨模块重设计、新接口、新流程、大范围重构或完整新逻辑验证，必须升级为 `L2` 或 `L1`。
3. 稳定后必须补回规格历史，文档模式为 `HOTFIX_RECORD`，记录位于 `spec/features/<feature-name>/hotfix/`。

## 覆盖规则

1. 用户或开发者显式指定等级时，只能上调，不能违反强制规则下调。
2. 信息不完整时，默认选择更保守、更慢的等级。

## 文档执行门禁

1. `L0` 可按需在 `spec/questions/` 下生成并保存实体 `<date>-<topic>.md`，但不作为实现门禁。
2. `L1` 必须先创建 `spec/features/<feature-name>/`，并在其中保存 `plan.md`、`spec.md`、`tasks.md`。
3. `L2` 必须先在 `spec/features/<feature-name>/smallchange/` 下生成并保存实体 `<date>-<change-name>.md`。
4. `L3` 必须先在 `spec/features/<feature-name>/hotfix/` 下生成并保存实体 `<date>-<hotfix-name>.md`。
5. `L1` / `L2` / `L3` 的文档未落地前，不得编码，也不得执行会推进实现的命令。
6. `L1` / `L2` / `L3` 文档落地后，若后续要推进实现，仍必须等待用户确认，并由用户手动明确继续。
""",
        "spec/templates/QUESTION_TEMPLATE.md": """# Question: <topic>

## Classification

Requested Level: AUTO | L0 | L1 | L2 | L3
Final Level: L0
Change Type: QUESTION
Doc Mode: QUESTION_RECORD
Workflow: Context -> Investigation -> Answer
Human Gate: 无；如分析后已明确需要实现，可直接升级到 `L1`、`L2` 或 `L3` 并继续推进

## Preconditions

- 当前目标是澄清问题、分析现状、比较方案或给出建议
- 尚未请求直接修改实现或推进实现的命令
- 若分析结论转为明确变更需求，升级为 `L1`、`L2` 或 `L3`

## 可选记录

- 本模板仅在需要沉淀分析记录时使用，不是进入实现的前置门禁
- 如需保存，写入 `spec/questions/<date>-<topic>.md`

## 问题陈述

描述当前问题、疑问或需要判断的事项。

## 已知上下文

- 相关模块：
- 已知事实：
- 未知点：

## Investigation

1. ...
2. ...
3. ...

## Answer

- 结论：
- 依据：
- 建议下一步：

## Escalation Triggers

- 哪些信号会让该问题升级为 L1 / L2 / L3：
""",
        "spec/templates/PLAN_TEMPLATE.md": """# Plan: <feature-name>

## Manual Execution Gate

- 本文档是实体门禁文档之一，必须先保存为 `spec/features/<feature-name>/plan.md`
- 创建 feature 目录时，同时建立 `spec/features/<feature-name>/smallchange/` 与 `spec/features/<feature-name>/hotfix/`
- 用户确认并手动明确继续前，不得进入编码或执行推进实现的命令

## 问题陈述

描述用户问题或业务需求。

## 目标

- ...

## 范围边界

In scope:
- ...

Out of scope:
- ...

## 影响系统

- Components:
- Interfaces:
- Data or storage impact:

## 风险与假设

- Risks:
- Assumptions:
""",
        "spec/templates/SPEC_TEMPLATE.md": """# Feature Spec: <feature-name>

## Manual Execution Gate

- 本文档是实体门禁文档之一，必须先保存为 `spec/features/<feature-name>/spec.md`
- 用户确认并手动明确继续前，不得进入编码或执行推进实现的命令

## 背景

描述用户问题和业务目标。

## 范围

In scope:
- ...

Out of scope:
- ...

## 设计

- Components:
- Data model/API:
- Risks:

## 验收标准

1. ...
2. ...
3. ...
""",
        "spec/templates/TASK_TEMPLATE.md": """# Tasks: <feature-or-change-name>

## Classification

Final Level: L1
Change Type: FEATURE
Doc Mode: FULL_SPEC

## Manual Execution Gate

- 本文档是实体门禁文档之一，必须先保存为 `spec/features/<feature-name>/tasks.md`
- 用户确认并手动明确继续前，不得进入编码或执行推进实现的命令

## 背景

描述本组任务要解决的问题。

## Tasks

1. ...
2. ...
3. ...

## Verification

1. Tests:
2. Manual checks:
3. Rollback considerations:
""",
        "spec/templates/CHANGE_TEMPLATE.md": """# Change: <change-name>

## Classification

Requested Level: AUTO | L0 | L1 | L2 | L3
Final Level: L2
Change Type: SMALL_CHANGE | BUG_FIX
Doc Mode: CHANGE_RECORD
Workflow: Tasks -> Code
Human Gate: 先生成并保存 `spec/features/<feature-name>/smallchange/<date>-<change-name>.md`，待用户确认并手动明确继续后才能进入代码实现

## Preconditions

- 相关 feature `spec.md` 已存在并已阅读
- 若不存在既有 feature spec，升级为 `L1 + FULL_SPEC`
- 必须先确保 `spec/features/<feature-name>/smallchange/` 存在，并将本方案保存为实体 `<date>-<change-name>.md`
- 用户确认并手动明确继续前，不得进入编码或执行推进实现的命令

## 背景

描述问题以及为什么该变更仍属于小改动。

## 范围

In scope:
- ...

Out of scope:
- ...

## Tasks

1. ...
2. ...
3. ...

## Verification

1. Automated tests:
2. Manual checks:
3. Regression focus:

## Rollback Notes

- ...
""",
        "spec/templates/HOTFIX_TEMPLATE.md": """# Hotfix: <incident-or-change-name>

## Classification

Requested Level: AUTO | L0 | L1 | L2 | L3
Final Level: L3
Change Type: BUG_FIX
Doc Mode: HOTFIX_RECORD
Workflow: Patch Proposal -> Code
Human Gate: 先生成并保存 `spec/features/<feature-name>/hotfix/<date>-<hotfix-name>.md`，待用户确认并手动明确继续后才能进入代码实现

## Preconditions

- 当前目标是尽快恢复服务
- 补丁范围保持为最小安全补丁
- 若范围扩大，升级为 `L2` 或 `L1`
- 必须先确保 `spec/features/<feature-name>/hotfix/` 存在，并将本方案保存为实体 `<date>-<hotfix-name>.md`
- 用户确认并手动明确继续前，不得进入编码或执行推进实现的命令

## 事故背景

描述生产问题或紧急故障。

## 最小补丁方案

1. ...
2. ...
3. ...

## Verification

1. Reproduce the issue:
2. Confirm the service is restored:
3. Review logs or alerts:

## Rollback Or Fallback

- ...
""",
        "spec/features/.gitkeep": "",
        "spec/questions/.gitkeep": "",
    },
    "en": {
        "AGENTS.md": """Always respond in English

# Project Agent Policy

## Repository Snapshot

- Project Summary: {{PROJECT_SUMMARY}}
- Detected Stack: {{DETECTED_STACK}}
- Suggested Test Command: {{TEST_COMMAND}}
- Suggested Source Roots: {{SOURCE_ROOTS}}
- Spec Language: English

## State Model

INIT -> ANALYSIS -> EXECUTION -> COMPLETED | FAILED | ABORTED

## Classification First

Before planning, task generation, or coding, classify the request on three axes and output exactly:

Requested Level: AUTO | L0 | L1 | L2 | L3
Final Level: L0 | L1 | L2 | L3
Change Type: QUESTION | FEATURE | SMALL_CHANGE | BUG_FIX
Doc Mode: QUESTION_RECORD | FULL_SPEC | CHANGE_RECORD | HOTFIX_RECORD
Workflow: Context -> Investigation -> Answer | Context -> Plan -> Spec -> Tasks -> Code | Tasks -> Code | Patch Proposal -> Code
Human Gate:
Reason:
Scope Signals:
Escalation Note:

## Workflow Levels

Default workflow: Context -> Plan -> Spec -> Tasks -> Code

L0 (Question): Context -> Investigation -> Answer
L1 (Feature): Context -> Plan -> Spec -> Tasks -> Code
L2 (Small Change): Tasks -> Code
L3 (Hotfix): Patch Proposal -> Code

## Hard Rules

1. If the request is explanation, analysis, investigation, or option comparison without a direct implementation ask, prefer `L0 + QUESTION_RECORD`.
2. External contract changes must be at least `L1`, and `Doc Mode` must be `FULL_SPEC`.
3. `L2` requires an existing feature spec; if none exists, escalate to `L1`.
4. `L3` is only for the smallest safe patch; if scope expands, escalate to `L2` or `L1`.
5. User- or developer-requested levels may raise conservatism, but may not bypass hard rules.
6. `L1` / `L2` / `L3` must produce concrete `.md` documents first and obey their human gates; `L0` does not require a `QUESTION_RECORD`, and analysis may escalate directly into `L1`, `L2`, or `L3` when implementation is clearly needed.

## Human Gates

L0 requires no extra approval:

1. `Answer` may end the work directly
2. If implementation is clearly needed after analysis, escalate directly to `L1`, `L2`, or `L3`

L1 requires approval after:

1. `Plan`, `Spec`, and `Tasks` are all complete
2. one confirmation after `Tasks`

L2 requires approval after:

1. Tasks

L3 requires approval after:

1. Patch Proposal

## Safe Execution Rule

Do not implement code, or run implementation-driving commands, before classification is complete. If the work enters `L1`, `L2`, or `L3`, the required concrete `.md` documents and human gates still apply. `L0` analysis itself does not require a document or an extra human checkpoint first.

## Spec Entry Binding

1. `AGENTS.md` governs request classification, document gates, and execution boundaries.
2. After classification output is complete, the agent must read `spec/INDEX.md` before choosing either `spec/questions/` or `spec/features/<feature-name>/`.
3. `spec/INDEX.md` is the single navigation entry to the spec tree; do not skip it and assume a document path directly.
""",
        "spec/INDEX.md": """# Spec Index

## Core

1. [SPEC_CONTEXT.md](./SPEC_CONTEXT.md)
2. [SPEC_WORKFLOW.md](./SPEC_WORKFLOW.md)
3. [CHANGE_POLICY.md](./CHANGE_POLICY.md)

## Agent Entry

Agents should enter the spec tree from this file, then route either to `spec/questions/` or the relevant feature under `spec/features/<feature-name>/`.

## Binding To AGENTS.md

1. `AGENTS.md` defines request classification, Doc Mode, human gates, and execution boundaries.
2. This file maps the classification result from `AGENTS.md` to the concrete spec path and required document set.
3. After finishing classification output, the agent must return to this index and enter the correct document path based on `Doc Mode`.
4. Do not start writing `plan/spec/tasks/question/change/hotfix` documents before reading this index.

## Prompt Sources

1. [spec_bootstrap_prompt_v6.md](./prompts/spec_bootstrap_prompt_v6.md)
2. [change_classifier.prompt.md](./prompts/change_classifier.prompt.md)
3. [generate_question_answer.prompt.md](./prompts/generate_question_answer.prompt.md)
4. [generate_feature_tasks.prompt.md](./prompts/generate_feature_tasks.prompt.md)
5. [generate_change_tasks.prompt.md](./prompts/generate_change_tasks.prompt.md)

## Templates

1. [PLAN_TEMPLATE.md](./templates/PLAN_TEMPLATE.md)
2. [SPEC_TEMPLATE.md](./templates/SPEC_TEMPLATE.md)
3. [QUESTION_TEMPLATE.md](./templates/QUESTION_TEMPLATE.md)
4. [TASK_TEMPLATE.md](./templates/TASK_TEMPLATE.md)
5. [CHANGE_TEMPLATE.md](./templates/CHANGE_TEMPLATE.md)
6. [HOTFIX_TEMPLATE.md](./templates/HOTFIX_TEMPLATE.md)

## Usage

1. [usage_examples.md](./usage/usage_examples.md)
2. Features path: `spec/features/<feature-name>/`
3. Question records: `spec/questions/<date>-<topic>.md`

## Document Layout

1. Optional `L0` question records live in `spec/questions/<date>-<topic>.md`
2. `L1` primary docs live in `spec/features/<feature-name>/plan.md`, `spec/features/<feature-name>/spec.md`, and `spec/features/<feature-name>/tasks.md`
3. `L2` change records live in `spec/features/<feature-name>/smallchange/<date>-<change-name>.md`
4. `L3` hotfix records live in `spec/features/<feature-name>/hotfix/<date>-<hotfix-name>.md`
5. When a feature folder is created, create `smallchange/` and `hotfix/` under it as well

## Navigation

1. Read this index first.
2. If the request is analysis-only, check `spec/questions/` first.
3. Otherwise locate the relevant feature folder.
4. Read `plan.md` for L1 changes.
5. Read `spec.md` before generating tasks or code.
6. Read `tasks.md` or change-level task notes before coding.
""",
        "spec/SPEC_CONTEXT.md": """# SPEC_CONTEXT

## Repository Summary

- Project: {{PROJECT_SUMMARY}}
- Stack: {{DETECTED_STACK}}
- Source roots: {{SOURCE_ROOTS}}
- Suggested test command: {{TEST_COMMAND}}

## Domain Constraints

- Business constraints:
- Compliance/security constraints:

## Project Rules And Collaboration Constraints

- CI and automation flows:
- Code-quality and formatting rules:
- Local commit gates:

## Non-functional Constraints

- Performance:
- Reliability:
- Observability:

## Assumptions And Unknowns

- Open questions:
- Pending decisions:
- Known gaps in current repository context:
""",
        "spec/SPEC_WORKFLOW.md": """# SPEC_WORKFLOW

## Global Flow

Context -> Plan -> Spec -> Tasks -> Code

## Classification Order

1. Check whether the request is only a question, investigation, explanation, or option comparison.
2. Check whether `Requested Level` was explicitly specified.
3. Check whether the request changes an external contract.
4. Check whether the work is a production or security hotfix.
5. Check whether an existing feature spec can be reused.
6. Then finalize `Change Type` and `Doc Mode`.

## Change Levels

### L0 Question

- Workflow: `Context -> Investigation -> Answer`
- Doc Mode: `QUESTION_RECORD`
- Use for: clarification questions, code-reading conclusions, root-cause analysis, option comparison, read-only investigation, or deciding whether a future change is needed
- Execution rule: optionally save a concrete record at `spec/questions/<date>-<topic>.md`; if analysis makes implementation clearly necessary, escalate directly to `L1`, `L2`, or `L3` and continue without an extra confirmation stop

### L1 Feature Change

- Workflow: `Context -> Plan -> Spec -> Tasks -> Code`
- Doc Mode: `FULL_SPEC`
- Use for: new capabilities, external contract changes, cross-module design work, or behavior changes without a reusable existing spec
- Hard gate: create `spec/features/<feature-name>/` first, then generate `plan.md`, `spec.md`, and `tasks.md` there; also create `smallchange/` and `hotfix/` before coding

### L2 Small Change

- Workflow: `Tasks -> Code`
- Doc Mode: `CHANGE_RECORD`
- Requirement: an existing related feature spec must already exist; otherwise escalate to `L1`
- Hard gate: generate a concrete change record at `spec/features/<feature-name>/smallchange/<date>-<change-name>.md` first; wait for user review, and continue to code only after a manual go-ahead

### L3 Hotfix

- Workflow: `Patch Proposal -> Code`
- Doc Mode: `HOTFIX_RECORD`
- Requirement: the goal is rapid restoration and the patch must stay minimal
- Hard gate: generate a concrete hotfix record at `spec/features/<feature-name>/hotfix/<date>-<hotfix-name>.md` first; wait for user review, and continue to code only after a manual go-ahead

## Hard Escalation Rules

- If the change affects APIs, database schema, message contracts, file formats, or permission boundaries, it must be `L1 + FULL_SPEC`.
- If no existing `spec.md` or equivalent baseline spec exists for the feature, do not use `L2`; escalate to `L1 + FULL_SPEC`.
- If a hotfix grows beyond the smallest safe patch, escalate to `L2` or `L1`.
- If an investigation request turns into a concrete implementation ask or behavior change, escalate from `L0` to `L1`, `L2`, or `L3`.
- If implementation changes behavior, update spec artifacts accordingly.

## Human Gate Rules

- `L0`: none; `Answer` may finish the work, or immediately escalate to `L1`, `L2`, or `L3`
- `L1`: complete `Plan`, `Spec`, and `Tasks`, then approve once after `Tasks`
- `L2`: approval after `Tasks`
- `L3`: approval after `Patch Proposal`

## Document-First Rule

- `L0`: optionally save `spec/questions/<date>-<topic>.md`, but this is not a prerequisite for implementation
- `L1`: create `spec/features/<feature-name>/` first, then save `plan.md`, `spec.md`, and `tasks.md` there
- `L2`: confirm the feature folder exists, then save `spec/features/<feature-name>/smallchange/<date>-<change-name>.md`
- `L3`: confirm the feature folder exists, then save `spec/features/<feature-name>/hotfix/<date>-<hotfix-name>.md`
- For `L1`, `L2`, and `L3`, code work and implementation-driving commands must wait until the document exists, the user reviews it, and the user manually tells the agent to continue

## Prompt Routing

- Level classification: `spec/prompts/change_classifier.prompt.md`
- L0 answer generation: `spec/prompts/generate_question_answer.prompt.md`
- L1 tasks: `spec/prompts/generate_feature_tasks.prompt.md`
- L2 tasks: `spec/prompts/generate_change_tasks.prompt.md`
""",
        "spec/CHANGE_POLICY.md": """# CHANGE_POLICY

## Classification Axes

1. Workflow Level: `L0 | L1 | L2 | L3`
2. Change Type: `QUESTION | FEATURE | SMALL_CHANGE | BUG_FIX`
3. Doc Mode: `QUESTION_RECORD | FULL_SPEC | CHANGE_RECORD | HOTFIX_RECORD`

## L0 Constraints

1. Use `L0` only for clarification, analysis, code reading, option comparison, read-only investigation, or deciding whether a change is needed.
2. When a durable analysis record is useful, use `QUESTION_RECORD` under `spec/questions/<date>-<topic>.md`, but it is optional.
3. If the investigation becomes concrete implementation design, behavior change, or contract change, escalate to `L1`, `L2`, or `L3` and continue.

## External Contract Changes

Any of the following must be classified as `L1 + FULL_SPEC`:

1. API path, method, auth, status code, or error code changes
2. Request or response field changes, semantic changes, or requiredness changes
3. Database schema, migration, index, or constraint changes
4. Message contracts, event payloads, WebSocket payloads, or import/export format changes
5. Permission point or role-boundary changes
6. Any caller-visible behavior change that affects other systems, frontend clients, mobile apps, or scripts

## L2 Constraints

1. A reusable feature `spec.md` or equivalent baseline spec must already exist.
2. If no baseline spec exists, do not use `L2`; escalate to `L1 + FULL_SPEC`.
3. Documentation uses `CHANGE_RECORD` under `spec/features/<feature-name>/smallchange/`.

## L3 Constraints

1. Only use `L3` for the smallest safe patch to a production incident, security issue, or critical runtime failure.
2. If the fix requires cross-module redesign, a new interface, a new flow, a broad refactor, or full validation of new logic, escalate to `L2` or `L1`.
3. After stabilization, backfill the spec history with `HOTFIX_RECORD` under `spec/features/<feature-name>/hotfix/`.

## Override Rule

1. An explicitly requested level may raise conservatism, but may not lower the level against hard rules.
2. When information is incomplete, choose the more conservative and slower level.

## Document Execution Gate

1. `L0` may optionally generate and save a concrete `<date>-<topic>.md` under `spec/questions/`, but this is not an implementation gate.
2. `L1` must first create `spec/features/<feature-name>/`, then save `plan.md`, `spec.md`, and `tasks.md` inside it.
3. `L2` must first generate and save a concrete `<date>-<change-name>.md` under `spec/features/<feature-name>/smallchange/`.
4. `L3` must first generate and save a concrete `<date>-<hotfix-name>.md` under `spec/features/<feature-name>/hotfix/`.
5. Before `L1`, `L2`, or `L3` documents exist, do not code and do not run implementation-driving commands.
6. After `L1`, `L2`, or `L3` documents exist, still wait for user confirmation and a manual go-ahead if the work will continue into implementation.
""",
        "spec/templates/QUESTION_TEMPLATE.md": """# Question: <topic>

## Classification

Requested Level: AUTO | L0 | L1 | L2 | L3
Final Level: L0
Change Type: QUESTION
Doc Mode: QUESTION_RECORD
Workflow: Context -> Investigation -> Answer
Human Gate: None; if implementation is clearly needed after analysis, escalate directly to `L1`, `L2`, or `L3` and continue

## Preconditions

- The current goal is clarification, analysis, investigation, or recommendation
- No direct implementation change has been requested yet
- If the result becomes a concrete change request, escalate to `L1`, `L2`, or `L3`

## Optional Record

- Use this template only when a durable analysis record is worth keeping; it is not a prerequisite for implementation
- If saved, write it to `spec/questions/<date>-<topic>.md`

## Question

Describe the question, uncertainty, or decision to make.

## Known Context

- Relevant modules:
- Known facts:
- Unknowns:

## Investigation

1. ...
2. ...
3. ...

## Answer

- Conclusion:
- Evidence:
- Recommended next step:

## Escalation Triggers

- Signals that should upgrade this record to L1 / L2 / L3:
""",
        "spec/templates/PLAN_TEMPLATE.md": """# Plan: <feature-name>

## Manual Execution Gate

- This is one of the concrete gate documents and must first be saved as `spec/features/<feature-name>/plan.md`
- When the feature folder is created, also create `spec/features/<feature-name>/smallchange/` and `spec/features/<feature-name>/hotfix/`
- Do not start coding or run implementation-driving commands before user confirmation and a manual go-ahead

## Problem Statement

Describe the user problem or business need.

## Goals

- ...

## Scope Boundaries

In scope:
- ...

Out of scope:
- ...

## Affected Systems

- Components:
- Interfaces:
- Data or storage impact:

## Risks And Assumptions

- Risks:
- Assumptions:
""",
        "spec/templates/SPEC_TEMPLATE.md": """# Feature Spec: <feature-name>

## Manual Execution Gate

- This is one of the concrete gate documents and must first be saved as `spec/features/<feature-name>/spec.md`
- Do not start coding or run implementation-driving commands before user confirmation and a manual go-ahead

## Background

Describe user problem and business objective.

## Scope

In scope:
- ...

Out of scope:
- ...

## Design

- Components:
- Data model/API:
- Risks:

## Acceptance Criteria

1. ...
2. ...
3. ...
""",
        "spec/templates/TASK_TEMPLATE.md": """# Tasks: <feature-or-change-name>

## Classification

Final Level: L1
Change Type: FEATURE
Doc Mode: FULL_SPEC

## Manual Execution Gate

- This is one of the concrete gate documents and must first be saved as `spec/features/<feature-name>/tasks.md`
- Do not start coding or run implementation-driving commands before user confirmation and a manual go-ahead

## Context

Describe what this task set solves.

## Tasks

1. ...
2. ...
3. ...

## Verification

1. Tests:
2. Manual checks:
3. Rollback considerations:
""",
        "spec/templates/CHANGE_TEMPLATE.md": """# Change: <change-name>

## Classification

Requested Level: AUTO | L0 | L1 | L2 | L3
Final Level: L2
Change Type: SMALL_CHANGE | BUG_FIX
Doc Mode: CHANGE_RECORD
Workflow: Tasks -> Code
Human Gate: Save `spec/features/<feature-name>/smallchange/<date>-<change-name>.md` first, then wait for user confirmation and a manual go-ahead before coding

## Preconditions

- Related feature `spec.md` exists and has been read
- If no existing feature spec exists, escalate to `L1 + FULL_SPEC`
- Ensure `spec/features/<feature-name>/smallchange/` exists, then save this plan as a concrete `<date>-<change-name>.md`
- Do not start coding or run implementation-driving commands before user confirmation and a manual go-ahead

## Context

Describe the problem and why this remains a small change.

## Scope

In scope:
- ...

Out of scope:
- ...

## Tasks

1. ...
2. ...
3. ...

## Verification

1. Automated tests:
2. Manual checks:
3. Regression focus:

## Rollback Notes

- ...
""",
        "spec/templates/HOTFIX_TEMPLATE.md": """# Hotfix: <incident-or-change-name>

## Classification

Requested Level: AUTO | L0 | L1 | L2 | L3
Final Level: L3
Change Type: BUG_FIX
Doc Mode: HOTFIX_RECORD
Workflow: Patch Proposal -> Code
Human Gate: Save `spec/features/<feature-name>/hotfix/<date>-<hotfix-name>.md` first, then wait for user confirmation and a manual go-ahead before coding

## Preconditions

- The goal is rapid service restoration
- The patch remains the smallest safe patch
- If scope expands, escalate to `L2` or `L1`
- Ensure `spec/features/<feature-name>/hotfix/` exists, then save this proposal as a concrete `<date>-<hotfix-name>.md`
- Do not start coding or run implementation-driving commands before user confirmation and a manual go-ahead

## Incident Context

Describe the production issue or urgent failure.

## Proposed Minimal Patch

1. ...
2. ...
3. ...

## Verification

1. Reproduce the issue:
2. Confirm the service is restored:
3. Review logs or alerts:

## Rollback Or Fallback

- ...
""",
        "spec/features/.gitkeep": "",
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Initialize repository for spec-driven workflow."
    )
    parser.add_argument(
        "--project-root",
        default=".",
        help="Target project root directory (default: current directory).",
    )
    parser.add_argument(
        "--source-docs",
        default=None,
        help="Directory containing source docs/prompts. Supports legacy flat docs or localized subfolders (default: <project-root>/doc).",
    )
    parser.add_argument(
        "--language",
        default=DEFAULT_LANGUAGE,
        choices=SUPPORTED_LANGUAGES,
        help="Spec language to initialize: zh or en (default: zh).",
    )
    parser.add_argument("--apply", action="store_true", help="Apply changes.")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes only.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files.")
    parser.add_argument(
        "--reinit",
        action="store_true",
        help="Allow reinitialization when lock file exists.",
    )
    parser.add_argument(
        "--upgrade",
        action="store_true",
        help="Refresh an existing spec bootstrap by combining --reinit and --force.",
    )
    return parser.parse_args()


def fail(message: str) -> int:
    print(f"[ERROR] {message}")
    return 1


def ensure_source_docs(source_docs: Path) -> tuple[bool, list[str]]:
    missing: list[str] = []
    for name in DOC_TO_TARGET:
        if not (source_docs / name).exists():
            missing.append(name)
    return len(missing) == 0, missing


def resolve_source_docs(source_docs_root: Path, language: str) -> tuple[Path | None, list[str]]:
    localized_dir = source_docs_root / language
    if localized_dir.exists():
        ok, missing = ensure_source_docs(localized_dir)
        if ok:
            return localized_dir, []

    ok, missing = ensure_source_docs(source_docs_root)
    if ok:
        return source_docs_root, []

    if localized_dir.exists():
        return None, missing
    return None, missing


def gather_targets(project_root: Path, generated_files: dict[str, str]) -> list[Path]:
    generated = [project_root / rel for rel in generated_files]
    copied = [project_root / rel for rel in DOC_TO_TARGET.values()]
    lock_file = [project_root / ".spec-bootstrap.lock"]
    return generated + copied + lock_file


def safe_read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def dedupe(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        normalized = item.strip()
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        result.append(normalized)
    return result


def relative_display(project_root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(project_root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def format_command_for_subdir(command: str, subdir: str) -> str:
    if subdir in ("", "."):
        return command
    return f"(cd {subdir} && {command})"


def manifest_search_roots(project_root: Path) -> list[Path]:
    roots = [project_root]
    for container_name in COMMON_CONTAINER_DIRS:
        container_dir = project_root / container_name
        if not container_dir.is_dir():
            continue
        roots.append(container_dir)
        for child in sorted(container_dir.iterdir()):
            if child.is_dir():
                roots.append(child)
    return roots


def find_manifest_paths(project_root: Path, *names: str) -> list[Path]:
    found: list[Path] = []
    for root in manifest_search_roots(project_root):
        for name in names:
            candidate = root / name
            if candidate.exists():
                found.append(candidate)
    return found


def detect_existing_paths(project_root: Path, *names: str) -> list[str]:
    return dedupe([relative_display(project_root, path) for path in find_manifest_paths(project_root, *names)])


def parse_pyproject_data(path: Path) -> dict[str, Any]:
    if tomllib is None:
        return {}

    try:
        return tomllib.loads(safe_read_text(path))
    except tomllib.TOMLDecodeError:
        return {}


def detect_project_summary(project_root: Path) -> str:
    readme = project_root / "README.md"
    if readme.exists():
        for line in safe_read_text(readme).splitlines():
            stripped = line.strip()
            if stripped and not stripped.startswith("#"):
                return stripped
    package_json = project_root / "package.json"
    if package_json.exists():
        package_name = str(parse_package_json(package_json).get("name", "")).strip()
        if package_name:
            return package_name
    pyproject = project_root / "pyproject.toml"
    if pyproject.exists():
        pyproject_data = parse_pyproject_data(pyproject)
        project_name = str(pyproject_data.get("project", {}).get("name", "")).strip()
        if project_name:
            return project_name
        poetry_name = str(pyproject_data.get("tool", {}).get("poetry", {}).get("name", "")).strip()
        if poetry_name:
            return poetry_name
    if project_root.name:
        return project_root.name
    return DEFAULT_PROJECT_SUMMARY


def detect_common_roots(project_root: Path) -> list[str]:
    found = [candidate for candidate in COMMON_ROOT_CANDIDATES if (project_root / candidate).exists()]
    if not found:
        return []
    return dedupe([path.replace("\\", "/") for path in found])


def detect_java_package_root(java_root: Path) -> str | None:
    if not java_root.is_dir():
        return None

    current = java_root
    parts: list[str] = []
    while True:
        children = [child for child in current.iterdir() if child.is_dir()]
        files = [child for child in current.iterdir() if child.is_file()]
        if len(children) != 1 or files:
            break
        current = children[0]
        parts.append(current.name)

    if not parts:
        return None
    return ".".join(parts)


def parse_package_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(safe_read_text(path))
    except json.JSONDecodeError:
        return {}


def parse_pyproject_dependencies(path: Path) -> set[str]:
    data = parse_pyproject_data(path)
    deps: set[str] = set()
    project_deps = data.get("project", {}).get("dependencies", [])
    for item in project_deps:
        name = str(item).split()[0].split("[")[0].split(">")[0].split("=")[0].lower()
        if name:
            deps.add(name)

    poetry_deps = data.get("tool", {}).get("poetry", {}).get("dependencies", {})
    deps.update(str(name).lower() for name in poetry_deps.keys())

    poetry_groups = data.get("tool", {}).get("poetry", {}).get("group", {})
    for group in poetry_groups.values():
        for name in group.get("dependencies", {}).keys():
            deps.add(str(name).lower())

    return deps


def parse_requirements_dependencies(path: Path) -> set[str]:
    dependencies: set[str] = set()
    for raw_line in safe_read_text(path).splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or line.startswith("["):
            continue
        line = line.split(";")[0].split("[")[0]
        if "=" in line and "==" not in line and ">=" not in line and "<=" not in line and "~=" not in line:
            line = line.split("=", 1)[0]
        for separator in ("==", ">=", "<=", "~=", ">", "<"):
            line = line.split(separator)[0]
        dependency = line.strip().lower()
        if dependency:
            dependencies.add(dependency)
    return dependencies


def detect_java_signals(project_root: Path) -> dict[str, Any]:
    manifests = find_manifest_paths(project_root, "pom.xml", "build.gradle", "build.gradle.kts")
    java_roots = dedupe(
        [relative_display(project_root, path.parent / "src/main/java") for path in manifests if (path.parent / "src/main/java").exists()]
    )
    if not manifests and not java_roots and not (project_root / "src/main/java").exists():
        return {"detected": False}

    frameworks: list[str] = []
    build_tools: list[str] = []
    resource_roots: list[str] = []
    test_roots: list[str] = []
    package_roots: list[str] = []
    profiles: list[str] = []
    data_signals: list[str] = []
    quality_tools: list[str] = []
    run_commands: list[str] = []
    test_commands: list[str] = []

    if (project_root / "src/main/java").exists():
        java_roots.append("src/main/java")
    java_roots = dedupe(java_roots)

    for manifest in manifests:
        manifest_dir = manifest.parent
        relative_dir = relative_display(project_root, manifest_dir)
        manifest_text = safe_read_text(manifest).lower()

        if manifest.name == "pom.xml":
            build_tools.append("Maven")
            test_commands.append(format_command_for_subdir("mvn test", relative_dir))
            if "spring-boot" in manifest_text:
                run_commands.append(format_command_for_subdir("mvn spring-boot:run", relative_dir))
        else:
            build_tools.append("Gradle")
            test_commands.append(format_command_for_subdir("./gradlew test", relative_dir))
            if "spring-boot" in manifest_text:
                run_commands.append(format_command_for_subdir("./gradlew bootRun", relative_dir))

        if "spring-boot" in manifest_text:
            frameworks.append("Spring Boot")
        if "spring-web" in manifest_text or "spring-webmvc" in manifest_text or "starter-web" in manifest_text:
            frameworks.append("Spring Web")
        if "spring-data-jpa" in manifest_text or "starter-data-jpa" in manifest_text:
            frameworks.append("Spring Data JPA")
            data_signals.append(f"检测到 JPA 相关依赖：{manifest.name}")
        if "thymeleaf" in manifest_text:
            frameworks.append("Thymeleaf")
        if "testcontainers" in manifest_text:
            frameworks.append("Testcontainers")
        if "spotless" in manifest_text:
            quality_tools.append("Spotless")
        if "checkstyle" in manifest_text:
            quality_tools.append("Checkstyle")
        if "<pmd" in manifest_text or "pmd" in manifest_text:
            quality_tools.append("PMD")
        if "jacoco" in manifest_text:
            quality_tools.append("JaCoCo")

        java_root = manifest_dir / "src/main/java"
        if java_root.exists():
            package_root = detect_java_package_root(java_root)
            if package_root:
                package_roots.append(package_root)
        for root_name in ("src/main/resources", "src/test/java"):
            candidate = manifest_dir / root_name
            if candidate.exists():
                relative_candidate = relative_display(project_root, candidate)
                if root_name.endswith("resources"):
                    resource_roots.append(relative_candidate)
                else:
                    test_roots.append(relative_candidate)

        resources_dir = manifest_dir / "src/main/resources"
        if resources_dir.exists():
            for pattern in ("application.properties", "application.yml", "application.yaml", "application-*.properties", "application-*.yml", "application-*.yaml"):
                for profile in resources_dir.glob(pattern):
                    profiles.append(relative_display(project_root, profile))
            resources_text = " ".join(safe_read_text(file).lower() for file in resources_dir.glob("application*.*"))
            if "jdbc:" in resources_text or "spring.datasource" in resources_text:
                data_signals.append(f"检测到数据库配置文件：{relative_display(project_root, resources_dir)}")
            if "postgres" in resources_text:
                data_signals.append("推测使用 PostgreSQL，待确认 profile 与连接信息。")
            if "mysql" in resources_text or "mariadb" in resources_text:
                data_signals.append("推测使用 MySQL/MariaDB，待确认 profile 与连接信息。")
            if "h2" in resources_text:
                data_signals.append("检测到 H2 相关信号，建议确认本地与测试环境差异。")

    return {
        "detected": True,
        "build_tools": dedupe(build_tools),
        "frameworks": dedupe(frameworks),
        "source_roots": java_roots,
        "resource_roots": dedupe(resource_roots),
        "test_roots": dedupe(test_roots),
        "package_roots": dedupe(package_roots),
        "profiles": dedupe(profiles),
        "data_signals": dedupe(data_signals),
        "quality_tools": dedupe(quality_tools),
        "run_commands": dedupe(run_commands),
        "test_commands": dedupe(test_commands),
    }


def detect_frontend_signals(project_root: Path) -> dict[str, Any]:
    manifests = find_manifest_paths(project_root, "package.json")
    if not manifests and not any((project_root / name).exists() for name in ("pages", "components", "public")):
        return {"detected": False}

    frameworks: list[str] = []
    build_tools: list[str] = []
    ui_dirs: list[str] = []
    test_tools: list[str] = []
    quality_tools: list[str] = []
    quality_commands: list[str] = []
    package_managers: list[str] = []
    workspace_signals: list[str] = []
    run_commands: list[str] = []
    test_commands: list[str] = []

    for manifest in manifests:
        manifest_dir = manifest.parent
        relative_dir = relative_display(project_root, manifest_dir)
        package_data = parse_package_json(manifest)
        scripts = package_data.get("scripts", {}) if isinstance(package_data.get("scripts"), dict) else {}
        dependencies = package_data.get("dependencies", {}) if isinstance(package_data.get("dependencies"), dict) else {}
        dev_dependencies = package_data.get("devDependencies", {}) if isinstance(package_data.get("devDependencies"), dict) else {}
        dependency_names = {str(name).lower() for name in dependencies.keys()} | {str(name).lower() for name in dev_dependencies.keys()}

        package_manager = "npm"
        if (manifest_dir / "pnpm-lock.yaml").exists():
            package_manager = "pnpm"
        elif (manifest_dir / "yarn.lock").exists():
            package_manager = "yarn"
        package_managers.append(package_manager)

        if "react" in dependency_names:
            frameworks.append("React")
        if "vue" in dependency_names:
            frameworks.append("Vue")
        if "next" in dependency_names:
            frameworks.append("Next.js")
        if "nuxt" in dependency_names:
            frameworks.append("Nuxt")
        if "vite" in dependency_names or (manifest_dir / "vite.config.ts").exists() or (manifest_dir / "vite.config.js").exists():
            build_tools.append("Vite")
        if "webpack" in dependency_names or (manifest_dir / "webpack.config.js").exists():
            build_tools.append("Webpack")
        if "typescript" in dependency_names or (manifest_dir / "tsconfig.json").exists():
            frameworks.append("TypeScript")
        if "tailwindcss" in dependency_names or (manifest_dir / "tailwind.config.js").exists() or (manifest_dir / "tailwind.config.ts").exists():
            frameworks.append("Tailwind CSS")
        if "eslint" in dependency_names or any((manifest_dir / name).exists() for name in ESLINT_CONFIGS):
            quality_tools.append("ESLint")
        if "prettier" in dependency_names or any((manifest_dir / name).exists() for name in PRETTIER_CONFIGS):
            quality_tools.append("Prettier")
        if "stylelint" in dependency_names or any((manifest_dir / name).exists() for name in STYLELINT_CONFIGS):
            quality_tools.append("Stylelint")
        if "vitest" in dependency_names:
            test_tools.append("Vitest")
        if "jest" in dependency_names:
            test_tools.append("Jest")
        if "playwright" in dependency_names or any((manifest_dir / name).exists() for name in PLAYWRIGHT_CONFIGS):
            test_tools.append("Playwright")
        if "cypress" in dependency_names or any((manifest_dir / name).exists() for name in CYPRESS_CONFIGS):
            test_tools.append("Cypress")

        if "dev" in scripts:
            run_commands.append(format_command_for_subdir(f"{package_manager} run dev", relative_dir))
        elif "start" in scripts:
            run_commands.append(format_command_for_subdir(f"{package_manager} run start", relative_dir))
        if "test" in scripts:
            if package_manager == "npm":
                test_commands.append(format_command_for_subdir("npm test", relative_dir))
            elif package_manager == "yarn":
                test_commands.append(format_command_for_subdir("yarn test", relative_dir))
            else:
                test_commands.append(format_command_for_subdir(f"{package_manager} test", relative_dir))
        if "test:e2e" in scripts:
            test_commands.append(format_command_for_subdir(f"{package_manager} run test:e2e", relative_dir))
        for script_name in ("lint", "typecheck", "build"):
            if script_name in scripts:
                quality_commands.append(format_command_for_subdir(f"{package_manager} run {script_name}", relative_dir))

        if "workspaces" in package_data:
            workspace_signals.append("npm workspaces")
        if (manifest_dir / "pnpm-workspace.yaml").exists():
            workspace_signals.append("pnpm workspace")
        if (manifest_dir / "turbo.json").exists():
            workspace_signals.append("Turborepo")
        if (manifest_dir / "nx.json").exists():
            workspace_signals.append("Nx")

        for dirname in ("src/pages", "pages", "src/components", "components", "public", "app"):
            candidate = manifest_dir / dirname
            if candidate.exists():
                ui_dirs.append(relative_display(project_root, candidate))

    return {
        "detected": bool(manifests or ui_dirs),
        "manifest_paths": [relative_display(project_root, manifest) for manifest in manifests],
        "frameworks": dedupe(frameworks),
        "build_tools": dedupe(build_tools),
        "ui_dirs": dedupe(ui_dirs),
        "test_tools": dedupe(test_tools),
        "quality_tools": dedupe(quality_tools),
        "quality_commands": dedupe(quality_commands),
        "package_managers": dedupe(package_managers),
        "workspace_signals": dedupe(workspace_signals),
        "run_commands": dedupe(run_commands),
        "test_commands": dedupe(test_commands),
    }


def detect_python_signals(project_root: Path) -> dict[str, Any]:
    manifests = find_manifest_paths(project_root, "pyproject.toml", "requirements.txt", "Pipfile", "manage.py", "alembic.ini")
    if not manifests and not any((project_root / name).exists() for name in ("manage.py", "alembic.ini")):
        return {"detected": False}

    frameworks: list[str] = []
    app_roots: list[str] = []
    test_roots: list[str] = []
    migration_signals: list[str] = []
    quality_tools: list[str] = []
    run_commands: list[str] = []
    test_commands: list[str] = []
    dependency_names: set[str] = set()

    for manifest in manifests:
        manifest_dir = manifest.parent
        relative_dir = relative_display(project_root, manifest_dir)

        if manifest.name == "pyproject.toml":
            dependency_names.update(parse_pyproject_dependencies(manifest))
        elif manifest.name == "requirements.txt":
            dependency_names.update(parse_requirements_dependencies(manifest))
        elif manifest.name == "Pipfile":
            dependency_names.update(parse_requirements_dependencies(manifest))
        elif manifest.name == "manage.py":
            frameworks.append("Django")
            run_commands.append(format_command_for_subdir("python manage.py runserver", relative_dir))
            test_commands.append(format_command_for_subdir("python manage.py test", relative_dir))
        elif manifest.name == "alembic.ini":
            migration_signals.append(f"检测到 Alembic 配置：{relative_display(project_root, manifest)}")

        for dirname in ("app", "src", "tests"):
            candidate = manifest_dir / dirname
            if candidate.exists():
                relative_candidate = relative_display(project_root, candidate)
                if dirname == "tests":
                    test_roots.append(relative_candidate)
                else:
                    app_roots.append(relative_candidate)

    if "django" in dependency_names:
        frameworks.append("Django")
    if "fastapi" in dependency_names:
        frameworks.append("FastAPI")
        migration_signals.append("检测到 FastAPI 相关依赖，建议确认 ASGI 入口与运行命令。")
    if "flask" in dependency_names:
        frameworks.append("Flask")
    if "sqlalchemy" in dependency_names:
        frameworks.append("SQLAlchemy")
    if "celery" in dependency_names:
        frameworks.append("Celery")
    if "pydantic" in dependency_names:
        frameworks.append("Pydantic")
    if "pytest" in dependency_names:
        frameworks.append("pytest")
    if "ruff" in dependency_names:
        quality_tools.append("Ruff")
    if "black" in dependency_names:
        quality_tools.append("Black")
    if "mypy" in dependency_names:
        quality_tools.append("mypy")
    if "tox" in dependency_names:
        quality_tools.append("tox")

    root_tests = dedupe(test_roots)
    if root_tests:
        for root in root_tests:
            test_commands.append(f"python -m pytest {root}")
    elif dependency_names:
        test_commands.append("python -m pytest")

    if not app_roots and (project_root / "app").exists():
        app_roots.append("app")

    return {
        "detected": bool(manifests or dependency_names),
        "frameworks": dedupe(frameworks),
        "app_roots": dedupe(app_roots),
        "test_roots": root_tests,
        "migration_signals": dedupe(migration_signals),
        "quality_tools": dedupe(quality_tools),
        "run_commands": dedupe(run_commands),
        "test_commands": dedupe(test_commands),
    }


def detect_project_rule_signals(
    project_root: Path,
    java_signals: dict[str, Any],
    frontend_signals: dict[str, Any],
    python_signals: dict[str, Any],
) -> dict[str, list[str]]:
    ci_tools: list[str] = []
    automation_tools: list[str] = []
    quality_tools: list[str] = []
    hook_tools: list[str] = []
    workspace_tools: list[str] = []
    package_managers: list[str] = []
    quality_commands: list[str] = []
    version_files: list[str] = []

    github_workflows = project_root / ".github/workflows"
    if github_workflows.is_dir() and any(github_workflows.glob("*.y*ml")):
        ci_tools.append("GitHub Actions")
    if (project_root / ".gitlab-ci.yml").exists():
        ci_tools.append("GitLab CI")

    if (project_root / "Makefile").exists():
        automation_tools.append("Makefile")
    if (project_root / "justfile").exists():
        automation_tools.append("Justfile")
    if any((project_root / name).exists() for name in TASKFILE_CONFIGS):
        automation_tools.append("Taskfile")

    if (project_root / ".editorconfig").exists():
        quality_tools.append("EditorConfig")
    if detect_existing_paths(project_root, *ESLINT_CONFIGS):
        quality_tools.append("ESLint")
    if detect_existing_paths(project_root, *PRETTIER_CONFIGS):
        quality_tools.append("Prettier")
    if detect_existing_paths(project_root, *STYLELINT_CONFIGS):
        quality_tools.append("Stylelint")

    if (project_root / ".husky").is_dir():
        hook_tools.append("Husky")
    if (project_root / ".pre-commit-config.yaml").exists():
        hook_tools.append("pre-commit")

    if (project_root / ".nvmrc").exists() or (project_root / ".node-version").exists():
        version_files.append("Node version pinning")
    if (project_root / ".python-version").exists():
        version_files.append("Python version pinning")

    if (project_root / "pnpm-workspace.yaml").exists():
        workspace_tools.append("pnpm workspace")
    if (project_root / "turbo.json").exists():
        workspace_tools.append("Turborepo")
    if (project_root / "nx.json").exists():
        workspace_tools.append("Nx")

    quality_tools.extend(java_signals.get("quality_tools", []))
    quality_tools.extend(frontend_signals.get("quality_tools", []))
    quality_tools.extend(python_signals.get("quality_tools", []))
    workspace_tools.extend(frontend_signals.get("workspace_signals", []))
    package_managers.extend(frontend_signals.get("package_managers", []))
    quality_commands.extend(frontend_signals.get("quality_commands", []))

    return {
        "ci_tools": dedupe(ci_tools),
        "automation_tools": dedupe(automation_tools),
        "quality_tools": dedupe(quality_tools),
        "hook_tools": dedupe(hook_tools),
        "workspace_tools": dedupe(workspace_tools),
        "package_managers": dedupe(package_managers),
        "quality_commands": dedupe(quality_commands),
        "version_files": dedupe(version_files),
    }


def detect_repo_signals(project_root: Path) -> dict[str, Any]:
    java_signals = detect_java_signals(project_root)
    frontend_signals = detect_frontend_signals(project_root)
    python_signals = detect_python_signals(project_root)
    stack_markers: list[str] = []

    if java_signals.get("detected"):
        java_summary = "Java"
        if java_signals.get("frameworks"):
            java_summary += f" ({', '.join(java_signals['frameworks'][:2])})"
        stack_markers.append(java_summary)
    if frontend_signals.get("detected"):
        frontend_summary = "Frontend"
        frontend_labels = frontend_signals.get("frameworks", []) + frontend_signals.get("build_tools", [])
        if not frontend_labels and not frontend_signals.get("ui_dirs") and frontend_signals.get("manifest_paths"):
            frontend_summary = "Node.js"
        elif frontend_labels:
            frontend_summary += f" ({', '.join(frontend_labels[:3])})"
        stack_markers.append(frontend_summary)
    if python_signals.get("detected"):
        python_summary = "Python"
        if python_signals.get("frameworks"):
            python_summary += f" ({', '.join(python_signals['frameworks'][:2])})"
        stack_markers.append(python_summary)

    container_signals = [name for name in ("docker-compose.yml", "docker-compose.yaml", "Dockerfile") if (project_root / name).exists()]
    project_rules = detect_project_rule_signals(project_root, java_signals, frontend_signals, python_signals)
    return {
        "project_summary": detect_project_summary(project_root),
        "common_roots": detect_common_roots(project_root),
        "java": java_signals,
        "frontend": frontend_signals,
        "python": python_signals,
        "stack_markers": dedupe(stack_markers),
        "container_signals": container_signals,
        "project_rules": project_rules,
    }


def localize_signal_line(line: str, language: str) -> str:
    if language == "zh":
        return line

    if line.startswith("检测到 JPA 相关依赖："):
        return line.replace("检测到 JPA 相关依赖：", "Detected JPA-related dependency: ")
    if line.startswith("检测到数据库配置文件："):
        return line.replace("检测到数据库配置文件：", "Detected database config directory: ")
    if line == "推测使用 PostgreSQL，待确认 profile 与连接信息。":
        return "Potential PostgreSQL signal detected; confirm profile selection and connection details."
    if line == "推测使用 MySQL/MariaDB，待确认 profile 与连接信息。":
        return "Potential MySQL/MariaDB signal detected; confirm profile selection and connection details."
    if line == "检测到 H2 相关信号，建议确认本地与测试环境差异。":
        return "Detected H2-related signal; confirm differences between local and test environments."
    if line.startswith("检测到 Alembic 配置："):
        return line.replace("检测到 Alembic 配置：", "Detected Alembic configuration: ")
    if line == "检测到 FastAPI 相关依赖，建议确认 ASGI 入口与运行命令。":
        return "Detected FastAPI-related dependency; confirm the ASGI entrypoint and runtime command."
    return line


def detect_run_commands(signals: dict[str, Any]) -> list[str]:
    commands = []
    commands.extend(signals.get("java", {}).get("run_commands", []))
    commands.extend(signals.get("frontend", {}).get("run_commands", []))
    commands.extend(signals.get("python", {}).get("run_commands", []))
    return dedupe(commands)


def detect_test_commands(signals: dict[str, Any]) -> list[str]:
    commands = []
    commands.extend(signals.get("java", {}).get("test_commands", []))
    commands.extend(signals.get("frontend", {}).get("test_commands", []))
    commands.extend(signals.get("python", {}).get("test_commands", []))
    return dedupe(commands)


def detect_core_modules(project_root: Path, signals: dict[str, Any], language: str) -> list[str]:
    modules: list[str] = []
    java_signals = signals.get("java", {})
    frontend_signals = signals.get("frontend", {})
    python_signals = signals.get("python", {})

    if java_signals.get("detected"):
        java_parts = java_signals.get("build_tools", []) + java_signals.get("frameworks", [])
        java_summary = "检测到 Java 模块" if language == "zh" else "Detected Java module"
        if not java_parts:
            java_summary = "检测到 Java 工程" if language == "zh" else "Detected Java project"
        if java_parts:
            java_summary += f"：{', '.join(java_parts)}"
        modules.append(java_summary)
        if java_signals.get("source_roots"):
            label = "Java 源码目录" if language == "zh" else "Java source roots"
            modules.append(f"{label}：{', '.join(java_signals['source_roots'])}")
        if java_signals.get("package_roots"):
            label = "推测主包" if language == "zh" else "Inferred base package"
            modules.append(f"{label}：{', '.join(java_signals['package_roots'][:3])}")

    if frontend_signals.get("detected"):
        frontend_parts = frontend_signals.get("frameworks", []) + frontend_signals.get("build_tools", [])
        frontend_summary = "检测到前端模块" if language == "zh" else "Detected frontend module"
        if not frontend_parts:
            frontend_summary = "检测到前端结构" if language == "zh" else "Detected frontend structure"
        if frontend_parts:
            frontend_summary += f"：{', '.join(frontend_parts)}"
        modules.append(frontend_summary)
        if frontend_signals.get("ui_dirs"):
            label = "页面/组件目录" if language == "zh" else "Page/component directories"
            modules.append(f"{label}：{', '.join(frontend_signals['ui_dirs'][:5])}")

    if python_signals.get("detected"):
        python_parts = python_signals.get("frameworks", [])
        python_summary = "检测到 Python 模块" if language == "zh" else "Detected Python module"
        if not python_parts:
            python_summary = "检测到 Python 工程" if language == "zh" else "Detected Python project"
        if python_parts:
            python_summary += f"：{', '.join(python_parts)}"
        modules.append(python_summary)
        if python_signals.get("app_roots"):
            label = "Python 应用目录" if language == "zh" else "Python application directories"
            modules.append(f"{label}：{', '.join(python_signals['app_roots'][:5])}")

    if not modules:
        if language == "zh":
            modules.append("待确认：未检测到高置信度的模块边界，建议先结合 README 和现有目录结构补充。")
        else:
            modules.append("Confirmation needed: no high-confidence module boundary detected yet; review the README and current directory layout.")
    return modules


def build_context_model(project_root: Path, signals: dict[str, Any], language: str) -> dict[str, Any]:
    run_commands = detect_run_commands(signals)
    test_commands = detect_test_commands(signals)
    java_signals = signals.get("java", {})
    frontend_signals = signals.get("frontend", {})
    python_signals = signals.get("python", {})
    project_rules = signals.get("project_rules", {})

    runtime_constraints: list[str] = []
    if java_signals.get("profiles"):
        label = "检测到 Spring profile 或配置文件" if language == "zh" else "Detected Spring profiles or config files"
        runtime_constraints.append(f"{label}：{', '.join(java_signals['profiles'][:5])}")
    runtime_constraints.extend(localize_signal_line(line, language) for line in java_signals.get("data_signals", []))
    runtime_constraints.extend(localize_signal_line(line, language) for line in python_signals.get("migration_signals", []))
    if run_commands:
        label = "建议关注运行入口" if language == "zh" else "Suggested runtime entrypoints"
        runtime_constraints.append(f"{label}：{'; '.join(run_commands)}")
    if not runtime_constraints:
        if language == "zh":
            runtime_constraints.append("待确认：未检测到稳定的运行入口或数据配置，建议确认应用启动方式、数据库与 profile。")
        else:
            runtime_constraints.append("Confirmation needed: no stable runtime entrypoint or data configuration was detected; confirm app startup, database, and profile usage.")

    testing_constraints: list[str] = []
    if test_commands:
        label = "建议优先验证" if language == "zh" else "Suggested validation commands"
        testing_constraints.append(f"{label}：{'; '.join(test_commands)}")
    if "Testcontainers" in java_signals.get("frameworks", []):
        if language == "zh":
            testing_constraints.append("检测到 Testcontainers，建议确认测试环境依赖的容器运行条件。")
        else:
            testing_constraints.append("Detected Testcontainers; confirm container runtime assumptions for the test environment.")
    if frontend_signals.get("test_tools"):
        label = "检测到前端测试工具" if language == "zh" else "Detected frontend test tools"
        testing_constraints.append(f"{label}：{', '.join(frontend_signals['test_tools'])}")
    if python_signals.get("test_roots"):
        label = "检测到 Python 测试目录" if language == "zh" else "Detected Python test directories"
        testing_constraints.append(f"{label}：{', '.join(python_signals['test_roots'])}")
    if not testing_constraints:
        if language == "zh":
            testing_constraints.append("待确认：未检测到明确测试策略，建议确认自动化测试入口与回归范围。")
        else:
            testing_constraints.append("Confirmation needed: no clear test strategy was detected; confirm automation entrypoints and regression scope.")

    ui_api_constraints: list[str] = []
    if frontend_signals.get("frameworks") or frontend_signals.get("ui_dirs"):
        ui_labels = frontend_signals.get("frameworks", []) + frontend_signals.get("build_tools", [])
        if ui_labels:
            label = "检测到 UI 技术栈" if language == "zh" else "Detected UI stack"
            ui_api_constraints.append(f"{label}：{', '.join(dedupe(ui_labels))}")
        if frontend_signals.get("ui_dirs"):
            label = "建议关注用户可见目录" if language == "zh" else "User-visible directories to review"
            ui_api_constraints.append(f"{label}：{', '.join(frontend_signals['ui_dirs'][:5])}")
    if java_signals.get("frameworks") or python_signals.get("frameworks"):
        if language == "zh":
            ui_api_constraints.append("建议关注对外接口兼容性、序列化结构与前后端契约，避免把推测写成既定事实。")
        else:
            ui_api_constraints.append("Review public interface compatibility, serialization shape, and frontend/backend contracts without turning inferences into hard facts.")
    if not ui_api_constraints:
        if language == "zh":
            ui_api_constraints.append("待确认：未检测到明显的 UI 或接口目录，建议确认是否存在 API、页面或外部集成边界。")
        else:
            ui_api_constraints.append("Confirmation needed: no obvious UI or interface boundary was detected; confirm APIs, pages, or external integration surfaces.")

    engineering_constraints: list[str] = []
    if signals.get("common_roots"):
        label = "检测到常见源码根目录" if language == "zh" else "Detected common source roots"
        engineering_constraints.append(f"{label}：{', '.join(signals['common_roots'][:8])}")
    if signals.get("container_signals"):
        label = "检测到容器相关文件" if language == "zh" else "Detected container-related files"
        engineering_constraints.append(f"{label}：{', '.join(signals['container_signals'])}")
    if frontend_signals.get("build_tools"):
        label = "建议关注前端构建链路" if language == "zh" else "Suggested frontend build chain to review"
        engineering_constraints.append(f"{label}：{', '.join(frontend_signals['build_tools'])}")
    if java_signals.get("build_tools"):
        label = "检测到 Java 构建工具" if language == "zh" else "Detected Java build tools"
        engineering_constraints.append(f"{label}：{', '.join(java_signals['build_tools'])}")
    if not engineering_constraints:
        if language == "zh":
            engineering_constraints.append("待确认：工程约束不足，建议确认构建链路、部署方式与目录边界。")
        else:
            engineering_constraints.append("Confirmation needed: engineering constraints are still sparse; confirm build chain, deployment flow, and directory boundaries.")

    project_rule_constraints: list[str] = []
    if project_rules.get("ci_tools"):
        label = "检测到 CI / 自动化流程" if language == "zh" else "Detected CI and automation flows"
        project_rule_constraints.append(f"{label}：{', '.join(project_rules['ci_tools'])}")
    if project_rules.get("automation_tools"):
        label = "检测到统一任务入口" if language == "zh" else "Detected shared task entrypoints"
        project_rule_constraints.append(f"{label}：{', '.join(project_rules['automation_tools'])}")
    if project_rules.get("workspace_tools"):
        label = "检测到工作区或仓库编排约束" if language == "zh" else "Detected workspace or repository orchestration constraints"
        project_rule_constraints.append(f"{label}：{', '.join(project_rules['workspace_tools'])}")
    if project_rules.get("package_managers"):
        label = "检测到包管理器 / 工具链约束" if language == "zh" else "Detected package-manager or toolchain constraints"
        project_rule_constraints.append(f"{label}：{', '.join(project_rules['package_managers'])}")
    if project_rules.get("quality_tools"):
        label = "检测到代码质量 / 格式化规则" if language == "zh" else "Detected code-quality and formatting rules"
        project_rule_constraints.append(f"{label}：{', '.join(project_rules['quality_tools'])}")
    if project_rules.get("hook_tools"):
        label = "检测到本地提交门禁" if language == "zh" else "Detected local commit gates"
        project_rule_constraints.append(f"{label}：{', '.join(project_rules['hook_tools'])}")
    if project_rules.get("version_files"):
        label = "检测到运行时版本约束" if language == "zh" else "Detected runtime version pinning"
        project_rule_constraints.append(f"{label}：{', '.join(project_rules['version_files'])}")
    if project_rules.get("quality_commands"):
        label = "建议将以下命令视为提交前检查" if language == "zh" else "Treat these commands as likely pre-commit or CI checks"
        project_rule_constraints.append(f"{label}：{'; '.join(project_rules['quality_commands'])}")
    if not project_rule_constraints:
        if language == "zh":
            project_rule_constraints.append("待确认：尚未检测到稳定的项目规则来源，建议补充 CI、lint/format、hooks 与统一脚本约定。")
        else:
            project_rule_constraints.append("Confirmation needed: no stable repository-rule source was detected yet; review CI, lint/format, hooks, and shared task scripts.")

    if language == "zh":
        domain_constraints = [
            "业务约束：待确认，建议结合 README、现有接口与数据库模型补充。",
            "合规/安全约束：待确认，建议确认鉴权、敏感配置、数据访问边界。",
        ]
        non_functional_constraints = [
            "性能：待确认，建议关注热点接口、前端构建体积或数据库查询。",
            "可靠性：待确认，建议确认关键流程、事务边界与失败恢复策略。",
            "可观测性：待确认，建议确认日志、指标、追踪与告警基线。",
        ]
        assumptions = [
            "待确认问题：自动生成仅基于仓库信号，隐藏模块、运行入口与环境差异仍需人工确认。",
            "待决策事项：若仓库为混合栈，需确认主应用入口、子项目边界与发布方式。",
            "当前仓库上下文中的已知缺口：未对业务规则、外部系统依赖和生产配置做确定性推断。",
        ]
    else:
        domain_constraints = [
            "Business constraints: confirmation needed; extend with README, current interfaces, and data model context.",
            "Compliance/security constraints: confirmation needed; review auth, sensitive configuration, and data boundaries.",
        ]
        non_functional_constraints = [
            "Performance: confirmation needed; review hot paths, frontend bundle size, or database query pressure.",
            "Reliability: confirmation needed; review critical flows, transaction boundaries, and failure recovery.",
            "Observability: confirmation needed; review logs, metrics, tracing, and alerting baseline.",
        ]
        assumptions = [
            "Open questions: auto-generation relies on repository signals; hidden modules, runtime entrypoints, and environment differences still need review.",
            "Pending decisions: mixed-stack repositories should confirm primary app entrypoints, subproject boundaries, and release flow.",
            "Known gaps in current repository context: business rules, external integrations, and production configuration were not inferred as hard facts.",
        ]

    return {
        "project_summary": signals["project_summary"],
        "stack_summary": ", ".join(signals["stack_markers"]) if signals["stack_markers"] else DEFAULT_STACK,
        "source_roots": ", ".join(signals["common_roots"]) if signals["common_roots"] else DEFAULT_SOURCE_ROOTS,
        "run_commands": run_commands,
        "test_commands": test_commands,
        "core_modules": detect_core_modules(project_root, signals, language),
        "runtime_constraints": runtime_constraints,
        "testing_constraints": testing_constraints,
        "ui_api_constraints": ui_api_constraints,
        "engineering_constraints": engineering_constraints,
        "project_rule_constraints": project_rule_constraints,
        "domain_constraints": domain_constraints,
        "non_functional_constraints": non_functional_constraints,
        "assumptions": assumptions,
    }


def detect_stack(project_root: Path) -> str:
    return build_context_model(project_root, detect_repo_signals(project_root), DEFAULT_LANGUAGE)["stack_summary"]


def detect_test_command(project_root: Path) -> str:
    commands = build_context_model(project_root, detect_repo_signals(project_root), DEFAULT_LANGUAGE)["test_commands"]
    if not commands:
        return DEFAULT_TEST_COMMAND
    return "; ".join(commands)


def detect_source_roots(project_root: Path) -> str:
    roots = detect_common_roots(project_root)
    if not roots:
        return DEFAULT_SOURCE_ROOTS
    return ", ".join(roots)


def build_template_replacements(project_root: Path, context_model: dict[str, Any]) -> dict[str, str]:
    return {
        "{{PROJECT_SUMMARY}}": context_model["project_summary"],
        "{{DETECTED_STACK}}": context_model["stack_summary"],
        "{{TEST_COMMAND}}": "; ".join(context_model["test_commands"]) if context_model["test_commands"] else DEFAULT_TEST_COMMAND,
        "{{SOURCE_ROOTS}}": context_model["source_roots"],
    }


def render_section(title: str, lines: list[str]) -> str:
    section = [f"## {title}", ""]
    section.extend(f"- {line}" for line in lines)
    return "\n".join(section)


def render_spec_context(context: dict[str, Any], language: str) -> str:
    run_summary = "; ".join(context["run_commands"]) if context["run_commands"] else DEFAULT_RUN_COMMAND
    test_summary = "; ".join(context["test_commands"]) if context["test_commands"] else DEFAULT_TEST_COMMAND

    if language == "zh":
        sections = [
            render_section(
                "仓库摘要",
                [
                    f"Project: {context['project_summary']}",
                    f"Stack: {context['stack_summary']}",
                    f"Source roots: {context['source_roots']}",
                    f"Suggested run commands: {run_summary}",
                    f"Suggested test commands: {test_summary}",
                    "自动上下文说明：基于仓库文件与目录检测生成，低置信度信息已保留为待确认。",
                ],
            ),
            render_section("核心模块", context["core_modules"]),
            render_section("运行与数据约束", context["runtime_constraints"]),
            render_section("测试与验证约束", context["testing_constraints"]),
            render_section("UI 与接口约束", context["ui_api_constraints"]),
            render_section("工程约束", context["engineering_constraints"]),
            render_section("项目规则与协作约束", context["project_rule_constraints"]),
            render_section("领域约束", context["domain_constraints"]),
            render_section("非功能约束", context["non_functional_constraints"]),
            render_section("假设与未知项", context["assumptions"]),
        ]
    else:
        sections = [
            render_section(
                "Repository Summary",
                [
                    f"Project: {context['project_summary']}",
                    f"Stack: {context['stack_summary']}",
                    f"Source roots: {context['source_roots']}",
                    f"Suggested run commands: {run_summary}",
                    f"Suggested test commands: {test_summary}",
                    "Auto-context note: generated from repository files and directories; low-confidence items remain marked for confirmation.",
                ],
            ),
            render_section("Core Modules", context["core_modules"]),
            render_section("Runtime And Data Constraints", context["runtime_constraints"]),
            render_section("Testing And Validation Constraints", context["testing_constraints"]),
            render_section("UI And Interface Constraints", context["ui_api_constraints"]),
            render_section("Engineering Constraints", context["engineering_constraints"]),
            render_section("Project Rules And Collaboration Constraints", context["project_rule_constraints"]),
            render_section("Domain Constraints", context["domain_constraints"]),
            render_section("Non-functional Constraints", context["non_functional_constraints"]),
            render_section("Assumptions And Unknowns", context["assumptions"]),
        ]

    return "# SPEC_CONTEXT\n\n" + "\n\n".join(sections) + "\n"


def render_generated_file(
    rel_path: str,
    content: str,
    replacements: dict[str, str],
    context_model: dict[str, Any],
    language: str,
) -> str:
    if rel_path == "spec/SPEC_CONTEXT.md":
        return render_spec_context(context_model, language)

    rendered = content
    for placeholder, value in replacements.items():
        rendered = rendered.replace(placeholder, value)
    return rendered


def print_plan(
    project_root: Path,
    source_docs: Path,
    targets: list[Path],
    force: bool,
    language: str,
) -> None:
    print("[PLAN] Spec initialization preview")
    print(f"  project_root: {project_root}")
    print(f"  source_docs : {source_docs}")
    print(f"  language    : {language}")
    print(f"  overwrite   : {'yes' if force else 'no'}")
    for path in targets:
        status = "overwrite" if path.exists() else "create"
        print(f"  - {status}: {path.relative_to(project_root)}")


def write_text_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def apply_changes(
    project_root: Path,
    source_docs: Path,
    targets: list[Path],
    force: bool,
    generated_files: dict[str, str],
    language: str,
) -> int:
    conflicts = [p for p in targets if p.exists() and not force]
    if conflicts:
        print("[ERROR] Existing files would be overwritten. Re-run with --force.")
        for item in conflicts:
            print(f"  - {item.relative_to(project_root)}")
        return 1

    signals = detect_repo_signals(project_root)
    context_model = build_context_model(project_root, signals, language)
    replacements = build_template_replacements(project_root, context_model)

    for rel_path, content in generated_files.items():
        target = project_root / rel_path
        write_text_file(target, render_generated_file(rel_path, content, replacements, context_model, language))
        print(f"[WRITE] {target.relative_to(project_root)}")

    for src_name, dest_rel in DOC_TO_TARGET.items():
        src = source_docs / src_name
        dest = project_root / dest_rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dest)
        print(f"[COPY ] {dest.relative_to(project_root)} <- {src_name}")

    lock_file = project_root / ".spec-bootstrap.lock"
    lock_content = (
        "spec-bootstrap initialized\n"
        f"timestamp_utc={datetime.now(timezone.utc).isoformat()}\n"
        f"language={language}\n"
    )
    write_text_file(lock_file, lock_content)
    print(f"[WRITE] {lock_file.relative_to(project_root)}")
    return 0


def main() -> int:
    args = parse_args()
    if args.apply and args.dry_run:
        return fail("Use only one mode: --apply or --dry-run.")

    mode_apply = args.apply
    if not args.apply and not args.dry_run:
        mode_apply = False

    effective_force = args.force or args.upgrade
    effective_reinit = args.reinit or args.upgrade
    generated_files = GENERATED_FILES_BY_LANGUAGE[args.language]
    project_root = Path(args.project_root).resolve()
    source_docs_root = (
        Path(args.source_docs).resolve()
        if args.source_docs
        else (project_root / "doc").resolve()
    )

    if not project_root.exists():
        return fail(f"Project root not found: {project_root}")
    if not source_docs_root.exists():
        return fail(f"Source docs directory not found: {source_docs_root}")

    source_docs, missing = resolve_source_docs(source_docs_root, args.language)
    if source_docs is None:
        print("[ERROR] Missing required source files under doc directory:")
        for name in missing:
            print(f"  - {name}")
        return 1

    lock_file = project_root / ".spec-bootstrap.lock"
    if lock_file.exists() and not effective_reinit:
        return fail("Lock exists. Use --reinit or --upgrade to run initialization again.")

    targets = gather_targets(project_root, generated_files)
    print_plan(project_root, source_docs, targets, effective_force, args.language)

    if not mode_apply:
        print("[DRY-RUN] No file written.")
        return 0

    return apply_changes(
        project_root=project_root,
        source_docs=source_docs,
        targets=targets,
        force=effective_force,
        generated_files=generated_files,
        language=args.language,
    )


if __name__ == "__main__":
    sys.exit(main())
