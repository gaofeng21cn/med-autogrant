from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from med_autogrant.artifact_bundle import build_artifact_bundle_document
from med_autogrant.control_plane import (
    CURRENT_PROGRAM_CONTRACT_RELATIVE_PATH,
    read_current_program_contract as _read_current_program_contract_from_contract,
    read_program_id as _read_program_id_from_contract,
    resolve_current_program_contract_path,
    resolve_runtime_state_root,
    runtime_state_display_path,
)
from med_autogrant.final_package import (
    _validate_required_artifact_bundle_fields,
    build_final_package_document,
)
from med_autogrant.hosted_contract_bundle import (
    SUPPORTED_FINAL_PACKAGE_VERSION,
    _validate_required_final_package_fields,
    build_hosted_contract_bundle_document,
)
from med_autogrant.upstream_hermes import HermesGrantRunLedger
from med_autogrant.revision_executor import build_revision_execution_document
from med_autogrant.route_report import build_stage_route_report
from med_autogrant.stage_router import determine_next_step
from med_autogrant.workspace import (
    WorkspaceError,
    WorkspaceFileError,
    WorkspaceStateError,
    _require_workspace_context,
    build_critique_summary,
    load_workspace_document,
    summarize_workspace_document,
    validate_workspace_document,
)


JOURNAL_VERSION = 1
CURRENT_PROGRAM_RELATIVE_PATH = CURRENT_PROGRAM_CONTRACT_RELATIVE_PATH
EXECUTOR_ROUTING_CONTRACT_VERSION = 1
AUTHOR_SIDE_ROUTE_IDS = (
    "direction_screening",
    "question_refinement",
    "argument_building",
    "fit_alignment",
    "outline",
    "drafting",
    "critique",
    "revision",
    "frozen",
    "artifact_bundle",
    "final_package",
    "hosted_contract_bundle",
)
SERVICE_SAFE_ENTRY_ADAPTER = "MedAutoGrantDomainEntry"
SERVICE_SAFE_ENTRY_SURFACE_KIND = "service-safe-domain-entry-command"
EXECUTOR_ROUTE_OWNER = "med-autogrant"
REVIEW_CONTEXT_STAGES = frozenset({"critique", "revision", "frozen"})
DRAFT_ID_CONTEXT_STAGES = frozenset({"outline", "drafting", "critique", "revision", "frozen"})
PENDING_ROUTE_HANDOFF_REQUIREMENTS: dict[str, dict[str, list[str]]] = {
    "direction_screening": {
        "required_summary_fields": [
            "current_selection.selected_direction_id",
            "selected_direction.id",
            "selected_direction.title",
            "selected_direction.decision_status",
        ],
        "required_gate_fields": ["gates.direction_frozen"],
    },
    "question_refinement": {
        "required_summary_fields": [
            "current_selection.selected_direction_id",
            "current_selection.selected_question_id",
            "selected_direction.id",
            "selected_direction.title",
            "selected_question.id",
            "selected_question.core_question",
            "selected_question.knowledge_boundary",
        ],
        "required_gate_fields": [
            "gates.direction_frozen",
            "gates.scientific_question_frozen",
        ],
    },
    "argument_building": {
        "required_summary_fields": [
            "current_selection.selected_direction_id",
            "current_selection.selected_question_id",
            "selected_direction.id",
            "selected_question.id",
            "selected_question.core_question",
            "active_argument_chain.id",
            "active_argument_chain.necessity_claim",
        ],
        "required_gate_fields": [
            "gates.direction_frozen",
            "gates.scientific_question_frozen",
            "gates.argument_chain_frozen",
        ],
    },
    "fit_alignment": {
        "required_summary_fields": [
            "current_selection.selected_direction_id",
            "current_selection.selected_question_id",
            "current_selection.active_fit_mapping_id",
            "selected_direction.id",
            "selected_question.id",
            "active_argument_chain.id",
            "active_fit_mapping.id",
            "active_fit_mapping.applicant_fit_summary",
            "active_fit_mapping.unique_advantage",
        ],
        "required_gate_fields": [
            "gates.direction_frozen",
            "gates.scientific_question_frozen",
            "gates.argument_chain_frozen",
            "gates.fit_alignment_frozen",
        ],
    },
    "outline": {
        "required_summary_fields": [
            "current_selection.selected_direction_id",
            "current_selection.selected_question_id",
            "current_selection.active_fit_mapping_id",
            "current_selection.active_draft_id",
            "selected_direction.id",
            "selected_question.id",
            "active_argument_chain.id",
            "active_fit_mapping.id",
            "active_draft.id",
            "active_draft.version_label",
            "active_draft.status",
            "active_draft.outline_count",
        ],
        "required_gate_fields": [
            "gates.direction_frozen",
            "gates.scientific_question_frozen",
            "gates.argument_chain_frozen",
            "gates.fit_alignment_frozen",
            "gates.outline_frozen",
        ],
    },
    "drafting": {
        "required_summary_fields": [
            "current_selection.selected_direction_id",
            "current_selection.selected_question_id",
            "current_selection.active_fit_mapping_id",
            "current_selection.active_draft_id",
            "selected_direction.id",
            "selected_question.id",
            "active_argument_chain.id",
            "active_fit_mapping.id",
            "active_draft.id",
            "active_draft.version_label",
            "active_draft.status",
            "active_draft.outline_count",
            "active_draft.section_count",
        ],
        "required_gate_fields": [
            "gates.direction_frozen",
            "gates.scientific_question_frozen",
            "gates.argument_chain_frozen",
            "gates.fit_alignment_frozen",
            "gates.outline_frozen",
        ],
    },
    "critique": {
        "required_summary_fields": [
            "current_selection.selected_direction_id",
            "current_selection.selected_question_id",
            "current_selection.active_fit_mapping_id",
            "current_selection.active_draft_id",
            "current_selection.active_revision_plan_id",
            "selected_direction.id",
            "selected_question.id",
            "active_argument_chain.id",
            "active_fit_mapping.id",
            "active_draft.id",
            "active_draft.version_label",
            "active_draft.status",
            "active_revision_plan.id",
            "active_revision_plan.execution_status",
            "active_critique.id",
            "active_critique.verdict",
            "active_critique.blocking_issue_count",
        ],
        "required_gate_fields": [
            "gates.direction_frozen",
            "gates.scientific_question_frozen",
            "gates.argument_chain_frozen",
            "gates.fit_alignment_frozen",
            "gates.outline_frozen",
            "gates.presubmission_frozen",
        ],
    },
    "frozen": {
        "required_summary_fields": [
            "current_selection.selected_direction_id",
            "current_selection.selected_question_id",
            "current_selection.active_fit_mapping_id",
            "current_selection.active_draft_id",
            "current_selection.active_revision_plan_id",
            "selected_direction.id",
            "selected_question.id",
            "active_argument_chain.id",
            "active_fit_mapping.id",
            "active_draft.id",
            "active_draft.version_label",
            "active_draft.status",
            "active_draft.section_count",
            "active_revision_plan.id",
            "active_revision_plan.execution_status",
            "active_critique.id",
            "active_critique.verdict",
        ],
        "required_gate_fields": [
            "gates.direction_frozen",
            "gates.scientific_question_frozen",
            "gates.argument_chain_frozen",
            "gates.fit_alignment_frozen",
            "gates.outline_frozen",
            "gates.presubmission_frozen",
        ],
    },
}


class LocalRuntimeStateError(WorkspaceError):
    """Local runtime journal/state mismatch。"""


class HermesRuntimeSubstrate:
    """Hermes owns runtime orchestration while MedAutoGrant keeps domain semantics."""

    runtime_owner = "Hermes"

    def describe_topology(self) -> dict[str, Any]:
        return {
            "runtime_owner": self.runtime_owner,
            "default_formal_entry": "CLI",
            "supported_protocol_layer": "MCP",
            "internal_controller_surface": "controller",
            "compatibility_bridge": "Codex-default host-agent runtime",
            "domain_logic_modules": [
                "workspace",
                "stage_router",
                "route_report",
                "revision_executor",
                "artifact_bundle",
                "final_package",
                "hosted_contract_bundle",
            ],
        }

    def validate_workspace(self, *, input_path: str | Path) -> dict[str, Any]:
        document = self._load_workspace(input_path)
        result = validate_workspace_document(document)
        return result.to_dict(document)

    def summarize_workspace(self, *, input_path: str | Path) -> dict[str, Any]:
        document = self._load_workspace(input_path)
        return summarize_workspace_document(document)

    def next_step(self, *, input_path: str | Path) -> dict[str, Any]:
        document = self._load_workspace(input_path)
        return determine_next_step(document)

    def critique_summary(self, *, input_path: str | Path) -> dict[str, Any]:
        document = self._load_workspace(input_path)
        payload = build_critique_summary(document)
        payload["recommended_next_stage"] = determine_next_step(document)["recommended_stage"]
        return payload

    def stage_route_report(self, *, input_path: str | Path) -> dict[str, Any]:
        document = self._load_workspace(input_path)
        return build_stage_route_report(document)

    def run_local(
        self,
        *,
        input_path: str | Path,
        journal_path: str | Path | None = None,
        trigger: str = "run-local",
    ) -> dict[str, Any]:
        resolved_input_path = Path(input_path).expanduser().resolve()
        document = self._load_workspace(resolved_input_path)
        validation = validate_workspace_document(document)
        resolved_journal_path = _resolve_journal_path(document=document, journal_path=journal_path)
        journal = _load_or_initialize_journal(
            journal_path=resolved_journal_path,
            document=document,
            input_path=resolved_input_path,
        )

        if validation.ok:
            route_report = build_stage_route_report(document)
            stop_reason = derive_stop_reason(route_report)
            stage_action_envelope = derive_stage_action_envelope(
                route_report=route_report,
                stop_reason=stop_reason,
                journal_path=resolved_journal_path,
            )
            draft_id = route_report["verification_checkpoint"]["identity"]["draft_id"]
            lifecycle_stage = route_report["lifecycle_stage"]
        else:
            route_report = build_validation_failed_route_report(document=document, validation=validation)
            next_step = route_report["route"]["next_step"]
            stop_reason = {
                "code": "validation_failed",
                "reason": next_step["reason"],
                "current_stage": next_step["current_stage"],
                "recommended_next_stage": next_step["recommended_stage"],
                "checkpoint_status": route_report["checkpoint_status"],
                "requires_human_confirmation": False,
                "forced_rollback_stage": None,
                "forced_rollback_reason": None,
            }
            stage_action_envelope = None
            draft_id = None
            lifecycle_stage = document.get("lifecycle_stage")

        attempt_index = HermesGrantRunLedger().record_attempt(
            grant_run_id=document.get("grant_run_id"),
            workspace_id=document.get("workspace_id"),
            trigger=trigger,
            journal_path=resolved_journal_path,
            lifecycle_stage=lifecycle_stage,
            stop_reason=stop_reason,
            stage_action_envelope=stage_action_envelope,
            route_report=route_report,
        )
        journal = _append_attempt(
            journal=journal,
            attempt_index=attempt_index,
            trigger=trigger,
            lifecycle_stage=lifecycle_stage,
            route_report=route_report,
            stop_reason=stop_reason,
            stage_action_envelope=stage_action_envelope,
        )
        _write_journal(resolved_journal_path, journal)

        payload = {
            "ok": validation.ok,
            "command": trigger,
            "grant_run_id": document.get("grant_run_id"),
            "workspace_id": document.get("workspace_id"),
            "draft_id": draft_id,
            "lifecycle_stage": lifecycle_stage,
            "input_path": str(resolved_input_path),
            "journal_path": str(resolved_journal_path),
            "attempt_index": journal["attempts"][-1]["attempt_index"],
            "stop_reason": stop_reason,
            "stage_action_envelope": stage_action_envelope,
            "route_report": route_report,
            "resume": {
                "command": "resume-local",
                "journal_path": str(resolved_journal_path),
            },
        }
        if not validation.ok:
            payload["error"] = f"validation_failed: {validation.errors[0].path}: {validation.errors[0].message}"
            payload["errors"] = validation.to_dict(document)["errors"]
        return payload

    def resume_local(self, *, journal_path: str | Path) -> dict[str, Any]:
        resolved_journal_path = Path(journal_path).expanduser().resolve()
        journal = _read_journal(resolved_journal_path)
        input_path = journal.get("input_path")
        if not isinstance(input_path, str) or not input_path:
            raise LocalRuntimeStateError(f"journal 缺少 input_path: {resolved_journal_path}")
        return self.run_local(
            input_path=input_path,
            journal_path=resolved_journal_path,
            trigger="resume-local",
        )

    def build_artifact_bundle(
        self,
        *,
        input_path: str | Path,
        output_path: str | Path,
    ) -> dict[str, Any]:
        document = self._load_workspace(input_path)
        bundle = build_artifact_bundle_document(document=document)
        resolved_output_path = Path(output_path).expanduser().resolve()
        _guard_artifact_bundle_output_identity(
            resolved_output_path,
            grant_run_id=bundle["grant_run_id"],
            workspace_id=bundle["workspace_id"],
            draft_id=bundle["draft_id"],
            lifecycle_stage=bundle["lifecycle_stage"],
        )
        _write_artifact_bundle_output(resolved_output_path, bundle)
        return {
            "ok": True,
            "command": "build-artifact-bundle",
            "grant_run_id": bundle["grant_run_id"],
            "workspace_id": bundle["workspace_id"],
            "draft_id": bundle["draft_id"],
            "lifecycle_stage": bundle["lifecycle_stage"],
            "output_path": str(resolved_output_path),
            "bundle": bundle,
        }

    def execute_revision_pass(
        self,
        *,
        input_path: str | Path,
        output_path: str | Path,
    ) -> dict[str, Any]:
        document = self._load_workspace(input_path)
        revision_document = build_revision_execution_document(document=document)
        resolved_output_path = Path(output_path).expanduser().resolve()
        _guard_revision_output_identity(
            resolved_output_path,
            grant_run_id=revision_document["grant_run_id"],
            workspace_id=revision_document["workspace_id"],
            draft_id=revision_document["draft_id"],
            active_revision_plan_id=revision_document["active_revision_plan_id"],
            lifecycle_stage=revision_document["lifecycle_stage"],
        )
        _write_revised_workspace_output(
            resolved_output_path,
            revision_document["revised_workspace"],
        )
        return {
            "ok": True,
            "command": "execute-revision-pass",
            "grant_run_id": revision_document["grant_run_id"],
            "workspace_id": revision_document["workspace_id"],
            "draft_id": revision_document["draft_id"],
            "lifecycle_stage": revision_document["lifecycle_stage"],
            "output_path": str(resolved_output_path),
            "revision_execution": revision_document["revision_execution"],
            "revised_workspace": revision_document["revised_workspace"],
        }

    def build_final_package(
        self,
        *,
        input_path: str | Path,
        artifact_bundle_path: str | Path,
        output_path: str | Path,
    ) -> dict[str, Any]:
        document = self._load_workspace(input_path)
        context = _require_workspace_context(document)
        active_draft = context.active_draft
        artifact_bundle = _read_artifact_bundle(
            artifact_bundle_path,
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

    def build_hosted_contract_bundle(
        self,
        *,
        final_package_path: str | Path,
        output_path: str | Path,
    ) -> dict[str, Any]:
        final_package = _read_final_package(final_package_path)
        current_program_contract = _read_current_program_contract()
        program_id = _read_program_id()
        hosted_contract_bundle = build_hosted_contract_bundle_document(
            final_package=final_package,
            program_id=program_id,
            runtime_substrate_contract=_build_runtime_substrate_contract(
                current_program_contract=current_program_contract,
            ),
            runtime_state_contract=_build_runtime_state_contract(),
            operator_contract=_build_operator_contract(),
        )
        resolved_output_path = Path(output_path).expanduser().resolve()
        _guard_hosted_contract_output_identity(
            resolved_output_path,
            grant_run_id=final_package["grant_run_id"],
            workspace_id=final_package["workspace_id"],
            draft_id=final_package["draft_id"],
            program_id=program_id,
        )
        _write_hosted_contract_bundle_output(resolved_output_path, hosted_contract_bundle)
        return {
            "ok": True,
            "command": "build-hosted-contract-bundle",
            "grant_run_id": final_package["grant_run_id"],
            "workspace_id": final_package["workspace_id"],
            "draft_id": final_package["draft_id"],
            "output_path": str(resolved_output_path),
            "hosted_contract_bundle": hosted_contract_bundle,
        }

    def _load_workspace(self, input_path: str | Path) -> dict[str, Any]:
        return load_workspace_document(Path(input_path).expanduser().resolve())


def build_validation_failed_route_report(
    *,
    document: dict[str, Any],
    validation: Any,
) -> dict[str, Any]:
    lifecycle_stage = document.get("lifecycle_stage")
    validation_payload = validation.to_dict(document)
    reason = validation.errors[0].message if validation.errors else "workspace validation failed"
    checkpoint_status = None
    return {
        "ok": False,
        "grant_run_id": document.get("grant_run_id"),
        "workspace_id": document.get("workspace_id"),
        "lifecycle_stage": lifecycle_stage,
        "route": {
            "validate_workspace": validation_payload,
            "summarize_workspace": None,
            "next_step": {
                "grant_run_id": document.get("grant_run_id"),
                "workspace_id": document.get("workspace_id"),
                "presubmission_frozen": bool(document.get("gates", {}).get("presubmission_frozen")),
                "current_stage": lifecycle_stage,
                "recommended_stage": lifecycle_stage,
                "reason": reason,
                "actions": [],
                "requires_human_confirmation": False,
            },
            "critique_summary": None,
        },
        "checkpoint_status": checkpoint_status,
        "verification_checkpoint": {
            "checkpoint_status": checkpoint_status,
            "validation_ok": False,
            "identity": {
                "grant_run_id": document.get("grant_run_id"),
                "workspace_id": document.get("workspace_id"),
                "draft_id": None,
                "active_revision_plan_id": None,
                "reviewed_revision_plan_id": None,
            },
            "route_alignment": {
                "lifecycle_stage": lifecycle_stage,
                "recommended_next_stage": lifecycle_stage,
                "forced_rollback_stage": None,
                "forced_rollback_reason": None,
                "presubmission_frozen": bool(document.get("gates", {}).get("presubmission_frozen")),
            },
            "review_checkpoint": {
                "critique_id": None,
                "reviewed_revision_evidence": None,
                "blocking_issue_count": None,
            },
        },
    }


def derive_stop_reason(route_report: dict[str, Any]) -> dict[str, Any]:
    next_step = route_report["route"]["next_step"]
    checkpoint = route_report["verification_checkpoint"]
    checkpoint_status = checkpoint["checkpoint_status"]
    route_alignment = checkpoint["route_alignment"]
    forced_rollback_stage = route_alignment.get("forced_rollback_stage")
    forced_rollback_reason = route_alignment.get("forced_rollback_reason")
    requires_human_confirmation = bool(next_step.get("requires_human_confirmation"))

    if checkpoint_status == "submission_frozen":
        code = "presubmission_frozen"
    elif forced_rollback_stage or checkpoint_status == "rollback_required":
        code = "rollback_required"
    elif checkpoint_status == "freeze_ready":
        code = "freeze_ready"
    elif requires_human_confirmation:
        code = "human_confirmation_required"
    else:
        code = "stage_action_required"

    return {
        "code": code,
        "reason": next_step["reason"],
        "current_stage": next_step["current_stage"],
        "recommended_next_stage": next_step["recommended_stage"],
        "checkpoint_status": checkpoint_status,
        "requires_human_confirmation": requires_human_confirmation,
        "forced_rollback_stage": forced_rollback_stage,
        "forced_rollback_reason": forced_rollback_reason,
    }


def derive_stage_action_envelope(
    *,
    route_report: dict[str, Any],
    stop_reason: dict[str, Any],
    journal_path: Path,
) -> dict[str, Any] | None:
    if stop_reason.get("code") != "stage_action_required":
        return None

    summary = route_report["route"]["summarize_workspace"]
    next_step = route_report["route"]["next_step"]
    checkpoint = route_report["verification_checkpoint"]
    selection = summary.get("current_selection") or {}
    actions = next_step.get("actions") or []

    return {
        "envelope_version": 1,
        "status": "action_required",
        "grant_run_id": route_report["grant_run_id"],
        "workspace_id": route_report["workspace_id"],
        "draft_id": checkpoint["identity"]["draft_id"],
        "current_stage": next_step["current_stage"],
        "recommended_next_stage": next_step["recommended_stage"],
        "checkpoint_status": checkpoint["checkpoint_status"],
        "requires_human_confirmation": bool(next_step.get("requires_human_confirmation")),
        "selection": {
            "selected_direction_id": selection.get("selected_direction_id"),
            "selected_question_id": selection.get("selected_question_id"),
            "active_fit_mapping_id": selection.get("active_fit_mapping_id"),
            "active_draft_id": selection.get("active_draft_id"),
            "active_revision_plan_id": selection.get("active_revision_plan_id"),
        },
        "action_items": [
            {
                "index": index,
                "instruction": instruction,
            }
            for index, instruction in enumerate(actions, start=1)
        ],
        "route_reason": next_step["reason"],
        "executor_routing_contract": _build_executor_routing_contract(
            current_stage=next_step["current_stage"],
            recommended_next_stage=next_step["recommended_stage"],
        ),
        "resume_decision": {
            "command": "resume-local",
            "journal_path": str(journal_path),
            "append_attempt": True,
            "reuse_grant_run_id": True,
        },
    }


def _resolve_journal_path(*, document: dict[str, Any], journal_path: str | Path | None) -> Path:
    if journal_path is not None:
        return Path(journal_path).expanduser().resolve()
    grant_run_id = document.get("grant_run_id")
    if not isinstance(grant_run_id, str) or not grant_run_id:
        raise LocalRuntimeStateError("workspace 缺少 grant_run_id，无法推导默认 journal 路径。")
    return (_default_journal_root() / f"{grant_run_id}.json").resolve()


def _default_journal_root() -> Path:
    return resolve_runtime_state_root() / "sessions"


def _read_journal(journal_path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(journal_path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise WorkspaceFileError(f"未找到 journal 文件: {journal_path}") from exc
    except json.JSONDecodeError as exc:
        raise WorkspaceFileError(f"journal JSON 解析失败: {journal_path}") from exc
    if not isinstance(payload, dict):
        raise WorkspaceFileError(f"journal 顶层必须是 JSON object: {journal_path}")
    return payload


def _load_or_initialize_journal(
    *,
    journal_path: Path,
    document: dict[str, Any],
    input_path: Path,
) -> dict[str, Any]:
    if not journal_path.exists():
        return {
            "journal_version": JOURNAL_VERSION,
            "grant_run_id": document.get("grant_run_id"),
            "workspace_id": document.get("workspace_id"),
            "input_path": str(input_path),
            "latest_stop_reason": None,
            "latest_stage_action_envelope": None,
            "latest_route_report": None,
            "attempts": [],
        }

    journal = _read_journal(journal_path)
    if journal.get("grant_run_id") != document.get("grant_run_id"):
        raise LocalRuntimeStateError(
            f"journal grant_run_id 不匹配: {journal_path} -> {journal.get('grant_run_id')} != {document.get('grant_run_id')}"
        )
    if journal.get("workspace_id") != document.get("workspace_id"):
        raise LocalRuntimeStateError(
            f"journal workspace_id 不匹配: {journal_path} -> {journal.get('workspace_id')} != {document.get('workspace_id')}"
        )
    if journal.get("input_path") != str(input_path):
        raise LocalRuntimeStateError(
            f"journal input_path 不匹配: {journal_path} -> {journal.get('input_path')} != {input_path}"
        )
    attempts = journal.get("attempts")
    if not isinstance(attempts, list):
        raise LocalRuntimeStateError(f"journal attempts 不是 list: {journal_path}")
    return journal


def _append_attempt(
    *,
    journal: dict[str, Any],
    attempt_index: int,
    trigger: str,
    lifecycle_stage: str | None,
    route_report: dict[str, Any],
    stop_reason: dict[str, Any],
    stage_action_envelope: dict[str, Any] | None,
) -> dict[str, Any]:
    attempts = journal.setdefault("attempts", [])
    checkpoint_status = stop_reason.get("checkpoint_status")
    attempts.append(
        {
            "attempt_index": attempt_index,
            "trigger": trigger,
            "timestamp": datetime.now(UTC).isoformat(),
            "lifecycle_stage": lifecycle_stage,
            "checkpoint_status": checkpoint_status,
            "stop_reason": stop_reason,
            "stage_action_envelope": stage_action_envelope,
        }
    )
    journal["latest_stop_reason"] = stop_reason
    journal["latest_stage_action_envelope"] = stage_action_envelope
    journal["latest_route_report"] = route_report
    return journal


def _write_journal(journal_path: Path, journal: dict[str, Any]) -> None:
    journal_path.parent.mkdir(parents=True, exist_ok=True)
    journal_path.write_text(json.dumps(journal, ensure_ascii=False, indent=2), encoding="utf-8")


def _guard_artifact_bundle_output_identity(
    output_path: Path,
    *,
    grant_run_id: str,
    workspace_id: str,
    draft_id: str,
    lifecycle_stage: str,
) -> None:
    if not output_path.exists():
        return

    try:
        existing_payload = json.loads(output_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise WorkspaceStateError(
            f"bundle output identity 不匹配: {output_path} 已存在且不是可校验的 JSON object。",
            errors=[],
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        ) from exc
    except OSError as exc:
        raise WorkspaceFileError(f"读取 bundle output 失败: {output_path}") from exc

    if not isinstance(existing_payload, dict):
        raise WorkspaceStateError(
            f"bundle output identity 不匹配: {output_path} 已存在且顶层不是 JSON object。",
            errors=[],
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )

    same_identity = (
        existing_payload.get("grant_run_id") == grant_run_id
        and existing_payload.get("workspace_id") == workspace_id
        and existing_payload.get("draft_id") == draft_id
    )
    if same_identity:
        return

    raise WorkspaceStateError(
        (
            "bundle output identity 不匹配: "
            f"{output_path} -> "
            f"{existing_payload.get('grant_run_id')}/{existing_payload.get('workspace_id')}/{existing_payload.get('draft_id')} "
            f"!= {grant_run_id}/{workspace_id}/{draft_id}"
        ),
        errors=[],
        grant_run_id=grant_run_id,
        workspace_id=workspace_id,
        lifecycle_stage=lifecycle_stage,
    )


def _guard_revision_output_identity(
    output_path: Path,
    *,
    grant_run_id: str,
    workspace_id: str,
    draft_id: str,
    active_revision_plan_id: str,
    lifecycle_stage: str | None,
) -> None:
    if not output_path.exists():
        return

    try:
        existing_payload = json.loads(output_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise WorkspaceStateError(
            f"revision output identity 不匹配: {output_path} 已存在且不是可校验的 JSON object。",
            errors=[],
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        ) from exc
    except OSError as exc:
        raise WorkspaceFileError(f"读取 revised workspace output 失败: {output_path}") from exc

    if not isinstance(existing_payload, dict):
        raise WorkspaceStateError(
            f"revision output identity 不匹配: {output_path} 已存在且顶层不是 JSON object。",
            errors=[],
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )

    existing_grant_run_id = existing_payload.get("grant_run_id")
    existing_workspace_id = existing_payload.get("workspace_id")
    existing_draft_id = existing_payload.get("draft_id")
    if existing_draft_id is None:
        current_selection = existing_payload.get("current_selection")
        if isinstance(current_selection, dict):
            existing_draft_id = current_selection.get("active_draft_id")

    existing_active_revision_plan_id = None
    current_selection = existing_payload.get("current_selection")
    if isinstance(current_selection, dict):
        existing_active_revision_plan_id = current_selection.get("active_revision_plan_id")
    if existing_active_revision_plan_id is None:
        revision_execution = existing_payload.get("revision_execution")
        if isinstance(revision_execution, dict):
            existing_active_revision_plan_id = revision_execution.get("active_revision_plan_id")

    same_identity = (
        existing_grant_run_id == grant_run_id
        and existing_workspace_id == workspace_id
        and existing_draft_id == draft_id
        and existing_active_revision_plan_id == active_revision_plan_id
    )
    if same_identity:
        return

    raise WorkspaceStateError(
        (
            "revision output identity 不匹配: "
            f"{output_path} -> "
            f"{existing_grant_run_id}/{existing_workspace_id}/{existing_draft_id}/{existing_active_revision_plan_id} "
            f"!= {grant_run_id}/{workspace_id}/{draft_id}/{active_revision_plan_id}"
        ),
        errors=[],
        grant_run_id=grant_run_id,
        workspace_id=workspace_id,
        lifecycle_stage=lifecycle_stage,
    )


def _read_artifact_bundle(
    artifact_bundle_path: str | Path,
    *,
    grant_run_id: str,
    workspace_id: str,
    draft_id: str,
    lifecycle_stage: str | None,
) -> dict[str, Any]:
    resolved_bundle_path = Path(artifact_bundle_path).expanduser().resolve()
    try:
        artifact_bundle = json.loads(resolved_bundle_path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise WorkspaceFileError(f"未找到 artifact bundle 文件: {resolved_bundle_path}") from exc
    except json.JSONDecodeError as exc:
        raise WorkspaceFileError(f"artifact bundle JSON 解析失败: {resolved_bundle_path}") from exc

    if not isinstance(artifact_bundle, dict):
        raise WorkspaceStateError(
            f"artifact bundle 顶层必须是 JSON object: {resolved_bundle_path}",
            errors=[],
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )

    if artifact_bundle.get("bundle_kind") != "artifact_bundle":
        raise WorkspaceStateError(
            f"artifact bundle kind 非法: {artifact_bundle.get('bundle_kind')}",
            errors=[],
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )

    if (
        artifact_bundle.get("grant_run_id") != grant_run_id
        or artifact_bundle.get("workspace_id") != workspace_id
        or artifact_bundle.get("draft_id") != draft_id
    ):
        raise WorkspaceStateError(
            (
                "artifact bundle identity 不匹配: "
                f"{artifact_bundle.get('grant_run_id')}/{artifact_bundle.get('workspace_id')}/{artifact_bundle.get('draft_id')} "
                f"!= {grant_run_id}/{workspace_id}/{draft_id}"
            ),
            errors=[],
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )

    _validate_required_artifact_bundle_fields(
        artifact_bundle,
        grant_run_id=grant_run_id,
        workspace_id=workspace_id,
        lifecycle_stage=lifecycle_stage,
    )
    return artifact_bundle


def _read_final_package(final_package_path: str | Path) -> dict[str, Any]:
    resolved_final_package_path = Path(final_package_path).expanduser().resolve()
    try:
        final_package = json.loads(resolved_final_package_path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise WorkspaceFileError(f"未找到 final package 文件: {resolved_final_package_path}") from exc
    except json.JSONDecodeError as exc:
        raise WorkspaceFileError(f"final package JSON 解析失败: {resolved_final_package_path}") from exc

    if not isinstance(final_package, dict):
        raise WorkspaceStateError(f"final package 顶层必须是 JSON object: {resolved_final_package_path}")

    if final_package.get("package_kind") != "final_package":
        raise WorkspaceStateError(f"final package kind 非法: {final_package.get('package_kind')}")

    required_fields = (
        "package_version",
        "grant_run_id",
        "workspace_id",
        "draft_id",
        "lifecycle_stage",
        "freeze_manifest",
        "lineage",
        "checkpoint_summary",
    )
    for field in required_fields:
        if field not in final_package:
            raise WorkspaceStateError(f"final package 缺少字段: {field}")

    package_version = final_package.get("package_version")
    if not isinstance(package_version, int) or package_version != SUPPORTED_FINAL_PACKAGE_VERSION:
        raise WorkspaceStateError("final package 缺少字段: package_version")

    _validate_required_final_package_fields(final_package)
    return final_package


def _read_program_id(*, repo_root: Path | None = None) -> str:
    return _read_program_id_from_contract(repo_root=repo_root)


def _read_current_program_contract(*, repo_root: Path | None = None) -> dict[str, Any]:
    return _read_current_program_contract_from_contract(repo_root=repo_root)


def _build_executor_routing_contract(
    *,
    current_stage: str,
    recommended_next_stage: str,
    include_route_catalog: bool = False,
) -> dict[str, Any]:
    contract = {
        "contract_version": EXECUTOR_ROUTING_CONTRACT_VERSION,
        "current_stage_route": _build_stage_route_contract(
            current_stage,
            source_stage=current_stage,
        ),
        "recommended_executor_route": _build_stage_route_contract(
            recommended_next_stage,
            source_stage=current_stage,
        ),
    }
    if include_route_catalog:
        contract["author_side_route_catalog"] = [
            _build_author_side_route_contract(route_id, source_stage=route_id)
            for route_id in AUTHOR_SIDE_ROUTE_IDS
        ]
    return contract


def _build_stage_route_contract(stage: str, *, source_stage: str) -> dict[str, Any]:
    resolved_stage = _require_nonempty_route_id(stage, context="executor routing stage")
    if resolved_stage == "revision":
        return _build_author_side_route_contract("revision", source_stage=source_stage)
    if resolved_stage == "critique":
        return _build_author_side_route_contract("critique", source_stage=source_stage)
    return _build_pending_route_contract(resolved_stage, source_stage=source_stage)


def _build_author_side_route_contract(route_id: str, *, source_stage: str) -> dict[str, Any]:
    resolved_route_id = _require_nonempty_route_id(route_id, context="executor routing route")
    execution_command = {
        "revision": "execute-revision-pass",
        "artifact_bundle": "build-artifact-bundle",
        "final_package": "build-final-package",
        "hosted_contract_bundle": "build-hosted-contract-bundle",
    }.get(resolved_route_id)
    if execution_command is None:
        return _build_pending_route_contract(
            resolved_route_id,
            source_stage=source_stage,
        )
    return {
        "route_id": resolved_route_id,
        "route_status": "landed",
        "executor_owner": EXECUTOR_ROUTE_OWNER,
        "execution_surface": {
            "surface_kind": SERVICE_SAFE_ENTRY_SURFACE_KIND,
            "entry_adapter": SERVICE_SAFE_ENTRY_ADAPTER,
            "command": execution_command,
        },
        "handoff_contract_kind": SERVICE_SAFE_ENTRY_SURFACE_KIND,
    }


def _build_pending_route_contract(route_id: str, *, source_stage: str) -> dict[str, Any]:
    resolved_route_id = _require_nonempty_route_id(route_id, context="pending executor route")
    contract = {
        "route_id": resolved_route_id,
        "route_status": "pending",
        "executor_owner": EXECUTOR_ROUTE_OWNER,
        "execution_surface": None,
        "handoff_contract_kind": "handoff-required",
    }
    handoff_requirements = _build_pending_route_handoff_requirements(
        resolved_route_id,
        source_stage=source_stage,
    )
    if handoff_requirements is not None:
        contract["handoff_requirements"] = handoff_requirements
    return contract


def _build_pending_route_handoff_requirements(
    route_id: str,
    *,
    source_stage: str,
) -> dict[str, Any] | None:
    requirements = PENDING_ROUTE_HANDOFF_REQUIREMENTS.get(route_id)
    if requirements is None:
        return None

    required_domain_surfaces = [_build_service_safe_domain_surface("summarize-workspace")]
    if source_stage in REVIEW_CONTEXT_STAGES:
        required_domain_surfaces.append(_build_service_safe_domain_surface("critique-summary"))
    required_domain_surfaces.append(_build_service_safe_domain_surface("stage-route-report"))

    required_identity_fields = ["grant_run_id", "workspace_id"]
    if source_stage in DRAFT_ID_CONTEXT_STAGES:
        required_identity_fields.append("draft_id")

    return {
        "contract_kind": f"{route_id}-pending-handoff",
        "workspace_surface_kind": "nsfc_workspace",
        "required_domain_surfaces": required_domain_surfaces,
        "required_identity_fields": required_identity_fields,
        "required_summary_fields": list(requirements["required_summary_fields"]),
        "required_gate_fields": list(requirements["required_gate_fields"]),
    }


def _build_service_safe_domain_surface(command: str) -> dict[str, str]:
    resolved_command = _require_nonempty_route_id(command, context="service-safe domain surface command")
    return {
        "surface_kind": SERVICE_SAFE_ENTRY_SURFACE_KIND,
        "entry_adapter": SERVICE_SAFE_ENTRY_ADAPTER,
        "command": resolved_command,
    }


def _build_runtime_substrate_contract(*, current_program_contract: dict[str, Any]) -> dict[str, Any]:
    runtime_owner = current_program_contract.get("runtime_owner")
    if not isinstance(runtime_owner, dict):
        raise WorkspaceStateError("CURRENT_PROGRAM contract 缺少字段: runtime_owner")

    return {
        "runtime_owner": "Hermes",
        "current_owner_line": _require_nonempty_string(
            runtime_owner,
            "current_owner_line",
            context="CURRENT_PROGRAM contract runtime_owner",
        ),
        "active_phase": _require_nonempty_string(
            runtime_owner,
            "active_phase",
            context="CURRENT_PROGRAM contract runtime_owner",
        ),
        "active_tranche": _require_nonempty_string(
            runtime_owner,
            "active_tranche",
            context="CURRENT_PROGRAM contract runtime_owner",
        ),
        "compatibility_bridge": _require_nonempty_string(
            runtime_owner,
            "compatibility_bridge",
            context="CURRENT_PROGRAM contract runtime_owner",
        ),
        "repo_tracked_current_program_contract": CURRENT_PROGRAM_RELATIVE_PATH.as_posix(),
    }


def _build_runtime_state_contract() -> dict[str, Any]:
    return {
        "root": runtime_state_display_path(),
        "session_journal_root": _directory_display_path("sessions"),
        "logs_root": _directory_display_path("logs"),
        "reports_root": _directory_display_path("reports", "<program_id>"),
        "prompts_root": _directory_display_path("prompts"),
        "handoff_state_root": _directory_display_path("handoff_state"),
        "non_repo_tracked": True,
    }


def _build_operator_contract() -> dict[str, Any]:
    return {
        "canonical_audit_surfaces": [
            "validate-workspace",
            "summarize-workspace",
            "next-step",
            "critique-summary",
            "stage-route-report",
        ],
        "canonical_export_surfaces": [
            "execute-revision-pass",
            "build-artifact-bundle",
            "build-final-package",
            "build-hosted-contract-bundle",
        ],
        "checkpoint_aggregation_surface": "stage-route-report",
    }


def _require_nonempty_string(payload: dict[str, Any], field: str, *, context: str) -> str:
    value = payload.get(field)
    if not isinstance(value, str) or not value:
        raise WorkspaceStateError(f"{context} 缺少合法字段: {field}")
    return value


def _require_nonempty_route_id(value: Any, *, context: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise WorkspaceStateError(f"{context} 缺少合法 route_id")
    return value.strip()


def _directory_display_path(*segments: str) -> str:
    return runtime_state_display_path(*segments).rstrip("/") + "/"


def _resolve_control_plane_current_program_path(
    *,
    repo_root: Path | None = None,
    worktree_list_text: str | None = None,
) -> Path:
    del worktree_list_text
    return resolve_current_program_contract_path(repo_root=repo_root)


def _read_git_worktree_list(*, repo_root: Path) -> str:
    del repo_root
    raise WorkspaceStateError("项目级 .runtime-program 已退役；不再通过 git worktree 列表解析 control-plane root。")


def _select_control_plane_current_program_path(
    *,
    repo_root: Path,
    worktree_list_text: str,
) -> Path:
    del repo_root
    del worktree_list_text
    raise WorkspaceStateError("项目级 .runtime-program 已退役；不再通过 main worktree 回退解析 CURRENT_PROGRAM。")


def _parse_git_worktree_list_porcelain(worktree_list_text: str) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    current: dict[str, str] | None = None

    for raw_line in worktree_list_text.splitlines():
        if not raw_line:
            continue
        key, _, value = raw_line.partition(" ")
        if key == "worktree":
            if current is not None:
                entries.append(current)
            current = {"worktree": value}
            continue
        if current is None:
            continue
        if key in {"branch", "HEAD"}:
            current[key] = value

    if current is not None:
        entries.append(current)
    return entries


def _guard_final_package_output_identity(
    output_path: Path,
    *,
    grant_run_id: str,
    workspace_id: str,
    draft_id: str,
    lifecycle_stage: str | None,
) -> None:
    if not output_path.exists():
        return

    try:
        existing_payload = json.loads(output_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise WorkspaceStateError(
            f"final package output identity 不匹配: {output_path} 已存在且不是可校验的 JSON object。",
            errors=[],
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        ) from exc
    except OSError as exc:
        raise WorkspaceFileError(f"读取 final package output 失败: {output_path}") from exc

    if not isinstance(existing_payload, dict):
        raise WorkspaceStateError(
            f"final package output identity 不匹配: {output_path} 已存在且顶层不是 JSON object。",
            errors=[],
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )

    same_identity = (
        existing_payload.get("grant_run_id") == grant_run_id
        and existing_payload.get("workspace_id") == workspace_id
        and existing_payload.get("draft_id") == draft_id
    )
    if same_identity:
        return

    raise WorkspaceStateError(
        (
            "final package output identity 不匹配: "
            f"{output_path} -> "
            f"{existing_payload.get('grant_run_id')}/{existing_payload.get('workspace_id')}/{existing_payload.get('draft_id')} "
            f"!= {grant_run_id}/{workspace_id}/{draft_id}"
        ),
        errors=[],
        grant_run_id=grant_run_id,
        workspace_id=workspace_id,
        lifecycle_stage=lifecycle_stage,
    )


def _guard_hosted_contract_output_identity(
    output_path: Path,
    *,
    grant_run_id: str,
    workspace_id: str,
    draft_id: str,
    program_id: str,
) -> None:
    if not output_path.exists():
        return

    try:
        existing_payload = json.loads(output_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise WorkspaceStateError(
            f"hosted contract output identity 不匹配: {output_path} 已存在且不是可校验的 JSON object。"
        ) from exc
    except OSError as exc:
        raise WorkspaceFileError(f"读取 hosted contract output 失败: {output_path}") from exc

    if not isinstance(existing_payload, dict):
        raise WorkspaceStateError(
            f"hosted contract output identity 不匹配: {output_path} 已存在且顶层不是 JSON object。"
        )

    existing_execution_identity = existing_payload.get("execution_identity")
    if isinstance(existing_execution_identity, dict):
        existing_grant_run_id = existing_execution_identity.get("grant_run_id")
        existing_workspace_id = existing_execution_identity.get("workspace_id")
        existing_draft_id = existing_execution_identity.get("draft_id")
        existing_program_id = existing_execution_identity.get("program_id")
    else:
        existing_grant_run_id = existing_payload.get("grant_run_id")
        existing_workspace_id = existing_payload.get("workspace_id")
        existing_draft_id = existing_payload.get("draft_id")
        existing_program_id = existing_payload.get("program_id")

    same_identity = (
        existing_grant_run_id == grant_run_id
        and existing_workspace_id == workspace_id
        and existing_draft_id == draft_id
        and existing_program_id == program_id
    )
    if same_identity:
        return

    raise WorkspaceStateError(
        (
            "hosted contract output identity 不匹配: "
            f"{output_path} -> "
            f"{existing_grant_run_id}/{existing_workspace_id}/{existing_draft_id}/{existing_program_id} "
            f"!= {grant_run_id}/{workspace_id}/{draft_id}/{program_id}"
        )
    )


def _write_hosted_contract_bundle_output(output_path: Path, hosted_contract_bundle: dict[str, Any]) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        output_path.write_text(json.dumps(hosted_contract_bundle, ensure_ascii=False, indent=2), encoding="utf-8")
    except OSError as exc:
        raise WorkspaceFileError(f"写入 hosted contract output 失败: {output_path}") from exc


def _write_artifact_bundle_output(output_path: Path, bundle: dict[str, Any]) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        output_path.write_text(json.dumps(bundle, ensure_ascii=False, indent=2), encoding="utf-8")
    except OSError as exc:
        raise WorkspaceFileError(f"写入 bundle output 失败: {output_path}") from exc


def _write_revised_workspace_output(output_path: Path, revised_workspace: dict[str, Any]) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        output_path.write_text(json.dumps(revised_workspace, ensure_ascii=False, indent=2), encoding="utf-8")
    except OSError as exc:
        raise WorkspaceFileError(f"写入 revised workspace output 失败: {output_path}") from exc


def _write_final_package_output(output_path: Path, final_package: dict[str, Any]) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        output_path.write_text(json.dumps(final_package, ensure_ascii=False, indent=2), encoding="utf-8")
    except OSError as exc:
        raise WorkspaceFileError(f"写入 final package output 失败: {output_path}") from exc
