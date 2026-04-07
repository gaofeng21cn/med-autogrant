from __future__ import annotations

import json
import os
import subprocess
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


EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_minimal.json"
INPUT_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2a_input_intake.json"
DIRECTION_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2a_direction_screening.json"
QUESTION_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2a_question_refinement.json"
ARGUMENT_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2b_argument_building.json"
FIT_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2b_fit_alignment.json"
OUTLINE_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2b_outline.json"
DRAFTING_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2c_drafting.json"
CRITIQUE_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2c_critique.json"
REVISION_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2c_revision.json"


class CliValidateWorkspaceTest(unittest.TestCase):
    def run_cli(self, *args: str) -> tuple[int, str, str]:
        stdout = StringIO()
        stderr = StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            exit_code = main(list(args))
        return exit_code, stdout.getvalue(), stderr.getvalue()

    def test_validate_workspace_accepts_p2a_input_intake_workspace(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "validate-workspace",
            "--input",
            str(INPUT_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["lifecycle_stage"], "input_intake")

    def test_validate_workspace_accepts_p2a_direction_screening_workspace(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "validate-workspace",
            "--input",
            str(DIRECTION_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["lifecycle_stage"], "direction_screening")

    def test_validate_workspace_accepts_p2b_argument_building_workspace(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "validate-workspace",
            "--input",
            str(ARGUMENT_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["lifecycle_stage"], "argument_building")

    def test_validate_workspace_accepts_p2b_fit_alignment_workspace(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "validate-workspace",
            "--input",
            str(FIT_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["lifecycle_stage"], "fit_alignment")

    def test_validate_workspace_accepts_p2b_outline_workspace(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "validate-workspace",
            "--input",
            str(OUTLINE_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["lifecycle_stage"], "outline")

    def test_validate_workspace_accepts_p2c_drafting_workspace(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "validate-workspace",
            "--input",
            str(DRAFTING_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["lifecycle_stage"], "drafting")

    def test_validate_workspace_accepts_p2c_critique_workspace(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "validate-workspace",
            "--input",
            str(CRITIQUE_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["lifecycle_stage"], "critique")

    def test_validate_workspace_accepts_p2c_revision_workspace(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "validate-workspace",
            "--input",
            str(REVISION_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["lifecycle_stage"], "revision")

    def test_summarize_workspace_exposes_current_selection_for_question_refinement(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "summarize-workspace",
            "--input",
            str(QUESTION_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertEqual(payload["lifecycle_stage"], "question_refinement")
        self.assertEqual(payload["current_selection"]["selected_direction_id"], "dir-inflammatory-remodeling")
        self.assertEqual(payload["current_selection"]["selected_question_id"], "question-immune-fibrosis")
        self.assertIsNone(payload["active_argument_chain"])

    def test_next_step_routes_each_p2a_stage_forward(self) -> None:
        cases = [
            (INPUT_EXAMPLE_PATH, "input_intake", "direction_screening"),
            (DIRECTION_EXAMPLE_PATH, "direction_screening", "question_refinement"),
            (QUESTION_EXAMPLE_PATH, "question_refinement", "argument_building"),
        ]

        for example_path, current_stage, recommended_stage in cases:
            with self.subTest(example=example_path.name):
                exit_code, stdout, stderr = self.run_cli(
                    "next-step",
                    "--input",
                    str(example_path),
                    "--format",
                    "json",
                )

                self.assertEqual(exit_code, 0)
                self.assertEqual(stderr, "")
                payload = json.loads(stdout)
                self.assertEqual(payload["current_stage"], current_stage)
                self.assertEqual(payload["recommended_stage"], recommended_stage)

    def test_summarize_workspace_exposes_active_fit_mapping_for_fit_alignment(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "summarize-workspace",
            "--input",
            str(FIT_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertEqual(payload["lifecycle_stage"], "fit_alignment")
        self.assertEqual(payload["current_selection"]["active_fit_mapping_id"], "fit-001")
        self.assertEqual(payload["active_fit_mapping"]["id"], "fit-001")
        self.assertEqual(payload["active_fit_mapping"]["argument_chain_id"], "arg-001")

    def test_next_step_routes_each_p2b_stage_forward(self) -> None:
        cases = [
            (ARGUMENT_EXAMPLE_PATH, "argument_building", "fit_alignment"),
            (FIT_EXAMPLE_PATH, "fit_alignment", "outline"),
            (OUTLINE_EXAMPLE_PATH, "outline", "drafting"),
        ]

        for example_path, current_stage, recommended_stage in cases:
            with self.subTest(example=example_path.name):
                exit_code, stdout, stderr = self.run_cli(
                    "next-step",
                    "--input",
                    str(example_path),
                    "--format",
                    "json",
                )

                self.assertEqual(exit_code, 0)
                self.assertEqual(stderr, "")
                payload = json.loads(stdout)
                self.assertEqual(payload["current_stage"], current_stage)
                self.assertEqual(payload["recommended_stage"], recommended_stage)

    def test_summarize_workspace_exposes_draft_audit_for_p2c_drafting(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "summarize-workspace",
            "--input",
            str(DRAFTING_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertEqual(payload["lifecycle_stage"], "drafting")
        self.assertEqual(payload["active_draft"]["id"], "draft-v1")
        self.assertEqual(payload["active_draft"]["section_count"], 3)
        self.assertIsNone(payload["active_revision_plan"])

    def test_next_step_routes_each_p2c_stage_forward(self) -> None:
        cases = [
            (DRAFTING_EXAMPLE_PATH, "drafting", "critique"),
            (CRITIQUE_EXAMPLE_PATH, "critique", "revision"),
            (REVISION_EXAMPLE_PATH, "revision", "critique"),
        ]

        for example_path, current_stage, recommended_stage in cases:
            with self.subTest(example=example_path.name):
                exit_code, stdout, stderr = self.run_cli(
                    "next-step",
                    "--input",
                    str(example_path),
                    "--format",
                    "json",
                )

                self.assertEqual(exit_code, 0)
                self.assertEqual(stderr, "")
                payload = json.loads(stdout)
                self.assertEqual(payload["current_stage"], current_stage)
                self.assertEqual(payload["recommended_stage"], recommended_stage)

    def test_stage_route_report_aggregates_p2a_question_refinement_without_critique_summary(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "stage-route-report",
            "--input",
            str(QUESTION_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["lifecycle_stage"], "question_refinement")
        self.assertEqual(payload["route"]["next_step"]["recommended_stage"], "argument_building")
        self.assertEqual(
            payload["route"]["summarize_workspace"]["current_selection"]["selected_question_id"],
            "question-immune-fibrosis",
        )
        self.assertNotIn("critique_summary", payload["route"])

    def test_stage_route_report_aggregates_p2b_outline_without_critique_summary(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "stage-route-report",
            "--input",
            str(OUTLINE_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["lifecycle_stage"], "outline")
        self.assertEqual(payload["route"]["next_step"]["recommended_stage"], "drafting")
        self.assertEqual(payload["route"]["summarize_workspace"]["active_fit_mapping"]["id"], "fit-001")
        self.assertEqual(payload["route"]["summarize_workspace"]["active_draft"]["id"], "draft-outline-v1")
        self.assertNotIn("critique_summary", payload["route"])

    def test_stage_route_report_aggregates_p2c_drafting_without_critique_summary(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "stage-route-report",
            "--input",
            str(DRAFTING_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["lifecycle_stage"], "drafting")
        self.assertEqual(payload["route"]["next_step"]["recommended_stage"], "critique")
        self.assertEqual(payload["route"]["summarize_workspace"]["active_draft"]["section_count"], 3)
        self.assertNotIn("critique_summary", payload["route"])

    def test_critique_summary_exposes_revision_audit_for_p2c_critique(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "critique-summary",
            "--input",
            str(CRITIQUE_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertEqual(payload["lifecycle_stage"], "critique")
        self.assertEqual(payload["critique_id"], "critique-v1")
        self.assertEqual(payload["revision_plan_id"], "revision-v1")
        self.assertEqual(payload["execution_status"], "planned")
        self.assertEqual(payload["recommended_next_stage"], "revision")

    def test_critique_summary_exposes_completed_revision_evidence_for_p2c_revision(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "critique-summary",
            "--input",
            str(REVISION_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertEqual(payload["lifecycle_stage"], "revision")
        self.assertEqual(payload["execution_status"], "completed")
        self.assertEqual(payload["pre_revision_version_label"], "v0.3")
        self.assertEqual(payload["post_revision_version_label"], "v0.4")
        self.assertIn("比较", payload["comparison_summary"])
        self.assertEqual(payload["recommended_next_stage"], "critique")

    def test_stage_route_report_aggregates_p2c_critique_with_critique_summary(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "stage-route-report",
            "--input",
            str(CRITIQUE_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["lifecycle_stage"], "critique")
        self.assertEqual(payload["route"]["next_step"]["recommended_stage"], "revision")
        self.assertEqual(payload["route"]["critique_summary"]["execution_status"], "planned")

    def test_stage_route_report_aggregates_p2c_revision_with_re_review_boundary(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "stage-route-report",
            "--input",
            str(REVISION_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["lifecycle_stage"], "revision")
        self.assertEqual(payload["route"]["next_step"]["recommended_stage"], "critique")
        self.assertEqual(payload["route"]["critique_summary"]["execution_status"], "completed")

    def test_validate_workspace_json_output(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "validate-workspace",
            "--input",
            str(EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")

        payload = json.loads(stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["grant_run_id"], "grant-run-nsfc-demo-001-baseline-001")
        self.assertEqual(payload["workspace_id"], "nsfc-demo-001")
        self.assertEqual(payload["lifecycle_stage"], "critique")
        self.assertEqual(payload["error_count"], 0)
        self.assertEqual(payload["errors"], [])

    def test_critique_summary_json_output(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "critique-summary",
            "--input",
            str(EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")

        payload = json.loads(stdout)
        self.assertEqual(payload["grant_run_id"], "grant-run-nsfc-demo-001-baseline-001")
        self.assertEqual(payload["critique_id"], "critique-v1")
        self.assertEqual(payload["draft_id"], "draft-v1")
        self.assertEqual(payload["verdict"], "major_revision")
        self.assertEqual(payload["necessity_scientific_value"]["weight"], 60)
        self.assertEqual(payload["applicant_fit"]["weight"], 30)
        self.assertEqual(payload["feasibility"]["weight"], 10)
        self.assertIn("必要性表述仍略偏现象描述。", payload["blocking_issues"])

    def test_module_invocation_outputs_summary(self) -> None:
        env = dict(os.environ)
        env["PYTHONPATH"] = str(SRC_ROOT)

        completed = subprocess.run(
            [
                sys.executable,
                "-m",
                "med_autogrant.cli",
                "summarize-workspace",
                "--input",
                str(EXAMPLE_PATH),
                "--format",
                "json",
            ],
            check=False,
            capture_output=True,
            text=True,
            env=env,
            cwd=REPO_ROOT,
        )

        self.assertEqual(completed.returncode, 0)
        payload = json.loads(completed.stdout)
        self.assertEqual(payload["grant_run_id"], "grant-run-nsfc-demo-001-baseline-001")
        self.assertEqual(payload["workspace_id"], "nsfc-demo-001")
        self.assertEqual(payload["selected_question"]["id"], "question-immune-fibrosis")

    def test_stage_route_report_json_output(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "stage-route-report",
            "--input",
            str(EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")

        payload = json.loads(stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["grant_run_id"], "grant-run-nsfc-demo-001-baseline-001")
        self.assertEqual(payload["workspace_id"], "nsfc-demo-001")
        self.assertEqual(payload["lifecycle_stage"], "critique")
        self.assertEqual(
            payload["route"]["validate_workspace"]["grant_run_id"],
            "grant-run-nsfc-demo-001-baseline-001",
        )
        self.assertEqual(payload["route"]["validate_workspace"]["ok"], True)
        self.assertEqual(payload["route"]["next_step"]["recommended_stage"], "revision")
        self.assertEqual(payload["route"]["critique_summary"]["verdict"], "major_revision")

    def test_summarize_workspace_returns_structured_json_error_for_invalid_workspace(self) -> None:
        invalid_path = self.write_invalid_workspace()

        exit_code, stdout, stderr = self.run_cli(
            "summarize-workspace",
            "--input",
            str(invalid_path),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 1)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertFalse(payload["ok"])
        self.assertEqual(payload["command"], "summarize-workspace")
        self.assertEqual(payload["grant_run_id"], "grant-run-nsfc-demo-001-baseline-001")
        self.assertEqual(payload["workspace_id"], "nsfc-demo-001")
        self.assertEqual(payload["lifecycle_stage"], "critique")
        self.assertEqual(payload["errors"][0]["path"], "revision_plans")
        self.assertEqual(payload["errors"][0]["message"], "critique 阶段必须存在非空 RevisionPlan。")
        self.assertIn("critique 阶段必须存在非空 RevisionPlan", payload["error"])

    def test_next_step_returns_structured_json_error_for_invalid_workspace(self) -> None:
        invalid_path = self.write_invalid_workspace()

        exit_code, stdout, stderr = self.run_cli(
            "next-step",
            "--input",
            str(invalid_path),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 1)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertFalse(payload["ok"])
        self.assertEqual(payload["command"], "next-step")
        self.assertEqual(payload["grant_run_id"], "grant-run-nsfc-demo-001-baseline-001")
        self.assertEqual(payload["workspace_id"], "nsfc-demo-001")
        self.assertEqual(payload["lifecycle_stage"], "critique")
        self.assertEqual(payload["errors"][0]["path"], "revision_plans")
        self.assertEqual(payload["errors"][0]["message"], "critique 阶段必须存在非空 RevisionPlan。")
        self.assertIn("critique 阶段必须存在非空 RevisionPlan", payload["error"])

    def test_critique_summary_returns_structured_json_error_for_invalid_workspace(self) -> None:
        invalid_path = self.write_invalid_workspace()

        exit_code, stdout, stderr = self.run_cli(
            "critique-summary",
            "--input",
            str(invalid_path),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 1)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertFalse(payload["ok"])
        self.assertEqual(payload["command"], "critique-summary")
        self.assertEqual(payload["grant_run_id"], "grant-run-nsfc-demo-001-baseline-001")
        self.assertEqual(payload["workspace_id"], "nsfc-demo-001")
        self.assertEqual(payload["lifecycle_stage"], "critique")
        self.assertEqual(payload["errors"][0]["path"], "revision_plans")
        self.assertEqual(payload["errors"][0]["message"], "critique 阶段必须存在非空 RevisionPlan。")
        self.assertIn("critique 阶段必须存在非空 RevisionPlan", payload["error"])

    def test_stage_route_report_returns_structured_json_error_for_outline_only_critique_draft(self) -> None:
        invalid_path = self.write_outline_only_critique_workspace()

        exit_code, stdout, stderr = self.run_cli(
            "stage-route-report",
            "--input",
            str(invalid_path),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 1)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertFalse(payload["ok"])
        self.assertEqual(payload["command"], "stage-route-report")
        self.assertEqual(payload["grant_run_id"], "grant-run-nsfc-demo-001-baseline-001")
        self.assertEqual(payload["workspace_id"], "nsfc-demo-001")
        self.assertEqual(payload["lifecycle_stage"], "critique")
        self.assertEqual(payload["errors"][0]["path"], "application_drafts.status")
        self.assertEqual(payload["errors"][0]["message"], "critique 阶段的激活草稿 status 必须为 draft 或 revised。")
        self.assertIn("critique 阶段的激活草稿 status 必须为 draft 或 revised", payload["error"])

    def test_next_step_returns_structured_json_error_for_revision_stage_with_outline_draft(self) -> None:
        invalid_path = self.write_revision_outline_workspace()

        exit_code, stdout, stderr = self.run_cli(
            "next-step",
            "--input",
            str(invalid_path),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 1)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertFalse(payload["ok"])
        self.assertEqual(payload["command"], "next-step")
        self.assertEqual(payload["grant_run_id"], "grant-run-nsfc-demo-001-baseline-001")
        self.assertEqual(payload["workspace_id"], "nsfc-demo-001")
        self.assertEqual(payload["lifecycle_stage"], "revision")
        self.assertEqual(payload["errors"][0]["path"], "application_drafts.status")
        self.assertEqual(payload["errors"][0]["message"], "revision 阶段的激活草稿 status 必须为 draft 或 revised。")
        self.assertIn("revision 阶段的激活草稿 status 必须为 draft 或 revised", payload["error"])

    def test_validate_workspace_reports_revision_transition_error_when_completed_plan_does_not_switch_status(self) -> None:
        invalid_path = self.write_revision_completed_without_revised_workspace()

        exit_code, stdout, stderr = self.run_cli(
            "validate-workspace",
            "--input",
            str(invalid_path),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 1)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertFalse(payload["ok"])
        self.assertEqual(payload["grant_run_id"], "grant-run-nsfc-demo-001-baseline-001")
        self.assertEqual(payload["workspace_id"], "nsfc-demo-001")
        self.assertEqual(payload["lifecycle_stage"], "revision")
        self.assertGreaterEqual(payload["error_count"], 1)
        messages = {(item["path"], item["message"]) for item in payload["errors"]}
        self.assertIn(
            (
                "application_drafts.status",
                "revision plan 已标记 completed 时，激活草稿 status 必须显式切换为 revised。",
            ),
            messages,
        )

    def test_next_step_routes_completed_revision_back_to_critique(self) -> None:
        valid_path = self.write_completed_revision_workspace()

        exit_code, stdout, stderr = self.run_cli(
            "next-step",
            "--input",
            str(valid_path),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertEqual(payload["grant_run_id"], "grant-run-nsfc-demo-001-baseline-001")
        self.assertEqual(payload["current_stage"], "revision")
        self.assertEqual(payload["recommended_stage"], "critique")
        self.assertIn("revised", payload["reason"])

    def write_invalid_workspace(self) -> Path:
        payload = json.loads(EXAMPLE_PATH.read_text(encoding="utf-8"))
        payload["revision_plans"][0]["items"] = []

        tmp_dir = Path(tempfile.mkdtemp(prefix="med-autogrant-cli-test-"))
        invalid_path = tmp_dir / "invalid-workspace.json"
        invalid_path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        return invalid_path

    def write_outline_only_critique_workspace(self) -> Path:
        payload = json.loads(EXAMPLE_PATH.read_text(encoding="utf-8"))
        payload["application_drafts"][0]["status"] = "outline"
        payload["application_drafts"][0]["sections"] = []

        tmp_dir = Path(tempfile.mkdtemp(prefix="med-autogrant-cli-test-"))
        invalid_path = tmp_dir / "outline-only-critique-workspace.json"
        invalid_path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        return invalid_path

    def write_revision_outline_workspace(self) -> Path:
        payload = json.loads(EXAMPLE_PATH.read_text(encoding="utf-8"))
        payload["lifecycle_stage"] = "revision"
        payload["application_drafts"][0]["status"] = "outline"

        tmp_dir = Path(tempfile.mkdtemp(prefix="med-autogrant-cli-test-"))
        invalid_path = tmp_dir / "revision-outline-workspace.json"
        invalid_path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        return invalid_path

    def write_revision_completed_without_revised_workspace(self) -> Path:
        payload = json.loads(EXAMPLE_PATH.read_text(encoding="utf-8"))
        payload["lifecycle_stage"] = "revision"
        payload["revision_plans"][0]["execution_status"] = "completed"
        payload["revision_plans"][0]["pre_revision_version_label"] = "v0.3"
        payload["revision_plans"][0]["post_revision_version_label"] = "v0.4"
        payload["revision_plans"][0]["comparison_summary"] = "已按批注完成修订，但尚未切换草稿状态。"

        tmp_dir = Path(tempfile.mkdtemp(prefix="med-autogrant-cli-test-"))
        invalid_path = tmp_dir / "revision-completed-without-revised.json"
        invalid_path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        return invalid_path

    def write_completed_revision_workspace(self) -> Path:
        payload = json.loads(EXAMPLE_PATH.read_text(encoding="utf-8"))
        payload["lifecycle_stage"] = "revision"
        payload["application_drafts"][0]["status"] = "revised"
        payload["application_drafts"][0]["version_label"] = "v0.4"
        payload["revision_plans"][0]["execution_status"] = "completed"
        payload["revision_plans"][0]["pre_revision_version_label"] = "v0.3"
        payload["revision_plans"][0]["post_revision_version_label"] = "v0.4"
        payload["revision_plans"][0]["comparison_summary"] = "已根据 major_revision 完成立项依据与机制链条修订。"

        tmp_dir = Path(tempfile.mkdtemp(prefix="med-autogrant-cli-test-"))
        valid_path = tmp_dir / "revision-completed.json"
        valid_path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        return valid_path


if __name__ == "__main__":
    unittest.main()
