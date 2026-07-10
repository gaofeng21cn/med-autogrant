from __future__ import annotations

import json
from pathlib import Path


SCHEMA_ROOT = Path(__file__).resolve().parents[1] / "schemas" / "v1"


def test_closeout_schemas_keep_shape_and_non_authority_boundary() -> None:
    cases: tuple[tuple[str, str, dict[str, object], set[str]], ...] = (
        (
            "codex-stage-execution-receipt-bundle.schema.json",
            "codexStageExecutionReceiptBundle",
            {
                "projection_scope": "codex_stage_execution_and_review_receipt_refs_only",
                "codex_cli_is_default_executor": True,
            },
            {
                "mag_implements_opl_runtime",
                "mag_implements_app_workbench",
                "can_write_grant_truth_body",
                "can_write_memory_body",
                "execution_receipt_refs_equal_quality_ready",
                "review_receipt_refs_equal_quality_ready",
                "can_declare_fundability_ready",
                "can_declare_quality_ready",
                "can_declare_export_ready",
                "can_declare_submission_ready",
            },
        ),
        (
            "operator-closeout-readiness-projection.schema.json",
            "operatorCloseoutReadinessProjection",
            {"projection_scope": "operator_closeout_readiness_only"},
            {
                "mag_implements_opl_runtime",
                "mag_implements_app_workbench",
                "request_accounting_closure_equals_real_evidence",
                "receipt_refs_ready_equals_quality_ready",
                "production_tail_closure_equals_grant_ready",
                "can_declare_fundability_ready",
                "can_declare_quality_ready",
                "can_declare_export_ready",
                "can_declare_submission_ready",
            },
        ),
        (
            "physical-morphology-guard-projection.schema.json",
            "physicalMorphologyGuardProjection",
            {
                "projection_scope": "source_path_module_role_evidence_refs_only",
                "mag_role": "physical_morphology_read_guard_projection",
            },
            {
                "mag_implements_opl_runtime",
                "mag_implements_scheduler_daemon",
                "mag_implements_attempt_ledger",
                "mag_implements_local_journal",
                "mag_implements_app_workbench",
                "mag_restores_compatibility_alias",
                "can_declare_physical_cleanup_complete",
            },
        ),
        (
            "executor-first-closeout-bundle.schema.json",
            "executorFirstCloseoutBundle",
            {
                "mag_owns_grant_truth": True,
                "mag_owns_quality_verdict": True,
                "mag_owns_export_verdict": True,
                "mag_owns_package_authority": True,
                "mag_owns_owner_receipt_authority": True,
                "opl_owns_generic_runtime": True,
                "opl_owns_operator_workbench": True,
            },
            {
                "bundle_can_declare_fundability_ready",
                "bundle_can_declare_quality_ready",
                "bundle_can_declare_export_ready",
                "bundle_can_declare_submission_ready",
                "receipt_refs_equal_ready_verdict",
                "physical_guard_pass_equals_runtime_cleanup_complete",
            },
        ),
    )

    for schema_name, definition, expected_consts, false_fields in cases:
        schema = json.loads((SCHEMA_ROOT / schema_name).read_text(encoding="utf-8"))
        surface = schema["$defs"][definition]
        boundary = schema["$defs"]["authorityBoundary"]["properties"]
        assert {"surface_kind", "version", "target_domain_id", "owner", "authority_boundary"} <= set(surface["required"])
        assert surface["properties"]["version"]["const"] == "v1"
        assert surface["properties"]["target_domain_id"]["const"] == "med-autogrant"
        assert surface["properties"]["owner"]["const"] == "med-autogrant"
        assert {field for field, spec in boundary.items() if spec.get("const") is False} == false_fields
        assert {
            field: spec["const"]
            for field, spec in boundary.items()
            if "const" in spec and spec["const"] is not False
        } == expected_consts
