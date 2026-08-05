from __future__ import annotations

import json
import re
import tomllib
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = REPO_ROOT / "plugins" / "med-autogrant"
PLUGIN_MANIFEST_PATH = PLUGIN_ROOT / ".codex-plugin" / "plugin.json"
ROOT_PLUGIN_MANIFEST_PATH = REPO_ROOT / ".codex-plugin" / "plugin.json"
ROOT_PACKAGE_DESCRIPTOR_PATH = REPO_ROOT / "opl-package.json"
PLUGIN_ICON_PATH = PLUGIN_ROOT / "assets" / "icon.png"
PLUGIN_ICON_SOURCE_PATH = PLUGIN_ROOT / "assets" / "icon.svg"
PLUGIN_SKILL_PATH = PLUGIN_ROOT / "skills" / "med-autogrant" / "SKILL.md"
PLUGIN_SKILL_UI_METADATA_PATH = PLUGIN_ROOT / "skills" / "med-autogrant" / "agents" / "openai.yaml"
PLUGIN_PACKAGE_DESCRIPTOR_PATH = PLUGIN_ROOT / "opl-package.json"
PRIMARY_SKILL_PATH = REPO_ROOT / "agent" / "primary_skill" / "SKILL.md"
PACKAGE_MANIFEST_PATH = REPO_ROOT / "contracts" / "opl_agent_package_manifest.json"
REPO_LOCAL_INSTALLER_PATHS = (
    REPO_ROOT / "scripts" / "install-codex-plugin.sh",
    REPO_ROOT / "src" / "med_autogrant" / "codex_plugin_installer.py",
)


def test_codex_plugin_manifest_tracks_repo_metadata_and_skill_layout() -> None:
    pyproject_data = tomllib.loads((REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    manifest = json.loads(PLUGIN_MANIFEST_PATH.read_text(encoding="utf-8"))

    assert manifest["name"] == "med-autogrant"
    assert manifest["version"] == pyproject_data["project"]["version"]
    assert manifest["repository"] == "https://github.com/gaofeng21cn/med-autogrant"
    assert manifest["skills"] == "./skills/"
    assert manifest["interface"]["displayName"] == "Med Auto Grant"
    assert manifest["interface"]["category"] == "Research"
    assert manifest["interface"]["composerIcon"] == "./assets/icon.png"
    assert manifest["interface"]["logo"] == "./assets/icon.png"
    assert "domain app" in manifest["description"].lower()
    assert PLUGIN_ICON_PATH.is_file()
    assert PLUGIN_ICON_SOURCE_PATH.is_file()
    icon_source = PLUGIN_ICON_SOURCE_PATH.read_text(encoding="utf-8")
    assert '<rect width="512" height="512" rx="112"' in icon_source
    assert 'stroke-width="42"' in icon_source
    assert 'stroke="#FFE08A"' in icon_source
    assert PLUGIN_SKILL_PATH.is_file()
    assert PLUGIN_SKILL_UI_METADATA_PATH.is_file()


def test_package_version_matches_python_plugin_and_owner_manifest() -> None:
    pyproject_data = tomllib.loads((REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    lock_data = tomllib.loads((REPO_ROOT / "uv.lock").read_text(encoding="utf-8"))
    plugin_manifest = json.loads(PLUGIN_MANIFEST_PATH.read_text(encoding="utf-8"))
    package_manifest = json.loads(PACKAGE_MANIFEST_PATH.read_text(encoding="utf-8"))
    init_text = (REPO_ROOT / "src" / "med_autogrant" / "__init__.py").read_text(
        encoding="utf-8"
    )
    version = pyproject_data["project"]["version"]

    assert version == "0.3.8"
    assert f'__version__ = "{version}"' in init_text
    assert plugin_manifest["version"] == version
    assert package_manifest["version"] == version
    assert next(
        package["version"]
        for package in lock_data["package"]
        if package["name"] == "med-autogrant"
    ) == version
    assert "distribution_payload" not in package_manifest


def test_owner_manifest_does_not_define_a_package_lifecycle_manager() -> None:
    package_manifest = json.loads(PACKAGE_MANIFEST_PATH.read_text(encoding="utf-8"))

    assert "lifecycle" not in package_manifest
    assert all(not path.exists() for path in REPO_LOCAL_INSTALLER_PATHS)


def test_agent_package_uses_mag_identity_without_relabeling_carriers() -> None:
    pyproject_data = tomllib.loads((REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    package_manifest = json.loads(PACKAGE_MANIFEST_PATH.read_text(encoding="utf-8"))

    assert package_manifest["agent_id"] == "mag"
    assert package_manifest["package_id"] == "mag"
    assert package_manifest["version"] == pyproject_data["project"]["version"]
    assert package_manifest["codex_surface"]["plugin_id"] == "med-autogrant"
    assert package_manifest["codex_surface"]["configured_codex_plugin_carrier"] == {
        "kind": "codex_plugin_manager",
        "plugin_selector": "med-autogrant@med-autogrant",
        "executor_route": "codex_cli",
        "marketplace_source": "gaofeng21cn/med-autogrant",
        "publication_ref": (
            "ghcr.io/gaofeng21cn/one-person-lab-packages/mag:latest-stable"
        ),
    }
    assert "lifecycle" not in package_manifest
    assert "distribution_payload" not in package_manifest
    assert "opl-agent-med-autogrant" not in json.dumps(package_manifest)


def test_owner_dependency_contains_only_presence_callability_and_domain_authority() -> None:
    package_manifest = json.loads(PACKAGE_MANIFEST_PATH.read_text(encoding="utf-8"))
    dependency = package_manifest["capability_dependencies"][0]

    assert set(dependency) == {
        "module_id",
        "package_id",
        "kind",
        "required",
        "dependency_kind",
        "version_requirement",
        "capability_abi",
        "consumer_profile_id",
        "provider_manifest_ref",
        "required_export_ids",
        "required_module_ids",
        "availability_policy_ref",
        "authority_boundary",
    }
    assert dependency["required"] is False
    assert dependency["dependency_kind"] == "optional_enhancement"
    assert dependency["availability_policy_ref"] == (
        "contracts/scholar_skill_binding_contract.json#/availability_policy"
    )
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


def test_carrier_root_projects_descriptor_neutral_mag_owner_contract() -> None:
    owner_manifest = json.loads(PACKAGE_MANIFEST_PATH.read_text(encoding="utf-8"))
    carrier_descriptor = json.loads(
        PLUGIN_PACKAGE_DESCRIPTOR_PATH.read_text(encoding="utf-8")
    )
    plugin_manifest = json.loads(PLUGIN_MANIFEST_PATH.read_text(encoding="utf-8"))

    owner_dependency = owner_manifest["capability_dependencies"][0]
    expected_presence = "required" if owner_dependency["required"] else "optional"
    assert carrier_descriptor == {
        "surface_kind": owner_manifest["surface_kind"],
        "kind": "agent",
        "agent_id": owner_manifest["agent_id"],
        "package_id": owner_manifest["package_id"],
        "domain_id": "med-autogrant",
        "display_name": owner_manifest["display_name"],
        "presentation": owner_manifest["presentation"],
        "publisher": owner_manifest["publisher"],
        "version": owner_manifest["version"],
        "source": owner_manifest["source"],
        "carrier_source_role": owner_manifest["carrier_source_role"],
        "schema_ref": owner_manifest["schema_ref"],
        "domain_descriptor_ref": "contracts/domain_descriptor.json",
        "task_provider_ref": (
            "contracts/domain_descriptor.json"
            "#/standard_agent_interface/stage_catalog"
        ),
        "action_catalog_ref": "contracts/action_catalog.json",
        "view_refs": [],
        "entrypoints": [],
        "codex_surface": {
            "plugin_id": owner_manifest["codex_surface"]["plugin_id"],
            "plugin_source_path": ".",
            "configured_codex_plugin_carrier": owner_manifest["codex_surface"][
                "configured_codex_plugin_carrier"
            ],
            "required_skill_ids": owner_manifest["codex_surface"][
                "required_skill_ids"
            ],
        },
        "requires": [
            {
                "package_id": owner_dependency["package_id"],
                "presence": expected_presence,
            }
        ],
        # Kept only because the current Framework parser requires the field.
        # Dependency authority lives in the owner contract, not this projection.
        "capability_dependencies": [],
    }
    assert carrier_descriptor["version"] == plugin_manifest["version"]
    assert carrier_descriptor["codex_surface"]["plugin_id"] == plugin_manifest["name"]
    assert (REPO_ROOT / carrier_descriptor["domain_descriptor_ref"]).is_file()
    assert (REPO_ROOT / carrier_descriptor["action_catalog_ref"]).is_file()

    forbidden_manager_fields = {
        "content_lock",
        "distribution_payload",
        "lifecycle",
        "lifecycle_receipt",
        "lock_ref",
        "managed_policy_surface",
        "managed_update_source",
        "opl_managed_surface",
        "package_core",
        "registry_entry",
        "rollback_ref",
        "transaction",
    }
    assert forbidden_manager_fields.isdisjoint(carrier_descriptor)
    assert all(
        set(requirement) == {"package_id", "presence"}
        for requirement in carrier_descriptor["requires"]
    )


def test_repo_root_carrier_contains_hosted_runtime_closure() -> None:
    marketplace = json.loads(
        (REPO_ROOT / ".agents" / "plugins" / "marketplace.json").read_text(
            encoding="utf-8"
        )
    )
    plugin_source_root = (
        REPO_ROOT / marketplace["plugins"][0]["source"]["path"]
    ).resolve()
    root_plugin_manifest = json.loads(
        ROOT_PLUGIN_MANIFEST_PATH.read_text(encoding="utf-8")
    )
    owner_manifest = json.loads(PACKAGE_MANIFEST_PATH.read_text(encoding="utf-8"))
    domain_descriptor = json.loads(
        (plugin_source_root / owner_manifest["domain_descriptor_ref"]).read_text(
            encoding="utf-8"
        )
    )
    action_catalog = json.loads(
        (plugin_source_root / owner_manifest["action_catalog_ref"]).read_text(
            encoding="utf-8"
        )
    )

    assert plugin_source_root == REPO_ROOT.resolve()
    assert root_plugin_manifest["skills"] == "./plugins/med-autogrant/skills/"
    assert root_plugin_manifest["version"] == owner_manifest["version"]
    assert ROOT_PACKAGE_DESCRIPTOR_PATH.read_bytes() == PACKAGE_MANIFEST_PATH.read_bytes()
    assert domain_descriptor["domain_id"] == owner_manifest["domain_id"]
    stage_manifest_ref = domain_descriptor["standard_agent_interface"]["stage_catalog"][
        "relative_path"
    ]
    assert (plugin_source_root / stage_manifest_ref).is_file()
    assert all(
        action["execution_binding"]["stage_manifest_ref"] == stage_manifest_ref
        for action in action_catalog["actions"]
    )
    for hosted_runtime_ref in (
        "src/med_autogrant/product_entry_parts/domain_handler.py",
        "src/med_autogrant/product_entry_parts/domain_handler_dispatch.py",
    ):
        assert (plugin_source_root / hosted_runtime_ref).is_file()


def test_mag_package_manifest_declares_owner_home_presentation() -> None:
    package_manifest = json.loads(PACKAGE_MANIFEST_PATH.read_text(encoding="utf-8"))

    assert package_manifest["presentation"] == {
        "display_name_i18n": {"en-US": "Med Auto Grant"},
        "description_i18n": {"en-US": "Grant authoring domain agent for Codex"},
        "session_routing_summary_i18n": {
            "en-US": (
                "Enter the current MAG grant workflow and continue the same "
                "funding-call authoring loop."
            )
        },
        "home_shortcuts": [
            {
                "shortcut_id": "open_grant_user_loop",
                "label_i18n": {"en-US": "Open MAG user loop"},
                "default_visible": True,
                "user_configurable": True,
                "route": {
                    "route_kind": "agent_package_shortcut",
                    "executor": "codex_cli",
                    "codex_visible_entry": "med-autogrant",
                },
            }
        ],
    }


def test_mag_skill_metadata_declares_app_skill_and_contract_surfaces() -> None:
    skill_text = PLUGIN_SKILL_PATH.read_text(encoding="utf-8")
    metadata_text = PLUGIN_SKILL_UI_METADATA_PATH.read_text(encoding="utf-8")
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
    assert carrier["carrier_skill_ref"] == "plugins/med-autogrant/skills/med-autogrant/SKILL.md"
    assert PRIMARY_SKILL_PATH.read_bytes() == PLUGIN_SKILL_PATH.read_bytes()

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


def test_primary_skill_exposes_only_three_opl_actions_and_semantic_grant_admission() -> None:
    skill = PRIMARY_SKILL_PATH.read_text(encoding="utf-8")

    assert "description: Use when Codex needs Med Auto Grant (MAG) to plan, author, critique, revise, or package a medical grant application" in skill
    assert "Do not use for research-paper production, generic document formatting, patient care, or irreversible submission" in skill
    for heading in (
        "Admission",
        "Action Routing",
        "Default Workflow",
        "Quality And Hard Stops",
        "Output Expectations",
        "References",
    ):
        assert f"## {heading}\n" in skill

    assert "`open_grant_user_loop`: default end-to-end entry" in skill
    assert "`build_direct_entry`: enter `proposal_authoring` directly only when" in skill
    assert "`build_submission_ready_package`: enter `package_and_submit_ready` only when" in skill
    assert "Do not expose repo-local CLI commands" in skill
    assert "`MedAutoGrantDomainEntry`" in skill
    assert "Missing call material is a typed source gap for intake" in skill
    assert "`submission-ready` means a local package passed MAG gates; it does not mean submitted" in skill
    assert "Retry, review, and repair counts are quality budgets" in skill
    for retired_entry in (
        "scripts/run-python-clean.sh",
        "workspace route-report --input",
        "domain-handler dispatch --task",
        "opl agents conformance --agent",
    ):
        assert retired_entry not in skill
