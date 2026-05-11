from __future__ import annotations

import json
import unittest
from pathlib import Path
from urllib.parse import urlparse


REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_ROOT = REPO_ROOT / "schemas" / "v1"

EXPECTED_SCHEMAS = {
    "common.schema.json",
    "applicant-profile.schema.json",
    "track-record.schema.json",
    "active-project-set.schema.json",
    "preliminary-evidence-pack.schema.json",
    "project-profile.schema.json",
    "funding-landscape-discovery-input.schema.json",
    "funding-landscape-discovery.schema.json",
    "funding-landscape-cache.schema.json",
    "funding-landscape-diff-report.schema.json",
    "project-profile-selection-input.schema.json",
    "project-profile-selection.schema.json",
    "critique-loop-report.schema.json",
    "authoring-mainline-loop-report.schema.json",
    "funding-opportunity-brief.schema.json",
    "direction-hypothesis.schema.json",
    "scientific-question-card.schema.json",
    "argument-chain.schema.json",
    "applicant-fit-mapping.schema.json",
    "application-draft.schema.json",
    "mentor-critique.schema.json",
    "revision-plan.schema.json",
    "nsfc-workspace.schema.json",
    "grant-intake-audit.schema.json",
    "grant-evidence-grounding.schema.json",
    "grant-quality-scorecard.schema.json",
    "grant-quality-diff.schema.json",
    "grant-quality-closure-dossier.schema.json",
    "grant-autonomy-controller-input.schema.json",
    "grant-autonomy-controller-report.schema.json",
    "service-safe-domain-surface.schema.json",
    "executor-routing-contract.schema.json",
    "product-entry.schema.json",
    "grant-progress.schema.json",
    "grant-cockpit.schema.json",
    "grant-direct-entry.schema.json",
    "grant-user-loop.schema.json",
    "product-entry-manifest.schema.json",
    "product-status.schema.json",
    "hosted-contract-bundle.schema.json",
    "submission-ready-package.schema.json",
    "schema-index.json",
}


def walk_refs(node: object) -> list[str]:
    refs: list[str] = []
    if isinstance(node, dict):
        for key, value in node.items():
            if key == "$ref" and isinstance(value, str):
                refs.append(value)
            else:
                refs.extend(walk_refs(value))
    elif isinstance(node, list):
        for item in node:
            refs.extend(walk_refs(item))
    return refs


class SchemaRegistryTest(unittest.TestCase):
    def test_expected_schema_files_exist(self) -> None:
        self.assertTrue(SCHEMA_ROOT.is_dir(), "schemas/v1 目录必须存在。")
        actual = {path.name for path in SCHEMA_ROOT.glob("*.json")}
        self.assertEqual(EXPECTED_SCHEMAS, actual)

    def test_schema_files_are_valid_json(self) -> None:
        for name in EXPECTED_SCHEMAS:
            with self.subTest(schema=name):
                payload = json.loads((SCHEMA_ROOT / name).read_text(encoding="utf-8"))
                self.assertIsInstance(payload, dict)

    def test_non_index_schemas_expose_core_metadata(self) -> None:
        for name in EXPECTED_SCHEMAS - {"schema-index.json"}:
            with self.subTest(schema=name):
                payload = json.loads((SCHEMA_ROOT / name).read_text(encoding="utf-8"))
                self.assertIn("$schema", payload)
                self.assertIn("$id", payload)
                self.assertIn("title", payload)
                self.assertIn("type", payload)

    def test_local_refs_are_resolvable(self) -> None:
        for name in EXPECTED_SCHEMAS - {"schema-index.json"}:
            with self.subTest(schema=name):
                payload = json.loads((SCHEMA_ROOT / name).read_text(encoding="utf-8"))
                refs = walk_refs(payload)
                for ref in refs:
                    parsed = urlparse(ref)
                    if parsed.scheme in {"http", "https"}:
                        continue
                    path_part = parsed.path
                    if not path_part:
                        continue
                    target = (SCHEMA_ROOT / path_part).resolve()
                    self.assertTrue(target.exists(), f"{name} 引用了不存在的 schema: {ref}")

    def test_workspace_schema_references_all_core_objects(self) -> None:
        payload = json.loads((SCHEMA_ROOT / "nsfc-workspace.schema.json").read_text(encoding="utf-8"))
        refs = set(walk_refs(payload))
        expected_refs = {
            "applicant-profile.schema.json",
            "track-record.schema.json",
            "active-project-set.schema.json",
            "preliminary-evidence-pack.schema.json",
            "project-profile.schema.json",
            "funding-opportunity-brief.schema.json",
            "direction-hypothesis.schema.json",
            "scientific-question-card.schema.json",
            "argument-chain.schema.json",
            "applicant-fit-mapping.schema.json",
            "application-draft.schema.json",
            "mentor-critique.schema.json",
            "revision-plan.schema.json",
            "grant-intake-audit.schema.json#/$defs/grantIntakeAudit",
            "grant-evidence-grounding.schema.json#/$defs/grantEvidenceGrounding",
        }
        for ref in expected_refs:
            self.assertIn(ref, refs)

    def test_schema_index_tracks_domain_handoff_contract_schemas(self) -> None:
        payload = json.loads((SCHEMA_ROOT / "schema-index.json").read_text(encoding="utf-8"))
        names = {item["name"]: item["file"] for item in payload["schemas"]}

        self.assertEqual(names["service_safe_domain_surface"], "service-safe-domain-surface.schema.json")
        self.assertEqual(names["executor_routing_contract"], "executor-routing-contract.schema.json")
        self.assertEqual(names["product_entry"], "product-entry.schema.json")
        self.assertEqual(names["grant_intake_audit_surface"], "grant-intake-audit.schema.json")
        self.assertEqual(names["grant_evidence_grounding_surface"], "grant-evidence-grounding.schema.json")
        self.assertEqual(names["grant_quality_scorecard_surface"], "grant-quality-scorecard.schema.json")
        self.assertEqual(names["grant_quality_diff_surface"], "grant-quality-diff.schema.json")
        self.assertEqual(
            names["grant_quality_closure_dossier_surface"],
            "grant-quality-closure-dossier.schema.json",
        )
        self.assertEqual(names["project_profile"], "project-profile.schema.json")
        self.assertEqual(names["funding_landscape_discovery_input"], "funding-landscape-discovery-input.schema.json")
        self.assertEqual(names["funding_landscape_discovery"], "funding-landscape-discovery.schema.json")
        self.assertEqual(names["funding_landscape_cache"], "funding-landscape-cache.schema.json")
        self.assertEqual(names["funding_landscape_diff_report"], "funding-landscape-diff-report.schema.json")
        self.assertEqual(names["project_profile_selection_input"], "project-profile-selection-input.schema.json")
        self.assertEqual(names["project_profile_selection"], "project-profile-selection.schema.json")
        self.assertEqual(names["critique_loop_report"], "critique-loop-report.schema.json")
        self.assertEqual(names["authoring_mainline_loop_report"], "authoring-mainline-loop-report.schema.json")
        self.assertEqual(names["grant_autonomy_controller_input"], "grant-autonomy-controller-input.schema.json")
        self.assertEqual(names["grant_autonomy_controller_report"], "grant-autonomy-controller-report.schema.json")
        self.assertEqual(names["grant_progress_projection"], "grant-progress.schema.json")
        self.assertEqual(names["grant_cockpit_projection"], "grant-cockpit.schema.json")
        self.assertEqual(names["grant_direct_entry_surface"], "grant-direct-entry.schema.json")
        self.assertEqual(names["grant_user_loop_surface"], "grant-user-loop.schema.json")
        self.assertEqual(names["product_entry_manifest_surface"], "product-entry-manifest.schema.json")
        self.assertEqual(names["product_status_surface"], "product-status.schema.json")
        self.assertEqual(names["hosted_contract_bundle"], "hosted-contract-bundle.schema.json")
        self.assertEqual(names["submission_ready_package"], "submission-ready-package.schema.json")

    def test_loop_report_schemas_require_quality_surfaces(self) -> None:
        critique_schema = json.loads((SCHEMA_ROOT / "critique-loop-report.schema.json").read_text(encoding="utf-8"))
        critique_required = critique_schema["required"]
        self.assertIn("grant_quality_scorecard", critique_required)
        self.assertIn("grant_quality_closure_dossier", critique_required)
        self.assertEqual(
            critique_schema["properties"]["grant_quality_scorecard"]["$ref"],
            "grant-quality-scorecard.schema.json#/$defs/grantQualityScorecard",
        )
        self.assertEqual(
            critique_schema["properties"]["grant_quality_closure_dossier"]["$ref"],
            "grant-quality-closure-dossier.schema.json#/$defs/grantQualityClosureDossier",
        )

        mainline_schema = json.loads((SCHEMA_ROOT / "authoring-mainline-loop-report.schema.json").read_text(encoding="utf-8"))
        mainline_required = mainline_schema["required"]
        self.assertIn("grant_quality_scorecard", mainline_required)
        self.assertIn("grant_quality_closure_dossier", mainline_required)
        self.assertEqual(
            mainline_schema["properties"]["grant_quality_scorecard"]["$ref"],
            "grant-quality-scorecard.schema.json#/$defs/grantQualityScorecard",
        )
        self.assertEqual(
            mainline_schema["properties"]["grant_quality_closure_dossier"]["$ref"],
            "grant-quality-closure-dossier.schema.json#/$defs/grantQualityClosureDossier",
        )

    def test_autonomy_controller_schemas_require_tranche_planning_surface(self) -> None:
        input_schema = json.loads((SCHEMA_ROOT / "grant-autonomy-controller-input.schema.json").read_text(encoding="utf-8"))
        self.assertIn("controller_plan", input_schema["properties"])
        self.assertEqual(
            input_schema["$defs"]["controllerPlan"]["required"],
            ["current_tranche", "tranche_objective", "tranche_success_gate"],
        )

        report_schema = json.loads((SCHEMA_ROOT / "grant-autonomy-controller-report.schema.json").read_text(encoding="utf-8"))
        report_required = report_schema["required"]
        self.assertIn("controller_checkpoint", report_required)
        self.assertIn("controller_plan", report_required)
        self.assertIn("tranche_history", report_required)
        self.assertIn("latest_quality_closure_dossier", report_required)
        self.assertIn("closure_package_queue", report_required)
        self.assertIn("active_closure_package", report_required)
        self.assertEqual(
            report_schema["$defs"]["controllerPlan"]["required"],
            [
                "current_tranche",
                "tranche_objective",
                "tranche_success_gate",
                "quality_summary",
                "closure_package_queue_ids",
                "active_closure_package_id",
                "active_closure_package_action",
                "active_closure_package_target_stage",
                "next_controller_action",
                "decision_basis",
            ],
        )
        decision_basis_required = report_schema["$defs"]["controllerDecisionBasis"]["required"]
        self.assertIn("quality_summary", decision_basis_required)
        self.assertIn("closure_package_queue_ids", decision_basis_required)
        self.assertIn("active_closure_package_id", decision_basis_required)
        self.assertIn("active_closure_package_action", decision_basis_required)
        self.assertIn("active_closure_package_target_stage", decision_basis_required)
        tranche_history_required = report_schema["$defs"]["trancheHistoryEntry"]["required"]
        self.assertIn("quality_summary", tranche_history_required)
        self.assertIn("closure_package_queue_ids", tranche_history_required)
        self.assertIn("active_closure_package_id", tranche_history_required)
        self.assertIn("active_closure_package_action", tranche_history_required)
        self.assertIn("active_closure_package_target_stage", tranche_history_required)
        self.assertEqual(
            report_schema["$defs"]["trancheHistoryEntry"]["properties"]["next_controller_action"]["$ref"],
            "#/$defs/controllerAction",
        )
        dossier_any_of = report_schema["properties"]["latest_quality_closure_dossier"]["anyOf"]
        self.assertEqual(
            dossier_any_of[0]["$ref"],
            "grant-quality-closure-dossier.schema.json#/$defs/grantQualityClosureDossier",
        )

    def test_project_profile_schema_supports_family_grammar_contract(self) -> None:
        payload = json.loads((SCHEMA_ROOT / "project-profile.schema.json").read_text(encoding="utf-8"))
        properties = payload["properties"]
        self.assertIn("grant_family_grammar", properties)
        self.assertIn("family_grammar_trace", properties)
        self.assertEqual(
            properties["grant_family_grammar"]["$ref"],
            "common.schema.json#/$defs/projectProfileGrantFamilyGrammar",
        )
        self.assertEqual(
            properties["family_grammar_trace"]["$ref"],
            "common.schema.json#/$defs/projectProfileFamilyGrammarTrace",
        )

    def test_common_schema_supports_structured_family_governance_policy(self) -> None:
        payload = json.loads((SCHEMA_ROOT / "common.schema.json").read_text(encoding="utf-8"))
        defs = payload["$defs"]

        self.assertIn("projectProfileFamilyGovernancePolicy", defs)
        governance_policy = defs["projectProfileFamilyGovernancePolicy"]
        self.assertEqual(
            governance_policy["required"],
            [
                "default_tranche",
                "preferred_stop_target",
                "quality_bar",
                "rollback_bias",
                "evidence_escalation_policy",
                "controller_defaults",
            ],
        )

        family_trace = defs["projectProfileFamilyGrammarTrace"]
        self.assertIn("governance_policy", family_trace["required"])
        self.assertEqual(
            family_trace["properties"]["governance_policy"]["$ref"],
            "#/$defs/projectProfileFamilyGovernancePolicy",
        )

        family_grammar = defs["projectProfileGrantFamilyGrammar"]
        self.assertIn("governance_policy", family_grammar["required"])
        self.assertEqual(
            family_grammar["properties"]["governance_policy"]["$ref"],
            "#/$defs/projectProfileFamilyGovernancePolicy",
        )

    def test_product_surface_schemas_require_family_orchestration_companion(self) -> None:
        schema_files = [
            "grant-progress.schema.json",
            "grant-cockpit.schema.json",
            "grant-direct-entry.schema.json",
            "grant-user-loop.schema.json",
        ]
        for schema_file in schema_files:
            with self.subTest(schema=schema_file):
                payload = json.loads((SCHEMA_ROOT / schema_file).read_text(encoding="utf-8"))
                required = payload.get("required")
                self.assertIsInstance(required, list)
                self.assertIn("family_orchestration", required)

    def test_product_entry_surface_schemas_require_quickstart_companion(self) -> None:
        manifest_schema = json.loads((SCHEMA_ROOT / "product-entry-manifest.schema.json").read_text(encoding="utf-8"))
        manifest_required = manifest_schema["$defs"]["productEntryManifest"]["required"]
        self.assertIn("managed_runtime_contract", manifest_required)
        self.assertIn("runtime_inventory", manifest_required)
        self.assertIn("task_lifecycle", manifest_required)
        self.assertIn("session_continuity", manifest_required)
        self.assertIn("runtime_control", manifest_required)
        self.assertIn("progress_projection", manifest_required)
        self.assertIn("artifact_inventory", manifest_required)
        self.assertIn("skill_catalog", manifest_required)
        self.assertIn("automation", manifest_required)
        self.assertIn("family_orchestration", manifest_required)
        self.assertIn("product_entry_start", manifest_required)
        self.assertIn("product_entry_overview", manifest_required)
        self.assertIn("product_entry_preflight", manifest_required)
        self.assertIn("product_entry_readiness", manifest_required)
        self.assertIn("grant_authoring_readiness", manifest_required)
        self.assertIn("autonomy_observability", manifest_required)
        self.assertIn("product_entry_quickstart", manifest_required)
        self.assertIn("family_action_catalog", manifest_required)
        self.assertIn("family_stage_control_plane", manifest_required)
        self.assertIn("domain_memory_descriptor", manifest_required)
        self.assertIn("action_catalog_projections", manifest_required)

        status_schema = json.loads((SCHEMA_ROOT / "product-status.schema.json").read_text(encoding="utf-8"))
        status_required = status_schema["$defs"]["productStatus"]["required"]
        self.assertIn("family_orchestration", status_required)
        self.assertIn("product_entry_start", status_required)
        self.assertIn("product_entry_overview", status_required)
        self.assertIn("product_entry_preflight", status_required)
        self.assertIn("product_entry_readiness", status_required)
        self.assertIn("grant_authoring_readiness", status_required)
        self.assertIn("product_entry_quickstart", status_required)

    def test_product_entry_surface_schemas_pin_managed_runtime_contract_shape(self) -> None:
        manifest_schema = json.loads((SCHEMA_ROOT / "product-entry-manifest.schema.json").read_text(encoding="utf-8"))
        managed_runtime = manifest_schema["$defs"]["managedRuntimeContractSurface"]
        self.assertEqual(
            managed_runtime["required"],
            [
                "shared_contract_ref",
                "runtime_owner",
                "domain_owner",
                "executor_owner",
                "supervision_status_surface",
                "attention_queue_surface",
                "recovery_contract_surface",
                "fail_closed_rules",
            ],
        )
        self.assertEqual(
            managed_runtime["properties"]["shared_contract_ref"]["const"],
            "contracts/opl-framework/managed-runtime-three-layer-contract.json",
        )
        self.assertEqual(managed_runtime["properties"]["runtime_owner"]["const"], "codex_cli")
        self.assertEqual(managed_runtime["properties"]["domain_owner"]["const"], "med-autogrant")
        self.assertEqual(managed_runtime["properties"]["executor_owner"]["const"], "med-autogrant")

    def test_product_entry_surface_schemas_pin_runtime_control_shape(self) -> None:
        manifest_schema = json.loads((SCHEMA_ROOT / "product-entry-manifest.schema.json").read_text(encoding="utf-8"))
        runtime_control = manifest_schema["$defs"]["runtimeControlSurface"]
        self.assertEqual(runtime_control["properties"]["surface_kind"]["const"], "runtime_control")
        self.assertEqual(
            runtime_control["required"],
            [
                "surface_kind",
                "version",
                "summary",
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
            ],
        )
        self.assertEqual(
            runtime_control["properties"]["session_locator"]["$ref"],
            "#/$defs/runtimeControlSessionLocator",
        )
        self.assertEqual(
            runtime_control["properties"]["restore_point"]["$ref"],
            "#/$defs/runtimeControlRestorePoint",
        )
        self.assertEqual(
            runtime_control["properties"]["semantic_closure"]["$ref"],
            "#/$defs/runtimeControlSemanticClosure",
        )
        self.assertEqual(
            runtime_control["properties"]["progress_surface"]["$ref"],
            "#/$defs/runtimeControlSurfaceRef",
        )
        self.assertEqual(
            runtime_control["properties"]["artifact_pickup_surface"]["$ref"],
            "#/$defs/runtimeControlSurfaceRef",
        )
        self.assertEqual(
            runtime_control["properties"]["approval_control_surface"]["$ref"],
            "#/$defs/runtimeControlSurfaceRef",
        )
        self.assertEqual(
            runtime_control["properties"]["direct_entry"]["$ref"],
            "#/$defs/runtimeControlDirectEntry",
        )

    def test_product_entry_surface_schemas_pin_skill_runtime_continuity_shape(self) -> None:
        manifest_schema = json.loads((SCHEMA_ROOT / "product-entry-manifest.schema.json").read_text(encoding="utf-8"))
        skill_projection = manifest_schema["$defs"]["skillDomainProjection"]
        self.assertEqual(
            skill_projection["required"],
            [
                "plugin_name",
                "skill_entry",
                "skill_semantics",
                "entry_shell_key",
                "entry_command",
                "recommended_shell",
                "supporting_shell_keys",
                "shell_commands",
                "runtime_continuity",
                "opl_stage_runtime_registration",
                "domain_agent_skeleton_mapping",
            ],
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
            skill_projection["properties"]["domain_agent_skeleton_mapping"]["$ref"],
            "#/$defs/domainAgentSkeletonMapping",
        )
        domain_skeleton = manifest_schema["$defs"]["domainAgentSkeletonMapping"]
        self.assertEqual(domain_skeleton["properties"]["surface_kind"]["const"], "standard_domain_agent_skeleton_mapping")
        self.assertEqual(domain_skeleton["properties"]["skeleton_id"]["const"], "mag.standard_domain_agent_skeleton.v1")
        self.assertEqual(domain_skeleton["properties"]["artifact_locator_ref"]["const"], "/product_entry_manifest/artifact_locator_contract")
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
        self.assertIn("migration_plan", domain_memory["required"])
        self.assertIn("writeback_proposal_generator", domain_memory["required"])
        self.assertIn("accept_reject_command", domain_memory["required"])
        self.assertIn("receipt_locator", domain_memory["required"])
        self.assertIn("operator_receipt_projection", domain_memory["required"])
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
        self.assertIn(
            "native_helper_consumption",
            manifest_schema["$defs"]["oplStageRuntimeRegistration"]["required"],
        )
        self.assertIn(
            "family_lifecycle_adapter",
            manifest_schema["$defs"]["oplStageRuntimeRegistration"]["required"],
        )
        self.assertEqual(
            manifest_schema["$defs"]["oplStageRuntimeRegistration"]["properties"]["family_lifecycle_adapter"]["$ref"],
            "#/$defs/oplFamilyLifecycleAdapter",
        )
        native_helper_consumption = manifest_schema["$defs"]["oplStageRuntimeRegistration"]["properties"][
            "native_helper_consumption"
        ]
        self.assertEqual(native_helper_consumption["$ref"], "#/$defs/oplNativeHelperConsumption")
        self.assertIn("proof_surface", manifest_schema["$defs"]["oplNativeHelperConsumption"]["required"])
        self.assertEqual(
            manifest_schema["$defs"]["oplNativeHelperConsumption"]["properties"]["proof_surface"]["$ref"],
            "#/$defs/oplNativeHelperIndexingProof",
        )
        self.assertIn("todo_wakeup_indexing", manifest_schema["$defs"]["oplNativeHelperIndexProof"]["properties"]["proof_role"]["enum"])
        lifecycle_adapter = manifest_schema["$defs"]["oplFamilyLifecycleAdapter"]
        self.assertEqual(
            lifecycle_adapter["required"],
            [
                "surface_kind",
                "version",
                "adapter_id",
                "contract_refs",
                "persistence_projection",
                "lifecycle_projection",
                "owner_route_discovery",
                "adoption_projection",
                "adoption_surface",
                "non_goals",
            ],
        )
        self.assertEqual(
            lifecycle_adapter["properties"]["surface_kind"]["const"],
            "opl_family_lifecycle_adapter",
        )

        runtime_continuity = manifest_schema["$defs"]["skillRuntimeContinuitySurface"]
        self.assertEqual(runtime_continuity["properties"]["surface_kind"]["const"], "skill_runtime_continuity")
        self.assertEqual(
            runtime_continuity["required"],
            [
                "surface_kind",
                "runtime_owner",
                "domain_owner",
                "executor_owner",
                "authoring_continuity",
                "funding_call_lock",
                "quality_closure_surface",
                "submission_ready_gate",
                "session_locator_field",
                "session_surface_ref",
                "progress_surface_ref",
                "artifact_surface_ref",
                "restore_point_surface_ref",
                "recommended_resume_command",
                "recommended_progress_command",
                "recommended_artifact_command",
            ],
        )

    def test_product_entry_surface_schemas_pin_start_companion_shape(self) -> None:
        manifest_schema = json.loads((SCHEMA_ROOT / "product-entry-manifest.schema.json").read_text(encoding="utf-8"))
        start = manifest_schema["$defs"]["productEntryStart"]
        self.assertEqual(start["properties"]["surface_kind"]["const"], "product_entry_start")
        self.assertEqual(
            start["required"],
            [
                "surface_kind",
                "summary",
                "recommended_mode_id",
                "modes",
                "resume_surface",
                "human_gate_ids",
            ],
        )
        self.assertEqual(
            start["properties"]["modes"]["items"]["$ref"],
            "#/$defs/productEntryStartMode",
        )
        self.assertEqual(
            start["properties"]["resume_surface"]["$ref"],
            "#/$defs/familyOrchestrationResumeContract",
        )

        status_schema = json.loads((SCHEMA_ROOT / "product-status.schema.json").read_text(encoding="utf-8"))
        self.assertEqual(
            status_schema["$defs"]["productStatus"]["properties"]["product_entry_start"]["$ref"],
            "product-entry-manifest.schema.json#/$defs/productEntryStart",
        )

    def test_product_entry_surface_schemas_pin_overview_companion_shape(self) -> None:
        manifest_schema = json.loads((SCHEMA_ROOT / "product-entry-manifest.schema.json").read_text(encoding="utf-8"))
        overview = manifest_schema["$defs"]["productEntryOverview"]
        self.assertEqual(overview["properties"]["surface_kind"]["const"], "product_entry_overview")
        self.assertEqual(
            overview["required"],
            [
                "surface_kind",
                "summary",
                "product_entry_command",
                "recommended_command",
                "operator_loop_command",
                "project_profile_label",
                "template_label",
                "critique_policy_id",
                "progress_surface",
                "resume_surface",
                "recommended_step_id",
                "next_focus",
                "remaining_gaps_count",
                "human_gate_ids",
            ],
        )
        self.assertEqual(
            overview["properties"]["progress_surface"]["$ref"],
            "#/$defs/productEntryOverviewProgressSurface",
        )
        self.assertEqual(
            overview["properties"]["resume_surface"]["$ref"],
            "#/$defs/productEntryOverviewResumeSurface",
        )

        status_schema = json.loads((SCHEMA_ROOT / "product-status.schema.json").read_text(encoding="utf-8"))
        self.assertEqual(
            status_schema["$defs"]["productStatus"]["properties"]["product_entry_overview"]["$ref"],
            "product-entry-manifest.schema.json#/$defs/productEntryOverview",
        )

    def test_grant_quality_schemas_require_issue_closure_contract(self) -> None:
        scorecard_schema = json.loads((SCHEMA_ROOT / "grant-quality-scorecard.schema.json").read_text(encoding="utf-8"))
        tracked_issue_required = scorecard_schema["$defs"]["trackedIssue"]["required"]
        self.assertIn("lineage_id", tracked_issue_required)
        self.assertIn("lineage_basis", tracked_issue_required)
        self.assertIn("closure_status", tracked_issue_required)
        self.assertIn("blocking_reason", tracked_issue_required)
        self.assertIn("evidence_obligations", tracked_issue_required)
        self.assertIn("recommended_closure_action", tracked_issue_required)
        scorecard_required = scorecard_schema["$defs"]["grantQualityScorecard"]["required"]
        self.assertIn("assessment_owner", scorecard_required)
        self.assertIn("ai_reviewer_required", scorecard_required)
        self.assertIn("review_artifact_ref", scorecard_required)
        self.assertIn("evidence_supply_queue", scorecard_required)
        supply_item_required = scorecard_schema["$defs"]["evidenceSupplyQueueItem"]["required"]
        self.assertIn("gap_id", supply_item_required)
        self.assertIn("gap_kind", supply_item_required)
        self.assertIn("controller_action_hint", supply_item_required)
        self.assertIn("required_input_ids", supply_item_required)
        self.assertIn("linked_issue_ids", supply_item_required)

        diff_schema = json.loads((SCHEMA_ROOT / "grant-quality-diff.schema.json").read_text(encoding="utf-8"))
        issue_progress_required = diff_schema["$defs"]["issueProgress"]["required"]
        self.assertIn("issue_closure_progress", issue_progress_required)
        issue_closure_required = diff_schema["$defs"]["issueClosureProgress"]["required"]
        self.assertIn("lineage_id", issue_closure_required)
        self.assertIn("lineage_basis", issue_closure_required)
        self.assertIn("previous_issue_id", issue_closure_required)
        self.assertIn("current_issue_id", issue_closure_required)
        self.assertIn("previous_summary", issue_closure_required)
        self.assertIn("current_summary", issue_closure_required)
        self.assertIn("previous_closure_status", issue_closure_required)
        self.assertIn("current_closure_status", issue_closure_required)
        self.assertIn("closure_delta", issue_closure_required)
        diff_required = diff_schema["$defs"]["grantQualityDiff"]["required"]
        self.assertIn("evidence_supply_progress", diff_required)
        supply_progress_required = diff_schema["$defs"]["evidenceSupplyProgress"]["required"]
        self.assertIn("closed_gaps", supply_progress_required)
        self.assertIn("remaining_open_gaps", supply_progress_required)
        self.assertIn("newly_opened_gaps", supply_progress_required)
        self.assertIn("gap_progress", supply_progress_required)
        gap_progress_item_required = diff_schema["$defs"]["evidenceSupplyGapProgress"]["required"]
        self.assertIn("gap_id", gap_progress_item_required)
        self.assertIn("transition", gap_progress_item_required)
        self.assertIn("supply_delta", gap_progress_item_required)
        self.assertIn("action", diff_schema["$defs"]["controllerActionHint"]["required"])

        dossier_schema = json.loads(
            (SCHEMA_ROOT / "grant-quality-closure-dossier.schema.json").read_text(encoding="utf-8")
        )
        dossier_required = dossier_schema["$defs"]["grantQualityClosureDossier"]["required"]
        self.assertIn("quality_summary", dossier_required)
        self.assertIn("unclosed_hard_issues", dossier_required)
        self.assertIn("evidence_supply_queue_summary", dossier_required)
        self.assertIn("closure_packages", dossier_required)
        quality_summary_required = dossier_schema["$defs"]["qualitySummary"]["required"]
        self.assertIn("assessment_owner", quality_summary_required)
        self.assertIn("ai_reviewer_required", quality_summary_required)
        self.assertIn("review_artifact_ref", quality_summary_required)
        closure_package_required = dossier_schema["$defs"]["closurePackage"]["required"]
        self.assertIn("closure_id", closure_package_required)
        self.assertIn("severity", closure_package_required)
        self.assertIn("target_stage", closure_package_required)
        self.assertIn("action", closure_package_required)
        self.assertIn("required_input_ids", closure_package_required)
        self.assertIn("linked_issue_ids", closure_package_required)
        self.assertIn("blocking_reasons", closure_package_required)
        self.assertIn("evidence_obligations", closure_package_required)
        self.assertIn("acceptance_signals", closure_package_required)

    def test_product_entry_surface_schemas_pin_preflight_companion_shape(self) -> None:
        manifest_schema = json.loads((SCHEMA_ROOT / "product-entry-manifest.schema.json").read_text(encoding="utf-8"))
        preflight = manifest_schema["$defs"]["productEntryPreflight"]
        self.assertEqual(preflight["properties"]["surface_kind"]["const"], "product_entry_preflight")
        self.assertEqual(
            preflight["required"],
            [
                "surface_kind",
                "summary",
                "ready_to_try_now",
                "recommended_check_command",
                "recommended_start_command",
                "blocking_check_ids",
                "checks",
            ],
        )
        self.assertEqual(
            preflight["properties"]["checks"]["items"]["$ref"],
            "#/$defs/productEntryPreflightCheck",
        )

        status_schema = json.loads((SCHEMA_ROOT / "product-status.schema.json").read_text(encoding="utf-8"))
        self.assertEqual(
            status_schema["$defs"]["productStatus"]["properties"]["product_entry_preflight"]["$ref"],
            "product-entry-manifest.schema.json#/$defs/productEntryPreflight",
        )

    def test_product_entry_surface_schemas_pin_authoring_readiness_companion_shape(self) -> None:
        manifest_schema = json.loads((SCHEMA_ROOT / "product-entry-manifest.schema.json").read_text(encoding="utf-8"))
        product_readiness = manifest_schema["$defs"]["productEntryReadiness"]
        self.assertEqual(product_readiness["properties"]["surface_kind"]["const"], "product_entry_readiness")
        self.assertEqual(
            product_readiness["properties"]["verdict"]["const"],
            "agent_assisted_ready_not_product_grade",
        )
        self.assertEqual(
            product_readiness["required"],
            [
                "surface_kind",
                "verdict",
                "usable_now",
                "good_to_use_now",
                "fully_automatic",
                "summary",
                "recommended_start_surface",
                "recommended_start_command",
                "recommended_loop_surface",
                "recommended_loop_command",
                "blocking_gaps",
            ],
        )
        readiness = manifest_schema["$defs"]["grantAuthoringReadiness"]
        self.assertEqual(readiness["properties"]["surface_kind"]["const"], "grant_authoring_readiness")
        self.assertEqual(
            readiness["properties"]["verdict"]["const"],
            "agent_assisted_cli_ready_not_full_autopilot",
        )
        self.assertEqual(
            readiness["required"],
            [
                "surface_kind",
                "verdict",
                "fully_automatic",
                "usable_now",
                "good_to_use_now",
                "user_experience_level",
                "summary",
                "recommended_start_surface",
                "recommended_start_command",
                "recommended_loop_surface",
                "recommended_loop_command",
                "workflow_coverage",
                "blocking_gaps",
            ],
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

        status_schema = json.loads((SCHEMA_ROOT / "product-status.schema.json").read_text(encoding="utf-8"))
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
