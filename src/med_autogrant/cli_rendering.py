from __future__ import annotations

from typing import Any

from med_autogrant.workspace import WorkspaceError, WorkspaceStateError, load_workspace_document
from med_autogrant.public_cli import public_command_label
from opl_harness_shared.status_narration import build_status_narration_human_view



_WORKSPACE_STATUS_LABELS = {
    "attention_required": "需要处理",
    "healthy": "运行正常",
}

_PHASE_STATUS_LABELS = {
    "current": "当前阶段",
    "next": "下一阶段",
    "completed": "已完成",
}

_START_MODE_LABELS = {
    "open_frontdesk": "打开 frontdesk",
    "continue_grant_loop": "继续 grant loop",
    "build_direct_entry": "构建 direct entry",
}

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


def _workspace_status_label(value: object) -> str:
    text = str(value or "").strip()
    if not text:
        return "未知"
    return _WORKSPACE_STATUS_LABELS.get(text, text)


def _phase_status_label(value: object) -> str:
    text = str(value or "").strip()
    if not text:
        return "未知"
    return _PHASE_STATUS_LABELS.get(text, text)


def _start_mode_label(value: object) -> str:
    text = str(value or "").strip()
    if not text:
        return "未命名入口"
    return _START_MODE_LABELS.get(text, text.replace("_", " "))


def _entry_surface_label(value: object) -> str:
    text = str(value or "").strip()
    if not text:
        return "未命名入口"
    public_label = public_command_label(text.replace("_", "-"))
    if public_label != text.replace("_", "-"):
        return public_label
    return text.replace("_", " ")


def _field_label(field: str) -> str:
    return _HUMAN_FIELD_LABELS.get(field, field)


def _field_value(field: str, value: object) -> object:
    if field in _HUMAN_TOKEN_FIELDS:
        return _human_token_label(value) or value
    return value


def _render_field(field: str, value: object) -> str:
    return f"{_field_label(field)}: {_field_value(field, value)}"


def _render_shell_name(name: str) -> str:
    if name in _HUMAN_FIELD_LABELS:
        return _field_label(name)
    public_label = public_command_label(name.replace("_", "-"))
    if public_label != name.replace("_", "-"):
        return public_label
    return name

def _render_text(command: str, payload: dict[str, Any]) -> str:
    if command == "validate-workspace":
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

    if command == "summarize-workspace":
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

    if command == "grant-intake-audit":
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

    if command == "grant-evidence-grounding":
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

    if command == "grant-quality-scorecard":
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

    if command == "grant-quality-closure-dossier":
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

    if command == "grant-quality-diff":
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

    if command == "discover-funding-opportunities":
        discovery = payload["funding_landscape_discovery"]
        lines = [
            f"discovery_input_id: {payload['discovery_input_id']}",
            f"candidate_count: {discovery['candidate_count']}",
            f"当前判断: {discovery['discovery_summary']['decision']}",
        ]
        for item in discovery["funding_opportunity_pool"]:
            lines.append(f"- candidate: {item['brief_id']}")
        return "\n".join(lines)

    if command == "refresh-funding-opportunities-cache":
        snapshot = payload["cache_snapshot"]
        lines = [
            f"discovery_input_id: {payload['discovery_input_id']}",
            f"cache_path: {payload['cache_path']}",
            f"source_count: {snapshot['source_count']}",
            f"当前判断: cache refreshed",
        ]
        return "\n".join(lines)

    if command == "select-project-profile":
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

    if command == "initialize-intake-workspace":
        lines = [
            f"selection_input_id: {payload['selection_input_id']}",
            f"grant_run_id: {payload['grant_run_id']}",
            f"workspace_id: {payload['workspace_id']}",
            f"lifecycle_stage: {payload['lifecycle_stage']}",
            f"output_path: {payload['output_path']}",
            f"推荐 profile: {payload['project_profile_selection']['recommended_project_profile']['profile_label']}",
        ]
        return "\n".join(lines)

    if command == "next-step":
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

    if command == "critique-summary":
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

    if command == "stage-route-report":
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

    if command == "grant-progress":
        projection = payload["progress_projection"]
        human_view = build_status_narration_human_view(
            projection,
            fallback_current_stage=projection.get("current_stage"),
            fallback_latest_update=projection.get("current_stage_summary"),
            fallback_next_step=projection.get("next_system_action"),
            fallback_blockers=projection.get("current_blockers") or [],
        )
        lines = [
            f"grant_run_id: {payload['grant_run_id']}",
            f"workspace_id: {payload['workspace_id']}",
            f"draft_id: {payload['draft_id']}",
            f"lifecycle_stage: {payload['lifecycle_stage']}",
            f"checkpoint_status: {projection['checkpoint_status']}",
            f"当前阶段: {human_view.get('current_stage_label') or projection['current_stage']}",
            f"当前判断: {human_view.get('status_summary') or human_view.get('latest_update') or projection['current_stage_summary']}",
            f"下一步建议: {human_view.get('next_step') or projection['next_system_action']}",
        ]
        for item in projection["current_blockers"]:
            lines.append(f"- blocker: {item}")
        return "\n".join(lines)

    if command == "grant-cockpit":
        cockpit = payload["grant_cockpit"]
        workspace_alerts = list(cockpit["workspace_alerts"])
        lines = [
            f"grant_run_id: {payload['grant_run_id']}",
            f"workspace_id: {payload['workspace_id']}",
            f"draft_id: {payload['draft_id']}",
            f"lifecycle_stage: {payload['lifecycle_stage']}",
            f"当前状态: {_workspace_status_label(cockpit['workspace_status'])}",
        ]
        if workspace_alerts:
            lines.append(f"当前判断: {workspace_alerts[0]}")
        for item in workspace_alerts[1:]:
            lines.append(f"- 关注项: {item}")
        for name, command_line in cockpit["commands"].items():
            lines.append(f"- 可用命令 {name}: {command_line}")
        return "\n".join(lines)

    if command == "mainline-status":
        current_line = payload["current_line"]
        current_focus = payload["current_focus"]
        lines = [
            _render_field("program_id", payload["program_id"]),
            _render_field("current_line", current_line["current_owner_line"]),
            _render_field("current_focus", current_focus["summary"]),
        ]
        for item in current_focus["focus_items"]:
            lines.append(f"- 当前 focus 项: {item}")
        for item in payload["completed_records"]:
            lines.append(f"- 已完成 record {item['record_id']}: {item['summary']}")
        for item in payload["remaining_gaps"]:
            lines.append(f"- 剩余 gap: {item}")
        return "\n".join(lines)

    if command == "mainline-phase":
        reference = payload["maintainer_reference"]
        phase = reference["record_detail"]
        lines = [
            f"当前 line: {payload['current_line']['current_owner_line']}",
            f"维护参考 selector: {reference['selector']}",
            f"维护参考记录: {phase['phase_id']}",
            f"记录名称: {phase['phase_name']}",
            f"记录状态: {_phase_status_label(phase['status'])}",
        ]
        for item in phase["entry_points"]:
            lines.append(f"- 可用入口 {_entry_surface_label(item['name'])}: {item['command']}")
        return "\n".join(lines)

    if command == "grant-direct-entry":
        direct_entry = payload["grant_direct_entry"]
        lines = [
            f"grant_run_id: {payload['grant_run_id']}",
            f"workspace_id: {payload['workspace_id']}",
            f"draft_id: {payload['draft_id']}",
            f"当前阶段: {_human_token_label(payload['lifecycle_stage']) or payload['lifecycle_stage']}",
            f"task_intent: {direct_entry['task_intent']}",
            f"当前状态: {_workspace_status_label(direct_entry['workspace_status'])}",
            (
                f"推荐执行路径: "
                f"{_human_token_label(direct_entry['recommended_executor_route']['route_id']) or direct_entry['recommended_executor_route']['route_id']}"
            ),
        ]
        workspace_alerts = list(direct_entry["workspace_alerts"])
        if workspace_alerts:
            lines.append(f"当前判断: {workspace_alerts[0]}")
        for item in workspace_alerts[1:]:
            lines.append(f"- 关注项: {item}")
        return "\n".join(lines)

    if command == "grant-user-loop":
        user_loop = payload["grant_user_loop"]
        focus_items = list(user_loop["mainline_snapshot"]["next_focus"])
        lines = [
            _render_field("grant_run_id", payload["grant_run_id"]),
            _render_field("workspace_id", payload["workspace_id"]),
            _render_field("draft_id", payload["draft_id"]),
            _render_field("lifecycle_stage", payload["lifecycle_stage"]),
            _render_field("current_focus", focus_items[0] if focus_items else user_loop["mainline_snapshot"]["active_tranche"]),
            _render_field("next_action", user_loop["next_action"]["action_kind"]),
        ]
        if user_loop["next_action"]["command"] is not None:
            lines.append(f"- {_field_label('run_recommended_route')}: {user_loop['next_action']['command']}")
        for name, command_line in user_loop["user_loop"].items():
            if command_line is not None:
                lines.append(f"- {_render_shell_name(name)}: {command_line}")
        return "\n".join(lines)

    if command == "product-entry-manifest":
        manifest = payload["product_entry_manifest"]
        lines = [
            _render_field("grant_run_id", payload["grant_run_id"]),
            _render_field("workspace_id", payload["workspace_id"]),
            _render_field("draft_id", payload["draft_id"]),
            _render_field("lifecycle_stage", payload["lifecycle_stage"]),
            _render_field("manifest_kind", manifest["manifest_kind"]),
            _render_field("current_line", manifest["runtime"]["current_owner_line"]),
            _render_field("current_focus", manifest["repo_mainline"]["phase_summary"]),
            _render_field("active_phase", manifest["repo_mainline"]["active_phase"]),
        ]
        for name, item in manifest["product_entry_shell"].items():
            lines.append(f"- {_render_shell_name(name)}: {item['command']}")
        return "\n".join(lines)

    if command == "product-frontdesk":
        frontdesk = payload["product_frontdesk"]
        lines = [
            f"grant_run_id: {payload['grant_run_id']}",
            f"workspace_id: {payload['workspace_id']}",
            f"draft_id: {payload['draft_id']}",
            f"当前阶段: {_human_token_label(payload['lifecycle_stage']) or payload['lifecycle_stage']}",
            f"当前判断: {frontdesk['product_entry_status']['summary']}",
            f"前台入口命令: {frontdesk['summary']['frontdesk_command']}",
            f"推荐继续命令: {frontdesk['summary']['recommended_command']}",
            f"当前 loop 命令: {frontdesk['summary']['operator_loop_command']}",
        ]
        for name, item in frontdesk["entry_surfaces"].items():
            lines.append(f"- 可用入口 {name}: {item['command']}")
        return "\n".join(lines)

    if command == "product-preflight":
        preflight = payload["product_entry_preflight"]
        lines = [
            _render_field("grant_run_id", payload["grant_run_id"]),
            _render_field("workspace_id", payload["workspace_id"]),
            _render_field("draft_id", payload["draft_id"]),
            _render_field("lifecycle_stage", payload["lifecycle_stage"]),
            _render_field("ready_to_try_now", preflight["ready_to_try_now"]),
            _render_field("recommended_check_command", preflight["recommended_check_command"]),
            _render_field("recommended_start_command", preflight["recommended_start_command"]),
        ]
        for item in preflight["checks"]:
            lines.append(
                f"- {item['check_id']}: {item['status']} (blocking={item['blocking']}) -> {item['command']}"
            )
        return "\n".join(lines)

    if command == "product-start":
        start_surface = payload["product_entry_start"]
        lines = [
            f"grant_run_id: {payload['grant_run_id']}",
            f"workspace_id: {payload['workspace_id']}",
            f"draft_id: {payload['draft_id']}",
            f"当前阶段: {_human_token_label(payload['lifecycle_stage']) or payload['lifecycle_stage']}",
            f"建议入口: {_start_mode_label(start_surface['recommended_mode_id'])}",
        ]
        for mode in start_surface["modes"]:
            lines.append(f"- 可用入口 {_start_mode_label(mode['mode_id'])}: {mode['command']}")
        return "\n".join(lines)

    if command == "probe-upstream-hermes":
        lines = [
            f"package_version: {payload['package_version']}",
            f"hermes_command: {payload['hermes_command']}",
            f"runtime_root: {payload['runtime_root']}",
            f"state_db_path: {payload['state_db_path']}",
        ]
        for name, target in payload["entrypoints"].items():
            lines.append(f"- {name}: {target}")
        return "\n".join(lines)

    if command in {"runtime-run", "runtime-resume"}:
        lines = [
            f"grant_run_id: {payload['grant_run_id']}",
            f"workspace_id: {payload['workspace_id']}",
            f"lifecycle_stage: {payload['lifecycle_stage']}",
            f"stop_reason: {payload['stop_reason']['code']}",
            f"checkpoint_status: {payload['stop_reason']['checkpoint_status']}",
            f"recommended_next_stage: {payload['stop_reason']['recommended_next_stage']}",
            f"journal_path: {payload['journal_path']}",
        ]
        return "\n".join(lines)

    if command == "build-artifact-bundle":
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

    if command in {
        "execute-direction-screening-pass",
        "execute-question-refinement-pass",
        "execute-argument-building-pass",
        "execute-fit-alignment-pass",
        "execute-outline-pass",
        "execute-drafting-pass",
        "execute-freeze-pass",
    }:
        lines = [
            f"grant_run_id: {payload['grant_run_id']}",
            f"workspace_id: {payload['workspace_id']}",
            f"draft_id: {payload['draft_id']}",
            f"lifecycle_stage: {payload['lifecycle_stage']}",
            f"output_path: {payload['output_path']}",
        ]
        return "\n".join(lines)

    if command == "execute-critique-pass":
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

    if command == "execute-critique-revision-loop":
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

    if command == "execute-authoring-mainline-loop":
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

    if command == "execute-grant-autonomy-controller":
        report = payload["grant_autonomy_controller_report"]
        lines = [
            f"controller_status: {report['controller_status']}",
            f"termination_reason: {report['termination_reason']}",
            f"completed_cycles: {report['completed_cycles']}",
            f"unresolved_blockers: {len(report['unresolved_blockers'])}",
            f"evidence_gaps: {len(report['evidence_gaps'])}",
            f"output_dir: {payload['output_dir']}",
        ]
        return "\n".join(lines)

    if command == "execute-revision-pass":
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

    if command == "build-final-package":
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

    if command == "build-hosted-contract-bundle":
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

    if command == "build-submission-ready-package":
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

    if command == "build-product-entry":
        product_entry = payload["product_entry"]
        lines = [
            _render_field("grant_run_id", payload["grant_run_id"]),
            _render_field("workspace_id", payload["workspace_id"]),
            _render_field("draft_id", payload["draft_id"]),
            _render_field("lifecycle_stage", payload["lifecycle_stage"]),
            _render_field("entry_mode", product_entry["entry_mode"]),
            _render_field("task_intent", product_entry["task_intent"]),
            _render_field("target_domain_id", product_entry["target_domain_id"]),
            _render_field("checkpoint_status", product_entry["stage_snapshot"]["checkpoint_status"]),
            _render_field("output_path", payload["output_path"]),
        ]
        return "\n".join(lines)

    raise ValueError(f"未知命令: {command}")


def _extract_workspace_context_for_error(args: Any) -> dict[str, Any]:
    input_path = getattr(args, "input", None)
    if not input_path:
        return {}
    try:
        document = load_workspace_document(input_path)
    except WorkspaceError:
        return {}
    return {
        "grant_run_id": document.get("grant_run_id"),
        "workspace_id": document.get("workspace_id"),
        "lifecycle_stage": document.get("lifecycle_stage"),
    }


def _extract_error_details(exc: WorkspaceError) -> list[dict[str, str]]:
    if not isinstance(exc, WorkspaceStateError):
        return []
    return [
        {
            "path": issue.path,
            "message": issue.message,
        }
        for issue in exc.errors
    ]
