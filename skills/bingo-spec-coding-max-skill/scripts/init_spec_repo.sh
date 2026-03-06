#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PY_SCRIPT="$SCRIPT_DIR/init_spec_repo.py"

if command -v python3 >/dev/null 2>&1; then
  python3 "$PY_SCRIPT" "$@"
elif command -v python >/dev/null 2>&1; then
  python "$PY_SCRIPT" "$@"
else
  echo "[ERROR] Python is required but not found."
  exit 1
fi
