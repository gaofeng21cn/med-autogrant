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
    assert profile["route_selection_contract_ref"] == (
        "contracts/opl-framework/stage-quality-cycle-contract.json"
        "#/cross_stage_route_selection"
    )
    attempt_contract = profile["review_attempt_contract"]
    assert attempt_contract["attempt_roles"] == ["producer", "reviewer", "repairer", "re_reviewer"]
    assert attempt_contract["new_stage_attempt_per_role"] is True
    assert attempt_contract["new_execution_session_per_attempt"] is True
    assert attempt_contract["no_context_inheritance"] is True
    assert attempt_contract["same_thread_resume_role"] == "protocol_closeout_resume"
    assert attempt_contract["same_thread_resume_counts_as_review"] is False
    assert attempt_contract["same_thread_resume_consumes_quality_budget"] is False
    assert attempt_contract["route_authority_contract_ref"] == (
        "#/cross_stage_route_selection"
    )
    route = profile["cross_stage_route_selection"]
    assert route["semantic_route_decision_owner"] == "decisive_codex_attempt"
    assert route["stage_transition_materialization_owner"] == (
        "opl_stage_run_controller"
    )
    assert route["primary_only_decisive_attempt_role"] == "producer"
    assert route["formal_review_decisive_attempt_roles"] == ["reviewer", "re_reviewer"]
    assert route["producer_can_be_decisive_attempt_in_formal_review"] is False
    assert route["repairer_can_be_decisive_attempt"] is False
    assert "producer_or_repairer_may_return_terminal_route_decision" not in route
    assert route[
        "same_stage_repair_required_with_budget_remaining_continues_quality_loop"
    ] is True
    assert route[
        "repair_required_review_or_re_review_may_select_cross_stage_route_back_before_budget_exhaustion"
    ] is True
    assert route[
        "repair_required_cross_stage_route_back_requires_target_different_from_current_stage"
    ] is True
    assert route[
        "cross_stage_route_back_requires_narrowest_canonical_owner_stage"
    ] is True
    assert route[
        "repair_required_review_or_re_review_may_select_other_terminal_route_before_budget_exhaustion"
    ] is False
    assert route[
        "repair_required_review_or_re_review_may_select_terminal_route_after_budget_exhaustion"
    ] is True
    assert route["repair_budget_exhaustion_terminal_status"] == (
        "completed_with_quality_debt"
    )
    assert route["hard_stop_or_zero_consumable_artifact_route_output"] == "none"
    assert "repair_required_with_budget_remaining_route_output" not in json.dumps(profile)

    assert attempt_contract["attempt_output_contract"] == {
        "envelope_path": "route_impact.stage_quality_cycle",
        "outcome_field": "outcome",
        "outcome_required_for_roles": ["reviewer", "re_reviewer"],
        "outcome_values": [
            "pass", "repair_required", "quality_debt", "blocked", "human_gate",
        ],
        "attempts_must_not_emit_receipt_verdict": True,
        "receipt_materializer_owner": "opl_stage_run_controller",
        "review_receipt_verdict_mapping": {
            "pass": "pass",
            "repair_required": "repair_required",
            "quality_debt": "quality_debt",
            "blocked": "hard_stop",
            "human_gate": "hard_stop",
        },
    }
    assert set(attempt_contract["role_prompt_refs"]) == {"producer", "reviewer", "repairer", "re_reviewer"}
    assert attempt_contract["required_role_output_ref_fields"]["reviewer"] == [
        "route_impact.stage_quality_cycle.outcome", "finding_refs", "evidence_refs",
        "acceptance_criteria_refs",
    ]
    assert attempt_contract["required_role_output_ref_fields"]["repairer"] == [
        "repaired_artifact_refs", "repaired_artifact_hashes", "repair_map_refs",
        "changed_artifact_refs", "changed_artifact_hashes", "lineage_refs",
    ]
    assert attempt_contract["required_role_output_ref_fields"]["re_reviewer"] == [
        "route_impact.stage_quality_cycle.outcome", "re_review_closure_refs",
        "evidence_refs", "remaining_quality_debt_refs",
    ]
    assert "verdict" not in attempt_contract["required_role_output_ref_fields"]["reviewer"]
    assert "verdict" not in attempt_contract["required_role_output_ref_fields"]["re_reviewer"]
    assert "repair_map_refs" not in attempt_contract["required_role_output_ref_fields"]["reviewer"]
    assert "review_receipt_refs" not in attempt_contract["required_role_output_ref_fields"]["reviewer"]
    assert "review_receipt_refs" not in attempt_contract["required_role_output_ref_fields"]["re_reviewer"]

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
        if stage_id != "review_and_rebuttal":
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
    assert meta["terminal_route_output"] == "route_impact.stage_route_decision"
    assert meta["terminal_route_owner"] == "producer"
    assert "route_decision_evidence_refs" in meta["required_output_ref_fields"]
    assert meta["defect_owner_route_back"]["stage_refs"] == [
        "call_and_candidate_intake",
        "fundability_strategy",
        "specific_aims_and_structure",
        "proposal_authoring",
    ]
    prompt = (ROOT / "agent/prompts/review_and_rebuttal.md").read_text(encoding="utf-8")
    assert "Do not edit the proposal inside this Meta Review Stage" in prompt
    assert "decisive cross-Stage route owner" in prompt
    assert "`route_impact.stage_route_decision`" in prompt
    assert "producer_conversation_history" in meta["forbidden_inputs"]


def test_package_stage_reviews_current_final_bytes_before_ready_projection() -> None:
    manifest = read_json("agent/stages/manifest.json")
    profile = read_json("contracts/stage_quality_cycle_policy.json")
    stages = {stage["stage_id"]: stage for stage in manifest["stages"]}
    package_stage = stages["package_and_submit_ready"]
    package_policy = profile["stages"]["package_and_submit_ready"]

    assert package_stage["handoff_review_boundary"] == {
        "artifact_effect": "new_or_transformed_reviewable_bytes",
        "freezes_canonical_artifact_bytes": True,
        "issues_quality_export_publication_or_ready_claim": True,
        "downstream_owner_retains_acceptance": True,
    }
    assert package_stage["ensures"] == [
        "submission_ready_package_candidate_ref_recorded",
        "opl_stage_review_receipt_ref_recorded",
        "mag_submission_ready_export_verdict_or_owner_receipt_ref_recorded",
    ]
    assert package_policy["in_thread_refinement"] == {"allowed": True, "authoritative": False}
    assert package_policy["formal_review"] == {
        "required": True,
        "risk_tier": "high",
        "review_depth": "full",
        "context_isolation_required": True,
        "max_repair_rounds": 3,
    }

    prompt = (ROOT / package_stage["prompt_ref"]).read_text(encoding="utf-8")
    roles = (ROOT / "agent/prompts/stage-quality-cycle-roles.md").read_text(encoding="utf-8")
    for artifact in (
        "artifact-bundle.json",
        "final-package.json",
        "hosted-contract-bundle.json",
        "submission-ready-package.json",
    ):
        assert artifact in prompt
    assert "`same_stage_repair_required`" in prompt
    assert "`cross_stage_route_back_before_budget_exhaustion`" in prompt
    assert "no other terminal route is allowed before budget exhaustion" in prompt
    assert "repair only assembly, manifest, or provenance projection" in roles
    for finding_field in ("finding_id", "severity", "required", "evidence_refs", "repair_expectation"):
        assert f"`{finding_field}`" in roles
    assert "acceptance-criteria refs" in roles
    assert "Do not create a Review receipt or repair map" in roles
    assert "repair map keyed by every accepted `finding_id`" in roles
    assert "repairer cannot close findings or make a terminal Stage judgment" in roles
    assert "route_impact.stage_route_decision" in roles
    assert "route_impact.stage_route_recommendation" in roles
    assert "repair_required" in roles
    assert "StageRunController materializes only the exact-hash-bound `opl_stage_review_receipt`" in roles
    assert "to its identically named receipt verdict" in roles
    assert "to the same receipt verdict" not in roles
    assert "`route_impact.stage_quality_cycle.outcome`" in roles
    for outcome in ("pass", "repair_required", "quality_debt", "blocked", "human_gate"):
        assert f"`{outcome}`" in roles
    assert "`hard_stop` is never an Attempt outcome" in roles
    for closure_status in ("closed", "partially_closed", "still_open"):
        assert f"`{closure_status}`" in roles
    for repair_trigger in (
        "required_finding_not_closed",
        "repair_regression",
        "critical_new_finding",
    ):
        assert f"`{repair_trigger}`" in roles
    assert "`optional_observation` or quality debt without reopening the loop" in roles
    assert "cannot create a Review receipt or a ready verdict" in roles
    for legacy_field in (
        "route_back_stage_ref",
        "selected_next_stage_ref",
        "next_stage_ref",
        "workflow_complete",
    ):
        assert f"legacy `{legacy_field}`" in roles or f"`{legacy_field}`" in roles
    assert "materializes only the exact-hash-bound `opl_stage_review_receipt`" in prompt
    assert "When repair budget is exhausted and exact package bytes remain consumable" in prompt
    assert "keeps outcome `repair_required`" in prompt
    assert "projects `completed_with_quality_debt`" in prompt
    assert "Neither the reviewer Attempt nor OPL signs the MAG owner receipt" in prompt
    assert "submission_ready_package_receipt_recorded" not in prompt
    assert "submission_ready_package_receipt_recorded" not in json.dumps(manifest)


def test_quality_role_prompt_routes_only_cross_stage_findings_before_exhaustion() -> None:
    roles = (ROOT / "agent/prompts/stage-quality-cycle-roles.md").read_text(
        encoding="utf-8"
    )
    reviewer = roles.split("## Reviewer", 1)[1].split("## Repairer", 1)[0]
    re_reviewer = roles.split("## Re Reviewer", 1)[1]

    assert roles.count("`same_stage_repair_required`") >= 3
    assert "another repair round remains" in roles
    assert "returns outcome `repair_required`" in roles
    assert "controller creates the next fresh repairer Attempt" in roles
    assert "This branch is non-terminal" in roles

    assert roles.count("`cross_stage_route_back_before_budget_exhaustion`") >= 3
    assert "narrowest canonical owner of required work is a different declared Stage" in roles
    assert "outcome `repair_required` plus exactly one" in roles
    assert "`decision_kind=route_back`" in roles
    assert "`target_stage_id` different from the current Stage" in roles
    assert "only terminal route allowed before repair-budget exhaustion" in roles
    for decisive_review_section in (reviewer, re_reviewer):
        assert "`same_stage_repair_required`" in decisive_review_section
        assert (
            "`cross_stage_route_back_before_budget_exhaustion`"
            in decisive_review_section
        )

    assert "`final_budget_consumable`" in roles
    assert "no repair round remains" in roles
    assert "Required findings keep outcome `repair_required`" in roles
    assert "do not relabel them `quality_debt`" in roles
    assert "exactly one `route_impact.stage_route_decision`" in roles
    assert "remaining required finding refs and quality-debt refs" in roles
    assert "controller classifies this branch as `terminal_quality_debt`" in roles
    assert "projects `completed_with_quality_debt`" in roles
    assert "Use outcome `quality_debt` only when no required finding remains" in roles

    assert "`hard_boundary_or_zero_artifact`" in roles
    assert "zero consumable exact artifact is not a Stage-routing judgment" in roles
    assert "return neither `route_impact.stage_route_decision` nor " in roles
    assert "`route_impact.stage_route_recommendation`" in roles
    assert "zero consumable artifact uses `blocked`" in roles
    assert "terminalizes the StageRun as blocked or human-gated" in roles
    assert "A hard-boundary reviewer returns no route output" in roles

    assert "repairer cannot close findings or make a terminal Stage judgment" in roles
    assert "it must never return `stage_route_decision`" in roles
    assert "Under `hard_boundary_or_zero_artifact`, return no route output" in roles


def test_quality_policy_does_not_define_nested_stage_or_owner_graphs() -> None:
    profile = read_json("contracts/stage_quality_cycle_policy.json")
    forbidden = {
        "next_stage_refs",
        "requires",
        "ensures",
        "stage_route",
        "sub_stage_graph",
        "independent_owner",
        "stage_current_pointer",
        "stage_transition_authority",
    }

    def walk(value: object) -> None:
        if isinstance(value, dict):
            assert forbidden.isdisjoint(value)
            for child in value.values():
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    walk(profile)
