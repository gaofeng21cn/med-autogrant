from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from typing import Any

from support.cli import run_cli, run_json_cli  # noqa: E402


REPO_ROOT = Path(__file__).resolve().parents[1]
FREEZE_READY = REPO_ROOT / "examples" / "nsfc_workspace_p3a_ready_for_submission.json"
FROZEN = REPO_ROOT / "examples" / "nsfc_workspace_p3c_presubmission_frozen.json"
FORWARD = REPO_ROOT / "examples" / "nsfc_workspace_p2c_revision.json"
MISSING = object()


def _mutate(payload: dict[str, Any], path: tuple[str | int, ...], value: object) -> None:
    target: Any = payload
    for key in path[:-1]:
        target = target[key]
    if value is MISSING:
        target.pop(path[-1])
    else:
        target[path[-1]] = value


class FinalPackageTest(unittest.TestCase):
    def test_final_package_accepts_only_final_gate_states(self) -> None:
        cases = (
            (FREEZE_READY, "critique", "freeze_ready", "revised", False),
            (FROZEN, "frozen", "submission_frozen", "frozen", True),
        )
        for input_path, lifecycle_stage, checkpoint, draft_status, presubmission_frozen in cases:
            with self.subTest(checkpoint=checkpoint), tempfile.TemporaryDirectory() as tmp_dir:
                bundle_path = Path(tmp_dir) / "bundle.json"
                package_path = Path(tmp_dir) / "final.json"
                self._build_bundle(input_path, bundle_path)
                payload = self._build_final(input_path, bundle_path, package_path)
                final_package = payload["final_package"]
                bundle = json.loads(bundle_path.read_text(encoding="utf-8"))

                self.assertEqual(payload["command"], "build-final-package")
                self.assertEqual(payload["grant_run_id"], "grant-run-nsfc-demo-001-baseline-001")
                self.assertEqual(payload["workspace_id"], "nsfc-demo-001")
                self.assertEqual(payload["draft_id"], "draft-v1")
                self.assertEqual(payload["lifecycle_stage"], lifecycle_stage)
                self.assertEqual(payload["output_path"], str(package_path.resolve()))
                self.assertEqual(final_package["package_version"], 1)
                self.assertEqual(final_package["package_kind"], "final_package")
                self.assertEqual(
                    {
                        field: final_package[field]
                        for field in ("grant_run_id", "workspace_id", "draft_id", "lifecycle_stage")
                    },
                    {
                        "grant_run_id": payload["grant_run_id"],
                        "workspace_id": payload["workspace_id"],
                        "draft_id": payload["draft_id"],
                        "lifecycle_stage": lifecycle_stage,
                    },
                )
                self.assertEqual(
                    final_package["freeze_manifest"],
                    {
                        "draft_version_label": "v0.4",
                        "draft_status": draft_status,
                        "active_revision_plan_id": "revision-v1",
                        "critique_id": "critique-v1",
                        "checkpoint_status": checkpoint,
                        "presubmission_frozen": presubmission_frozen,
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
                self.assertEqual(final_package["checkpoint_summary"]["checkpoint_status"], checkpoint)
                self.assertEqual(
                    final_package["export_summary"],
                    {"outline_count": 2, "section_count": 3, "artifact_count": 6},
                )
                self.assertEqual(
                    final_package["deliverables"],
                    {
                        "artifact_bundle_manifest": bundle["manifest"],
                        "final_draft_outline": bundle["artifacts"]["draft_outline"],
                        "final_draft_sections": bundle["artifacts"]["draft_sections"],
                    },
                )
                self.assertEqual(json.loads(package_path.read_text(encoding="utf-8")), final_package)

    def test_nonfinal_checkpoint_materializes_quality_debt_but_identity_mismatch_fails_closed(self) -> None:
        for input_path in (FORWARD,):
            with self.subTest(input_path=input_path.name), tempfile.TemporaryDirectory() as tmp_dir:
                bundle_path = Path(tmp_dir) / "bundle.json"
                package_path = Path(tmp_dir) / "final.json"
                self._build_bundle(input_path, bundle_path)
                payload = self._build_final(input_path, bundle_path, package_path)
                self.assertTrue(payload["ok"])
                self.assertEqual(payload["status"], "completed_with_quality_debt")
                self.assertTrue(payload["next_stage_may_start"])
                self.assertFalse(payload["quality_debt"]["blocks_stage_transition"])
                self.assertIn(
                    "checkpoint_status_not_final",
                    " ".join(payload["quality_debt"]["reasons"]),
                )
                self.assertTrue(package_path.exists())

        for field in ("grant_run_id", "workspace_id", "draft_id"):
            with self.subTest(output_identity_field=field), tempfile.TemporaryDirectory() as tmp_dir:
                bundle_path = Path(tmp_dir) / "bundle.json"
                package_path = Path(tmp_dir) / "final.json"
                self._build_bundle(FROZEN, bundle_path)
                existing = {
                    "grant_run_id": "grant-run-nsfc-demo-001-baseline-001",
                    "workspace_id": "nsfc-demo-001",
                    "draft_id": "draft-v1",
                }
                existing[field] = "other"
                package_path.write_text(json.dumps(existing), encoding="utf-8")
                self._assert_failure(
                    FROZEN,
                    bundle_path,
                    package_path,
                    "final package output identity 不匹配",
                    package_must_be_absent=False,
                )
                self.assertEqual(json.loads(package_path.read_text(encoding="utf-8")), existing)

    def test_manual_artifact_bundle_validator_fails_closed_across_shape_boundaries(self) -> None:
        cases: tuple[tuple[tuple[str | int, ...], object, str], ...] = (
            (
                ("lifecycle_stage",),
                MISSING,
                "artifact bundle 缺少必填字段: lifecycle_stage",
            ),
            (("bundle_kind",), "other", "artifact bundle kind 非法"),
            (("grant_run_id",), "other", "artifact bundle identity 不匹配"),
            (("workspace_id",), "other", "artifact bundle identity 不匹配"),
            (("draft_id",), "other", "artifact bundle identity 不匹配"),
            (("manifest",), MISSING, "artifact bundle 缺少必填字段: manifest"),
            (
                ("selection", "selected_direction_id"),
                MISSING,
                "artifact bundle selection 缺少字段: selected_direction_id",
            ),
            (("manifest", "draft_status"), None, "artifact bundle manifest.draft_status 非法"),
            (("bundle_summary", "outline_count"), True, "artifact bundle bundle_summary.outline_count 非法"),
            (("artifacts", "draft_outline"), {}, "artifact bundle artifacts.draft_outline 非法"),
            (("artifacts", "draft_sections", 0), None, "artifact bundle artifacts.draft_sections[0] 非法"),
            (
                ("artifacts", "draft_outline", 0, "core_claim"),
                MISSING,
                "artifact bundle artifacts.draft_outline[0] 缺少字段: core_claim",
            ),
            (
                ("artifacts", "draft_sections", 0, "section_title"),
                None,
                "artifact bundle artifacts.draft_sections[0].section_title 非法",
            ),
            (
                ("artifacts", "draft_outline", 0, "linked_object_ids"),
                {},
                "artifact bundle artifacts.draft_outline[0].linked_object_ids 非法",
            ),
            (
                ("artifacts", "draft_sections", 0, "linked_object_ids"),
                [None],
                "artifact bundle artifacts.draft_sections[0].linked_object_ids[0] 非法",
            ),
            (("artifacts", "selected_direction"), [], "artifact bundle artifacts.selected_direction 非法"),
            (
                ("artifacts", "selected_direction", "direction_id"),
                None,
                "artifact bundle artifacts.selected_direction.direction_id 非法",
            ),
            (
                ("artifacts", "selected_question", "parent_direction_id"),
                None,
                "artifact bundle artifacts.selected_question.parent_direction_id 非法",
            ),
            (
                ("artifacts", "selected_direction", "title"),
                None,
                "artifact bundle artifacts.selected_direction.title 非法",
            ),
            (
                ("artifacts", "selected_direction", "required_evidence_ids"),
                {},
                "artifact bundle artifacts.selected_direction.required_evidence_ids 非法",
            ),
            (
                ("artifacts", "selected_direction", "required_evidence_ids"),
                [None],
                "artifact bundle artifacts.selected_direction.required_evidence_ids[0] 非法",
            ),
        )

        for case_path, value, error in cases:
            with self.subTest(path=case_path), tempfile.TemporaryDirectory() as tmp_dir:
                bundle_path = Path(tmp_dir) / "bundle.json"
                package_path = Path(tmp_dir) / "final.json"
                self._build_bundle(FROZEN, bundle_path)
                bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
                _mutate(bundle, case_path, value)
                bundle_path.write_text(json.dumps(bundle, ensure_ascii=False), encoding="utf-8")
                self._assert_failure(FROZEN, bundle_path, package_path, error)

    @staticmethod
    def _build_bundle(input_path: Path, output_path: Path) -> None:
        run_json_cli(
            "package", "artifact-bundle", "--input", str(input_path), "--output", str(output_path), "--format", "json"
        )

    @staticmethod
    def _build_final(input_path: Path, bundle_path: Path, package_path: Path) -> dict[str, Any]:
        return run_json_cli(
            "package",
            "final-package",
            "--input",
            str(input_path),
            "--artifact-bundle",
            str(bundle_path),
            "--output",
            str(package_path),
            "--format",
            "json",
        )

    def _assert_failure(
        self,
        input_path: Path,
        bundle_path: Path,
        package_path: Path,
        error: str,
        *,
        package_must_be_absent: bool = True,
    ) -> None:
        exit_code, stdout, stderr = run_cli(
            "package",
            "final-package",
            "--input",
            str(input_path),
            "--artifact-bundle",
            str(bundle_path),
            "--output",
            str(package_path),
            "--format",
            "json",
        )
        self.assertEqual(exit_code, 1)
        self.assertEqual(stderr, "")
        self.assertIn(error, json.loads(stdout)["error"])
        if package_must_be_absent:
            self.assertFalse(package_path.exists())
