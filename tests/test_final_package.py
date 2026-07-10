from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from typing import Any

from med_autogrant import artifact_bundle_validation as bundle_validation  # noqa: E402
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

    def test_nonfinal_checkpoint_and_output_identity_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_root = Path(tmp_dir)
            bundle_path = tmp_root / "bundle.json"
            package_path = tmp_root / "final.json"
            self._build_bundle(FORWARD, bundle_path)
            self._assert_failure(FORWARD, bundle_path, package_path, "checkpoint_status")

            self._build_bundle(FREEZE_READY, bundle_path)
            existing = {"grant_run_id": "other", "workspace_id": "other", "draft_id": "other"}
            package_path.write_text(json.dumps(existing), encoding="utf-8")
            self._assert_failure(
                FREEZE_READY,
                bundle_path,
                package_path,
                "final package output identity 不匹配",
                package_must_be_absent=False,
            )
            self.assertEqual(json.loads(package_path.read_text(encoding="utf-8")), existing)

    def test_manual_artifact_bundle_validator_fails_closed_for_every_contract_entry(self) -> None:
        cases: list[tuple[str, tuple[str | int, ...], object, str]] = [
            (
                "lifecycle_stage",
                ("lifecycle_stage",),
                MISSING,
                "artifact bundle 缺少必填字段: lifecycle_stage",
            ),
            ("identity", ("grant_run_id",), "other", "artifact bundle identity 不匹配"),
        ]
        for field in bundle_validation.REQUIRED_ARTIFACT_BUNDLE_OBJECT_FIELDS:
            cases.append((field, (field,), None, f"artifact bundle 缺少必填字段: {field}"))
        for object_field, fields in bundle_validation.REQUIRED_ARTIFACT_BUNDLE_NESTED_FIELDS.items():
            for field in fields:
                cases.append(
                    (
                        f"required:{object_field}.{field}",
                        (object_field, field),
                        MISSING,
                        f"artifact bundle {object_field} 缺少字段: {field}",
                    )
                )
        for object_field, fields in bundle_validation.REQUIRED_ARTIFACT_BUNDLE_STRING_NESTED_FIELDS.items():
            for field in fields:
                cases.append(
                    (
                        f"string:{object_field}.{field}",
                        (object_field, field),
                        None,
                        f"artifact bundle {object_field}.{field} 非法",
                    )
                )
        for object_field, fields in bundle_validation.REQUIRED_ARTIFACT_BUNDLE_NONNEGATIVE_INT_NESTED_FIELDS.items():
            for field in fields:
                cases.append(
                    (
                        f"integer:{object_field}.{field}",
                        (object_field, field),
                        True,
                        f"artifact bundle {object_field}.{field} 非法",
                    )
                )
        for object_field, fields in bundle_validation.REQUIRED_ARTIFACT_BUNDLE_LIST_NESTED_FIELDS.items():
            for field in fields:
                cases.append(
                    (
                        f"list:{object_field}.{field}",
                        (object_field, field),
                        {},
                        f"artifact bundle {object_field}.{field} 非法",
                    )
                )
        for list_field, fields in bundle_validation.REQUIRED_ARTIFACT_BUNDLE_LIST_ELEMENT_FIELDS.items():
            cases.append(
                (
                    f"object:artifacts.{list_field}[0]",
                    ("artifacts", list_field, 0),
                    None,
                    f"artifact bundle artifacts.{list_field}[0] 非法",
                )
            )
            for field in fields:
                cases.append(
                    (
                        f"required:artifacts.{list_field}[0].{field}",
                        ("artifacts", list_field, 0, field),
                        MISSING,
                        f"artifact bundle artifacts.{list_field}[0] 缺少字段: {field}",
                    )
                )
        for list_field, fields in bundle_validation.REQUIRED_ARTIFACT_BUNDLE_LIST_ELEMENT_REQUIRED_STRING_FIELDS.items():
            for field in fields:
                cases.append(
                    (
                        f"string:artifacts.{list_field}[0].{field}",
                        ("artifacts", list_field, 0, field),
                        None,
                        f"artifact bundle artifacts.{list_field}[0].{field} 非法",
                    )
                )
        for object_field, fields in bundle_validation.REQUIRED_ARTIFACT_BUNDLE_DICT_NESTED_FIELDS.items():
            for field in fields:
                cases.append(
                    (
                        f"object:{object_field}.{field}",
                        (object_field, field),
                        [],
                        f"artifact bundle {object_field}.{field} 非法",
                    )
                )
        for list_field, fields in bundle_validation.REQUIRED_ARTIFACT_BUNDLE_LIST_ELEMENT_REQUIRED_LIST_FIELDS.items():
            for field in fields:
                cases.append(
                    (
                        f"list:artifacts.{list_field}[0].{field}",
                        ("artifacts", list_field, 0, field),
                        {},
                        f"artifact bundle artifacts.{list_field}[0].{field} 非法",
                    )
                )
        for list_field, fields in (
            bundle_validation.REQUIRED_ARTIFACT_BUNDLE_LIST_ELEMENT_REQUIRED_LIST_ELEMENT_STRING_FIELDS.items()
        ):
            for field in fields:
                cases.append(
                    (
                        f"string:artifacts.{list_field}[0].{field}[0]",
                        ("artifacts", list_field, 0, field),
                        [None],
                        f"artifact bundle artifacts.{list_field}[0].{field}[0] 非法",
                    )
                )
        for object_field, field in bundle_validation.REQUIRED_ARTIFACT_BUNDLE_ARTIFACT_OBJECT_PRIMARY_ID_FIELDS.items():
            cases.append(
                (
                    f"id:artifacts.{object_field}.{field}",
                    ("artifacts", object_field, field),
                    None,
                    f"artifact bundle artifacts.{object_field}.{field} 非法",
                )
            )
        for object_field, fields in bundle_validation.REQUIRED_ARTIFACT_BUNDLE_ARTIFACT_OBJECT_LINKAGE_ID_FIELDS.items():
            for field in fields:
                cases.append(
                    (
                        f"linkage:artifacts.{object_field}.{field}",
                        ("artifacts", object_field, field),
                        None,
                        f"artifact bundle artifacts.{object_field}.{field} 非法",
                    )
                )
        for object_field, fields in bundle_validation.REQUIRED_ARTIFACT_BUNDLE_ARTIFACT_OBJECT_REQUIRED_STRING_FIELDS.items():
            for field in fields:
                cases.append(
                    (
                        f"string:artifacts.{object_field}.{field}",
                        ("artifacts", object_field, field),
                        None,
                        f"artifact bundle artifacts.{object_field}.{field} 非法",
                    )
                )
        for object_field, fields in bundle_validation.REQUIRED_ARTIFACT_BUNDLE_ARTIFACT_OBJECT_REQUIRED_LIST_FIELDS.items():
            for field in fields:
                field_path = ("artifacts", object_field, field)
                error = f"artifact bundle artifacts.{object_field}.{field} 非法"
                cases.append((f"list:{object_field}.{field}", field_path, {}, error))
                cases.append(
                    (
                        f"string:{object_field}.{field}[0]",
                        field_path,
                        [None],
                        error.replace(" 非法", "[0] 非法"),
                    )
                )

        for name, case_path, value, error in cases:
            with self.subTest(category=name), tempfile.TemporaryDirectory() as tmp_dir:
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
