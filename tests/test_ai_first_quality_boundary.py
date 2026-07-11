from __future__ import annotations

import json
from pathlib import Path

import pytest


pytestmark = pytest.mark.meta

REPO_ROOT = Path(__file__).resolve().parents[1]


def _read(relative_path: str) -> str:
    return (REPO_ROOT / relative_path).read_text(encoding="utf-8")


def test_scorecard_and_dossier_schemas_require_ai_reviewer_provenance() -> None:
    scorecard_schema = json.loads(_read("schemas/v1/grant-quality-scorecard.schema.json"))
    dossier_schema = json.loads(_read("schemas/v1/grant-quality-closure-dossier.schema.json"))

    scorecard_required = scorecard_schema["$defs"]["grantQualityScorecard"]["required"]
    assert "assessment_owner" in scorecard_required
    assert "ai_reviewer_required" in scorecard_required
    assert "review_artifact_ref" in scorecard_required
    assert "independent_review_evidence" in scorecard_required
    assert "ai_reviewer_blocker_reason" in scorecard_required
    assert scorecard_schema["$defs"]["grantQualityScorecard"]["properties"]["assessment_owner"]["enum"] == [
        "ai_reviewer_backed",
        "projection_only",
    ]
    evidence_required = scorecard_schema["$defs"]["nullableIndependentReviewEvidence"]["anyOf"][0]["$ref"]
    assert evidence_required == "common.schema.json#/$defs/independentReviewEvidence"

    summary_required = dossier_schema["$defs"]["qualitySummary"]["required"]
    assert "assessment_owner" in summary_required
    assert "ai_reviewer_required" in summary_required
    assert "review_artifact_ref" in summary_required
    assert "independent_review_evidence" in summary_required
    assert "ai_reviewer_blocker_reason" in summary_required


def test_submission_ready_schema_requires_owner_export_verdict_gate() -> None:
    submission_ready_schema = json.loads(_read("schemas/v1/submission-ready-package.schema.json"))

    required = submission_ready_schema["required"]
    assert "mechanical_package_completeness" in required
    assert "submission_ready_export_verdict" in required

    verdict = submission_ready_schema["$defs"]["submissionReadyExportVerdict"]
    assert verdict["required"] == [
        "export_verdict_ref",
        "verdict_state",
        "owner",
        "source_kind",
        "provenance_ref",
    ]
    assert "med-autogrant" in verdict["properties"]["owner"]["enum"]
    assert "Codex CLI critique executor" in verdict["properties"]["owner"]["enum"]
    assert "mag_owner_receipt" in verdict["properties"]["source_kind"]["enum"]
    assert "mag_owner_typed_blocker" in verdict["properties"]["source_kind"]["enum"]


def test_revision_executor_only_applies_ai_authored_mutation_payload() -> None:
    from med_autogrant.ai_first_boundaries import require_active_ai_backed_critique
    from med_autogrant.workspace import WorkspaceStateError

    with pytest.raises(WorkspaceStateError, match="AI reviewer-backed critique is required"):
        require_active_ai_backed_critique(
            {
                "current_selection": {"active_revision_plan_id": "revision-plan-1"},
                "revision_plans": [{"revision_plan_id": "revision-plan-1", "critique_id": "critique-1"}],
                "mentor_critiques": [{"critique_id": "critique-1", "metadata": {"owner": "projection"}}],
            }
        )


def test_active_critique_requires_independent_review_evidence_for_ai_backed_status() -> None:
    from med_autogrant.ai_first_boundaries import active_critique_ai_review_provenance

    document = {
        "current_selection": {"active_revision_plan_id": "revision-plan-1"},
        "revision_plans": [{"revision_plan_id": "revision-plan-1", "critique_id": "critique-1"}],
        "mentor_critiques": [
            {
                "critique_id": "critique-1",
                "metadata": {"owner": "Codex CLI critique executor"},
            }
        ],
    }

    missing_evidence = active_critique_ai_review_provenance(document)
    assert missing_evidence["assessment_owner"] == "projection_only"
    assert missing_evidence["ai_reviewer_required"] is True
    assert missing_evidence["independent_review_evidence"] is None
    assert "independent execution/review receipt refs" in missing_evidence["ai_reviewer_blocker_reason"]

    document["mentor_critiques"][0]["metadata"]["independent_review_evidence"] = {
        "execution_attempt_ref": "draft_artifact::grant-run::draft-1",
        "review_attempt_ref": "mentor_critiques::critique-1",
        "review_receipt_ref": "mentor_critiques::critique-1::metadata.independent_review_evidence",
        "no_shared_context_verified": True,
        "reviewer_owner": "Codex CLI critique executor",
    }
    complete_evidence = active_critique_ai_review_provenance(document)
    assert complete_evidence["assessment_owner"] == "ai_reviewer_backed"
    assert complete_evidence["ai_reviewer_required"] is False
    assert complete_evidence["review_artifact_ref"] == "mentor_critiques::critique-1"
    assert complete_evidence["independent_review_evidence"]["review_receipt_ref"].endswith(
        "independent_review_evidence"
    )

    document["mentor_critiques"][0]["metadata"]["independent_review_evidence"] = {
        "execution_attempt_ref": "mentor_critiques::critique-1",
        "review_attempt_ref": "mentor_critiques::critique-1",
        "review_receipt_ref": "mentor_critiques::critique-1::metadata.independent_review_evidence",
        "no_shared_context_verified": True,
        "reviewer_owner": "Codex CLI critique executor",
    }
    same_attempt = active_critique_ai_review_provenance(document)
    assert same_attempt["assessment_owner"] == "projection_only"
    assert same_attempt["ai_reviewer_required"] is True


def test_critique_executor_payloads_stamp_known_ai_reviewer_owners(monkeypatch: pytest.MonkeyPatch) -> None:
    from med_autogrant.critique_executor import _normalize_mentor_critique
    from med_autogrant.domain_executor_client import build_executor_payload

    monkeypatch.setattr("med_autogrant.critique_executor._validate_schema_payload", lambda *args, **kwargs: None)
    critique_context = {
        "draft_id": "draft-1",
        "next_critique_id": "critique-1",
        "selected_question": {"core_question": "question"},
        "lifecycle_stage": "drafting",
        "grant_run_id": "grant-run-1",
        "workspace_id": "workspace-1",
    }
    critique_policy = {"weighted_dimensions": []}
    payload = {
        "overall_diagnosis": "diagnosis",
        "necessity_scientific_value": {},
        "applicant_fit": {},
        "technical_feasibility": {},
        "blocking_issues": [],
        "actionable_revision_plan": [],
        "verdict": "major_revision",
    }

    codex_executor = build_executor_payload(
        {
            "surface_kind": "opl_agent_execution_receipt",
            "executor_kind": "codex_cli",
            "mode": "structured_call",
            "session_id": "codex-session-1",
            "exit_code": 0,
            "non_equivalence_notice": "codex_cli_first_class_default",
            "proof": {"model": "gpt-5.4", "reasoning_effort": "high"},
        }
    )
    codex_critique = _normalize_mentor_critique(
        critique_context=critique_context,
        critique_policy=critique_policy,
        executor_payload=codex_executor,
        payload=payload,
    )
    assert codex_critique["metadata"]["owner"] == "Codex CLI critique executor"
    assert codex_critique["metadata"]["independent_review_evidence"] == {
        "execution_attempt_ref": "draft_artifact::grant-run-1::draft-1",
        "review_attempt_ref": "mentor_critiques::critique-1",
        "review_receipt_ref": "opl_agent_execution_receipt::codex-session-1",
        "no_shared_context_verified": True,
        "reviewer_owner": "Codex CLI critique executor",
        "reviewer_agent_ref": "codex_cli::codex-session-1",
    }

    hermes_proof = {
        "full_agent_loop_proved": True,
        "session_id": "session-1",
        "api_calls": 1,
        "tool_call_count": 1,
        "event_count": 2,
        "provider_reasoning_status": "unproven_custom_chat_completions",
        "event_stream": [{"type": "tool_start", "tool": "read_file"}],
    }
    hermes_executor = build_executor_payload(
        {
            "surface_kind": "opl_agent_execution_receipt",
            "executor_kind": "hermes_agent",
            "mode": "agent_loop",
            "cwd": "/tmp",
            "prompt_preview": "prompt",
            "session_id": "session-1",
            "event_summary": [{"type": "tool_start", "tool": "read_file"}],
            "stdout_preview": "{}",
            "stderr_preview": "",
            "exit_code": 0,
            "closeout_packet": None,
            "executor_contract": {
                "entrypoint": "OPL AgentExecutionRequest -> AgentExecutionReceipt",
                "model": "gpt-5.4",
                "provider": "custom",
                "api_mode": "chat_completions",
                "reasoning_effort": "xhigh",
            },
            "capabilities": ["full_agent_loop_receipt", "tool_event_proof", "session_id"],
            "non_equivalence_notice": "connectivity_lifecycle_receipt_audit_only",
            "proof": hermes_proof,
        },
    )
    hermes_critique = _normalize_mentor_critique(
        critique_context=critique_context,
        critique_policy=critique_policy,
        executor_payload=hermes_executor,
        payload=payload,
    )
    assert hermes_critique["metadata"]["owner"] == "OPL executor client critique receipt owner"
    assert hermes_critique["metadata"]["independent_review_evidence"]["execution_attempt_ref"] == (
        "draft_artifact::grant-run-1::draft-1"
    )
    assert hermes_critique["metadata"]["independent_review_evidence"]["review_receipt_ref"] == (
        "opl_agent_execution_receipt::session-1"
    )
    assert hermes_critique["metadata"]["independent_review_evidence"]["reviewer_owner"] == (
        "OPL executor client critique receipt owner"
    )
