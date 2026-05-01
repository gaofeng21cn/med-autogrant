from __future__ import annotations

__test__ = False

from product_entry_cases.support import *  # noqa: F401,F403


class ProductEntryRuntimeRegistrationTest(unittest.TestCase):
    def test_opl_runtime_manager_registration_keeps_mag_as_truth_owner(self) -> None:
        from med_autogrant.product_entry_parts.runtime_registration import (
            _build_opl_native_helper_indexing_proof,
            _build_opl_runtime_manager_registration,
        )

        registration = _build_opl_runtime_manager_registration(
            runtime_summary={"runtime_owner": "upstream-hermes-agent"},
            runtime_continuity={
                "session_locator_field": "grant_run_id",
                "recommended_resume_command": "medautogrant runtime-resume --journal journal.json --format json",
                "recommended_progress_command": "medautogrant grant-progress --input workspace.json --format json",
            },
            shell_commands={"product_frontdesk": "medautogrant product-frontdesk --input workspace.json --format json"},
            skill_catalog_command="medautogrant skill-catalog --input workspace.json --format json",
        )

        self.assertEqual(registration["surface_kind"], "opl_runtime_manager_domain_registration")
        self.assertEqual(registration["domain_owner"], "med-autogrant")
        self.assertEqual(registration["runtime_owner"], "upstream-hermes-agent")
        self.assertEqual(registration["executor_owner"], "med-autogrant")
        self.assertEqual(registration["domain_entry_surface"]["surface_kind"], "product_frontdesk")
        self.assertEqual(
            registration["registration_surface"]["ref"],
            "/skill_catalog/skills/0/domain_projection/opl_runtime_manager_registration",
        )
        self.assertEqual(registration["native_helper_consumption"]["managed_by"], "one-person-lab")
        self.assertEqual(
            registration["native_helper_consumption"]["proof_surface"],
            _build_opl_native_helper_indexing_proof(),
        )
        self.assertEqual(
            registration["resume_contract"],
            {
                "session_locator_field": "grant_run_id",
                "recommended_resume_command": "medautogrant runtime-resume --journal journal.json --format json",
                "recommended_progress_command": "medautogrant grant-progress --input workspace.json --format json",
            },
        )
        self.assertEqual(
            registration["wakeup_boundary"],
            {
                "owner": "med-autogrant",
                "surface_ref": "/automation/automations/1",
                "policy": "explicit_authoring_loop_continuation",
            },
        )
        self.assertIn("not_a_grant_truth_owner", registration["non_goals"])
        self.assertIn("not_a_quality_gate", registration["non_goals"])
        self.assertIn("not_a_submission_ready_export_gate", registration["non_goals"])

    def test_native_helper_indexing_proof_is_index_only(self) -> None:
        from med_autogrant.product_entry_parts.runtime_registration import _build_opl_native_helper_indexing_proof

        proof = _build_opl_native_helper_indexing_proof()

        self.assertEqual(proof["surface_kind"], "opl_native_helper_indexing_proof")
        self.assertEqual(
            proof["covered_index_keys"],
            [
                "workspace_registry_index",
                "managed_session_ledger_index",
                "artifact_projection_index",
                "attention_queue_index",
                "runtime_health_snapshot_index",
            ],
        )
        self.assertEqual(proof["coverage"]["workspace_registry_index"]["write_policy"], "opl_index_only")
        self.assertIn("mag_repo_tracked_truth_remains_authoritative", proof["readonly_boundaries"])
        self.assertIn("quality_gate_remains_mag_owned", proof["readonly_boundaries"])
        self.assertIn("submission_ready_gate_remains_mag_owned", proof["readonly_boundaries"])
