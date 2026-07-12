from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
AUTHORITY_IDS = {
    "fundability_verdict",
    "quality_verdict",
    "export_verdict",
    "package_authority",
    "memory_accept_reject",
    "owner_receipt_signer",
    "grant_native_helper",
}


def test_functional_audit_keeps_seven_distinct_authority_ids() -> None:
    audit = json.loads(
        (REPO_ROOT / "contracts" / "functional_privatization_audit.json").read_text(
            encoding="utf-8"
        )
    )
    modules = {item["module_id"]: item for item in audit["modules"]}

    assert set(modules) == AUTHORITY_IDS
    assert audit["surface_kind"] == "functional_privatization_audit"
    assert audit["schema_version"] == 1
    assert audit["domain_id"] == "med-autogrant"
    assert audit["target_domain_id"] == "med-autogrant"
    assert audit["default_surface_boundary"]["state"] == "physically_absent"
    assert set(audit["retired_default_surface_ids"]) == {
        "product_entry",
        "product_status",
        "product_session",
        "workbench",
    }

    for module_id, item in modules.items():
        expected_layer = (
            "private_platform_residue_inventory"
            if module_id == "grant_native_helper"
            else "authority_function_inventory"
        )
        assert item["classification"] == (
            "refs_only_domain_adapter"
            if module_id == "grant_native_helper"
            else "minimal_authority_function"
        )
        assert item["standardization_layer"] == expected_layer
        assert item["code_paths"]
        assert all((REPO_ROOT / code_path).is_file() for code_path in item["code_paths"])

    retired_provenance = audit["retired_generated_surface_provenance"]
    assert len(retired_provenance) == 3
    assert all(
        entry["surface_id"]
        and entry["replacement_ref"]
        and entry["provenance_refs"]
        for entry in retired_provenance
    )

    bridge_exit_gate = audit["bridge_exit_gate"]
    assert set(bridge_exit_gate) == {
        "physical_delete_authorization_refs",
        "no_forbidden_write_refs",
        "provenance_refs",
    }
    assert all(bridge_exit_gate[field] for field in bridge_exit_gate)

    native_helper = modules["grant_native_helper"]
    assert {
        "src/med_autogrant/cli.py",
        "src/med_autogrant/product_entry_parts/domain_handler.py",
    } <= set(native_helper["current_surface_refs"])
    assert native_helper["bridge_exit_gate"]["keep_as_authority_adapter_refs"]
    assert native_helper["bridge_exit_gate"]["no_forbidden_write_refs"]
    assert native_helper["bridge_exit_gate"]["provenance_refs"]


def test_pack_compiler_uses_the_same_seven_authority_ids() -> None:
    pack = json.loads(
        (REPO_ROOT / "contracts" / "pack_compiler_input.json").read_text(encoding="utf-8")
    )

    assert set(pack["minimal_authority_functions"]) == AUTHORITY_IDS
    assert pack["declarative_domain_pack"]
