from __future__ import annotations

import json
import unittest
from pathlib import Path


SCHEMA_ROOT = Path(__file__).resolve().parents[1] / "schemas" / "v1"


def load_schema(name: str) -> dict[str, object]:
    return json.loads((SCHEMA_ROOT / name).read_text(encoding="utf-8"))


class ProductEntrySurfaceSchemaRegistryTest(unittest.TestCase):
    def test_product_surface_schemas_require_family_orchestration_companion(self) -> None:
        schema_files = [
            "grant-progress.schema.json",
            "grant-cockpit.schema.json",
            "grant-direct-entry.schema.json",
            "grant-user-loop.schema.json",
        ]
        for schema_file in schema_files:
            with self.subTest(schema=schema_file):
                payload = load_schema(schema_file)
                required = payload.get("required")
                self.assertIsInstance(required, list)
                self.assertIn("family_orchestration", required)

    def test_product_entry_surface_schemas_require_quickstart_companion(self) -> None:
        manifest_schema = load_schema("product-entry-manifest.schema.json")
        manifest_required = set(manifest_schema["$defs"]["productEntryManifest"]["required"])
        self.assertLessEqual(
            {
                "opl_provider_runtime_contract",
                "runtime_control",
                "family_orchestration",
                "product_entry_start",
                "product_entry_overview",
                "product_entry_preflight",
                "product_entry_readiness",
                "grant_authoring_readiness",
                "product_entry_quickstart",
                "family_action_catalog",
                "family_stage_control_plane",
                "domain_memory_descriptor",
                "temporal_stage_run_consumption_policy",
            },
            manifest_required,
        )

        status_schema = load_schema("product-status.schema.json")
        status_required = set(status_schema["$defs"]["productStatus"]["required"])
        self.assertLessEqual(
            {
                "family_orchestration",
                "product_entry_start",
                "product_entry_overview",
                "product_entry_preflight",
                "product_entry_readiness",
                "grant_authoring_readiness",
                "product_entry_quickstart",
                "temporal_stage_run_consumption_policy",
            },
            status_required,
        )

    def test_product_entry_surface_schemas_pin_opl_provider_runtime_contract_shape(self) -> None:
        manifest_schema = load_schema("product-entry-manifest.schema.json")
        provider_runtime = manifest_schema["$defs"]["oplProviderRuntimeContractSurface"]
        self.assertLessEqual(
            {
                "shared_contract_ref",
                "runtime_owner",
                "domain_owner",
                "executor_owner",
                "fail_closed_rules",
            },
            set(provider_runtime["required"]),
        )
        self.assertEqual(
            provider_runtime["properties"]["shared_contract_ref"]["const"],
            "contracts/opl-framework/managed-runtime-three-layer-contract.json",
        )
        self.assertEqual(provider_runtime["properties"]["runtime_owner"]["const"], "configured_family_runtime_provider")
        self.assertEqual(provider_runtime["properties"]["domain_owner"]["const"], "med-autogrant")
        self.assertEqual(provider_runtime["properties"]["executor_owner"]["const"], "codex_cli")

    def test_product_entry_surface_schemas_pin_runtime_control_shape(self) -> None:
        manifest_schema = load_schema("product-entry-manifest.schema.json")
        runtime_control = manifest_schema["$defs"]["runtimeControlSurface"]
        self.assertEqual(runtime_control["properties"]["surface_kind"]["const"], "runtime_control")
        self.assertLessEqual(
            {
                "surface_kind",
                "runtime_owner",
                "domain_owner",
                "executor_owner",
                "session_locator",
                "restore_point",
                "semantic_closure",
                "progress_surface",
                "artifact_pickup_surface",
                "approval_control_surface",
                "direct_entry",
                "temporal_stage_run_consumption_policy_ref",
                "temporal_stage_run_consumption_policy",
            },
            set(runtime_control["required"]),
        )
        expected_refs = {
            "session_locator": "#/$defs/runtimeControlSessionLocator",
            "restore_point": "#/$defs/runtimeControlRestorePoint",
            "semantic_closure": "#/$defs/runtimeControlSemanticClosure",
            "progress_surface": "#/$defs/runtimeControlSurfaceRef",
            "artifact_pickup_surface": "#/$defs/runtimeControlSurfaceRef",
            "approval_control_surface": "#/$defs/runtimeControlSurfaceRef",
            "direct_entry": "#/$defs/runtimeControlDirectEntry",
        }
        for field, ref in expected_refs.items():
            with self.subTest(field=field):
                self.assertEqual(runtime_control["properties"][field]["$ref"], ref)
        self.assertEqual(
            runtime_control["properties"]["temporal_stage_run_consumption_policy_ref"]["const"],
            "/product_entry_manifest/temporal_stage_run_consumption_policy",
        )
        self.assertEqual(
            runtime_control["properties"]["temporal_stage_run_consumption_policy"]["$ref"],
            "#/$defs/temporalStageRunConsumptionPolicy",
        )

    def test_product_entry_manifest_schema_pins_temporal_stage_run_consumption_policy(self) -> None:
        manifest_schema = load_schema("product-entry-manifest.schema.json")
        policy = manifest_schema["$defs"]["temporalStageRunConsumptionPolicy"]
        self.assertEqual(policy["properties"]["surface_kind"]["const"], "temporal_stage_run_consumption_policy")
        self.assertIn("contract_ref", policy["required"])
        self.assertIn("grant_ready_completion_audit", policy["required"])
        self.assertEqual(
            policy["properties"]["contract_ref"]["const"],
            "contracts/temporal_stage_run_consumption_policy.json",
        )
        self.assertEqual(policy["properties"]["runtime_substrate_owner"]["const"], "one-person-lab")
        self.assertEqual(policy["properties"]["runtime_substrate"]["const"], "temporal")
        self.assertEqual(policy["properties"]["stage_run_substrate_owner"]["const"], "one-person-lab")
        self.assertEqual(policy["properties"]["stage_run_owner_surface"]["const"], "opl_temporal_stage_run_kernel")
        self.assertEqual(policy["properties"]["temporal_attempt_ledger_owner"]["const"], "one-person-lab/OPL")
        for field in (
            "provider_completion_is_domain_completion",
            "domain_repo_can_own_temporal_runtime",
            "domain_repo_can_write_opl_stage_attempts",
            "domain_repo_can_own_stage_run_substrate",
            "mag_can_own_status_user_loop_direct_entry_domain_handler_or_workbench_shell",
            "generated_surface_ready_can_claim_domain_ready",
            "mag_writes_opl_stage_attempt_records",
        ):
            with self.subTest(policy_false_field=field):
                self.assertFalse(policy["properties"][field]["const"])
        boundary = policy["properties"]["authority_boundary"]["properties"]
        for field in (
            "provider_completion_counts_as_domain_completion",
            "generated_surface_ready_counts_as_domain_ready",
            "mag_can_write_opl_stage_attempts",
            "mag_can_own_temporal_runtime",
        ):
            self.assertFalse(boundary[field]["const"])
        stage_run_boundary = policy["properties"]["stage_run_consumption_boundary"]
        self.assertEqual(
            stage_run_boundary["properties"]["surface_kind"]["const"],
            "mag_stage_run_consumption_boundary",
        )
        self.assertEqual(
            stage_run_boundary["properties"]["consumer_role"]["const"],
            "consume_opl_stage_run_refs_only",
        )
        self.assertEqual(
            stage_run_boundary["properties"]["opl_substrate_owner"]["const"],
            "one-person-lab",
        )
        self.assertFalse(
            stage_run_boundary["properties"]["payload_body_allowed"]["const"]
        )
        self.assertFalse(
            stage_run_boundary["properties"]["mag_runtime_state_write_allowed"]["const"]
        )
        stage_run_authority = stage_run_boundary["properties"]["authority_boundary"]["properties"]
        for field in (
            "mag_can_start_temporal_worker",
            "mag_can_schedule_stage_run",
            "mag_can_write_attempt_ledger",
            "mag_can_own_generated_shell",
        ):
            self.assertFalse(stage_run_authority[field]["const"])
        audit = policy["properties"]["grant_ready_completion_audit"]
        self.assertEqual(audit["properties"]["surface_kind"]["const"], "grant_ready_completion_audit")
        self.assertEqual(audit["properties"]["audit_id"]["const"], "mag.grant_ready_completion_audit.v1")
        self.assertEqual(audit["properties"]["state"]["const"], "blocked_without_mag_owner_closing_ref")
        claim_permissions = audit["properties"]["claim_permissions"]["properties"]
        for field in ("grant_ready", "quality_ready", "export_ready", "submission_ready"):
            self.assertFalse(claim_permissions[field]["const"])
        audit_boundary = audit["properties"]["authority_boundary"]["properties"]
        for field in (
            "provider_completion_counts_as_grant_ready",
            "schema_completeness_counts_as_grant_ready",
            "generated_surface_ready_counts_as_grant_ready",
            "focused_tests_count_as_grant_ready",
        ):
            self.assertFalse(audit_boundary[field]["const"])

    def test_product_entry_manifest_schema_pins_functional_harness_consumer_boundary(self) -> None:
        manifest_schema = load_schema("product-entry-manifest.schema.json")
        thinning = manifest_schema["$defs"]["magConsumerThinningContract"]
        self.assertIn("functional_harness_consumer_coverage", thinning["required"])

        consumed = thinning["properties"]["consumed_opl_standard_surfaces"]
        self.assertIn("functional_harness_consumer_coverage_ref", consumed["required"])
        consumed_primitives = consumed["properties"]["consumed_generic_primitives"]["const"]
        self.assertIn("functional_harness_queue_stage_attempt_typed_closeout", consumed_primitives)
        self.assertIn("functional_harness_restart_dead_letter_repair_human_gate", consumed_primitives)

        exposed_refs = thinning["properties"]["exposed_domain_handler_return_refs"]
        self.assertIn("generated_surface_bridge_exit_gate_ref", exposed_refs["required"])
        self.assertIn("generated_hosted_default_caller_proof_ref", exposed_refs["required"])
        self.assertIn("generated_hosted_default_caller_proof", thinning["required"])
        default_caller_proof = thinning["properties"]["generated_hosted_default_caller_proof"]
        self.assertEqual(
            default_caller_proof["properties"]["surface_kind"]["const"],
            "mag_generated_hosted_default_caller_proof",
        )
        self.assertEqual(
            default_caller_proof["properties"]["current_mag_role"]["const"],
            "domain_handler_ref_only_adapter_and_migration_input",
        )
        parity = default_caller_proof["properties"]["direct_hosted_parity_workorder"]
        self.assertEqual(
            parity["properties"]["required_request_id"]["const"],
            "direct_hosted_parity_no_regression",
        )
        self.assertFalse(parity["properties"]["claims_parity_passed"]["const"])
        no_forbidden_write = default_caller_proof["properties"]["no_forbidden_write_boundary"]
        self.assertEqual(
            no_forbidden_write["properties"]["required_request_id"]["const"],
            "continuous_no_forbidden_write_guard",
        )
        self.assertFalse(
            no_forbidden_write["properties"]["claims_no_forbidden_write_passed"]["const"]
        )
        classification = default_caller_proof["properties"]["repo_local_product_shell_classification"]
        self.assertFalse(classification["properties"]["generic_runtime_owner"]["const"])
        self.assertTrue(classification["properties"]["migration_input"]["const"])
        bridge_ref = "/product_entry_manifest/mag_consumer_thinning_contract/generated_surface_handoff/bridge_exit_gate"
        self.assertEqual(exposed_refs["properties"]["generated_surface_bridge_exit_gate_ref"]["const"], bridge_ref)
        evidence_request_ref = (
            "/product_entry_manifest/mag_consumer_thinning_contract/external_evidence_request_pack"
        )
        self.assertIn("external_evidence_request_pack_ref", exposed_refs["required"])
        self.assertEqual(
            exposed_refs["properties"]["external_evidence_request_pack_ref"]["const"],
            evidence_request_ref,
        )
        bridge_refs = thinning["properties"]["bridge_exit_gate_refs"]
        self.assertIn("bridge_exit_gate_refs", thinning["required"])
        self.assertEqual(
            bridge_refs["properties"]["legacy_exit_gate_policy"]["const"],
            "delete_or_history_tombstone_after_replacement_proof",
        )
        self.assertFalse(bridge_refs["properties"]["claims_all_bridge_exits_complete"]["const"])
        self.assertTrue(bridge_refs["properties"]["mag_handler_boundary_ready"]["const"])
        generated_handoff = manifest_schema["$defs"]["ownerReceiptContract"]["properties"][
            "generated_surface_handoff"
        ]
        currentness = generated_handoff["properties"]["current_mag_path_status"]["properties"]
        self.assertEqual(
            currentness["surface_kind"]["const"],
            "mag_generated_surface_handoff_currentness_proof",
        )
        self.assertEqual(currentness["status"]["const"], "current")
        self.assertEqual(currentness["checked_surface_count"]["const"], 6)
        self.assertEqual(currentness["missing_current_mag_path_count"]["const"], 0)
        self.assertEqual(
            currentness["stale_path_policy"]["const"],
            "history_or_source_ref_refresh_only",
        )
        self.assertTrue(currentness["claims_opl_replacement_exists"]["const"])
        self.assertFalse(currentness["claims_domain_repo_physical_delete_authorized"]["const"])
        self.assertFalse(currentness["claims_all_bridge_exits_complete"]["const"])
        self.assertFalse(currentness["claims_production_long_run_soak_complete"]["const"])
        generated_surface = generated_handoff["properties"]["generated_or_bridge_surfaces"]["items"]
        self.assertIn("current_mag_path_status", generated_surface["required"])
        path_status = generated_surface["properties"]["current_mag_path_status"]["properties"]
        self.assertEqual(path_status["surface_kind"]["const"], "mag_current_path_status")
        self.assertEqual(path_status["status"]["const"], "current")
        self.assertEqual(path_status["missing_count"]["const"], 0)
        self.assertEqual(path_status["stale_path_policy"]["const"], "history_or_source_ref_refresh_only")
        self.assertTrue(path_status["paths"]["items"]["properties"]["exists"]["const"])
        coverage = thinning["properties"]["functional_harness_consumer_coverage"]
        self.assertEqual(
            coverage["properties"]["surface_kind"]["const"],
            "mag_functional_harness_consumer_coverage",
        )
        self.assertEqual(
            coverage["properties"]["coverage_chain_ids"]["const"],
            [
                "memory_refs_only_writeback_chain",
                "queue_stage_attempt_typed_closeout_chain",
                "generic_transition_runner_chain",
                "restart_dead_letter_repair_human_gate_chain",
            ],
        )
        self.assertFalse(coverage["properties"]["claims_opl_functional_harness_pass"]["const"])
        self.assertFalse(coverage["properties"]["claims_grant_ready"]["const"])
        self.assertFalse(coverage["properties"]["claims_export_ready"]["const"])
        self.assertFalse(
            coverage["properties"]["fail_closed_rules"]["properties"]["opl_harness_pass_is_grant_ready"][
                "const"
            ]
        )
        self.assertFalse(
            coverage["properties"]["fail_closed_rules"]["properties"]["opl_harness_pass_is_export_ready"][
                "const"
            ]
        )
        self.assertFalse(
            coverage["properties"]["fail_closed_rules"]["properties"]["opl_can_hold_generic_runtime_in_mag"][
                "const"
            ]
        )

        followthrough = thinning["properties"]["functional_followthrough_gap_classification"]
        self.assertIn("functional_followthrough_gap_classification", thinning["required"])
        self.assertEqual(
            followthrough["properties"]["surface_kind"]["const"],
            "mag_functional_followthrough_gap_classification",
        )
        self.assertEqual(
            followthrough["properties"]["state"]["const"],
            "mag_handler_boundary_ready_external_evidence_gated",
        )
        self.assertEqual(
            followthrough["properties"]["mag_functional_structure_gap_count"]["const"],
            0,
        )
        self.assertEqual(
            followthrough["properties"]["remaining_mag_functional_structure_gaps"]["maxItems"],
            0,
        )
        self.assertEqual(
            followthrough["properties"]["closed_classification_surface_ids"]["const"],
            [
                "P1_adapter_thinning_and_pack_input",
                "P2_package_export_artifact_lifecycle_handoff",
                "P3_grant_strategy_memory_locator_writeback_handoff",
                "P4_skeleton_generated_surface_and_legacy_retirement",
            ],
        )
        self.assertEqual(
            followthrough["properties"]["reclassified_testing_evidence_gap_ids"]["const"],
            [
                "real_workspace_memory_body_migration_and_retrieval_writeback_apply",
                "real_workspace_package_lifecycle_and_cleanup_restore_retention_receipts",
                "opl_generated_surface_production_consumption_no_regression",
                "focused_opl_hosted_receipt_verification",
                "continuous_live_receipt_reconciliation",
                "long_run_live_soak_and_no_forbidden_write_proof",
            ],
        )
        followthrough_authority = followthrough["properties"]["authority_boundary"]["properties"]
        self.assertTrue(followthrough_authority["mag_repo_functional_structure_gaps_zero"]["const"])
        self.assertTrue(followthrough_authority["classification_closed"]["const"])
        self.assertFalse(followthrough_authority["followthrough_gaps_open"]["const"])
        self.assertTrue(followthrough_authority["claims_opl_replacement_exists"]["const"])
        self.assertFalse(
            followthrough_authority["claims_domain_repo_physical_delete_authorized"]["const"]
        )
        self.assertFalse(
            followthrough_authority["claims_opl_generated_surface_production_consumed"]["const"]
        )
        self.assertFalse(followthrough_authority["claims_production_long_run_soak_complete"]["const"])

    def test_product_entry_surface_schemas_pin_skill_runtime_continuity_shape(self) -> None:
        manifest_schema = load_schema("product-entry-manifest.schema.json")
        skill_projection = manifest_schema["$defs"]["skillDomainProjection"]
        self.assertLessEqual(
            {
                "plugin_name",
                "skill_entry",
                "skill_semantics",
                "entry_command",
                "runtime_continuity",
                "opl_stage_runtime_registration",
                "standard_domain_agent_skeleton",
            },
            set(skill_projection["required"]),
        )
        self.assertEqual(skill_projection["properties"]["skill_semantics"]["const"], "domain_app")
        self.assertEqual(skill_projection["properties"]["entry_shell_key"]["const"], "product_status")
        self.assertEqual(
            skill_projection["properties"]["runtime_continuity"]["$ref"],
            "#/$defs/skillRuntimeContinuitySurface",
        )
        self.assertEqual(
            skill_projection["properties"]["opl_stage_runtime_registration"]["$ref"],
            "#/$defs/oplStageRuntimeRegistration",
        )
        self.assertEqual(
            skill_projection["properties"]["standard_domain_agent_skeleton"]["$ref"],
            "#/$defs/standardDomainAgentSkeleton",
        )
        domain_skeleton = manifest_schema["$defs"]["standardDomainAgentSkeleton"]
        self.assertEqual(domain_skeleton["properties"]["surface_kind"]["const"], "standard_domain_agent_skeleton")
        self.assertEqual(domain_skeleton["properties"]["skeleton_id"]["const"], "mag.standard_domain_agent_skeleton.v1")
        self.assertEqual(
            domain_skeleton["properties"]["artifact_locator_ref"]["const"],
            "/product_entry_manifest/artifact_locator_contract",
        )
        self.assertEqual(
            domain_skeleton["properties"]["controlled_stage_attempt_ref"]["const"],
            "/product_entry_manifest/controlled_stage_attempt_projection",
        )
        self.assertEqual(
            manifest_schema["$defs"]["artifactLocatorContract"]["properties"]["surface_kind"]["const"],
            "domain_artifact_locator_contract",
        )
        self.assertEqual(
            manifest_schema["$defs"]["controlledStageAttemptProjection"]["properties"]["surface_kind"]["const"],
            "controlled_stage_attempt_projection",
        )
        domain_memory = manifest_schema["$defs"]["domainMemoryDescriptorLocator"]
        self.assertLessEqual(
            {
                "migration_plan",
                "writeback_proposal_generator",
                "accept_reject_command",
                "receipt_locator",
                "operator_receipt_projection",
            },
            set(domain_memory["required"]),
        )
        self.assertEqual(
            domain_memory["properties"]["migration_plan"]["properties"]["surface_kind"]["const"],
            "domain_memory_migration_plan",
        )
        self.assertEqual(
            domain_memory["properties"]["migration_plan"]["properties"]["plan_id"]["const"],
            "mag.domain_memory_migration_plan.v1",
        )
        self.assertEqual(
            domain_memory["properties"]["migration_plan"]["properties"]["migration_state"]["const"],
            "runtime_apply_contract_landed",
        )
        self.assertEqual(
            domain_memory["properties"]["writeback_proposal_generator"]["properties"]["surface_kind"]["const"],
            "domain_memory_writeback_proposal_generator",
        )
        self.assertEqual(
            domain_memory["properties"]["accept_reject_command"]["properties"]["surface_kind"]["const"],
            "domain_memory_accept_reject_command",
        )
        self.assertEqual(
            domain_memory["properties"]["operator_receipt_projection"]["properties"]["surface_kind"]["const"],
            "mag_domain_memory_operator_receipt_projection",
        )
        self.assertEqual(
            domain_memory["properties"]["receipt_locator"]["properties"]["surface_kind"]["const"],
            "domain_memory_receipt_locator",
        )
        family_memory_ref = manifest_schema["$defs"]["familyDomainMemoryRef"]
        self.assertEqual(family_memory_ref["properties"]["surface_kind"]["const"], "family_domain_memory_ref")
        self.assertEqual(family_memory_ref["properties"]["version"]["const"], "family-domain-memory-ref.v1")
        self.assertIn("forbidden_opl_authority", family_memory_ref["properties"]["authority_boundary"]["required"])
        self.assertEqual(
            family_memory_ref["properties"]["authority_boundary"]["properties"]["forbidden_opl_authority"][
                "contains"
            ],
            {"const": "memory_store_owner"},
        )
        self.assertEqual(
            manifest_schema["$defs"]["productEntryManifest"]["properties"]["domain_memory_descriptor"]["$ref"],
            "#/$defs/familyDomainMemoryRef",
        )
        self.assertEqual(
            manifest_schema["$defs"]["oplStageRuntimeRegistration"]["properties"]["surface_kind"]["const"],
            "opl_stage_runtime_domain_registration",
        )
        self.assertEqual(
            manifest_schema["$defs"]["oplStageRuntimeRegistration"]["properties"]["executor_owner"]["const"],
            "codex_cli",
        )
        self.assertEqual(
            manifest_schema["$defs"]["oplStageRuntimeRegistration"]["properties"]["executor_adapter_owner"]["const"],
            "one-person-lab",
        )
        executor_adapter_contract = manifest_schema["$defs"]["executorAdapterContract"]
        self.assertEqual(
            executor_adapter_contract["properties"]["contract_ref"]["const"],
            "contracts/opl-framework/family-executor-adapter-defaults.json",
        )
        self.assertEqual(
            executor_adapter_contract["properties"]["receipt_contract"]["const"],
            "AgentExecutionReceipt",
        )
        self.assertEqual(
            executor_adapter_contract["properties"]["canonical_executor_backends"]["const"],
            ["codex_cli", "hermes_agent", "claude_code"],
        )
        self.assertFalse(executor_adapter_contract["properties"]["fallback_allowed"]["const"])
        stage_registration = manifest_schema["$defs"]["oplStageRuntimeRegistration"]
        self.assertLessEqual({"native_helper_consumption", "family_lifecycle_adapter"}, set(stage_registration["required"]))
        self.assertEqual(stage_registration["properties"]["family_lifecycle_adapter"]["$ref"], "#/$defs/oplFamilyLifecycleAdapter")
        native_helper_consumption = stage_registration["properties"]["native_helper_consumption"]
        self.assertEqual(native_helper_consumption["$ref"], "#/$defs/oplNativeHelperConsumption")
        native_helper_defs = manifest_schema["$defs"]["oplNativeHelperConsumption"]
        native_helper_required = set(native_helper_defs["required"])
        self.assertLessEqual({"proof_surface", "index_consumption_policy", "authority_boundary"}, native_helper_required)
        self.assertNotIn("language", native_helper_required)
        self.assertEqual(native_helper_defs["properties"]["proof_surface"]["$ref"], "#/$defs/oplNativeHelperIndexingProof")
        self.assertEqual(native_helper_defs["properties"]["authority_boundary"]["$ref"], "#/$defs/oplNativeHelperAuthorityBoundary")
        self.assertEqual(
            manifest_schema["$defs"]["oplNativeHelperIndexingProof"]["properties"]["surface_kind"]["const"],
            "opl_native_helper_ref_consumption_proof",
        )
        self.assertNotIn("proof_role", manifest_schema["$defs"]["oplNativeHelperIndexRef"]["required"])
        self.assertNotIn("oplNativeHelperBackedIndex", manifest_schema["$defs"])
        lifecycle_adapter = manifest_schema["$defs"]["oplFamilyLifecycleAdapter"]
        self.assertLessEqual(
            {
                "surface_kind",
                "adapter_id",
                "contract_refs",
                "persistence_projection",
                "lifecycle_projection",
                "owner_route_discovery",
                "non_goals",
            },
            set(lifecycle_adapter["required"]),
        )
        self.assertEqual(
            lifecycle_adapter["properties"]["surface_kind"]["const"],
            "opl_family_lifecycle_adapter",
        )
        owner_split = (
            lifecycle_adapter["properties"]["owner_route_discovery"]["$ref"],
            manifest_schema["$defs"]["oplFamilyOwnerRouteDiscovery"]["properties"]["owner_split"],
        )
        self.assertEqual(owner_split[0], "#/$defs/oplFamilyOwnerRouteDiscovery")
        self.assertEqual(
            owner_split[1]["properties"]["runtime_kernel_owner"]["const"],
            "configured_family_runtime_provider",
        )
        self.assertEqual(owner_split[1]["properties"]["executor_owner"]["const"], "codex_cli")
        self.assertEqual(owner_split[1]["properties"]["executor_adapter_owner"]["const"], "one-person-lab")

        runtime_continuity = manifest_schema["$defs"]["skillRuntimeContinuitySurface"]
        self.assertEqual(runtime_continuity["properties"]["surface_kind"]["const"], "skill_runtime_continuity")
        self.assertLessEqual(
            {
                "surface_kind",
                "runtime_owner",
                "domain_owner",
                "executor_owner",
                "authoring_continuity",
                "funding_call_lock",
                "quality_closure_surface",
                "submission_ready_gate",
                "session_surface_ref",
                "progress_surface_ref",
                "artifact_surface_ref",
            },
            set(runtime_continuity["required"]),
        )

    def test_product_entry_surface_schemas_pin_start_companion_shape(self) -> None:
        manifest_schema = load_schema("product-entry-manifest.schema.json")
        start = manifest_schema["$defs"]["productEntryStart"]
        self.assertEqual(start["properties"]["surface_kind"]["const"], "product_entry_start")
        self.assertLessEqual(
            {"surface_kind", "recommended_mode_id", "modes", "resume_surface", "human_gate_ids"},
            set(start["required"]),
        )
        self.assertEqual(
            start["properties"]["modes"]["items"]["$ref"],
            "#/$defs/productEntryStartMode",
        )
        self.assertEqual(
            start["properties"]["resume_surface"]["$ref"],
            "#/$defs/familyOrchestrationResumeContract",
        )

        status_schema = load_schema("product-status.schema.json")
        self.assertEqual(
            status_schema["$defs"]["productStatus"]["properties"]["product_entry_start"]["$ref"],
            "product-entry-manifest.schema.json#/$defs/productEntryStart",
        )

    def test_product_entry_surface_schemas_pin_overview_companion_shape(self) -> None:
        manifest_schema = load_schema("product-entry-manifest.schema.json")
        overview = manifest_schema["$defs"]["productEntryOverview"]
        self.assertEqual(overview["properties"]["surface_kind"]["const"], "product_entry_overview")
        self.assertLessEqual(
            {
                "surface_kind",
                "product_entry_command",
                "operator_loop_command",
                "progress_surface",
                "resume_surface",
                "human_gate_ids",
            },
            set(overview["required"]),
        )
        self.assertEqual(
            overview["properties"]["progress_surface"]["$ref"],
            "#/$defs/productEntryOverviewProgressSurface",
        )
        self.assertEqual(
            overview["properties"]["resume_surface"]["$ref"],
            "#/$defs/productEntryOverviewResumeSurface",
        )

        status_schema = load_schema("product-status.schema.json")
        self.assertEqual(
            status_schema["$defs"]["productStatus"]["properties"]["product_entry_overview"]["$ref"],
            "product-entry-manifest.schema.json#/$defs/productEntryOverview",
        )

    def test_product_entry_surface_schemas_pin_preflight_companion_shape(self) -> None:
        manifest_schema = load_schema("product-entry-manifest.schema.json")
        preflight = manifest_schema["$defs"]["productEntryPreflight"]
        self.assertEqual(preflight["properties"]["surface_kind"]["const"], "product_entry_preflight")
        self.assertLessEqual(
            {"surface_kind", "ready_to_try_now", "recommended_check_command", "blocking_check_ids", "checks"},
            set(preflight["required"]),
        )
        self.assertEqual(
            preflight["properties"]["checks"]["items"]["$ref"],
            "#/$defs/productEntryPreflightCheck",
        )

        status_schema = load_schema("product-status.schema.json")
        self.assertEqual(
            status_schema["$defs"]["productStatus"]["properties"]["product_entry_preflight"]["$ref"],
            "product-entry-manifest.schema.json#/$defs/productEntryPreflight",
        )

    def test_product_entry_surface_schemas_pin_authoring_readiness_companion_shape(self) -> None:
        manifest_schema = load_schema("product-entry-manifest.schema.json")
        product_readiness = manifest_schema["$defs"]["productEntryReadiness"]
        self.assertEqual(product_readiness["properties"]["surface_kind"]["const"], "product_entry_readiness")
        self.assertEqual(
            product_readiness["properties"]["verdict"]["const"],
            "agent_assisted_ready_not_product_grade",
        )
        self.assertLessEqual(
            {"surface_kind", "verdict", "usable_now", "fully_automatic", "blocking_gaps"},
            set(product_readiness["required"]),
        )
        readiness = manifest_schema["$defs"]["grantAuthoringReadiness"]
        self.assertEqual(readiness["properties"]["surface_kind"]["const"], "grant_authoring_readiness")
        self.assertEqual(
            readiness["properties"]["verdict"]["const"],
            "agent_assisted_cli_ready_not_full_autopilot",
        )
        self.assertLessEqual(
            {"surface_kind", "verdict", "fully_automatic", "usable_now", "workflow_coverage", "blocking_gaps"},
            set(readiness["required"]),
        )
        self.assertEqual(
            readiness["properties"]["workflow_coverage"]["items"]["$ref"],
            "#/$defs/grantAuthoringWorkflowCoverageItem",
        )
        coverage_item = manifest_schema["$defs"]["grantAuthoringWorkflowCoverageItem"]
        self.assertEqual(
            coverage_item["properties"]["coverage_status"]["enum"],
            ["landed_route", "partially_supported", "not_landed"],
        )

        status_schema = load_schema("product-status.schema.json")
        self.assertEqual(
            status_schema["$defs"]["productStatus"]["properties"]["product_entry_readiness"]["$ref"],
            "product-entry-manifest.schema.json#/$defs/productEntryReadiness",
        )
        self.assertEqual(
            status_schema["$defs"]["productStatus"]["properties"]["grant_authoring_readiness"]["$ref"],
            "product-entry-manifest.schema.json#/$defs/grantAuthoringReadiness",
        )


if __name__ == "__main__":
    unittest.main()
