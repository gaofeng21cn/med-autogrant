from __future__ import annotations

from typing import Any, Mapping

from med_autogrant.product_entry_parts.domain_agent_skeleton import (
    build_domain_memory_descriptor_locator,
)
from med_autogrant.product_entry_parts.domain_memory_runtime import (
    build_domain_memory_operator_projection_contract,
)
from med_autogrant.product_entry_parts.primitives import (
    _optional_string_from_mapping,
    _require_nonempty_string_from_mapping,
)


def build_manifest_domain_memory_descriptor_locator(
    *,
    progress_payload: Mapping[str, Any],
    verification_identity: Mapping[str, Any],
) -> dict[str, Any]:
    return build_domain_memory_descriptor_locator(
        grant_run_id=_require_nonempty_string_from_mapping(
            progress_payload,
            "grant_run_id",
            context="grant-progress",
        ),
        workspace_id=_require_nonempty_string_from_mapping(
            progress_payload,
            "workspace_id",
            context="grant-progress",
        ),
        draft_id=_optional_string_from_mapping(verification_identity, "draft_id"),
        lifecycle_stage=_require_nonempty_string_from_mapping(
            progress_payload,
            "lifecycle_stage",
            context="grant-progress",
        ),
        operator_receipt_projection=build_domain_memory_operator_projection_contract(),
    )
