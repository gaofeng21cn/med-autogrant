from __future__ import annotations

import json
import unittest
from pathlib import Path


SCHEMA_ROOT = Path(__file__).resolve().parents[1] / "schemas" / "v1"


class ConsumerThinningSchemaRegistryTest(unittest.TestCase):
    def test_output_guard_schema_pins_external_evidence_request_ref(self) -> None:
        manifest_schema = json.loads((SCHEMA_ROOT / "product-entry-manifest.schema.json").read_text(encoding="utf-8"))
        thinning = manifest_schema["$defs"]["magConsumerThinningContract"]
        output_guard = thinning["properties"]["thin_surface_output_guard"]
        evidence_request_ref = (
            "/product_entry_manifest/mag_consumer_thinning_contract/external_evidence_request_pack"
        )

        self.assertIn(
            "private_functional_state_output_classes_forbidden",
            output_guard["required"],
        )
        guard_required_refs = output_guard["properties"]["required_sidecar_return_refs"]
        self.assertIn("external_evidence_request_pack_ref", guard_required_refs["required"])
        self.assertEqual(
            guard_required_refs["properties"]["external_evidence_request_pack_ref"]["const"],
            evidence_request_ref,
        )
        self.assertEqual(
            output_guard["properties"]["private_functional_state_output_classes_forbidden"]["const"],
            [
                "local_runtime_journal_state",
                "local_attempt_ledger_state",
                "attention_queue_state",
                "stage_attempt_ledger_state",
                "package_lifecycle_state",
                "source_intake_state",
                "operator_workbench_state",
                "scheduler_daemon_state",
                "hermes_state_db_runtime_state",
            ],
        )
        forbidden_output_classes = output_guard["properties"]["forbidden_output_classes"]["allOf"]
        forbidden_consts = {entry["contains"]["const"] for entry in forbidden_output_classes}
        self.assertIn("functional_harness_runtime_state", forbidden_consts)
        self.assertIn("opl_harness_pass_grant_ready", forbidden_consts)
        self.assertIn("opl_harness_pass_export_ready", forbidden_consts)
        self.assertIn("local_attempt_ledger_state", forbidden_consts)
        self.assertIn("package_lifecycle_state", forbidden_consts)
        self.assertIn("source_intake_state", forbidden_consts)
        self.assertIn("hermes_state_db_runtime_state", forbidden_consts)
        guard_authority = output_guard["properties"]["authority_boundary"]
        self.assertIn("mag_can_emit_private_functional_state", guard_authority["required"])
        self.assertFalse(
            guard_authority["properties"]["mag_can_emit_private_functional_state"]["const"]
        )
        self.assertFalse(
            guard_authority["properties"]["mag_can_emit_local_attempt_ledger_state"]["const"]
        )
        self.assertFalse(
            guard_authority["properties"]["mag_can_emit_source_intake_state"]["const"]
        )
        self.assertFalse(
            guard_authority["properties"]["mag_can_emit_package_lifecycle_state"]["const"]
        )
        self.assertFalse(
            guard_authority["properties"]["mag_can_emit_hermes_state_db_runtime_state"]["const"]
        )
        authority = thinning["properties"]["authority_boundary"]["properties"]
        self.assertFalse(authority["opl_harness_pass_can_declare_grant_ready"]["const"])
        self.assertFalse(authority["opl_harness_pass_can_declare_export_ready"]["const"])

    def test_external_evidence_request_pack_schema_stays_request_only(self) -> None:
        manifest_schema = json.loads((SCHEMA_ROOT / "product-entry-manifest.schema.json").read_text(encoding="utf-8"))
        thinning = manifest_schema["$defs"]["magConsumerThinningContract"]
        evidence_pack = thinning["properties"]["external_evidence_request_pack"]

        self.assertIn("external_evidence_request_pack", thinning["required"])
        self.assertEqual(
            evidence_pack["properties"]["surface_kind"]["const"],
            "mag_external_evidence_request_pack",
        )
        self.assertEqual(
            evidence_pack["properties"]["request_pack_id"]["const"],
            "mag.external_evidence_request_pack.v1",
        )
        self.assertEqual(
            evidence_pack["properties"]["state"]["const"],
            "request_pack_declared_external_evidence_not_claimed",
        )
        self.assertEqual(
            evidence_pack["properties"]["policy"]["const"],
            "request_refs_receipt_shapes_and_parity_only_no_runtime_implementation",
        )
        self.assertEqual(
            evidence_pack["properties"]["required_request_ids"]["const"],
            [
                "opl_generated_hosted_caller_pack_consumption",
                "app_workbench_package_ref_consumption",
                "production_default_caller_release_dist_consumption",
                "owner_receipt_typed_blocker_ref_roundtrip",
                "continuous_no_forbidden_write_guard",
                "direct_hosted_parity_no_regression",
                "temporal_provider_long_soak_receipt_reconciliation",
            ],
        )
        request_item = evidence_pack["properties"]["requests"]["items"]
        self.assertEqual(request_item["properties"]["state"]["const"], "requested_not_received")
        self.assertEqual(
            request_item["properties"]["mag_role"]["const"],
            "requester_and_contract_owner_only",
        )
        self.assertTrue(
            request_item["properties"]["evidence_not_claimed_by_mag_repo"]["const"]
        )
        forbidden_payload_classes = request_item["properties"]["forbidden_payload_classes"]["allOf"]
        forbidden_payload_consts = {entry["contains"]["const"] for entry in forbidden_payload_classes}
        self.assertIn("memory_body", forbidden_payload_consts)
        self.assertIn("opl_runtime_state_body", forbidden_payload_consts)
        self.assertIn("app_workbench_state_body", forbidden_payload_consts)
        forbidden_claims = evidence_pack["properties"]["forbidden_completion_claims"]["properties"]
        self.assertFalse(forbidden_claims["provider_completion_is_fundability_ready"]["const"])
        self.assertFalse(forbidden_claims["provider_completion_is_quality_ready"]["const"])
        self.assertFalse(forbidden_claims["provider_completion_is_export_ready"]["const"])
        self.assertFalse(forbidden_claims["claims_opl_replacement_exists"]["const"])
        self.assertFalse(forbidden_claims["claims_all_bridge_exits_complete"]["const"])
        self.assertFalse(forbidden_claims["claims_production_long_run_soak_complete"]["const"])
        evidence_authority = evidence_pack["properties"]["authority_boundary"]["properties"]
        self.assertTrue(evidence_authority["mag_request_pack_only"]["const"])
        self.assertFalse(evidence_authority["mag_implements_opl_runtime"]["const"])
        self.assertFalse(evidence_authority["mag_implements_app_workbench"]["const"])
        self.assertFalse(evidence_authority["mag_claims_external_evidence_exists"]["const"])
        self.assertFalse(evidence_authority["mag_claims_direct_hosted_parity_passed"]["const"])
        self.assertFalse(evidence_authority["mag_claims_long_soak_complete"]["const"])
        self.assertFalse(evidence_authority["opl_can_declare_fundability_verdict"]["const"])
        self.assertFalse(evidence_authority["opl_can_declare_quality_verdict"]["const"])
        self.assertFalse(evidence_authority["opl_can_declare_export_verdict"]["const"])

    def test_minimal_authority_surface_schema_requires_ai_first_boundary_fields(self) -> None:
        manifest_schema = json.loads((SCHEMA_ROOT / "product-entry-manifest.schema.json").read_text(encoding="utf-8"))
        thinning = manifest_schema["$defs"]["magConsumerThinningContract"]
        self.assertEqual(
            thinning["properties"]["minimal_authority_functions"]["$ref"],
            "#/$defs/ownerReceiptContract/properties/minimal_authority_functions",
        )
        self.assertEqual(
            thinning["properties"]["minimal_authority_surface_taxonomy"]["$ref"],
            "#/$defs/ownerReceiptContract/properties/minimal_authority_surface_taxonomy",
        )
        authority_item = manifest_schema["$defs"]["ownerReceiptContract"]["properties"][
            "minimal_authority_functions"
        ]["items"]
        required = set(authority_item["required"])

        for field in {
            "surface_kind",
            "authority_surface_id",
            "work_mode",
            "judgment_owner",
            "programmatic_role",
            "ai_stage_artifact_required",
            "mechanical_decision_forbidden",
            "programmatic_verdict_generation_allowed",
            "forbidden_decision_sources",
            "decision_boundary",
        }:
            self.assertIn(field, required)
        self.assertEqual(
            authority_item["properties"]["surface_kind"]["const"],
            "mag_minimal_authority_surface",
        )
        self.assertEqual(
            authority_item["properties"]["mechanical_decision_forbidden"]["const"],
            True,
        )
        self.assertEqual(
            authority_item["properties"]["programmatic_verdict_generation_allowed"]["const"],
            False,
        )
        self.assertEqual(
            authority_item["properties"]["decision_boundary"]["properties"][
                "programmatic_role_may_compute_ready_verdict"
            ]["const"],
            False,
        )
        taxonomy = manifest_schema["$defs"]["ownerReceiptContract"]["properties"][
            "minimal_authority_surface_taxonomy"
        ]
        self.assertEqual(
            taxonomy["properties"]["mechanical_decision_forbidden_for_all_surfaces"]["const"],
            True,
        )
        self.assertEqual(
            taxonomy["properties"]["programmatic_verdict_generation_allowed"]["const"],
            False,
        )
