from __future__ import annotations

import json
import tempfile
from pathlib import Path

from .context import (
    FORWARD_PROGRESS_EXAMPLE_PATH,
    FREEZE_READY_EXAMPLE_PATH,
    FROZEN_EXAMPLE_PATH,
    FinalPackageCliCase,
)


class TestFinalPackageArtifactObjectCases(FinalPackageCliCase):
    def test_build_final_package_fails_closed_when_artifact_bundle_artifact_object_values_are_not_dicts(self) -> None:
        cases = (
            ("selected_direction", []),
            ("selected_direction", "oops"),
            ("selected_question", []),
            ("selected_question", "oops"),
            ("argument_chain", None),
            ("argument_chain", "oops"),
            ("fit_mapping", []),
            ("fit_mapping", "oops"),
        )
        for nested_field, bad_value in cases:
            with self.subTest(nested_field=nested_field, bad_value=bad_value):
                with tempfile.TemporaryDirectory() as tmp_dir:
                    bundle_path = Path(tmp_dir) / f"bad-artifacts-object-{nested_field}.json"
                    package_path = Path(tmp_dir) / "package.json"
                    self._build_bundle(FROZEN_EXAMPLE_PATH, bundle_path)
                    bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
                    bundle["artifacts"][nested_field] = bad_value
                    bundle_path.write_text(json.dumps(bundle, ensure_ascii=False, indent=2), encoding="utf-8")

                    exit_code, stdout, stderr = self.run_cli(
                        "package",
                "final-package",
                "--input",
                        str(FROZEN_EXAMPLE_PATH),
                        "--artifact-bundle",
                        str(bundle_path),
                        "--output",
                        str(package_path),
                        "--format",
                        "json",
                    )

                    self.assertEqual(exit_code, 1)
                    self.assertEqual(stderr, "")
                    payload = json.loads(stdout)
                    self.assertFalse(payload["ok"])
                    self.assertIn(f"artifact bundle artifacts.{nested_field} 非法", payload["error"])
                    self.assertFalse(package_path.exists())

    def test_build_final_package_fails_closed_when_artifact_bundle_artifact_object_primary_ids_are_missing_or_invalid(self) -> None:
        cases = (
            ("selected_direction", "direction_id", None),
            ("selected_direction", "direction_id", "remove"),
            ("selected_question", "question_id", ""),
            ("selected_question", "question_id", "remove"),
            ("argument_chain", "argument_chain_id", None),
            ("argument_chain", "argument_chain_id", "remove"),
            ("fit_mapping", "fit_mapping_id", ""),
            ("fit_mapping", "fit_mapping_id", "remove"),
        )
        for object_field, nested_field, bad_value in cases:
            with self.subTest(object_field=object_field, nested_field=nested_field, bad_value=bad_value):
                with tempfile.TemporaryDirectory() as tmp_dir:
                    bundle_path = Path(tmp_dir) / f"bad-artifact-object-id-{object_field}-{nested_field}.json"
                    package_path = Path(tmp_dir) / "package.json"
                    self._build_bundle(FROZEN_EXAMPLE_PATH, bundle_path)
                    bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
                    if bad_value == "remove":
                        bundle["artifacts"][object_field].pop(nested_field, None)
                    else:
                        bundle["artifacts"][object_field][nested_field] = bad_value
                    bundle_path.write_text(json.dumps(bundle, ensure_ascii=False, indent=2), encoding="utf-8")

                    exit_code, stdout, stderr = self.run_cli(
                        "package",
                "final-package",
                "--input",
                        str(FROZEN_EXAMPLE_PATH),
                        "--artifact-bundle",
                        str(bundle_path),
                        "--output",
                        str(package_path),
                        "--format",
                        "json",
                    )

                    self.assertEqual(exit_code, 1)
                    self.assertEqual(stderr, "")
                    payload = json.loads(stdout)
                    self.assertFalse(payload["ok"])
                    self.assertIn(f"artifact bundle artifacts.{object_field}.{nested_field} 非法", payload["error"])
                    self.assertFalse(package_path.exists())

    def test_build_final_package_fails_closed_when_artifact_bundle_artifact_object_linkage_ids_are_missing_or_invalid(self) -> None:
        cases = (
            ("selected_question", "parent_direction_id", None),
            ("selected_question", "parent_direction_id", "remove"),
            ("argument_chain", "scientific_question_id", ""),
            ("argument_chain", "scientific_question_id", "remove"),
            ("fit_mapping", "scientific_question_id", None),
            ("fit_mapping", "scientific_question_id", "remove"),
            ("fit_mapping", "argument_chain_id", ""),
            ("fit_mapping", "argument_chain_id", "remove"),
        )
        for object_field, nested_field, bad_value in cases:
            with self.subTest(object_field=object_field, nested_field=nested_field, bad_value=bad_value):
                with tempfile.TemporaryDirectory() as tmp_dir:
                    bundle_path = Path(tmp_dir) / f"bad-artifact-object-linkage-{object_field}-{nested_field}.json"
                    package_path = Path(tmp_dir) / "package.json"
                    self._build_bundle(FROZEN_EXAMPLE_PATH, bundle_path)
                    bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
                    if bad_value == "remove":
                        bundle["artifacts"][object_field].pop(nested_field, None)
                    else:
                        bundle["artifacts"][object_field][nested_field] = bad_value
                    bundle_path.write_text(json.dumps(bundle, ensure_ascii=False, indent=2), encoding="utf-8")

                    exit_code, stdout, stderr = self.run_cli(
                        "package",
                "final-package",
                "--input",
                        str(FROZEN_EXAMPLE_PATH),
                        "--artifact-bundle",
                        str(bundle_path),
                        "--output",
                        str(package_path),
                        "--format",
                        "json",
                    )

                    self.assertEqual(exit_code, 1)
                    self.assertEqual(stderr, "")
                    payload = json.loads(stdout)
                    self.assertFalse(payload["ok"])
                    self.assertIn(f"artifact bundle artifacts.{object_field}.{nested_field} 非法", payload["error"])
                    self.assertFalse(package_path.exists())

    def test_build_final_package_fails_closed_when_artifact_bundle_artifact_object_required_string_fields_are_missing_or_invalid(self) -> None:
        string_fields = {
            "selected_direction": (
                "title",
                "rationale",
                "knowledge_gap_summary",
                "applicant_fit_summary",
                "novelty_angle",
                "risk_summary",
                "decision_status",
            ),
            "selected_question": (
                "phenomenon",
                "knowledge_boundary",
                "unknown_mechanism",
                "core_question",
                "falsifiable_statement",
                "proposed_breakthrough_angle",
                "why_not_engineering",
                "why_now",
            ),
            "argument_chain": (
                "background_claim",
                "field_gap",
                "necessity_claim",
                "uniqueness_claim",
                "route_justification",
                "non_arbitrary_route_reason",
                "if_not_done_loss",
            ),
            "fit_mapping": (
                "applicant_fit_summary",
                "unique_advantage",
                "methods_readiness",
                "resource_readiness",
                "risk_mitigation",
            ),
        }
        cases: list[tuple[str, str, object]] = []
        for object_field, fields in string_fields.items():
            for nested_field in fields:
                bad_value = None if len(cases) % 2 == 0 else ""
                cases.append((object_field, nested_field, bad_value))
                cases.append((object_field, nested_field, "remove"))

        for object_field, nested_field, bad_value in cases:
            with self.subTest(object_field=object_field, nested_field=nested_field, bad_value=bad_value):
                with tempfile.TemporaryDirectory() as tmp_dir:
                    bundle_path = Path(tmp_dir) / f"bad-artifact-object-string-{object_field}-{nested_field}.json"
                    package_path = Path(tmp_dir) / "package.json"
                    self._build_bundle(FROZEN_EXAMPLE_PATH, bundle_path)
                    bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
                    if bad_value == "remove":
                        bundle["artifacts"][object_field].pop(nested_field, None)
                    else:
                        bundle["artifacts"][object_field][nested_field] = bad_value
                    bundle_path.write_text(json.dumps(bundle, ensure_ascii=False, indent=2), encoding="utf-8")

                    exit_code, stdout, stderr = self.run_cli(
                        "package",
                "final-package",
                "--input",
                        str(FROZEN_EXAMPLE_PATH),
                        "--artifact-bundle",
                        str(bundle_path),
                        "--output",
                        str(package_path),
                        "--format",
                        "json",
                    )

                    self.assertEqual(exit_code, 1)
                    self.assertEqual(stderr, "")
                    payload = json.loads(stdout)
                    self.assertFalse(payload["ok"])
                    self.assertIn(f"artifact bundle artifacts.{object_field}.{nested_field} 非法", payload["error"])
                    self.assertFalse(package_path.exists())

    def test_build_final_package_fails_closed_when_artifact_bundle_artifact_object_required_list_fields_are_missing_or_invalid(self) -> None:
        cases = (
            ("selected_direction", "required_evidence_ids", None),
            ("selected_direction", "required_evidence_ids", "remove"),
            ("selected_question", "subquestions", {}),
            ("selected_question", "subquestions", "remove"),
            ("selected_question", "linked_evidence_ids", None),
            ("selected_question", "linked_evidence_ids", "remove"),
            ("argument_chain", "linked_evidence_ids", {}),
            ("argument_chain", "linked_evidence_ids", "remove"),
            ("fit_mapping", "linked_evidence_ids", None),
            ("fit_mapping", "linked_evidence_ids", "remove"),
        )
        for object_field, nested_field, bad_value in cases:
            with self.subTest(object_field=object_field, nested_field=nested_field, bad_value=bad_value):
                with tempfile.TemporaryDirectory() as tmp_dir:
                    bundle_path = Path(tmp_dir) / f"bad-artifact-object-list-{object_field}-{nested_field}.json"
                    package_path = Path(tmp_dir) / "package.json"
                    self._build_bundle(FROZEN_EXAMPLE_PATH, bundle_path)
                    bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
                    if bad_value == "remove":
                        bundle["artifacts"][object_field].pop(nested_field, None)
                    else:
                        bundle["artifacts"][object_field][nested_field] = bad_value
                    bundle_path.write_text(json.dumps(bundle, ensure_ascii=False, indent=2), encoding="utf-8")

                    exit_code, stdout, stderr = self.run_cli(
                        "package",
                "final-package",
                "--input",
                        str(FROZEN_EXAMPLE_PATH),
                        "--artifact-bundle",
                        str(bundle_path),
                        "--output",
                        str(package_path),
                        "--format",
                        "json",
                    )

                    self.assertEqual(exit_code, 1)
                    self.assertEqual(stderr, "")
                    payload = json.loads(stdout)
                    self.assertFalse(payload["ok"])
                    self.assertIn(f"artifact bundle artifacts.{object_field}.{nested_field} 非法", payload["error"])
                    self.assertFalse(package_path.exists())

    def test_build_final_package_fails_closed_when_artifact_bundle_artifact_object_required_list_elements_are_not_nonempty_strings(self) -> None:
        cases = (
            ("selected_direction", "required_evidence_ids", None),
            ("selected_direction", "required_evidence_ids", {}),
            ("selected_direction", "required_evidence_ids", ""),
            ("selected_question", "subquestions", None),
            ("selected_question", "linked_evidence_ids", {}),
            ("selected_question", "linked_evidence_ids", ""),
            ("argument_chain", "linked_evidence_ids", None),
            ("argument_chain", "linked_evidence_ids", {}),
            ("fit_mapping", "linked_evidence_ids", ""),
        )
        for object_field, nested_field, bad_value in cases:
            with self.subTest(object_field=object_field, nested_field=nested_field, bad_value=bad_value):
                with tempfile.TemporaryDirectory() as tmp_dir:
                    bundle_path = Path(tmp_dir) / f"bad-object-list-element-{object_field}-{nested_field}.json"
                    package_path = Path(tmp_dir) / "package.json"
                    self._build_bundle(FROZEN_EXAMPLE_PATH, bundle_path)
                    bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
                    bundle["artifacts"][object_field][nested_field][0] = bad_value
                    bundle_path.write_text(json.dumps(bundle, ensure_ascii=False, indent=2), encoding="utf-8")

                    exit_code, stdout, stderr = self.run_cli(
                        "package",
                "final-package",
                "--input",
                        str(FROZEN_EXAMPLE_PATH),
                        "--artifact-bundle",
                        str(bundle_path),
                        "--output",
                        str(package_path),
                        "--format",
                        "json",
                    )

                    self.assertEqual(exit_code, 1)
                    self.assertEqual(stderr, "")
                    payload = json.loads(stdout)
                    self.assertFalse(payload["ok"])
                    self.assertIn(f"artifact bundle artifacts.{object_field}.{nested_field}[0] 非法", payload["error"])
                    self.assertFalse(package_path.exists())


