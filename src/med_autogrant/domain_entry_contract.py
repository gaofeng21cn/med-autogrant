from __future__ import annotations

from typing import Any, Mapping

from med_autogrant import editable_shared_bootstrap as _editable_shared_bootstrap
from med_autogrant.public_cli import public_command_label

_editable_shared_bootstrap.ensure_editable_dependency_paths()

from opl_harness_shared.family_entry_contracts import (
    build_domain_agent_entry_spec as _build_shared_domain_agent_entry_spec,
    build_domain_entry_command_catalog as _build_shared_domain_entry_command_catalog,
    build_family_direct_opl_shared_handoff as _build_shared_family_direct_opl_shared_handoff,
    build_family_domain_entry_contract as _build_shared_family_domain_entry_contract,
    build_family_gateway_interaction_contract as _build_shared_family_gateway_interaction_contract,
)


PRODUCT_ENTRY_KIND = "med_auto_grant_product_entry"
PRODUCT_ENTRY_BUILD_COMMAND = public_command_label("build-product-entry")
SUPPORTED_PRODUCT_ENTRY_MODES = ("direct", "opl-handoff")
SERVICE_SAFE_ENTRY_ADAPTER = "MedAutoGrantDomainEntry"
SERVICE_SAFE_ENTRY_SURFACE_KIND = "service-safe-domain-entry-command"
DOMAIN_AGENT_ID = "mag"
DOMAIN_AGENT_ENTRY_TITLE = "Med Auto Grant Domain Agent"
DOMAIN_AGENT_ENTRY_DESCRIPTION = "Grant authoring domain truth owner surface for Med Auto Grant."
DOMAIN_AGENT_DEFAULT_ENGINE = "codex"
DOMAIN_AGENT_WORKSPACE_REQUIREMENT = "required"
DOMAIN_AGENT_LOCATOR_SCHEMA: dict[str, Any] = {
    "required_fields": ["input_path"],
    "optional_fields": ["workspace_id", "grant_run_id", "draft_id"],
    "workspace_field": "input_path",
    "workspace_kind": "nsfc_workspace",
    "workspace_id_field": "workspace_id",
    "run_id_field": "grant_run_id",
    "draft_id_field": "draft_id",
}
DOMAIN_AGENT_CODEX_ENTRY_STRATEGY = "domain_agent_entry"
DOMAIN_AGENT_ARTIFACT_CONVENTIONS = "grant_proposal_package"
DOMAIN_AGENT_PROGRESS_CONVENTIONS = "grant_workloop_narration"
DOMAIN_AGENT_ENTRY_COMMAND = "product-frontdesk"
DOMAIN_AGENT_MANIFEST_COMMAND = "product-entry-manifest"
DOMAIN_ENTRY_COMMAND_CATALOG_ENTRIES: list[dict[str, Any]] = [
    {"command": "probe-upstream-hermes", "required_fields": [], "optional_fields": []},
    {"command": "validate-workspace", "required_fields": ["input_path"], "optional_fields": []},
    {"command": "summarize-workspace", "required_fields": ["input_path"], "optional_fields": []},
    {"command": "grant-intake-audit", "required_fields": ["input_path"], "optional_fields": []},
    {"command": "grant-evidence-grounding", "required_fields": ["input_path"], "optional_fields": []},
    {"command": "grant-quality-scorecard", "required_fields": ["input_path"], "optional_fields": []},
    {
        "command": "grant-quality-diff",
        "required_fields": ["input_path", "previous_input_path"],
        "optional_fields": [],
    },
    {"command": "discover-funding-opportunities", "required_fields": ["input_path"], "optional_fields": []},
    {
        "command": "refresh-funding-opportunities-cache",
        "required_fields": ["input_path"],
        "optional_fields": ["output_path"],
    },
    {"command": "select-project-profile", "required_fields": ["input_path"], "optional_fields": []},
    {
        "command": "initialize-intake-workspace",
        "required_fields": ["input_path", "output_path"],
        "optional_fields": [],
    },
    {"command": "next-step", "required_fields": ["input_path"], "optional_fields": []},
    {"command": "critique-summary", "required_fields": ["input_path"], "optional_fields": []},
    {"command": "stage-route-report", "required_fields": ["input_path"], "optional_fields": []},
    {"command": "runtime-run", "required_fields": ["input_path"], "optional_fields": ["journal_path"]},
    {"command": "runtime-resume", "required_fields": ["journal_path"], "optional_fields": []},
    {
        "command": "execute-direction-screening-pass",
        "required_fields": ["input_path", "output_path"],
        "optional_fields": [],
    },
    {
        "command": "execute-question-refinement-pass",
        "required_fields": ["input_path", "output_path"],
        "optional_fields": [],
    },
    {
        "command": "execute-argument-building-pass",
        "required_fields": ["input_path", "output_path"],
        "optional_fields": [],
    },
    {
        "command": "execute-fit-alignment-pass",
        "required_fields": ["input_path", "output_path"],
        "optional_fields": [],
    },
    {
        "command": "execute-outline-pass",
        "required_fields": ["input_path", "output_path"],
        "optional_fields": [],
    },
    {
        "command": "execute-drafting-pass",
        "required_fields": ["input_path", "output_path"],
        "optional_fields": [],
    },
    {
        "command": "build-artifact-bundle",
        "required_fields": ["input_path", "output_path"],
        "optional_fields": [],
    },
    {
        "command": "execute-critique-pass",
        "required_fields": ["input_path", "output_path"],
        "optional_fields": ["executor_kind"],
    },
    {
        "command": "execute-critique-revision-loop",
        "required_fields": ["input_path", "output_dir"],
        "optional_fields": ["max_rounds", "executor_kind"],
    },
    {
        "command": "execute-authoring-mainline-loop",
        "required_fields": ["input_path", "output_dir"],
        "optional_fields": ["max_cycles", "executor_kind"],
    },
    {
        "command": "execute-grant-autonomy-controller",
        "required_fields": ["input_path", "output_dir"],
        "optional_fields": ["executor_kind"],
    },
    {
        "command": "execute-revision-pass",
        "required_fields": ["input_path", "output_path"],
        "optional_fields": [],
    },
    {
        "command": "execute-freeze-pass",
        "required_fields": ["input_path", "output_path"],
        "optional_fields": [],
    },
    {
        "command": "build-final-package",
        "required_fields": ["input_path", "artifact_bundle_path", "output_path"],
        "optional_fields": [],
    },
    {
        "command": "build-hosted-contract-bundle",
        "required_fields": ["final_package_path", "output_path"],
        "optional_fields": [],
    },
    {
        "command": "build-submission-ready-package",
        "required_fields": ["input_path", "output_dir"],
        "optional_fields": [],
    },
]


def build_domain_entry_contract() -> dict[str, Any]:
    catalog = _build_shared_domain_entry_command_catalog(DOMAIN_ENTRY_COMMAND_CATALOG_ENTRIES)
    domain_agent_entry_spec = _build_shared_domain_agent_entry_spec(
        agent_id=DOMAIN_AGENT_ID,
        title=DOMAIN_AGENT_ENTRY_TITLE,
        description=DOMAIN_AGENT_ENTRY_DESCRIPTION,
        default_engine=DOMAIN_AGENT_DEFAULT_ENGINE,
        workspace_requirement=DOMAIN_AGENT_WORKSPACE_REQUIREMENT,
        locator_schema=DOMAIN_AGENT_LOCATOR_SCHEMA,
        codex_entry_strategy=DOMAIN_AGENT_CODEX_ENTRY_STRATEGY,
        artifact_conventions=DOMAIN_AGENT_ARTIFACT_CONVENTIONS,
        progress_conventions=DOMAIN_AGENT_PROGRESS_CONVENTIONS,
        entry_command=DOMAIN_AGENT_ENTRY_COMMAND,
        manifest_command=DOMAIN_AGENT_MANIFEST_COMMAND,
    )
    return _build_shared_family_domain_entry_contract(
        entry_adapter=SERVICE_SAFE_ENTRY_ADAPTER,
        service_safe_surface_kind=SERVICE_SAFE_ENTRY_SURFACE_KIND,
        product_entry_builder_command=PRODUCT_ENTRY_BUILD_COMMAND,
        product_entry_kind=PRODUCT_ENTRY_KIND,
        supported_entry_modes=list(SUPPORTED_PRODUCT_ENTRY_MODES),
        domain_agent_entry_spec=domain_agent_entry_spec,
        **catalog,
    )


def build_gateway_interaction_contract(
    *,
    extra_payload: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    return _build_shared_family_gateway_interaction_contract(
        shared_downstream_entry=SERVICE_SAFE_ENTRY_ADAPTER,
        extra_payload=extra_payload,
    )


def build_shared_handoff(
    *,
    direct_entry_builder_command: str,
    opl_handoff_builder_command: str,
) -> dict[str, Any]:
    return _build_shared_family_direct_opl_shared_handoff(
        direct_entry_builder_command=direct_entry_builder_command,
        opl_handoff_builder_command=opl_handoff_builder_command,
    )
