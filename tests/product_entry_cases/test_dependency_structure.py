from __future__ import annotations


from product_entry_cases.support import *  # noqa: F401,F403


OLD_RUNTIME_TOKEN = "hermes" + "_runtime"
OLD_RUNTIME_IMPORT = f"from med_autogrant import {OLD_RUNTIME_TOKEN}"


class ProductEntryPartsStructureTest(unittest.TestCase):
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
