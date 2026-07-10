from __future__ import annotations

import json
from pathlib import Path


SCHEMA_ROOT = Path(__file__).resolve().parents[1] / "schemas" / "v1"


def test_closeout_schemas_keep_shape_and_non_authority_boundary() -> None:
    cases = (
        (
            "codex-stage-execution-receipt-bundle.schema.json",
            "codexStageExecutionReceiptBundle",
            "codex_stage_execution_and_review_receipt_refs_only",
            ("can_declare_fundability_ready", "can_declare_quality_ready", "can_declare_export_ready", "can_declare_submission_ready"),
        ),
        (
            "operator-closeout-readiness-projection.schema.json",
            "operatorCloseoutReadinessProjection",
            "operator_closeout_readiness_only",
            ("request_accounting_closure_equals_real_evidence", "receipt_refs_ready_equals_quality_ready", "can_declare_submission_ready"),
        ),
        (
            "physical-morphology-guard-projection.schema.json",
            "physicalMorphologyGuardProjection",
            "source_path_module_role_evidence_refs_only",
            ("mag_implements_opl_runtime", "mag_implements_scheduler_daemon", "mag_implements_attempt_ledger", "mag_restores_compatibility_alias"),
        ),
        (
            "executor-first-closeout-bundle.schema.json",
            "executorFirstCloseoutBundle",
            None,
            ("bundle_can_declare_fundability_ready", "bundle_can_declare_quality_ready", "bundle_can_declare_export_ready", "bundle_can_declare_submission_ready"),
        ),
    )

    for schema_name, definition, scope, false_fields in cases:
        schema = json.loads((SCHEMA_ROOT / schema_name).read_text(encoding="utf-8"))
        surface = schema["$defs"][definition]
        boundary = schema["$defs"]["authorityBoundary"]["properties"]
        assert {"surface_kind", "version", "target_domain_id", "owner", "authority_boundary"} <= set(surface["required"])
        assert surface["properties"]["version"]["const"] == "v1"
        assert surface["properties"]["target_domain_id"]["const"] == "med-autogrant"
        assert surface["properties"]["owner"]["const"] == "med-autogrant"
        if scope is not None:
            assert boundary["projection_scope"]["const"] == scope
        assert all(boundary[field]["const"] is False for field in false_fields)
