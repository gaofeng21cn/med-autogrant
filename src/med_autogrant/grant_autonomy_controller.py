from __future__ import annotations

from typing import Any, Callable

from med_autogrant.grant_autonomy_loop_shell import run_grant_autonomy_loop
from med_autogrant.grant_autonomy_controller_plan import _normalize_controller_plan
from med_autogrant.grant_autonomy_request import validate_grant_autonomy_request
from med_autogrant.grant_autonomy_start import _resolve_grant_autonomy_start
from med_autogrant.grant_governance_adapter import apply_family_governance_to_controller_plan
from med_autogrant.grant_autonomy_report_resume import _fail_closed_report
from med_autogrant.opl_execution_boundary import require_opl_default_stage_attempt

Discoverer = Callable[[dict[str, Any]], dict[str, Any]]
Selector = Callable[[dict[str, Any]], dict[str, Any]]
Initializer = Callable[[dict[str, Any], dict[str, Any]], dict[str, Any]]
MainlineRunner = Callable[[dict[str, Any]], dict[str, Any]]
QualityEvaluator = Callable[[dict[str, Any]], dict[str, Any]]


def run_grant_autonomy_controller(
    *,
    request: dict[str, Any],
    selector: Selector,
    initializer: Initializer,
    mainline_runner: MainlineRunner,
    quality_evaluator: QualityEvaluator,
    discoverer: Discoverer | None = None,
    opl_stage_attempt: dict[str, Any] | None = None,
) -> dict[str, Any]:
    request_state = validate_grant_autonomy_request(request)
    if not request_state["ok"]:
        return request_state["report"]

    request_id = request_state["request_id"]
    start = request_state["start"]
    start_mode = request_state["start_mode"]
    goal = request_state["goal"]
    goal_target = request_state["goal_target"]
    max_rounds_or_cycles = request_state["max_rounds_or_cycles"]
    budget_max = request_state["budget_max"]
    require_zero_blockers = request_state["require_zero_blockers"]
    require_zero_evidence_gaps = request_state["require_zero_evidence_gaps"]
    controller_plan_input = request_state["controller_plan_input"]
    initial_blockers = request_state["initial_blockers"]
    initial_evidence_gaps = request_state["initial_evidence_gaps"]
    reselection_enabled = request_state["reselection_enabled"]
    rollback_enabled = request_state["rollback_enabled"]
    max_reselections = request_state["max_reselections"]
    max_rollbacks = request_state["max_rollbacks"]

    requested_opl_stage_attempt = (
        opl_stage_attempt if opl_stage_attempt is not None else request.get("opl_stage_attempt")
    )
    boundary = require_opl_default_stage_attempt(
        requested_opl_stage_attempt if isinstance(requested_opl_stage_attempt, dict) else None,
        controller_id="autonomy-controller",
    )
    if not boundary["ok"]:
        return _fail_closed_report(
            request_id=request_id,
            started_from_mode=start_mode,
            goal=goal,
            max_rounds_or_cycles=max_rounds_or_cycles,
            budget_max=budget_max,
            spent_steps=0,
            termination_reason="opl_provider_attempt_required",
            blocker_queue=initial_blockers,
            evidence_gap_queue=initial_evidence_gaps,
            unresolved_blockers=[boundary["typed_blocker"]["typed_blocker_ref"]],
            evidence_gaps=[],
            action_trace=[],
            reselection_decisions=[],
            rollback_decisions=[],
            controller_plan=controller_plan_input if isinstance(controller_plan_input, dict) else None,
            tranche_history=[],
            completed_cycles=0,
            final_workspace={},
        )

    action_trace: list[dict[str, Any]] = []
    reselection_decisions: list[dict[str, Any]] = []
    rollback_decisions: list[dict[str, Any]] = []
    tranche_history: list[dict[str, Any]] = []
    spent_steps = 0
    reselection_count = 0
    rollback_count = 0
    completed_cycles = 0
    latest_blocker_report: dict[str, Any] = {}
    unresolved_blockers = list(initial_blockers)
    evidence_gaps = list(initial_evidence_gaps)
    latest_quality_closure_dossier: dict[str, Any] | None = None
    closure_package_queue: list[dict[str, Any]] = []
    active_closure_package: dict[str, Any] | None = None

    selection_input: dict[str, Any] | None = None
    workspace: dict[str, Any] | None = None
    explicit_controller_plan = isinstance(controller_plan_input, dict)

    start_result = _resolve_grant_autonomy_start(
        request_id=request_id,
        start=start,
        start_mode=start_mode,
        goal=goal,
        max_rounds_or_cycles=max_rounds_or_cycles,
        budget_max=budget_max,
        initial_blockers=initial_blockers,
        initial_evidence_gaps=initial_evidence_gaps,
        action_trace=action_trace,
        reselection_decisions=reselection_decisions,
        rollback_decisions=rollback_decisions,
        tranche_history=tranche_history,
        spent_steps=spent_steps,
        completed_cycles=completed_cycles,
        latest_blocker_report=latest_blocker_report,
        unresolved_blockers=unresolved_blockers,
        evidence_gaps=evidence_gaps,
        latest_quality_closure_dossier=latest_quality_closure_dossier,
        closure_package_queue=closure_package_queue,
        active_closure_package=active_closure_package,
        reselection_count=reselection_count,
        rollback_count=rollback_count,
        selection_input=selection_input,
        workspace=workspace,
        explicit_controller_plan=explicit_controller_plan,
        controller_plan_input=controller_plan_input,
        selector=selector,
        initializer=initializer,
        discoverer=discoverer,
    )
    if not start_result["ok"]:
        return start_result["report"]

    initial_blockers = start_result["initial_blockers"]
    initial_evidence_gaps = start_result["initial_evidence_gaps"]
    action_trace = start_result["action_trace"]
    reselection_decisions = start_result["reselection_decisions"]
    rollback_decisions = start_result["rollback_decisions"]
    tranche_history = start_result["tranche_history"]
    spent_steps = start_result["spent_steps"]
    completed_cycles = start_result["completed_cycles"]
    latest_blocker_report = start_result["latest_blocker_report"]
    unresolved_blockers = start_result["unresolved_blockers"]
    evidence_gaps = start_result["evidence_gaps"]
    latest_quality_closure_dossier = start_result["latest_quality_closure_dossier"]
    closure_package_queue = start_result["closure_package_queue"]
    active_closure_package = start_result["active_closure_package"]
    reselection_count = start_result["reselection_count"]
    rollback_count = start_result["rollback_count"]
    selection_input = start_result["selection_input"]
    workspace = start_result["workspace"]
    explicit_controller_plan = start_result["explicit_controller_plan"]
    controller_plan_input = start_result["controller_plan_input"]
    max_rounds_or_cycles = start_result["max_rounds_or_cycles"]
    budget_max = start_result["budget_max"]

    controller_plan = _normalize_controller_plan(
        controller_plan_input,
        goal=goal,
        require_zero_blockers=require_zero_blockers,
        require_zero_evidence_gaps=require_zero_evidence_gaps,
    )
    controller_plan = apply_family_governance_to_controller_plan(
        controller_plan,
        workspace=workspace,
        explicit_controller_plan=explicit_controller_plan,
    )

    return run_grant_autonomy_loop(
        request_id=request_id,
        start_mode=start_mode,
        goal=goal,
        goal_target=goal_target,
        max_rounds_or_cycles=max_rounds_or_cycles,
        budget_max=budget_max,
        spent_steps=spent_steps,
        initial_blockers=initial_blockers,
        initial_evidence_gaps=initial_evidence_gaps,
        action_trace=action_trace,
        reselection_decisions=reselection_decisions,
        rollback_decisions=rollback_decisions,
        tranche_history=tranche_history,
        completed_cycles=completed_cycles,
        latest_blocker_report=latest_blocker_report,
        unresolved_blockers=unresolved_blockers,
        evidence_gaps=evidence_gaps,
        latest_quality_closure_dossier=latest_quality_closure_dossier,
        closure_package_queue=closure_package_queue,
        active_closure_package=active_closure_package,
        controller_plan=controller_plan,
        selection_input=selection_input,
        workspace=workspace,
        explicit_controller_plan=explicit_controller_plan,
        reselection_enabled=reselection_enabled,
        rollback_enabled=rollback_enabled,
        max_reselections=max_reselections,
        max_rollbacks=max_rollbacks,
        reselection_count=reselection_count,
        rollback_count=rollback_count,
        selector=selector,
        initializer=initializer,
        mainline_runner=mainline_runner,
        quality_evaluator=quality_evaluator,
    )
