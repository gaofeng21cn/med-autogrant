from __future__ import annotations

import json
import shutil
import subprocess
import tomllib
import unittest
from pathlib import Path

from med_autogrant.family_shared_release import inspect_current_repo_family_shared_alignment


REPO_ROOT = Path(__file__).resolve().parents[1]
LINE_BUDGET_TARGET = 1000
LINE_BUDGET_LIMIT = 1500
LEGACY_OVER_TARGET_BUDGETS: dict[str, int] = {}
CODE_SUFFIXES = {".py", ".sh", ".js", ".ts", ".tsx", ".jsx"}
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


def _tracked_code_files() -> list[Path]:
    completed = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard"],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return [
        REPO_ROOT / path
        for path in completed.stdout.splitlines()
        if (REPO_ROOT / path).suffix in CODE_SUFFIXES
    ]


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
        unignored_cache = REPO_ROOT / "local_unignored_cache" / "__pycache__"
        ignored_cache.mkdir(parents=True, exist_ok=True)
        unignored_cache.mkdir(parents=True, exist_ok=True)
        (ignored_cache / "module.pyc").write_bytes(b"cache")
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
            self.assertFalse(unignored_cache.exists())
        finally:
            if ignored_cache.exists():
                shutil.rmtree(ignored_cache)
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

    def test_repo_tracked_code_files_stay_within_line_budget(self) -> None:
        over_limit: list[str] = []
        new_or_grown_over_target: list[str] = []
        for path in _tracked_code_files():
            if not path.exists():
                continue
            line_count = sum(1 for _ in path.open(encoding="utf-8"))
            relative_path = path.relative_to(REPO_ROOT).as_posix()
            if line_count > LINE_BUDGET_LIMIT:
                over_limit.append(f"{line_count} {relative_path}")
            elif line_count > LINE_BUDGET_TARGET:
                allowed_line_count = LEGACY_OVER_TARGET_BUDGETS.get(relative_path)
                if allowed_line_count is None or line_count > allowed_line_count:
                    budget = allowed_line_count or LINE_BUDGET_TARGET
                    new_or_grown_over_target.append(f"{line_count} {relative_path} (budget {budget})")

        self.assertEqual(over_limit, [])
        self.assertEqual(new_or_grown_over_target, [])

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


if __name__ == "__main__":
    unittest.main()
