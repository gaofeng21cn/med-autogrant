from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROFILE_PATH = ROOT / "contracts" / "epistemic_review_scope_profile.json"
EXPECTED_SCOPE_IDS = {
    "mag:package_and_submit_ready:grant_content",
    "mag:package_and_submit_ready:grant_methodology",
    "mag:package_and_submit_ready:grant_reference",
    "mag:package_and_submit_ready:grant_display",
    "mag:package_and_submit_ready:grant_export",
    "mag:package_and_submit_ready:grant_package",
}
CHANGE_CLASS_ROLES = {
    "analysis_result": {"analysis_result"},
    "analysis_parameters": {"analysis_parameters"},
    "claim": {"claim"},
    "reference_source": {"reference_source"},
    "layout": {"layout"},
    "package_composition": {"package_content"},
    "package_wrapper": {"package_wrapper"},
}


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def scopes_by_id() -> dict[str, dict]:
    profile = read_json(PROFILE_PATH)
    return {scope["scope_id"]: scope for scope in profile["review_scopes"]}


def dependency_closure(scope: dict) -> set[str]:
    sources_by_dependent: dict[str, set[str]] = {}
    for edge in scope["dependency_edges"]:
        sources_by_dependent.setdefault(edge["dependent_ref"], set()).add(
            edge["source_ref"]
        )
    closure = set(scope["reviewed_node_refs"])
    pending = list(closure)
    while pending:
        dependent_ref = pending.pop()
        for source_ref in sources_by_dependent.get(dependent_ref, set()):
            if source_ref not in closure:
                closure.add(source_ref)
                pending.append(source_ref)
    return closure


def stale_scopes(node_ref: str, change_class: str) -> set[str]:
    if change_class in {"governance_metadata", "review_receipt", "locator_only"}:
        return set()
    expected_roles = CHANGE_CLASS_ROLES[change_class]
    stale: set[str] = set()
    for scope_id, scope in scopes_by_id().items():
        nodes = {node["node_ref"]: node for node in scope["nodes"]}
        node = nodes.get(node_ref)
        if (
            node is not None
            and node["role"] in expected_roles
            and node_ref in dependency_closure(scope)
        ):
            stale.add(scope_id)
    return stale


def test_profile_binds_canonical_framework_and_existing_stage_attempt_budget() -> None:
    profile = read_json(PROFILE_PATH)
    policy = read_json(ROOT / "contracts" / "stage_quality_cycle_policy.json")
    package_review = policy["stages"]["package_and_submit_ready"]["formal_review"]

    assert profile["surface_kind"] == "mag_epistemic_review_scope_profile"
    assert profile["domain_id"] == "med-autogrant"
    assert profile["owner"] == "med-autogrant"
    assert profile["stage_id"] == "package_and_submit_ready"
    assert profile["framework_binding"] == {
        "currentness_contract_ref": (
            "contracts/opl-framework/epistemic-review-currentness-contract.json"
        ),
        "scope_schema_ref": (
            "contracts/opl-framework/epistemic-review-scope-v2.schema.json"
        ),
        "stage_quality_contract_ref": (
            "contracts/opl-framework/stage-quality-cycle-contract.json"
        ),
    }
    assert profile["stage_attempt_budget"] == {
        "policy_ref": (
            "contracts/stage_quality_cycle_policy.json"
            "#/stages/package_and_submit_ready/formal_review/scope_budget"
        ),
        "all_review_scopes_share_one_stage_attempt_budget": True,
        "framework_enforces_budget": True,
        "parallel_evidence_control_plane_allowed": False,
        "mag_can_schedule_or_materialize_attempts": False,
    }
    assert package_review["max_repair_rounds"] == 3
    assert package_review["scope_budget"] == {
        "surface_kind": "opl_stage_quality_scope_budget",
        "version": "opl-stage-quality-scope-budget.v1",
        "max_attempts": 3,
        "max_elapsed_ms": 21_600_000,
        "max_tokens": 1_000_000,
        "token_budget_requires_observed_usage": True,
        "foreground_execution_must_use_managed_attempt": True,
    }


def test_review_scopes_are_closed_acyclic_epistemic_dependency_graphs() -> None:
    scopes = scopes_by_id()
    assert set(scopes) == EXPECTED_SCOPE_IDS

    for scope_id, scope in scopes.items():
        assert scope["surface_kind"] == "opl_epistemic_review_scope"
        assert scope["version"] == "opl-epistemic-review-scope.v2"
        assert scope["evidence_profile"] == "epistemic_provenance"
        assert scope["trust_model"] == "trusted_local_workspace"
        node_refs = [node["node_ref"] for node in scope["nodes"]]
        assert len(node_refs) == len(set(node_refs)), scope_id
        assert set(scope["reviewed_node_refs"]) <= set(node_refs), scope_id
        for edge in scope["dependency_edges"]:
            assert {edge["source_ref"], edge["dependent_ref"]} <= set(node_refs)
            assert edge["source_ref"] != edge["dependent_ref"]
        assert dependency_closure(scope) <= set(node_refs)
        assert scope["authority_boundary"] == {
            "hash_is_locator_or_stale_hint_only": True,
            "hash_is_content_authority": False,
            "release_integrity_is_separate": True,
            "framework_can_issue_domain_verdict": False,
        }


def test_metadata_layout_and_package_only_deltas_preserve_semantic_reviews() -> None:
    semantic_scopes = {
        "mag:package_and_submit_ready:grant_content",
        "mag:package_and_submit_ready:grant_methodology",
        "mag:package_and_submit_ready:grant_reference",
    }

    assert stale_scopes(
        "mag:governance:receipt_metadata", "governance_metadata"
    ) == set()
    layout_stale = stale_scopes("mag:provenance:grant_layout", "layout")
    package_stale = stale_scopes(
        "mag:artifact:hosted-contract-bundle.json", "package_wrapper"
    )

    assert layout_stale == {"mag:package_and_submit_ready:grant_display"}
    assert package_stale == {"mag:package_and_submit_ready:grant_package"}
    assert layout_stale.isdisjoint(semantic_scopes)
    assert package_stale.isdisjoint(semantic_scopes)
    assert stale_scopes(
        "mag:artifact:final-package.json", "package_composition"
    ) == {
        "mag:package_and_submit_ready:grant_export",
        "mag:package_and_submit_ready:grant_package",
    }


def test_content_methodology_and_reference_changes_stale_only_real_dependents() -> None:
    assert stale_scopes("mag:artifact:grant_body", "analysis_result") == {
        "mag:package_and_submit_ready:grant_content"
    }
    assert stale_scopes(
        "mag:provenance:methodology_parameters", "analysis_parameters"
    ) == {"mag:package_and_submit_ready:grant_methodology"}
    assert stale_scopes("mag:reference:rationale_source", "reference_source") == {
        "mag:package_and_submit_ready:grant_content",
        "mag:package_and_submit_ready:grant_reference",
    }
    assert stale_scopes("mag:reference:methodology_source", "reference_source") == {
        "mag:package_and_submit_ready:grant_methodology",
        "mag:package_and_submit_ready:grant_reference",
    }
    assert stale_scopes("mag:claim:scientific_rationale", "claim") == {
        "mag:package_and_submit_ready:grant_content",
        "mag:package_and_submit_ready:grant_reference",
        "mag:package_and_submit_ready:grant_display",
    }
    assert stale_scopes("mag:claim:scientific_rationale", "locator_only") == set()


def test_release_integrity_remains_exact_byte_and_separate() -> None:
    profile = read_json(PROFILE_PATH)
    integrity = profile["release_integrity"]
    owner_contract = read_json(ROOT / "contracts" / "owner_receipt_contract.json")
    readiness = owner_contract["local_submission_ready_projection_contract"]

    assert integrity["member_refs"] == [
        "mag:artifact:artifact-bundle.json",
        "mag:artifact:final-package.json",
        "mag:artifact:hosted-contract-bundle.json",
        "mag:artifact:submission-ready-package.json",
    ]
    assert integrity["exact_current_bytes_required"] is True
    assert integrity["member_mutation_requires_new_integrity_evidence"] is True
    assert integrity["can_replace_epistemic_review"] is False
    assert integrity["epistemic_review_can_replace_release_integrity"] is False
    assert readiness["review_receipt_must_match_current_package_hashes"] is False
    assert readiness["hash_change_alone_invalidates_epistemic_review"] is False
    assert readiness["release_integrity_must_match_current_package_hashes"] is True
    assert readiness["release_integrity_can_replace_epistemic_review"] is False
