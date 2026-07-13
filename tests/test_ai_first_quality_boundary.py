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


def test_submission_ready_schema_requires_exact_review_receipt_and_mag_owner_verdict() -> None:
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
    assert verdict["properties"]["owner"] == {"const": "med-autogrant"}
    assert "mag_owner_receipt" in verdict["properties"]["source_kind"]["enum"]
    assert "mag_owner_typed_blocker" in verdict["properties"]["source_kind"]["enum"]
    assert all(
        source_kind.startswith("mag_owner_")
        for source_kind in verdict["properties"]["source_kind"]["enum"]
    )
    typed_blocker_rule = verdict["allOf"][0]
    assert typed_blocker_rule["if"]["properties"]["source_kind"] == {
        "const": "mag_owner_typed_blocker"
    }
    assert typed_blocker_rule["then"]["properties"]["verdict_state"] == {
        "const": "blocked"
    }
    assert submission_ready_schema["properties"]["readiness_verdict"]["enum"] == [
        "candidate_ready_for_review",
        "candidate_blocked",
    ]
    assert submission_ready_schema["properties"]["submission_ready"] == {"const": False}
    handoff_review = submission_ready_schema["$defs"]["handoffReview"]
    assert handoff_review["properties"]["ready_claim_authorized"] == {"const": False}
    assert handoff_review["properties"]["decisive_attempt_roles"]["const"] == [
        "reviewer",
        "re_reviewer",
    ]
    assert handoff_review["properties"]["review_receipt_surface_kind"] == {
        "const": "opl_stage_review_receipt"
    }
    assert handoff_review["properties"]["review_receipt_materializer"] == {
        "const": "opl_stage_run_controller"
    }
    assert handoff_review["properties"]["local_readiness_authority_owner"] == {
        "const": "med-autogrant"
    }
    assert handoff_review["properties"]["local_readiness_requirement_mode"] == {
        "const": "all_of"
    }
    assert handoff_review["properties"]["local_readiness_contract_ref"] == {
        "const": (
            "contracts/owner_receipt_contract.json"
            "#/local_submission_ready_projection_contract"
        )
    }
    assert handoff_review["properties"]["local_readiness_required_ref_kinds"]["const"] == [
        "opl_stage_review_receipt",
        "submission_ready_export_verdict",
    ]

    receipt_bundle_schema = json.loads(_read("schemas/v1/codex-stage-execution-receipt-bundle.schema.json"))
    authority = receipt_bundle_schema["$defs"]["authorityBoundary"]
    for field in (
        "review_receipt_surface_kind",
        "review_receipt_materializer",
        "review_receipt_authorizes_local_readiness",
        "local_readiness_authority_owner",
        "local_readiness_requirement_mode",
        "local_readiness_contract_ref",
        "local_readiness_required_ref_kinds",
    ):
        assert field in authority["required"]
    assert authority["properties"]["review_receipt_authorizes_local_readiness"] == {
        "const": False
    }
    assert authority["properties"]["local_readiness_required_ref_kinds"]["const"] == [
        "opl_stage_review_receipt",
        "submission_ready_export_verdict",
    ]

    owner_receipt_contract = json.loads(_read("contracts/owner_receipt_contract.json"))
    local_readiness = owner_receipt_contract["local_submission_ready_projection_contract"]
    assert local_readiness == {
        "owner": "med-autogrant",
        "requirement_mode": "all_of",
        "required_input_ref_kinds": [
            "opl_stage_review_receipt",
            "submission_ready_export_verdict",
        ],
        "review_receipt_must_match_current_package_hashes": True,
        "owner_evidence_must_reference_required_inputs": True,
        "opl_can_authorize_local_readiness": False,
        "external_portal_acceptance": "separate_human_gate",
    }


def test_revision_quality_context_keeps_missing_ai_review_as_nonblocking_debt() -> None:
    from med_autogrant.ai_first_boundaries import active_ai_backed_critique_quality_context

    context = active_ai_backed_critique_quality_context(
        {
            "current_selection": {"active_revision_plan_id": "revision-plan-1"},
            "revision_plans": [{"revision_plan_id": "revision-plan-1", "critique_id": "critique-1"}],
            "mentor_critiques": [{"critique_id": "critique-1", "metadata": {"owner": "projection"}}],
        }
    )
    assert context["assessment_owner"] == "projection_only"
    assert context["ai_reviewer_required"] is True
    assert context["ai_reviewer_blocker_reason"]


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
