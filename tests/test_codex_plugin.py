from __future__ import annotations

import json
import re
import tomllib
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
ROOT_PACKAGE_DESCRIPTOR_PATH = REPO_ROOT / "opl-package.json"
SKILL_ROOT = REPO_ROOT / "skills" / "med-autogrant"
SKILL_PATH = SKILL_ROOT / "SKILL.md"
SKILL_UI_METADATA_PATH = SKILL_ROOT / "agents" / "openai.yaml"
PRIMARY_SKILL_PATH = REPO_ROOT / "agent" / "primary_skill" / "SKILL.md"
REPO_LOCAL_INSTALLER_PATHS = (
    REPO_ROOT / "scripts" / "install-codex-plugin.sh",
    REPO_ROOT / "src" / "med_autogrant" / "codex_plugin_installer.py",
)


def test_v2_package_manifest_tracks_repo_metadata_and_skill_layout() -> None:
    pyproject_data = tomllib.loads((REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    manifest = json.loads(ROOT_PACKAGE_DESCRIPTOR_PATH.read_text(encoding="utf-8"))
    identity = manifest["identity"]
    codex = manifest["host_hints"]["codex"]

    assert manifest["schema_version"] == "opl.package.v2"
    assert identity["id"] == "mag"
    assert identity["version"] == pyproject_data["project"]["version"]
    assert identity["repository"] == "https://github.com/gaofeng21cn/med-autogrant"
    assert identity["name"]["en-US"] == "Med Auto Grant"
    assert "medical grant" in identity["summary"]["en-US"].lower()
    assert (REPO_ROOT / identity["icon"]).is_file()
    assert codex["plugin_name"] == "med-autogrant"
    assert codex["category"] == "Research"
    assert manifest["provides"]["skills"] == [
        {"id": "med-autogrant", "path": "./skills/med-autogrant", "exposure": "default"}
    ]
    assert not (REPO_ROOT / "mcp.json").exists()
    assert not (REPO_ROOT / "plugins").exists()
    assert not (REPO_ROOT / ".codex-plugin").exists()
    assert SKILL_PATH.is_file()
    assert SKILL_UI_METADATA_PATH.is_file()


def test_package_version_matches_python_package_and_uv_lock() -> None:
    pyproject_data = tomllib.loads((REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    lock_data = tomllib.loads((REPO_ROOT / "uv.lock").read_text(encoding="utf-8"))
    manifest = json.loads(ROOT_PACKAGE_DESCRIPTOR_PATH.read_text(encoding="utf-8"))
    init_text = (REPO_ROOT / "src" / "med_autogrant" / "__init__.py").read_text(
        encoding="utf-8"
    )
    version = pyproject_data["project"]["version"]

    assert re.fullmatch(r"\d+\.\d+\.\d+", version)
    assert f'__version__ = "{version}"' in init_text
    assert manifest["identity"]["version"] == version
    assert next(
        package["version"]
        for package in lock_data["package"]
        if package["name"] == "med-autogrant"
    ) == version
    assert "distribution_payload" not in manifest


def test_owner_manifest_does_not_define_a_package_lifecycle_manager() -> None:
    manifest = json.loads(ROOT_PACKAGE_DESCRIPTOR_PATH.read_text(encoding="utf-8"))

    assert "lifecycle" not in manifest
    assert all(not path.exists() for path in REPO_LOCAL_INSTALLER_PATHS)


def test_agent_package_uses_mag_identity_without_relabeling_carriers() -> None:
    pyproject_data = tomllib.loads((REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    manifest = json.loads(ROOT_PACKAGE_DESCRIPTOR_PATH.read_text(encoding="utf-8"))

    assert manifest["identity"]["id"] == "mag"
    assert manifest["identity"]["version"] == pyproject_data["project"]["version"]
    assert manifest["host_hints"]["codex"]["plugin_name"] == "med-autogrant"
    assert manifest["distribution"] == {
        "oci": "ghcr.io/gaofeng21cn/one-person-lab-packages/mag",
        "visibility": "public",
    }
    assert "lifecycle" not in manifest
    assert "distribution_payload" not in manifest
    assert "opl-agent-med-autogrant" not in json.dumps(manifest)


def test_owner_dependency_contains_only_presence_callability_and_domain_authority() -> None:
    manifest = json.loads(ROOT_PACKAGE_DESCRIPTOR_PATH.read_text(encoding="utf-8"))
    binding = json.loads(
        (REPO_ROOT / "contracts" / "scholar_skill_binding_contract.json").read_text(
            encoding="utf-8"
        )
    )
    dependency = manifest["dependencies"]["packages"][0]

    assert dependency == {
        "id": binding["provider_package_id"],
        "version": ">=0.2.25 <0.3.0",
        "optional": False,
        "required_capabilities": binding["eligible_export_ids"],
        "required_module_ids": binding["eligible_module_ids"],
    }
    forbidden_lifecycle_fields = {
        "activation_materialization",
        "codex_distribution",
        "developer_distribution",
        "install_owner",
        "install_update_source",
        "lock_ref",
        "materializer",
        "opl_distribution",
        "receipt_ref",
        "repair_command",
        "status_ref",
        "sync_command_refs",
        "sync_scopes",
    }
    assert forbidden_lifecycle_fields.isdisjoint(dependency)


def test_v2_manifest_references_resolvable_domain_runtime_and_stage_resources() -> None:
    manifest = json.loads(ROOT_PACKAGE_DESCRIPTOR_PATH.read_text(encoding="utf-8"))
    domain_descriptor = json.loads(
        (REPO_ROOT / "contracts" / "domain_descriptor.json").read_text(encoding="utf-8")
    )
    action_catalog = json.loads(
        (REPO_ROOT / "contracts" / "action_catalog.json").read_text(encoding="utf-8")
    )

    stage_manifest_ref = domain_descriptor["standard_agent_interface"]["stage_catalog"][
        "relative_path"
    ]
    assert manifest["provides"]["agent"]["stages_ref"] == stage_manifest_ref
    assert domain_descriptor["domain_id"] == "med-autogrant"
    assert all(
        action["execution_binding"]["stage_manifest_ref"] == stage_manifest_ref
        for action in action_catalog["actions"]
    )

    pack = json.loads((REPO_ROOT / "contracts/pack_compiler_input.json").read_text())
    required_resources = (
        "contracts/domain_descriptor.json",
        "contracts/action_catalog.json",
        stage_manifest_ref,
        "src/med_autogrant/product_entry/domain_handler.py",
        "src/med_autogrant/product_entry/domain_handler_dispatch.py",
        "runtime/app_contribution.py",
        "schemas/v1/nsfc-workspace.schema.json",
        "contracts/runtime-program/current-program.json",
        *pack["required_domain_pack_paths"],
    )
    for resource in required_resources:
        assert (REPO_ROOT / resource).is_file(), resource


def test_mag_package_manifest_declares_owner_home_presentation() -> None:
    manifest = json.loads(ROOT_PACKAGE_DESCRIPTOR_PATH.read_text(encoding="utf-8"))
    identity = manifest["identity"]

    assert identity["icon"] == "assets/branding/medautogrant-logo.png"
    assert identity["name"] == {
        "zh-CN": "Med Auto Grant",
        "en-US": "Med Auto Grant",
    }
    assert identity["summary"] == {
        "zh-CN": "医学基金申请规划、撰写、评审与修订。",
        "en-US": "Medical grant application planning, writing, review, and revision.",
    }
    assert identity["routing_summary"] == {
        "zh-CN": "医学基金申请规划、撰写、评审与修订。",
        "en-US": (
            "Enter the current MAG grant workflow and continue the same "
            "funding-call authoring loop."
        ),
    }
    assert identity["home_shortcuts"] == [
        {
            "id": "open_grant_user_loop",
            "label": {
                "zh-CN": "开展基金申请工作",
                "en-US": "Open MAG user loop",
            },
            "default_visible": True,
            "target": {
                "kind": "agent",
                "ref": "mag",
            },
        }
    ]


def test_mag_skill_metadata_declares_app_skill_and_contract_surfaces() -> None:
    skill_text = SKILL_PATH.read_text(encoding="utf-8")
    metadata_text = SKILL_UI_METADATA_PATH.read_text(encoding="utf-8")
    pack_input = json.loads((REPO_ROOT / "contracts/pack_compiler_input.json").read_text())
    capability_map = json.loads((REPO_ROOT / "contracts/capability_map.json").read_text())
    action_catalog = json.loads((REPO_ROOT / "contracts/action_catalog.json").read_text())
    frontmatter_match = re.match(r"---\n(?P<frontmatter>.*?)\n---", skill_text, re.DOTALL)

    assert frontmatter_match is not None
    frontmatter = frontmatter_match.group("frontmatter")
    assert re.search(r"^name:\s*med-autogrant$", frontmatter, re.MULTILINE)
    assert pack_input["canonical_agent_id"] == "mag"

    primary_skill = next(
        capability
        for capability in capability_map["capabilities"]
        if capability["surface_role"] == "primary_skill"
    )
    carrier = primary_skill["carrier_projection_contract"]
    assert carrier["canonical_source"] == "agent/primary_skill/SKILL.md"
    assert carrier["carrier_skill_ref"] == "skills/med-autogrant/SKILL.md"
    assert PRIMARY_SKILL_PATH.read_bytes() == SKILL_PATH.read_bytes()

    for action in action_catalog["actions"]:
        assert action["execution_binding"] == {
            "kind": "stage_binding",
            "stage_manifest_ref": "agent/stages/manifest.json",
        }
        assert action["authority_boundary"]["domain_truth_owner"] == "med-autogrant"
        assert action["authority_boundary"]["opl_role"] == "projection_consumer_only"
        assert action["authority_boundary"]["write_policy"] == "no_domain_truth_writes"
        assert action["authority_boundary"]["opl_can_write_domain_truth"] is False
        assert action["supported_surfaces"]["mcp"]["descriptor_only"] is True
        assert action["supported_surfaces"]["mcp"]["public_runtime"] is False

    assert 'display_name: "Med Auto Grant"' in metadata_text
    assert "$med-autogrant" in metadata_text
