from __future__ import annotations

from .context import FinalPackageCliCase


class TestFinalPackageArtifactListCases(FinalPackageCliCase):
    def test_build_final_package_fails_closed_when_artifact_bundle_artifact_lists_are_not_lists(self) -> None:
        cases = (
            ("draft_outline", {}),
            ("draft_outline", "oops"),
            ("draft_sections", {}),
            ("draft_sections", None),
            ("draft_sections", "oops"),
        )
        for nested_field, bad_value in cases:
            with self.subTest(nested_field=nested_field, bad_value=bad_value):
                self._assert_bundle_path_fails(
                    f"bad-artifacts-{nested_field}.json",
                    ("artifacts", nested_field),
                    f"artifact bundle artifacts.{nested_field} 非法",
                    bad_value=bad_value,
                )

    def test_build_final_package_fails_closed_when_artifact_bundle_list_element_shapes_are_invalid(self) -> None:
        object_cases = (
            ("draft_outline", "oops", "artifact bundle artifacts.draft_outline[0] 非法"),
            ("draft_sections", None, "artifact bundle artifacts.draft_sections[0] 非法"),
        )
        for list_field, bad_value, error_snippet in object_cases:
            with self.subTest(list_field=list_field, bad_value=bad_value):
                self._assert_bundle_path_fails(
                    f"bad-{list_field}-element.json",
                    ("artifacts", list_field, 0),
                    error_snippet,
                    bad_value=bad_value,
                )

        missing_field_cases = (
            ("draft_outline", "section_key"),
            ("draft_outline", "section_title"),
            ("draft_outline", "core_claim"),
            ("draft_outline", "linked_object_ids"),
            ("draft_sections", "section_key"),
            ("draft_sections", "section_title"),
            ("draft_sections", "text"),
            ("draft_sections", "linked_object_ids"),
        )
        for list_field, nested_field in missing_field_cases:
            with self.subTest(list_field=list_field, nested_field=nested_field):
                self._assert_bundle_path_fails(
                    f"missing-{list_field}-{nested_field}.json",
                    ("artifacts", list_field, 0, nested_field),
                    f"artifact bundle artifacts.{list_field}[0] 缺少字段: {nested_field}",
                )

    def test_build_final_package_fails_closed_when_artifact_bundle_artifact_list_element_required_string_fields_are_not_nonempty_strings(self) -> None:
        cases = (
            ("draft_outline", "section_key", None),
            ("draft_outline", "section_title", ""),
            ("draft_outline", "core_claim", None),
            ("draft_sections", "section_key", ""),
            ("draft_sections", "section_title", None),
            ("draft_sections", "text", ""),
        )
        for list_field, nested_field, bad_value in cases:
            with self.subTest(list_field=list_field, nested_field=nested_field, bad_value=bad_value):
                self._assert_bundle_path_fails(
                    f"bad-list-element-string-{list_field}-{nested_field}.json",
                    ("artifacts", list_field, 0, nested_field),
                    f"artifact bundle artifacts.{list_field}[0].{nested_field} 非法",
                    bad_value=bad_value,
                )

    def test_build_final_package_fails_closed_when_artifact_bundle_artifact_list_element_linked_object_ids_fields_are_not_lists(self) -> None:
        cases = (
            ("draft_outline", None),
            ("draft_outline", {}),
            ("draft_sections", None),
            ("draft_sections", {}),
        )
        for list_field, bad_value in cases:
            with self.subTest(list_field=list_field, bad_value=bad_value):
                self._assert_bundle_path_fails(
                    f"bad-linked-object-ids-{list_field}.json",
                    ("artifacts", list_field, 0, "linked_object_ids"),
                    f"artifact bundle artifacts.{list_field}[0].linked_object_ids 非法",
                    bad_value=bad_value,
                )

    def test_build_final_package_fails_closed_when_artifact_bundle_artifact_list_element_linked_object_ids_list_elements_are_not_nonempty_strings(self) -> None:
        cases = (
            ("draft_outline", None),
            ("draft_outline", {}),
            ("draft_outline", ""),
            ("draft_sections", None),
            ("draft_sections", {}),
            ("draft_sections", ""),
        )
        for list_field, bad_value in cases:
            with self.subTest(list_field=list_field, bad_value=bad_value):
                self._assert_bundle_path_fails(
                    f"bad-linked-object-id-element-{list_field}.json",
                    ("artifacts", list_field, 0, "linked_object_ids", 0),
                    f"artifact bundle artifacts.{list_field}[0].linked_object_ids[0] 非法",
                    bad_value=bad_value,
                )
