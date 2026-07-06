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

    def test_retired_product_entry_contract_api_is_not_present(self) -> None:
        self.assertFalse(
            (REPO_ROOT / "src" / "med_autogrant" / "product_entry_contract_api.py").exists()
        )

    def test_product_entry_runtime_contracts_use_true_runtime_owner(self) -> None:
        bridge_text = (
            REPO_ROOT / "src" / "med_autogrant" / "product_entry_parts" / "runtime_contracts.py"
        ).read_text(encoding="utf-8")

        self.assertIn("med_autogrant.domain_runtime_parts.contracts", bridge_text)
        self.assertIn("med_autogrant.domain_runtime_parts.shared", bridge_text)
        self.assertNotIn("med_autogrant.product_entry_contract_api", bridge_text)
        self.assertNotIn("med_autogrant.domain_runtime import", bridge_text)
