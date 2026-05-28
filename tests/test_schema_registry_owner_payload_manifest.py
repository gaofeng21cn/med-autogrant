from __future__ import annotations

import json
import unittest
from pathlib import Path


SCHEMA_ROOT = Path(__file__).resolve().parents[1] / "schemas" / "v1"


class OwnerPayloadManifestSchemaTest(unittest.TestCase):
    def test_product_entry_manifest_schema_pins_owner_payload_response_boundary(self) -> None:
        manifest_schema = json.loads(
            (SCHEMA_ROOT / "product-entry-manifest.schema.json").read_text(encoding="utf-8")
        )
        manifest = manifest_schema["$defs"]["productEntryManifest"]
        self.assertIn("owner_payload_response", manifest["required"])
        self.assertIn("workspace_receipt_scaleout_evidence", manifest["required"])
        self.assertEqual(
            manifest["properties"]["owner_payload_response"]["$ref"],
            "#/$defs/magOplOwnerPayloadResponse",
        )

        owner_payload = manifest_schema["$defs"]["magOplOwnerPayloadResponse"]
        self.assertEqual(
            owner_payload["properties"]["surface_kind"]["const"],
            "mag_opl_owner_payload_response",
        )
        self.assertEqual(
            owner_payload["properties"]["payload_path_policy"]["const"],
            "operator_must_choose_success_refs_path_or_domain_owned_typed_blocker_path_empty_template_blocks",
        )
        self.assertFalse(owner_payload["properties"]["body_included"]["const"])
        self.assertFalse(owner_payload["properties"]["grant_ready_claimed"]["const"])
        self.assertFalse(owner_payload["properties"]["quality_ready_claimed"]["const"])
        self.assertFalse(owner_payload["properties"]["export_ready_claimed"]["const"])
        self.assertFalse(owner_payload["properties"]["submission_ready_claimed"]["const"])

        authority = owner_payload["properties"]["authority_boundary"]["properties"]
        self.assertFalse(authority["opl_writes_grant_truth"]["const"])
        self.assertFalse(authority["opl_reads_memory_body"]["const"])
        self.assertFalse(authority["opl_reads_artifact_body"]["const"])
        self.assertFalse(authority["opl_authorizes_quality_or_export"]["const"])
        self.assertFalse(authority["can_declare_submission_ready"]["const"])
        self.assertFalse(authority["typed_blocker_is_submission_ready"]["const"])

        stage_summary = manifest_schema["$defs"]["magStageExpectedReceiptPayloadSummary"]
        self.assertFalse(stage_summary["properties"]["payload_body_allowed"]["const"])
        self.assertFalse(stage_summary["properties"]["success_refs_visible_is_completion"]["const"])
        self.assertFalse(stage_summary["properties"]["grant_ready_claimed"]["const"])
        self.assertFalse(stage_summary["properties"]["quality_ready_claimed"]["const"])
        self.assertFalse(stage_summary["properties"]["export_ready_claimed"]["const"])
        self.assertFalse(stage_summary["properties"]["submission_ready_claimed"]["const"])

        manifest_consumer = manifest_schema["$defs"]["magManifestOwnerPayloadConsumerEvidence"]
        self.assertEqual(
            manifest_consumer["properties"]["surface_kind"]["const"],
            "mag_manifest_owner_payload_consumer_evidence",
        )
        self.assertEqual(
            manifest_consumer["properties"]["consumer"]["const"],
            "one_person_lab_app_operator_manifest",
        )
        self.assertEqual(
            manifest_consumer["properties"]["projection_policy"]["const"],
            "default_manifest_consumer_reads_owner_payload_refs_and_count_only_scaleout_without_submitting_operator_payload_or_claiming_ready",
        )
        self.assertFalse(manifest_consumer["properties"]["operator_payload_submitted"]["const"])
        self.assertFalse(
            manifest_consumer["properties"]["count_only_scaleout_snapshot_is_receipt_refs"][
                "const"
            ]
        )
        self.assertFalse(
            manifest_consumer["properties"]["claims_sustained_app_consumption_complete"][
                "const"
            ]
        )
        self.assertFalse(manifest_consumer["properties"]["claims_submission_ready"]["const"])
        workorder = manifest_consumer["properties"]["sustained_consumption_followthrough_workorder"]
        self.assertEqual(
            workorder["properties"]["surface_kind"]["const"],
            "mag_manifest_sustained_consumption_followthrough_workorder",
        )
        self.assertEqual(
            workorder["properties"]["payload_owner"]["const"],
            "app_operator_or_release_default_caller",
        )
        self.assertFalse(workorder["properties"]["empty_payload_template_is_success_evidence"]["const"])
        self.assertFalse(workorder["properties"]["claims_sustained_app_consumption_complete"]["const"])
        self.assertFalse(workorder["properties"]["claims_provider_long_soak_complete"]["const"])
        workorder_authority = workorder["properties"]["authority_boundary"]["properties"]
        self.assertFalse(workorder_authority["can_create_owner_receipt"]["const"])
        self.assertFalse(
            workorder_authority["can_declare_app_sustained_consumption_complete"]["const"]
        )
        consumer_authority = manifest_consumer["properties"]["authority_boundary"]["properties"]
        self.assertFalse(consumer_authority["can_create_owner_receipt"]["const"])
        self.assertFalse(consumer_authority["can_submit_operator_payload"]["const"])
        self.assertFalse(
            consumer_authority["can_declare_app_sustained_consumption_complete"]["const"]
        )
        self.assertFalse(consumer_authority["can_declare_submission_ready"]["const"])

        scaleout = manifest_schema["$defs"]["magWorkspaceReceiptScaleoutEvidence"]
        claims = scaleout["properties"]["claims"]["properties"]
        self.assertFalse(claims["claims_grant_ready"]["const"])
        self.assertFalse(claims["claims_submission_ready_export"]["const"])
        self.assertFalse(
            scaleout["properties"]["authority_boundary"]["properties"][
                "can_declare_submission_ready"
            ]["const"]
        )


if __name__ == "__main__":
    unittest.main()
