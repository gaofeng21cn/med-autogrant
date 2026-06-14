from __future__ import annotations

import ast
import json
import shutil
import subprocess
import tomllib
import unittest
from pathlib import Path

from med_autogrant.family_shared_release import inspect_current_repo_family_shared_alignment


REPO_ROOT = Path(__file__).resolve().parents[1]
TRACKED_PATH_FORBIDDEN_EXACT_NAMES = {
    ".DS_Store",
    ".agent-contract-baseline.json",
}
TRACKED_PATH_FORBIDDEN_PARTS = {
    ".agents",
    ".codex",
    ".omx",
    ".runtime-program",
    "__pycache__",
    "build",
    "dist",
    "out",
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
    return completed.stdout.splitlines()


def _tracked_or_pending_files() -> list[str]:
    completed = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard"],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.splitlines()


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

    def test_forbidden_generated_and_local_state_paths_are_not_tracked(self) -> None:
        forbidden_paths = [path for path in _tracked_files() if _is_forbidden_tracked_path(path)]

        self.assertEqual(forbidden_paths, [])

    def test_repo_does_not_track_repo_local_agent_state(self) -> None:
        agent_paths = [path for path in _tracked_files() if path.startswith(".agents/")]

        self.assertEqual(agent_paths, [])
        self.assertTrue((REPO_ROOT / "plugins" / "mag" / ".codex-plugin" / "plugin.json").is_file())

    def test_pyproject_pins_opl_harness_shared_to_a_full_commit(self) -> None:
        pyproject = tomllib.loads((REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
        dependency = next(
            item
            for item in pyproject["project"]["dependencies"]
            if item.startswith("opl-harness-shared @ ")
        )

        self.assertRegex(
            dependency,
            r"^opl-harness-shared @ git\+https://github\.com/gaofeng21cn/one-person-lab\.git@[0-9a-f]{40}#subdirectory=python/opl-harness-shared$",
        )

    def test_family_shared_release_alignment_is_fail_closed_for_repo_truth(self) -> None:
        inspection = inspect_current_repo_family_shared_alignment()

        self.assertEqual(len(inspection["owner_commit"]), 40)
        self.assertEqual(inspection["verify_command"], "scripts/verify.sh family")
        self.assertEqual(inspection["status"], "aligned")
        self.assertEqual(
            [item["file"] for item in inspection["findings"]],
            ["pyproject.toml", "uv.lock"],
        )
        self.assertTrue(all(item["status"] == "aligned" for item in inspection["findings"]))
        self.assertTrue(all(item["pins"] == [inspection["owner_commit"]] for item in inspection["findings"]))

    def test_repo_tracked_code_file_line_budget_is_advisory_by_default(self) -> None:
        result = subprocess.run(
            ["python", "scripts/line_budget.py"],
            cwd=REPO_ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("test-line-budget-strict:", (REPO_ROOT / "Makefile").read_text(encoding="utf-8"))

    def test_machine_surfaces_do_not_restore_retired_product_entry_compatibility_claims(self) -> None:
        retired_claim_patterns = (
            '"compatibility_alias_allowed": true',
            "compatibility_alias_allowed: true",
            '"claims_compatibility_alias_owner": true',
            "claims_compatibility_alias_owner: true",
            '"mag_restores_compatibility_alias": true',
            "mag_restores_compatibility_alias: true",
            "active_compatibility_alias",
            "default_compatibility_alias",
        )
        scanned_roots = ("src/", "tests/", "schemas/", "contracts/", "plugins/")
        scanned_suffixes = {".py", ".json", ".yaml", ".yml", ".toml", ".sh"}
        violations: list[str] = []

        for relative_path in _tracked_or_pending_files():
            if relative_path == "tests/test_repository_hygiene.py":
                continue
            if not relative_path.startswith(scanned_roots):
                continue
            path = REPO_ROOT / relative_path
            if path.suffix not in scanned_suffixes or not path.is_file():
                continue
            text = path.read_text(encoding="utf-8").lower()
            for pattern in retired_claim_patterns:
                if pattern in text:
                    violations.append(f"{relative_path}: {pattern}")

        self.assertEqual(violations, [])

    def test_cli_validate_cases_is_not_a_star_import_facade(self) -> None:
        offenders: list[str] = []
        for relative_path in _tracked_or_pending_files():
            if not relative_path.startswith("tests/test_cli_validate_workspace_") or not relative_path.endswith(".py"):
                continue
            path = REPO_ROOT / relative_path
            tree = ast.parse(path.read_text(encoding="utf-8"))
            if any(
                isinstance(node, ast.ImportFrom)
                and node.module == "cli_validate_cases"
                and any(alias.name == "*" for alias in node.names)
                for node in ast.walk(tree)
            ):
                offenders.append(relative_path)

        self.assertEqual(offenders, [])

    def test_source_modules_do_not_generate_dynamic_all_exports(self) -> None:
        offenders: list[str] = []
        for relative_path in _tracked_or_pending_files():
            if not relative_path.startswith("src/") or not relative_path.endswith(".py"):
                continue
            path = REPO_ROOT / relative_path
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if not (
                    isinstance(node, ast.Assign)
                    and any(isinstance(target, ast.Name) and target.id == "__all__" for target in node.targets)
                    and isinstance(node.value, ast.ListComp)
                    and isinstance(node.value.generators[0].iter, ast.Call)
                    and isinstance(node.value.generators[0].iter.func, ast.Name)
                    and node.value.generators[0].iter.func.id == "globals"
                ):
                    continue
                offenders.append(relative_path)

        self.assertEqual(offenders, [])


if __name__ == "__main__":
    unittest.main()
