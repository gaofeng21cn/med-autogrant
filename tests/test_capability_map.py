from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]

EXPECTED_LEGACY_PROFESSIONAL_SKILL_REDIRECTS = {
    "legacy-professional-skill:mag-call-fit-analyst": "agent/professional_skills/mag-strategy-intake-specialist/SKILL.md",
    "legacy-professional-skill:mag-fundability-strategist": "agent/professional_skills/mag-strategy-intake-specialist/SKILL.md",
    "legacy-professional-skill:mag-specific-aims-architect": "agent/professional_skills/mag-strategy-intake-specialist/SKILL.md",
    "legacy-professional-skill:mag-grant-strategy-memory-curator": "agent/professional_skills/mag-strategy-intake-specialist/SKILL.md",
    "legacy-professional-skill:mag-proposal-section-author": "agent/professional_skills/mag-grant-workflow-specialist/SKILL.md",
    "legacy-professional-skill:mag-grant-reviewer": "agent/professional_skills/mag-grant-workflow-specialist/SKILL.md",
    "legacy-professional-skill:mag-rebuttal-planner": "agent/professional_skills/mag-grant-workflow-specialist/SKILL.md",
    "legacy-professional-skill:mag-submission-package-auditor": "agent/professional_skills/mag-grant-workflow-specialist/SKILL.md",
}

EXPECTED_OWNER_CLOSEOUT_RETURN_SHAPES = {
    "owner_receipt_ref",
    "typed_blocker_ref",
    "human_gate_ref",
    "route_back_ref",
}


def test_capability_map_declares_all_professional_skills() -> None:
    capability_map = json.loads((REPO_ROOT / "contracts/capability_map.json").read_text())
    skill_paths = {
        str(path.relative_to(REPO_ROOT))
        for path in (REPO_ROOT / "agent/professional_skills").glob("*/SKILL.md")
    }

    professional_skill_entries = [
        capability
        for capability in capability_map["capabilities"]
        if capability["surface_role"] == "professional_skill"
    ]
    mapped_paths = {
        capability["physical_source_ref"]["ref"]
        for capability in professional_skill_entries
    }

    assert mapped_paths == skill_paths
    for capability in professional_skill_entries:
        assert capability["capability_kind"] == "professional_skill"
        assert capability["physical_source_ref"]["role"] == "professional_skill_source"
        assert not any(capability["authority_boundary"].values())


def test_pack_compiler_input_lists_all_professional_skills() -> None:
    compiler_input = json.loads((REPO_ROOT / "contracts/pack_compiler_input.json").read_text())
    skill_paths = {
        str(path.relative_to(REPO_ROOT))
        for path in (REPO_ROOT / "agent/professional_skills").glob("*/SKILL.md")
    }

    assert skill_paths <= set(compiler_input["required_domain_pack_paths"])


def test_capability_map_self_evolution_routing_fields_are_refs_only() -> None:
    capability_map = json.loads((REPO_ROOT / "contracts/capability_map.json").read_text())

    for capability in capability_map["capabilities"]:
        source_ref = capability["physical_source_ref"]["ref"]
        assert capability["improvement_tokens"]
        assert source_ref in capability["canonical_target_paths"]
        assert "rtk ./scripts/verify.sh" in capability["verification_refs"]
        assert "opl:agents-scaffold-validate" in capability["verification_refs"]
        assert capability["forbidden_surfaces"]

        closeout = capability["owner_closeout_boundary"]
        assert closeout["owner"] == "med-autogrant"
        assert set(closeout["required_return_shapes"]) == (
            EXPECTED_OWNER_CLOSEOUT_RETURN_SHAPES
        )
        assert closeout["can_write_owner_receipt_body"] is False
        assert closeout["can_create_typed_blocker"] is False


def test_legacy_professional_skill_redirects_preserve_coverage_without_restoring_files() -> None:
    capability_map = json.loads((REPO_ROOT / "contracts/capability_map.json").read_text())
    skill_paths = {
        str(path.relative_to(REPO_ROOT))
        for path in (REPO_ROOT / "agent/professional_skills").glob("*/SKILL.md")
    }
    capabilities_by_id = {
        capability["capability_id"]: capability
        for capability in capability_map["capabilities"]
        if capability["surface_role"] == "professional_skill"
    }
    redirects = capability_map["legacy_professional_skill_redirects"]

    assert {entry["legacy_ref"]: entry["covered_by_skill_ref"] for entry in redirects} == (
        EXPECTED_LEGACY_PROFESSIONAL_SKILL_REDIRECTS
    )

    for entry in redirects:
        legacy_skill_id = entry["legacy_ref"].removeprefix("legacy-professional-skill:")
        assert entry["state"] == "legacy_redirect"
        assert entry["capability_kind"] == "legacy_professional_skill_redirect"
        assert entry["capability_preserved"] is True
        assert entry["default_codex_exposure"] is False
        assert entry["covered_by_skill_ref"] in skill_paths
        assert entry["covered_by_capability_id"] in capabilities_by_id
        assert (
            capabilities_by_id[entry["covered_by_capability_id"]]["physical_source_ref"]["ref"]
            == entry["covered_by_skill_ref"]
        )
        assert not (REPO_ROOT / "agent/professional_skills" / legacy_skill_id / "SKILL.md").exists()
        assert not (REPO_ROOT / "agent/professional_skills" / legacy_skill_id / "TOMBSTONE.md").exists()
