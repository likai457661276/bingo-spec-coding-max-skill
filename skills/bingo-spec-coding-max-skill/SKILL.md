---
name: bingo-spec-coding-max-skill
description: 初始化专用技能。仅在用户显式输入 `$bingo-spec-coding-max-skill` 时使用。将项目初始化为 Spec 驱动结构，创建 AGENTS.md、spec 目录及模板，并把 doc 目录下的提示词与示例注入到 spec/prompts 与 spec/usage。支持 Windows 与 macOS，默认 dry-run，使用 --apply 才落地。
---

# bingo-spec-coding-max-skill

仅在用户明确手动触发 `$bingo-spec-coding-max-skill` 时执行。

## 执行规则

1. 默认先执行 dry-run，先展示将创建或覆盖的文件。
2. 仅在用户明确确认后执行 apply。
3. 检测到 `.spec-bootstrap.lock` 时停止并提示使用 `--reinit`。
4. 已存在文件默认不覆盖，除非传 `--force`。

dry-run 预览应覆盖：

- `AGENTS.md`
- `spec/INDEX.md`
- `spec/templates/PLAN_TEMPLATE.md`
- `spec/templates/SPEC_TEMPLATE.md`
- `spec/templates/TASK_TEMPLATE.md`
- `spec/templates/CHANGE_TEMPLATE.md`
- `spec/templates/HOTFIX_TEMPLATE.md`
- `spec/prompts/*`
- `spec/features/`

## 运行入口

Windows:

```powershell
powershell -ExecutionPolicy Bypass -File .\skills\bingo-spec-coding-max-skill\scripts\init_spec_repo.ps1 --dry-run
powershell -ExecutionPolicy Bypass -File .\skills\bingo-spec-coding-max-skill\scripts\init_spec_repo.ps1 --apply
```

macOS:

```bash
bash ./skills/bingo-spec-coding-max-skill/scripts/init_spec_repo.sh --dry-run
bash ./skills/bingo-spec-coding-max-skill/scripts/init_spec_repo.sh --apply
```

## 输入来源

默认从项目根目录 `doc/` 读取以下文件并注入：

1. `spec_bootstrap_prompt_v6.md`（初始化流程提示词）
2. `change_classifier.prompt.md`
3. `generate_feature_tasks.prompt.md`
4. `generate_change_tasks.prompt.md`
5. `usage_examples.md`

若目录不同，使用 `--source-docs <path>` 指定。

## 作为 Codex 本地技能使用

推荐将当前目录安装到 `$CODEX_HOME/skills/bingo-spec-coding-max-skill`。

推荐优先使用安装脚本：

一步式接入：

macOS / Linux:

```bash
bash ./skills/bingo-spec-coding-max-skill/scripts/setup_codex_skill_for_project.sh --target-project /path/to/your-project
```

Windows:

```powershell
powershell -ExecutionPolicy Bypass -File .\skills\bingo-spec-coding-max-skill\scripts\setup_codex_skill_for_project.ps1 -TargetProject C:\path\to\your-project
```

如果只想单独安装 skill，再使用下面的安装脚本。

macOS / Linux:

```bash
bash ./skills/bingo-spec-coding-max-skill/scripts/install_codex_skill.sh
```

Windows:

```powershell
powershell -ExecutionPolicy Bypass -File .\skills\bingo-spec-coding-max-skill\scripts\install_codex_skill.ps1
```

默认安装模式：

- macOS / Linux: `symlink`
- Windows: `copy`
- 默认 `CODEX_HOME`: `~/.codex`

技能安装后，应在目标项目内触发，而不是在技能仓库内触发。

目标项目要求：

1. 当前工作目录是目标项目根目录
2. 目标项目存在 `doc/` 输入目录
3. 默认先执行 dry-run
4. 用户确认后再执行 apply

如果目标项目还没有 `doc/` 输入目录，先使用准备脚本：

macOS / Linux:

```bash
bash ./skills/bingo-spec-coding-max-skill/scripts/prepare_target_project.sh --target-project /path/to/your-project
```

Windows:

```powershell
powershell -ExecutionPolicy Bypass -File .\skills\bingo-spec-coding-max-skill\scripts\prepare_target_project.ps1 -TargetProject C:\path\to\your-project
```

macOS / Linux:

```bash
bash "$CODEX_HOME/skills/bingo-spec-coding-max-skill/scripts/init_spec_repo.sh" --project-root . --dry-run
bash "$CODEX_HOME/skills/bingo-spec-coding-max-skill/scripts/init_spec_repo.sh" --project-root . --apply
```

Windows:

```powershell
powershell -ExecutionPolicy Bypass -File $env:CODEX_HOME\skills\bingo-spec-coding-max-skill\scripts\init_spec_repo.ps1 --project-root . --dry-run
powershell -ExecutionPolicy Bypass -File $env:CODEX_HOME\skills\bingo-spec-coding-max-skill\scripts\init_spec_repo.ps1 --project-root . --apply
```
