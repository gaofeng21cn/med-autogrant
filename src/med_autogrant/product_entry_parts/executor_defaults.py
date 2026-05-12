from __future__ import annotations

from typing import Any

from med_autogrant.runtime_defaults import (
    DEFAULT_EXECUTOR_OWNER,
    NON_DEFAULT_EXECUTOR_EQUIVALENCE_NOTICE,
    OPL_AGENT_EXECUTION_RECEIPT_CONTRACT,
    OPL_AGENT_EXECUTION_REQUEST_CONTRACT,
    OPL_EXECUTOR_ADAPTER_CONTRACT_REF,
    OPL_EXECUTOR_ADAPTER_OWNER,
)


def build_executor_defaults_surface() -> dict[str, Any]:
    return {
        "surface_kind": "mag_opl_executor_defaults",
        "default_executor_name": DEFAULT_EXECUTOR_OWNER,
        "default_executor_mode": "autonomous",
        "default_model": "inherit_local_codex_default",
        "default_reasoning_effort": "inherit_local_codex_default",
        "canonical_executor_backends": ["codex_cli", "hermes_agent", "claude_code"],
        "executor_registry": {
            "surface_kind": "opl_agent_executor_registry",
            "request_contract": OPL_AGENT_EXECUTION_REQUEST_CONTRACT,
            "receipt_contract": OPL_AGENT_EXECUTION_RECEIPT_CONTRACT,
            "default_resolution_order": [
                "cli_flag",
                "stage_attempt_input",
                "OPL_EXECUTOR_KIND",
                DEFAULT_EXECUTOR_OWNER,
            ],
            "non_default_equivalence": NON_DEFAULT_EXECUTOR_EQUIVALENCE_NOTICE,
        },
        "executor_labels": {
            "codex_cli": "Codex CLI",
            "hermes_agent": "Hermes-Agent",
            "claude_code": "Claude Code",
        },
        "executor_statuses": {
            "codex_cli": "default",
            "hermes_agent": "experimental",
            "claude_code": "experimental",
        },
        "guardrails": {
            "chat_completion_only_executor_forbidden": True,
            "hermes_agent_requires_full_agent_loop": True,
            "non_default_executor_requires_explicit_selection": True,
            "non_default_executor_forbids_silent_codex_fallback": True,
            "fallback_allowed": False,
            "domain_truth_stays_mag_owned": True,
        },
        "adapter_owner": OPL_EXECUTOR_ADAPTER_OWNER,
        "adapter_contract_ref": OPL_EXECUTOR_ADAPTER_CONTRACT_REF,
    }
