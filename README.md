# bingo-spec-coding-max-skill

把任意代码仓库初始化为 Spec-Driven Development 结构的 bootstrap kit。

它包含四部分能力：

- `doc/`: 初始化规范、分类提示词、任务生成提示词、示例
- `skills/bingo-spec-coding-max-skill/`: 手动触发的 Skill 定义
- `skills/bingo-spec-coding-max-skill/scripts/`: 跨平台初始化脚本
- 生成产物：项目级 `AGENTS.md` 与 `spec/` 目录骨架

这个项目的目标不是只提供一段 prompt，而是提供一套可落地的初始化入口，让后续 AI 开发流程能够围绕统一的 `Context -> Plan -> Spec -> Tasks -> Code` 结构运行。

## 产品定位

本仓库定位为：

一个用于初始化 Spec 驱动协作规范的 bootstrap kit。

初始化完成后，目标仓库应具备：

- 一个项目级 `AGENTS.md`
- 一个统一入口 `spec/INDEX.md`
- 一组可复用的模板与 prompts
- 一套明确的变更分级和人类门禁规则

## 适用场景

- 新仓库希望从一开始就采用 Spec 驱动协作
- 现有仓库希望补齐 AI 可读的规范骨架
- 团队希望统一 Codex / GPT / Claude 的工作入口
- 需要把高风险改动与低风险改动区分处理

## 当前仓库结构

- `doc/`: 初始化输入文档
- `skills/bingo-spec-coding-max-skill/`: Skill 定义与跨平台初始化脚本

## 变更分级

本项目使用两层表达：

- 流程分级：`L1 | L2 | L3`
- 质量门禁类型：`FEATURE | SMALL_CHANGE | BUG_FIX`

默认映射关系：

- `L1 -> FEATURE`
- `L2 -> SMALL_CHANGE`，若是纯缺陷修复也可归入 `BUG_FIX`
- `L3 -> BUG_FIX`

### L1 Feature Change

适用范围：

- 新功能
- 新 API
- 新模块
- 数据库 schema 变更
- 重要业务逻辑变更

默认流程：

`Context -> Plan -> Spec -> Tasks -> Code`

### L2 Small Change

适用范围：

- 普通 bug fix
- 校验规则修正
- 日志改进
- 范围有限的行为调整

默认流程：

`Tasks -> Code`

### L3 Hotfix

适用范围：

- 生产故障
- 安全问题
- 紧急关键缺陷

默认流程：

`Patch Proposal -> Code`

## 人类门禁

本项目明确要求：AI 不能只靠分级自动一路执行到代码提交，不同等级必须在不同阶段暂停，等待人类确认。

### L1 的人类介入时机

必须介入 3 次：

- `Plan` 完成后确认：确认方向、边界、影响范围
- `Spec` 完成后确认：确认需求、约束、验收标准
- `Tasks` 完成后确认：确认实施顺序、拆分粒度、测试范围

允许进入编码的前提：

- `Plan` 已确认
- `Spec` 已确认
- `Tasks` 已确认

不应跳过上述任一门禁直接编码。

### L2 的人类介入时机

必须介入 1 次：

- `Tasks` 完成后确认：确认变更范围足够小、不会引入架构漂移、验证方式足够明确

允许进入编码的前提：

- 已读取相关 feature spec
- `Tasks` 已确认

如果变更在分析后发现已超出“小改动”边界，应升级为 `L1`。

### L3 的人类介入时机

必须介入 1 次：

- `Patch Proposal` 完成后确认：确认补丁足够小、风险可接受、回滚方式明确

允许进入编码的前提：

- 已定位问题范围
- 最小补丁方案已确认

如果补丁不再是“最小安全修复”，应降速并升级为 `L2` 或 `L1`。

## Skill 触发规则

仅在用户显式提到 `$bingo-spec-coding-max-skill` 时执行。

默认执行方式：

1. 先 `dry-run`
2. 展示将创建或覆盖的文件，包括 `v6` prompt、L1/L2/L3 模板与 `spec/features/` 骨架
3. 获得确认后再 `apply`

## 作为 Codex 技能接入现有项目

这里的目标不是把当前仓库当作业务项目打开，而是把 `bingo-spec-coding-max-skill` 安装为 Codex 的本地技能，然后在任意现有项目中显式触发它。

### 接入模型

推荐使用两层结构：

- 技能仓库：保存 `skills/bingo-spec-coding-max-skill/` 的定义、脚本和维护版本
- 目标项目：提供待初始化的代码仓库、`doc/` 输入文件，以及最终生成的 `AGENTS.md` 和 `spec/`

这样做的好处是：

- 技能可以集中维护和升级
- 初始化结果会写入目标项目，而不是写回技能仓库
- 同一个技能可以复用到多个项目

### 安装到 Codex

建议优先使用仓库自带的一步式脚本，它会同时完成：

- 安装 `bingo-spec-coding-max-skill` 到 `$CODEX_HOME/skills/`
- 将 `doc/` 输入模板复制到目标项目

macOS / Linux:

```bash
bash ./skills/bingo-spec-coding-max-skill/scripts/setup_codex_skill_for_project.sh --target-project /path/to/your-project
```

Windows:

```powershell
powershell -ExecutionPolicy Bypass -File .\skills\bingo-spec-coding-max-skill\scripts\setup_codex_skill_for_project.ps1 -TargetProject C:\path\to\your-project
```

如果你只想单独安装 skill，再使用下方安装脚本。

macOS / Linux:

```bash
bash ./skills/bingo-spec-coding-max-skill/scripts/install_codex_skill.sh
```

Windows:

```powershell
powershell -ExecutionPolicy Bypass -File .\skills\bingo-spec-coding-max-skill\scripts\install_codex_skill.ps1
```

默认安装模式：

- macOS / Linux 默认使用 `symlink`
- Windows 默认使用 `copy`
- 默认 `CODEX_HOME` 为 `~/.codex`，如果环境变量未设置也可直接运行

可选安装参数：

- macOS / Linux: `--mode symlink|copy --force`
- Windows: `-Mode symlink|copy -Force`

如果你希望手动安装，也可以直接把 skill 放到 `$CODEX_HOME/skills/`。

macOS / Linux:

```bash
mkdir -p "$CODEX_HOME/skills"
ln -s "/path/to/bingo-spec-coding-max-skill/skills/bingo-spec-coding-max-skill" "$CODEX_HOME/skills/bingo-spec-coding-max-skill"
```

如果你不想使用软链接，也可以直接复制：

```bash
mkdir -p "$CODEX_HOME/skills"
cp -R "/path/to/bingo-spec-coding-max-skill/skills/bingo-spec-coding-max-skill" "$CODEX_HOME/skills/bingo-spec-coding-max-skill"
```

安装完成后，Codex 会把它视为一个本地技能，名称为 `$bingo-spec-coding-max-skill`。

### 目标项目需要准备什么

在现有项目中，至少准备一个 `doc/` 目录，并放入以下输入文件：

```text
doc/
  spec_bootstrap_prompt_v6.md
  change_classifier.prompt.md
  generate_feature_tasks.prompt.md
  generate_change_tasks.prompt.md
  usage_examples.md
```

推荐做法有两种：

1. 从本仓库复制 `doc/` 到目标项目
2. 由你的团队在目标项目内维护自己的 `doc/` 版本，再复用当前 skill

如果目标项目没有这些文件，初始化脚本会报缺失错误并停止。

如果你只想单独准备目标项目，也可以使用准备脚本：

macOS / Linux:

```bash
bash ./skills/bingo-spec-coding-max-skill/scripts/prepare_target_project.sh --target-project /path/to/your-project
```

Windows:

```powershell
powershell -ExecutionPolicy Bypass -File .\skills\bingo-spec-coding-max-skill\scripts\prepare_target_project.ps1 -TargetProject C:\path\to\your-project
```

如果目标项目里已经存在 `doc/` 文件并且你确认要覆盖：

- macOS / Linux: 追加 `--force`
- Windows: 追加 `-Force`

这个脚本只负责把初始化输入模板写入目标项目，不会执行 spec 初始化。

### 在目标项目中如何触发

1. 用 Codex 打开目标项目根目录
2. 确认当前工作目录就是目标项目，而不是技能仓库
3. 如果还没准备 `doc/`，先运行准备脚本
4. 显式输入：

```text
请执行 $bingo-spec-coding-max-skill，对当前项目先 dry-run，确认后再 apply。
```

Codex 应该按以下方式工作：

- 读取 `$CODEX_HOME/skills/bingo-spec-coding-max-skill/SKILL.md`
- 使用当前项目的 `doc/` 作为输入
- 在当前项目内生成 `AGENTS.md`、`spec/` 和 `.spec-bootstrap.lock`

### 推荐的执行命令

如果 Codex 需要在终端中显式执行脚本，建议使用技能目录下的脚本，但把 `project-root` 指向当前项目。

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

### 接入约束

- 技能目录负责提供能力，不负责保存业务项目输出
- 目标项目必须自行维护 `doc/` 输入内容
- 首次使用必须先 `dry-run`
- 只有在用户确认后才应执行 `apply`
- 已有 `.spec-bootstrap.lock` 时，除非明确要求，否则不应重复初始化

### 端到端示例

下面示例展示如何把当前技能接入一个已存在项目，并在 Codex 中开始使用。

macOS / Linux:

```bash
export CODEX_HOME="$HOME/.codex"

bash ./skills/bingo-spec-coding-max-skill/scripts/setup_codex_skill_for_project.sh --target-project /path/to/existing-project

cd /path/to/existing-project

bash "$CODEX_HOME/skills/bingo-spec-coding-max-skill/scripts/init_spec_repo.sh" --project-root . --dry-run
```

进入 Codex 后可直接输入：

```text
请执行 $bingo-spec-coding-max-skill，对当前项目先 dry-run，确认后再 apply。
```

Windows:

```powershell
$env:CODEX_HOME = "$HOME\.codex"

powershell -ExecutionPolicy Bypass -File .\skills\bingo-spec-coding-max-skill\scripts\setup_codex_skill_for_project.ps1 -TargetProject C:\path\to\existing-project

Set-Location C:\path\to\existing-project

powershell -ExecutionPolicy Bypass -File $env:CODEX_HOME\skills\bingo-spec-coding-max-skill\scripts\init_spec_repo.ps1 --project-root . --dry-run
```

预期结果：

- 目标项目生成 `doc/` 输入模板
- Codex 可识别 `$bingo-spec-coding-max-skill`
- dry-run 会预览 `AGENTS.md`、`spec/`、模板与 prompts
- 确认后可继续执行 `apply`

## 运行方式

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

## 可选参数

- `--project-root <path>`: 目标项目根目录，默认当前目录
- `--source-docs <path>`: 输入文档目录，默认 `<project-root>/doc`
- `--force`: 覆盖已有文件
- `--reinit`: 忽略 lock 重新初始化

## 初始化输出

执行 `--apply` 后，当前脚本会创建或写入：

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

## 初始化后的目录示意

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

其中：

- `spec/templates/PLAN_TEMPLATE.md` 用于 `L1`
- `spec/templates/CHANGE_TEMPLATE.md` 用于 `L2`
- `spec/templates/HOTFIX_TEMPLATE.md` 用于 `L3`
- `spec/features/` 是后续 feature 规格和 change 历史的根目录

## 使用示例

### 手动触发

```text
请执行 $bingo-spec-coding-max-skill，对当前仓库做初始化。先 dry-run，确认后再 apply。
```

### 分级示例

1. `L1`: 新增登录功能，先做 `Plan -> Spec -> Tasks`，每阶段等待确认，再进入编码。
2. `L2`: 修复密码校验缺陷，先生成变更任务，确认后再编码。
3. `L3`: 修复生产环境令牌故障，先提出最小补丁方案，确认后再编码。

详细示例见：

- `doc/usage_examples.md`
- `spec/usage/usage_examples.md`，初始化后生成
