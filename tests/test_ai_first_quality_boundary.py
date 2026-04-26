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
    assert scorecard_schema["$defs"]["grantQualityScorecard"]["properties"]["assessment_owner"]["enum"] == [
        "ai_reviewer_backed",
        "projection_only",
    ]

    summary_required = dossier_schema["$defs"]["qualitySummary"]["required"]
    assert "assessment_owner" in summary_required
    assert "ai_reviewer_required" in summary_required
    assert "review_artifact_ref" in summary_required


def test_quality_candidate_statuses_are_gated_by_ai_reviewer_backed_critique() -> None:
    boundaries = _read("src/med_autogrant/ai_first_boundaries.py")
    quality_assessment = _read("src/med_autogrant/grant_quality_assessment.py")
    runtime_ops = _read("src/med_autogrant/hermes_runtime_parts/runtime_ops.py")

    assert '"Codex CLI critique executor"' in boundaries
    assert '"Hermes-native critique proof executor"' in boundaries
    assert "owner in AI_REVIEWER_BACKED_OWNERS" in boundaries
    assert 'return "blocked"' in quality_assessment
    assert "if ai_reviewer_required:" in quality_assessment
    assert "quality_status = overall_status if not ai_reviewer_required" in runtime_ops
    assert '"not_ready"' in runtime_ops
    assert "AI reviewer-backed critique is required" in runtime_ops


def test_revision_executor_only_applies_ai_authored_mutation_payload() -> None:
    revision_executor = _read("src/med_autogrant/revision_executor.py")

    assert "require_active_ai_backed_critique(document)" in revision_executor
    assert 'section["text"] = mutation_payload["replacement_text"]' in revision_executor
    assert 'outline_item["core_claim"] = mutation_payload["replacement_core_claim"]' in revision_executor
    assert "fallback" not in revision_executor.lower()
    assert "default replacement" not in revision_executor.lower()


def test_critique_executor_stamps_known_ai_reviewer_owners() -> None:
    critique_executor = _read("src/med_autogrant/critique_executor.py")

    assert 'metadata["owner"] = "Codex CLI critique executor"' in critique_executor
    assert 'metadata["owner"] = "Hermes-native critique proof executor"' in critique_executor
