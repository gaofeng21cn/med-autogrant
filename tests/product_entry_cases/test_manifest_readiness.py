from __future__ import annotations


from product_entry_cases.support import *  # noqa: F401,F403


class ProductEntryManifestReadinessTest(unittest.TestCase):
    def test_manifest_readiness_surfaces_keep_agent_assisted_boundary(self) -> None:
        from med_autogrant.product_entry_parts.manifest_readiness import build_manifest_readiness_surfaces

        surfaces = build_manifest_readiness_surfaces(
            product_frontdesk_command="medautogrant product-frontdesk --input workspace.json --format json",
            grant_user_loop_command=(
                "medautogrant grant-user-loop --input workspace.json "
                "--task-intent '<describe-task-intent>' --format json"
            ),
        )

        grant_readiness = surfaces["grant_authoring_readiness"]
        product_readiness = surfaces["product_entry_readiness"]
        self.assertEqual(grant_readiness["surface_kind"], "grant_authoring_readiness")
        self.assertEqual(grant_readiness["verdict"], "agent_assisted_cli_ready_not_full_autopilot")
        self.assertFalse(grant_readiness["fully_automatic"])
        self.assertTrue(grant_readiness["usable_now"])
        self.assertFalse(grant_readiness["good_to_use_now"])
        self.assertEqual(grant_readiness["recommended_start_surface"], "product_frontdesk")
        self.assertEqual(grant_readiness["recommended_loop_surface"], "grant_user_loop")
        self.assertEqual(len(grant_readiness["workflow_coverage"]), 9)
        coverage_by_id = {item["step_id"]: item for item in grant_readiness["workflow_coverage"]}
        self.assertEqual(
            coverage_by_id["final_review_figures_package"]["coverage_status"],
            "partially_supported",
        )
        self.assertIn("官网代投", coverage_by_id["final_review_figures_package"]["remaining_gap"])
        self.assertIn("不会凭空生成真实预实验", coverage_by_id["preliminary_evidence_and_basis"]["remaining_gap"])
        self.assertEqual(
            product_readiness["summary"],
            grant_readiness["summary"],
        )
        self.assertEqual(
            product_readiness["blocking_gaps"],
            grant_readiness["blocking_gaps"],
        )
        self.assertEqual(product_readiness["recommended_start_command"], grant_readiness["recommended_start_command"])
