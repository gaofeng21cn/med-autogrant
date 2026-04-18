from __future__ import annotations

import subprocess
import sys
import tomllib
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

    def test_series_doc_governance_checklist_is_repo_tracked_and_linked_from_docs_indexes(self) -> None:
        checklist = (REPO_ROOT / "docs/references/series-doc-governance-checklist.md").read_text(encoding="utf-8")
        docs_readme = (REPO_ROOT / "docs/README.md").read_text(encoding="utf-8")
        docs_readme_zh = (REPO_ROOT / "docs/README.zh-CN.md").read_text(encoding="utf-8")
        previous_index = -1

        for heading in (
            "## 目标",
            "## 一、默认入口",
            "## 二、核心五件套",
            "## 三、公开层与内部层",
            "## 四、系列一致性检查",
            "## 五、默认验证",
        ):
            with self.subTest(heading=heading):
                current_index = checklist.find(heading)
                self.assertGreaterEqual(current_index, 0)
                self.assertGreater(current_index, previous_index)
                previous_index = current_index

        for label in ("One Person Lab", "Med Auto Science", "Med Auto Grant", "RedCube AI"):
            with self.subTest(label=label):
                self.assertIn(label, checklist)

        for doc_name in ("project.md", "status.md", "architecture.md", "invariants.md", "decisions.md"):
            with self.subTest(doc_name=doc_name):
                self.assertIn(doc_name, checklist)

        self.assertIn("docs/specs/**", checklist)
        self.assertIn("schemas/v1/", checklist)
        self.assertIn("contracts/runtime-program/", checklist)
        self.assertIn("Hermes-Agent", checklist)
        self.assertIn("AGENTS.md", checklist)
        self.assertIn("第二真相源", checklist)
        self.assertIn("scripts/verify.sh meta", checklist)
        self.assertIn("make test-meta", checklist)
        self.assertIn("series-doc-governance-checklist.md", docs_readme)
        self.assertIn("series-doc-governance-checklist.md", docs_readme_zh)


if __name__ == "__main__":
    unittest.main()
