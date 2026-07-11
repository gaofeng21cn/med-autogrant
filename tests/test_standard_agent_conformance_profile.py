from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def _read_json(relative_path: str) -> dict[str, object]:
    return json.loads((REPO_ROOT / relative_path).read_text(encoding="utf-8"))


def test_conformance_profile_tracks_domain_owned_stage_and_morphology_sources() -> None:
    profile = _read_json("contracts/standard_agent_conformance_profile.json")
    stage_manifest = _read_json("agent/stages/manifest.json")
    private_policy = _read_json("contracts/private_functional_surface_policy.json")

    stage_ids = [stage["stage_id"] for stage in stage_manifest["stages"]]
    morphology = private_policy["physical_source_morphology_policy"]

    assert profile["surface_kind"] == "opl_standard_agent_conformance_profile"
    assert profile["version"] == "opl.standard-agent-conformance-profile.v1"
    assert profile["target_domain_id"] == "med-autogrant"
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
