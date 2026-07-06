from __future__ import annotations

from pathlib import Path
from typing import Any

from med_autogrant.domain_entry_contract import build_domain_entry_contract
from med_autogrant.product_entry_parts.primitives import (
    PRODUCT_ENTRY_KIND,
    PRODUCT_ENTRY_VERSION,
    SUPPORTED_ENTRY_MODES,
    TARGET_DOMAIN_ID,
    _read_funding_call_from_summary,
    _require_entry_mode,
    _require_mapping,
    _require_nonempty_string,
    _require_nonempty_string_from_mapping,
    _require_optional_string,
    _write_product_entry_output,
)
from med_autogrant.product_entry_parts.runtime_contracts import (
    PRODUCT_ENTRY_SCHEMA_FILE,
    _build_executor_routing_contract,
    _build_operator_contract,
    _build_runtime_state_contract,
    _build_runtime_substrate_contract,
    _read_current_program_contract,
    _validate_contract_schema,
    _validate_executor_routing_contract,
)
from med_autogrant.product_entry_parts.runtime_surfaces import (
    DOMAIN_AUTHORITY_SURFACE_REF,
    GENERATED_SESSION_RESUME_SURFACE_REF,
    GENERATED_SESSION_SURFACE_REF,
    _build_default_runtime_continuity_surfaces,
)
from med_autogrant.domain_entry import MedAutoGrantDomainEntry
from med_autogrant.workspace_types import WorkspaceStateError
from med_autogrant.product_entry_parts.progress import ProductEntryProgressMixin
from med_autogrant.product_entry_parts.manifest import ProductEntryManifestMixin
from med_autogrant.product_entry_parts.preflight import ProductEntryPreflightMixin
from med_autogrant.product_entry_parts.evidence import ProductEntryEvidenceMixin
from med_autogrant.product_entry_parts.domain_handler import build_domain_handler_export, dispatch_domain_handler_task


class MedAutoGrantProductEntry(
    ProductEntryProgressMixin,
    ProductEntryManifestMixin,
    ProductEntryPreflightMixin,
    ProductEntryEvidenceMixin,
):
    """轻量 grant product entry 壳，复用已 landed 的 domain entry 与默认 runtime contract。"""

    def __init__(self, *, domain_entry: Any | None = None) -> None:
        self._domain_entry = domain_entry or MedAutoGrantDomainEntry()

    def build(
        self,
        *,
        input_path: str | Path,
        entry_mode: str,
        task_intent: str,
        output_path: str | Path | None = None,
        funding_call: str | None = None,
    ) -> dict[str, Any]:
        resolved_input_path = Path(input_path).expanduser().resolve()
        resolved_entry_mode = _require_entry_mode(entry_mode)
        resolved_task_intent = _require_nonempty_string(task_intent, field_name="task_intent")

        route_report = self._domain_entry.dispatch(
            {
                "command": "stage-route-report",
                "input_path": str(resolved_input_path),
            }
        )
        if route_report.get("ok") is not True:
            raise WorkspaceStateError("product entry 只允许从已验证通过的 workspace 构建。")

        workspace_summary = self._domain_entry.dispatch(
            {
                "command": "summarize-workspace",
                "input_path": str(resolved_input_path),
            }
        )

        grant_run_id = _require_nonempty_string_from_mapping(
            route_report,
            "grant_run_id",
            context="stage-route-report",
        )
        workspace_id = _require_nonempty_string_from_mapping(
            route_report,
            "workspace_id",
            context="stage-route-report",
        )
        lifecycle_stage = _require_nonempty_string_from_mapping(
            route_report,
            "lifecycle_stage",
            context="stage-route-report",
        )
        verification_checkpoint = _require_mapping(
            route_report,
            "verification_checkpoint",
            context="stage-route-report",
        )
        checkpoint_status = _require_nonempty_string_from_mapping(
            verification_checkpoint,
            "checkpoint_status",
            context="stage-route-report.verification_checkpoint",
        )
        identity = _require_mapping(
            verification_checkpoint,
            "identity",
            context="stage-route-report.verification_checkpoint",
        )
        draft_id = _require_optional_string(identity.get("draft_id"), field_name="draft_id")

        route = _require_mapping(route_report, "route", context="stage-route-report")
        next_step = _require_mapping(route, "next_step", context="stage-route-report.route")
        recommended_next_stage = _require_nonempty_string_from_mapping(
            next_step,
            "recommended_stage",
            context="stage-route-report.route.next_step",
        )

        resolved_funding_call = (
            _require_nonempty_string(funding_call, field_name="funding_call")
            if funding_call is not None
            else _read_funding_call_from_summary(workspace_summary)
        )

        current_program_contract = _read_current_program_contract()
        executor_routing_contract = _build_executor_routing_contract(
            current_stage=lifecycle_stage,
            recommended_next_stage=recommended_next_stage,
            include_route_catalog=True,
        )
        _validate_executor_routing_contract(
            executor_routing_contract,
            current_stage=lifecycle_stage,
            recommended_next_stage=recommended_next_stage,
            include_route_catalog=True,
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )
        progress_payload = self.read_grant_progress(input_path=resolved_input_path)
        progress_projection = _require_mapping(
            progress_payload,
            "progress_projection",
            context="build-product-entry.grant_progress",
        )
        continuity_surfaces = _build_default_runtime_continuity_surfaces(
            resolved_input_path=resolved_input_path,
            resolved_task_intent=resolved_task_intent,
            progress_projection=progress_projection,
            workspace_summary=workspace_summary,
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )
        product_entry = {
            "entry_version": PRODUCT_ENTRY_VERSION,
            "entry_kind": PRODUCT_ENTRY_KIND,
            "target_domain_id": TARGET_DOMAIN_ID,
            "task_intent": resolved_task_intent,
            "entry_mode": resolved_entry_mode,
            "workspace_locator": {
                "workspace_surface_kind": "nsfc_workspace",
                "workspace_path": str(resolved_input_path),
            },
            "runtime_session_contract": {
                "grant_run_id": grant_run_id,
                "session_handle_kind": "grant_run_id",
                "session_owner": "one-person-lab",
                "generated_session_surface_ref": GENERATED_SESSION_SURFACE_REF,
                "generated_resume_surface_ref": GENERATED_SESSION_RESUME_SURFACE_REF,
                "domain_authority_surface_ref": DOMAIN_AUTHORITY_SURFACE_REF,
                "runtime_substrate_contract": _build_runtime_substrate_contract(
                    current_program_contract=current_program_contract,
                ),
                "runtime_state_contract": _build_runtime_state_contract(),
            },
            "return_surface_contract": {
                "entry_adapter": "MedAutoGrantDomainEntry",
                "default_formal_entry": "CLI",
                "supported_entry_modes": list(SUPPORTED_ENTRY_MODES),
                "domain_entry_contract": build_domain_entry_contract(),
                "checkpoint_aggregation_surface": "stage-route-report",
                "operator_contract": _build_operator_contract(),
                "session_continuity": dict(continuity_surfaces["session_continuity"]),
                "progress_projection": dict(continuity_surfaces["progress_projection"]),
                "artifact_inventory": dict(continuity_surfaces["artifact_inventory"]),
                "runtime_control": dict(continuity_surfaces["runtime_control"]),
            },
            "domain_payload": {
                "workspace_id": workspace_id,
                "draft_id": draft_id,
                "funding_call": resolved_funding_call,
            },
            "stage_snapshot": {
                "lifecycle_stage": lifecycle_stage,
                "checkpoint_status": checkpoint_status,
                "recommended_next_stage": recommended_next_stage,
            },
            "executor_routing_contract": executor_routing_contract,
        }
        _validate_contract_schema(
            product_entry,
            schema_file=PRODUCT_ENTRY_SCHEMA_FILE,
            context="product_entry",
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )

        resolved_output_path = None
        if output_path is not None:
            resolved_output_path = Path(output_path).expanduser().resolve()
            _write_product_entry_output(resolved_output_path, product_entry)

        return {
            "ok": True,
            "command": "build-product-entry",
            "grant_run_id": grant_run_id,
            "workspace_id": workspace_id,
            "draft_id": draft_id,
            "lifecycle_stage": lifecycle_stage,
            "input_path": str(resolved_input_path),
            "output_path": str(resolved_output_path) if resolved_output_path is not None else None,
            "product_entry": product_entry,
        }

    def build_domain_handler_export(self, *, input_path: str | Path) -> dict[str, Any]:
        return build_domain_handler_export(self, input_path=input_path)

    def dispatch_domain_handler_task(self, *, task_path: str | Path) -> dict[str, Any]:
        return dispatch_domain_handler_task(self, task_path=task_path)
