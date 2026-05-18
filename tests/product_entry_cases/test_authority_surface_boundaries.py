from __future__ import annotations

import unittest

from product_entry_cases.support import CRITIQUE_EXAMPLE_PATH
from med_autogrant.product_entry_parts import MedAutoGrantProductEntry


class AuthoritySurfaceBoundaryTest(unittest.TestCase):
    def test_minimal_authority_surfaces_separate_ai_judgment_from_programmatic_guards(self) -> None:
        manifest = MedAutoGrantProductEntry().build_product_entry_manifest(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
        )["product_entry_manifest"]
        thinning = manifest["mag_consumer_thinning_contract"]
        authority_surfaces = {
            item["authority_surface_id"]: item for item in thinning["minimal_authority_functions"]
        }
        taxonomy = thinning["minimal_authority_surface_taxonomy"]

        self.assertEqual(set(authority_surfaces), set(thinning["minimal_authority_function_ids"]))
        self.assertTrue(taxonomy["legacy_function_id_compatibility"])
        self.assertEqual(
            taxonomy["ai_first_judgment_surface_ids"],
            [
                "fundability_verdict",
                "quality_verdict",
                "export_verdict",
                "memory_accept_reject",
            ],
        )
        self.assertEqual(
            taxonomy["programmatic_authority_surface_ids"],
            ["package_authority", "owner_receipt_signer", "grant_helper"],
        )
        self.assertTrue(taxonomy["mechanical_decision_forbidden_for_all_surfaces"])
        self.assertFalse(taxonomy["programmatic_verdict_generation_allowed"])

        for function_id, surface in authority_surfaces.items():
            with self.subTest(authority_surface=function_id):
                self.assertEqual(surface["surface_kind"], "mag_minimal_authority_surface")
                self.assertEqual(surface["function_id"], function_id)
                self.assertTrue(surface["legacy_function_id_compatibility"])
                self.assertTrue(surface["mechanical_decision_forbidden"])
                self.assertFalse(surface["programmatic_verdict_generation_allowed"])
                self.assertIn("programmatic_ready_verdict", surface["output_boundary"]["forbidden_outputs"])
                self.assertIn("schema_completeness", surface["forbidden_decision_sources"])
                self.assertFalse(
                    surface["decision_boundary"]["programmatic_role_may_compute_ready_verdict"]
                )
                self.assertTrue(
                    surface["decision_boundary"]["programmatic_role_may_materialize_refs_only"]
                )

        for function_id in taxonomy["ai_first_judgment_surface_ids"]:
            with self.subTest(ai_first_judgment_surface=function_id):
                surface = authority_surfaces[function_id]
                self.assertEqual(surface["work_mode"], "ai_first_domain_judgment_surface")
                self.assertTrue(surface["ai_stage_artifact_required"])
                self.assertTrue(surface["decision_boundary"]["ai_first_judgment_required"])

        for function_id in taxonomy["programmatic_authority_surface_ids"]:
            with self.subTest(programmatic_authority_surface=function_id):
                surface = authority_surfaces[function_id]
                self.assertEqual(surface["work_mode"], "programmatic_authority_guard_surface")
                self.assertFalse(surface["ai_stage_artifact_required"])
                self.assertFalse(surface["decision_boundary"]["ai_first_judgment_required"])


if __name__ == "__main__":
    unittest.main()
