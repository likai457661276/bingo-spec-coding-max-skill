#!/usr/bin/env bash
set -euo pipefail

MODE="symlink"
FORCE="false"
UPGRADE="false"
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
    --force)
      FORCE="true"
      shift
      ;;
    --upgrade)
      UPGRADE="true"
      shift
      ;;
    *)
      echo "[ERROR] Unknown argument: $1"
      echo "Usage: $0 [--mode symlink|copy] [--codex-home <path>] [--force] [--upgrade]"
      exit 1
      ;;
  esac
done

if [[ "$MODE" != "symlink" && "$MODE" != "copy" ]]; then
  echo "[ERROR] --mode must be 'symlink' or 'copy'."
  exit 1
fi

if [[ -z "$CODEX_HOME_VALUE" ]]; then
  CODEX_HOME_VALUE="$DEFAULT_CODEX_HOME"
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_SOURCE_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
TARGET_ROOT="$CODEX_HOME_VALUE/skills"
TARGET_DIR="$TARGET_ROOT/bingo-spec-coding-max-skill"

mkdir -p "$TARGET_ROOT"

REPLACE_EXISTING="$FORCE"
if [[ "$UPGRADE" == "true" ]]; then
  REPLACE_EXISTING="true"
fi

if [[ -e "$TARGET_DIR" || -L "$TARGET_DIR" ]]; then
  if [[ "$REPLACE_EXISTING" != "true" ]]; then
    echo "[ERROR] Target already exists: $TARGET_DIR"
    echo "        Re-run with --force or --upgrade to replace it."
    exit 1
  fi
  rm -rf "$TARGET_DIR"
  EXISTING_TARGET="true"
else
  EXISTING_TARGET="false"
fi

if [[ "$MODE" == "symlink" ]]; then
  ln -s "$SKILL_SOURCE_DIR" "$TARGET_DIR"
  if [[ "$EXISTING_TARGET" == "true" ]]; then
    ACTION="upgraded via symlink"
  else
    ACTION="symlinked"
  fi
else
  cp -R "$SKILL_SOURCE_DIR" "$TARGET_DIR"
  if [[ "$EXISTING_TARGET" == "true" ]]; then
    ACTION="upgraded via copy"
  else
    ACTION="copied"
  fi
fi

echo "[OK] Skill $ACTION to: $TARGET_DIR"
echo "[INFO] Using CODEX_HOME: $CODEX_HOME_VALUE"
echo "[INFO] Trigger from a target project with: \$bingo-spec-coding-max-skill"
