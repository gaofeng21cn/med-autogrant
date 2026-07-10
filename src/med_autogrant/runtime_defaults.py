from __future__ import annotations

import os
from typing import Any


DEFAULT_RUNTIME_OWNER = "configured_family_runtime_provider"
DEFAULT_TASK_RUNTIME_OWNER = "one-person-lab"
DEFAULT_EXECUTOR_OWNER = "codex_cli"
DEFAULT_RUNTIME_SUBSTRATE = "temporal"
OPTIONAL_HOSTED_CARRIERS = ("hermes_agent", "claude_code")
OPL_EXECUTOR_ADAPTER_OWNER = "one-person-lab"
OPL_EXECUTOR_ADAPTER_CONTRACT_REF = "contracts/opl-framework/family-executor-adapter-defaults.json"
OPL_AGENT_EXECUTION_REQUEST_CONTRACT = "AgentExecutionRequest"
OPL_AGENT_EXECUTION_RECEIPT_CONTRACT = "AgentExecutionReceipt"
NON_DEFAULT_EXECUTOR_EQUIVALENCE_NOTICE = "connectivity_lifecycle_receipt_audit_only"
DEFAULT_OPL_COMMAND = ("opl",)


def build_default_runtime_summary(*, current_owner_line: str) -> dict[str, Any]:
    return {
        "current_owner_line": current_owner_line,
        "runtime_owner": DEFAULT_RUNTIME_OWNER,
        "default_task_runtime_owner": DEFAULT_TASK_RUNTIME_OWNER,
        "default_runtime_substrate": DEFAULT_RUNTIME_SUBSTRATE,
        "opl_temporal_hosted_autonomy_default": True,
        "default_stage_executor": DEFAULT_EXECUTOR_OWNER,
        "mag_implements_daemon": False,
        "mag_implements_scheduler": False,
        "mag_implements_attempt_loop": False,
        "mag_owns_attempt_ledger": False,
        "optional_carriers": list(OPTIONAL_HOSTED_CARRIERS),
    }


def parse_opl_command(env: dict[str, str] | None = None) -> tuple[str, ...]:
    resolved_env = env or os.environ
    value = str(resolved_env.get("MED_AUTOGRANT_OPL_COMMAND") or "").strip()
    if not value:
        return DEFAULT_OPL_COMMAND
    return tuple(part for part in value.split() if part) or DEFAULT_OPL_COMMAND
