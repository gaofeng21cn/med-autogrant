from __future__ import annotations

import tomllib


from product_entry_cases.support import *  # noqa: F401,F403


class ProductEntryRuntimeRegistrationTest(unittest.TestCase):
    def test_default_install_and_runtime_registration_do_not_require_hermes(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        pyproject = tomllib.loads((REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
        lock = tomllib.loads((REPO_ROOT / "uv.lock").read_text(encoding="utf-8"))
        lock_package = next(package for package in lock["package"] if package["name"] == "med-autogrant")

        self.assertNotIn("hermes-agent[acp]", pyproject["project"]["dependencies"])
        self.assertIn("hermes-agent[acp]", pyproject["project"]["optional-dependencies"]["proof"])
        self.assertNotIn("hermes-agent", {dependency["name"] for dependency in lock_package["dependencies"]})
        self.assertEqual(lock_package["optional-dependencies"]["proof"][0]["name"], "hermes-agent")

        manifest = MedAutoGrantProductEntry().build_product_entry_manifest(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
        )["product_entry_manifest"]

        self.assertEqual(manifest["managed_runtime_contract"]["runtime_owner"], "codex_cli")
        self.assertEqual(manifest["managed_runtime_contract"]["executor_owner"], "codex_cli")
        self.assertEqual(manifest["runtime_inventory"]["runtime_owner"], "codex_cli")
        self.assertEqual(manifest["runtime_inventory"]["executor_owner"], "codex_cli")
        self.assertEqual(manifest["runtime_inventory"]["substrate"], "codex_cli_default_runtime")
        self.assertEqual(manifest["runtime_control"]["runtime_owner"], "codex_cli")
        self.assertEqual(manifest["runtime_control"]["executor_owner"], "codex_cli")
        self.assertEqual(
            manifest["skill_catalog"]["skills"][0]["domain_projection"]["opl_stage_runtime_registration"][
                "family_lifecycle_adapter"
            ]["owner_route_discovery"]["owner_split"]["runtime_kernel_owner"],
            "codex_cli",
        )
        self.assertIn("hermes_agent", manifest["runtime_inventory"]["domain_projection"]["runtime"]["optional_carriers"])
        self.assertIn("claude_code", manifest["runtime_inventory"]["domain_projection"]["runtime"]["optional_carriers"])

    def test_opl_stage_runtime_registration_keeps_mag_as_truth_owner(self) -> None:
        from med_autogrant.product_entry_parts.runtime_registration import (
            _build_opl_native_helper_indexing_proof,
            _build_opl_stage_runtime_registration,
        )

        registration = _build_opl_stage_runtime_registration(
            runtime_summary={"runtime_owner": "codex-cli"},
            runtime_continuity={
                "session_locator_field": "grant_run_id",
                "recommended_resume_command": "medautogrant runtime-resume --journal journal.json --format json",
                "recommended_progress_command": "medautogrant grant-progress --input workspace.json --format json",
            },
            shell_commands={
                "product_status": "medautogrant product-status --input workspace.json --format json",
                "grant_progress": "medautogrant grant-progress --input workspace.json --format json",
                "grant_cockpit": "medautogrant grant-cockpit --input workspace.json --format json",
                "grant_direct_entry": "medautogrant grant-direct-entry --input workspace.json --task-intent <intent> --format json",
                "grant_user_loop": "medautogrant grant-user-loop --input workspace.json --task-intent <intent> --format json",
            },
            skill_catalog_command="medautogrant skill-catalog --input workspace.json --format json",
        )

        self.assertEqual(registration["surface_kind"], "opl_stage_runtime_domain_registration")
        self.assertEqual(registration["domain_owner"], "med-autogrant")
        self.assertEqual(registration["runtime_owner"], "codex-cli")
        self.assertEqual(registration["executor_owner"], "codex_cli")
        self.assertEqual(registration["executor_adapter_owner"], "one-person-lab")
        self.assertEqual(
            registration["executor_adapter_contract"],
            {
                "contract_ref": "contracts/opl-framework/family-executor-adapter-defaults.json",
                "registry_surface_kind": "opl_agent_executor_registry",
                "request_contract": "AgentExecutionRequest",
                "receipt_contract": "AgentExecutionReceipt",
                "canonical_executor_backends": ["codex_cli", "hermes_agent", "claude_code"],
                "default_executor": "codex_cli",
                "non_default_equivalence": "connectivity_lifecycle_receipt_audit_only",
                "fallback_allowed": False,
            },
        )
        self.assertEqual(registration["domain_entry_surface"]["surface_kind"], "product_status")
        self.assertEqual(
            registration["registration_surface"]["ref"],
            "/skill_catalog/skills/0/domain_projection/opl_stage_runtime_registration",
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
        family_adapter = registration["family_lifecycle_adapter"]
        self.assertEqual(family_adapter["surface_kind"], "opl_family_lifecycle_adapter")
        self.assertEqual(family_adapter["adapter_id"], "mag.opl_family.lifecycle_adapter.v1")
        self.assertEqual(family_adapter["adoption_surface"]["contract_ref"], "contracts/runtime-program/opl-family-contract-adoption.json")
        self.assertEqual(family_adapter["adoption_surface"]["opl_role"], "family-level projection consumer only")
        self.assertEqual(
            family_adapter["persistence_projection"]["source_surface_refs"],
            [
                "/skill_catalog/skills/0/domain_projection/runtime_continuity",
                "/session_continuity",
                "/artifact_inventory",
                "/runtime_control/restore_point",
            ],
        )
        self.assertEqual(
            family_adapter["persistence_projection"]["write_policy"],
            "opl_index_only_no_domain_truth_writes",
        )
        self.assertEqual(
            family_adapter["lifecycle_projection"]["maps_to_opl_contract"],
            "opl_family_runtime_attempt_contract.v1",
        )
        for required_field in (
            "attempt_state",
            "workspace_boundary",
            "owner_repo",
            "last_observed_projection",
        ):
            self.assertIn(required_field, family_adapter["lifecycle_projection"]["required_projection_fields"])
        self.assertEqual(
            family_adapter["owner_route_discovery"]["owner_split"]["domain_truth_owner"],
            "med-autogrant",
        )
        self.assertEqual(
            family_adapter["owner_route_discovery"]["owner_split"]["executor_owner"],
            "codex_cli",
        )
        self.assertEqual(
            family_adapter["owner_route_discovery"]["owner_split"]["executor_adapter_owner"],
            "one-person-lab",
        )
        self.assertIn(
            "medautogrant grant-user-loop",
            family_adapter["owner_route_discovery"]["route_surface_refs"]["operator_loop"]["command"],
        )
        self.assertEqual(
            family_adapter["adoption_projection"]["maps_to_opl_contract"],
            "opl_family_product_operator_projection.v1",
        )
        self.assertEqual(
            family_adapter["adoption_projection"]["required_operator_fields"],
            ["source_refs", "freshness", "owner_split", "next_surface_ref", "human_gate_reason"],
        )

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
