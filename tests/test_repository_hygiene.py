from __future__ import annotations

import subprocess
import tomllib
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


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


if __name__ == "__main__":
    unittest.main()
