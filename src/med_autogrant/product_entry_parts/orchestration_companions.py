from __future__ import annotations

from typing import Any, Mapping

from med_autogrant.product_entry_parts.primitives import (
    GRANT_DIRECT_ENTRY_KIND,
    GRANT_USER_LOOP_KIND,
    PRODUCT_FRONTDESK_KIND,
    TARGET_DOMAIN_ID,
    _optional_mapping,
    _optional_string_from_mapping,
    _require_mapping,
    _require_nonempty_string,
    _require_nonempty_string_from_mapping,
)
from med_autogrant.product_entry_parts.runtime_contracts import _build_author_side_route_contract
from med_autogrant.workspace_types import WorkspaceStateError

from opl_harness_shared.family_orchestration import (
    buildFamilyIntakeEvidenceCompanion as _build_shared_family_intake_evidence_companion,
    build_family_product_entry_orchestration as _build_shared_family_product_entry_orchestration,
)
from opl_harness_shared.managed_runtime import build_managed_runtime_contract as _build_shared_managed_runtime_contract
from opl_harness_shared.product_entry_companions import (
    build_product_entry_start as _build_shared_product_entry_start,
    collect_family_human_gate_ids as _collect_family_human_gate_ids,
)


def _build_managed_runtime_contract() -> dict[str, Any]:
    return _build_shared_managed_runtime_contract(
        domain_owner=TARGET_DOMAIN_ID,
        executor_owner="med-autogrant",
        supervision_status_surface="grant_progress",
        attention_queue_surface=GRANT_USER_LOOP_KIND,
        recovery_contract_surface=GRANT_USER_LOOP_KIND,
    )


def _build_product_entry_start(
    *,
    product_frontdesk_command: str,
    grant_user_loop_command: str,
    grant_direct_entry_command: str,
    operator_loop_actions: Mapping[str, Mapping[str, Any]],
    family_orchestration: Mapping[str, Any],
) -> dict[str, Any]:
    return _build_shared_product_entry_start(
        summary=(
            "先进入 direct grant frontdesk；需要继续当前写作主线时恢复 grant user loop，"
            "需要把用户意图显式装配成入口合同时再构建 direct entry。"
        ),
        recommended_mode_id="open_frontdesk",
        modes=[
            {
                "mode_id": "open_frontdesk",
                "title": "Open grant frontdesk",
                "command": product_frontdesk_command,
                "surface_kind": PRODUCT_FRONTDESK_KIND,
                "summary": "打开当前 direct grant frontdoor。",
                "requires": [],
            },
            {
                "mode_id": "continue_grant_loop",
                "title": "Continue current grant loop",
                "command": grant_user_loop_command,
                "surface_kind": GRANT_USER_LOOP_KIND,
                "summary": _require_nonempty_string_from_mapping(
                    operator_loop_actions["open_loop"],
                    "summary",
                    context="operator_loop_actions.open_loop",
                ),
                "requires": ["task_intent"],
            },
            {
                "mode_id": "build_direct_entry",
                "title": "Build direct entry",
                "command": grant_direct_entry_command,
                "surface_kind": GRANT_DIRECT_ENTRY_KIND,
                "summary": _require_nonempty_string_from_mapping(
                    operator_loop_actions["build_direct_entry"],
                    "summary",
                    context="operator_loop_actions.build_direct_entry",
                ),
                "requires": list(
                    _require_mapping(
                        operator_loop_actions,
                        "build_direct_entry",
                        context="operator_loop_actions",
                    ).get("requires")
                    or []
                ),
            },
        ],
        resume_surface=dict(
            _require_mapping(
                family_orchestration,
                "resume_contract",
                context="family_orchestration",
            )
        ),
        human_gate_ids=_collect_family_human_gate_ids(family_orchestration),
    )


def _route_status_from_route_id(route_id: str) -> str:
    resolved_route_id = _require_nonempty_string(route_id, field_name="route_id")
    route_contract = _build_author_side_route_contract(
        resolved_route_id,
        source_stage=resolved_route_id,
    )
    return _require_nonempty_string_from_mapping(
        route_contract,
        "route_status",
        context="author_side_route_contract",
    )


def _build_family_orchestration_companion(
    *,
    current_route_id: str,
    recommended_route_id: str,
    recommended_route_status: str,
    needs_author_decision: bool,
    workspace_summary: Mapping[str, Any] | None = None,
    intake_evidence_companion: Mapping[str, Any] | None = None,
    project_profile_companion: Mapping[str, Any] | None = None,
    review_surface_ref: str,
    event_envelope_surface_ref: str,
    checkpoint_lineage_surface_ref: str,
    resume_surface_kind: str,
) -> dict[str, Any]:
    resolved_current_route_id = _require_nonempty_string(current_route_id, field_name="current_route_id")
    resolved_recommended_route_id = _require_nonempty_string(
        recommended_route_id,
        field_name="recommended_route_id",
    )
    resolved_review_surface_ref = _require_nonempty_string(
        review_surface_ref,
        field_name="review_surface_ref",
    )
    resolved_event_envelope_surface_ref = _require_nonempty_string(
        event_envelope_surface_ref,
        field_name="event_envelope_surface_ref",
    )
    resolved_checkpoint_lineage_surface_ref = _require_nonempty_string(
        checkpoint_lineage_surface_ref,
        field_name="checkpoint_lineage_surface_ref",
    )
    resolved_resume_surface_kind = _require_nonempty_string(
        resume_surface_kind,
        field_name="resume_surface_kind",
    )
    route_status = _require_nonempty_string(
        recommended_route_status,
        field_name="recommended_route_status",
    )
    if route_status not in {"landed", "pending"}:
        raise WorkspaceStateError("family_orchestration.recommended_route_status 只允许 landed 或 pending。")

    gate_status = "requested" if needs_author_decision or route_status == "pending" else "approved"
    gate_id = f"mag_route_gate_{resolved_recommended_route_id}"
    current_node_id = f"route:{resolved_current_route_id}"
    recommended_node_id = f"route:{resolved_recommended_route_id}"
    edge_on = "decision" if gate_status == "requested" else "success"
    resolved_intake_evidence_companion = (
        dict(intake_evidence_companion)
        if isinstance(intake_evidence_companion, Mapping)
        else _build_intake_evidence_companion(workspace_summary)
    )
    resolved_project_profile_companion = (
        dict(project_profile_companion)
        if isinstance(project_profile_companion, Mapping)
        else _build_project_profile_companion(workspace_summary)
    )
    payload = _build_shared_family_product_entry_orchestration(
        graph_id=f"mag_{resolved_current_route_id}_to_{resolved_recommended_route_id}_graph",
        target_domain_id=TARGET_DOMAIN_ID,
        graph_kind="grant_route_orchestration",
        graph_version="2026-04-13",
        nodes=[
            {
                "node_id": current_node_id,
                "node_kind": _route_to_action_node_kind(resolved_current_route_id),
                "title": f"Current route: {resolved_current_route_id}",
                "produces_checkpoint": True,
            },
            {
                "node_id": recommended_node_id,
                "node_kind": _route_to_action_node_kind(resolved_recommended_route_id),
                "title": f"Recommended route: {resolved_recommended_route_id}",
                "produces_checkpoint": True,
            },
        ],
        edges=[
            {
                "from": current_node_id,
                "to": recommended_node_id,
                "on": edge_on,
            }
        ],
        entry_nodes=[current_node_id],
        exit_nodes=[recommended_node_id],
        human_gates=[
            {
                "gate_id": gate_id,
                "trigger_nodes": [recommended_node_id],
                "blocking": gate_status == "requested",
            }
        ],
        checkpoint_nodes=[current_node_id, recommended_node_id],
        human_gate_previews=[
            {
                "gate_id": gate_id,
                "title": f"确认 {resolved_recommended_route_id} route 执行决策",
                "status": gate_status,
                "review_surface": {
                    "ref_kind": "json_pointer",
                    "ref": resolved_review_surface_ref,
                    "label": "route review surface",
                },
            }
        ],
        action_graph_ref={
            "ref_kind": "json_pointer",
            "ref": "/family_orchestration/action_graph",
            "label": "mag family action graph",
        },
        resume_surface_kind=resolved_resume_surface_kind,
        session_locator_field="grant_run_id",
        checkpoint_locator_field="lifecycle_stage",
        event_envelope_surface={
            "ref_kind": "json_pointer",
            "ref": resolved_event_envelope_surface_ref,
            "label": "family event envelope surface",
        },
        checkpoint_lineage_surface={
            "ref_kind": "json_pointer",
            "ref": resolved_checkpoint_lineage_surface_ref,
            "label": "family checkpoint lineage surface",
        },
        intake_evidence_companion=resolved_intake_evidence_companion,
    )
    if resolved_project_profile_companion is not None:
        payload["project_profile_companion"] = resolved_project_profile_companion
    return payload


def _route_to_action_node_kind(route_id: str) -> str:
    if route_id in {"critique", "revision", "frozen"}:
        return "review"
    if route_id in {"artifact_bundle", "final_package", "hosted_contract_bundle"}:
        return "publish"
    return "authoring"


def _build_intake_evidence_companion(workspace_summary: Mapping[str, Any] | None) -> dict[str, Any] | None:
    if not isinstance(workspace_summary, Mapping):
        return None
    intake_audit = _optional_mapping(workspace_summary, "grant_intake_audit")
    evidence_grounding = _optional_mapping(workspace_summary, "grant_evidence_grounding")
    intake_snapshot = _optional_mapping(workspace_summary, "intake_snapshot")
    if not isinstance(intake_audit, Mapping) or not isinstance(evidence_grounding, Mapping):
        return None
    trust_ranked_evidence = [
        entry
        for entry in evidence_grounding.get("trust_ranked_evidence", [])
        if isinstance(entry, Mapping)
    ]
    if not trust_ranked_evidence:
        return None

    workspace_id = _require_nonempty_string_from_mapping(
        workspace_summary,
        "workspace_id",
        context="summarize-workspace",
    )
    funding_program = (
        _require_nonempty_string_from_mapping(
            intake_snapshot,
            "funding_program",
            context="summarize-workspace.intake_snapshot",
        )
        if isinstance(intake_snapshot, Mapping)
        else _require_nonempty_string_from_mapping(
            evidence_grounding,
            "funding_program",
            context="grant_evidence_grounding",
        )
    )
    return _build_shared_family_intake_evidence_companion(
        target_domain_id=TARGET_DOMAIN_ID,
        intake_audit={
            "summary": _require_nonempty_string_from_mapping(
                intake_audit,
                "summary",
                context="grant_intake_audit",
            ),
            "verdict": _require_nonempty_string_from_mapping(
                intake_audit,
                "overall_readiness",
                context="grant_intake_audit",
            ),
            "summary_ref": {
                "ref_kind": "workspace_locator",
                "ref": f"grant_workspace::{workspace_id}::grant_intake_audit",
                "label": "grant intake audit",
            },
        },
        trust_ranked_evidence_refs=[
            {
                "ref_kind": _require_nonempty_string_from_mapping(
                    entry,
                    "ref_kind",
                    context="grant_evidence_grounding.trust_ranked_evidence",
                ),
                "ref": _require_nonempty_string_from_mapping(
                    entry,
                    "ref",
                    context="grant_evidence_grounding.trust_ranked_evidence",
                ),
                "label": _require_nonempty_string_from_mapping(
                    entry,
                    "label",
                    context="grant_evidence_grounding.trust_ranked_evidence",
                ),
                "trust_rank": int(entry["trust_rank"]),
                "trust_note": _optional_string_from_mapping(entry, "trust_note"),
                "supports": list(entry.get("supports") or []),
            }
            for entry in trust_ranked_evidence
        ],
        grounding_scope={
            "scope_kind": _require_nonempty_string_from_mapping(
                evidence_grounding,
                "scope_kind",
                context="grant_evidence_grounding",
            ),
            "summary": _require_nonempty_string_from_mapping(
                evidence_grounding,
                "summary",
                context="grant_evidence_grounding",
            ),
            "scope_refs": [
                {
                    "ref_kind": "workspace_locator",
                    "ref": f"grant_workspace::{workspace_id}::grant_evidence_grounding",
                    "label": "grant evidence grounding",
                },
                {
                    "ref_kind": "workspace_locator",
                    "ref": f"grant_workspace::{workspace_id}::funding_opportunity_brief::{funding_program}",
                    "label": "funding opportunity brief",
                },
            ],
        },
        human_gate_refs=[
            {
                "ref_kind": "workspace_locator",
                "ref": f"grant_workspace::{workspace_id}::family_human_gate",
                "label": "grant route gate",
            }
        ],
        checkpoint_lineage_refs=[
            {
                "ref_kind": "workspace_locator",
                "ref": f"grant_workspace::{workspace_id}::checkpoint_lineage",
                "label": "grant checkpoint lineage",
            }
        ],
    )


def _build_project_profile_companion(workspace_summary: Mapping[str, Any] | None) -> dict[str, Any] | None:
    if not isinstance(workspace_summary, Mapping):
        return None
    workspace_id = _require_nonempty_string_from_mapping(
        workspace_summary,
        "workspace_id",
        context="summarize-workspace",
    )
    project_profile = _require_mapping(
        workspace_summary,
        "project_profile",
        context="summarize-workspace",
    )
    profile_id = _require_nonempty_string_from_mapping(
        project_profile,
        "profile_id",
        context="summarize-workspace.project_profile",
    )
    funding_program = _require_nonempty_string_from_mapping(
        project_profile,
        "funding_program",
        context="summarize-workspace.project_profile",
    )
    return {
        "surface_kind": "project_profile_companion",
        "version": 1,
        "profile_id": profile_id,
        "preset_id": _require_nonempty_string_from_mapping(
            project_profile,
            "preset_id",
            context="summarize-workspace.project_profile",
        ),
        "profile_label": _require_nonempty_string_from_mapping(
            project_profile,
            "profile_label",
            context="summarize-workspace.project_profile",
        ),
        "funding_program": funding_program,
        "funder": _require_nonempty_string_from_mapping(
            project_profile,
            "funder",
            context="summarize-workspace.project_profile",
        ),
        "program_family": _require_nonempty_string_from_mapping(
            project_profile,
            "program_family",
            context="summarize-workspace.project_profile",
        ),
        "template_profile": {
            "template_id": _require_nonempty_string_from_mapping(
                project_profile,
                "template_id",
                context="summarize-workspace.project_profile",
            ),
            "template_label": _require_nonempty_string_from_mapping(
                project_profile,
                "template_label",
                context="summarize-workspace.project_profile",
            ),
        },
        "collaboration_preferences": {
            "collaboration_mode": _require_nonempty_string_from_mapping(
                project_profile,
                "collaboration_mode",
                context="summarize-workspace.project_profile",
            ),
            "author_touchpoints": list(project_profile.get("author_touchpoints") or []),
            "evidence_policy": _require_nonempty_string_from_mapping(
                project_profile,
                "evidence_policy",
                context="summarize-workspace.project_profile",
            ),
            "drafting_voice": _require_nonempty_string_from_mapping(
                project_profile,
                "drafting_voice",
                context="summarize-workspace.project_profile",
            ),
        },
        "critique_policy": {
            "preset_id": _require_nonempty_string_from_mapping(
                project_profile,
                "critique_policy_preset_id",
                context="summarize-workspace.project_profile",
            ),
            "policy_id": _require_nonempty_string_from_mapping(
                project_profile,
                "critique_policy_id",
                context="summarize-workspace.project_profile",
            ),
        },
        "profile_ref": {
            "ref_kind": "workspace_locator",
            "ref": f"grant_workspace::{workspace_id}::project_profile::{profile_id}",
            "label": "project profile",
        },
        "funding_opportunity_ref": {
            "ref_kind": "workspace_locator",
            "ref": f"grant_workspace::{workspace_id}::funding_opportunity_brief::{funding_program}",
            "label": "funding opportunity brief",
        },
    }


__all__ = [name for name in globals() if not name.startswith("__")]
