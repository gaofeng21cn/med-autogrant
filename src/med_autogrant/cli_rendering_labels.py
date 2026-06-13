from __future__ import annotations

from opl_harness_shared.status_narration import build_status_narration_human_view

from med_autogrant.public_cli import public_command_label


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
    "open_product_entry": "打开 status",
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
