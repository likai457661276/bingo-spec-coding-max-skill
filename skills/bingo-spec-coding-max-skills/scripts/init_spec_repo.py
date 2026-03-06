#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
import shutil
import sys


DEFAULT_PROJECT_SUMMARY = "Fill in project goals and architecture summary."
DEFAULT_STACK = "Unknown stack. Fill in runtime, framework, database, and deployment details."
DEFAULT_TEST_COMMAND = "No common test command detected."
DEFAULT_SOURCE_ROOTS = "No common source roots detected."


DOC_TO_TARGET = {
    "spec_bootstrap_prompt_v6.md": "spec/prompts/spec_bootstrap_prompt_v6.md",
    "change_classifier.prompt.md": "spec/prompts/change_classifier.prompt.md",
    "generate_feature_tasks.prompt.md": "spec/prompts/generate_feature_tasks.prompt.md",
    "generate_change_tasks.prompt.md": "spec/prompts/generate_change_tasks.prompt.md",
    "usage_examples.md": "spec/usage/usage_examples.md",
}


GENERATED_FILES = {
    "AGENTS.md": """Always respond in Chinese-simplified

# Project Agent Policy

## Repository Snapshot

- Project Summary: {{PROJECT_SUMMARY}}
- Detected Stack: {{DETECTED_STACK}}
- Suggested Test Command: {{TEST_COMMAND}}
- Suggested Source Roots: {{SOURCE_ROOTS}}

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
        help="Directory containing source docs/prompts (default: <project-root>/doc).",
    )
    parser.add_argument("--apply", action="store_true", help="Apply changes.")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes only.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files.")
    parser.add_argument(
        "--reinit",
        action="store_true",
        help="Allow reinitialization when lock file exists.",
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


def gather_targets(project_root: Path) -> list[Path]:
    generated = [project_root / rel for rel in GENERATED_FILES]
    copied = [project_root / rel for rel in DOC_TO_TARGET.values()]
    lock_file = [project_root / ".spec-bootstrap.lock"]
    return generated + copied + lock_file


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


def render_generated_file(content: str, project_root: Path) -> str:
    replacements = {
        "{{PROJECT_SUMMARY}}": detect_project_summary(project_root),
        "{{DETECTED_STACK}}": detect_stack(project_root),
        "{{TEST_COMMAND}}": detect_test_command(project_root),
        "{{SOURCE_ROOTS}}": detect_source_roots(project_root),
    }
    rendered = content
    for placeholder, value in replacements.items():
        rendered = rendered.replace(placeholder, value)
    return rendered


def print_plan(project_root: Path, source_docs: Path, targets: list[Path], force: bool) -> None:
    print("[PLAN] Spec initialization preview")
    print(f"  project_root: {project_root}")
    print(f"  source_docs : {source_docs}")
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
) -> int:
    conflicts = [p for p in targets if p.exists() and not force]
    if conflicts:
        print("[ERROR] Existing files would be overwritten. Re-run with --force.")
        for item in conflicts:
            print(f"  - {item.relative_to(project_root)}")
        return 1

    for rel_path, content in GENERATED_FILES.items():
        target = project_root / rel_path
        write_text_file(target, render_generated_file(content, project_root))
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
        # Default safe mode.
        mode_apply = False

    project_root = Path(args.project_root).resolve()
    source_docs = (
        Path(args.source_docs).resolve()
        if args.source_docs
        else (project_root / "doc").resolve()
    )

    if not project_root.exists():
        return fail(f"Project root not found: {project_root}")
    if not source_docs.exists():
        return fail(f"Source docs directory not found: {source_docs}")

    ok, missing = ensure_source_docs(source_docs)
    if not ok:
        print("[ERROR] Missing required source files under doc directory:")
        for name in missing:
            print(f"  - {name}")
        return 1

    lock_file = project_root / ".spec-bootstrap.lock"
    if lock_file.exists() and not args.reinit:
        return fail("Lock exists. Use --reinit to run initialization again.")

    targets = gather_targets(project_root)
    print_plan(project_root, source_docs, targets, args.force)

    if not mode_apply:
        print("[DRY-RUN] No file written.")
        return 0

    return apply_changes(project_root, source_docs, targets, args.force)


if __name__ == "__main__":
    sys.exit(main())
