# bingo-spec-coding-max-skill

#### [English](./README.md) | 简体中文

![Spec Driven](https://img.shields.io/badge/Spec-Driven-blue)
![Workflow](https://img.shields.io/badge/Workflow-Context%20%E2%86%92%20Plan%20%E2%86%92%20Spec%20%E2%86%92%20Tasks%20%E2%86%92%20Code-0A7)
![Platforms](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-444)

把任意代码仓库初始化为 Spec-Driven Development 结构的 bootstrap kit。

> 一个可落地的初始化入口，用于统一 AI 协作流程、明确质量门禁，并让交付过程可重复。
>
> 项目的核心思想：采用简单无感的方式让项目从 vibe coding 过渡到 spec coding，而不是增加开发者的心智负担。

## 文档导航

- [作为 Codex 技能接入现有项目](#作为-codex-技能接入现有项目)
- [变更分级](#变更分级)
- [人类门禁](#人类门禁)
- [运行方式](#运行方式)
- [使用示例](#使用示例)

它包含四部分能力：

- `skills/bingo-spec-coding-max-skill/resources/doc/`: skill 内置初始化规范、分类提示词、任务生成提示词、示例
- `skills/bingo-spec-coding-max-skill/`: 手动触发的 Skill 定义
- `skills/bingo-spec-coding-max-skill/scripts/`: 跨平台初始化脚本
- 生成产物：项目级 `AGENTS.md` 与 `spec/` 目录骨架

当前版本额外支持：

- 自动生成增强版仓库级 `spec/SPEC_CONTEXT.md`
- 自动识别 `Java`、`Frontend`、`Python` 与混合仓库信号
- 自动补全运行命令、测试命令、源码目录、核心模块与工程约束初稿
- 对低置信度信息保留“待确认”，避免把推断写成确定事实

这个项目的目标不是只提供一段 prompt，而是提供一套可落地的初始化入口，让后续 AI 开发流程能够围绕统一的 `Context -> Plan -> Spec -> Tasks -> Code` 结构运行，并尽量保持开发者原本的 vibe coding 习惯。

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
- 希望为 Java / Frontend / Python 项目自动生成可用的 `SPEC_CONTEXT` 初稿
- 希望在混合仓库中先得到多栈上下文草稿，再进入 Plan / Spec / Tasks

## 当前仓库结构

- `skills/bingo-spec-coding-max-skill/resources/doc/`: skill 内置初始化输入文档
- `skills/bingo-spec-coding-max-skill/`: Skill 定义与跨平台初始化脚本

## 变更分级

当前版本把分级升级为三轴判断：

- `Workflow Level`: `L1 | L2 | L3`
- `Change Type`: `FEATURE | SMALL_CHANGE | BUG_FIX`
- `Doc Mode`: `FULL_SPEC | CHANGE_RECORD | HOTFIX_RECORD`

进入规划、任务拆分或编码前，要求先输出：

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

强制规则：

- 外部契约变更必须至少为 `L1 + FULL_SPEC`
- 没有既有 feature spec，不允许直接走 `L2`
- `L3` 只能用于最小安全补丁
- 用户或开发者显式指定等级只能上调，不能绕过硬规则降级
- `L1 / L2 / L3` 都必须先生成实体 `.md` 文档，待用户确认并手动明确继续后，才能进入编码或执行推进实现的命令

默认映射关系：

- `L1 -> FEATURE + FULL_SPEC`
- `L2 -> SMALL_CHANGE/BUG_FIX + CHANGE_RECORD`
- `L3 -> BUG_FIX + HOTFIX_RECORD`

## 人类门禁

本项目明确要求：AI 不能只靠分级自动一路执行到代码提交，不同等级必须在不同阶段暂停，等待人类确认。
更严格地说，三种等级都必须先把对应的实体 `.md` 文档落地，再等待用户确认并手动明确继续。

### L1 的人类介入时机

必须介入 3 次：

- `Plan` 完成后确认：确认方向、边界、影响范围
- `Spec` 完成后确认：确认需求、约束、验收标准
- `Tasks` 完成后确认：确认实施顺序、拆分粒度、测试范围

允许进入编码的前提：

- `Plan` 已确认
- `Spec` 已确认
- `Tasks` 已确认
- `spec/features/<feature-name>/plan.md`、`spec/features/<feature-name>/spec.md`、`spec/features/<feature-name>/tasks.md` 已实际生成
- 用户已手动明确继续

不应跳过上述任一门禁直接编码。

### L2 的人类介入时机

必须介入 1 次：

- `Tasks` 完成后确认：确认变更范围足够小、不会引入架构漂移、验证方式足够明确

允许进入编码的前提：

- 已读取相关 feature spec
- `Tasks` 已确认
- `spec/features/<feature-name>/smallchange/<date>-<change-name>.md` 或等价变更记录 `.md` 已实际生成
- 用户已手动明确继续

如果变更在分析后发现已超出“小改动”边界，或根本没有可复用的 feature spec，应升级为 `L1`。

### L3 的人类介入时机

必须介入 1 次：

- `Patch Proposal` 完成后确认：确认补丁足够小、风险可接受、回滚方式明确

允许进入编码的前提：

- 已定位问题范围
- 最小补丁方案已确认
- `spec/features/<feature-name>/hotfix/<date>-<hotfix-name>.md` 或等价补丁方案 `.md` 已实际生成
- 用户已手动明确继续

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

推荐的主路径现在很简单：

1. 先把 `bingo-spec-coding-max-skill` 安装到 `$CODEX_HOME/skills/`
2. 用 Codex 打开目标项目
3. 在目标项目里直接手动触发 `$bingo-spec-coding-max-skill`

触发后，skill 会先自动刷新当前项目的 `doc/`，再进入 `dry-run` 初始化。

安装命令：

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

- macOS / Linux: `--mode symlink|copy --force --upgrade`
- Windows: `-Mode symlink|copy -Force -Upgrade`

如果你只想升级已安装到 Codex 的技能文件：

macOS / Linux:

```bash
bash ./skills/bingo-spec-coding-max-skill/scripts/install_codex_skill.sh --upgrade
```

Windows:

```powershell
powershell -ExecutionPolicy Bypass -File .\skills\bingo-spec-coding-max-skill\scripts\install_codex_skill.ps1 -Upgrade
```

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

目标项目不需要手动准备 `doc/`。手动触发 skill 时，它会先删除当前项目已有的 `doc/`，再同步一份最新模板。

同步后的 `doc/` 结构如下：

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

默认初始化语言为中文，即优先读取 `doc/zh/`；传入英文语言参数时读取 `doc/en/`。为了兼容旧版本，脚本仍可回退读取平铺的 `doc/*.md`。

如果你只想脱离 Codex，单独刷新目标项目的 `doc/`，仍可手动执行 `sync_skill_docs.py`，但对正常使用来说不是必需步骤。

### 在目标项目中如何触发

1. 用 Codex 打开目标项目根目录
2. 确认当前工作目录就是目标项目，而不是技能仓库
3. 显式输入：

```text
请执行 $bingo-spec-coding-max-skill，对当前项目先 dry-run，确认后再 apply。
```

Codex 应该按以下方式工作：

- 读取 `$CODEX_HOME/skills/bingo-spec-coding-max-skill/SKILL.md`
- 先自动执行 `sync_skill_docs.py`，刷新当前项目 `doc/`
- 使用当前项目的 `doc/` 作为输入
- 在当前项目内生成 `AGENTS.md`、`spec/` 和 `.spec-bootstrap.lock`

### 推荐的执行命令

如果 Codex 需要在终端中显式执行脚本，建议使用技能目录下的脚本，但把 `project-root` 指向当前项目。等价执行顺序如下：

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

如果项目已经初始化过，想重新生成 spec 规范：

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

如果刚升级过 skill，或目标项目已经初始化过，重新手动触发 `$bingo-spec-coding-max-skill` 即可。skill 会先刷新 `doc/`，然后再走新的初始化预览。

### 接入约束

- 技能目录负责提供能力，不负责保存业务项目输出
- skill 会先自动刷新目标项目 `doc/` 输入内容
- 首次使用必须先 `dry-run`
- 只有在用户确认后才应执行 `apply`
- 已有 `.spec-bootstrap.lock` 时，除非明确要求，否则不应重复初始化

### 端到端示例

下面示例展示如何把当前技能接入一个已存在项目，并在 Codex 中开始使用。

macOS / Linux:

```bash
export CODEX_HOME="$HOME/.codex"

bash ./skills/bingo-spec-coding-max-skill/scripts/install_codex_skill.sh

cd /path/to/existing-project
```

进入 Codex 后可直接输入：

```text
请执行 $bingo-spec-coding-max-skill，对当前项目先 dry-run，确认后再 apply。
```

Windows:

```powershell
$env:CODEX_HOME = "$HOME\.codex"

powershell -ExecutionPolicy Bypass -File .\skills\bingo-spec-coding-max-skill\scripts\install_codex_skill.ps1

Set-Location C:\path\to\existing-project
```

预期结果：

- skill 会自动刷新目标项目 `doc/` 输入模板
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
- `--language <zh|en>`: 指定生成中文或英文 spec 结构，默认 `zh`
- `--force`: 覆盖已有文件
- `--reinit`: 忽略 lock 重新初始化
- `--upgrade`: 用于已初始化项目的规范升级，等价于 `--reinit --force`

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

其中 `spec/SPEC_CONTEXT.md` 会基于当前仓库自动生成增强版初稿，固定包含以下章节：

- 仓库摘要
- 核心模块
- 运行与数据约束
- 测试与验证约束
- UI 与接口约束
- 工程约束
- 领域约束
- 非功能约束
- 假设与未知项

自动生成规则：

- 高置信度信息直接写入初稿，例如构建工具、测试命令、常见源码目录、框架依赖
- 低置信度信息使用“检测到”“推测”“建议关注”“待确认”等保守措辞
- 弱特征仓库会优雅回退到最小上下文模板，不会强行编造架构结论

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
- `L1` 文档固定保存在 `spec/features/<feature-name>/`
- `L2` 历史固定保存在 `spec/features/<feature-name>/smallchange/`
- `L3` 历史固定保存在 `spec/features/<feature-name>/hotfix/`

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

- `skills/bingo-spec-coding-max-skill/resources/doc/usage_examples.md`
- `spec/usage/usage_examples.md`，初始化后生成
