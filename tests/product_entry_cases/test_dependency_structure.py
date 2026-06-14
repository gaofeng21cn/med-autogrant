from __future__ import annotations

import ast
import unittest

from product_entry_cases.support import REPO_ROOT


OLD_RUNTIME_TOKEN = "hermes" + "_runtime"
OLD_RUNTIME_IMPORT = f"from med_autogrant import {OLD_RUNTIME_TOKEN}"


class ProductEntryPartsStructureTest(unittest.TestCase):
    def test_product_entry_parts_package_root_is_marker_only(self) -> None:
        package_path = REPO_ROOT / "src" / "med_autogrant" / "product_entry_parts" / "__init__.py"
        package_text = package_path.read_text(encoding="utf-8")
        package_tree = ast.parse(package_text)

        forbidden_nodes = [
            node
            for node in ast.walk(package_tree)
            if isinstance(node, (ast.Import, ast.ImportFrom, ast.FunctionDef, ast.AsyncFunctionDef))
            or (
                isinstance(node, ast.Assign)
                and any(isinstance(target, ast.Name) and target.id == "__all__" for target in node.targets)
            )
        ]
        self.assertEqual([], forbidden_nodes)
        self.assertNotIn("MedAutoGrantProductEntry", package_text)

    def test_retired_product_entry_shared_reexport_is_not_present(self) -> None:
        self.assertFalse(
            (REPO_ROOT / "src" / "med_autogrant" / "product_entry_parts" / "shared.py").exists()
        )

    def test_consumer_thinning_audit_package_reexports_are_not_present(self) -> None:
        package_path = (
            REPO_ROOT
            / "src"
            / "med_autogrant"
            / "product_entry_parts"
            / "consumer_thinning_audit"
            / "__init__.py"
        )
        package_text = package_path.read_text(encoding="utf-8")
        consumer_text = (
            REPO_ROOT / "src" / "med_autogrant" / "product_entry_parts" / "consumer_thinning.py"
        ).read_text(encoding="utf-8")
        package_tree = ast.parse(package_text)

        forbidden_nodes = [
            node
            for node in ast.walk(package_tree)
            if isinstance(node, (ast.Import, ast.ImportFrom))
            or (
                isinstance(node, ast.Assign)
                and any(isinstance(target, ast.Name) and target.id == "__all__" for target in node.targets)
            )
        ]
        self.assertEqual([], forbidden_nodes)
        for builder_name in (
            "build_default_caller_deletion_bridge_exit_gate",
            "build_functional_module_audit_item",
            "build_legacy_exit_gate",
            "build_privatized_functional_module_audit",
            "build_retired_functional_module_audit_item",
        ):
            self.assertNotIn(builder_name, package_text)

        self.assertIn("consumer_thinning_audit.report", consumer_text)
        self.assertNotIn("from med_autogrant.product_entry_parts.consumer_thinning_audit import", consumer_text)
        self.assertNotIn("_build_privatized_functional_module_audit", consumer_text)

    def test_product_entry_parts_do_not_star_import_each_other(self) -> None:
        product_entry_parts = sorted(
            (REPO_ROOT / "src" / "med_autogrant" / "product_entry_parts").glob("*.py")
        )

        offenders = [
            path.relative_to(REPO_ROOT).as_posix()
            for path in product_entry_parts
            if "import *" in path.read_text(encoding="utf-8")
        ]

        self.assertEqual([], offenders)

    def test_product_entry_parts_do_not_generate_dynamic_all_exports(self) -> None:
        product_entry_parts = sorted(
            (REPO_ROOT / "src" / "med_autogrant" / "product_entry_parts").glob("*.py")
        )
        offenders: list[str] = []
        for path in product_entry_parts:
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if not (
                    isinstance(node, ast.Assign)
                    and any(isinstance(target, ast.Name) and target.id == "__all__" for target in node.targets)
                    and isinstance(node.value, ast.ListComp)
                    and isinstance(node.value.generators[0].iter, ast.Call)
                    and isinstance(node.value.generators[0].iter.func, ast.Name)
                    and node.value.generators[0].iter.func.id == "globals"
                ):
                    continue
                offenders.append(path.relative_to(REPO_ROOT).as_posix())

        self.assertEqual([], offenders)

    def test_product_entry_case_support_is_not_a_star_import_facade(self) -> None:
        support_path = REPO_ROOT / "tests" / "product_entry_cases" / "support.py"
        support_tree = ast.parse(support_path.read_text(encoding="utf-8"))
        support_all_exports = [
            node
            for node in ast.walk(support_tree)
            if isinstance(node, ast.Assign)
            and any(isinstance(target, ast.Name) and target.id == "__all__" for target in node.targets)
        ]
        self.assertEqual([], support_all_exports)

        offenders = [
            path.relative_to(REPO_ROOT).as_posix()
            for path in sorted((REPO_ROOT / "tests" / "product_entry_cases").glob("test_*.py"))
            if any(
                isinstance(node, ast.ImportFrom)
                and node.module == "product_entry_cases.support"
                and any(alias.name == "*" for alias in node.names)
                for node in ast.walk(ast.parse(path.read_text(encoding="utf-8")))
            )
        ]
        self.assertEqual([], offenders)

    def test_product_entry_parts_do_not_call_runtime_facade(self) -> None:
        product_entry_parts = sorted(
            (REPO_ROOT / "src" / "med_autogrant" / "product_entry_parts").glob("*.py")
        )
        forbidden_fragments = (
            "from med_autogrant.domain_runtime import",
            OLD_RUNTIME_IMPORT,
        )
        offenders = [
            path.relative_to(REPO_ROOT).as_posix()
            for path in product_entry_parts
            if any(fragment in path.read_text(encoding="utf-8") for fragment in forbidden_fragments)
        ]

        self.assertEqual([], offenders)

    def test_product_entry_runtime_contract_bridge_uses_contract_api(self) -> None:
        bridge_text = (
            REPO_ROOT / "src" / "med_autogrant" / "product_entry_parts" / "runtime_contracts.py"
        ).read_text(encoding="utf-8")

        self.assertIn("med_autogrant.product_entry_contract_api", bridge_text)
        self.assertNotIn("med_autogrant.domain_runtime_parts", bridge_text)
        self.assertNotIn("med_autogrant.domain_runtime import", bridge_text)

    def test_product_entry_contract_api_exports_public_bridge_only(self) -> None:
        from med_autogrant import product_entry_contract_api as contract_api

        expected_exports = {
            "GRANT_COCKPIT_SCHEMA_FILE",
            "GRANT_DIRECT_ENTRY_SCHEMA_FILE",
            "GRANT_PROGRESS_SCHEMA_FILE",
            "GRANT_USER_LOOP_SCHEMA_FILE",
            "PRODUCT_ENTRY_MANIFEST_SCHEMA_FILE",
            "PRODUCT_ENTRY_SCHEMA_FILE",
            "PRODUCT_STATUS_SCHEMA_FILE",
            "build_author_side_route_contract",
            "build_executor_routing_contract",
            "build_operator_contract",
            "build_runtime_state_contract",
            "build_runtime_substrate_contract",
            "read_current_program_contract",
            "validate_contract_schema",
            "validate_executor_routing_contract",
        }

        self.assertEqual(set(contract_api.__all__), expected_exports)
        self.assertTrue(all(not name.startswith("_") for name in contract_api.__all__))

    def test_product_entry_entry_keeps_evidence_delegates_in_mixin(self) -> None:
        entry_path = REPO_ROOT / "src" / "med_autogrant" / "product_entry_parts" / "entry.py"
        evidence_path = REPO_ROOT / "src" / "med_autogrant" / "product_entry_parts" / "evidence.py"
        entry_text = entry_path.read_text(encoding="utf-8")
        evidence_text = evidence_path.read_text(encoding="utf-8")

        self.assertIn("ProductEntryEvidenceMixin", entry_text)
        self.assertIn("class ProductEntryEvidenceMixin", evidence_text)
        self.assertNotIn("def write_owner_receipt_evidence", entry_text)
        self.assertNotIn("def build_receipt_readiness_projection", entry_text)
        self.assertIn("def write_owner_receipt_evidence", evidence_text)
        self.assertIn("def build_receipt_readiness_projection", evidence_text)
