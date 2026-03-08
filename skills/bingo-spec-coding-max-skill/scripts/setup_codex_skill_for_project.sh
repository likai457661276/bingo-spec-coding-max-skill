#!/usr/bin/env bash
set -euo pipefail

MODE="symlink"
FORCE="false"
UPGRADE_SKILL="false"
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
    --upgrade-skill)
      UPGRADE_SKILL="true"
      shift
      ;;
    *)
      echo "[ERROR] Unknown argument: $1"
      echo "Usage: $0 [--target-project <path>] [--mode symlink|copy] [--codex-home <path>] [--force] [--upgrade-skill]"
      exit 1
      ;;
  esac
done

if [[ -z "$CODEX_HOME_VALUE" ]]; then
  CODEX_HOME_VALUE="$DEFAULT_CODEX_HOME"
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_PROJECT_DIR="$(cd "$TARGET_PROJECT" && pwd)"
TARGET_DOC_DIR="$TARGET_PROJECT_DIR/doc"
SKILL_TARGET_DIR="$CODEX_HOME_VALUE/skills/bingo-spec-coding-max-skill"
DOC_FILES_EXIST="false"

if [[ -d "$TARGET_DOC_DIR" ]] && find "$TARGET_DOC_DIR" -type f -print -quit | grep -q .; then
  DOC_FILES_EXIST="true"
fi

INSTALL_ARGS=(--mode "$MODE" --codex-home "$CODEX_HOME_VALUE")
PREPARE_ARGS=(--target-project "$TARGET_PROJECT")

if [[ "$FORCE" == "true" ]]; then
  INSTALL_ARGS+=(--force)
  PREPARE_ARGS+=(--force)
fi
if [[ "$UPGRADE_SKILL" == "true" ]]; then
  INSTALL_ARGS+=(--upgrade)
fi

if [[ -e "$SKILL_TARGET_DIR" && "$FORCE" != "true" && "$UPGRADE_SKILL" != "true" ]]; then
  echo "[SKIP ] Existing Codex skill preserved: $SKILL_TARGET_DIR"
else
  bash "$SCRIPT_DIR/install_codex_skill.sh" "${INSTALL_ARGS[@]}"
fi
if [[ "$FORCE" != "true" && "$DOC_FILES_EXIST" == "true" ]]; then
  echo "[SKIP ] Existing doc inputs preserved: $TARGET_DOC_DIR"
else
  bash "$SCRIPT_DIR/prepare_target_project.sh" "${PREPARE_ARGS[@]}"
fi

echo "[OK] Codex skill installed and target project prepared."
echo "[INFO] Open the target project in Codex and trigger: \$bingo-spec-coding-max-skill"
