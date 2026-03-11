#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import shutil
import sys


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Copy bundled skill doc templates into the target project."
    )
    parser.add_argument(
        "--project-root",
        default=".",
        help="Target project root directory (default: current directory).",
    )
    return parser.parse_args()


def resolve_source_doc_dir(script_path: Path) -> Path:
    skill_dir = script_path.resolve().parent.parent
    candidate = skill_dir / "resources" / "doc"
    if candidate.is_dir():
        return candidate
    raise FileNotFoundError(
        "Unable to locate bundled doc templates under skill resources/doc/."
    )


def copy_doc_tree(source_doc_dir: Path, project_root: Path) -> None:
    target_doc_dir = project_root / "doc"
    if target_doc_dir.exists():
        shutil.rmtree(target_doc_dir)
        print(f"[REMOVE] Existing doc inputs cleared: {target_doc_dir}")

    shutil.copytree(source_doc_dir, target_doc_dir)
    print(f"[COPY ] Doc templates synced to: {target_doc_dir}")


def main() -> int:
    args = parse_args()
    script_path = Path(__file__)
    project_root = Path(args.project_root).resolve()

    try:
        source_doc_dir = resolve_source_doc_dir(script_path)
    except FileNotFoundError as exc:
        print(f"[ERROR] {exc}")
        return 1

    if not project_root.exists():
        print(f"[ERROR] Project root does not exist: {project_root}")
        return 1

    copy_doc_tree(source_doc_dir, project_root)
    print("[INFO] Next step: run init_spec_repo in dry-run mode to regenerate the spec scaffold preview.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
