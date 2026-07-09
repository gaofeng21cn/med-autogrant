from __future__ import annotations

from .context import REMOVE, FinalPackageCliCase


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
                self._assert_bundle_path_fails(
                    f"bad-artifacts-object-{nested_field}.json",
                    ("artifacts", nested_field),
                    f"artifact bundle artifacts.{nested_field} 非法",
                    bad_value=bad_value,
                )

    def test_build_final_package_fails_closed_when_artifact_bundle_artifact_object_primary_ids_are_missing_or_invalid(self) -> None:
        cases = (
            ("selected_direction", "direction_id", None),
            ("selected_direction", "direction_id", REMOVE),
            ("selected_question", "question_id", ""),
            ("selected_question", "question_id", REMOVE),
            ("argument_chain", "argument_chain_id", None),
            ("argument_chain", "argument_chain_id", REMOVE),
            ("fit_mapping", "fit_mapping_id", ""),
            ("fit_mapping", "fit_mapping_id", REMOVE),
        )
        for object_field, nested_field, bad_value in cases:
            with self.subTest(object_field=object_field, nested_field=nested_field, bad_value=bad_value):
                self._assert_bundle_path_fails(
                    f"bad-artifact-object-id-{object_field}-{nested_field}.json",
                    ("artifacts", object_field, nested_field),
                    f"artifact bundle artifacts.{object_field}.{nested_field} 非法",
                    bad_value=bad_value,
                )

    def test_build_final_package_fails_closed_when_artifact_bundle_artifact_object_linkage_ids_are_missing_or_invalid(self) -> None:
        cases = (
            ("selected_question", "parent_direction_id", None),
            ("selected_question", "parent_direction_id", REMOVE),
            ("argument_chain", "scientific_question_id", ""),
            ("argument_chain", "scientific_question_id", REMOVE),
            ("fit_mapping", "scientific_question_id", None),
            ("fit_mapping", "scientific_question_id", REMOVE),
            ("fit_mapping", "argument_chain_id", ""),
            ("fit_mapping", "argument_chain_id", REMOVE),
        )
        for object_field, nested_field, bad_value in cases:
            with self.subTest(object_field=object_field, nested_field=nested_field, bad_value=bad_value):
                self._assert_bundle_path_fails(
                    f"bad-artifact-object-linkage-{object_field}-{nested_field}.json",
                    ("artifacts", object_field, nested_field),
                    f"artifact bundle artifacts.{object_field}.{nested_field} 非法",
                    bad_value=bad_value,
                )

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
                cases.append((object_field, nested_field, REMOVE))

        for object_field, nested_field, bad_value in cases:
            with self.subTest(object_field=object_field, nested_field=nested_field, bad_value=bad_value):
                self._assert_bundle_path_fails(
                    f"bad-artifact-object-string-{object_field}-{nested_field}.json",
                    ("artifacts", object_field, nested_field),
                    f"artifact bundle artifacts.{object_field}.{nested_field} 非法",
                    bad_value=bad_value,
                )

    def test_build_final_package_fails_closed_when_artifact_bundle_artifact_object_required_list_fields_are_missing_or_invalid(self) -> None:
        cases = (
            ("selected_direction", "required_evidence_ids", None),
            ("selected_direction", "required_evidence_ids", REMOVE),
            ("selected_question", "subquestions", {}),
            ("selected_question", "subquestions", REMOVE),
            ("selected_question", "linked_evidence_ids", None),
            ("selected_question", "linked_evidence_ids", REMOVE),
            ("argument_chain", "linked_evidence_ids", {}),
            ("argument_chain", "linked_evidence_ids", REMOVE),
            ("fit_mapping", "linked_evidence_ids", None),
            ("fit_mapping", "linked_evidence_ids", REMOVE),
        )
        for object_field, nested_field, bad_value in cases:
            with self.subTest(object_field=object_field, nested_field=nested_field, bad_value=bad_value):
                self._assert_bundle_path_fails(
                    f"bad-artifact-object-list-{object_field}-{nested_field}.json",
                    ("artifacts", object_field, nested_field),
                    f"artifact bundle artifacts.{object_field}.{nested_field} 非法",
                    bad_value=bad_value,
                )

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
                self._assert_bundle_path_fails(
                    f"bad-object-list-element-{object_field}-{nested_field}.json",
                    ("artifacts", object_field, nested_field, 0),
                    f"artifact bundle artifacts.{object_field}.{nested_field}[0] 非法",
                    bad_value=bad_value,
                )
