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


def test_generated_pack_compiler_input_lists_all_professional_skills() -> None:
    from med_autogrant.opl_standard_pack import build_standard_pack

    generated = build_standard_pack()["pack_compiler_input"]
    skill_paths = {
        str(path.relative_to(REPO_ROOT))
        for path in (REPO_ROOT / "agent/professional_skills").glob("*/SKILL.md")
    }

    assert skill_paths <= set(generated["required_domain_pack_paths"])


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
