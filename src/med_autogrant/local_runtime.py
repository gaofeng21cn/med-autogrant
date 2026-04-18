from __future__ import annotations

from pathlib import Path
from typing import Any

from med_autogrant.hermes_runtime import HermesRuntimeSubstrate, LocalRuntimeStateError


def run_local_runtime(
    *,
    input_path: str | Path,
    journal_path: str | Path | None = None,
    trigger: str = "runtime-run",
) -> dict[str, Any]:
    return HermesRuntimeSubstrate().run_local(
        input_path=input_path,
        journal_path=journal_path,
        trigger=trigger,
    )


def resume_local_runtime(*, journal_path: str | Path) -> dict[str, Any]:
    return HermesRuntimeSubstrate().resume_local(journal_path=journal_path)
