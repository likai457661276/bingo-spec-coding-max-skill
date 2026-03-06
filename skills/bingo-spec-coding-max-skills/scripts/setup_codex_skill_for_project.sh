#!/usr/bin/env bash
set -euo pipefail

MODE="symlink"
FORCE="false"
TARGET_PROJECT="."
CODEX_HOME_VALUE="${CODEX_HOME:-}"
DEFAULT_CODEX_HOME="$HOME/.codex"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --mode)
      MODE="${2:-}"
      shift 2
      ;;
    --codex-home)
      CODEX_HOME_VALUE="${2:-}"
      shift 2
      ;;
    --target-project)
      TARGET_PROJECT="${2:-}"
      shift 2
      ;;
    --force)
      FORCE="true"
      shift
      ;;
    *)
      echo "[ERROR] Unknown argument: $1"
      echo "Usage: $0 [--target-project <path>] [--mode symlink|copy] [--codex-home <path>] [--force]"
      exit 1
      ;;
  esac
done

if [[ -z "$CODEX_HOME_VALUE" ]]; then
  CODEX_HOME_VALUE="$DEFAULT_CODEX_HOME"
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

INSTALL_ARGS=(--mode "$MODE" --codex-home "$CODEX_HOME_VALUE")
PREPARE_ARGS=(--target-project "$TARGET_PROJECT")

if [[ "$FORCE" == "true" ]]; then
  INSTALL_ARGS+=(--force)
  PREPARE_ARGS+=(--force)
fi

bash "$SCRIPT_DIR/install_codex_skill.sh" "${INSTALL_ARGS[@]}"
bash "$SCRIPT_DIR/prepare_target_project.sh" "${PREPARE_ARGS[@]}"

echo "[OK] Codex skill installed and target project prepared."
echo "[INFO] Open the target project in Codex and trigger: \$bingo-spec-coding-max-skills"
