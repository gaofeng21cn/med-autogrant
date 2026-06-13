from __future__ import annotations

import unittest
from unittest.mock import (
    Mock,
    patch,
)

from med_autogrant.domain_runtime_parts.shared import AUTHOR_SIDE_ROUTE_IDS
from med_autogrant.workspace import WorkspaceStateError
from product_entry_cases.support import (
    _expected_route,
    CANONICAL_EXPORT_SURFACES,
    CRITIQUE_EXAMPLE_PATH,
    DOMAIN_ENTRY_COMMAND_CONTRACTS,
    PUBLIC_PRODUCT_ENTRY_BUILDER_COMMAND,
    SUPPORTED_DOMAIN_ENTRY_COMMANDS,
)


class ProductEntryFailureModeTest(unittest.TestCase):
    def test_product_entry_fails_closed_on_blank_task_intent(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        with self.assertRaisesRegex(WorkspaceStateError, "task_intent"):
            MedAutoGrantProductEntry().build(
                input_path=str(CRITIQUE_EXAMPLE_PATH),
                entry_mode="direct",
                task_intent="   ",
            )

    def test_product_entry_rejects_missing_workspace_identity_from_stage_snapshot(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        domain_entry = Mock()
        domain_entry.dispatch.side_effect = [
            {
                "ok": True,
                "grant_run_id": "grant-run-test",
                "workspace_id": None,
                "lifecycle_stage": "critique",
                "verification_checkpoint": {
                    "checkpoint_status": "forward_progress",
                    "identity": {
                        "draft_id": "draft-test",
                    },
                },
                "route": {
                    "next_step": {
                        "recommended_stage": "revision",
                    }
                },
            },
            {
                "grant_run_id": "grant-run-test",
                "workspace_id": "workspace-test",
                "intake_snapshot": {
                    "funding_program": "nsfc-2026-general",
                },
            },
        ]

        with self.assertRaisesRegex(WorkspaceStateError, "workspace_id"):
            MedAutoGrantProductEntry(domain_entry=domain_entry).build(
                input_path=str(CRITIQUE_EXAMPLE_PATH),
                entry_mode="direct",
                task_intent="tighten-grant-mainline",
            )

    def test_product_entry_fails_closed_on_invalid_executor_routing_contract_shape(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        with patch(
            "med_autogrant.product_entry_parts.entry._build_executor_routing_contract",
            return_value={
                "contract_version": 1,
                "current_stage_route": {
                    "route_id": "critique",
                    "route_status": "pending",
                },
            },
            ):
                with self.assertRaises(WorkspaceStateError):
                    MedAutoGrantProductEntry().build(
                        input_path=str(CRITIQUE_EXAMPLE_PATH),
                        entry_mode="direct",
                        task_intent="tighten-grant-mainline",
                    )

    def test_grant_direct_entry_fails_closed_on_mismatched_entry_mode(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        with patch(
            "med_autogrant.product_entry.MedAutoGrantProductEntry.build",
            side_effect=[
                _mismatched_entry_mode_payload(),
                _mismatched_entry_mode_payload(),
            ],
        ):
            with self.assertRaisesRegex(WorkspaceStateError, "grant_direct_entry.direct_entry"):
                MedAutoGrantProductEntry().build_grant_direct_entry(
                    input_path=str(CRITIQUE_EXAMPLE_PATH),
                    task_intent="tighten-grant-mainline",
                )


def _mismatched_entry_mode_payload() -> dict[str, object]:
    return {
        "ok": True,
        "command": "build-product-entry",
        "grant_run_id": "grant-run-test",
        "workspace_id": "workspace-test",
        "draft_id": "draft-test",
        "lifecycle_stage": "critique",
        "input_path": str(CRITIQUE_EXAMPLE_PATH.resolve()),
        "output_path": None,
        "product_entry": _mismatched_product_entry(),
    }


def _mismatched_product_entry() -> dict[str, object]:
    return {
        "entry_version": 1,
        "entry_kind": "med_auto_grant_product_entry",
        "target_domain_id": "med-autogrant",
        "task_intent": "tighten-grant-mainline",
        "entry_mode": "opl-handoff",
        "workspace_locator": {
            "workspace_surface_kind": "nsfc_workspace",
            "workspace_path": str(CRITIQUE_EXAMPLE_PATH.resolve()),
        },
        "runtime_session_contract": _runtime_session_contract_fixture(),
        "return_surface_contract": _return_surface_contract_fixture(),
        "domain_payload": {
            "workspace_id": "workspace-test",
            "draft_id": "draft-test",
            "funding_call": "nsfc-2026-general",
        },
        "stage_snapshot": {
            "lifecycle_stage": "critique",
            "checkpoint_status": "forward_progress",
            "recommended_next_stage": "revision",
        },
        "executor_routing_contract": {
            "contract_version": 1,
            "current_stage_route": _expected_route("critique", source_stage="critique"),
            "recommended_executor_route": _expected_route("revision", source_stage="critique"),
            "author_side_route_catalog": [
                _expected_route(route_id, source_stage=route_id)
                for route_id in AUTHOR_SIDE_ROUTE_IDS
            ],
        },
    }


def _runtime_session_contract_fixture() -> dict[str, object]:
    return {
        "grant_run_id": "grant-run-test",
        "session_handle_kind": "grant_run_id",
        "session_owner": "one-person-lab",
        "generated_session_surface_ref": "opl://generated-surfaces/mag/product-entry-session",
        "generated_resume_surface_ref": "opl://generated-surfaces/mag/product-entry-session#resume",
        "domain_authority_surface_ref": "/product_entry_manifest/owner_receipt_contract",
        "runtime_substrate_contract": {
            "runtime_owner": "configured_family_runtime_provider",
            "current_owner_line": (
                "OPL/Temporal hosted autonomous runtime is the default task runtime; "
                "MAG stays a grant-domain authority surface with Codex CLI as the default stage executor"
            ),
            "active_phase": "P4 mature direct grant product entry",
            "active_tranche": "P4.G authoring-quality-first completion semantics alignment",
            "provenance_oracle": "post-R5A local runtime closeout / stage-led provenance oracle",
            "repo_tracked_current_program_contract": "contracts/runtime-program/current-program.json",
        },
        "runtime_state_contract": {
            "root": "$CODEX_HOME/projects/med-autogrant/runtime-state/",
            "session_state_owner": "one-person-lab",
            "generated_session_surface_ref": "opl://generated-surfaces/mag/product-entry-session",
            "generated_resume_surface_ref": "opl://generated-surfaces/mag/product-entry-session#resume",
            "logs_root": "$CODEX_HOME/projects/med-autogrant/runtime-state/logs/",
            "reports_root": "$CODEX_HOME/projects/med-autogrant/runtime-state/reports/<program_id>/",
            "prompts_root": "$CODEX_HOME/projects/med-autogrant/runtime-state/prompts/",
            "handoff_state_root": "$CODEX_HOME/projects/med-autogrant/runtime-state/handoff_state/",
            "non_repo_tracked": True,
        },
    }


def _return_surface_contract_fixture() -> dict[str, object]:
    return {
        "entry_adapter": "MedAutoGrantDomainEntry",
        "default_formal_entry": "CLI",
        "supported_entry_modes": ["direct", "opl-handoff"],
        "domain_entry_contract": {
            "entry_adapter": "MedAutoGrantDomainEntry",
            "service_safe_surface_kind": "service-safe-domain-entry-command",
            "product_entry_builder_command": PUBLIC_PRODUCT_ENTRY_BUILDER_COMMAND,
            "product_entry_kind": "med_auto_grant_product_entry",
            "supported_entry_modes": ["direct", "opl-handoff"],
            "supported_commands": SUPPORTED_DOMAIN_ENTRY_COMMANDS,
            "command_contracts": DOMAIN_ENTRY_COMMAND_CONTRACTS,
        },
        "checkpoint_aggregation_surface": "stage-route-report",
        "operator_contract": {
            "canonical_audit_surfaces": [
                "validate-workspace",
                "summarize-workspace",
                "grant-intake-audit",
                "grant-evidence-grounding",
                "grant-quality-scorecard",
                "grant-quality-closure-dossier",
                "grant-quality-diff",
                "next-step",
                "critique-summary",
                "stage-route-report",
            ],
            "canonical_export_surfaces": CANONICAL_EXPORT_SURFACES,
            "checkpoint_aggregation_surface": "stage-route-report",
        },
    }
