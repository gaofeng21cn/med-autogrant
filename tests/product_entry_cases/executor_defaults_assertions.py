from __future__ import annotations

from typing import Any, Mapping


def assert_executor_defaults(testcase: Any, executor_defaults: Mapping[str, Any]) -> None:
    testcase.assertEqual(executor_defaults["surface_kind"], "mag_opl_executor_defaults")
    testcase.assertEqual(executor_defaults["default_executor_name"], "codex_cli")
    testcase.assertEqual(
        executor_defaults["canonical_executor_backends"],
        ["codex_cli", "hermes_agent", "claude_code"],
    )
    testcase.assertEqual(executor_defaults["executor_registry"]["surface_kind"], "opl_agent_executor_registry")
    testcase.assertEqual(executor_defaults["executor_registry"]["request_contract"], "AgentExecutionRequest")
    testcase.assertEqual(executor_defaults["executor_registry"]["receipt_contract"], "AgentExecutionReceipt")
    testcase.assertEqual(
        executor_defaults["executor_registry"]["non_default_equivalence"],
        "connectivity_lifecycle_receipt_audit_only",
    )
    testcase.assertTrue(executor_defaults["guardrails"]["non_default_executor_requires_explicit_selection"])
    testcase.assertTrue(executor_defaults["guardrails"]["non_default_executor_forbids_silent_codex_fallback"])
    testcase.assertFalse(executor_defaults["guardrails"]["fallback_allowed"])
    testcase.assertEqual(executor_defaults["adapter_owner"], "one-person-lab")
