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
    "grant_transition_oracle",
    "grant_native_helper",
}


def test_functional_audit_keeps_eight_distinct_authority_ids() -> None:
    audit = json.loads(
        (REPO_ROOT / "contracts" / "functional_privatization_audit.json").read_text(
            encoding="utf-8"
        )
    )
    modules = {
        item["module_id"]: item
        for item in audit["modules"]
        if item["module_id"] != "mag_declarative_grant_pack"
    }

    assert set(modules) == AUTHORITY_IDS
    assert all(
        item["classification"]
        in {"domain_authority", "minimal_authority_function", "refs_only_domain_adapter"}
        for item in modules.values()
    )


def test_pack_compiler_uses_the_same_eight_authority_ids() -> None:
    pack = json.loads(
        (REPO_ROOT / "contracts" / "pack_compiler_input.json").read_text(encoding="utf-8")
    )

    assert set(pack["minimal_authority_functions"]) == AUTHORITY_IDS
