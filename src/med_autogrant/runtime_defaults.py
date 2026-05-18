from __future__ import annotations

import os
from typing import Any


DEFAULT_RUNTIME_OWNER = "configured_family_runtime_provider"
DEFAULT_EXECUTOR_OWNER = "codex_cli"
DEFAULT_RUNTIME_SUBSTRATE = "opl_provider_runtime"
OPTIONAL_HOSTED_CARRIER = "hermes_agent"
OPTIONAL_HOSTED_CARRIERS = ("hermes_agent", "claude_code")
OPL_EXECUTOR_ADAPTER_OWNER = "one-person-lab"
OPL_EXECUTOR_ADAPTER_CONTRACT_REF = "contracts/opl-framework/family-executor-adapter-defaults.json"
OPL_AGENT_EXECUTION_REQUEST_CONTRACT = "AgentExecutionRequest"
OPL_AGENT_EXECUTION_RECEIPT_CONTRACT = "AgentExecutionReceipt"
NON_DEFAULT_EXECUTOR_EQUIVALENCE_NOTICE = "connectivity_lifecycle_receipt_audit_only"
DEFAULT_EXECUTOR_EQUIVALENCE_NOTICE = "codex_cli_first_class_default"
DEFAULT_OPL_COMMAND = ("opl",)


def build_default_runtime_summary(*, current_owner_line: str) -> dict[str, Any]:
    return {
        "current_owner_line": current_owner_line,
        "runtime_owner": DEFAULT_RUNTIME_OWNER,
        "optional_carriers": list(OPTIONAL_HOSTED_CARRIERS),
    }


def parse_opl_command(env: dict[str, str] | None = None) -> tuple[str, ...]:
    resolved_env = env or os.environ
    value = str(resolved_env.get("MED_AUTOGRANT_OPL_COMMAND") or "").strip()
    if not value:
        return DEFAULT_OPL_COMMAND
    return tuple(part for part in value.split() if part) or DEFAULT_OPL_COMMAND
