import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "skills/bingo-spec-coding-max-skill/scripts/init_spec_repo.py"


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

    def create_localized_source_docs(self, root: Path) -> Path:
        source_docs = root / "doc"
        for language, marker in (("zh", "ZH"), ("en", "EN")):
            language_dir = source_docs / language
            language_dir.mkdir(parents=True, exist_ok=True)
            required_files = {
                "spec_bootstrap_prompt_v6.md": f"# {marker} bootstrap\n",
                "change_classifier.prompt.md": f"# {marker} classifier\n",
                "generate_feature_tasks.prompt.md": f"# {marker} feature tasks\n",
                "generate_change_tasks.prompt.md": f"# {marker} change tasks\n",
                "usage_examples.md": f"# {marker} usage\n",
            }
            for name, content in required_files.items():
                (language_dir / name).write_text(content, encoding="utf-8")
        return source_docs

    def create_java_project(self, root: Path) -> None:
        (root / "pom.xml").write_text(
            """
<project>
  <dependencies>
    <dependency>spring-boot-starter-web</dependency>
    <dependency>spring-boot-starter-data-jpa</dependency>
    <dependency>org.testcontainers:junit-jupiter</dependency>
  </dependencies>
</project>
""".strip()
            + "\n",
            encoding="utf-8",
        )
        (root / "src/main/java/org/example/demo").mkdir(parents=True, exist_ok=True)
        (root / "src/main/java/org/example/demo/App.java").write_text("class App {}\n", encoding="utf-8")
        (root / "src/test/java/org/example/demo").mkdir(parents=True, exist_ok=True)
        (root / "src/test/java/org/example/demo/AppTests.java").write_text("class AppTests {}\n", encoding="utf-8")
        (root / "src/main/resources").mkdir(parents=True, exist_ok=True)
        (root / "src/main/resources/application-postgres.properties").write_text(
            "spring.datasource.url=jdbc:postgresql://localhost:5432/demo\n",
            encoding="utf-8",
        )

    def create_frontend_project(self, root: Path, project_dir: Path | None = None) -> None:
        target = project_dir or root
        target.mkdir(parents=True, exist_ok=True)
        (target / "package.json").write_text(
            """
{
  "name": "frontend-demo",
  "scripts": {
    "dev": "vite",
    "test": "vitest run"
  },
  "dependencies": {
    "react": "^18.0.0",
    "vite": "^5.0.0",
    "tailwindcss": "^3.0.0"
  },
  "devDependencies": {
    "typescript": "^5.0.0",
    "vitest": "^1.0.0",
    "@playwright/test": "^1.0.0"
  }
}
""".strip()
            + "\n",
            encoding="utf-8",
        )
        (target / "src/pages").mkdir(parents=True, exist_ok=True)
        (target / "src/components").mkdir(parents=True, exist_ok=True)
        (target / "public").mkdir(parents=True, exist_ok=True)
        (target / "playwright.config.ts").write_text("export default {};\n", encoding="utf-8")

    def create_python_project(self, root: Path) -> None:
        (root / "pyproject.toml").write_text(
            """
[project]
dependencies = [
  "fastapi>=0.100",
  "sqlalchemy>=2.0",
  "pydantic>=2.0",
  "pytest>=8.0"
]
""".strip()
            + "\n",
            encoding="utf-8",
        )
        (root / "alembic.ini").write_text("[alembic]\nscript_location = alembic\n", encoding="utf-8")
        (root / "app").mkdir(parents=True, exist_ok=True)
        (root / "app/main.py").write_text("app = object()\n", encoding="utf-8")
        (root / "tests").mkdir(parents=True, exist_ok=True)
        (root / "tests/test_app.py").write_text("def test_app():\n    assert True\n", encoding="utf-8")

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
            self.assertIn("Lock exists. Use --reinit or --upgrade to run initialization again.", second_run.stdout)

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
            self.assertIn("Suggested test commands: npm test", context_content)

    def test_default_language_is_chinese_and_uses_localized_docs(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir)
            self.create_localized_source_docs(project_root)

            result = self.run_script(project_root, "--apply")

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("language    : zh", result.stdout)
            self.assertIn(str(project_root / "doc" / "zh"), result.stdout)

            agents_content = (project_root / "AGENTS.md").read_text(encoding="utf-8")
            prompt_content = (project_root / "spec/prompts/spec_bootstrap_prompt_v6.md").read_text(encoding="utf-8")
            lock_content = (project_root / ".spec-bootstrap.lock").read_text(encoding="utf-8")

            self.assertIn("Always respond in Chinese-simplified", agents_content)
            self.assertIn("默认工作流", agents_content)
            self.assertEqual(prompt_content, "# ZH bootstrap\n")
            self.assertIn("language=zh", lock_content)

    def test_explicit_english_language_switches_templates_and_docs(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir)
            self.create_localized_source_docs(project_root)

            result = self.run_script(project_root, "--apply", "--language", "en")

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("language    : en", result.stdout)
            self.assertIn(str(project_root / "doc" / "en"), result.stdout)

            agents_content = (project_root / "AGENTS.md").read_text(encoding="utf-8")
            prompt_content = (project_root / "spec/prompts/spec_bootstrap_prompt_v6.md").read_text(encoding="utf-8")
            lock_content = (project_root / ".spec-bootstrap.lock").read_text(encoding="utf-8")

            self.assertIn("Always respond in English", agents_content)
            self.assertIn("Default workflow:", agents_content)
            self.assertEqual(prompt_content, "# EN bootstrap\n")
            self.assertIn("language=en", lock_content)

            context_content = (project_root / "spec/SPEC_CONTEXT.md").read_text(encoding="utf-8")
            self.assertIn("## Repository Summary", context_content)
            self.assertIn("Auto-context note:", context_content)

    def test_upgrade_reinitializes_existing_project_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir)
            self.create_localized_source_docs(project_root)

            first_run = self.run_script(project_root, "--apply")
            second_run = self.run_script(project_root, "--apply", "--upgrade", "--language", "en")

            self.assertEqual(first_run.returncode, 0, first_run.stderr)
            self.assertEqual(second_run.returncode, 0, second_run.stderr)
            self.assertIn("overwrite   : yes", second_run.stdout)
            self.assertIn("language    : en", second_run.stdout)

            agents_content = (project_root / "AGENTS.md").read_text(encoding="utf-8")
            prompt_content = (project_root / "spec/prompts/spec_bootstrap_prompt_v6.md").read_text(encoding="utf-8")
            lock_content = (project_root / ".spec-bootstrap.lock").read_text(encoding="utf-8")

            self.assertIn("Always respond in English", agents_content)
            self.assertIn("Spec Language: English", agents_content)
            self.assertEqual(prompt_content, "# EN bootstrap\n")
            self.assertIn("language=en", lock_content)

    def test_java_repo_generates_enhanced_spec_context(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir)
            self.create_source_docs(project_root)
            self.create_java_project(project_root)

            result = self.run_script(project_root, "--apply")

            self.assertEqual(result.returncode, 0, result.stderr)
            context_content = (project_root / "spec/SPEC_CONTEXT.md").read_text(encoding="utf-8")

            self.assertIn("Spring Boot", context_content)
            self.assertIn("Spring Data JPA", context_content)
            self.assertIn("Testcontainers", context_content)
            self.assertIn("src/main/java", context_content)
            self.assertIn("org.example.demo", context_content)
            self.assertIn("PostgreSQL", context_content)

    def test_frontend_repo_generates_enhanced_spec_context(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir)
            self.create_source_docs(project_root)
            self.create_frontend_project(project_root)

            result = self.run_script(project_root, "--apply")

            self.assertEqual(result.returncode, 0, result.stderr)
            context_content = (project_root / "spec/SPEC_CONTEXT.md").read_text(encoding="utf-8")

            self.assertIn("React", context_content)
            self.assertIn("Vite", context_content)
            self.assertIn("TypeScript", context_content)
            self.assertIn("Playwright", context_content)
            self.assertIn("src/pages", context_content)
            self.assertIn("npm run dev", context_content)

    def test_python_repo_generates_enhanced_spec_context(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir)
            self.create_source_docs(project_root)
            self.create_python_project(project_root)

            result = self.run_script(project_root, "--apply")

            self.assertEqual(result.returncode, 0, result.stderr)
            context_content = (project_root / "spec/SPEC_CONTEXT.md").read_text(encoding="utf-8")

            self.assertIn("FastAPI", context_content)
            self.assertIn("SQLAlchemy", context_content)
            self.assertIn("Pydantic", context_content)
            self.assertIn("Alembic", context_content)
            self.assertIn("python -m pytest tests", context_content)
            self.assertIn("app", context_content)

    def test_hybrid_repo_lists_multiple_stacks_and_commands(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir)
            self.create_source_docs(project_root)
            self.create_java_project(project_root)
            self.create_frontend_project(project_root, project_root / "frontend")

            result = self.run_script(project_root, "--apply")

            self.assertEqual(result.returncode, 0, result.stderr)
            context_content = (project_root / "spec/SPEC_CONTEXT.md").read_text(encoding="utf-8")

            self.assertIn("Stack: Java", context_content)
            self.assertIn("Frontend", context_content)
            self.assertIn("mvn spring-boot:run", context_content)
            self.assertIn("(cd frontend && npm run dev)", context_content)

    def test_weak_signal_repo_falls_back_to_confirmation_placeholders(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir)
            self.create_source_docs(project_root)

            result = self.run_script(project_root, "--apply")

            self.assertEqual(result.returncode, 0, result.stderr)
            context_content = (project_root / "spec/SPEC_CONTEXT.md").read_text(encoding="utf-8")

            self.assertIn("Unknown stack. Fill in runtime, framework, database, and deployment details.", context_content)
            self.assertIn("待确认：未检测到高置信度的模块边界", context_content)
            self.assertIn("No common run command detected.", context_content)


if __name__ == "__main__":
    unittest.main()
