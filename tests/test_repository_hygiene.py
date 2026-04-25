from __future__ import annotations

import subprocess
import tomllib
import unittest
from pathlib import Path

from med_autogrant.family_shared_release import inspect_current_repo_family_shared_alignment


REPO_ROOT = Path(__file__).resolve().parents[1]
LINE_BUDGET_TARGET = 1000
LINE_BUDGET_LIMIT = 1500
LEGACY_OVER_TARGET_BUDGETS = {
    "src/med_autogrant/grant_autonomy_controller.py": 1326,
}
CODE_SUFFIXES = {".py", ".sh", ".js", ".ts", ".tsx", ".jsx"}


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


class RepositoryHygieneTest(unittest.TestCase):
    def test_gitignore_fully_ignores_local_tooling_state(self) -> None:
        text = (REPO_ROOT / ".gitignore").read_text(encoding="utf-8")

        self.assertNotIn(".codex/", text)
        self.assertNotIn(".runtime-program/", text)
        self.assertNotIn(".omx/", text)

    def test_local_tooling_state_is_not_tracked(self) -> None:
        completed = subprocess.run(
            ["git", "ls-files", ".runtime-program", ".codex", ".omx"],
            cwd=REPO_ROOT,
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(completed.returncode, 0)
        self.assertEqual(completed.stdout.strip(), "")

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


if __name__ == "__main__":
    unittest.main()
