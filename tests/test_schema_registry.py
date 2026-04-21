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
    "service-safe-domain-surface.schema.json",
    "pending-handoff-requirements.schema.json",
    "executor-routing-contract.schema.json",
    "product-entry.schema.json",
    "grant-progress.schema.json",
    "grant-cockpit.schema.json",
    "grant-direct-entry.schema.json",
    "grant-user-loop.schema.json",
    "product-entry-manifest.schema.json",
    "product-frontdesk.schema.json",
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
        self.assertEqual(names["grant_progress_projection"], "grant-progress.schema.json")
        self.assertEqual(names["grant_cockpit_projection"], "grant-cockpit.schema.json")
        self.assertEqual(names["grant_direct_entry_surface"], "grant-direct-entry.schema.json")
        self.assertEqual(names["grant_user_loop_surface"], "grant-user-loop.schema.json")
        self.assertEqual(names["product_entry_manifest_surface"], "product-entry-manifest.schema.json")
        self.assertEqual(names["product_frontdesk_surface"], "product-frontdesk.schema.json")
        self.assertEqual(names["hosted_contract_bundle"], "hosted-contract-bundle.schema.json")
        self.assertEqual(names["submission_ready_package"], "submission-ready-package.schema.json")

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

    def test_frontdoor_surface_schemas_require_quickstart_companion(self) -> None:
        manifest_schema = json.loads((SCHEMA_ROOT / "product-entry-manifest.schema.json").read_text(encoding="utf-8"))
        manifest_required = manifest_schema["$defs"]["productEntryManifest"]["required"]
        self.assertIn("managed_runtime_contract", manifest_required)
        self.assertIn("runtime_inventory", manifest_required)
        self.assertIn("task_lifecycle", manifest_required)
        self.assertIn("skill_catalog", manifest_required)
        self.assertIn("automation", manifest_required)
        self.assertIn("family_orchestration", manifest_required)
        self.assertIn("product_entry_start", manifest_required)
        self.assertIn("product_entry_overview", manifest_required)
        self.assertIn("product_entry_preflight", manifest_required)
        self.assertIn("product_entry_readiness", manifest_required)
        self.assertIn("grant_authoring_readiness", manifest_required)
        self.assertIn("product_entry_quickstart", manifest_required)

        frontdesk_schema = json.loads((SCHEMA_ROOT / "product-frontdesk.schema.json").read_text(encoding="utf-8"))
        frontdesk_required = frontdesk_schema["$defs"]["productFrontdesk"]["required"]
        self.assertIn("family_orchestration", frontdesk_required)
        self.assertIn("product_entry_start", frontdesk_required)
        self.assertIn("product_entry_overview", frontdesk_required)
        self.assertIn("product_entry_preflight", frontdesk_required)
        self.assertIn("product_entry_readiness", frontdesk_required)
        self.assertIn("grant_authoring_readiness", frontdesk_required)
        self.assertIn("product_entry_quickstart", frontdesk_required)

    def test_frontdoor_surface_schemas_pin_managed_runtime_contract_shape(self) -> None:
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
            "contracts/opl-gateway/managed-runtime-three-layer-contract.json",
        )
        self.assertEqual(managed_runtime["properties"]["runtime_owner"]["const"], "upstream_hermes_agent")
        self.assertEqual(managed_runtime["properties"]["domain_owner"]["const"], "med-autogrant")
        self.assertEqual(managed_runtime["properties"]["executor_owner"]["const"], "med-autogrant")

    def test_frontdoor_surface_schemas_pin_start_companion_shape(self) -> None:
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

        frontdesk_schema = json.loads((SCHEMA_ROOT / "product-frontdesk.schema.json").read_text(encoding="utf-8"))
        self.assertEqual(
            frontdesk_schema["$defs"]["productFrontdesk"]["properties"]["product_entry_start"]["$ref"],
            "product-entry-manifest.schema.json#/$defs/productEntryStart",
        )

    def test_frontdoor_surface_schemas_pin_overview_companion_shape(self) -> None:
        manifest_schema = json.loads((SCHEMA_ROOT / "product-entry-manifest.schema.json").read_text(encoding="utf-8"))
        overview = manifest_schema["$defs"]["productEntryOverview"]
        self.assertEqual(overview["properties"]["surface_kind"]["const"], "product_entry_overview")
        self.assertEqual(
            overview["required"],
            [
                "surface_kind",
                "summary",
                "frontdesk_command",
                "recommended_command",
                "operator_loop_command",
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

        frontdesk_schema = json.loads((SCHEMA_ROOT / "product-frontdesk.schema.json").read_text(encoding="utf-8"))
        self.assertEqual(
            frontdesk_schema["$defs"]["productFrontdesk"]["properties"]["product_entry_overview"]["$ref"],
            "product-entry-manifest.schema.json#/$defs/productEntryOverview",
        )

    def test_frontdoor_surface_schemas_pin_preflight_companion_shape(self) -> None:
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

        frontdesk_schema = json.loads((SCHEMA_ROOT / "product-frontdesk.schema.json").read_text(encoding="utf-8"))
        self.assertEqual(
            frontdesk_schema["$defs"]["productFrontdesk"]["properties"]["product_entry_preflight"]["$ref"],
            "product-entry-manifest.schema.json#/$defs/productEntryPreflight",
        )

    def test_frontdoor_surface_schemas_pin_authoring_readiness_companion_shape(self) -> None:
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

        frontdesk_schema = json.loads((SCHEMA_ROOT / "product-frontdesk.schema.json").read_text(encoding="utf-8"))
        self.assertEqual(
            frontdesk_schema["$defs"]["productFrontdesk"]["properties"]["product_entry_readiness"]["$ref"],
            "product-entry-manifest.schema.json#/$defs/productEntryReadiness",
        )
        self.assertEqual(
            frontdesk_schema["$defs"]["productFrontdesk"]["properties"]["grant_authoring_readiness"]["$ref"],
            "product-entry-manifest.schema.json#/$defs/grantAuthoringReadiness",
        )


if __name__ == "__main__":
    unittest.main()
