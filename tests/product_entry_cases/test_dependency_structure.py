from __future__ import annotations

__test__ = False

from product_entry_cases.support import *  # noqa: F401,F403


class ProductEntryPartsStructureTest(unittest.TestCase):
    def test_core_product_entry_parts_do_not_star_import_each_other(self) -> None:
        core_parts = [
            REPO_ROOT / "src" / "med_autogrant" / "product_entry_parts" / "shared.py",
            REPO_ROOT / "src" / "med_autogrant" / "product_entry_parts" / "runtime_surfaces.py",
            REPO_ROOT / "src" / "med_autogrant" / "product_entry_parts" / "loop_contracts.py",
        ]

        offenders = [
            path.relative_to(REPO_ROOT).as_posix()
            for path in core_parts
            if "import *" in path.read_text(encoding="utf-8")
        ]

        self.assertEqual([], offenders)
