from __future__ import annotations


from product_entry_cases.support import *  # noqa: F401,F403


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
            "from med_autogrant.hermes_runtime import",
            "from med_autogrant import hermes_runtime",
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
        self.assertNotIn("med_autogrant.hermes_runtime_parts", bridge_text)
        self.assertNotIn("med_autogrant.hermes_runtime import", bridge_text)
