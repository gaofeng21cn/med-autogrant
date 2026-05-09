from __future__ import annotations

from typing import Any


DEFAULT_RUNTIME_OWNER = "codex_cli"
DEFAULT_RUNTIME_SUBSTRATE = "codex_cli_default_runtime"
OPTIONAL_HOSTED_CARRIER = "hermes_agent"


def build_default_runtime_summary(*, current_owner_line: str) -> dict[str, Any]:
    return {
        "current_owner_line": current_owner_line,
        "runtime_owner": DEFAULT_RUNTIME_OWNER,
        "optional_carriers": [OPTIONAL_HOSTED_CARRIER],
    }
