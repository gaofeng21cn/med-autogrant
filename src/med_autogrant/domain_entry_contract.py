from __future__ import annotations

from typing import Any, Mapping

from med_autogrant import editable_shared_bootstrap as _editable_shared_bootstrap
from med_autogrant.public_cli import public_command_label

_editable_shared_bootstrap.ensure_editable_dependency_paths()

from opl_harness_shared.family_entry_contracts import (
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
DOMAIN_ENTRY_COMMAND_CATALOG_ENTRIES: list[dict[str, Any]] = [
    {"command": "probe-upstream-hermes", "required_fields": [], "optional_fields": []},
    {"command": "validate-workspace", "required_fields": ["input_path"], "optional_fields": []},
    {"command": "summarize-workspace", "required_fields": ["input_path"], "optional_fields": []},
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
        "optional_fields": [],
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
    return _build_shared_family_domain_entry_contract(
        entry_adapter=SERVICE_SAFE_ENTRY_ADAPTER,
        service_safe_surface_kind=SERVICE_SAFE_ENTRY_SURFACE_KIND,
        product_entry_builder_command=PRODUCT_ENTRY_BUILD_COMMAND,
        product_entry_kind=PRODUCT_ENTRY_KIND,
        supported_entry_modes=list(SUPPORTED_PRODUCT_ENTRY_MODES),
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
