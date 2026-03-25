---
name: bingo-spec-coding-max-skill
description: 初始化专用技能。仅在用户显式输入 `$bingo-spec-coding-max-skill` 时使用。将项目初始化为 Spec 驱动结构，创建 AGENTS.md、spec 目录及模板，并把 doc 目录下的提示词与示例注入到 spec/prompts 与 spec/usage。支持中文或英文 spec 环境，默认中文。支持 Windows 与 macOS，默认 dry-run，使用 --apply 才落地。
---

# bingo-spec-coding-max-skill

仅在用户明确手动触发 `$bingo-spec-coding-max-skill` 时执行。

## 执行规则

1. 默认先执行 dry-run，先展示将创建或覆盖的文件。
2. 仅在用户明确确认后执行 apply。
3. 检测到 `.spec-bootstrap.lock` 时停止并提示使用 `--reinit` 或 `--upgrade`。
4. 已存在文件默认不覆盖，除非传 `--force`。
5. 对已初始化项目做规范重建时，优先使用 `--upgrade`，它等价于 `--reinit --force`。
6. 初始化时会自动生成仓库级 `SPEC_CONTEXT` 初稿，支持 Java / Frontend / Python / 混合仓库；不确定信息保留为“待确认”。
7. 注入的分级规则采用三轴输出：`Requested Level / Final Level / Change Type / Doc Mode`，并新增 `L0` 问题分析通道，同时内置外部契约强制 `L1`、无既有 spec 禁止直接 `L2`、`L3` 仅限最小安全补丁等规则。
8. 在目标项目内手动触发 skill 时，先自动执行 Python 同步脚本刷新当前项目的 `doc/`；若当前项目已有 `doc/`，先清空后重拷贝，再进入 `dry-run` 初始化。

dry-run 预览应覆盖：

- `AGENTS.md`
- `spec/INDEX.md`
- `spec/templates/PLAN_TEMPLATE.md`
- `spec/templates/SPEC_TEMPLATE.md`
- `spec/templates/QUESTION_TEMPLATE.md`
- `spec/templates/TASK_TEMPLATE.md`
- `spec/templates/CHANGE_TEMPLATE.md`
- `spec/templates/HOTFIX_TEMPLATE.md`
- `spec/prompts/*`
- `spec/questions/`
- `spec/features/`

初始化后的需求文档约定：

- `L0` 如需保留问题记录，可写入 `spec/questions/<date>-<topic>.md`
- `L1` 文档写入 `spec/features/<feature-name>/`
- `L2` 文档写入 `spec/features/<feature-name>/smallchange/`
- `L3` 文档写入 `spec/features/<feature-name>/hotfix/`
- 创建 feature 目录时，同时建立 `smallchange/` 与 `hotfix/`

## 运行入口

Windows:

```powershell
powershell -ExecutionPolicy Bypass -File .\skills\bingo-spec-coding-max-skill\scripts\init_spec_repo.ps1 --dry-run -Language zh
powershell -ExecutionPolicy Bypass -File .\skills\bingo-spec-coding-max-skill\scripts\init_spec_repo.ps1 --apply -Language zh
```

macOS:

```bash
bash ./skills/bingo-spec-coding-max-skill/scripts/init_spec_repo.sh --dry-run --language zh
bash ./skills/bingo-spec-coding-max-skill/scripts/init_spec_repo.sh --apply --language zh
```

## 输入来源

skill 内置模板位于 `skills/bingo-spec-coding-max-skill/resources/doc/`。

手动触发时，先把内置模板同步到项目根目录 `doc/<language>/`，再从当前项目的 `doc/` 读取以下文件并注入：

1. `spec_bootstrap_prompt_v6.md`（初始化流程提示词）
2. `change_classifier.prompt.md`
3. `generate_question_answer.prompt.md`
4. `generate_feature_tasks.prompt.md`
5. `generate_change_tasks.prompt.md`
6. `usage_examples.md`

默认语言参数为 `zh`，可切换为 `en`。

若目录不同，使用 `--source-docs <path>` 指定；若该目录本身没有平铺文件，脚本会继续尝试读取其下的 `zh/` 或 `en/` 子目录。

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

如果对已接入项目执行升级刷新：

- 传 `--upgrade-skill` 或 `-UpgradeSkill`
- 会先删除目标项目原有 `doc/`
- 会清除目标项目现有 `spec/`、`AGENTS.md`、`.spec-bootstrap.lock`
- 然后重新复制最新 `doc/`
- 最后要求在目标项目内重新执行初始化，重新生成整套 spec 体系

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

技能升级命令：

macOS / Linux:

```bash
bash ./skills/bingo-spec-coding-max-skill/scripts/install_codex_skill.sh --upgrade
```

Windows:

```powershell
powershell -ExecutionPolicy Bypass -File .\skills\bingo-spec-coding-max-skill\scripts\install_codex_skill.ps1 -Upgrade
```

技能安装后，应在目标项目内触发，而不是在技能仓库内触发。

目标项目要求：

1. 当前工作目录是目标项目根目录
2. 直接手动触发 `$bingo-spec-coding-max-skill`
3. skill 会先自动刷新当前项目的 `doc/`
4. 默认先执行 dry-run
5. 用户确认后再执行 apply
6. 若未显式指定，初始化语言默认为中文

macOS / Linux:

```bash
bash "$CODEX_HOME/skills/bingo-spec-coding-max-skill/scripts/init_spec_repo.sh" --project-root . --dry-run
bash "$CODEX_HOME/skills/bingo-spec-coding-max-skill/scripts/init_spec_repo.sh" --project-root . --apply
```

Windows:

```powershell
powershell -ExecutionPolicy Bypass -File $env:CODEX_HOME\skills\bingo-spec-coding-max-skill\scripts\init_spec_repo.ps1 --project-root . --dry-run -Language zh
powershell -ExecutionPolicy Bypass -File $env:CODEX_HOME\skills\bingo-spec-coding-max-skill\scripts\init_spec_repo.ps1 --project-root . --apply -Language zh
```

如果目标项目已经初始化过，想重新生成 spec 规范：

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
