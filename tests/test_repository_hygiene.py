from __future__ import annotations

import ast
import shutil
import subprocess
import tomllib
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
TRACKED_PATH_FORBIDDEN_EXACT_NAMES = {
    ".DS_Store",
    ".agent-contract-baseline.json",
}
TRACKED_PATH_FORBIDDEN_PARTS = {
    ".agents",
    ".codex",
    ".codex-plugin",
    ".omx",
    ".runtime-program",
    "__pycache__",
    "build",
    "dist",
    "out",
    "plugins",
    "runtime-state",
}


def _tracked_files() -> list[str]:
    completed = subprocess.run(
        ["git", "ls-files"],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return [line for line in completed.stdout.splitlines() if (REPO_ROOT / line).exists()]


def _is_forbidden_tracked_path(path: str) -> bool:
    parts = Path(path).parts
    return (
        any(part in TRACKED_PATH_FORBIDDEN_EXACT_NAMES for part in parts)
        or any(part in TRACKED_PATH_FORBIDDEN_PARTS for part in parts)
        or any(part.endswith(".egg-info") for part in parts)
    )


class RepositoryHygieneTest(unittest.TestCase):
    def test_repo_hygiene_script_removes_only_ignored_generated_artifacts(self) -> None:
        ignored_cache = REPO_ROOT / "src" / "med_autogrant" / "__pycache__"
        ignored_quality_details = REPO_ROOT / "artifacts" / "opl-quality-details"
        unignored_cache = REPO_ROOT / "local_unignored_cache" / "__pycache__"
        ignored_cache.mkdir(parents=True, exist_ok=True)
        ignored_quality_details.mkdir(parents=True, exist_ok=True)
        unignored_cache.mkdir(parents=True, exist_ok=True)
        (ignored_cache / "module.pyc").write_bytes(b"cache")
        (ignored_quality_details / "quality-details.json").write_text("{}", encoding="utf-8")
        (unignored_cache / "module.pyc").write_bytes(b"cache")

        try:
            script = (REPO_ROOT / "scripts" / "repo-hygiene.sh").read_text(encoding="utf-8")
            self.assertIn("scripts/repo-hygiene.sh [--fix]", script)
            self.assertIn("git check-ignore -q", script)
            self.assertIn("git ls-files --others --exclude-standard", script)

            result = subprocess.run(
                ["bash", "scripts/repo-hygiene.sh", "--fix"],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(ignored_cache.exists())
            self.assertFalse(ignored_quality_details.exists())
            self.assertFalse((REPO_ROOT / "artifacts").exists())
            self.assertFalse(unignored_cache.exists())
        finally:
            if ignored_cache.exists():
                shutil.rmtree(ignored_cache)
            if ignored_quality_details.exists():
                shutil.rmtree(ignored_quality_details)
            if unignored_cache.parent.exists():
                shutil.rmtree(unignored_cache.parent)

    def test_gitignore_fully_ignores_local_tooling_state(self) -> None:
        text = (REPO_ROOT / ".gitignore").read_text(encoding="utf-8")

        self.assertNotIn(".codex/", text)
        self.assertNotIn(".runtime-program/", text)
        self.assertNotIn(".omx/", text)
        self.assertIn("opl-release.lock.json", text.splitlines())

    def test_forbidden_generated_and_local_state_paths_are_not_tracked(self) -> None:
        forbidden_paths = [path for path in _tracked_files() if _is_forbidden_tracked_path(path)]

        self.assertEqual(forbidden_paths, [])

    def test_repo_has_no_legacy_carrier_mirrors_or_opl_framework_imports(self) -> None:
        for legacy_dir in ("plugins", ".codex-plugin", ".agents"):
            self.assertFalse((REPO_ROOT / legacy_dir).exists(), legacy_dir)
        for legacy_file in (
            "app-contribution-adapter.json",
            "contracts/carrier_projection.json",
            "contracts/opl_agent_package_manifest.json",
            "scripts/sync_carrier.py",
        ):
            self.assertFalse((REPO_ROOT / legacy_file).exists(), legacy_file)
        self.assertFalse((REPO_ROOT / "src" / "opl_framework").exists())
        self.assertFalse((REPO_ROOT / "src" / "opl_framework").is_symlink())
        self.assertTrue((REPO_ROOT / "skills" / "med-autogrant" / "SKILL.md").is_file())
        for scan_root in ("src", "runtime", "scripts", "tests"):
            for path in (REPO_ROOT / scan_root).rglob("*.py"):
                tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            self.assertFalse(
                                alias.name == "opl_framework" or alias.name.startswith("opl_framework."),
                                f"{path}: {alias.name}",
                            )
                    elif isinstance(node, ast.ImportFrom) and node.module:
                        self.assertFalse(
                            node.module == "opl_framework" or node.module.startswith("opl_framework."),
                            f"{path}: {node.module}",
                        )

    def test_framework_python_carrier_is_not_an_agent_dependency(self) -> None:
        pyproject = tomllib.loads((REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
        self.assertFalse(any("one-person-lab.git" in item for item in pyproject["project"]["dependencies"]))
        self.assertNotIn("one-person-lab.git", (REPO_ROOT / "uv.lock").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
