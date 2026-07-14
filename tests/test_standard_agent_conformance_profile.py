from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
EXPECTED_STAGE_DISPLAY_NAMES = {
    "call_and_candidate_intake": {
        "en-US": "Call and candidate intake",
        "zh-CN": "申报指南与候选方向梳理",
    },
    "fundability_strategy": {
        "en-US": "Fundability strategy",
        "zh-CN": "资助竞争力策略",
    },
    "specific_aims_and_structure": {
        "en-US": "Specific aims and structure",
        "zh-CN": "研究目标与申请书结构",
    },
    "proposal_authoring": {
        "en-US": "Proposal authoring",
        "zh-CN": "申请书撰写",
    },
    "review_and_rebuttal": {
        "en-US": "Grant Meta Review",
        "zh-CN": "申请书综合评审",
    },
    "package_and_submit_ready": {
        "en-US": "Package and submit ready",
        "zh-CN": "材料定稿与提交准备",
    },
}


def _read_json(relative_path: str) -> dict[str, object]:
    return json.loads((REPO_ROOT / relative_path).read_text(encoding="utf-8"))


def test_conformance_profile_tracks_domain_owned_stage_and_morphology_sources() -> None:
    profile = _read_json("contracts/standard_agent_conformance_profile.json")
    stage_manifest = _read_json("agent/stages/manifest.json")
    private_policy = _read_json("contracts/private_functional_surface_policy.json")

    stages = stage_manifest["stages"]
    stage_ids = [stage["stage_id"] for stage in stages]
    morphology = private_policy["physical_source_morphology_policy"]

    assert profile["surface_kind"] == "opl_standard_agent_conformance_profile"
    assert profile["version"] == "opl.standard-agent-conformance-profile.v1"
    assert profile["target_domain_id"] == "med-autogrant"
    assert stage_ids == list(EXPECTED_STAGE_DISPLAY_NAMES)
    for stage in stages:
        expected_names = EXPECTED_STAGE_DISPLAY_NAMES[stage["stage_id"]]
        display_names = stage["display_names"]

        assert isinstance(display_names, dict)
        assert {
            locale: display_names.get(locale) for locale in expected_names
        } == expected_names
        assert stage["title"] == display_names["en-US"]
    assert profile["golden_path"] == {
        "required_stage_ids": stage_ids,
        "allowed_stage_ids": stage_ids,
        "default_stage_id": "call_and_candidate_intake",
        "forbidden_owner_tokens": [],
    }
    assert profile["physical_morphology"]["required_surface_ids"] == morphology[
        "required_surface_ids"
    ]
    assert profile["physical_morphology"]["surface_classifications"] == morphology[
        "surface_classifications"
    ]
    assert profile["physical_morphology"]["required_parity_gates"] == [
        "opl_generated_surface_default_caller",
        "opl_python_executor_client",
        "mag_no_forbidden_write",
    ]
