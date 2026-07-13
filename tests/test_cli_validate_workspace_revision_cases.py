from __future__ import annotations

import tempfile
from pathlib import Path

from cli_validate_cases import (
    CRITIQUE_EXAMPLE_PATH,
    DRAFTING_EXAMPLE_PATH,
    FORCED_ROLLBACK_EXAMPLE_PATH,
    MAJOR_REFRAME_EXAMPLE_PATH,
    OUTLINE_EXAMPLE_PATH,
    PRESUBMISSION_FROZEN_EXAMPLE_PATH,
    QUESTION_EXAMPLE_PATH,
    READY_FOR_SUBMISSION_EXAMPLE_PATH,
    REVISION_EXAMPLE_PATH,
    RE_REVIEW_EXAMPLE_PATH,
    CliValidateWorkspaceTest,
)


class CliValidateWorkspaceRevisionCasesTest(CliValidateWorkspaceTest):
    def test_route_report_preserves_late_stage_branches(self) -> None:
        cases = (
            (QUESTION_EXAMPLE_PATH, "question_refinement", "argument_building", "forward_progress"),
            (OUTLINE_EXAMPLE_PATH, "outline", "drafting", "forward_progress"),
            (DRAFTING_EXAMPLE_PATH, "drafting", "critique", "forward_progress"),
            (CRITIQUE_EXAMPLE_PATH, "critique", "revision", "forward_progress"),
            (REVISION_EXAMPLE_PATH, "revision", "critique", "forward_progress"),
            (MAJOR_REFRAME_EXAMPLE_PATH, "critique", "question_refinement", "forward_progress"),
            (READY_FOR_SUBMISSION_EXAMPLE_PATH, "critique", "frozen", "freeze_ready"),
            (RE_REVIEW_EXAMPLE_PATH, "critique", "revision", "forward_progress"),
            (FORCED_ROLLBACK_EXAMPLE_PATH, "critique", "argument_building", "route_back_recommended"),
            (PRESUBMISSION_FROZEN_EXAMPLE_PATH, "frozen", "frozen", "submission_frozen"),
        )

        for input_path, stage, recommended_stage, checkpoint in cases:
            with self.subTest(example=input_path.name):
                payload = self.run_workspace_json("route-report", input_path)
                self.assertTrue(payload["ok"])
                self.assertEqual(payload["lifecycle_stage"], stage)
                self.assertEqual(payload["route"]["next_step"]["recommended_stage"], recommended_stage)
                self.assertEqual(payload["verification_checkpoint"]["checkpoint_status"], checkpoint)

        rereview = self.run_workspace_json("route-report", RE_REVIEW_EXAMPLE_PATH)
        self.assertEqual(
            rereview["verification_checkpoint"]["review_checkpoint"]
            ["reviewed_revision_evidence"]["revision_plan_id"],
            "revision-v1",
        )
        rollback = self.run_workspace_json("route-report", FORCED_ROLLBACK_EXAMPLE_PATH)
        self.assertEqual(rollback["route"]["next_step"]["forced_rollback_stage"], "argument_building")

    def test_critique_summary_preserves_revision_branch_evidence(self) -> None:
        cases = (
            (
                CRITIQUE_EXAMPLE_PATH,
                {
                    "lifecycle_stage": "critique",
                    "critique_id": "critique-v1",
                    "revision_plan_id": "revision-v1",
                    "execution_status": "planned",
                    "recommended_next_stage": "revision",
                },
            ),
            (
                REVISION_EXAMPLE_PATH,
                {
                    "lifecycle_stage": "revision",
                    "execution_status": "completed",
                    "pre_revision_version_label": "v0.3",
                    "post_revision_version_label": "v0.4",
                    "recommended_next_stage": "critique",
                },
            ),
            (
                MAJOR_REFRAME_EXAMPLE_PATH,
                {"verdict": "major_reframe", "recommended_next_stage": "question_refinement"},
            ),
            (
                READY_FOR_SUBMISSION_EXAMPLE_PATH,
                {"verdict": "ready_for_submission", "recommended_next_stage": "frozen"},
            ),
            (
                RE_REVIEW_EXAMPLE_PATH,
                {
                    "critique_id": "critique-v2",
                    "revision_plan_id": "revision-v2",
                    "reviewed_revision_plan_id": "revision-v1",
                },
            ),
            (
                FORCED_ROLLBACK_EXAMPLE_PATH,
                {
                    "critique_id": "critique-v2",
                    "forced_rollback_stage": "argument_building",
                    "presubmission_frozen": False,
                    "recommended_next_stage": "argument_building",
                },
            ),
            (
                PRESUBMISSION_FROZEN_EXAMPLE_PATH,
                {
                    "lifecycle_stage": "frozen",
                    "verdict": "ready_for_submission",
                    "presubmission_frozen": True,
                    "recommended_next_stage": "frozen",
                },
            ),
        )
        for input_path, expected in cases:
            with self.subTest(example=input_path.name):
                payload = self.run_workspace_json("critique-summary", input_path)
                for field, value in expected.items():
                    self.assertEqual(payload[field], value)

    def test_validate_accepts_late_revision_fixtures(self) -> None:
        for input_path, lifecycle_stage in (
            (RE_REVIEW_EXAMPLE_PATH, "critique"),
            (FORCED_ROLLBACK_EXAMPLE_PATH, "critique"),
            (PRESUBMISSION_FROZEN_EXAMPLE_PATH, "frozen"),
        ):
            with self.subTest(example=input_path.name):
                payload = self.run_workspace_json("validate", input_path)
                self.assertTrue(payload["ok"])
                self.assertEqual(payload["lifecycle_stage"], lifecycle_stage)

    def test_generated_revision_roundtrip_reenters_all_read_surfaces(self) -> None:
        cases = (
            (CRITIQUE_EXAMPLE_PATH, "v0.4", None),
            (RE_REVIEW_EXAMPLE_PATH, "v0.5", "revision-v1"),
        )

        with tempfile.TemporaryDirectory() as tmp_dir:
            for input_path, version, reviewed_plan_id in cases:
                with self.subTest(example=input_path.name):
                    output_path = Path(tmp_dir) / f"{input_path.stem}-revised.json"
                    revised = self.run_json_cli(
                        "pass", "revision", "--input", str(input_path),
                        "--output", str(output_path), "--format", "json",
                    )
                    validated = self.run_workspace_json("validate", output_path)
                    summary = self.run_workspace_json("summarize", output_path)
                    critique = self.run_workspace_json("critique-summary", output_path)
                    route = self.run_workspace_json("route-report", output_path)

                    self.assertTrue(revised["ok"])
                    self.assertTrue(validated["ok"])
                    self.assertEqual(validated["lifecycle_stage"], "critique")
                    self.assertEqual(summary["active_draft"]["status"], "revised")
                    self.assertEqual(summary["active_draft"]["version_label"], version)
                    self.assertEqual(summary["active_revision_plan"]["execution_status"], "completed")
                    self.assertEqual(critique["reviewed_revision_plan_id"], reviewed_plan_id)
                    self.assertEqual(critique["draft_status"], "revised")
                    self.assertEqual(critique["draft_version_label"], version)
                    self.assertEqual(route["route"]["next_step"]["recommended_stage"], "critique")
                    self.assertEqual(route["verification_checkpoint"]["checkpoint_status"], "forward_progress")
                    self.assertEqual(
                        route["route"]["critique_summary"]["reviewed_revision_plan_id"],
                        reviewed_plan_id,
                    )

    def test_presubmission_frozen_gate_stays_closed(self) -> None:
        summary = self.run_workspace_json("summarize", PRESUBMISSION_FROZEN_EXAMPLE_PATH)
        critique = self.run_workspace_json("critique-summary", PRESUBMISSION_FROZEN_EXAMPLE_PATH)
        route = self.run_workspace_json("route-report", PRESUBMISSION_FROZEN_EXAMPLE_PATH)

        self.assertEqual(summary["lifecycle_stage"], "frozen")
        self.assertTrue(summary["gates"]["presubmission_frozen"])
        self.assertEqual(summary["active_draft"]["status"], "frozen")
        self.assertTrue(critique["presubmission_frozen"])
        self.assertEqual(critique["recommended_next_stage"], "frozen")
        self.assertTrue(route["verification_checkpoint"]["route_alignment"]["presubmission_frozen"])
