from __future__ import annotations

import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_ROOT = REPO_ROOT / "schemas" / "v1"


class CloseoutSchemaRegistryTest(unittest.TestCase):
    def test_closeout_surface_schemas_pin_authority_boundaries(self) -> None:
        codex_schema = json.loads(
            (SCHEMA_ROOT / "codex-stage-execution-receipt-bundle.schema.json").read_text(encoding="utf-8")
        )
        codex_boundary = codex_schema["$defs"]["authorityBoundary"]["properties"]
        self.assertEqual(codex_boundary["projection_scope"]["const"], "codex_stage_execution_and_review_receipt_refs_only")
        self.assertFalse(codex_boundary["mag_implements_opl_runtime"]["const"])
        self.assertFalse(codex_boundary["mag_implements_app_workbench"]["const"])
        self.assertFalse(codex_boundary["execution_receipt_refs_equal_quality_ready"]["const"])
        self.assertFalse(codex_boundary["review_receipt_refs_equal_quality_ready"]["const"])
        self.assertFalse(codex_boundary["can_declare_fundability_ready"]["const"])
        self.assertFalse(codex_boundary["can_declare_quality_ready"]["const"])
        self.assertFalse(codex_boundary["can_declare_export_ready"]["const"])
        self.assertFalse(codex_boundary["can_declare_submission_ready"]["const"])

        operator_schema = json.loads(
            (SCHEMA_ROOT / "operator-closeout-readiness-projection.schema.json").read_text(encoding="utf-8")
        )
        operator_boundary = operator_schema["$defs"]["authorityBoundary"]["properties"]
        self.assertEqual(operator_boundary["projection_scope"]["const"], "operator_closeout_readiness_only")
        self.assertFalse(operator_boundary["request_accounting_closure_equals_real_evidence"]["const"])
        self.assertFalse(operator_boundary["receipt_refs_ready_equals_quality_ready"]["const"])
        self.assertFalse(operator_boundary["production_tail_closure_equals_grant_ready"]["const"])
        self.assertFalse(operator_boundary["can_declare_fundability_ready"]["const"])
        self.assertFalse(operator_boundary["can_declare_quality_ready"]["const"])
        self.assertFalse(operator_boundary["can_declare_export_ready"]["const"])
        self.assertFalse(operator_boundary["can_declare_submission_ready"]["const"])

        physical_schema = json.loads(
            (SCHEMA_ROOT / "physical-morphology-guard-projection.schema.json").read_text(encoding="utf-8")
        )
        physical_boundary = physical_schema["$defs"]["authorityBoundary"]["properties"]
        self.assertEqual(physical_boundary["projection_scope"]["const"], "source_path_module_role_evidence_refs_only")
        self.assertEqual(physical_boundary["mag_role"]["const"], "physical_morphology_read_guard_projection")
        self.assertFalse(physical_boundary["mag_implements_opl_runtime"]["const"])
        self.assertFalse(physical_boundary["mag_implements_scheduler_daemon"]["const"])
        self.assertFalse(physical_boundary["mag_implements_attempt_ledger"]["const"])
        self.assertFalse(physical_boundary["mag_implements_local_journal"]["const"])
        self.assertFalse(physical_boundary["mag_implements_app_workbench"]["const"])
        self.assertFalse(physical_boundary["mag_restores_compatibility_alias"]["const"])

        closeout_schema = json.loads(
            (SCHEMA_ROOT / "executor-first-closeout-bundle.schema.json").read_text(encoding="utf-8")
        )
        closeout_boundary = closeout_schema["$defs"]["authorityBoundary"]["properties"]
        self.assertFalse(closeout_boundary["bundle_can_declare_fundability_ready"]["const"])
        self.assertFalse(closeout_boundary["bundle_can_declare_quality_ready"]["const"])
        self.assertFalse(closeout_boundary["bundle_can_declare_export_ready"]["const"])
        self.assertFalse(closeout_boundary["bundle_can_declare_submission_ready"]["const"])
        self.assertFalse(closeout_boundary["receipt_refs_equal_ready_verdict"]["const"])
        self.assertFalse(closeout_boundary["physical_guard_pass_equals_runtime_cleanup_complete"]["const"])

    def test_closeout_surface_schemas_require_expected_surface_shapes(self) -> None:
        expected_defs = {
            "codex-stage-execution-receipt-bundle.schema.json": "codexStageExecutionReceiptBundle",
            "operator-closeout-readiness-projection.schema.json": "operatorCloseoutReadinessProjection",
            "physical-morphology-guard-projection.schema.json": "physicalMorphologyGuardProjection",
            "executor-first-closeout-bundle.schema.json": "executorFirstCloseoutBundle",
        }

        for schema_file, def_name in expected_defs.items():
            with self.subTest(schema=schema_file):
                payload = json.loads((SCHEMA_ROOT / schema_file).read_text(encoding="utf-8"))
                surface = payload["$defs"][def_name]
                required = surface["required"]
                self.assertIn("surface_kind", required)
                self.assertIn("version", required)
                self.assertIn("target_domain_id", required)
                self.assertIn("owner", required)
                self.assertIn("authority_boundary", required)
                self.assertEqual(surface["properties"]["version"]["const"], "v1")
                self.assertEqual(surface["properties"]["target_domain_id"]["const"], "med-autogrant")
                self.assertEqual(surface["properties"]["owner"]["const"], "med-autogrant")
