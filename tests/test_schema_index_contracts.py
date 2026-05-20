from __future__ import annotations

import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_ROOT = REPO_ROOT / "schemas" / "v1"


class SchemaIndexContractTest(unittest.TestCase):
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
        self.assertEqual(
            names["codex_stage_execution_receipt_bundle"],
            "codex-stage-execution-receipt-bundle.schema.json",
        )
        self.assertEqual(
            names["operator_closeout_readiness_projection"],
            "operator-closeout-readiness-projection.schema.json",
        )
        self.assertEqual(
            names["physical_morphology_guard_projection"],
            "physical-morphology-guard-projection.schema.json",
        )
        self.assertEqual(
            names["executor_first_closeout_bundle"],
            "executor-first-closeout-bundle.schema.json",
        )
