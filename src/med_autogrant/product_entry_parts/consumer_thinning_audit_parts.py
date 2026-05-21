from __future__ import annotations

from collections.abc import Callable
from typing import Any


def build_retire_or_tombstone_surfaces(
    *,
    build_retired_functional_module_audit_item: Callable[..., dict[str, Any]],
    build_legacy_exit_gate: Callable[..., dict[str, Any]],
) -> list[dict[str, Any]]:
    return [
        build_retired_functional_module_audit_item(
            "default_hermes_gateway_local_manager_runtime_owner",
            code_paths=[
                "src/med_autogrant/product_entry_parts/executor_defaults.py",
            ],
            active_callers=[],
            active_caller_status="legacy_runtime_owner_physically_removed",
            migration_action=(
                "Delete old Hermes/Gateway/local-manager runtime owner code; current non-default "
                "executor use must go through explicit OPL executor adapter refs."
            ),
            retention_reason=(
                "Only executor-default guard metadata remains in active source; old runtime owner and "
                "probe code is not retained as a compatibility surface."
            ),
            cannot_absorb_reason=(
                "Default runtime ownership must not stay in MAG. Explicit hermes_agent execution is "
                "modeled separately as an executor adapter receipt path, not a runtime owner."
            ),
            evidence_refs=[
                "/product_entry_manifest/controlled_domain_memory_apply_proof/repo_source_layout_audit",
                "docs/status.md#旧面退役校准",
            ],
        ),
        build_retired_functional_module_audit_item(
            "local_runtime_journal_attempt_ledger",
            code_paths=[
                "src/med_autogrant/product_entry_parts/loop_contracts.py",
                "src/med_autogrant/product_entry_parts/runtime_surfaces.py",
                "src/med_autogrant/hosted_contract_bundle.py",
                "src/med_autogrant/domain_runtime_parts/io.py",
                "src/med_autogrant/domain_runtime_parts/runtime_ops.py",
            ],
            active_callers=[],
            active_caller_status="legacy_local_journal_attempt_ledger_physically_removed",
            migration_action=(
                "Old local journal and attempt ledger code has been deleted; OPL owns session ledger, "
                "typed attention queue, wakeup scheduler, and stage-attempt ledger."
            ),
            retention_reason=(
                "Active MAG source retains only refs-only session/runtime locator surfaces; local journal "
                "implementation and tests are not retained."
            ),
            cannot_absorb_reason=(
                "The legacy local ledger itself should not be absorbed as MAG-owned code; OPL should "
                "provide the generic ledger while MAG keeps safe action refs and grant next-action meaning."
            ),
            evidence_refs=[
                "/product_entry_manifest/session_continuity",
                "/product_entry_manifest/automation",
                "/sidecar_export/user_loop_attention_queue",
            ],
            exit_gate=build_legacy_exit_gate(
                gate_id="mag.legacy.local_runtime_journal_attempt_ledger.exit.v1",
                replacement_primitives=[
                    "session_ledger",
                    "typed_queue",
                    "stage_attempt_ledger",
                ],
                exit_action="delete_or_history_tombstone_local_journal_attempt_ledger_code",
            ),
        ),
        build_retired_functional_module_audit_item(
            "domain_runtime_patch_bridge",
            code_paths=[
                "src/med_autogrant/domain_runtime.py",
            ],
            active_callers=[],
            active_caller_status="retired_no_active_caller_expected",
            migration_action="Remove or keep only tombstone/provenance; do not add compatibility aliases.",
            retention_reason="No active runtime authority should depend on the patch bridge.",
            cannot_absorb_reason="This is retired compatibility glue, not an OPL primitive to absorb.",
            evidence_refs=[
                "docs/decisions.md#2026-05-14：退役-domain-runtime-facade-patch-bridge",
                "tests/test_domain_runtime_split.py::RuntimeSplitStructureTest::test_runtime_patch_target_bridge_is_retired",
                "tests/test_runtime_cli_structural_helpers.py::test_domain_runtime_parts_do_not_depend_on_facade_patch_bridge",
            ],
        ),
        build_retired_functional_module_audit_item(
            "compatibility_only_product_entry_aggregate_test",
            code_paths=["tests/test_product_entry.py"],
            active_callers=[],
            active_caller_status="legacy_aggregate_test_physically_removed_focused_cases_are_replacement_tests",
            migration_action="Keep focused replacement tests; do not classify them as legacy aggregate callers.",
            retention_reason=(
                "The aggregate compatibility test entry is gone; focused tests protect current "
                "machine-readable contracts."
            ),
            cannot_absorb_reason="Testing layout is repo-local hygiene, not a generic OPL runtime primitive.",
            evidence_refs=[
                "tests/test_product_entry.py:absent",
                "tests/product_entry_cases/:focused_replacement_tests",
            ],
        ),
        build_retired_functional_module_audit_item(
            "legacy_flat_shell_aliases",
            code_paths=[
                "src/med_autogrant/cli_parts/parser_adders.py",
                "src/med_autogrant/cli_parts/handlers.py",
                "src/med_autogrant/public_cli.py",
            ],
            active_callers=["grouped public command tokens"],
            active_caller_status="legacy_alias_retired_grouped_commands_active",
            migration_action="Route callers to grouped product/workspace/pass/package commands.",
            retention_reason=(
                "Machine command fields may stay stable, but user-facing flat aliases should not."
            ),
            cannot_absorb_reason="Flat aliases are retired local CLI surface, not a reusable OPL primitive.",
            evidence_refs=[
                "/product_entry_manifest/ideal_state_closure_status/direct_retirement_posture",
                "docs/status.md#旧面退役校准",
            ],
        ),
        build_retired_functional_module_audit_item(
            "repo_owned_scheduler_daemon",
            code_paths=[
                "src/med_autogrant/runtime_defaults.py",
                "src/med_autogrant/domain_runtime_parts/substrate.py",
                "src/med_autogrant/product_entry_parts/runtime_surfaces.py",
            ],
            active_callers=[
                "product-entry runtime_control refs projection",
            ],
            active_caller_status="legacy_scheduler_daemon_physically_removed_refs_only_runtime_control",
            migration_action=(
                "OPL owns provider scheduler/daemon; MAG keeps refs-only runtime_control projection "
                "without local run/resume diagnostics."
            ),
            retention_reason=(
                "Runtime-control metadata remains a refs-only projection, not a daemon or scheduler."
            ),
            cannot_absorb_reason=(
                "OPL owns production scheduler/daemon; MAG only exposes grant route and authority refs."
            ),
            evidence_refs=[
                "/product_entry_manifest/mag_consumer_thinning_contract/forbidden_mag_generic_owner_roles",
                "/product_entry_manifest/physical_skeleton_follow_through/active_path_scan_no_legacy_default_caller",
            ],
            exit_gate=build_legacy_exit_gate(
                gate_id="mag.legacy.repo_owned_scheduler_daemon.exit.v1",
                replacement_primitives=[
                    "generic_scheduler_daemon",
                    "provider_daemon",
                    "repair_command_projection",
                ],
                exit_action="delete_or_history_tombstone_repo_owned_scheduler_daemon_surface",
            ),
        ),
    ]
