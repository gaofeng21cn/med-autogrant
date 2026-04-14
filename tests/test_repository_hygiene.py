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

        self.assertNotIn(".codex/", text)
        self.assertNotIn(".runtime-program/", text)
        self.assertNotIn(".omx/", text)

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
            ["git", "ls-files", ".runtime-program", ".codex", ".omx"],
            cwd=REPO_ROOT,
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(completed.returncode, 0)
        self.assertEqual(completed.stdout.strip(), "")

    def test_series_doc_governance_checklist_is_repo_tracked_and_linked_from_docs_indexes(self) -> None:
        checklist = (REPO_ROOT / "docs/references/series-doc-governance-checklist.md").read_text(encoding="utf-8")
        docs_readme = (REPO_ROOT / "docs/README.md").read_text(encoding="utf-8")
        docs_readme_zh = (REPO_ROOT / "docs/README.zh-CN.md").read_text(encoding="utf-8")

        for label in ("One Person Lab", "Med Auto Science", "Med Auto Grant", "RedCube AI"):
            with self.subTest(label=label):
                self.assertIn(label, checklist)

        for doc_name in ("project.md", "status.md", "architecture.md", "invariants.md", "decisions.md"):
            with self.subTest(doc_name=doc_name):
                self.assertIn(doc_name, checklist)

        self.assertIn("docs/specs/**", checklist)
        self.assertIn("schemas/v1/", checklist)
        self.assertIn("contracts/runtime-program/", checklist)
        self.assertIn("scripts/verify.sh meta", checklist)
        self.assertIn("make test-meta", checklist)
        self.assertIn("series-doc-governance-checklist.md", docs_readme)
        self.assertIn("series-doc-governance-checklist.md", docs_readme_zh)


if __name__ == "__main__":
    unittest.main()
