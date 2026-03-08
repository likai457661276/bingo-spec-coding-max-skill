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


DOC_TO_TARGET = {
    "spec_bootstrap_prompt_v6.md": "spec/prompts/spec_bootstrap_prompt_v6.md",
    "change_classifier.prompt.md": "spec/prompts/change_classifier.prompt.md",
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

## Spec Workflow

默认工作流：

Context -> Plan -> Spec -> Tasks -> Code

分级工作流：

L1（Feature）: Context -> Plan -> Spec -> Tasks -> Code
L2（Small Change）: Tasks -> Code
L3（Hotfix）: Patch Proposal -> Code

## Change Types

所有代码改动都必须声明以下之一：

BUG_FIX | SMALL_CHANGE | FEATURE

映射关系：

L1 -> FEATURE
L2 -> SMALL_CHANGE（纯缺陷修复可使用 BUG_FIX）
L3 -> BUG_FIX

## Human Gates

L1 需要在以下阶段后获得确认：

1. Plan
2. Spec
3. Tasks

L2 需要在以下阶段后获得确认：

1. Tasks

L3 需要在以下阶段后获得确认：

1. Patch Proposal

## Safe Execution Rule

在当前变更级别要求的门禁明确通过之前，不得进入代码实现阶段。
""",
        "spec/INDEX.md": """# 规格索引

## 核心文档

1. [SPEC_CONTEXT.md](./SPEC_CONTEXT.md)
2. [SPEC_WORKFLOW.md](./SPEC_WORKFLOW.md)
3. [CHANGE_POLICY.md](./CHANGE_POLICY.md)

## Agent 入口

Agent 应从本文件进入规格树，再定位到 `spec/features/<feature-name>/` 下的相关特性目录。

## Prompt 来源

1. [spec_bootstrap_prompt_v6.md](./prompts/spec_bootstrap_prompt_v6.md)
2. [change_classifier.prompt.md](./prompts/change_classifier.prompt.md)
3. [generate_feature_tasks.prompt.md](./prompts/generate_feature_tasks.prompt.md)
4. [generate_change_tasks.prompt.md](./prompts/generate_change_tasks.prompt.md)

## 模板

1. [PLAN_TEMPLATE.md](./templates/PLAN_TEMPLATE.md)
2. [SPEC_TEMPLATE.md](./templates/SPEC_TEMPLATE.md)
3. [TASK_TEMPLATE.md](./templates/TASK_TEMPLATE.md)
4. [CHANGE_TEMPLATE.md](./templates/CHANGE_TEMPLATE.md)
5. [HOTFIX_TEMPLATE.md](./templates/HOTFIX_TEMPLATE.md)

## 使用示例

1. [usage_examples.md](./usage/usage_examples.md)
2. 特性目录：`spec/features/<feature-name>/`

## 导航规则

1. 先阅读本索引。
2. 再定位到相关特性目录。
3. L1 先读 `plan.md`。
4. 编写任务或代码前先读 `spec.md`。
5. 编码前读取 `tasks.md` 或变更任务说明。
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

## 变更分级

### L1 Feature Change

1. 分析仓库上下文
2. 产出计划
3. 产出功能规格
4. 产出任务拆分
5. 实施代码

必须确认：Plan、Spec、Tasks。

### L2 Small Change

1. 阅读相关 feature spec
2. 生成 change tasks
3. 等待确认
4. 实施代码

### L3 Hotfix

1. 快速定位问题
2. 提出最小补丁
3. 等待确认
4. 实施补丁

## 升级规则

- 当 L2 超出局部修复范围时，升级为 L1。
- 当 L3 不再是最小安全补丁时，升级为 L2 或 L1。
- 当实现改变了既有行为时，必须回写规格文档。

## Prompt 路由

- 分级判断：`spec/prompts/change_classifier.prompt.md`
- L1 任务生成：`spec/prompts/generate_feature_tasks.prompt.md`
- L2 任务生成：`spec/prompts/generate_change_tasks.prompt.md`
""",
        "spec/CHANGE_POLICY.md": """# CHANGE_POLICY

## 允许的变更标签

1. FEATURE
2. SMALL_CHANGE
3. BUG_FIX

## 映射规则

1. L1 -> FEATURE
2. L2 -> SMALL_CHANGE（纯缺陷修复可使用 BUG_FIX）
3. L3 -> BUG_FIX

## 执行护栏

1. 优先最小文件改动。
2. L2/L3 避免引入架构变化。
3. Hotfix 必须是最小安全补丁。

## 文档规则

1. L1 编码前必须先更新 plan、spec、tasks。
2. L2 必须在相关 feature 下记录 change 历史。
3. L3 稳定后必须补回规格历史。
""",
        "spec/templates/PLAN_TEMPLATE.md": """# Plan: <feature-name>

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

## Spec Workflow

Default workflow:

Context -> Plan -> Spec -> Tasks -> Code

Change-level workflow:

L1 (Feature): Context -> Plan -> Spec -> Tasks -> Code
L2 (Small Change): Tasks -> Code
L3 (Hotfix): Patch Proposal -> Code

## Change Types

All code changes must declare one of:

BUG_FIX | SMALL_CHANGE | FEATURE

Mapping:

L1 -> FEATURE
L2 -> SMALL_CHANGE (or BUG_FIX if defect-only)
L3 -> BUG_FIX

## Human Gates

L1 requires approval after:

1. Plan
2. Spec
3. Tasks

L2 requires approval after:

1. Tasks

L3 requires approval after:

1. Patch Proposal

## Safe Execution Rule

Do not implement code before the required gate for the current level is explicitly approved.
""",
        "spec/INDEX.md": """# Spec Index

## Core

1. [SPEC_CONTEXT.md](./SPEC_CONTEXT.md)
2. [SPEC_WORKFLOW.md](./SPEC_WORKFLOW.md)
3. [CHANGE_POLICY.md](./CHANGE_POLICY.md)

## Agent Entry

Agents should enter the spec tree from this file, then locate the relevant feature under `spec/features/<feature-name>/`.

## Prompt Sources

1. [spec_bootstrap_prompt_v6.md](./prompts/spec_bootstrap_prompt_v6.md)
2. [change_classifier.prompt.md](./prompts/change_classifier.prompt.md)
3. [generate_feature_tasks.prompt.md](./prompts/generate_feature_tasks.prompt.md)
4. [generate_change_tasks.prompt.md](./prompts/generate_change_tasks.prompt.md)

## Templates

1. [PLAN_TEMPLATE.md](./templates/PLAN_TEMPLATE.md)
2. [SPEC_TEMPLATE.md](./templates/SPEC_TEMPLATE.md)
3. [TASK_TEMPLATE.md](./templates/TASK_TEMPLATE.md)
4. [CHANGE_TEMPLATE.md](./templates/CHANGE_TEMPLATE.md)
5. [HOTFIX_TEMPLATE.md](./templates/HOTFIX_TEMPLATE.md)

## Usage

1. [usage_examples.md](./usage/usage_examples.md)
2. Features path: `spec/features/<feature-name>/`

## Navigation

1. Read this index first.
2. Locate the relevant feature folder.
3. Read `plan.md` for L1 changes.
4. Read `spec.md` before generating tasks or code.
5. Read `tasks.md` or change-level task notes before coding.
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

## Change Levels

### L1 Feature Change

1. Analyze repository context
2. Create plan
3. Create feature spec
4. Create tasks
5. Implement code

Required approvals: Plan, Spec, Tasks.

### L2 Small Change

1. Read existing feature spec
2. Generate change tasks
3. Wait for approval
4. Implement code

### L3 Hotfix

1. Locate issue quickly
2. Propose minimal patch
3. Wait for approval
4. Implement patch

## Human Gate Rules

### L1

- Approval after `Plan`
- Approval after `Spec`
- Approval after `Tasks`

### L2

- Approval after `Tasks`

### L3

- Approval after `Patch Proposal`

## Escalation Rules

- Escalate L2 to L1 when the change expands beyond a local fix.
- Escalate L3 to L2 or L1 when the patch is no longer minimal.
- Update spec artifacts when implementation changes documented behavior.

## Prompt Routing

- Level classification: `spec/prompts/change_classifier.prompt.md`
- L1 tasks: `spec/prompts/generate_feature_tasks.prompt.md`
- L2 tasks: `spec/prompts/generate_change_tasks.prompt.md`
""",
        "spec/CHANGE_POLICY.md": """# CHANGE_POLICY

## Allowed Change Tags

1. FEATURE
2. SMALL_CHANGE
3. BUG_FIX

## Mapping Rule

1. L1 -> FEATURE
2. L2 -> SMALL_CHANGE (or BUG_FIX for defect-only updates)
3. L3 -> BUG_FIX

## Execution Guardrail

1. Minimal-file-change first.
2. Avoid architecture changes in L2/L3.
3. Hotfix must target smallest safe patch.

## Documentation Rule

1. L1 changes must update plan, spec, and tasks before coding.
2. L2 changes must be recorded under the related feature change history.
3. L3 hotfixes must be backfilled into spec history after stabilization.
""",
        "spec/templates/PLAN_TEMPLATE.md": """# Plan: <feature-name>

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


def detect_project_summary(project_root: Path) -> str:
    readme = project_root / "README.md"
    if readme.exists():
        for line in safe_read_text(readme).splitlines():
            stripped = line.strip()
            if stripped and not stripped.startswith("#"):
                return stripped
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
    if tomllib is None:
        return set()

    try:
        data = tomllib.loads(safe_read_text(path))
    except tomllib.TOMLDecodeError:
        return set()

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
        "run_commands": dedupe(run_commands),
        "test_commands": dedupe(test_commands),
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
    return {
        "project_summary": detect_project_summary(project_root),
        "common_roots": detect_common_roots(project_root),
        "java": java_signals,
        "frontend": frontend_signals,
        "python": python_signals,
        "stack_markers": dedupe(stack_markers),
        "container_signals": container_signals,
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


def detect_project_summary(project_root: Path) -> str:
    readme = project_root / "README.md"
    if readme.exists():
        for line in readme.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if stripped and not stripped.startswith("#"):
                return stripped
    return DEFAULT_PROJECT_SUMMARY


def detect_stack(project_root: Path) -> str:
    markers = []
    if (project_root / "package.json").exists():
        markers.append("Node.js")
    if (project_root / "pyproject.toml").exists() or (project_root / "requirements.txt").exists():
        markers.append("Python")
    if (project_root / "go.mod").exists():
        markers.append("Go")
    if (project_root / "Cargo.toml").exists():
        markers.append("Rust")
    if (project_root / "pom.xml").exists() or (project_root / "build.gradle").exists():
        markers.append("Java")
    if not markers:
        return DEFAULT_STACK
    return ", ".join(markers)


def detect_test_command(project_root: Path) -> str:
    if (project_root / "package.json").exists():
        return "npm test"
    if (project_root / "pyproject.toml").exists() or (project_root / "requirements.txt").exists():
        return "pytest"
    if (project_root / "go.mod").exists():
        return "go test ./..."
    if (project_root / "Cargo.toml").exists():
        return "cargo test"
    if (project_root / "pom.xml").exists():
        return "mvn test"
    if (project_root / "build.gradle").exists():
        return "./gradlew test"
    return DEFAULT_TEST_COMMAND


def detect_source_roots(project_root: Path) -> str:
    candidates = ["src", "app", "lib", "backend", "frontend", "packages", "services"]
    found = [name for name in candidates if (project_root / name).exists()]
    if not found:
        return DEFAULT_SOURCE_ROOTS
    return ", ".join(found)


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
