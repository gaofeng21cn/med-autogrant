from __future__ import annotations

from typing import Any, Mapping

from med_autogrant.product_entry_parts.primitives import TARGET_DOMAIN_ID, _require_nonempty_string
from med_autogrant.workspace_types import WorkspaceStateError


MAG_OPL_OWNER_PAYLOAD_RESPONSE_KIND = "mag_opl_owner_payload_response"

_PRODUCTION_ACCEPTANCE_KIND = "mag_production_acceptance_evidence.v1"
_EXTERNAL_EVIDENCE_LEDGER_KIND = "mag_external_evidence_receipt_ledger.v1"
_RECEIPT_READINESS_KIND = "mag_receipt_readiness_projection"
_PAYLOAD_PATH_POLICY = (
    "operator_must_choose_success_refs_path_or_domain_owned_typed_blocker_path_empty_template_blocks"
)
_REQUIRED_RETURN_SHAPES = (
    "domain_owner_receipt_ref",
    "no_regression_evidence_ref",
    "owner_chain_ref",
    "typed_blocker_ref",
)
_STAGE_REQUIRED_RETURN_SHAPES = (
    "domain_receipt_ref",
    "monitor_freshness_ref",
    "runtime_event_ref",
    "typed_blocker_ref",
)
_STAGE_PAYLOAD_TEMPLATE = {
    "domain_receipt_refs": [],
    "monitor_freshness_refs": [],
    "runtime_event_refs": [],
    "typed_blocker_refs": [],
}
_FORBIDDEN_BODY_KEYS = frozenset(
    {
        "artifact_body",
        "artifact_content",
        "fundability_verdict_body",
        "grant_artifact_body",
        "grant_artifact_content",
        "grant_truth_body",
        "memory_body",
        "opl_runtime_state_body",
        "package_archive_body",
        "package_body",
        "proposal_text",
        "proposal_text_body",
        "submission_ready_export_verdict_body",
    }
)
_FORBIDDEN_READY_CLAIM_KEYS = frozenset(
    {
        "claims_authoring_quality_ready",
        "claims_export_ready",
        "claims_fundability_ready",
        "claims_grant_or_fundability_ready",
        "claims_grant_ready",
        "claims_human_approval_obtained",
        "claims_quality_ready",
        "claims_submission_ready",
        "claims_submission_ready_export",
        "export_ready",
        "fundability_ready",
        "quality_ready",
        "submission_ready",
        "submission_ready_export",
    }
)


def build_opl_owner_payload_response(
    *,
    production_acceptance: Mapping[str, Any],
    external_evidence_receipt_ledger: Mapping[str, Any],
    receipt_readiness_projection: Mapping[str, Any],
) -> dict[str, Any]:
    _assert_mapping_kind(
        production_acceptance,
        expected_kind=_PRODUCTION_ACCEPTANCE_KIND,
        context="production_acceptance",
    )
    _assert_mapping_kind(
        external_evidence_receipt_ledger,
        expected_kind=_EXTERNAL_EVIDENCE_LEDGER_KIND,
        context="external_evidence_receipt_ledger",
    )
    _assert_mapping_kind(
        receipt_readiness_projection,
        expected_kind=_RECEIPT_READINESS_KIND,
        context="receipt_readiness_projection",
    )
    _assert_body_free(production_acceptance, path="production_acceptance")
    _assert_body_free(external_evidence_receipt_ledger, path="external_evidence_receipt_ledger")
    _assert_body_free(receipt_readiness_projection, path="receipt_readiness_projection")

    production_receipt_refs = _production_owner_receipt_refs(production_acceptance)
    production_support_refs = _production_owner_chain_support_refs(production_acceptance)
    ledger_owner_refs = _ledger_owner_receipt_refs(external_evidence_receipt_ledger)
    receipt_readiness_refs = _receipt_readiness_refs(receipt_readiness_projection)
    typed_blocker_refs = _submission_ready_typed_blocker_refs(external_evidence_receipt_ledger)
    no_regression_refs = _no_regression_evidence_refs(external_evidence_receipt_ledger)
    stage_expected_receipt_payload_summary = _stage_expected_receipt_payload_summary(
        external_evidence_receipt_ledger
    )
    domain_owner_receipt_refs = _dedupe(
        [*production_receipt_refs, *ledger_owner_refs, *receipt_readiness_refs["owner_receipt"]]
    )
    owner_chain_refs = _dedupe(
        [
            *domain_owner_receipt_refs,
            *production_support_refs,
            *receipt_readiness_refs["memory_accept_reject"],
            *receipt_readiness_refs["package_export_lifecycle"],
            *receipt_readiness_refs["cleanup_restore_retention_lifecycle"],
            *_monitor_freshness_refs(external_evidence_receipt_ledger),
        ]
    )
    record_payload = {
        "domain_id": TARGET_DOMAIN_ID,
        "domain_owner_receipt_refs": domain_owner_receipt_refs,
        "typed_blocker_refs": typed_blocker_refs,
        "owner_chain_refs": owner_chain_refs,
        "no_regression_evidence_refs": no_regression_refs,
        "domain_receipt_refs": domain_owner_receipt_refs,
        "no_regression_refs": no_regression_refs,
    }
    return {
        "surface_kind": MAG_OPL_OWNER_PAYLOAD_RESPONSE_KIND,
        "version": "v1",
        "status": _response_status(typed_blocker_refs),
        "mode": "refs_only_domain_owner_receipt_or_domain_owned_typed_blocker_payload",
        "owner": TARGET_DOMAIN_ID,
        "target_domain_id": TARGET_DOMAIN_ID,
        "domain_id": TARGET_DOMAIN_ID,
        "record_payload": record_payload,
        "opl_runtime_action_execute_payload": record_payload,
        "domain_owner_receipt_refs": domain_owner_receipt_refs,
        "typed_blocker_refs": typed_blocker_refs,
        "owner_chain_refs": owner_chain_refs,
        "no_regression_evidence_refs": no_regression_refs,
        "stage_expected_receipt_payload_summary": stage_expected_receipt_payload_summary,
        "required_return_shapes": list(_REQUIRED_RETURN_SHAPES),
        "payload_path_policy": _PAYLOAD_PATH_POLICY,
        "accepted_payload_paths": _accepted_payload_paths(),
        "body_included": False,
        "grant_ready_claimed": False,
        "quality_ready_claimed": False,
        "export_ready_claimed": False,
        "submission_ready_claimed": False,
        "authority_boundary": {
            "owner": TARGET_DOMAIN_ID,
            "refs_only": True,
            "mag_owner_receipt_authority": True,
            "opl_records_refs_only": True,
            "opl_writes_grant_truth": False,
            "opl_reads_memory_body": False,
            "opl_reads_artifact_body": False,
            "opl_authorizes_quality_or_export": False,
            "can_declare_fundability_ready": False,
            "can_declare_quality_ready": False,
            "can_declare_export_ready": False,
            "can_declare_submission_ready": False,
            "typed_blocker_is_submission_ready": False,
        },
        "forbidden_payload_fields": sorted(_FORBIDDEN_BODY_KEYS),
    }


def _assert_mapping_kind(value: Any, *, expected_kind: str, context: str) -> None:
    if not isinstance(value, Mapping):
        raise WorkspaceStateError(f"{context} 必须是 JSON object。")
    if value.get("surface_kind") != expected_kind:
        raise WorkspaceStateError(f"{context}.surface_kind 必须是 {expected_kind}。")


def _production_owner_receipt_refs(production_acceptance: Mapping[str, Any]) -> list[str]:
    refs: list[str] = []
    closure = _optional_mapping(production_acceptance, "closure_evidence")
    if closure is not None:
        owner_receipt_ref = closure.get("owner_receipt_ref")
        if owner_receipt_ref is not None:
            refs.append(
                _require_nonempty_string(
                    owner_receipt_ref,
                    field_name="owner_receipt_ref",
                    context="production_acceptance.closure_evidence",
                )
            )
    production_refs = _optional_mapping(production_acceptance, "refs")
    refs.extend(_owner_payload_receipt_refs(_read_ref_list(production_refs, "owner_receipt_refs")))
    refs.extend(_owner_payload_receipt_refs(_read_ref_list(production_refs, "grant_owner_receipt_refs")))
    return _dedupe(refs)


def _production_owner_chain_support_refs(production_acceptance: Mapping[str, Any]) -> list[str]:
    production_refs = _optional_mapping(production_acceptance, "refs")
    refs = [
        *_read_ref_list(production_refs, "owner_receipt_refs"),
        *_read_ref_list(production_refs, "grant_owner_receipt_refs"),
        *_read_ref_list(production_refs, "conformance_refs"),
    ]
    return _dedupe(refs)


def _owner_payload_receipt_refs(refs: list[str]) -> list[str]:
    return [
        ref
        for ref in refs
        if ref.startswith("receipt:")
        or ref.startswith("runtime://")
        or ref.startswith("workspace-runtime-ref:")
    ]


def _ledger_owner_receipt_refs(ledger: Mapping[str, Any]) -> list[str]:
    refs: list[str] = []
    closeout = _optional_mapping(ledger, "grant_stage_controlled_attempt_closeout")
    if closeout is None:
        return refs
    ref_packet = _optional_mapping(closeout, "live_grant_stage_attempt_ref_packet")
    if ref_packet is not None:
        refs.extend(
            _owner_receipt_or_typed_blocker_ref(
                _optional_mapping(ref_packet, "owner_receipt_or_typed_blocker_refs")
            )
        )
    stage_closeout_refs = closeout.get("stage_closeout_refs", [])
    if not isinstance(stage_closeout_refs, list):
        raise WorkspaceStateError("grant_stage_controlled_attempt_closeout.stage_closeout_refs 必须是 list。")
    for index, item in enumerate(stage_closeout_refs):
        if not isinstance(item, Mapping):
            raise WorkspaceStateError(f"stage_closeout_refs[{index}] 必须是 object。")
        ref = item.get("owner_receipt_or_typed_blocker_ref")
        if ref is not None:
            refs.append(
                _require_nonempty_string(
                    ref,
                    field_name="owner_receipt_or_typed_blocker_ref",
                    context=f"stage_closeout_refs[{index}]",
                )
            )
    return _dedupe(refs)


def _owner_receipt_or_typed_blocker_ref(value: Mapping[str, Any] | None) -> list[str]:
    if value is None:
        return []
    refs: list[str] = []
    for field_name in ("owner_receipt_ref", "typed_blocker_ref"):
        ref = value.get(field_name)
        if ref is not None:
            refs.append(_require_nonempty_string(ref, field_name=field_name))
    return refs


def _receipt_readiness_refs(projection: Mapping[str, Any]) -> dict[str, list[str]]:
    receipt_refs = _optional_mapping(projection, "receipt_refs") or {}
    return {
        "owner_receipt": _read_ref_list(receipt_refs, "owner_receipt"),
        "memory_accept_reject": _read_ref_list(receipt_refs, "memory_accept_reject"),
        "package_export_lifecycle": _read_ref_list(receipt_refs, "package_export_lifecycle"),
        "cleanup_restore_retention_lifecycle": _read_ref_list(
            receipt_refs,
            "cleanup_restore_retention_lifecycle",
        ),
    }


def _submission_ready_typed_blocker_refs(ledger: Mapping[str, Any]) -> list[str]:
    refs: list[str] = []
    closeout = _optional_mapping(ledger, "grant_stage_controlled_attempt_closeout")
    if closeout is None:
        return refs
    tail = _optional_mapping(closeout, "submission_ready_export_gate_tail")
    if tail is not None:
        typed_blocker_ref = tail.get("typed_blocker_ref")
        if typed_blocker_ref is not None:
            refs.append(
                _require_nonempty_string(
                    typed_blocker_ref,
                    field_name="typed_blocker_ref",
                    context="submission_ready_export_gate_tail",
                )
            )
    typed_blocker_items = closeout.get("stage_typed_blocker_refs", [])
    if typed_blocker_items is None:
        return _dedupe(refs)
    if not isinstance(typed_blocker_items, list):
        raise WorkspaceStateError("grant_stage_controlled_attempt_closeout.stage_typed_blocker_refs 必须是 list。")
    for index, item in enumerate(typed_blocker_items):
        if not isinstance(item, Mapping):
            raise WorkspaceStateError(f"stage_typed_blocker_refs[{index}] 必须是 object。")
        ref = item.get("typed_blocker_ref")
        if ref is not None:
            refs.append(
                _require_nonempty_string(
                    ref,
                    field_name="typed_blocker_ref",
                    context=f"stage_typed_blocker_refs[{index}]",
                )
            )
    return _dedupe(refs)


def _stage_expected_receipt_payload_summary(ledger: Mapping[str, Any]) -> dict[str, Any]:
    closeout = _optional_mapping(ledger, "grant_stage_controlled_attempt_closeout")
    if closeout is None:
        stage_closeout_refs: list[Mapping[str, Any]] = []
    else:
        raw_stage_closeout_refs = closeout.get("stage_closeout_refs", [])
        if raw_stage_closeout_refs is None:
            raw_stage_closeout_refs = []
        if not isinstance(raw_stage_closeout_refs, list):
            raise WorkspaceStateError("grant_stage_controlled_attempt_closeout.stage_closeout_refs 必须是 list。")
        stage_closeout_refs = []
        for index, item in enumerate(raw_stage_closeout_refs):
            if not isinstance(item, Mapping):
                raise WorkspaceStateError(f"stage_closeout_refs[{index}] 必须是 object。")
            stage_closeout_refs.append(item)

    stage_blocker_refs_by_id = _stage_source_runtime_typed_blocker_refs_by_id(closeout)
    stages = [
        _stage_expected_receipt_payload_item(
            item,
            sequence=index + 1,
            stage_blocker=stage_blocker_refs_by_id.get(
                _require_nonempty_string(
                    item.get("stage_id"),
                    field_name="stage_id",
                    context=f"stage_closeout_refs[{index}]",
                )
            ),
        )
        for index, item in enumerate(stage_closeout_refs)
    ]
    stage_ids = [stage["stage_id"] for stage in stages]
    typed_blocker_refs = _dedupe(
        [
            ref
            for stage in stages
            for ref in stage["typed_blocker_path_payload"]["typed_blocker_refs"]
        ]
    )
    return {
        "surface_kind": "mag_stage_expected_receipt_payload_summary",
        "owner": TARGET_DOMAIN_ID,
        "consumer": "one_person_lab",
        "status": _stage_expected_receipt_payload_status(typed_blocker_refs),
        "payload_kind": "stage_expected_receipt_or_monitor_freshness_refs",
        "payload_path_policy": _PAYLOAD_PATH_POLICY,
        "payload_body_allowed": False,
        "empty_payload_template_is_success_evidence": False,
        "required_operator_payload_refs": [
            "domain_receipt_refs",
            "monitor_freshness_refs",
            "runtime_event_refs",
            "typed_blocker_refs",
        ],
        "required_return_shapes": list(_STAGE_REQUIRED_RETURN_SHAPES),
        "accepted_payload_paths": _stage_accepted_payload_paths(),
        "accepted_payload_paths_ref": "mag owner payload response#/stage_expected_receipt_payload_summary/accepted_payload_paths",
        "stage_count": len(stages),
        "stage_ids": stage_ids,
        "stage_payload_template": dict(_STAGE_PAYLOAD_TEMPLATE),
        "typed_blocker_path_payload": {
            "typed_blocker_refs": typed_blocker_refs,
        },
        "success_ref_models": {
            "expected_receipt_ref_model": "contracts/external_evidence/mag-evidence-receipt-ledger.json#/grant_stage_controlled_attempt_closeout/stage_closeout_refs/*/expected_receipt_ref",
            "monitor_freshness_ref_model": "contracts/external_evidence/mag-evidence-receipt-ledger.json#/grant_stage_controlled_attempt_closeout/stage_closeout_refs/*/monitor_freshness_refs",
            "runtime_event_ref_model": "contracts/external_evidence/mag-evidence-receipt-ledger.json#/grant_stage_controlled_attempt_closeout/opl_stage_source_runtime_evidence_typed_blocker_handoff/stage_typed_blocker_refs/*/blocked_runtime_event_refs",
            "source_runtime_event_ref": "contracts/external_evidence/mag-evidence-receipt-ledger.json#/grant_stage_controlled_attempt_closeout/opl_stage_source_runtime_evidence_typed_blocker_handoff/stage_typed_blocker_refs/<stage-id>/blocked_runtime_event_refs",
        },
        "stages": stages,
        "operator_payload_submitted": False,
        "success_refs_visible_is_completion": False,
        "domain_readiness_claimed": False,
        "grant_ready_claimed": False,
        "quality_ready_claimed": False,
        "export_ready_claimed": False,
        "submission_ready_claimed": False,
        "production_soak_complete_claimed": False,
        "authority_boundary": _stage_payload_authority_boundary(),
    }


def _stage_expected_receipt_payload_item(
    item: Mapping[str, Any],
    *,
    sequence: int,
    stage_blocker: Mapping[str, Any] | None,
) -> dict[str, Any]:
    stage_id = _require_nonempty_string(item.get("stage_id"), field_name="stage_id")
    owner_receipt_or_typed_blocker_ref = item.get("owner_receipt_or_typed_blocker_ref")
    domain_receipt_refs: list[str] = []
    typed_blocker_refs: list[str] = []
    if owner_receipt_or_typed_blocker_ref is not None:
        ref = _require_nonempty_string(
            owner_receipt_or_typed_blocker_ref,
            field_name="owner_receipt_or_typed_blocker_ref",
            context=f"stage_closeout_refs[{sequence - 1}]",
        )
        if ref.startswith("receipt:") or ref.startswith("runtime://") or ref.startswith("workspace-runtime-ref:"):
            domain_receipt_refs.append(ref)
        else:
            typed_blocker_refs.append(ref)

    expected_receipt_ref = item.get("expected_receipt_ref")
    if expected_receipt_ref is not None:
        domain_receipt_refs.append(
            _require_nonempty_string(
                expected_receipt_ref,
                field_name="expected_receipt_ref",
                context=f"stage_closeout_refs[{sequence - 1}]",
            )
        )
    if stage_blocker is not None:
        blocker_ref = stage_blocker.get("typed_blocker_ref")
        if blocker_ref is not None:
            typed_blocker_refs.append(
                _require_nonempty_string(
                    blocker_ref,
                    field_name="typed_blocker_ref",
                    context=f"stage_source_runtime_typed_blocker_refs[{stage_id}]",
                )
            )
    return {
        "stage_id": stage_id,
        "sequence": sequence,
        "payload_kind": "stage_expected_receipt_or_monitor_freshness_refs",
        "current_payload_template": dict(_STAGE_PAYLOAD_TEMPLATE),
        "success_refs_path_payload": {
            "domain_receipt_refs": _dedupe(domain_receipt_refs),
            "monitor_freshness_refs": _read_ref_list(item, "monitor_freshness_refs"),
            "runtime_event_refs": _read_ref_list(stage_blocker, "blocked_runtime_event_refs"),
        },
        "typed_blocker_path_payload": {
            "typed_blocker_refs": _dedupe(typed_blocker_refs),
        },
        "operator_payload_submitted": False,
        "recommended_current_payload_path": (
            "typed_blocker_path" if typed_blocker_refs else "success_refs_path"
        ),
        "success_refs_visible_is_completion": False,
        "domain_readiness_claimed": False,
        "grant_ready_claimed": False,
        "quality_ready_claimed": False,
        "export_ready_claimed": False,
        "submission_ready_claimed": False,
        "production_soak_complete_claimed": False,
        "authority_boundary": _stage_payload_authority_boundary(),
    }


def _stage_source_runtime_typed_blocker_refs_by_id(
    closeout: Mapping[str, Any] | None,
) -> dict[str, Mapping[str, Any]]:
    if closeout is None:
        return {}
    handoff = _optional_mapping(closeout, "opl_stage_source_runtime_evidence_typed_blocker_handoff")
    if handoff is None:
        return {}
    raw_items = handoff.get("stage_typed_blocker_refs", [])
    if raw_items is None:
        return {}
    if not isinstance(raw_items, list):
        raise WorkspaceStateError(
            "opl_stage_source_runtime_evidence_typed_blocker_handoff.stage_typed_blocker_refs 必须是 list。"
        )
    stage_blockers: dict[str, Mapping[str, Any]] = {}
    for index, item in enumerate(raw_items):
        if not isinstance(item, Mapping):
            raise WorkspaceStateError(
                "opl_stage_source_runtime_evidence_typed_blocker_handoff."
                f"stage_typed_blocker_refs[{index}] 必须是 object。"
            )
        stage_id = _require_nonempty_string(
            item.get("stage_id"),
            field_name="stage_id",
            context=(
                "opl_stage_source_runtime_evidence_typed_blocker_handoff."
                f"stage_typed_blocker_refs[{index}]"
            ),
        )
        stage_blockers[stage_id] = item
    return stage_blockers


def _stage_expected_receipt_payload_status(typed_blocker_refs: list[str]) -> str:
    if typed_blocker_refs:
        return "per_stage_expected_receipt_payload_refs_ready_with_live_evidence_typed_blockers"
    return "per_stage_expected_receipt_payload_refs_ready"


def _stage_accepted_payload_paths() -> dict[str, dict[str, Any]]:
    return {
        "success_refs_path": {
            "required_any_operator_payload_refs": [
                "domain_receipt_refs",
                "monitor_freshness_refs",
                "runtime_event_refs",
            ],
            "typed_blocker_refs_must_be_absent": True,
            "closes_owner_chain": False,
            "closes_domain_ready": False,
            "closes_production_ready": False,
        },
        "typed_blocker_path": {
            "required_operator_payload_refs": ["typed_blocker_refs"],
            "success_claimed": False,
            "closes_owner_chain": False,
            "closes_domain_ready": False,
            "closes_production_ready": False,
        },
    }


def _stage_payload_authority_boundary() -> dict[str, Any]:
    return {
        "owner": TARGET_DOMAIN_ID,
        "refs_only": True,
        "mag_owns_domain_receipt_refs": True,
        "mag_owns_typed_blocker_refs": True,
        "opl_records_refs_only": True,
        "can_execute_domain_action": False,
        "can_write_domain_truth": False,
        "can_write_owner_receipt": False,
        "can_create_owner_receipt": False,
        "can_generate_domain_owner_receipt": False,
        "can_generate_typed_blocker": False,
        "can_close_owner_chain": False,
        "can_close_domain_ready": False,
        "can_claim_production_ready": False,
        "can_authorize_quality_or_export": False,
        "can_declare_fundability_ready": False,
        "can_declare_quality_ready": False,
        "can_declare_export_ready": False,
        "can_declare_submission_ready": False,
        "typed_blocker_is_submission_ready": False,
    }


def _no_regression_evidence_refs(ledger: Mapping[str, Any]) -> list[str]:
    closeout = _optional_mapping(ledger, "grant_stage_controlled_attempt_closeout")
    if closeout is None:
        return []
    refs = []
    for field_name in (
        "direct_hosted_parity_no_regression_ref",
        "no_forbidden_write_guard_ref",
        "release_dist_consumption_ref",
    ):
        ref = closeout.get(field_name)
        if ref is not None:
            refs.append(_require_nonempty_string(ref, field_name=field_name, context="grant_stage_closeout"))
    ref_packet = _optional_mapping(closeout, "live_grant_stage_attempt_ref_packet")
    if ref_packet is not None:
        for field_name in (
            "direct_hosted_parity_no_regression_ref",
            "no_forbidden_write_guard_ref",
            "release_dist_consumption_ref",
        ):
            ref = ref_packet.get(field_name)
            if ref is not None:
                refs.append(_require_nonempty_string(ref, field_name=field_name, context="live_ref_packet"))
    return _dedupe(refs)


def _monitor_freshness_refs(ledger: Mapping[str, Any]) -> list[str]:
    refs: list[str] = []
    closeout = _optional_mapping(ledger, "grant_stage_controlled_attempt_closeout")
    if closeout is None:
        return refs
    ref_packet = _optional_mapping(closeout, "live_grant_stage_attempt_ref_packet")
    if ref_packet is not None:
        refs.extend(_read_ref_list(ref_packet, "monitor_freshness_refs"))
    stage_closeout_refs = closeout.get("stage_closeout_refs", [])
    if isinstance(stage_closeout_refs, list):
        for index, item in enumerate(stage_closeout_refs):
            if not isinstance(item, Mapping):
                raise WorkspaceStateError(f"stage_closeout_refs[{index}] 必须是 object。")
            refs.extend(_read_ref_list(item, "monitor_freshness_refs"))
    return _dedupe(refs)


def _accepted_payload_paths() -> dict[str, dict[str, Any]]:
    return {
        "success_refs_path": {
            "required_any_operator_payload_refs": [
                "domain_owner_receipt_refs",
                "no_regression_evidence_refs",
                "owner_chain_refs",
            ],
            "typed_blocker_refs_must_be_absent": True,
            "closes_owner_chain": False,
            "closes_domain_ready": False,
            "closes_production_ready": False,
        },
        "typed_blocker_path": {
            "required_operator_payload_refs": ["typed_blocker_refs"],
            "success_claimed": False,
            "closes_owner_chain": False,
            "closes_domain_ready": False,
            "closes_production_ready": False,
        },
    }


def _response_status(typed_blocker_refs: list[str]) -> str:
    if any("submission_ready_export_gate" in ref for ref in typed_blocker_refs):
        return "blocked_by_submission_ready_human_gate"
    if typed_blocker_refs:
        return "blocked_by_domain_typed_blocker_refs"
    return "success_refs_ready_not_domain_ready"


def _assert_body_free(value: Any, *, path: str) -> None:
    if isinstance(value, Mapping):
        for raw_key, item in value.items():
            key = _require_nonempty_string(raw_key, field_name="key", context=path)
            normalized_key = _normalize_key(key)
            if normalized_key in _FORBIDDEN_BODY_KEYS:
                raise WorkspaceStateError(f"OPL owner payload response 禁止包含 body 字段: {path}.{key}")
            if normalized_key in _FORBIDDEN_READY_CLAIM_KEYS and bool(item):
                raise WorkspaceStateError(
                    f"OPL owner payload response 禁止包含 ready/export claim: {path}.{key}"
                )
            _assert_body_free(item, path=f"{path}.{key}")
        return
    if isinstance(value, list):
        for index, item in enumerate(value):
            _assert_body_free(item, path=f"{path}[{index}]")


def _optional_mapping(payload: Mapping[str, Any], field_name: str) -> Mapping[str, Any] | None:
    value = payload.get(field_name)
    if value is None:
        return None
    if not isinstance(value, Mapping):
        raise WorkspaceStateError(f"{field_name} 必须是 object。")
    return value


def _read_ref_list(value: Mapping[str, Any] | None, field_name: str) -> list[str]:
    if value is None:
        return []
    raw_refs = value.get(field_name, [])
    if raw_refs is None:
        return []
    if not isinstance(raw_refs, list):
        raise WorkspaceStateError(f"{field_name} 必须是 string list。")
    return [
        _require_nonempty_string(ref, field_name=field_name)
        for ref in raw_refs
    ]


def _normalize_key(value: str) -> str:
    return value.strip().lower().replace("-", "_").replace(" ", "_")


def _dedupe(values: list[str]) -> list[str]:
    deduped: list[str] = []
    for value in values:
        if value not in deduped:
            deduped.append(value)
    return deduped


__all__ = [
    "MAG_OPL_OWNER_PAYLOAD_RESPONSE_KIND",
    "build_opl_owner_payload_response",
]
