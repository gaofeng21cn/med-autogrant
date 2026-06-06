from __future__ import annotations

from pathlib import Path

# Keep the historical module path importable while loading focused audit parts below.
__path__ = [str(Path(__file__).with_suffix(""))]

from med_autogrant.product_entry_parts.consumer_thinning_audit_parts.classification import (
    build_declarative_pack_surfaces,
    build_mag_owned_grant_authority_surfaces,
    build_refs_only_adapter_surfaces,
)
from med_autogrant.product_entry_parts.consumer_thinning_audit_parts.evidence_gates import (
    build_default_caller_deletion_bridge_exit_gate,
    build_legacy_exit_gate,
)
from med_autogrant.product_entry_parts.consumer_thinning_audit_parts.model import (
    build_functional_module_audit_item,
    build_retired_functional_module_audit_item,
)
from med_autogrant.product_entry_parts.consumer_thinning_audit_parts.report import (
    build_privatized_functional_module_audit,
)
from med_autogrant.product_entry_parts.consumer_thinning_audit_parts.retired_surfaces import (
    build_retire_or_tombstone_surfaces,
)

__all__ = [
    "build_declarative_pack_surfaces",
    "build_default_caller_deletion_bridge_exit_gate",
    "build_functional_module_audit_item",
    "build_legacy_exit_gate",
    "build_mag_owned_grant_authority_surfaces",
    "build_privatized_functional_module_audit",
    "build_refs_only_adapter_surfaces",
    "build_retire_or_tombstone_surfaces",
    "build_retired_functional_module_audit_item",
]
