from __future__ import annotations

import unittest

from product_entry_cases.direct_entry_assertions import (
    assert_grant_direct_entry_composes_projection_and_entry_envelopes,
)
from product_entry_cases.support import CRITIQUE_EXAMPLE_PATH


class ProductEntryDirectEntryTest(unittest.TestCase):
    def test_grant_direct_entry_composes_projection_and_entry_envelopes(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        payload = MedAutoGrantProductEntry().build_grant_direct_entry(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
            task_intent="tighten-grant-mainline",
        )

        assert_grant_direct_entry_composes_projection_and_entry_envelopes(self, payload)


if __name__ == "__main__":
    unittest.main()
