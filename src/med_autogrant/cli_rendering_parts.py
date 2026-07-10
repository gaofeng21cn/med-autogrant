from __future__ import annotations

import json
from typing import Any, Callable

from opl_harness_shared.status_narration import build_status_narration_human_view


_HUMAN_FIELD_LABELS = {
    "grant_run_id": "当前 grant run",
    "workspace_id": "当前 workspace",
    "lifecycle_stage": "当前阶段",
    "ok": "校验结果",
    "error_count": "错误数量",
    "mode": "当前模式",
    "selected_direction": "当前方向",
    "selected_question": "当前问题",
    "active_fit_mapping": "当前 fit 映射",
    "active_draft": "当前草稿",
    "active_critique_verdict": "当前批注结论",
    "critique_id": "当前批注编号",
    "draft_id": "当前草稿编号",
    "verdict": "当前结论",
    "overall_diagnosis": "整体诊断",
    "recommended_next_stage": "建议下一阶段",
    "active_tranche": "维护者参考 tranche",
    "next_action": "当前动作",
    "run_recommended_route": "推荐执行命令",
    "ready_to_try_now": "当前可直接尝试",
    "recommended_check_command": "前置检查命令",
    "recommended_start_command": "推荐启动命令",
    "manifest_kind": "manifest 类型",
    "active_phase": "维护者参考 phase",
    "entry_mode": "当前入口模式",
    "task_intent": "当前任务意图",
    "target_domain_id": "目标域",
    "checkpoint_status": "当前 checkpoint",
    "output_path": "输出位置",
    "output_dir": "输出位置",
    "program_id": "当前 program",
    "current_line": "当前 line",
    "current_focus": "当前 focus",
}

_HUMAN_TOKEN_FIELDS = {
    "lifecycle_stage",
    "recommended_next_stage",
    "checkpoint_status",
}


def _human_token_label(value: object) -> str | None:
    view = build_status_narration_human_view(None, fallback_current_stage=str(value or "").strip() or None)
    label = view.get("current_stage_label")
    return str(label).strip() or None


def _field_label(field: str) -> str:
    return _HUMAN_FIELD_LABELS.get(field, field)


def _field_value(field: str, value: object) -> object:
    if field in _HUMAN_TOKEN_FIELDS:
        return _human_token_label(value) or value
    return value


def _render_field(field: str, value: object) -> str:
    return f"{_field_label(field)}: {_field_value(field, value)}"


def _render_validate_workspace(payload: dict[str, Any]) -> str:
    lines = [
        _render_field("grant_run_id", payload["grant_run_id"]),
        _render_field("workspace_id", payload["workspace_id"]),
        _render_field("lifecycle_stage", payload["lifecycle_stage"]),
        _render_field("ok", payload["ok"]),
        _render_field("error_count", payload["error_count"]),
    ]
    for item in payload["errors"]:
        lines.append(f"- {item['path']}: {item['message']}")
    return "\n".join(lines)


def _render_summarize_workspace(payload: dict[str, Any]) -> str:
    selected_direction = payload["selected_direction"]["title"] if payload["selected_direction"] is not None else "none"
    selected_question = (
        payload["selected_question"]["core_question"] if payload["selected_question"] is not None else "none"
    )
    active_fit_mapping = (
        payload["active_fit_mapping"]["id"] if payload["active_fit_mapping"] is not None else "none"
    )
    active_draft = payload["active_draft"]["project_title"] if payload["active_draft"] is not None else "none"
    active_critique_verdict = payload["active_critique"]["verdict"] if payload["active_critique"] is not None else "none"
    return "\n".join(
        [
            _render_field("grant_run_id", payload["grant_run_id"]),
            _render_field("workspace_id", payload["workspace_id"]),
            _render_field("mode", payload["mode"]),
            _render_field("lifecycle_stage", payload["lifecycle_stage"]),
            _render_field("selected_direction", selected_direction),
            _render_field("selected_question", selected_question),
            _render_field("active_fit_mapping", active_fit_mapping),
            _render_field("active_draft", active_draft),
            _render_field("active_critique_verdict", active_critique_verdict),
        ]
    )


def _render_grant_intake_audit(payload: dict[str, Any]) -> str:
    audit = payload["grant_intake_audit"]
    lines = [
        _render_field("grant_run_id", payload["grant_run_id"]),
        _render_field("workspace_id", payload["workspace_id"]),
        _render_field("lifecycle_stage", payload["lifecycle_stage"]),
        f"intake_status: {audit['intake_status']}",
        f"当前判断: {audit['summary']}",
    ]
    for item in audit["blocking_gaps"]:
        lines.append(f"- blocker: {item}")
    return "\n".join(lines)


def _render_grant_evidence_grounding(payload: dict[str, Any]) -> str:
    grounding = payload["grant_evidence_grounding"]
    lines = [
        _render_field("grant_run_id", payload["grant_run_id"]),
        _render_field("workspace_id", payload["workspace_id"]),
        _render_field("lifecycle_stage", payload["lifecycle_stage"]),
        f"grounding_status: {grounding['grounding_status']}",
        f"当前判断: {grounding['summary']}",
    ]
    for item in grounding["evidence_gaps"]:
        lines.append(f"- gap: {item}")
    return "\n".join(lines)


def _render_grant_quality_scorecard(payload: dict[str, Any]) -> str:
    scorecard = payload["grant_quality_scorecard"]
    lines = [
        _render_field("grant_run_id", payload["grant_run_id"]),
        _render_field("workspace_id", payload["workspace_id"]),
        _render_field("lifecycle_stage", payload["lifecycle_stage"]),
        f"overall_status: {scorecard['overall_status']}",
        f"overall_score: {scorecard['overall_score']}",
        f"当前判断: {scorecard['summary']}",
    ]
    for item in scorecard["unresolved_hard_issues"]:
        lines.append(f"- hard_issue: {item}")
    return "\n".join(lines)


def _render_grant_quality_closure_dossier(payload: dict[str, Any]) -> str:
    dossier = payload["grant_quality_closure_dossier"]
    lines = [
        _render_field("grant_run_id", payload["grant_run_id"]),
        _render_field("workspace_id", payload["workspace_id"]),
        _render_field("lifecycle_stage", payload["lifecycle_stage"]),
        f"overall_status: {dossier['quality_summary']['overall_status']}",
        f"overall_score: {dossier['quality_summary']['overall_score']}",
        f"closure_package_count: {len(dossier['closure_packages'])}",
        f"当前判断: {dossier['quality_summary']['summary']}",
    ]
    for item in dossier["unclosed_hard_issues"]:
        lines.append(f"- hard_issue: {item}")
    return "\n".join(lines)


def _render_grant_quality_diff(payload: dict[str, Any]) -> str:
    diff = payload["grant_quality_diff"]
    lines = [
        f"current_workspace_id: {diff['current_workspace_id']}",
        f"previous_workspace_id: {diff['previous_workspace_id']}",
        f"overall_progression: {diff['overall_progression']}",
        f"score_delta: {diff['score_delta']}",
    ]
    for item in diff["issue_progress"]["closed_issues"]:
        lines.append(f"- closed_issue: {item}")
    for item in diff["issue_progress"]["remaining_open_issues"]:
        lines.append(f"- remaining_issue: {item}")
    for item in diff["issue_progress"]["newly_opened_issues"]:
        lines.append(f"- new_issue: {item}")
    return "\n".join(lines)


def _render_discover_funding_opportunities(payload: dict[str, Any]) -> str:
    discovery = payload["funding_landscape_discovery"]
    lines = [
        f"discovery_input_id: {payload['discovery_input_id']}",
        f"candidate_count: {discovery['candidate_count']}",
        f"当前判断: {discovery['discovery_summary']['decision']}",
    ]
    for item in discovery["funding_opportunity_pool"]:
        lines.append(f"- candidate: {item['brief_id']}")
    return "\n".join(lines)


def _render_refresh_funding_opportunities_cache(payload: dict[str, Any]) -> str:
    snapshot = payload["cache_snapshot"]
    lines = [
        f"discovery_input_id: {payload['discovery_input_id']}",
        f"cache_path: {payload['cache_path']}",
        f"source_count: {snapshot['source_count']}",
        f"当前判断: cache refreshed",
    ]
    return "\n".join(lines)


def _render_select_project_profile(payload: dict[str, Any]) -> str:
    selection = payload["project_profile_selection"]
    lines = [
        f"selection_input_id: {payload['selection_input_id']}",
        f"推荐 profile: {selection['recommended_project_profile']['profile_label']}",
        f"推荐 funding: {selection['recommended_funding_opportunity']['brief_id']}",
        f"当前判断: {selection['selection_summary']['selected_profile_preset_id']}",
    ]
    for code in selection["selection_summary"]["reason_codes"]:
        lines.append(f"- reason_code: {code}")
    return "\n".join(lines)


def _render_initialize_intake_workspace(payload: dict[str, Any]) -> str:
    lines = [
        f"selection_input_id: {payload['selection_input_id']}",
        f"grant_run_id: {payload['grant_run_id']}",
        f"workspace_id: {payload['workspace_id']}",
        f"lifecycle_stage: {payload['lifecycle_stage']}",
        f"workspace_path: {payload.get('workspace_path') or payload['output_path']}",
        f"推荐 profile: {payload['project_profile_selection']['recommended_project_profile']['profile_label']}",
    ]
    if payload.get("workspace_root"):
        lines.insert(4, f"workspace_root: {payload['workspace_root']}")
    return "\n".join(lines)


def _render_next_step(payload: dict[str, Any]) -> str:
    lines = [
        f"grant_run_id: {payload['grant_run_id']}",
        f"workspace_id: {payload['workspace_id']}",
        f"当前阶段: {_human_token_label(payload['current_stage']) or payload['current_stage']}",
        f"下一阶段: {_human_token_label(payload['recommended_stage']) or payload['recommended_stage']}",
        f"当前判断: {payload['reason']}",
    ]
    for action in payload["actions"]:
        lines.append(f"- 建议动作: {action}")
    return "\n".join(lines)


def _render_critique_summary(payload: dict[str, Any]) -> str:
    lines = [
        _render_field("grant_run_id", payload["grant_run_id"]),
        _render_field("workspace_id", payload["workspace_id"]),
        _render_field("critique_id", payload["critique_id"]),
        _render_field("draft_id", payload["draft_id"]),
        _render_field("verdict", payload["verdict"]),
        _render_field("overall_diagnosis", payload["overall_diagnosis"]),
        _render_field("recommended_next_stage", payload["recommended_next_stage"]),
    ]
    for item in payload["blocking_issues"]:
        lines.append(f"- {item}")
    return "\n".join(lines)


def _render_stage_route_report(payload: dict[str, Any]) -> str:
    critique_summary = payload["route"].get("critique_summary")
    critique_verdict = critique_summary["verdict"] if isinstance(critique_summary, dict) else "n/a"
    lifecycle_stage = payload["lifecycle_stage"]
    recommended_stage = payload["route"]["next_step"]["recommended_stage"]
    checkpoint_status = payload["verification_checkpoint"]["checkpoint_status"]
    lines = [
        f"grant_run_id: {payload['grant_run_id']}",
        f"workspace_id: {payload['workspace_id']}",
        f"当前阶段: {_human_token_label(lifecycle_stage) or lifecycle_stage}",
        f"下一阶段: {_human_token_label(recommended_stage) or recommended_stage}",
        f"当前 checkpoint: {_human_token_label(checkpoint_status) or checkpoint_status}",
        f"当前判断: 批注结论 {critique_verdict}",
    ]
    return "\n".join(lines)


def _render_build_artifact_bundle(payload: dict[str, Any]) -> str:
    bundle = payload["bundle"]
    lines = [
        f"grant_run_id: {payload['grant_run_id']}",
        f"workspace_id: {payload['workspace_id']}",
        f"draft_id: {payload['draft_id']}",
        f"lifecycle_stage: {payload['lifecycle_stage']}",
        f"output_path: {payload['output_path']}",
        f"bundle_kind: {bundle['bundle_kind']}",
        f"outline_count: {bundle['bundle_summary']['outline_count']}",
        f"section_count: {bundle['bundle_summary']['section_count']}",
    ]
    return "\n".join(lines)


def _render_execute_direction_screening_pass(payload: dict[str, Any]) -> str:
    lines = [
        f"grant_run_id: {payload['grant_run_id']}",
        f"workspace_id: {payload['workspace_id']}",
        f"draft_id: {payload['draft_id']}",
        f"lifecycle_stage: {payload['lifecycle_stage']}",
        f"output_path: {payload['output_path']}",
    ]
    return "\n".join(lines)


def _render_execute_critique_pass(payload: dict[str, Any]) -> str:
    critique_execution = payload["critique_execution"]
    executor = critique_execution.get("executor", {})
    lines = [
        f"grant_run_id: {payload['grant_run_id']}",
        f"workspace_id: {payload['workspace_id']}",
        f"draft_id: {payload['draft_id']}",
        f"lifecycle_stage: {payload['lifecycle_stage']}",
        f"output_path: {payload['output_path']}",
        f"executor_kind: {executor.get('kind')}",
        f"critique_id: {critique_execution['critique_id']}",
        f"active_revision_plan_id: {critique_execution['active_revision_plan_id']}",
        f"verdict: {critique_execution['verdict']}",
    ]
    if executor.get("mode"):
        lines.append(f"executor_mode: {executor['mode']}")
    if executor.get("session_id"):
        lines.append(f"executor_session_id: {executor['session_id']}")
    return "\n".join(lines)


def _render_execute_critique_revision_loop(payload: dict[str, Any]) -> str:
    loop_report = payload["loop_report"]
    lines = [
        f"grant_run_id: {payload['grant_run_id']}",
        f"workspace_id: {payload['workspace_id']}",
        f"draft_id: {payload['draft_id']}",
        f"lifecycle_stage: {payload['lifecycle_stage']}",
        f"loop_status: {loop_report['loop_status']}",
        f"termination_reason: {loop_report['termination_reason']}",
        f"completed_rounds: {loop_report['completed_rounds']}",
        f"output_dir: {payload['output_dir']}",
    ]
    return "\n".join(lines)


def _render_execute_authoring_mainline_loop(payload: dict[str, Any]) -> str:
    loop_report = payload["mainline_loop_report"]
    lines = [
        f"grant_run_id: {payload['grant_run_id']}",
        f"workspace_id: {payload['workspace_id']}",
        f"draft_id: {payload['draft_id']}",
        f"lifecycle_stage: {payload['lifecycle_stage']}",
        f"loop_status: {loop_report['loop_status']}",
        f"termination_reason: {loop_report['termination_reason']}",
        f"completed_cycles: {loop_report['completed_cycles']}",
        f"output_dir: {payload['output_dir']}",
    ]
    return "\n".join(lines)


def _render_execute_revision_pass(payload: dict[str, Any]) -> str:
    revision_execution = payload["revision_execution"]
    lines = [
        f"grant_run_id: {payload['grant_run_id']}",
        f"workspace_id: {payload['workspace_id']}",
        f"draft_id: {payload['draft_id']}",
        f"lifecycle_stage: {payload['lifecycle_stage']}",
        f"output_path: {payload['output_path']}",
        f"active_revision_plan_id: {revision_execution['active_revision_plan_id']}",
        f"post_revision_version_label: {revision_execution['post_revision_version_label']}",
    ]
    return "\n".join(lines)


def _render_build_final_package(payload: dict[str, Any]) -> str:
    final_package = payload["final_package"]
    lines = [
        f"grant_run_id: {payload['grant_run_id']}",
        f"workspace_id: {payload['workspace_id']}",
        f"draft_id: {payload['draft_id']}",
        f"lifecycle_stage: {payload['lifecycle_stage']}",
        f"output_path: {payload['output_path']}",
        f"package_kind: {final_package['package_kind']}",
        f"checkpoint_status: {final_package['checkpoint_summary']['checkpoint_status']}",
    ]
    return "\n".join(lines)


def _render_build_hosted_contract_bundle(payload: dict[str, Any]) -> str:
    hosted_contract_bundle = payload["hosted_contract_bundle"]
    lines = [
        f"grant_run_id: {payload['grant_run_id']}",
        f"workspace_id: {payload['workspace_id']}",
        f"draft_id: {payload['draft_id']}",
        f"output_path: {payload['output_path']}",
        f"bundle_kind: {hosted_contract_bundle['bundle_kind']}",
        f"program_id: {hosted_contract_bundle['execution_identity']['program_id']}",
    ]
    return "\n".join(lines)


def _render_build_submission_ready_package(payload: dict[str, Any]) -> str:
    submission_ready_package = payload["submission_ready_package"]
    lines = [
        f"grant_run_id: {payload['grant_run_id']}",
        f"workspace_id: {payload['workspace_id']}",
        f"draft_id: {payload['draft_id']}",
        f"lifecycle_stage: {payload['lifecycle_stage']}",
        f"output_dir: {payload['output_dir']}",
        f"readiness_verdict: {submission_ready_package['readiness_verdict']}",
        f"blocking_issue_count: {submission_ready_package['audit_summary']['blocking_issue_count']}",
    ]
    return "\n".join(lines)


def _render_foundry_series(payload: dict[str, Any]) -> str:
    series = payload["foundry_agent_series"]
    lines = [
        _render_field("command", payload["command"]),
        _render_field("domain_label", series["domain_label"]),
        _render_field("foundry_agent_id", series["foundry_agent_id"]),
        _render_field("series_version", series["version"]),
        _render_field("contract_ref", series["contract_ref"]),
    ]
    for section_key in ("status", "inspect", "interfaces", "validation", "doctor", "peers"):
        section = payload.get(section_key)
        if not isinstance(section, dict):
            continue
        lines.append(f"- {section_key}: {json.dumps(section, ensure_ascii=False, sort_keys=True)}")
    return "\n".join(lines)


_TEXT_RENDERERS: dict[str, Callable[[dict[str, Any]], str]] = {
    'foundry-status': _render_foundry_series,
    'foundry-inspect': _render_foundry_series,
    'foundry-interfaces': _render_foundry_series,
    'foundry-validate': _render_foundry_series,
    'foundry-doctor': _render_foundry_series,
    'foundry-peers': _render_foundry_series,
    'validate-workspace': _render_validate_workspace,
    'summarize-workspace': _render_summarize_workspace,
    'grant-intake-audit': _render_grant_intake_audit,
    'grant-evidence-grounding': _render_grant_evidence_grounding,
    'grant-quality-scorecard': _render_grant_quality_scorecard,
    'grant-quality-closure-dossier': _render_grant_quality_closure_dossier,
    'grant-quality-diff': _render_grant_quality_diff,
    'discover-funding-opportunities': _render_discover_funding_opportunities,
    'refresh-funding-opportunities-cache': _render_refresh_funding_opportunities_cache,
    'select-project-profile': _render_select_project_profile,
    'initialize-intake-workspace': _render_initialize_intake_workspace,
    'next-step': _render_next_step,
    'critique-summary': _render_critique_summary,
    'stage-route-report': _render_stage_route_report,
    'build-artifact-bundle': _render_build_artifact_bundle,
    'execute-direction-screening-pass': _render_execute_direction_screening_pass,
    'execute-question-refinement-pass': _render_execute_direction_screening_pass,
    'execute-argument-building-pass': _render_execute_direction_screening_pass,
    'execute-fit-alignment-pass': _render_execute_direction_screening_pass,
    'execute-outline-pass': _render_execute_direction_screening_pass,
    'execute-drafting-pass': _render_execute_direction_screening_pass,
    'execute-freeze-pass': _render_execute_direction_screening_pass,
    'execute-critique-pass': _render_execute_critique_pass,
    'execute-critique-revision-loop': _render_execute_critique_revision_loop,
    'execute-authoring-mainline-loop': _render_execute_authoring_mainline_loop,
    'execute-revision-pass': _render_execute_revision_pass,
    'build-final-package': _render_build_final_package,
    'build-hosted-contract-bundle': _render_build_hosted_contract_bundle,
    'build-submission-ready-package': _render_build_submission_ready_package,
}


def _render_text(command: str, payload: dict[str, Any]) -> str:
    renderer = _TEXT_RENDERERS.get(command)
    if renderer is None:
        raise ValueError(f"未知命令: {command}")
    return renderer(payload)
