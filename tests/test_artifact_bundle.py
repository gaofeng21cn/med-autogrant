from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from typing import Any

from med_autogrant.revision_executor import build_revision_execution_payload  # noqa: E402
from support.cli import run_cli, run_json_cli  # noqa: E402


REPO_ROOT = Path(__file__).resolve().parents[1]
OUTLINE_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2b_outline.json"
REVISION_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2c_revision.json"
RE_REVIEW_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p3b_re_review_major_revision.json"


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


class ArtifactBundleTest(unittest.TestCase):
    def test_artifact_bundle_projects_stage_specific_refs(self) -> None:
        cases = (
            (
                OUTLINE_EXAMPLE_PATH,
                "outline",
                "draft-outline-v1",
                "outline-v1",
                "outline",
                "specific_aims_and_structure",
                "specific_aims_structure_manifest_ref",
                2,
                0,
            ),
            (
                REVISION_EXAMPLE_PATH,
                "revision",
                "draft-v1",
                "v0.4",
                "revised",
                "proposal_authoring",
                "reviewable_grant_artifact_bundle_ref",
                2,
                3,
            ),
        )
        for input_path, lifecycle_stage, draft_id, version_label, draft_status, stage_id, output_role, outline_count, section_count in cases:
            with self.subTest(stage=stage_id), tempfile.TemporaryDirectory() as tmp_dir:
                output_path = Path(tmp_dir) / "bundle.json"
                payload = run_json_cli(
                    "package",
                    "artifact-bundle",
                    "--input",
                    str(input_path),
                    "--output",
                    str(output_path),
                    "--format",
                    "json",
                )
                bundle = payload["bundle"]

                self.assertEqual(payload["command"], "build-artifact-bundle")
                self.assertEqual(payload["grant_run_id"], "grant-run-nsfc-demo-001-baseline-001")
                self.assertEqual(payload["workspace_id"], "nsfc-demo-001")
                self.assertEqual(payload["draft_id"], draft_id)
                self.assertEqual(payload["lifecycle_stage"], lifecycle_stage)
                self.assertEqual(payload["output_path"], str(output_path.resolve()))
                self.assertEqual(bundle["bundle_version"], 1)
                self.assertEqual(bundle["bundle_kind"], "artifact_bundle")
                self.assertEqual(bundle["grant_run_id"], payload["grant_run_id"])
                self.assertEqual(bundle["workspace_id"], payload["workspace_id"])
                self.assertEqual(bundle["draft_id"], draft_id)
                self.assertEqual(bundle["lifecycle_stage"], lifecycle_stage)
                self.assertEqual(
                    bundle["selection"],
                    {
                        "selected_direction_id": "dir-inflammatory-remodeling",
                        "selected_question_id": "question-immune-fibrosis",
                        "active_fit_mapping_id": "fit-001",
                        "active_draft_id": draft_id,
                    },
                )
                self.assertEqual(
                    {field: bundle["manifest"][field] for field in ("direction_id", "question_id", "argument_chain_id", "fit_mapping_id", "draft_id", "draft_version_label", "draft_status")},
                    {
                        "direction_id": "dir-inflammatory-remodeling",
                        "question_id": "question-immune-fibrosis",
                        "argument_chain_id": "arg-001",
                        "fit_mapping_id": "fit-001",
                        "draft_id": draft_id,
                        "draft_version_label": version_label,
                        "draft_status": draft_status,
                    },
                )
                self.assertEqual(
                    bundle["lineage"],
                    {
                        "frozen_question_id": "question-immune-fibrosis",
                        "argument_chain_id": "arg-001",
                        "fit_mapping_id": "fit-001",
                        "draft_id": draft_id,
                    },
                )
                self.assertEqual(bundle["bundle_summary"], {"outline_count": outline_count, "section_count": section_count})
                self.assertEqual(bundle["artifacts"]["selected_direction"]["direction_id"], "dir-inflammatory-remodeling")
                self.assertEqual(bundle["artifacts"]["selected_question"]["question_id"], "question-immune-fibrosis")
                self.assertEqual(bundle["artifacts"]["argument_chain"]["argument_chain_id"], "arg-001")
                self.assertEqual(bundle["artifacts"]["fit_mapping"]["fit_mapping_id"], "fit-001")
                self.assertEqual(len(bundle["artifacts"]["draft_outline"]), outline_count)
                self.assertEqual(len(bundle["artifacts"]["draft_sections"]), section_count)
                self._assert_projection(bundle, stage_id, output_role)
                self.assertEqual(json.loads(output_path.read_text(encoding="utf-8")), bundle)

    def test_rereview_revision_output_is_consumable_by_artifact_owner(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            revised_path = Path(tmp_dir) / "revised.json"
            bundle_path = Path(tmp_dir) / "bundle.json"
            build_revision_execution_payload(_load(RE_REVIEW_EXAMPLE_PATH), output_path=revised_path)
            bundle = run_json_cli(
                "package",
                "artifact-bundle",
                "--input",
                str(revised_path),
                "--output",
                str(bundle_path),
                "--format",
                "json",
            )["bundle"]

            self.assertEqual(bundle["grant_run_id"], "grant-run-nsfc-demo-001-baseline-001")
            self.assertEqual(bundle["workspace_id"], "nsfc-demo-001")
            self.assertEqual(bundle["draft_id"], "draft-v1")
            self.assertEqual(bundle["lifecycle_stage"], "critique")
            self.assertEqual(bundle["manifest"]["draft_version_label"], "v0.5")
            self.assertEqual(
                bundle["lineage"],
                {
                    "frozen_question_id": "question-immune-fibrosis",
                    "argument_chain_id": "arg-001",
                    "fit_mapping_id": "fit-001",
                    "draft_id": "draft-v1",
                },
            )
            self.assertEqual(len(bundle["artifacts"]["draft_sections"]), 3)
            self._assert_projection(bundle, "review_and_rebuttal", "review_quality_closure_receipt_ref")

    def test_artifact_output_identity_guard_preserves_existing_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            output_path = Path(tmp_dir) / "bundle.json"
            existing = {"grant_run_id": "other-run", "workspace_id": "other-workspace", "draft_id": "other-draft"}
            output_path.write_text(json.dumps(existing), encoding="utf-8")

            exit_code, stdout, stderr = run_cli(
                "package",
                "artifact-bundle",
                "--input",
                str(REVISION_EXAMPLE_PATH),
                "--output",
                str(output_path),
                "--format",
                "json",
            )
            self.assertEqual(exit_code, 1)
            self.assertEqual(stderr, "")
            self.assertIn("bundle output identity 不匹配", json.loads(stdout)["error"])
            self.assertEqual(json.loads(output_path.read_text(encoding="utf-8")), existing)

    def _assert_projection(self, bundle: dict[str, Any], stage_id: str, output_role: str) -> None:
        projection = bundle["stage_output_projection"]
        self.assertEqual(projection["owner"], "med-autogrant")
        self.assertEqual(projection["stage_id"], stage_id)
        self.assertEqual(projection["stage_output_role"], output_role)
        self.assertEqual(bundle["manifest"]["manifest_ref"], projection["manifest_ref"])
        self.assertEqual(bundle["manifest"]["owner_receipt_or_typed_blocker_ref"], projection["owner_receipt_or_typed_blocker_ref"])
        consumption = projection["opl_consumption"]
        self.assertEqual(consumption["role"], "refs_manifest_receipt_only")
        for field in (
            "can_read_artifact_body",
            "can_write_grant_truth",
            "can_infer_fundability",
            "can_infer_quality",
            "can_infer_export",
            "can_infer_submission_ready",
        ):
            self.assertFalse(consumption[field])
