from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


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
