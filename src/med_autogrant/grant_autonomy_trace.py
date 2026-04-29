from __future__ import annotations

from typing import Any


def spend_budget_step(
    *,
    spent_steps: int,
    budget_max: int,
    action_trace: list[dict[str, Any]],
    step_action: str,
    cycle: int | None,
) -> tuple[bool, int]:
    if spent_steps + 1 > budget_max:
        return False, spent_steps
    next_spent_steps = spent_steps + 1
    action_trace.append(
        {
            "step_action": step_action,
            "cycle": cycle,
            "step_index": next_spent_steps,
            "result": "executed",
        }
    )
    return True, next_spent_steps
