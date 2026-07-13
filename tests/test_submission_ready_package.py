from __future__ import annotations

from copy import deepcopy
import json
import tempfile
import unittest
from pathlib import Path

from support.cli import run_cli, run_json_cli  # noqa: E402


REPO_ROOT = Path(__file__).resolve().parents[1]
FROZEN = REPO_ROOT / "examples" / "nsfc_workspace_p3c_presubmission_frozen.json"
EXPORT_VERDICT = {
    "export_verdict_ref": "mag-verdict://submission-ready-export/nsfc-demo-001/draft-v1",
    "verdict_state": "submission_ready",
    "owner": "med-autogrant",
    "source_kind": "mag_owner_receipt",
    "provenance_ref": "runtime://mag/receipts/export/nsfc-demo-001/draft-v1.json",
}


class SubmissionReadyPackageTest(unittest.TestCase):
    def test_submission_ready_is_the_complete_package_integration_owner(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_root = Path(tmp_dir)
            workspace_path = self._complete_workspace(tmp_root, include_export_verdict=True)
            output_dir = tmp_root / "submission-ready"
            payload = run_json_cli(
                "package", "submission-ready", "--input", str(workspace_path), "--output-dir", str(output_dir), "--format", "json"
            )

            paths = {name: Path(path) for name, path in payload["output_paths"].items()}
            self.assertEqual(set(paths), {"artifact_bundle", "final_package", "hosted_contract_bundle", "submission_ready_package"})
            self.assertTrue(all(path.exists() for path in paths.values()))
            self.assertEqual(json.loads(paths["artifact_bundle"].read_text(encoding="utf-8"))["bundle_kind"], "artifact_bundle")
            final_package = json.loads(paths["final_package"].read_text(encoding="utf-8"))
            self.assertEqual(final_package["package_kind"], "final_package")
            self.assertEqual(final_package["checkpoint_summary"]["checkpoint_status"], "submission_frozen")
            self.assertEqual(json.loads(paths["hosted_contract_bundle"].read_text(encoding="utf-8"))["bundle_kind"], "hosted_contract_bundle")

            package = payload["submission_ready_package"]
            self.assertEqual(package["package_kind"], "submission_ready_package")
            self.assertEqual(package["readiness_verdict"], "submission_ready")
            self.assertTrue(package["submission_ready"])
            self.assertFalse(package["fully_automatic"])
            self.assertFalse(package["external_submission_performed"])
            self.assertEqual(package["submission_ready_export_verdict"], EXPORT_VERDICT)
            self.assertEqual(package["mechanical_package_completeness"]["status"], "passed")
            self.assertEqual(package["audit_summary"]["blocking_issue_count"], 0)
            self.assertIn("## 研究方案", package["submission_dossier"]["final_draft_markdown"])
            self.assertEqual(json.loads(paths["submission_ready_package"].read_text(encoding="utf-8")), package)

    def test_incomplete_materials_record_quality_debt_without_submission_ready_claim(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_root = Path(tmp_dir)
            output_dir = tmp_root / "submission-ready"
            payload = run_json_cli(
                "package",
                "submission-ready",
                "--input",
                str(self._workspace_with_export_verdict(tmp_root)),
                "--output-dir",
                str(output_dir),
                "--format",
                "json",
            )
            package = payload["submission_ready_package"]
            issue_ids = {issue["issue_id"] for issue in package["blocking_issues"]}

            self.assertFalse(package["submission_ready"])
            self.assertEqual(package["readiness_verdict"], "blocked")
            self.assertIn("missing_mandatory_sections", issue_ids)
            self.assertTrue(output_dir.exists())

    def test_missing_owner_export_verdict_fails_closed_before_writing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_root = Path(tmp_dir)
            output_dir = tmp_root / "submission-ready"
            exit_code, stdout, stderr = run_cli(
                "package",
                "submission-ready",
                "--input",
                str(self._complete_workspace(tmp_root, include_export_verdict=False)),
                "--output-dir",
                str(output_dir),
                "--format",
                "json",
            )

            self.assertEqual(exit_code, 1)
            self.assertEqual(stderr, "")
            self.assertIn(
                "submission_ready_export_verdict: must be one of: object",
                json.loads(stdout)["error"],
            )
            self.assertFalse(output_dir.exists())

    @staticmethod
    def _workspace_with_export_verdict(tmp_root: Path) -> Path:
        workspace = deepcopy(json.loads(FROZEN.read_text(encoding="utf-8")))
        workspace["submission_ready_export_verdict"] = EXPORT_VERDICT
        output_path = tmp_root / "incomplete-with-export-verdict.json"
        output_path.write_text(json.dumps(workspace, ensure_ascii=False), encoding="utf-8")
        return output_path

    @staticmethod
    def _complete_workspace(tmp_root: Path, *, include_export_verdict: bool) -> Path:
        workspace = deepcopy(json.loads(FROZEN.read_text(encoding="utf-8")))
        workspace["application_drafts"][-1]["sections"].extend(
            [
                {"section_key": "plan", "section_title": "研究方案", "text": "完成通讯轴筛选、时间窗验证与功能阻断。", "linked_object_ids": ["question-immune-fibrosis", "arg-001", "fit-001"]},
                {"section_key": "innovation", "section_title": "创新点", "text": "以跨细胞通讯解释纤维化重塑机制。", "linked_object_ids": ["question-immune-fibrosis", "arg-001", "fit-001"]},
            ]
        )
        for item in workspace["preliminary_evidence_pack"]["evidence_items"]:
            item["gaps"] = []
        if include_export_verdict:
            workspace["submission_ready_export_verdict"] = EXPORT_VERDICT
        output_path = tmp_root / f"complete-{include_export_verdict}.json"
        output_path.write_text(json.dumps(workspace, ensure_ascii=False), encoding="utf-8")
        return output_path
