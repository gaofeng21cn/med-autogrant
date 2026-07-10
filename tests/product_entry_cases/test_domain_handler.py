from __future__ import annotations

import json
from pathlib import Path

import pytest

from med_autogrant.product_entry_parts.domain_handler import build_domain_handler_export
from med_autogrant.product_entry_parts.domain_handler_dispatch import dispatch_domain_handler_task
from med_autogrant.workspace import WorkspaceStateError
from product_entry_cases.support import CRITIQUE_EXAMPLE_PATH


def _write_task(tmp_path: Path, payload: dict[str, object]) -> Path:
    task_path = tmp_path / "task.json"
    task_path.write_text(json.dumps(payload), encoding="utf-8")
    return task_path


def test_domain_handler_export_is_direct_and_keeps_eight_authority_targets() -> None:
    payload = build_domain_handler_export(input_path=CRITIQUE_EXAMPLE_PATH)
    export = payload["domain_handler_export"]

    assert export["caller_boundary"]["generated_caller_owner"] == "one-person-lab"
    assert export["authority_boundary"]["generated_surface_ready_counts_as_domain_ready"] is False
    assert {
        item["authority_id"] for item in export["minimal_authority_functions"]
    } == {
        "fundability_verdict",
        "quality_verdict",
        "export_verdict",
        "package_authority",
        "memory_accept_reject",
        "owner_receipt_signer",
        "grant_transition_oracle",
        "grant_native_helper",
    }
    assert export["allowed_dispatch_actions"] == [
        "domain-memory/decide",
        "domain-memory/propose",
        "stage-attempt/closeout",
    ]
    assert "product_entry_manifest" not in export


def test_domain_handler_rejects_generic_platform_actions(tmp_path: Path) -> None:
    task_path = _write_task(
        tmp_path,
        {
            "action": "status/read",
            "input_path": str(CRITIQUE_EXAMPLE_PATH),
        },
    )

    with pytest.raises(WorkspaceStateError, match="action 不允许"):
        dispatch_domain_handler_task(task_path=task_path)


def test_domain_handler_writes_memory_decision_receipt_refs_only(tmp_path: Path) -> None:
    proposal_task = _write_task(
        tmp_path,
        {
            "task_id": "memory-proposal-1",
            "action": "domain-memory/propose",
            "input_path": str(CRITIQUE_EXAMPLE_PATH),
            "stage_id": "review_and_rebuttal",
            "source_ref": "runtime-closeout://grant-run/example",
            "lesson_summary": "Preserve reusable reviewer-risk framing.",
        },
    )
    proposal = dispatch_domain_handler_task(task_path=proposal_task)
    proposal_path = tmp_path / "proposal.json"
    proposal_path.write_text(
        json.dumps(proposal["domain_handler_dispatch"]["result"]["proposal"]),
        encoding="utf-8",
    )
    decision_task = _write_task(
        tmp_path,
        {
            "task_id": "memory-decision-1",
            "action": "domain-memory/decide",
            "input_path": str(CRITIQUE_EXAMPLE_PATH),
            "proposal_path": str(proposal_path),
            "decision": "accepted",
            "decision_reason": "Reusable stage strategy.",
            "runtime_root": str(tmp_path / "runtime-state"),
        },
    )

    decision = dispatch_domain_handler_task(task_path=decision_task)
    result = decision["domain_handler_dispatch"]["result"]
    assert result["write_policy"] == "runtime_store_only_no_repo_write"
    assert result["receipt_evidence"]["contains_memory_body"] is False
    assert Path(result["receipt_evidence"]["receipt_instance_ref"]).is_file()


def test_domain_handler_stage_closeout_writes_owner_receipt(tmp_path: Path) -> None:
    task_path = _write_task(
        tmp_path,
        {
            "task_id": "stage-closeout-1",
            "action": "stage-attempt/closeout",
            "input_path": str(CRITIQUE_EXAMPLE_PATH),
            "receipt_shape": "no_regression_evidence",
            "stage_id": "review_and_rebuttal",
            "source_ref": "opl-stage-attempt://stage-closeout-1",
            "closeout_summary": "No regression over MAG-owned refs.",
            "runtime_root": str(tmp_path / "runtime-state"),
        },
    )

    payload = dispatch_domain_handler_task(task_path=task_path)
    result = payload["domain_handler_dispatch"]["result"]
    receipt = result["owner_receipt_evidence"]
    assert result["return_shape"] == "no_regression_evidence"
    assert result["typed_blocker"] is None
    assert receipt["forbidden_write_proof"]["grant_truth_written"] is False
    assert Path(receipt["receipt_instance_ref"]).is_file()
