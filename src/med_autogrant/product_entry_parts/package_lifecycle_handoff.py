from __future__ import annotations

from typing import Any, Mapping

from med_autogrant.product_entry_parts.primitives import TARGET_DOMAIN_ID, _require_nonempty_string
from med_autogrant.submission_ready import (
    SubmissionReadyExportVerdictError,
    normalize_submission_ready_export_verdict,
)
from med_autogrant.workspace_types import WorkspaceStateError


PACKAGE_LIFECYCLE_HANDOFF_PROJECTION_KIND = "mag_package_lifecycle_handoff_projection"
PACKAGE_STAGE_ID = "package_and_submit_ready"
STAGE_OUTPUT_ARTIFACT_LIFECYCLE_ROLE = "stage_output_artifact_ref"
PACKAGE_STAGE_OUTPUT_ROLE = "submission_ready_package_manifest_ref"
FINAL_PACKAGE_LIFECYCLE_ROLE = "canonical_promotion_ref"
SUBMISSION_READY_PACKAGE_LIFECYCLE_ROLE = "export_artifact_ref"
PACKAGE_LIFECYCLE_HANDOFF_POLICY = "refs_manifest_missing_output_receipt_blocker_handoff_only"
REQUIRED_STAGE_FOLDER_PACKAGE_REF_KEYS = (
    "artifact_bundle_ref",
    "final_package_ref",
    "submission_ready_package_ref",
)

_FORBIDDEN_BODY_KEY_PARTS = (
    ("artifact", "body"),
    ("artifact", "content"),
    ("artifact", "payload"),
    ("evidence", "body"),
    ("grant", "artifact"),
    ("grant", "body"),
    ("package", "body"),
    ("package", "content"),
    ("package", "payload"),
    ("private", "evidence"),
)
_OPL_EXPORT_READY_CLAIM_KEYS = {
    "opl_can_declare_export_ready",
    "opl_can_declare_submission_ready_export",
    "opl_can_issue_export_verdict",
    "opl_declares_export_ready",
    "opl_holds_export_verdict",
    "opl_submission_ready_export",
}
_OPL_ARTIFACT_WRITE_KEYS = {
    "opl_can_write_artifact_body",
    "opl_can_write_package_body",
    "opl_writes_artifact_body",
    "opl_writes_package_body",
    "opl_writes_package_artifact",
}


def build_package_lifecycle_handoff_projection(
    *,
    package_refs: Mapping[str, Any],
    gap_report: Mapping[str, Any],
    export_verdict: Mapping[str, Any],
    manual_portal_boundary: Mapping[str, Any],
    lifecycle_receipt_refs: Mapping[str, Any],
) -> dict[str, Any]:
    payloads = (
        ("package_refs", package_refs),
        ("gap_report", gap_report),
        ("export_verdict", export_verdict),
        ("manual_portal_boundary", manual_portal_boundary),
        ("lifecycle_receipt_refs", lifecycle_receipt_refs),
    )
    for context, payload in payloads:
        _require_mapping_payload(payload, context=context)
        _reject_forbidden_payload(payload, context=context)

    projected_package_refs = _read_ref_mapping(package_refs, context="package_refs")
    projected_receipt_refs = _read_ref_mapping(lifecycle_receipt_refs, context="lifecycle_receipt_refs")

    return {
        "surface_kind": PACKAGE_LIFECYCLE_HANDOFF_PROJECTION_KIND,
        "version": "v1",
        "state": "refs_ready_for_opl_artifact_package_lifecycle_shell",
        "owner": TARGET_DOMAIN_ID,
        "target_domain_id": TARGET_DOMAIN_ID,
        "package_refs": projected_package_refs,
        "stage_folder_lifecycle_projection": _stage_folder_lifecycle_projection(
            package_refs=projected_package_refs,
            lifecycle_receipt_refs=projected_receipt_refs,
        ),
        "gap_summary": _project_gap_summary(gap_report),
        "export_verdict_refs": _project_export_verdict_refs(export_verdict),
        "manual_portal_boundary": _project_manual_portal_boundary(manual_portal_boundary),
        "receipt_refs": projected_receipt_refs,
        "authority_boundary": _authority_boundary(),
        "projection_policy": "refs_and_gap_summary_only_no_content_payloads_no_private_material",
    }


def _require_mapping_payload(payload: Mapping[str, Any], *, context: str) -> None:
    if not isinstance(payload, Mapping):
        raise WorkspaceStateError(f"{context} must be a JSON object.")


def _reject_forbidden_payload(payload: Mapping[str, Any], *, context: str) -> None:
    for path, key, value in _walk_payload(payload, root=context):
        normalized_key = _normalize_key(key)
        if normalized_key in _OPL_EXPORT_READY_CLAIM_KEYS and bool(value):
            raise WorkspaceStateError("OPL cannot declare MAG export readiness.")
        if normalized_key in _OPL_ARTIFACT_WRITE_KEYS and bool(value):
            raise WorkspaceStateError("OPL cannot write MAG artifact or package body.")
        if _is_forbidden_body_key(normalized_key):
            raise WorkspaceStateError(
                f"{path} contains package body or private evidence, which cannot be projected."
            )
        if isinstance(value, str) and _looks_like_private_evidence_token(value):
            raise WorkspaceStateError(
                f"{path} contains package body or private evidence, which cannot be projected."
            )


def _walk_payload(payload: Any, *, root: str) -> list[tuple[str, str, Any]]:
    items: list[tuple[str, str, Any]] = []
    if isinstance(payload, Mapping):
        for raw_key, value in payload.items():
            if not isinstance(raw_key, str) or not raw_key.strip():
                raise WorkspaceStateError(f"{root} keys must be non-empty strings.")
            key = raw_key.strip()
            path = f"{root}.{key}"
            items.append((path, key, value))
            items.extend(_walk_payload(value, root=path))
    elif isinstance(payload, list):
        for index, item in enumerate(payload):
            items.extend(_walk_payload(item, root=f"{root}[{index}]"))
    return items


def _read_ref_mapping(payload: Mapping[str, Any], *, context: str) -> dict[str, Any]:
    refs: dict[str, Any] = {}
    for raw_key, value in payload.items():
        key = _require_nonempty_string(raw_key, field_name=f"{context}.key", context=context)
        if isinstance(value, str):
            refs[key] = _require_nonempty_string(value, field_name=key, context=context)
            continue
        if isinstance(value, list):
            refs[key] = _read_string_list(value, field_name=key, context=context)
            continue
        raise WorkspaceStateError(f"{context}.{key} must be a ref string or ref string list.")
    if not refs:
        raise WorkspaceStateError(f"{context} requires at least one ref.")
    if context == "package_refs":
        _require_stage_folder_package_refs(refs)
    return refs


def _require_stage_folder_package_refs(refs: Mapping[str, Any]) -> None:
    for key in REQUIRED_STAGE_FOLDER_PACKAGE_REF_KEYS:
        value = refs.get(key)
        if not isinstance(value, str) or not value.strip():
            raise WorkspaceStateError(f"package_refs.{key} is required for stage folder lifecycle projection.")


def _stage_folder_lifecycle_projection(
    *,
    package_refs: Mapping[str, Any],
    lifecycle_receipt_refs: Mapping[str, Any],
) -> dict[str, Any]:
    owner_closeout_ref = _owner_receipt_or_typed_blocker_ref(lifecycle_receipt_refs)
    return {
        "surface_kind": "mag_stage_folder_lifecycle_projection",
        "stage_id": PACKAGE_STAGE_ID,
        "artifact_bundle": {
            "ref": str(package_refs["artifact_bundle_ref"]),
            "lifecycle_contract_role": STAGE_OUTPUT_ARTIFACT_LIFECYCLE_ROLE,
            "stage_output_role": PACKAGE_STAGE_OUTPUT_ROLE,
        },
        "final_package": {
            "ref": str(package_refs["final_package_ref"]),
            "lifecycle_contract_role": FINAL_PACKAGE_LIFECYCLE_ROLE,
        },
        "submission_ready_package": {
            "ref": str(package_refs["submission_ready_package_ref"]),
            "lifecycle_contract_role": SUBMISSION_READY_PACKAGE_LIFECYCLE_ROLE,
        },
        "owner_receipt_or_typed_blocker_ref": owner_closeout_ref,
        "missing_output_policy": "typed_blocker_required_no_opl_inference",
        "handoff_policy": PACKAGE_LIFECYCLE_HANDOFF_POLICY,
        "authority_boundary": {
            "mag_owns_package_authority": True,
            "mag_owns_export_verdict": True,
            "opl_can_read_artifact_body": False,
            "opl_can_interpret_grant_quality": False,
            "opl_can_declare_submission_ready": False,
        },
    }


def _owner_receipt_or_typed_blocker_ref(lifecycle_receipt_refs: Mapping[str, Any]) -> str:
    for key in ("owner_receipt_ref", "typed_blocker_ref", "lifecycle_receipt_ref"):
        value = lifecycle_receipt_refs.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    raise WorkspaceStateError(
        "lifecycle_receipt_refs requires owner_receipt_ref, typed_blocker_ref, or lifecycle_receipt_ref."
    )


def _project_gap_summary(gap_report: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "gap_report_ref": _require_nonempty_string(
            gap_report.get("gap_report_ref"),
            field_name="gap_report_ref",
            context="gap_report",
        ),
        "state": _optional_string(gap_report.get("state"), field_name="state", context="gap_report"),
        "summary": _require_nonempty_string(
            gap_report.get("summary"),
            field_name="summary",
            context="gap_report",
        ),
        "gap_refs": _read_string_list(
            gap_report.get("gap_refs", []),
            field_name="gap_refs",
            context="gap_report",
        ),
    }


def _project_export_verdict_refs(export_verdict: Mapping[str, Any]) -> dict[str, str]:
    try:
        return normalize_submission_ready_export_verdict(export_verdict, context="export_verdict")
    except SubmissionReadyExportVerdictError as exc:
        raise WorkspaceStateError(str(exc)) from exc


def _project_manual_portal_boundary(manual_portal_boundary: Mapping[str, Any]) -> dict[str, str]:
    projected = {
        "manual_portal_boundary_ref": _require_nonempty_string(
            manual_portal_boundary.get("manual_portal_boundary_ref"),
            field_name="manual_portal_boundary_ref",
            context="manual_portal_boundary",
        )
    }
    for key in ("state", "safe_action_ref"):
        value = manual_portal_boundary.get(key)
        if value is not None:
            projected[key] = _require_nonempty_string(
                value,
                field_name=key,
                context="manual_portal_boundary",
            )
    return projected


def _read_string_list(value: Any, *, field_name: str, context: str) -> list[str]:
    if not isinstance(value, list):
        raise WorkspaceStateError(f"{context}.{field_name} must be a string list.")
    refs: list[str] = []
    for item in value:
        ref = _require_nonempty_string(item, field_name=field_name, context=context)
        if ref not in refs:
            refs.append(ref)
    return refs


def _optional_string(value: Any, *, field_name: str, context: str) -> str | None:
    if value is None:
        return None
    return _require_nonempty_string(value, field_name=field_name, context=context)


def _normalize_key(key: str) -> str:
    return key.strip().lower().replace("-", "_").replace(" ", "_")


def _is_forbidden_body_key(normalized_key: str) -> bool:
    return any(all(part in normalized_key for part in parts) for parts in _FORBIDDEN_BODY_KEY_PARTS)


def _looks_like_private_evidence_token(value: str) -> bool:
    normalized = value.lower().replace("-", "_").replace(" ", "_")
    return "private_evidence" in normalized or "package_body" in normalized


def _authority_boundary() -> dict[str, bool | str]:
    return {
        "mag_owns_submission_export_verdict": True,
        "mag_owns_submission_ready_export_verdict": True,
        "mag_owns_export_verdict": True,
        "mag_owns_package_authority": True,
        "mag_owns_stage_folder_lifecycle_projection": True,
        "mag_owns_package_refs": True,
        "mag_owns_gap_report": True,
        "mag_owns_manual_portal_boundary": True,
        "mag_owns_lifecycle_receipt_refs": True,
        "opl_owns_artifact_package_lifecycle_shell": True,
        "opl_owns_locator": True,
        "opl_owns_retention_ui": True,
        "opl_role": "artifact_package_lifecycle_shell_consumer",
        "opl_can_declare_export_ready": False,
        "opl_can_declare_submission_ready": False,
        "opl_can_issue_export_verdict": False,
        "opl_can_write_artifact_body": False,
        "opl_can_write_package_content": False,
        "opl_can_hold_package_authority": False,
        "opl_can_interpret_grant_quality": False,
    }


__all__ = [
    "PACKAGE_LIFECYCLE_HANDOFF_PROJECTION_KIND",
    "build_package_lifecycle_handoff_projection",
]
