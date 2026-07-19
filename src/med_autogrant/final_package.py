from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from med_autogrant.domain_runtime_parts.io import (
    _guard_final_package_output_identity,
    _read_artifact_bundle,
    _write_final_package_output,
)
from med_autogrant.route_report import build_stage_route_report
from med_autogrant.workspace_projection_parts import _require_workspace_context


FINAL_PACKAGE_VERSION = 1
FINAL_PACKAGE_KIND = "final_package"
ALLOWED_CHECKPOINT_STATUSES = {"freeze_ready", "submission_frozen"}


def build_final_package_document(
    *,
    document: dict[str, Any],
    artifact_bundle: dict[str, Any],
) -> dict[str, Any]:
    context = _require_workspace_context(document)
    active_draft = context.active_draft
    active_revision_plan = context.active_revision_plan
    active_critique = context.active_critique
    route_report = build_stage_route_report(document)
    verification_checkpoint = route_report["verification_checkpoint"]
    checkpoint_status = verification_checkpoint["checkpoint_status"]
    draft_status = active_draft.get("status")
    quality_debt_reasons = [
        *(
            [f"checkpoint_status_not_final:{checkpoint_status}"]
            if checkpoint_status not in ALLOWED_CHECKPOINT_STATUSES
            else []
        ),
        *(
            [f"active_draft_not_revised_or_frozen:{draft_status}"]
            if draft_status not in {"revised", "frozen"}
            else []
        ),
    ]

    return {
        "package_version": FINAL_PACKAGE_VERSION,
        "package_kind": FINAL_PACKAGE_KIND,
        "grant_run_id": document["grant_run_id"],
        "workspace_id": document["workspace_id"],
        "draft_id": active_draft["draft_id"],
        "lifecycle_stage": document["lifecycle_stage"],
        "status": (
            "completed_with_quality_debt"
            if quality_debt_reasons
            else "completed"
        ),
        "quality_debt": (
            {
                "status": "recorded_non_blocking",
                "reasons": quality_debt_reasons,
                "blocks_stage_transition": False,
                "blocks_submission_ready_claim": True,
                "next_stage_may_start": True,
                "semantic_route_owner": "decisive_codex_attempt",
            }
            if quality_debt_reasons
            else None
        ),
        "freeze_manifest": {
            "draft_version_label": active_draft["version_label"],
            "draft_status": draft_status,
            "active_revision_plan_id": active_revision_plan["revision_plan_id"],
            "critique_id": active_critique["critique_id"],
            "checkpoint_status": checkpoint_status,
            "presubmission_frozen": bool(document.get("gates", {}).get("presubmission_frozen")),
        },
        "lineage": {
            "frozen_question_id": active_draft["frozen_question_id"],
            "selected_direction_id": context.selected_direction["direction_id"],
            "selected_question_id": context.selected_question["question_id"],
            "active_fit_mapping_id": context.active_fit_mapping["fit_mapping_id"],
            "draft_id": active_draft["draft_id"],
            "revision_plan_id": active_revision_plan["revision_plan_id"],
        },
        "checkpoint_summary": {
            "verification_checkpoint": verification_checkpoint,
            "checkpoint_status": checkpoint_status,
        },
        "export_summary": {
            "outline_count": len(active_draft.get("outline", [])),
            "section_count": len(active_draft.get("sections", [])),
            "artifact_count": len(artifact_bundle["artifacts"]),
        },
        "deliverables": {
            "artifact_bundle_manifest": deepcopy(artifact_bundle["manifest"]),
            "final_draft_outline": deepcopy(active_draft.get("outline", [])),
            "final_draft_sections": deepcopy(active_draft.get("sections", [])),
        },
    }

def build_final_package_payload(
    document: dict[str, Any],
    *,
    artifact_bundle_path: str | Path,
    output_path: str | Path,
) -> dict[str, Any]:
    context = _require_workspace_context(document)
    active_draft = context.active_draft
    artifact_bundle = _read_artifact_bundle(
        artifact_bundle_path=artifact_bundle_path,
        grant_run_id=document["grant_run_id"],
        workspace_id=document["workspace_id"],
        draft_id=active_draft["draft_id"],
        lifecycle_stage=document.get("lifecycle_stage"),
    )
    final_package = build_final_package_document(
        document=document,
        artifact_bundle=artifact_bundle,
    )
    resolved_output_path = Path(output_path).expanduser().resolve()
    _guard_final_package_output_identity(
        resolved_output_path,
        grant_run_id=final_package["grant_run_id"],
        workspace_id=final_package["workspace_id"],
        draft_id=final_package["draft_id"],
        lifecycle_stage=final_package["lifecycle_stage"],
    )
    _write_final_package_output(resolved_output_path, final_package)
    return {
        "ok": True,
        "command": "build-final-package",
        "grant_run_id": final_package["grant_run_id"],
        "workspace_id": final_package["workspace_id"],
        "draft_id": final_package["draft_id"],
        "lifecycle_stage": final_package["lifecycle_stage"],
        "output_path": str(resolved_output_path),
        "final_package": final_package,
    }
