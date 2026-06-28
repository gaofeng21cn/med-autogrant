from __future__ import annotations

from collections.abc import Callable
from typing import Any

from med_autogrant.product_entry_parts.consumer_thinning_audit.evidence_gates import (
    build_legacy_exit_gate as _default_build_legacy_exit_gate,
)
from med_autogrant.product_entry_parts.consumer_thinning_audit.model import (
    build_retired_functional_module_audit_item as _default_build_retired_functional_module_audit_item,
)


def build_retire_or_tombstone_surfaces(
    *,
    build_retired_functional_module_audit_item: Callable[..., dict[str, Any]]
    | None = None,
    build_legacy_exit_gate: Callable[..., dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    if build_retired_functional_module_audit_item is None:
        build_retired_functional_module_audit_item = (
            _default_build_retired_functional_module_audit_item
        )
    if build_legacy_exit_gate is None:
        build_legacy_exit_gate = _default_build_legacy_exit_gate

    return [
        build_retired_functional_module_audit_item(
            "closed_default_path_history_index",
            code_paths=[
                "src/med_autogrant/product_entry_parts/functional_closure_skeleton.py:closed_default_path_history_summary",
            ],
            active_callers=[],
            active_caller_status="closed_default_paths_absent_no_active_caller",
            migration_action=(
                "Keep only compact history index refs for closed default paths; explicit non-default "
                "executor use goes through OPL executor adapter refs."
            ),
            retention_reason=(
                "No closed default path remains as active source residue or compatibility surface; "
                "history refs are body-free provenance only."
            ),
            cannot_absorb_reason=(
                "Default runtime ownership must not stay in MAG. Explicit non-default executor "
                "selection remains a separate adapter receipt path, not this closed default path."
            ),
            evidence_refs=[
                (
                    "/product_entry_manifest/physical_skeleton_follow_through/"
                    "closed_default_path_history_summary"
                ),
                "docs/status.md#旧面退役校准",
            ],
        ),
        build_retired_functional_module_audit_item(
            "legacy_local_runtime_history_attempt_record",
            code_paths=[
                "src/med_autogrant/product_entry_parts/local_runtime_journal.py:absent",
                "src/med_autogrant/product_entry_parts/local_attempt_record.py:absent",
                "src/med_autogrant/runtime_journal.py:absent",
            ],
            active_callers=[],
            active_caller_status="legacy_local_runtime_history_attempt_record_absent_no_active_caller",
            migration_action=(
                "Old local runtime history and attempt-record code has been deleted; OPL owns session "
                "records, typed attention queue, wakeup scheduler, and stage-attempt records."
            ),
            retention_reason=(
                "Active MAG source retains refs-only session/runtime locator projections under refs-only "
                "adapter classifications; local runtime history implementation and tests are not retained."
            ),
            cannot_absorb_reason=(
                "The legacy local attempt-record store itself should not be absorbed as MAG-owned code; "
                "OPL should provide the generic stage record surface while MAG keeps safe action refs and "
                "grant next-action meaning."
            ),
            evidence_refs=[
                "/product_entry_manifest/session_continuity",
                "/product_entry_manifest/automation",
                "/domain_handler_export/user_loop_attention_queue",
            ],
            exit_gate=build_legacy_exit_gate(
                gate_id="mag.legacy.local_runtime_history_attempt_record.exit.v1",
                replacement_primitives=[
                    "session_ledger",
                    "typed_queue",
                    "stage_attempt_records",
                ],
                exit_action="delete_or_history_tombstone_local_runtime_history_attempt_record_code",
            ),
        ),
        build_retired_functional_module_audit_item(
            "domain_runtime_patch_bridge",
            code_paths=[
                "src/med_autogrant/domain_runtime.py:absent",
            ],
            active_callers=[],
            active_caller_status="retired_physical_facade_removed_no_active_caller",
            migration_action="Keep only tombstone/provenance; do not add compatibility aliases or re-export facades.",
            retention_reason="The old domain_runtime facade file is absent from active source.",
            cannot_absorb_reason="This is retired compatibility glue, not an OPL primitive to absorb.",
            evidence_refs=[
                "docs/decisions.md#2026-05-14：退役-domain-runtime-facade-patch-bridge",
                "tests/test_domain_runtime_split.py::RuntimeSplitStructureTest::test_runtime_patch_target_bridge_is_retired",
                "tests/test_domain_runtime_split.py::RuntimeSplitStructureTest::test_retired_runtime_facade_is_not_present_in_source",
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
                "src/med_autogrant/cli_parts/legacy_flat_aliases.py:absent",
                "src/med_autogrant/public_cli_flat_aliases.py:absent",
            ],
            active_callers=[],
            active_caller_status="legacy_alias_absent_grouped_cli_is_domain_handler_target",
            migration_action=(
                "Keep grouped product/workspace/pass/package commands classified as direct domain "
                "handler targets; do not keep a legacy flat-alias compatibility surface."
            ),
            retention_reason=(
                "Machine command fields may stay stable in grouped handlers, but retired flat aliases "
                "have no active caller and must not be reintroduced as compatibility commands."
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
                "src/med_autogrant/scheduler_daemon.py:absent",
                "src/med_autogrant/product_entry_parts/scheduler_daemon.py:absent",
                "src/med_autogrant/domain_runtime_parts/scheduler_daemon.py:absent",
            ],
            active_callers=[],
            active_caller_status="legacy_scheduler_daemon_absent_runtime_control_is_refs_only_adapter",
            migration_action=(
                "OPL owns provider scheduler/daemon; MAG keeps any runtime_control projection under "
                "refs-only adapter classifications without local run/resume diagnostics."
            ),
            retention_reason=(
                "Runtime-control metadata remains covered by refs-only adapter entries, not by this "
                "legacy scheduler/daemon tombstone."
            ),
            cannot_absorb_reason=(
                "OPL owns production scheduler/daemon; MAG only exposes grant route and authority refs."
            ),
            evidence_refs=[
                "/product_entry_manifest/mag_consumer_thinning_contract/forbidden_mag_generic_owner_roles",
                "/product_entry_manifest/physical_skeleton_follow_through/active_path_current_role_guard",
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
