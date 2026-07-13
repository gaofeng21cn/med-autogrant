from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from med_autogrant.product_entry_parts.domain_handler import build_domain_handler_export
from med_autogrant.product_entry_parts.domain_handler_contract import ALLOWED_ACTIONS


pytestmark = pytest.mark.meta
REPO_ROOT = Path(__file__).resolve().parents[1]


def _read_json(relative_path: str) -> dict[str, object]:
    return json.loads((REPO_ROOT / relative_path).read_text(encoding="utf-8"))


def test_pack_compiler_input_declares_python_helper_boundary_without_generic_runtime() -> None:
    pack_input = _read_json("contracts/pack_compiler_input.json")
    profile = pack_input["implementation_profile"]

    assert pack_input["canonical_agent_id"] == "mag"
    assert pack_input["domain_id"] == "med-autogrant"
    assert profile["profile_id"] == "opl.standard_domain_agent.v1"
    assert profile["agent_identity"] == "declarative_standard_agent_pack"
    assert profile["pack_formats"] == ["markdown", "json"]
    assert profile["generated_surfaces_owner"] == "one-person-lab"
    helpers = profile["helpers"]
    assert helpers["optional"] is True
    assert helpers["language_is_identity"] is False
    assert helpers["rust_policy"] == "framework_hot_path_only"

    helper_implementations = helpers["entries"]
    assert {entry["language"] for entry in helper_implementations} == {"python"}
    assert {entry["role"] for entry in helper_implementations} == {"domain_helper"}
    for entry in helper_implementations:
        assert entry["source_roots"]
        for source_root in entry["source_roots"]:
            assert source_root.endswith("/"), source_root
            assert (REPO_ROOT / source_root).is_dir(), source_root


def test_stage_manifest_keeps_mag_authority_boundary_without_private_compiler() -> None:
    manifest = _read_json("agent/stages/manifest.json")
    authority = manifest["authority_boundary"]
    assert authority["domain_truth_owner"] == "med-autogrant"
    assert authority["fundability_verdict_owner"] == "med-autogrant"
    assert authority["authoring_quality_verdict_owner"] == "med-autogrant"
    assert authority["package_authority_owner"] == "med-autogrant"
    assert authority["submission_ready_export_verdict_owner"] == "med-autogrant"
    assert authority["opl_can_write_grant_truth"] is False
    assert authority["opl_can_authorize_quality_or_export"] is False

    assert len(manifest["stages"]) == 6
    for stage in manifest["stages"]:
        assert stage["prompt_ref"].startswith("agent/prompts/")
        assert stage["policy_ref"].startswith("agent/stages/")
        assert stage["allowed_action_refs"]

    assert not (REPO_ROOT / "contracts" / "stage_control_plane.json").exists()
    assert not (REPO_ROOT / "src" / "med_autogrant" / "stage_control_plane.py").exists()


def test_hosted_action_stage_routes_match_manifest_action_coverage() -> None:
    manifest = _read_json("agent/stages/manifest.json")
    action_catalog = _read_json("contracts/action_catalog.json")
    pack_input = _read_json("contracts/pack_compiler_input.json")
    next_stages = {
        stage["stage_id"]: set(stage["next_stage_refs"])
        for stage in manifest["stages"]
    }

    def reachable(source_stage_id: str, target_stage_id: str) -> bool:
        pending = [source_stage_id]
        visited: set[str] = set()
        while pending:
            stage_id = pending.pop()
            if stage_id == target_stage_id:
                return True
            if stage_id not in visited:
                visited.add(stage_id)
                pending.extend(next_stages[stage_id] - visited)
        return False

    expected_stages_by_action = {
        action["action_id"]: {
            stage["stage_id"]
            for stage in manifest["stages"]
            if action["action_id"] in stage["allowed_action_refs"]
        }
        for action in action_catalog["actions"]
    }
    manifest_action_ids = {
        action_id
        for stage in manifest["stages"]
        for action_id in stage["allowed_action_refs"]
    }
    catalog_action_ids = {action["action_id"] for action in action_catalog["actions"]}

    assert set(action_catalog) == {
        "surface_kind",
        "version",
        "catalog_id",
        "target_domain_id",
        "owner",
        "authority_boundary",
        "actions",
        "notes",
    }
    assert action_catalog["version"] == "family-action-catalog.v2"
    assert catalog_action_ids == {
        "open_grant_user_loop",
        "build_direct_entry",
        "build_submission_ready_package",
    }
    assert manifest_action_ids == catalog_action_ids
    assert pack_input["source_refs"]["stage_manifest"] == "agent/stages/manifest.json"
    assert pack_input["source_refs"]["action_catalog"] == "contracts/action_catalog.json"
    assert pack_input["source_refs"]["domain_handler_registry_source_ref"] == (
        "contracts/domain_handler_registry.json"
    )
    assert pack_input["source_refs"]["source_closure_audit_source_ref"] == (
        "contracts/source_closure_audit.json"
    )
    assert {
        pack_input["source_refs"]["stage_manifest"],
        pack_input["source_refs"]["action_catalog"],
    } <= set(pack_input["required_domain_pack_paths"])
    assert pack_input["standard_stage_pack_conformance"] == {
        "version": "standard-stage-pack.v2",
        "required": True,
        "enforcement_ref": pack_input["source_refs"]["stage_manifest"],
    }

    for action in action_catalog["actions"]:
        assert set(action) == {
            "action_id",
            "title",
            "summary",
            "owner",
            "effect",
            "execution_binding",
            "input_schema_ref",
            "output_schema_ref",
            "required_fields",
            "optional_fields",
            "workspace_locator_fields",
            "human_gate_ids",
            "stage_route",
            "supported_surfaces",
            "authority_boundary",
        }
        assert action["effect"] == "mutating"
        assert action["execution_binding"] == {
            "kind": "stage_binding",
            "stage_manifest_ref": "agent/stages/manifest.json",
        }
        assert set(action["supported_surfaces"]) == {
            "cli",
            "mcp",
            "skill",
            "product_entry",
            "openai",
            "ai_sdk",
        }
        assert all(
            "command" not in descriptor
            for descriptor in action["supported_surfaces"].values()
            if descriptor is not None
        )
        input_schema = _read_json(action["input_schema_ref"])
        assert input_schema["additionalProperties"] is False
        assert input_schema["required"] == action["required_fields"]
        assert set(input_schema["properties"]) == set(
            action["required_fields"] + action["optional_fields"]
        )

        route = action["stage_route"]
        required = route["required_stage_refs"]
        optional = route["optional_stage_refs"]
        routed_stages = required + optional

        assert route["route_policy"] == "ai_selected_progress_route"
        assert required and route["entry_stage_ref"] == required[0]
        assert len(routed_stages) == len(set(routed_stages))
        assert set(routed_stages) == expected_stages_by_action[action["action_id"]]
        assert set(route["terminal_stage_refs"]) <= set(routed_stages)
        assert all(target in next_stages[source] for source, target in zip(required, required[1:]))
        assert all(reachable(required[0], stage_id) for stage_id in optional)


def test_hosted_action_registry_and_source_closure_contracts_are_closed() -> None:
    descriptor = _read_json("contracts/domain_descriptor.json")
    registry = _read_json("contracts/domain_handler_registry.json")
    source_audit = _read_json("contracts/source_closure_audit.json")

    assert registry == {
        "surface_kind": "domain_handler_registry",
        "version": "domain-handler-registry.v1",
        "handlers": [],
    }
    assert set(source_audit) == {"surface_kind", "version", "entries"}
    assert source_audit["surface_kind"] == "standard_agent_source_closure_audit"
    assert source_audit["version"] == "standard-agent-source-closure-audit.v1"
    entries = source_audit["entries"]
    expected_entries = {
        ("scripts/line_budget.py", "main"): (
            "developer_tool",
            ("process_spawn",),
            ("git",),
        ),
        ("src/med_autogrant/domain_runtime_parts/io.py", "_write_hosted_contract_bundle_output"): (
            "minimal_authority_function",
            ("filesystem_write",),
            (),
        ),
        ("src/med_autogrant/domain_runtime_parts/io.py", "_write_artifact_bundle_output"): (
            "minimal_authority_function",
            ("filesystem_write",),
            (),
        ),
        ("src/med_autogrant/domain_runtime_parts/io.py", "_write_revised_workspace_output"): (
            "minimal_authority_function",
            ("filesystem_write",),
            (),
        ),
        ("src/med_autogrant/domain_runtime_parts/io.py", "_write_final_package_output"): (
            "minimal_authority_function",
            ("filesystem_write",),
            (),
        ),
        ("src/med_autogrant/domain_runtime_parts/io.py", "_write_submission_ready_package_output"): (
            "minimal_authority_function",
            ("filesystem_write",),
            (),
        ),
        ("src/med_autogrant/domain_runtime_parts/io.py", "_write_json_output"): (
            "minimal_authority_function",
            ("filesystem_write",),
            (),
        ),
        (
            "src/med_autogrant/product_entry_parts/domain_memory_runtime.py",
            "write_domain_memory_receipt_evidence",
        ): ("minimal_authority_function", ("filesystem_write",), ()),
        (
            "src/med_autogrant/product_entry_parts/owner_receipt_common.py",
            "write_receipt",
        ): ("minimal_authority_function", ("filesystem_write",), ()),
    }
    assert len(entries) == len(expected_entries)
    for entry in entries:
        key = (entry["file"], entry["symbol"])
        assert key in expected_entries
        expected_role, expected_effects, expected_targets = expected_entries[key]
        assert entry["role"] == expected_role
        assert tuple(entry["allowed_effects"]) == expected_effects
        assert tuple(entry["allowed_targets"]) == expected_targets
        assert entry["source_digest"].startswith("sha256:")
        assert len(entry["source_digest"]) == len("sha256:") + 64
    assert descriptor["standard_contract_refs"]["domain_handler_registry"] == (
        "contracts/domain_handler_registry.json"
    )
    assert descriptor["standard_contract_refs"]["source_closure_audit"] == (
        "contracts/source_closure_audit.json"
    )

    interface = descriptor["standard_agent_interface"]
    assert "entry_command_template" not in interface["workspace_binding"]
    assert "manifest_command_template" not in interface["workspace_binding"]
    assert "dispatch_command" not in interface["runtime"]


def test_descriptor_check_rejects_malformed_stage_manifest(tmp_path: Path) -> None:
    isolated_repo = tmp_path / "repo"
    shutil.copytree(REPO_ROOT / "agent", isolated_repo / "agent")
    shutil.copytree(REPO_ROOT / "contracts", isolated_repo / "contracts")
    (isolated_repo / "scripts").mkdir()
    shutil.copy2(
        REPO_ROOT / "scripts" / "check_descriptor_contracts.py",
        isolated_repo / "scripts" / "check_descriptor_contracts.py",
    )

    manifest_path = isolated_repo / "agent" / "stages" / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    del manifest["version"]
    manifest["owner"] = "wrong-owner"
    manifest["stages"][1]["stage_id"] = manifest["stages"][0]["stage_id"]
    manifest["stages"][0]["policy_ref"] = "agent/stages/missing.md"
    manifest["stages"][0]["allowed_action_refs"].append("unknown_action")
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

    result = subprocess.run(
        [sys.executable, isolated_repo / "scripts" / "check_descriptor_contracts.py"],
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 1
    assert "version is missing or invalid" in result.stdout
    assert "owner must match target_domain_id" in result.stdout
    assert "duplicate stage_id" in result.stdout
    assert "missing repo ref" in result.stdout
    assert "unknown allowed_action_ref" in result.stdout


def test_current_program_and_direct_handler_share_three_actions() -> None:
    current_program = _read_json("contracts/runtime-program/current-program.json")
    configured_actions = current_program["domain_handler"]["allowed_dispatch_actions"]
    expected_actions = sorted(ALLOWED_ACTIONS)
    export = build_domain_handler_export(
        input_path=REPO_ROOT / "examples" / "nsfc_workspace_p2c_critique.json"
    )
    assert configured_actions == expected_actions
    assert (
        export["domain_handler_export"]["allowed_dispatch_actions"]
        == expected_actions
    )
    handler_export = export["domain_handler_export"]
    assert "family_stage_control_plane" not in handler_export
    assert handler_export["declarative_stage_manifest_ref"] == "agent/stages/manifest.json"
    assert handler_export["family_stage_control_plane_ref"] == (
        "/product_entry_manifest/family_stage_control_plane"
    )
