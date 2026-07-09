from __future__ import annotations

import tempfile
from pathlib import Path

from med_autogrant.route_report import build_stage_route_report
from med_autogrant.workspace import load_workspace_document

from .context import (
    FORWARD_PROGRESS_EXAMPLE_PATH,
    FREEZE_READY_EXAMPLE_PATH,
    FROZEN_EXAMPLE_PATH,
    FinalPackageCliCase,
)


class TestFinalPackageBuildCases(FinalPackageCliCase):
    def test_build_final_package_writes_freeze_ready_package(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            bundle_path = Path(tmp_dir) / "freeze-ready-bundle.json"
            package_path = Path(tmp_dir) / "freeze-ready-package.json"
            self._build_bundle(FREEZE_READY_EXAMPLE_PATH, bundle_path)

            payload = self._assert_final_package_ok(FREEZE_READY_EXAMPLE_PATH, bundle_path, package_path)
            self.assertEqual(payload["command"], "build-final-package")
            self.assertEqual(payload["grant_run_id"], "grant-run-nsfc-demo-001-baseline-001")
            self.assertEqual(payload["workspace_id"], "nsfc-demo-001")
            self.assertEqual(payload["draft_id"], "draft-v1")
            self.assertEqual(payload["lifecycle_stage"], "critique")
            self.assertEqual(payload["output_path"], str(package_path.resolve()))

            final_package = payload["final_package"]
            self.assertEqual(final_package["package_version"], 1)
            self.assertEqual(final_package["package_kind"], "final_package")
            self.assertEqual(
                final_package["freeze_manifest"],
                {
                    "draft_version_label": "v0.4",
                    "draft_status": "revised",
                    "active_revision_plan_id": "revision-v1",
                    "critique_id": "critique-v1",
                    "checkpoint_status": "freeze_ready",
                    "presubmission_frozen": False,
                },
            )
            self.assertEqual(
                final_package["lineage"],
                {
                    "frozen_question_id": "question-immune-fibrosis",
                    "selected_direction_id": "dir-inflammatory-remodeling",
                    "selected_question_id": "question-immune-fibrosis",
                    "active_fit_mapping_id": "fit-001",
                    "draft_id": "draft-v1",
                    "revision_plan_id": "revision-v1",
                },
            )

            route_report = build_stage_route_report(load_workspace_document(FREEZE_READY_EXAMPLE_PATH))
            self.assertEqual(
                final_package["checkpoint_summary"],
                {
                    "verification_checkpoint": route_report["verification_checkpoint"],
                    "checkpoint_status": "freeze_ready",
                },
            )
            self.assertEqual(
                final_package["export_summary"],
                {
                    "outline_count": 2,
                    "section_count": 3,
                    "artifact_count": 6,
                },
            )

            bundle = self._read_json(bundle_path)
            self.assertEqual(final_package["deliverables"]["artifact_bundle_manifest"], bundle["manifest"])
            self.assertEqual(len(final_package["deliverables"]["final_draft_outline"]), 2)
            self.assertEqual(len(final_package["deliverables"]["final_draft_sections"]), 3)
            self.assertEqual(self._read_json(package_path), final_package)

    def test_build_final_package_writes_submission_frozen_package(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            bundle_path = Path(tmp_dir) / "frozen-bundle.json"
            package_path = Path(tmp_dir) / "frozen-package.json"
            self._build_bundle(FROZEN_EXAMPLE_PATH, bundle_path)

            payload = self._assert_final_package_ok(FROZEN_EXAMPLE_PATH, bundle_path, package_path)
            final_package = payload["final_package"]
            self.assertEqual(final_package["freeze_manifest"]["draft_status"], "frozen")
            self.assertEqual(final_package["freeze_manifest"]["checkpoint_status"], "submission_frozen")
            self.assertTrue(final_package["freeze_manifest"]["presubmission_frozen"])
            self.assertEqual(final_package["checkpoint_summary"]["checkpoint_status"], "submission_frozen")

    def test_build_final_package_fails_closed_when_checkpoint_is_not_final_gate(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            bundle_path = Path(tmp_dir) / "forward-progress-bundle.json"
            package_path = Path(tmp_dir) / "forward-progress-package.json"
            self._build_bundle(FORWARD_PROGRESS_EXAMPLE_PATH, bundle_path)

            self._assert_final_package_fails(
                FORWARD_PROGRESS_EXAMPLE_PATH,
                bundle_path,
                package_path,
                "checkpoint_status",
            )

