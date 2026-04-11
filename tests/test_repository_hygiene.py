from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "src"))


class RepositoryHygieneTest(unittest.TestCase):
    def test_gitignore_fully_ignores_local_tooling_state(self) -> None:
        text = (REPO_ROOT / ".gitignore").read_text(encoding="utf-8")

        self.assertIn(".codex/", text)
        self.assertIn(".runtime-program/", text)
        self.assertNotIn("!.codex/", text)
        self.assertNotIn("!.runtime-program/", text)

    def test_public_readmes_do_not_expose_local_tooling_paths(self) -> None:
        for path in (REPO_ROOT / "README.md", REPO_ROOT / "README.zh-CN.md"):
            with self.subTest(path=path.name):
                text = path.read_text(encoding="utf-8")
                self.assertNotIn(".runtime-program/context", text)
                self.assertNotIn(".runtime-program/plans", text)
                self.assertNotIn(".runtime-program/reports", text)
                self.assertNotIn(".codex/", text)

    def test_local_tooling_state_is_not_tracked(self) -> None:
        completed = subprocess.run(
            ["git", "ls-files", ".runtime-program", ".codex"],
            cwd=REPO_ROOT,
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(completed.returncode, 0)
        self.assertEqual(completed.stdout.strip(), "")


if __name__ == "__main__":
    unittest.main()
