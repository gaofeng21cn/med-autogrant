from __future__ import annotations

import unittest

from med_autogrant.product_entry import MedAutoGrantProductEntry
from product_entry_cases.family_stage_control_plane_assertions import (
    assert_family_stage_control_plane_preserves_opl_projection_and_mag_authority,
)
from product_entry_cases.support import CRITIQUE_EXAMPLE_PATH


class FamilyStageControlPlaneTest(unittest.TestCase):
    def test_stage_control_plane_preserves_opl_projection_and_mag_authority(self) -> None:
        manifest = MedAutoGrantProductEntry().build_product_entry_manifest(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
        )["product_entry_manifest"]

        assert_family_stage_control_plane_preserves_opl_projection_and_mag_authority(
            self,
            action_catalog=manifest["family_action_catalog"],
            stage_plane=manifest["family_stage_control_plane"],
        )


if __name__ == "__main__":
    unittest.main()
