import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_json(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def test_mag_declares_isolated_stage_review_for_every_ai_producer() -> None:
    manifest = read_json("agent/stages/manifest.json")
    profile = read_json("contracts/stage_quality_cycle_policy.json")

    assert manifest["quality_governance_profile_ref"] == "contracts/opl-framework/official-knowledge-deliverable-quality-profile.json"
    assert manifest["meta_review_policy_ref"] == "contracts/stage_quality_cycle_policy.json#/meta_review_policy"
    assert profile["framework_contract_ref"] == "contracts/opl-framework/stage-quality-cycle-contract.json"
    attempt_contract = profile["review_attempt_contract"]
    assert attempt_contract["attempt_roles"] == ["producer", "reviewer", "repairer", "re_reviewer"]
    assert attempt_contract["new_stage_attempt_per_role"] is True
    assert attempt_contract["new_execution_session_per_attempt"] is True
    assert attempt_contract["no_context_inheritance"] is True
    assert attempt_contract["same_thread_resume_role"] == "protocol_closeout_resume"
    assert attempt_contract["same_thread_resume_counts_as_review"] is False
    assert attempt_contract["same_thread_resume_consumes_quality_budget"] is False
    assert set(attempt_contract["role_prompt_refs"]) == {"producer", "reviewer", "repairer", "re_reviewer"}
    assert attempt_contract["required_role_output_ref_fields"]["reviewer"] == [
        "finding_refs", "repair_map_refs", "reviewed_artifact_hashes"
    ]
    assert "re_review_closure_refs" in attempt_contract["required_role_output_ref_fields"]["re_reviewer"]

    manifest_stages = {stage["stage_id"]: stage for stage in manifest["stages"]}
    assert set(profile["stages"]) == set(manifest_stages)
    for stage_id, policy in profile["stages"].items():
        assert manifest_stages[stage_id]["stage_quality_cycle_policy_ref"] == (
            f"contracts/stage_quality_cycle_policy.json#/stages/{stage_id}"
        )
        assert set(policy) == {
            "surface_kind", "version", "enabled", "stage_prompt_ref", "role_prompt_refs",
            "quality_rubric_refs", "in_thread_refinement", "formal_review", "budget_exhaustion",
            "attempt_boundary",
        }
        assert policy["enabled"] is True
        assert set(policy["role_prompt_refs"]) == {"producer", "reviewer", "repairer", "re_reviewer"}
        assert policy["in_thread_refinement"]["authoritative"] is False
        assert policy["stage_prompt_ref"] == manifest_stages[stage_id]["prompt_ref"]
        assert policy["quality_rubric_refs"] == manifest_stages[stage_id]["quality_gate_refs"]
        assert policy["formal_review"]["context_isolation_required"] is True
        assert set(policy["attempt_boundary"]) == {
            "inherits_stage_goal_scope_authority", "role_overlay_may_only_narrow",
            "controller_creates_next_attempt", "attempt_is_not_sub_stage",
        }
        assert all(policy["attempt_boundary"].values())
        if stage_id not in {"review_and_rebuttal", "package_and_submit_ready"}:
            assert policy["formal_review"]["required"] is True
            assert policy["formal_review"]["max_repair_rounds"] == 3


def test_mag_meta_review_is_independent_and_routes_to_defect_owner() -> None:
    manifest = read_json("agent/stages/manifest.json")
    profile = read_json("contracts/stage_quality_cycle_policy.json")
    stages = {stage["stage_id"]: stage for stage in manifest["stages"]}
    meta = profile["meta_review_policy"]

    assert stages["review_and_rebuttal"]["stage_role"] == "cross_stage_meta_review"
    assert meta["stage_id"] == "review_and_rebuttal"
    assert meta["attempt_role"] == "producer"
    assert meta["stage_prompt_ref"] == "agent/prompts/review_and_rebuttal.md"
    assert meta["independent_stage_run_required"] is True
    assert meta["new_execution_session_required"] is True
    assert meta["no_context_inheritance"] is True
    assert meta["max_route_back_rounds"] == 3
    assert meta["defect_owner_route_back"]["stage_refs"] == [
        "call_and_candidate_intake",
        "fundability_strategy",
        "specific_aims_and_structure",
        "proposal_authoring",
    ]
    prompt = (ROOT / "agent/prompts/review_and_rebuttal.md").read_text(encoding="utf-8")
    assert "Do not edit the proposal inside this Meta Review Stage" in prompt
    assert "producer_conversation_history" in meta["forbidden_inputs"]


def test_quality_policy_does_not_define_nested_stage_or_owner_graphs() -> None:
    profile = read_json("contracts/stage_quality_cycle_policy.json")
    forbidden = {"next_stage", "requires", "ensures", "stage_route", "sub_stage_graph", "independent_owner"}

    def walk(value: object) -> None:
        if isinstance(value, dict):
            assert forbidden.isdisjoint(value)
            for child in value.values():
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    walk(profile)
