# spec-init-bootstrap

初始化专用 Skill，用于把仓库落地为 Spec 驱动开发结构。

## 当前仓库结构

- `doc/`: 初始化输入文档（提示词与示例）
- `skills/spec-init-bootstrap/`: Skill 定义与跨平台初始化脚本

## 手动触发规则

仅在用户显式提到 `$spec-init-bootstrap` 时执行。

## 运行方式

### Windows (PowerShell)

```powershell
powershell -ExecutionPolicy Bypass -File .\skills\spec-init-bootstrap\scripts\init_spec_repo.ps1 --dry-run
powershell -ExecutionPolicy Bypass -File .\skills\spec-init-bootstrap\scripts\init_spec_repo.ps1 --apply
```

### macOS (bash)

```bash
bash ./skills/spec-init-bootstrap/scripts/init_spec_repo.sh --dry-run
bash ./skills/spec-init-bootstrap/scripts/init_spec_repo.sh --apply
```

## 可选参数

- `--project-root <path>`: 目标项目根目录（默认当前目录）
- `--source-docs <path>`: 输入文档目录（默认 `<project-root>/doc`）
- `--force`: 覆盖已有文件
- `--reinit`: 忽略 lock 重新初始化

## 初始化输出

执行 `--apply` 后，脚本会创建/写入：

- `AGENTS.md`
- `spec/INDEX.md`
- `spec/SPEC_CONTEXT.md`
- `spec/SPEC_WORKFLOW.md`
- `spec/CHANGE_POLICY.md`
- `spec/templates/SPEC_TEMPLATE.md`
- `spec/templates/TASK_TEMPLATE.md`
- `spec/prompts/*.md`
- `spec/usage/usage_examples.md`
- `.spec-bootstrap.lock`

## 使用示例

### 手动触发（先预览后落地）

```text
请执行 $spec-init-bootstrap，对当前仓库做初始化。先 dry-run。
```

Windows:

```powershell
powershell -ExecutionPolicy Bypass -File .\skills\spec-init-bootstrap\scripts\init_spec_repo.ps1 --dry-run
powershell -ExecutionPolicy Bypass -File .\skills\spec-init-bootstrap\scripts\init_spec_repo.ps1 --apply
```

macOS:

```bash
bash ./skills/spec-init-bootstrap/scripts/init_spec_repo.sh --dry-run
bash ./skills/spec-init-bootstrap/scripts/init_spec_repo.sh --apply
```

### 变更等级示例（L1/L2/L3）

1. L1 新增登录功能：流程 `计划 → 规格 → 任务 → 代码`
2. L2 密码校验缺陷：流程 `任务 → 代码`
3. L3 生产令牌故障：流程 `补丁 → 代码`

详细示例见：

- `doc/usage_examples.md`
- `spec/usage/usage_examples.md`（初始化后生成）
