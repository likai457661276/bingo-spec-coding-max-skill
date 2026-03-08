Always respond in Chinese-simplified.

# 项目级 Agent 说明

## 项目定位

本仓库不是业务系统，而是一个用于把其他仓库初始化为 Spec-Driven Development 结构的 bootstrap kit。

核心目标：

- 提供可复用的初始化脚本
- 生成目标项目的 `AGENTS.md` 与 `spec/` 骨架
- 提供中英文 prompts、usage 示例与技能定义
- 让初始化行为可测试、可预览、可审计

## 运行环境

执行前先识别当前环境，再选择对应命令与路径风格：

- Windows：使用 PowerShell 路径与命令习惯
- macOS / Linux：使用 Bash 路径与命令习惯
- 不要把 Unix 命令习惯直接假设到 Windows
- 不要把 Windows 路径分隔符直接假设到 Unix

如果环境判断会影响命令正确性，先确认再执行。

## 仓库结构

- `README.md` / `README_CN.md`：对外说明，分别维护英文与中文文档
- `doc/`：初始化注入源，包含通用文件以及 `doc/zh/`、`doc/en/` 本地化内容
- `skills/bingo-spec-coding-max-skill/SKILL.md`：技能定义与触发约束
- `skills/bingo-spec-coding-max-skill/agents/openai.yaml`：代理入口配置
- `skills/bingo-spec-coding-max-skill/scripts/`：初始化、安装、准备项目等脚本
- `tests/test_init_spec_repo.py`：核心初始化行为测试

## 事实来源

当文档、脚本、测试不一致时，先读下面几处再判断：

1. `skills/bingo-spec-coding-max-skill/scripts/init_spec_repo.py`
2. `tests/test_init_spec_repo.py`
3. `skills/bingo-spec-coding-max-skill/SKILL.md`
4. `README_CN.md` 与 `README.md`

其中：

- `init_spec_repo.py` 是初始化行为的主实现
- `.ps1` 与 `.sh` 更偏平台入口与安装流程
- 测试定义当前应被稳定保障的输出契约

## 修改规则

### 初始化行为变更

如果修改以下内容，必须同步检查脚本、文档、测试是否仍一致：

- 生成文件列表
- 默认语言
- dry-run / apply / force / reinit 语义
- 锁文件行为
- 目标目录结构
- 生成模板内容

涉及初始化输出契约的改动，至少更新：

- `skills/bingo-spec-coding-max-skill/scripts/init_spec_repo.py`
- `tests/test_init_spec_repo.py`
- 必要时更新 `README_CN.md`、`README.md`、`SKILL.md`

### 跨平台脚本变更

若修改安装或准备项目流程，优先保持 PowerShell 与 Bash 入口语义一致：

- `install_codex_skill.ps1` 对应 `install_codex_skill.sh`
- `prepare_target_project.ps1` 对应 `prepare_target_project.sh`
- `setup_codex_skill_for_project.ps1` 对应 `setup_codex_skill_for_project.sh`

如果只能先改一侧，必须在说明中明确另一侧暂未同步。

### 文档与本地化

本仓库同时维护中文与英文内容。修改用户可见说明时：

- 优先同步 `README_CN.md` 与 `README.md`
- 优先同步 `doc/zh/` 与 `doc/en/` 中语义对应的文件
- 如果暂时只更新单语版本，必须明确说明差异是暂时的还是有意保留

### 非源码目录

默认不要编辑以下内容，除非用户明确要求：

- `.idea/`
- `__pycache__/`
- 其他临时产物或本地环境文件

## 执行流程

所有任务遵循：

`INIT -> ANALYSIS -> EXECUTION -> COMPLETED | FAILED | ABORTED`

要求：

- 先分析，再执行
- 不清楚目标项目或宿主环境时，不盲猜
- 优先做小步、可审阅的修改
- 不做无说明的大范围重写

## 安全规则

这是一个会初始化其他仓库的工具仓库，因此要特别谨慎：

- 默认保持 dry-run 优先
- 未经明确确认，不要对外部目标项目直接执行 `--apply`
- 未经明确确认，不要使用 `--force` 或 `--reinit` 覆盖既有初始化结果
- 不暴露本机环境中的敏感路径、密钥、令牌或私有配置

## 验证要求

对初始化逻辑、模板、参数或输出做了修改后，至少做与改动相称的验证。

优先验证：

1. `python -m unittest tests.test_init_spec_repo`
2. `python skills/bingo-spec-coding-max-skill/scripts/init_spec_repo.py --help`

如果变更涉及安装脚本或平台差异，再补充对应平台的命令级自检。

## 沟通要求

汇报结果时应说明：

- 改了什么
- 为什么改
- 影响哪些入口或生成物
- 用什么方式验证

如果没有完成验证，要明确写出未验证项与原因。
