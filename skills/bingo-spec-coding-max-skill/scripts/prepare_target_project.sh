#!/usr/bin/env bash
set -euo pipefail

TARGET_PROJECT="."
FORCE="false"
CLEAN="false"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --target-project)
      TARGET_PROJECT="${2:-}"
      shift 2
      ;;
    --force)
      FORCE="true"
      shift
      ;;
    --clean)
      CLEAN="true"
      shift
      ;;
    *)
      echo "[ERROR] Unknown argument: $1"
      echo "Usage: $0 [--target-project <path>] [--force] [--clean]"
      exit 1
      ;;
  esac
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
SOURCE_DOC_DIR="$SKILL_DIR/resources/doc"
TARGET_PROJECT_DIR="$(cd "$TARGET_PROJECT" && pwd)"
TARGET_DOC_DIR="$TARGET_PROJECT_DIR/doc"

if [[ ! -d "$SOURCE_DOC_DIR" ]]; then
  echo "[ERROR] Bundled doc templates not found: $SOURCE_DOC_DIR"
  exit 1
fi

if [[ "$CLEAN" == "true" && -d "$TARGET_DOC_DIR" ]]; then
  rm -rf "$TARGET_DOC_DIR"
  echo "[REMOVE] Existing doc inputs cleared: $TARGET_DOC_DIR"
fi

mkdir -p "$TARGET_DOC_DIR"

while IFS= read -r -d '' source_file; do
  relative_path="${source_file#"$SOURCE_DOC_DIR"/}"
  target_file="$TARGET_DOC_DIR/$relative_path"
  target_parent="$(dirname "$target_file")"

  mkdir -p "$target_parent"

  if [[ -e "$target_file" && "$FORCE" != "true" ]]; then
    echo "[ERROR] Target file already exists: $target_file"
    echo "        Re-run with --force to overwrite existing doc inputs."
    exit 1
  fi

  cp "$source_file" "$target_file"
  echo "[COPY ] $target_file"
done < <(find "$SOURCE_DOC_DIR" -type f -print0)

echo "[OK] Target project prepared: $TARGET_PROJECT_DIR"
echo "[INFO] Next step: trigger \$bingo-spec-coding-max-skill inside the target project."
