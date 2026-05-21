from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Any

from med_autogrant.grant_autonomy_controller_plan import _build_tranche_history_entry
from med_autogrant.grant_autonomy_report_resume import (
    _build_report,
    _fail_closed_report,
)


@dataclass(frozen=True)
class GrantAutonomyLoopContext:
    request_id: str
    start_mode: str
    goal: dict[str, Any]
    max_rounds_or_cycles: int
    budget_max: int
    initial_blockers: list[str]
    initial_evidence_gaps: list[str]
    action_trace: list[dict[str, Any]]
    reselection_decisions: list[dict[str, Any]]
    rollback_decisions: list[dict[str, Any]]

    def fail_closed_report(
        self,
        *,
        spent_steps: int,
        termination_reason: str,
        completed_cycles: int,
        workspace: dict[str, Any] | None,
        latest_blocker_report: dict[str, Any],
        unresolved_blockers: list[str],
        evidence_gaps: list[str],
        controller_plan: dict[str, Any] | None = None,
        tranche_history: list[dict[str, Any]] | None = None,
        latest_quality_closure_dossier: dict[str, Any] | None = None,
        closure_package_queue: list[dict[str, Any]] | None = None,
        active_closure_package: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        return _fail_closed_report(
            request_id=self.request_id,
            started_from_mode=self.start_mode,
            goal=deepcopy(self.goal),
            max_rounds_or_cycles=self.max_rounds_or_cycles,
            budget_max=self.budget_max,
            spent_steps=spent_steps,
            termination_reason=termination_reason,
            blocker_queue=self.initial_blockers,
            evidence_gap_queue=self.initial_evidence_gaps,
            action_trace=self.action_trace,
            reselection_decisions=self.reselection_decisions,
            rollback_decisions=self.rollback_decisions,
            completed_cycles=completed_cycles,
            final_workspace=workspace,
            blocker_report=latest_blocker_report,
            unresolved_blockers=unresolved_blockers,
            evidence_gaps=evidence_gaps,
            controller_plan=controller_plan,
            tranche_history=tranche_history,
            latest_quality_closure_dossier=latest_quality_closure_dossier,
            closure_package_queue=closure_package_queue,
            active_closure_package=active_closure_package,
        )

    def success_report(
        self,
        *,
        spent_steps: int,
        controller_status: str,
        termination_reason: str,
        completed_cycles: int,
        workspace: dict[str, Any] | None,
        latest_blocker_report: dict[str, Any],
        unresolved_blockers: list[str],
        evidence_gaps: list[str],
        controller_plan: dict[str, Any],
        tranche_history: list[dict[str, Any]],
        latest_quality_closure_dossier: dict[str, Any] | None,
        closure_package_queue: list[dict[str, Any]],
        active_closure_package: dict[str, Any] | None,
    ) -> dict[str, Any]:
        return _build_report(
            request_id=self.request_id,
            started_from_mode=self.start_mode,
            goal=deepcopy(self.goal),
            max_rounds_or_cycles=self.max_rounds_or_cycles,
            budget_max=self.budget_max,
            spent_steps=spent_steps,
            controller_status=controller_status,
            termination_reason=termination_reason,
            blocker_queue=self.initial_blockers,
            evidence_gap_queue=self.initial_evidence_gaps,
            blocker_report=latest_blocker_report,
            unresolved_blockers=unresolved_blockers,
            evidence_gaps=evidence_gaps,
            action_trace=self.action_trace,
            reselection_decisions=self.reselection_decisions,
            rollback_decisions=self.rollback_decisions,
            controller_plan=controller_plan,
            tranche_history=tranche_history,
            completed_cycles=completed_cycles,
            final_workspace=workspace,
            latest_quality_closure_dossier=latest_quality_closure_dossier,
            closure_package_queue=closure_package_queue,
            active_closure_package=active_closure_package,
        )


def append_tranche_history(
    tranche_history: list[dict[str, Any]],
    *,
    cycle: int,
    controller_plan: dict[str, Any],
    quality_status: str,
    unresolved_blockers: list[str],
    evidence_gaps: list[str],
    next_controller_action: str,
    gate_status: str,
    decision_reason: str,
    termination_reason: str,
    latest_quality_closure_dossier: dict[str, Any] | None = None,
    closure_package_queue: list[dict[str, Any]] | None = None,
    active_closure_package: dict[str, Any] | None = None,
) -> None:
    tranche_history.append(
        _build_tranche_history_entry(
            cycle=cycle,
            controller_plan=controller_plan,
            quality_status=quality_status,
            unresolved_blockers=unresolved_blockers,
            evidence_gaps=evidence_gaps,
            next_controller_action=next_controller_action,
            gate_status=gate_status,
            decision_reason=decision_reason,
            termination_reason=termination_reason,
            quality_closure_dossier=latest_quality_closure_dossier,
            closure_package_queue=closure_package_queue,
            active_closure_package=active_closure_package,
        )
    )
