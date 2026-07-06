from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from med_autogrant.public_cli import (
    GENERATED_SURFACE_COMMAND_REFS,
    INTERNAL_TO_PUBLIC_COMMAND,
    PUBLIC_COMMAND_GROUP_SUMMARIES,
    PUBLIC_GROUP_COMMANDS,
)


REPO_ROOT = Path(__file__).resolve().parents[2]
SERIES_CONTRACT_PATH = REPO_ROOT / "contracts" / "foundry_agent_series.json"
EXPECTED_OPERATIONS = ("status", "inspect", "interfaces", "validate", "doctor", "peers")
PEER_AGENTS = ("medautoscience", "medautogrant", "redcube", "opl_meta_agent")
ORDINARY_SERIES_SPINE = ("workspace", "work", "stage", "run", "vault", "handoff", "connect")


def build_foundry_series_status() -> dict[str, Any]:
    contract = _read_series_contract()
    return _base_payload(
        contract,
        "foundry-status",
        status={
            "series_label": "OPL Foundry Agent",
            "series_version": contract["version"],
            "foundry_agent_id": contract["foundry_agent_id"],
            "domain_label": contract["domain_label"],
            "authority_owner": contract["authority_owner"],
            "stage_control_plane_ref": contract["stage_control_plane_ref"],
            "ordinary_path": "workspace/work/stage/run/vault/handoff/connect",
            "public_command_surface": "medautogrant foundry",
            "executable_command_surfaces": ["medautogrant"],
            "brand_shorthand": "mag",
            "brand_shorthand_path_safe": False,
        },
    )


def build_foundry_series_inspect() -> dict[str, Any]:
    contract = _read_series_contract()
    profile = _mapping(contract, "domain_specific_profile")
    return _base_payload(
        contract,
        "foundry-inspect",
        inspect={
            "domain_id": contract["domain_id"],
            "domain_aliases": list(contract.get("domain_aliases") or []),
            "domain_pack_kind": _mapping(profile, "mag_domain_input_profile").get("domain_pack_kind"),
            "primary_inputs": list(
                _mapping(profile, "mag_domain_input_profile").get("primary_inputs") or []
            ),
            "primary_outputs": list(
                _mapping(profile, "mag_domain_output_profile").get("primary_outputs") or []
            ),
            "retained_authority": list(profile.get("mag_authority_retained") or []),
            "opl_scope": profile.get("opl_scope"),
        },
    )


def build_foundry_series_interfaces() -> dict[str, Any]:
    contract = _read_series_contract()
    return _base_payload(
        contract,
        "foundry-interfaces",
        interfaces={
            "ordinary_operations": list(EXPECTED_OPERATIONS),
            "ordinary_series_spine": list(ORDINARY_SERIES_SPINE),
            "ordinary_command_spine": list(ORDINARY_SERIES_SPINE),
            "group_summaries": {
                group: PUBLIC_COMMAND_GROUP_SUMMARIES[group] for group in PUBLIC_GROUP_COMMANDS
            },
            "commands_by_group": {
                group: list(commands) for group, commands in PUBLIC_GROUP_COMMANDS.items()
            },
            "generated_surface_refs": dict(GENERATED_SURFACE_COMMAND_REFS),
        },
    )


def build_foundry_series_validate() -> dict[str, Any]:
    contract = _read_series_contract()
    required_fields = tuple(contract["required_identity_fields"])
    missing_fields = [
        field
        for field in required_fields
        if not isinstance(contract.get(field), str) or not str(contract.get(field)).strip()
    ]
    required_packets = tuple(contract["required_stage_packets"])
    missing_command_surface_ops = [
        operation
        for operation in EXPECTED_OPERATIONS
        if INTERNAL_TO_PUBLIC_COMMAND.get(f"foundry-{operation}") != ("foundry", operation)
    ]
    problems = [f"missing_identity_field:{field}" for field in missing_fields]
    problems.extend(
        f"missing_command_surface_operation:{operation}"
        for operation in missing_command_surface_ops
    )
    return _base_payload(
        contract,
        "foundry-validate",
        validation={
            "ok": not problems,
            "checked_identity_fields": list(required_fields),
            "checked_stage_packets": list(required_packets),
            "checked_command_surface_operations": list(EXPECTED_OPERATIONS),
            "problems": problems,
        },
    )


def build_foundry_series_doctor() -> dict[str, Any]:
    contract = _read_series_contract()
    authority = _mapping(contract, "authority_boundary")
    thinning = _mapping(contract, "purpose_first_adapter_thinning_policy")
    return _base_payload(
        contract,
        "foundry-doctor",
        doctor={
            "status": "ok" if authority.get("generated_surface_can_claim_domain_ready") is False else "blocked",
            "series_contract_ref": "contracts/foundry_agent_series.json",
            "shared_policy_release": dict(_mapping(contract, "shared_policy_release")),
            "authority_boundary": dict(authority),
            "default_operator_delta_shape": thinning.get("default_operator_delta_shape"),
            "evidence_tail_boundary": dict(_mapping(thinning, "evidence_tail_boundary")),
        },
    )


def build_foundry_series_peers() -> dict[str, Any]:
    contract = _read_series_contract()
    profile = _mapping(contract, "domain_specific_profile")
    members = tuple(profile.get("series_members") or ())
    return _base_payload(
        contract,
        "foundry-peers",
        peers={
            "series_members": list(members or PEER_AGENTS),
            "current_agent": contract["foundry_agent_id"],
            "domain_profile_defaults": dict(
                _mapping(_mapping(contract, "workspace_topology_profile"), "domain_profile_defaults")
            ),
            "variation_policy": profile.get("series_variation_policy"),
        },
    )


def _read_series_contract() -> dict[str, Any]:
    payload = json.loads(SERIES_CONTRACT_PATH.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("contracts/foundry_agent_series.json must contain a JSON object")
    return payload


def _base_payload(contract: Mapping[str, Any], command: str, **section: Any) -> dict[str, Any]:
    authority_invariants = _mapping(
        _mapping(contract, "series_design_profile"), "authority_invariants"
    )
    payload: dict[str, Any] = {
        "ok": True,
        "command": command,
        "surface_kind": "mag_foundry_agent_series_cli_projection",
        "foundry_agent_series": {
            "surface_kind": contract["surface_kind"],
            "version": contract["version"],
            "product_layer": contract["product_layer"],
            "product_model": contract["product_model"],
            "domain_id": contract["domain_id"],
            "foundry_agent_id": contract["foundry_agent_id"],
            "domain_label": contract["domain_label"],
            "authority_owner": contract["authority_owner"],
            "contract_ref": "contracts/foundry_agent_series.json",
        },
        "authority_boundary": {
            "opl_can_read_domain_body": authority_invariants.get("opl_can_read_domain_body") is True,
            "opl_can_write_domain_truth": authority_invariants.get("opl_can_write_domain_truth") is True,
            "opl_can_authorize_quality_or_export": (
                authority_invariants.get("opl_can_authorize_quality_or_export") is True
            ),
            "domain_owns_truth_quality_artifact_memory_and_receipts": _mapping(
                contract, "authority_boundary"
            ).get("domain_owns_truth_quality_artifact_memory_and_receipts")
            is True,
            "provider_completion_is_closeout": _mapping(
                _mapping(contract, "series_design_profile"), "shared_closeout_contract"
            ).get("provider_completion_is_closeout")
            is True,
        },
    }
    payload.update(section)
    return payload


def _mapping(payload: Mapping[str, Any], key: str) -> Mapping[str, Any]:
    value = payload.get(key)
    if not isinstance(value, Mapping):
        raise ValueError(f"foundry series contract field must be an object: {key}")
    return value
