# bingo-spec-coding-max-skill

#### English | [简体中文](./README_CN.md)

![Spec Driven](https://img.shields.io/badge/Spec-Driven-blue)
![Workflow](https://img.shields.io/badge/Workflow-Context%20%E2%86%92%20Plan%20%E2%86%92%20Spec%20%E2%86%92%20Tasks%20%E2%86%92%20Code-0A7)
![Platforms](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-444)

Bootstrap kit that turns any repository into a Spec-Driven Development workspace.

> A practical bootstrap entry for teams that want consistent AI collaboration, explicit quality gates, and repeatable delivery flow.
>
> Core idea: help projects move from vibe coding to spec coding in a simple, low-friction way instead of adding cognitive burden for developers.

## Docs

- [Quick Start](#quick-start)
- [Choose By Scenario](#choose-by-scenario)
- [Change Classification](#change-classification)
- [Human Gates](#human-gates)
- [Install as a Codex Skill](#install-as-a-codex-skill-for-existing-projects)
- [Initialization Output](#initialization-output)
- [Examples](#examples)
- [License](#license)

It provides four core parts:

- `skills/bingo-spec-coding-max-skill/resources/doc/`: skill-bundled bootstrap specs, classifier prompts, task-generation prompts, and examples
- `skills/bingo-spec-coding-max-skill/`: manually triggered Skill definition
- `skills/bingo-spec-coding-max-skill/scripts/`: cross-platform bootstrap scripts
- generated outputs: project-level `AGENTS.md` and the `spec/` skeleton

The current version also adds:

- automatic generation of an enhanced repository-level `spec/SPEC_CONTEXT.md`
- auto-detection for `Java`, `Frontend`, `Python`, and mixed repositories
- draft runtime commands, test commands, source roots, core modules, and engineering constraints
- conservative wording for low-confidence signals so inferred details are not presented as hard facts

The goal is not to ship just another prompt. This repository provides a practical initialization entry point so later AI-assisted development can run around a consistent `Context -> Plan -> Spec -> Tasks -> Code` structure while preserving developers' existing vibe coding habits as much as possible.

## Quick Start

If you only want the shortest path to a working setup:

1. install the skill into `$CODEX_HOME/skills/`
2. open the target project root in Codex
3. explicitly trigger `$bingo-spec-coding-max-skill`
4. review the `dry-run` preview, then confirm `apply`

The two most common command paths are:

- first initialization: `--dry-run` -> `--apply`
- upgrade an already initialized project: `--dry-run --upgrade` -> `--apply --upgrade`

## Choose By Scenario

- first time adding the spec system to a project: start with [Install as a Codex Skill](#install-as-a-codex-skill-for-existing-projects)
- project already initialized and you only want the latest rule framework: jump to [Recommended Execution Commands](#recommended-execution-commands) and use `--upgrade`
- project already contains team-authored spec docs: read [How To Handle Existing Spec Docs](#how-to-handle-existing-spec-docs) first
- you want to wipe and rebuild the whole spec system: read the `--upgrade-skill` warning in [How To Handle Existing Spec Docs](#how-to-handle-existing-spec-docs)

## Positioning

This repository is a bootstrap kit for initializing Spec-driven collaboration rules.

At the current stage, it is most accurate to describe it as an initializer plus workflow-framework injector:

- it injects a consistent spec structure, prompts, templates, and approval gates into the target repository
- it provides `L0/L1/L2/L3` classification rules for the target project
- it provides default workflow templates and entry conventions for each level

The intended outcome is:

- developers provide a broad request in their usual style
- the initialized target project uses `AGENTS.md`, `SPEC_WORKFLOW.md`, and prompts to decide whether the work is `L0`, `L1`, `L2`, or `L3`
- the initialized target project then routes the request into the correct `Answer / Plan / Spec / Tasks / Patch Proposal`
- the transition stays simple and lightweight instead of interrupting existing vibe coding habits

After initialization, the target repository should have:

- a project-level `AGENTS.md`
- a single entrypoint at `spec/INDEX.md`
- an explicit binding from `AGENTS.md` into the spec tree through `spec/INDEX.md`
- reusable templates and prompts
- explicit request classification and human-gate rules

## Use Cases

- new repositories that want to adopt Spec-driven collaboration from day one
- existing repositories that need an AI-readable spec skeleton
- teams that want a unified operating entry for Codex / GPT / Claude
- workflows that need to separate high-risk changes from low-risk changes
- repositories that want a usable first draft of `SPEC_CONTEXT` for Java / Frontend / Python stacks
- mixed-stack repositories that want a multi-stack context draft before Plan / Spec / Tasks work starts

## Current Repository Layout

- `skills/bingo-spec-coding-max-skill/resources/doc/`: skill-bundled bootstrap input documents
- `skills/bingo-spec-coding-max-skill/`: Skill definition and cross-platform bootstrap scripts

## Change Classification

The current version upgrades classification to three axes:

- `Workflow Level`: `L0 | L1 | L2 | L3`
- `Change Type`: `QUESTION | FEATURE | SMALL_CHANGE | BUG_FIX`
- `Doc Mode`: `QUESTION_RECORD | FULL_SPEC | CHANGE_RECORD | HOTFIX_RECORD`

Before planning, task generation, or coding, the initialized project is expected to output:

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

Hard rules:

- if the request is explanation, analysis, investigation, or option comparison without a direct implementation ask, prefer `L0 + QUESTION_RECORD`
- external contract changes must be at least `L1 + FULL_SPEC`
- do not use `L2` unless a reusable feature spec already exists
- `L3` is only for the smallest safe patch
- explicitly requested levels may raise conservatism, but may not bypass hard rules
- `L1 / L2 / L3` must generate concrete `.md` documents first, and coding or implementation-driving commands may continue only after user confirmation and a manual go-ahead
- `L0` does not require a question document first; if analysis makes implementation clearly necessary, it may escalate directly to `L1`, `L2`, or `L3`

Default mapping:

- `L0 -> QUESTION + QUESTION_RECORD`
- `L1 -> FEATURE + FULL_SPEC`
- `L2 -> SMALL_CHANGE/BUG_FIX + CHANGE_RECORD`
- `L3 -> BUG_FIX + HOTFIX_RECORD`

## Human Gates

This project explicitly requires human confirmation at defined checkpoints for `L1`, `L2`, and `L3`. AI must not classify those changes and continue all the way to code commit without stopping at the required stage.
`L0` does not have an extra human gate. It may end after analysis, or escalate and continue when implementation is clearly needed.

### Human Checkpoints for L0

`L0` is for clarification, investigation, explanation, or option comparison without making the question record itself a hard gate.

Execution is:

- if the work stays analysis-only, finish the `Answer` and stop there
- if the result should move into implementation, reclassify directly into `L1`, `L2`, or `L3`
- if a durable record is useful, optionally save `spec/questions/<date>-<topic>.md`

### Human Checkpoints for L1

One checkpoint is mandatory:

- confirm after `Tasks`: by this point `Plan`, `Spec`, and `Tasks` must all exist, and the user confirms direction, requirements, constraints, acceptance criteria, implementation order, task granularity, and test scope in one pass

Coding may start only when:

- `Tasks` is confirmed
- `spec/features/<feature-name>/plan.md`, `spec/features/<feature-name>/spec.md`, and `spec/features/<feature-name>/tasks.md` exist as concrete files
- the user has manually told the agent to continue

Do not skip any of these gates.

### Human Checkpoints for L2

One checkpoint is mandatory:

- confirm after `Tasks`: verify the change is still small, does not introduce architecture drift, and has a clear validation approach

Coding may start only when:

- the related feature spec has been read
- `Tasks` is confirmed
- `spec/features/<feature-name>/smallchange/<date>-<change-name>.md` or an equivalent change-record `.md` exists as a concrete file
- the user has manually told the agent to continue

If analysis shows the change is no longer small, or there is no reusable feature spec at all, escalate it to `L1`.

### Human Checkpoints for L3

One checkpoint is mandatory:

- confirm after `Patch Proposal`: verify the patch is minimal, risk is acceptable, and rollback is clear

Coding may start only when:

- the failure scope is located
- the minimal patch is confirmed
- `spec/features/<feature-name>/hotfix/<date>-<hotfix-name>.md` or an equivalent patch-proposal `.md` exists as a concrete file
- the user has manually told the agent to continue

If the patch is no longer the smallest safe fix, slow down and escalate to `L2` or `L1`.

## Skill Trigger Rule

Run this skill only when the user explicitly mentions `$bingo-spec-coding-max-skill`.

Default execution flow:

1. run `dry-run`
2. show which files will be created or overwritten, including the `v6` prompt, `L0/L1/L2/L3` templates, `spec/questions/`, and the `spec/features/` skeleton
3. run `apply` only after confirmation

## Install as a Codex Skill for Existing Projects

The goal here is not to open this repository as a business project. Instead, install `bingo-spec-coding-max-skill` as a local Codex skill and trigger it explicitly inside any existing repository.

### Integration Model

Recommended two-layer structure:

- skill repository: stores `skills/bingo-spec-coding-max-skill/`, scripts, and versioned maintenance
- target project: stores the repository to initialize, the `doc/` inputs, and the generated `AGENTS.md` and `spec/`

Benefits:

- the skill can be maintained and upgraded centrally
- initialization writes into the target project, not back into the skill repository
- the same skill can be reused across multiple projects

### Install into Codex

The recommended path is now simple:

1. install `bingo-spec-coding-max-skill` into `$CODEX_HOME/skills/`
2. open the target project in Codex
3. directly trigger `$bingo-spec-coding-max-skill` inside the target project

After the trigger, the skill automatically refreshes the current project's `doc/` and then starts the `dry-run` initialization flow.

Install command:

macOS / Linux:

```bash
bash ./skills/bingo-spec-coding-max-skill/scripts/install_codex_skill.sh
```

Windows:

```powershell
powershell -ExecutionPolicy Bypass -File .\skills\bingo-spec-coding-max-skill\scripts\install_codex_skill.ps1
```

Default install mode:

- macOS / Linux defaults to `symlink`
- Windows defaults to `copy`
- default `CODEX_HOME` is `~/.codex` if the environment variable is not set

Optional install flags:

- macOS / Linux: `--mode symlink|copy --force --upgrade`
- Windows: `-Mode symlink|copy -Force -Upgrade`

If you only want to upgrade the skill files already installed into Codex:

macOS / Linux:

```bash
bash ./skills/bingo-spec-coding-max-skill/scripts/install_codex_skill.sh --upgrade
```

Windows:

```powershell
powershell -ExecutionPolicy Bypass -File .\skills\bingo-spec-coding-max-skill\scripts\install_codex_skill.ps1 -Upgrade
```

If you want a manual install, place the skill directly under `$CODEX_HOME/skills/`.

macOS / Linux:

```bash
mkdir -p "$CODEX_HOME/skills"
ln -s "/path/to/bingo-spec-coding-max-skill/skills/bingo-spec-coding-max-skill" "$CODEX_HOME/skills/bingo-spec-coding-max-skill"
```

If you do not want a symlink, copy it instead:

```bash
mkdir -p "$CODEX_HOME/skills"
cp -R "/path/to/bingo-spec-coding-max-skill/skills/bingo-spec-coding-max-skill" "$CODEX_HOME/skills/bingo-spec-coding-max-skill"
```

After installation, Codex recognizes it as a local skill named `$bingo-spec-coding-max-skill`.

### What the Target Project Must Provide

The target project does not need manual `doc/` preparation. When you manually trigger the skill, it deletes the current project's existing `doc/` first and then syncs the latest template set.

After sync, the target project's `doc/` layout is:

```text
doc/
  zh/
    spec_bootstrap_prompt_v6.md
    change_classifier.prompt.md
    generate_question_answer.prompt.md
    generate_feature_tasks.prompt.md
    generate_change_tasks.prompt.md
    usage_examples.md
  en/
    spec_bootstrap_prompt_v6.md
    change_classifier.prompt.md
    generate_question_answer.prompt.md
    generate_feature_tasks.prompt.md
    generate_change_tasks.prompt.md
    usage_examples.md
```

Initialization defaults to Chinese and reads `doc/zh/`. When English is selected, it reads `doc/en/`. For backward compatibility, the script still falls back to flat `doc/*.md` files.

If you want to refresh `doc/` outside Codex, you can still run `sync_skill_docs.py` manually, but that is no longer required for the normal path.

### How to Trigger It in the Target Project

1. open the target project root in Codex
2. make sure the current working directory is the target project, not the skill repository
3. explicitly enter:

```text
Please run $bingo-spec-coding-max-skill for the current project. Start with dry-run, then apply after confirmation.
```

Codex should:

- read `$CODEX_HOME/skills/bingo-spec-coding-max-skill/SKILL.md`
- automatically run `sync_skill_docs.py` first to refresh the current project's `doc/`
- use the current project's `doc/` as input
- generate `AGENTS.md`, `spec/`, and `.spec-bootstrap.lock` inside the current project

### Recommended Execution Commands

If Codex needs to call scripts from the terminal, use the scripts under the skill directory and point `project-root` to the current project. The equivalent command order is:

Common choices:

- first initialization: use the first `--dry-run` / `--apply` pair below
- upgrade an already initialized project: use the second command pair with `--upgrade`
- important existing `spec` docs in the project: do not jump straight to `apply --upgrade`; inspect the preview first and read [How To Handle Existing Spec Docs](#how-to-handle-existing-spec-docs)

macOS / Linux:

```bash
bash "$CODEX_HOME/skills/bingo-spec-coding-max-skill/scripts/init_spec_repo.sh" --project-root . --dry-run --language zh
bash "$CODEX_HOME/skills/bingo-spec-coding-max-skill/scripts/init_spec_repo.sh" --project-root . --apply --language zh
```

Windows:

```powershell
powershell -ExecutionPolicy Bypass -File $env:CODEX_HOME\skills\bingo-spec-coding-max-skill\scripts\init_spec_repo.ps1 --project-root . --dry-run -Language zh
powershell -ExecutionPolicy Bypass -File $env:CODEX_HOME\skills\bingo-spec-coding-max-skill\scripts\init_spec_repo.ps1 --project-root . --apply -Language zh
```

If the project has already been initialized and you want to regenerate the spec scaffold:

macOS / Linux:

```bash
bash "$CODEX_HOME/skills/bingo-spec-coding-max-skill/scripts/init_spec_repo.sh" --project-root . --dry-run --upgrade --language zh
bash "$CODEX_HOME/skills/bingo-spec-coding-max-skill/scripts/init_spec_repo.sh" --project-root . --apply --upgrade --language zh
```

Windows:

```powershell
powershell -ExecutionPolicy Bypass -File $env:CODEX_HOME\skills\bingo-spec-coding-max-skill\scripts\init_spec_repo.ps1 --project-root . --dry-run -Upgrade -Language zh
powershell -ExecutionPolicy Bypass -File $env:CODEX_HOME\skills\bingo-spec-coding-max-skill\scripts\init_spec_repo.ps1 --project-root . --apply -Upgrade -Language zh
```

If the skill was just upgraded, or the project has already been initialized before, simply trigger `$bingo-spec-coding-max-skill` again. The skill refreshes `doc/` first and then runs the new initialization preview.

### How To Handle Existing Spec Docs

If the target project already contains team-maintained `spec/` documents, do not default to a full wipe-and-rebuild.

Prefer this safer path first:

- run `dry-run --upgrade` to inspect which bootstrap-managed files would be replaced
- run `apply --upgrade` only after that preview looks correct
- keep team-authored business documents under `spec/features/` or `spec/questions/` when possible, instead of reusing bootstrap framework file names

Please distinguish these two upgrade paths:

- `--upgrade`
  - used for upgrading the rule framework in an already initialized project
  - equivalent to `--reinit --force`
  - mainly overwrites bootstrap-managed files such as `AGENTS.md`, `spec/INDEX.md`, `spec/SPEC_WORKFLOW.md`, `spec/templates/*`, `spec/prompts/*`, and `spec/usage/usage_examples.md`
  - best when you want to keep existing business spec docs and only refresh the framework

- `--upgrade-skill`
  - used by the setup script for a full refresh
  - clears the target project's `doc/`, `spec/`, `AGENTS.md`, and `.spec-bootstrap.lock`
  - best when you intend to rebuild the spec system from scratch
  - back up important spec documents first

Conservative recommendation:

- valuable existing spec docs: use `dry-run --upgrade` first
- messy existing spec docs and a planned reset: back up first, then consider `--upgrade-skill`

Interaction example:

Assume the target project already contains:

- `spec/features/auth-login/spec.md`
- `spec/features/auth-login/tasks.md`
- `spec/features/auth-login/smallchange/2026-03-01-trim-password-input.md`

You only want to upgrade the project to the latest skill rules and keep those business-owned spec docs.

User:

```text
Please upgrade the current project to the latest bingo-spec-coding-max-skill rule set, but do not overwrite anything yet. The project already has documents under spec/features/auth-login/, and I want to confirm those business spec files will not be wiped.
```

What the agent should do first:

```text
Run dry-run --upgrade first and inspect which bootstrap-managed files would be replaced before applying anything.
```

What the agent should report after dry-run:

```text
The preview mainly updates rule-framework files such as:
- AGENTS.md
- spec/INDEX.md
- spec/SPEC_WORKFLOW.md
- spec/CHANGE_POLICY.md
- spec/templates/*
- spec/prompts/*
- spec/usage/usage_examples.md

At this stage, there is no signal that spec/features/auth-login/spec.md, tasks.md, or the smallchange history files need to be cleared directly.

If your goal is only to refresh the rule framework, I can continue with apply --upgrade next.
```

User confirmation:

```text
Yes, continue with apply --upgrade, but keep the existing auth-login business spec docs.
```

What the agent should say after apply:

```text
The bootstrap-managed framework files were refreshed in upgrade mode.
The existing business-owned documents were kept in place:
- spec/features/auth-login/spec.md
- spec/features/auth-login/tasks.md
- spec/features/auth-login/smallchange/2026-03-01-trim-password-input.md

This update refreshed the rule framework, templates, prompts, AGENTS.md, and index/policy files.
If you later want a full rebuild, we should evaluate --upgrade-skill separately.
```

### Integration Constraints

- the skill directory provides capability, but should not store business project outputs
- the skill refreshes the target project's `doc/` inputs automatically
- the first run must start with `dry-run`
- `apply` should run only after explicit user confirmation
- if `.spec-bootstrap.lock` already exists, do not reinitialize unless explicitly requested

### End-to-End Example

The example below shows how to install this skill into an existing project and start using it in Codex.

macOS / Linux:

```bash
export CODEX_HOME="$HOME/.codex"

bash ./skills/bingo-spec-coding-max-skill/scripts/install_codex_skill.sh

cd /path/to/existing-project
```

Inside Codex, you can then enter:

```text
Please run $bingo-spec-coding-max-skill for the current project. Start with dry-run, then apply after confirmation.
```

Windows:

```powershell
$env:CODEX_HOME = "$HOME\.codex"

powershell -ExecutionPolicy Bypass -File .\skills\bingo-spec-coding-max-skill\scripts\install_codex_skill.ps1

Set-Location C:\path\to\existing-project
```

Expected result:

- the skill automatically refreshes the target project's `doc/` input templates
- Codex can recognize `$bingo-spec-coding-max-skill`
- `dry-run` previews `AGENTS.md`, `spec/`, templates, and prompts
- after confirmation, `apply` can continue

## Usage

### Windows (PowerShell)

```powershell
powershell -ExecutionPolicy Bypass -File .\skills\bingo-spec-coding-max-skill\scripts\init_spec_repo.ps1 --dry-run
powershell -ExecutionPolicy Bypass -File .\skills\bingo-spec-coding-max-skill\scripts\init_spec_repo.ps1 --apply
```

### macOS (bash)

```bash
bash ./skills/bingo-spec-coding-max-skill/scripts/init_spec_repo.sh --dry-run
bash ./skills/bingo-spec-coding-max-skill/scripts/init_spec_repo.sh --apply
```

## Optional Flags

- `--project-root <path>`: target project root, default is current directory
- `--source-docs <path>`: input document directory, default is `<project-root>/doc`
- `--language <zh|en>`: choose Chinese or English spec scaffolding, default is `zh`
- `--force`: overwrite existing files
- `--reinit`: ignore lock file and reinitialize
- `--upgrade`: upgrade an existing spec bootstrap, equivalent to `--reinit --force`

## Initialization Output

Running `--apply` creates or writes:

- `AGENTS.md`
- `spec/INDEX.md`
- `spec/SPEC_CONTEXT.md`
- `spec/SPEC_WORKFLOW.md`
- `spec/CHANGE_POLICY.md`
- `spec/templates/PLAN_TEMPLATE.md`
- `spec/templates/SPEC_TEMPLATE.md`
- `spec/templates/TASK_TEMPLATE.md`
- `spec/templates/CHANGE_TEMPLATE.md`
- `spec/templates/HOTFIX_TEMPLATE.md`
- `spec/prompts/*.md`
- `spec/usage/usage_examples.md`
- `.spec-bootstrap.lock`

`spec/SPEC_CONTEXT.md` is now generated as an enhanced repository-context draft with these fixed sections:

- Repository Summary
- Core Modules
- Runtime And Data Constraints
- Testing And Validation Constraints
- UI And Interface Constraints
- Engineering Constraints
- Domain Constraints
- Non-functional Constraints
- Assumptions And Unknowns

Generation rules:

- high-confidence signals are written directly into the draft, such as build tools, test commands, common source roots, and framework dependencies
- low-confidence signals use conservative wording such as "detected", "potential", "suggested", or "confirmation needed"
- weak-signal repositories fall back gracefully to a minimal context template instead of inventing architecture conclusions

## Resulting Directory Layout

```text
.
├── AGENTS.md
├── spec
│   ├── INDEX.md
│   ├── SPEC_CONTEXT.md
│   ├── SPEC_WORKFLOW.md
│   ├── CHANGE_POLICY.md
│   ├── features
│   │   ├── .gitkeep
│   │   └── auth-login
│   │       ├── plan.md
│   │       ├── spec.md
│   │       ├── tasks.md
│   │       ├── smallchange
│   │       │   └── 2026-03-09-trim-password-input.md
│   │       └── hotfix
│   │           └── 2026-03-09-jwt-validation-patch.md
│   ├── prompts
│   │   ├── spec_bootstrap_prompt_v6.md
│   │   ├── change_classifier.prompt.md
│   │   ├── generate_question_answer.prompt.md
│   │   ├── generate_feature_tasks.prompt.md
│   │   └── generate_change_tasks.prompt.md
│   ├── questions
│   │   └── 2026-03-09-why-login-fails.md
│   ├── templates
│   │   ├── PLAN_TEMPLATE.md
│   │   ├── SPEC_TEMPLATE.md
│   │   ├── QUESTION_TEMPLATE.md
│   │   ├── TASK_TEMPLATE.md
│   │   ├── CHANGE_TEMPLATE.md
│   │   └── HOTFIX_TEMPLATE.md
│   └── usage
│       └── usage_examples.md
└── .spec-bootstrap.lock
```

Where:

- `spec/templates/QUESTION_TEMPLATE.md` is used for `L0`
- `spec/templates/PLAN_TEMPLATE.md` is used for `L1`
- `spec/templates/CHANGE_TEMPLATE.md` is used for `L2`
- `spec/templates/HOTFIX_TEMPLATE.md` is used for `L3`
- `spec/questions/` stores question-analysis and read-only investigation records
- `spec/features/` is the root directory for future feature specs and change history
- `L0` records, when kept, live under `spec/questions/`
- `L1` docs live under `spec/features/<feature-name>/`
- `L2` history lives under `spec/features/<feature-name>/smallchange/`
- `L3` history lives under `spec/features/<feature-name>/hotfix/`

## Examples

### Manual Trigger

```text
Please run $bingo-spec-coding-max-skill to initialize the current repository. Start with dry-run, then apply after confirmation.
```

### Classification Examples

#### Full `L0` Example

How the user asks:

```text
Please help me analyze this first: login keeps failing in the test environment, but I do not want to change code yet. I want to understand whether configuration, token validation, or request parameter handling is the more likely cause.
```

What the agent should output:

```text
Requested Level: AUTO
Final Level: L0
Change Type: QUESTION
Doc Mode: QUESTION_RECORD
Workflow: Context -> Investigation -> Answer
Human Gate: None; if implementation is clearly needed after analysis, escalate to L1, L2, or L3 and continue
Reason: The current goal is analysis and explanation, not implementation, so the request should stay on the L0 question flow first.
Scope Signals: Read-only investigation; compare multiple possible causes; no implementation change requested yet
Escalation Note: If the investigation turns into authentication-flow changes, interface behavior changes, or a concrete patch, escalate to L1, L2, or L3
```

If you want to keep an analysis record, the document goes here:

- `spec/questions/2026-03-09-why-login-fails.md`

1. `L1`: add a login feature. Finish `Plan -> Spec -> Tasks`, confirm once after `Tasks`, then start coding.
2. `L2`: fix password validation. Generate change tasks first, confirm them, then start coding.
3. `L3`: fix a production token failure. Propose the minimal patch first, confirm it, then start coding.

Detailed examples:

- `skills/bingo-spec-coding-max-skill/resources/doc/usage_examples.md`
- `spec/usage/usage_examples.md`, generated after initialization

## License

This project is released under the [MIT License](./LICENSE).

You may use, copy, modify, distribute, and sublicense the repository as long as the original license notice is retained. See [LICENSE](./LICENSE) for the exact terms.
