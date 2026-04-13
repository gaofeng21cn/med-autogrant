from __future__ import annotations

from copy import deepcopy
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from med_autogrant.cli import main  # noqa: E402


FROZEN_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p3c_presubmission_frozen.json"


class SubmissionReadyPackageCliTest(unittest.TestCase):
    def run_cli(self, *args: str) -> tuple[int, str, str]:
        stdout = StringIO()
        stderr = StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            try:
                exit_code = main(list(args))
            except SystemExit as exc:
                exit_code = int(exc.code)
        return exit_code, stdout.getvalue(), stderr.getvalue()

    def test_build_submission_ready_package_writes_local_submission_bundle(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            workspace_path = self._write_complete_submission_workspace(Path(tmp_dir))
            output_dir = Path(tmp_dir) / "submission-ready"

            exit_code, stdout, stderr = self.run_cli(
                "build-submission-ready-package",
                "--input",
                str(workspace_path),
                "--output-dir",
                str(output_dir),
                "--format",
                "json",
            )

            self.assertEqual(exit_code, 0)
            self.assertEqual(stderr, "")
            payload = json.loads(stdout)
            self.assertTrue(payload["ok"])
            self.assertEqual(payload["command"], "build-submission-ready-package")
            self.assertEqual(payload["grant_run_id"], "grant-run-nsfc-demo-001-baseline-001")
            self.assertEqual(payload["workspace_id"], "nsfc-demo-001")
            self.assertEqual(payload["draft_id"], "draft-v1")
            self.assertEqual(payload["lifecycle_stage"], "frozen")

            output_paths = payload["output_paths"]
            self.assertEqual(
                set(output_paths),
                {
                    "artifact_bundle",
                    "final_package",
                    "hosted_contract_bundle",
                    "submission_ready_package",
                },
            )
            for output_path in output_paths.values():
                self.assertTrue(Path(output_path).exists(), output_path)

            submission_package = payload["submission_ready_package"]
            self.assertEqual(submission_package["package_kind"], "submission_ready_package")
            self.assertEqual(submission_package["readiness_verdict"], "submission_ready")
            self.assertTrue(submission_package["fully_automatic"])
            self.assertTrue(submission_package["submission_ready"])
            self.assertFalse(submission_package["external_submission_performed"])
            self.assertEqual(submission_package["automation_scope"], "local_submission_package")
            self.assertEqual(submission_package["audit_summary"]["blocking_issue_count"], 0)
            self.assertEqual(submission_package["audit_summary"]["missing_mandatory_sections"], [])
            self.assertEqual(submission_package["audit_summary"]["unresolved_evidence_gap_count"], 0)
            self.assertIn("## 研究方案", submission_package["submission_dossier"]["final_draft_markdown"])
            self.assertIn("## 创新点", submission_package["submission_dossier"]["final_draft_markdown"])
            self.assertEqual(
                json.loads(Path(output_paths["submission_ready_package"]).read_text(encoding="utf-8")),
                submission_package,
            )

    def test_build_submission_ready_package_fails_closed_for_incomplete_submission_materials(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            output_dir = Path(tmp_dir) / "submission-ready"

            exit_code, stdout, stderr = self.run_cli(
                "build-submission-ready-package",
                "--input",
                str(FROZEN_EXAMPLE_PATH),
                "--output-dir",
                str(output_dir),
                "--format",
                "json",
            )

            self.assertEqual(exit_code, 1)
            self.assertEqual(stderr, "")
            payload = json.loads(stdout)
            self.assertFalse(payload["ok"])
            self.assertIn("submission ready package blocked", payload["error"])
            self.assertIn("missing_mandatory_sections", payload["error"])
            self.assertFalse(output_dir.exists())

    def _write_complete_submission_workspace(self, tmp_root: Path) -> Path:
        workspace = json.loads(FROZEN_EXAMPLE_PATH.read_text(encoding="utf-8"))
        workspace = deepcopy(workspace)
        active_draft = workspace["application_drafts"][-1]
        active_draft["outline"].extend(
            [
                {
                    "section_key": "plan",
                    "section_title": "研究方案",
                    "core_claim": "围绕关键通讯轴识别、时间窗验证与功能阻断形成可执行研究方案。",
                    "linked_object_ids": [
                        "question-immune-fibrosis",
                        "arg-001",
                        "fit-001",
                        "prelim-item-1",
                    ],
                },
                {
                    "section_key": "innovation",
                    "section_title": "创新点",
                    "core_claim": "以炎症巨噬细胞-成纤维细胞跨细胞通讯作为纤维化重塑的新机制切入点。",
                    "linked_object_ids": [
                        "question-immune-fibrosis",
                        "arg-001",
                        "fit-001",
                    ],
                },
            ]
        )
        active_draft["sections"].extend(
            [
                {
                    "section_key": "plan",
                    "section_title": "研究方案",
                    "text": "研究方案包括通讯轴筛选、关键时间窗验证、功能阻断和跨组学一致性复核四个步骤。",
                    "linked_object_ids": [
                        "question-immune-fibrosis",
                        "arg-001",
                        "fit-001",
                        "prelim-item-1",
                    ],
                },
                {
                    "section_key": "innovation",
                    "section_title": "创新点",
                    "text": "创新点在于把心梗后炎症巨噬细胞介导的跨细胞通讯作为纤维化重塑的可验证机制主线。",
                    "linked_object_ids": [
                        "question-immune-fibrosis",
                        "arg-001",
                        "fit-001",
                    ],
                },
            ]
        )
        for evidence_item in workspace["preliminary_evidence_pack"]["evidence_items"]:
            evidence_item["gaps"] = []

        workspace_path = tmp_root / "submission-ready-workspace.json"
        workspace_path.write_text(json.dumps(workspace, ensure_ascii=False, indent=2), encoding="utf-8")
        return workspace_path


if __name__ == "__main__":
    unittest.main()
