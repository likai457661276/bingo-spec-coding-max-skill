import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "skills/bingo-spec-coding-max-skills/scripts/init_spec_repo.py"


class InitSpecRepoTests(unittest.TestCase):
    def run_script(self, project_root: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(SCRIPT_PATH),
                "--project-root",
                str(project_root),
                *args,
            ],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

    def create_source_docs(self, root: Path) -> Path:
        source_docs = root / "doc"
        source_docs.mkdir(parents=True, exist_ok=True)

        required_files = {
            "spec_bootstrap_prompt_v6.md": "# bootstrap\n",
            "change_classifier.prompt.md": "# classifier\n",
            "generate_feature_tasks.prompt.md": "# feature tasks\n",
            "generate_change_tasks.prompt.md": "# change tasks\n",
            "usage_examples.md": "# usage\n",
        }

        for name, content in required_files.items():
            (source_docs / name).write_text(content, encoding="utf-8")

        return source_docs

    def test_dry_run_does_not_write_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir)
            self.create_source_docs(project_root)

            result = self.run_script(project_root, "--dry-run")

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("[DRY-RUN] No file written.", result.stdout)
            self.assertFalse((project_root / "AGENTS.md").exists())
            self.assertFalse((project_root / ".spec-bootstrap.lock").exists())

    def test_apply_creates_core_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir)
            self.create_source_docs(project_root)

            result = self.run_script(project_root, "--apply")

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((project_root / "AGENTS.md").exists())
            self.assertTrue((project_root / "spec/INDEX.md").exists())
            self.assertTrue((project_root / "spec/features/.gitkeep").exists())
            self.assertTrue((project_root / "spec/templates/PLAN_TEMPLATE.md").exists())
            self.assertTrue((project_root / "spec/templates/CHANGE_TEMPLATE.md").exists())
            self.assertTrue((project_root / "spec/templates/HOTFIX_TEMPLATE.md").exists())
            self.assertTrue((project_root / ".spec-bootstrap.lock").exists())

    def test_lock_blocks_reinitialization_without_reinit(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir)
            self.create_source_docs(project_root)

            first_run = self.run_script(project_root, "--apply")
            second_run = self.run_script(project_root, "--dry-run")

            self.assertEqual(first_run.returncode, 0, first_run.stderr)
            self.assertNotEqual(second_run.returncode, 0)
            self.assertIn("Lock exists. Use --reinit to run initialization again.", second_run.stdout)

    def test_detected_project_metadata_is_written_to_generated_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir)
            self.create_source_docs(project_root)
            (project_root / "README.md").write_text(
                "# Demo Project\n\nA lightweight service for testing bootstrap detection.\n",
                encoding="utf-8",
            )
            (project_root / "package.json").write_text('{"name":"demo","scripts":{"test":"npm test"}}\n', encoding="utf-8")
            (project_root / "src").mkdir()

            result = self.run_script(project_root, "--apply")

            self.assertEqual(result.returncode, 0, result.stderr)

            agents_content = (project_root / "AGENTS.md").read_text(encoding="utf-8")
            context_content = (project_root / "spec/SPEC_CONTEXT.md").read_text(encoding="utf-8")

            self.assertIn("A lightweight service for testing bootstrap detection.", agents_content)
            self.assertIn("Detected Stack: Node.js", agents_content)
            self.assertIn("Suggested Test Command: npm test", agents_content)
            self.assertIn("Suggested Source Roots: src", agents_content)

            self.assertIn("Project: A lightweight service for testing bootstrap detection.", context_content)
            self.assertIn("Stack: Node.js", context_content)
            self.assertIn("Source roots: src", context_content)
            self.assertIn("Suggested test command: npm test", context_content)


if __name__ == "__main__":
    unittest.main()
