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
                with tempfile.TemporaryDirectory() as tmp_dir:
                    bundle_path = Path(tmp_dir) / f"bad-artifacts-{nested_field}.json"
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

    def test_build_final_package_fails_closed_when_artifact_bundle_list_element_shapes_are_invalid(self) -> None:
        object_cases = (
            ("draft_outline", "replace", "oops", "artifact bundle artifacts.draft_outline[0] 非法"),
            ("draft_sections", "replace", None, "artifact bundle artifacts.draft_sections[0] 非法"),
        )
        for list_field, mode, bad_value, error_snippet in object_cases:
            with self.subTest(list_field=list_field, mode=mode, bad_value=bad_value):
                with tempfile.TemporaryDirectory() as tmp_dir:
                    bundle_path = Path(tmp_dir) / f"bad-{list_field}-element.json"
                    package_path = Path(tmp_dir) / "package.json"
                    self._build_bundle(FROZEN_EXAMPLE_PATH, bundle_path)
                    bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
                    bundle["artifacts"][list_field][0] = bad_value
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
                    self.assertIn(error_snippet, payload["error"])
                    self.assertFalse(package_path.exists())

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
                with tempfile.TemporaryDirectory() as tmp_dir:
                    bundle_path = Path(tmp_dir) / f"missing-{list_field}-{nested_field}.json"
                    package_path = Path(tmp_dir) / "package.json"
                    self._build_bundle(FROZEN_EXAMPLE_PATH, bundle_path)
                    bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
                    bundle["artifacts"][list_field][0].pop(nested_field, None)
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
                    self.assertIn(
                        f"artifact bundle artifacts.{list_field}[0] 缺少字段: {nested_field}",
                        payload["error"],
                    )
                    self.assertFalse(package_path.exists())

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
                with tempfile.TemporaryDirectory() as tmp_dir:
                    bundle_path = Path(tmp_dir) / f"bad-list-element-string-{list_field}-{nested_field}.json"
                    package_path = Path(tmp_dir) / "package.json"
                    self._build_bundle(FROZEN_EXAMPLE_PATH, bundle_path)
                    bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
                    bundle["artifacts"][list_field][0][nested_field] = bad_value
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
                    self.assertIn(f"artifact bundle artifacts.{list_field}[0].{nested_field} 非法", payload["error"])
                    self.assertFalse(package_path.exists())

    def test_build_final_package_fails_closed_when_artifact_bundle_artifact_list_element_linked_object_ids_fields_are_not_lists(self) -> None:
        cases = (
            ("draft_outline", None),
            ("draft_outline", {}),
            ("draft_sections", None),
            ("draft_sections", {}),
        )
        for list_field, bad_value in cases:
            with self.subTest(list_field=list_field, bad_value=bad_value):
                with tempfile.TemporaryDirectory() as tmp_dir:
                    bundle_path = Path(tmp_dir) / f"bad-linked-object-ids-{list_field}.json"
                    package_path = Path(tmp_dir) / "package.json"
                    self._build_bundle(FROZEN_EXAMPLE_PATH, bundle_path)
                    bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
                    bundle["artifacts"][list_field][0]["linked_object_ids"] = bad_value
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
                    self.assertIn(f"artifact bundle artifacts.{list_field}[0].linked_object_ids 非法", payload["error"])
                    self.assertFalse(package_path.exists())

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
                with tempfile.TemporaryDirectory() as tmp_dir:
                    bundle_path = Path(tmp_dir) / f"bad-linked-object-id-element-{list_field}.json"
                    package_path = Path(tmp_dir) / "package.json"
                    self._build_bundle(FROZEN_EXAMPLE_PATH, bundle_path)
                    bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
                    bundle["artifacts"][list_field][0]["linked_object_ids"][0] = bad_value
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
                    self.assertIn(f"artifact bundle artifacts.{list_field}[0].linked_object_ids[0] 非法", payload["error"])
                    self.assertFalse(package_path.exists())


