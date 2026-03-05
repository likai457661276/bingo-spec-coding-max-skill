---
name: spec-init-bootstrap
description: 初始化专用技能。仅在用户显式输入 `$spec-init-bootstrap` 时使用。将项目初始化为 Spec 驱动结构，创建 AGENTS.md、spec 目录及模板，并把 doc 目录下的提示词与示例注入到 spec/prompts 与 spec/usage。支持 Windows 与 macOS，默认 dry-run，使用 --apply 才落地。
---

# Spec Init Bootstrap

仅在用户明确手动触发 `$spec-init-bootstrap` 时执行。

## 执行规则

1. 默认先执行 dry-run，先展示将创建或覆盖的文件。
2. 仅在用户明确确认后执行 apply。
3. 检测到 `.spec-bootstrap.lock` 时停止并提示使用 `--reinit`。
4. 已存在文件默认不覆盖，除非传 `--force`。

## 运行入口

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

## 输入来源

默认从项目根目录 `doc/` 读取以下文件并注入：

1. `spec_bootstrap_prompt_v5.md`（初始化流程提示词）
2. `change_classifier.prompt.md`
3. `generate_feature_tasks.prompt.md`
4. `generate_change_tasks.prompt.md`
5. `usage_examples.md`

若目录不同，使用 `--source-docs <path>` 指定。
