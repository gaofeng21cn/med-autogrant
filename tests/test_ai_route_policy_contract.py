from __future__ import annotations

import ast
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def _assert_progress_first_route_policy(policy: dict[str, object]) -> None:
    assert policy["semantic_route_decision_owner"] == "decisive_codex_attempt"
    assert policy["stage_transition_materialization_owner"] == "opl_stage_run_controller"
    assert policy["primary_only_decisive_attempt_role"] == "producer"
    assert policy["formal_review_decisive_attempt_roles"] == ["reviewer", "re_reviewer"]
    assert policy["repairer_can_be_decisive_attempt"] is False
    assert "route_selection_owner" not in policy
    assert policy["codex_may_advance_skip_repeat_reverse_or_route_back"] is True
    assert policy["any_declared_stage_may_start_from_any_prior_stage_result"] is True
    assert policy["declared_requires_are_quality_context_not_launch_gates"] is True
    assert policy["next_stage_refs_are_recommendations_not_constraints"] is True


def test_stage_manifest_splits_semantic_route_decision_from_transition_materialization() -> None:
    manifest = json.loads((REPO_ROOT / "agent/stages/manifest.json").read_text(encoding="utf-8"))
    policy = manifest["progress_first_policy"]
    _assert_progress_first_route_policy(policy)
    assert policy["no_output_or_failure_diagnostic_advances_stage"] is True


def test_stage_operating_principles_match_progress_first_route_policy() -> None:
    principles = json.loads(
        (REPO_ROOT / "contracts/stage_operating_principles.json").read_text(encoding="utf-8")
    )
    policy = principles["speed_policy"]
    _assert_progress_first_route_policy(policy)
    assert policy["decisive_codex_attempt_is_single_semantic_control_plane"] is True
    assert "codex_cli_is_single_semantic_control_plane" not in policy


def test_active_source_never_assigns_semantic_route_ownership_to_codex_cli() -> None:
    offenders: list[str] = []
    source_root = REPO_ROOT / "src/med_autogrant"

    for source_path in sorted(source_root.rglob("*.py")):
        tree = ast.parse(source_path.read_text(encoding="utf-8"), filename=str(source_path))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Dict):
                continue
            for key_node, value_node in zip(node.keys, node.values, strict=True):
                if not (
                    isinstance(key_node, ast.Constant)
                    and isinstance(key_node.value, str)
                    and isinstance(value_node, ast.Constant)
                    and isinstance(value_node.value, str)
                ):
                    continue
                key = key_node.value
                value = value_node.value
                semantic_owner_aliases = {
                    "semantic_owner",
                    "semantic_route_owner",
                    "semantic_route_decision_owner",
                    "route_selection_owner",
                    "route_back_selection_owner",
                }
                executor_claims_semantic_ownership = (
                    key in semantic_owner_aliases and value == "codex_cli"
                ) or (key == "codex_cli_role" and "semantic_route" in value)
                if executor_claims_semantic_ownership:
                    relative_path = source_path.relative_to(REPO_ROOT)
                    offenders.append(f"{relative_path}:{node.lineno}:{key}={value}")

    assert offenders == []
