# bingo-spec-coding-max-skill

#### English | [简体中文](./README_CN.md)

![Spec Driven](https://img.shields.io/badge/Spec-Driven-blue)
![Workflow](https://img.shields.io/badge/Workflow-Context%20%E2%86%92%20Plan%20%E2%86%92%20Spec%20%E2%86%92%20Tasks%20%E2%86%92%20Code-0A7)
![Platforms](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-444)

Bootstrap kit that turns any repository into a Spec-Driven Development workspace.

> A practical bootstrap entry for teams that want consistent AI collaboration, explicit quality gates, and repeatable delivery flow.

## Docs

- [Install as a Codex Skill](#install-as-a-codex-skill-for-existing-projects)
- [Change Classification](#change-classification)
- [Human Gates](#human-gates)
- [Usage](#usage)
- [Examples](#examples)

It provides four core parts:

- `doc/`: bootstrap specs, classifier prompts, task-generation prompts, and examples
- `skills/bingo-spec-coding-max-skill/`: manually triggered Skill definition
- `skills/bingo-spec-coding-max-skill/scripts/`: cross-platform bootstrap scripts
- generated outputs: project-level `AGENTS.md` and the `spec/` skeleton

The current version also adds:

- automatic generation of an enhanced repository-level `spec/SPEC_CONTEXT.md`
- auto-detection for `Java`, `Frontend`, `Python`, and mixed repositories
- draft runtime commands, test commands, source roots, core modules, and engineering constraints
- conservative wording for low-confidence signals so inferred details are not presented as hard facts

The goal is not to ship just another prompt. This repository provides a practical initialization entry point so later AI-assisted development can run around a consistent `Context -> Plan -> Spec -> Tasks -> Code` structure.

## Positioning

This repository is a bootstrap kit for initializing Spec-driven collaboration rules.

After initialization, the target repository should have:

- a project-level `AGENTS.md`
- a single entrypoint at `spec/INDEX.md`
- reusable templates and prompts
- explicit change classification and human-gate rules

## Use Cases

- new repositories that want to adopt Spec-driven collaboration from day one
- existing repositories that need an AI-readable spec skeleton
- teams that want a unified operating entry for Codex / GPT / Claude
- workflows that need to separate high-risk changes from low-risk changes
- repositories that want a usable first draft of `SPEC_CONTEXT` for Java / Frontend / Python stacks
- mixed-stack repositories that want a multi-stack context draft before Plan / Spec / Tasks work starts

## Current Repository Layout

- `doc/`: bootstrap input documents
- `skills/bingo-spec-coding-max-skill/`: Skill definition and cross-platform bootstrap scripts

## Change Classification

This project uses two related expressions:

- process levels: `L1 | L2 | L3`
- quality gate types: `FEATURE | SMALL_CHANGE | BUG_FIX`

Default mapping:

- `L1 -> FEATURE`
- `L2 -> SMALL_CHANGE`, or `BUG_FIX` if it is strictly a defect fix
- `L3 -> BUG_FIX`

### L1 Feature Change

Scope:

- new features
- new APIs
- new modules
- database schema changes
- important business logic changes

Default flow:

`Context -> Plan -> Spec -> Tasks -> Code`

### L2 Small Change

Scope:

- regular bug fixes
- validation rule corrections
- logging improvements
- limited-scope behavior adjustments

Default flow:

`Tasks -> Code`

### L3 Hotfix

Scope:

- production incidents
- security issues
- urgent critical defects

Default flow:

`Patch Proposal -> Code`

## Human Gates

This project explicitly requires human confirmation at defined checkpoints. AI must not classify a change and continue all the way to code commit without stopping at the required stage.

### Human Checkpoints for L1

Three checkpoints are mandatory:

- confirm after `Plan`: direction, boundaries, and impact
- confirm after `Spec`: requirements, constraints, and acceptance criteria
- confirm after `Tasks`: implementation order, task granularity, and test scope

Coding may start only when:

- `Plan` is confirmed
- `Spec` is confirmed
- `Tasks` is confirmed

Do not skip any of these gates.

### Human Checkpoints for L2

One checkpoint is mandatory:

- confirm after `Tasks`: verify the change is still small, does not introduce architecture drift, and has a clear validation approach

Coding may start only when:

- the related feature spec has been read
- `Tasks` is confirmed

If analysis shows the change is no longer small, escalate it to `L1`.

### Human Checkpoints for L3

One checkpoint is mandatory:

- confirm after `Patch Proposal`: verify the patch is minimal, risk is acceptable, and rollback is clear

Coding may start only when:

- the failure scope is located
- the minimal patch is confirmed

If the patch is no longer the smallest safe fix, slow down and escalate to `L2` or `L1`.

## Skill Trigger Rule

Run this skill only when the user explicitly mentions `$bingo-spec-coding-max-skill`.

Default execution flow:

1. run `dry-run`
2. show which files will be created or overwritten, including the `v6` prompt, L1/L2/L3 templates, and the `spec/features/` skeleton
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

Prefer the one-step setup script shipped with this repository. It installs `bingo-spec-coding-max-skill` into `$CODEX_HOME/skills/` and copies the `doc/` input templates into the target project.

macOS / Linux:

```bash
bash ./skills/bingo-spec-coding-max-skill/scripts/setup_codex_skill_for_project.sh --target-project /path/to/your-project
```

Windows:

```powershell
powershell -ExecutionPolicy Bypass -File .\skills\bingo-spec-coding-max-skill\scripts\setup_codex_skill_for_project.ps1 -TargetProject C:\path\to\your-project
```

If you only want the one-step script to upgrade the skill already installed in Codex, without overwriting the target project's `doc/`, add:

- macOS / Linux: `--upgrade-skill`
- Windows: `-UpgradeSkill`

If the skill is already installed and you do not pass `-UpgradeSkill` or `-Force`, the one-step script now skips skill installation and continues preparing the target project.
If the target project's `doc/` already contains input files and you do not pass `-Force`, the one-step script also skips `doc/` preparation and preserves the existing content.

If you only want to install the skill, use the installer below.

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

If you only want to upgrade the skill files already installed into Codex, without overwriting the target project's `doc/` inputs:

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

Inside the existing project, prepare at least a `doc/` directory. Recommended layout:

```text
doc/
  zh/
    spec_bootstrap_prompt_v6.md
    change_classifier.prompt.md
    generate_feature_tasks.prompt.md
    generate_change_tasks.prompt.md
    usage_examples.md
  en/
    spec_bootstrap_prompt_v6.md
    change_classifier.prompt.md
    generate_feature_tasks.prompt.md
    generate_change_tasks.prompt.md
    usage_examples.md
```

Initialization defaults to Chinese and reads `doc/zh/`. When English is selected, it reads `doc/en/`. For backward compatibility, the script still falls back to flat `doc/*.md` files.

Recommended approaches:

1. copy `doc/` from this repository into the target project
2. maintain your own `doc/` version in the target project and reuse the current skill

If the target project does not contain these files, the bootstrap script fails with a missing-input error.

If you only want to prepare the target project, use the preparation script:

macOS / Linux:

```bash
bash ./skills/bingo-spec-coding-max-skill/scripts/prepare_target_project.sh --target-project /path/to/your-project
```

Windows:

```powershell
powershell -ExecutionPolicy Bypass -File .\skills\bingo-spec-coding-max-skill\scripts\prepare_target_project.ps1 -TargetProject C:\path\to\your-project
```

If `doc/` already exists and you want to overwrite it:

- macOS / Linux: add `--force`
- Windows: add `-Force`

This script only writes the bootstrap input templates to the target project. It does not run spec initialization.

### How to Trigger It in the Target Project

1. open the target project root in Codex
2. make sure the current working directory is the target project, not the skill repository
3. if `doc/` is not prepared yet, run the preparation script first
4. explicitly enter:

```text
Please run $bingo-spec-coding-max-skill for the current project. Start with dry-run, then apply after confirmation.
```

Codex should:

- read `$CODEX_HOME/skills/bingo-spec-coding-max-skill/SKILL.md`
- use the current project's `doc/` as input
- generate `AGENTS.md`, `spec/`, and `.spec-bootstrap.lock` inside the current project

### Recommended Execution Commands

If Codex needs to call scripts from the terminal, use the scripts under the skill directory and point `project-root` to the current project.

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

### Integration Constraints

- the skill directory provides capability, but should not store business project outputs
- the target project must maintain its own `doc/` inputs
- the first run must start with `dry-run`
- `apply` should run only after explicit user confirmation
- if `.spec-bootstrap.lock` already exists, do not reinitialize unless explicitly requested

### End-to-End Example

The example below shows how to install this skill into an existing project and start using it in Codex.

macOS / Linux:

```bash
export CODEX_HOME="$HOME/.codex"

bash ./skills/bingo-spec-coding-max-skill/scripts/setup_codex_skill_for_project.sh --target-project /path/to/existing-project

cd /path/to/existing-project

bash "$CODEX_HOME/skills/bingo-spec-coding-max-skill/scripts/init_spec_repo.sh" --project-root . --dry-run
```

Inside Codex, you can then enter:

```text
Please run $bingo-spec-coding-max-skill for the current project. Start with dry-run, then apply after confirmation.
```

Windows:

```powershell
$env:CODEX_HOME = "$HOME\.codex"

powershell -ExecutionPolicy Bypass -File .\skills\bingo-spec-coding-max-skill\scripts\setup_codex_skill_for_project.ps1 -TargetProject C:\path\to\existing-project

Set-Location C:\path\to\existing-project

powershell -ExecutionPolicy Bypass -File $env:CODEX_HOME\skills\bingo-spec-coding-max-skill\scripts\init_spec_repo.ps1 --project-root . --dry-run
```

Expected result:

- the target project gets the `doc/` input templates
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
│   │   └── .gitkeep
│   ├── prompts
│   │   ├── spec_bootstrap_prompt_v6.md
│   │   ├── change_classifier.prompt.md
│   │   ├── generate_feature_tasks.prompt.md
│   │   └── generate_change_tasks.prompt.md
│   ├── templates
│   │   ├── PLAN_TEMPLATE.md
│   │   ├── SPEC_TEMPLATE.md
│   │   ├── TASK_TEMPLATE.md
│   │   ├── CHANGE_TEMPLATE.md
│   │   └── HOTFIX_TEMPLATE.md
│   └── usage
│       └── usage_examples.md
└── .spec-bootstrap.lock
```

Where:

- `spec/templates/PLAN_TEMPLATE.md` is used for `L1`
- `spec/templates/CHANGE_TEMPLATE.md` is used for `L2`
- `spec/templates/HOTFIX_TEMPLATE.md` is used for `L3`
- `spec/features/` is the root directory for future feature specs and change history

## Examples

### Manual Trigger

```text
Please run $bingo-spec-coding-max-skill to initialize the current repository. Start with dry-run, then apply after confirmation.
```

### Classification Examples

1. `L1`: add a login feature. Finish `Plan -> Spec -> Tasks`, wait for confirmation at each stage, then start coding.
2. `L2`: fix password validation. Generate change tasks first, confirm them, then start coding.
3. `L3`: fix a production token failure. Propose the minimal patch first, confirm it, then start coding.

Detailed examples:

- `doc/usage_examples.md`
- `spec/usage/usage_examples.md`, generated after initialization
