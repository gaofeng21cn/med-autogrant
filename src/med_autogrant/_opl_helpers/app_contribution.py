"""Host-neutral App Contribution boundary helpers for Med Auto Grant."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
import os
from pathlib import Path
from typing import Any


class AppContributionError(ValueError):
    """Domain-neutral App contribution validation or boundary error."""

    def __init__(self, message: str, *, reason_code: str = "app_contribution_invalid") -> None:
        super().__init__(message)
        self.reason_code = reason_code


def resolve_workspace_root(workspace: str | None = None, *, env_var: str = "OPL_PROFILE_WORKSPACE") -> Path | None:
    """Resolve explicit workspace or env workspace cleanly; return None if unset or non-absolute."""

    selected = workspace if workspace is not None else os.environ.get(env_var, "")
    if not selected or not Path(selected).is_absolute():
        return None
    return Path(selected).resolve(strict=True)


def verify_work_item_identity(
    input_value: Mapping[str, Any],
    *,
    expected_agent_ids: Iterable[str] = (),
    expected_domain_ids: Iterable[str] = (),
    require_resolved: bool = True,
) -> tuple[dict[str, Any], str | None]:
    """Validate optional `work_item_identity` envelope and extract domain work-item id."""

    identity = input_value.get("work_item_identity") or {}
    if not isinstance(identity, dict):
        raise AppContributionError("work_item_identity must be an object.")
    if not identity:
        return {}, None
    allowed_agents = set(expected_agent_ids)
    allowed_domains = set(expected_domain_ids)
    if require_resolved and identity.get("identity_state") != "resolved":
        raise AppContributionError("work_item_identity must have identity_state 'resolved'.")
    if allowed_agents and identity.get("agent_id") not in allowed_agents:
        raise AppContributionError("work_item_identity agent_id does not match the selected package.")
    if allowed_domains and identity.get("domain_id") not in allowed_domains:
        raise AppContributionError("work_item_identity domain_id does not match the selected package.")
    work_item_id = identity.get("domain_work_item_id") or identity.get("work_item_id")
    return identity, str(work_item_id) if isinstance(work_item_id, str) and work_item_id else None
