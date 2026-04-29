from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from med_autogrant import editable_shared_bootstrap as _editable_shared_bootstrap

_editable_shared_bootstrap.ensure_editable_dependency_paths()

from med_autogrant.domain_entry_contract import (
    build_domain_entry_contract,
    build_gateway_interaction_contract,
    build_shared_handoff,
)
from med_autogrant.mainline_status import read_mainline_status
from med_autogrant.product_entry_parts.orchestration_companions import (
    _build_family_orchestration_companion,
    _build_managed_runtime_contract,
    _build_product_entry_start,
    _route_status_from_route_id,
)
from med_autogrant.product_entry_parts.primitives import (
    GRANT_COCKPIT_KIND,
    GRANT_DIRECT_ENTRY_KIND,
    GRANT_DIRECT_ENTRY_VERSION,
    GRANT_PROGRESS_PROJECTION_KIND,
    GRANT_PROGRESS_PROJECTION_VERSION,
    GRANT_USER_LOOP_KIND,
    GRANT_USER_LOOP_VERSION,
    PRODUCT_ENTRY_KIND,
    PRODUCT_ENTRY_MANIFEST_KIND,
    PRODUCT_ENTRY_VERSION,
    PRODUCT_FRONTDESK_KIND,
    REVIEW_CONTEXT_STAGES,
    SUPPORTED_ENTRY_MODES,
    TARGET_DOMAIN_ID,
    _assert_entry_mode,
    _optional_mapping,
    _optional_string_from_mapping,
    _read_funding_call_from_summary,
    _read_nonempty_string_list,
    _require_entry_mode,
    _require_mapping,
    _require_matching_top_level_identity,
    _require_nonempty_string,
    _require_nonempty_string_from_mapping,
    _require_optional_string,
    _write_product_entry_output,
)
from med_autogrant.product_entry_parts.progress_projection_helpers import (
    _build_author_decision_summary,
    _build_current_stage_summary,
    _build_focus_payload,
    _build_workspace_overview,
    _build_workspace_status,
    _read_next_system_action,
    _read_projection_blockers,
)
from med_autogrant.product_entry_parts.runtime_contracts import (
    GRANT_COCKPIT_SCHEMA_FILE,
    GRANT_DIRECT_ENTRY_SCHEMA_FILE,
    GRANT_PROGRESS_SCHEMA_FILE,
    GRANT_USER_LOOP_SCHEMA_FILE,
    PRODUCT_ENTRY_MANIFEST_SCHEMA_FILE,
    PRODUCT_ENTRY_SCHEMA_FILE,
    PRODUCT_FRONTDESK_SCHEMA_FILE,
    _build_author_side_route_contract,
    _build_executor_routing_contract,
    _build_operator_contract,
    _build_runtime_state_contract,
    _build_runtime_substrate_contract,
    _read_current_program_contract,
    _validate_contract_schema,
    _validate_executor_routing_contract,
)
from med_autogrant.public_cli import public_cli_command, public_command_label
from med_autogrant.workspace import load_workspace_document
from med_autogrant.workspace_types import WorkspaceFileError, WorkspaceStateError
from med_autogrant.workspace_validation import validate_workspace_document

from opl_harness_shared.automation_companions import (
    build_automation_catalog as _build_shared_automation_catalog,
    build_automation_descriptor as _build_shared_automation_descriptor,
)
from opl_harness_shared.family_orchestration import (
    buildFamilyIntakeEvidenceCompanion as _build_shared_family_intake_evidence_companion,
    build_family_product_entry_orchestration as _build_shared_family_product_entry_orchestration,
)
from opl_harness_shared.managed_runtime import build_managed_runtime_contract as _build_shared_managed_runtime_contract
from opl_harness_shared.product_entry_companions import (
    build_family_product_frontdesk_from_manifest as _build_shared_family_product_frontdesk_from_manifest,
    build_family_product_entry_manifest as _build_shared_family_product_entry_manifest,
    build_product_entry_start as _build_shared_product_entry_start,
    build_operator_loop_action_catalog as _build_shared_operator_loop_action_catalog,
    build_product_entry_overview as _build_shared_product_entry_overview,
    build_product_entry_quickstart as _build_shared_product_entry_quickstart,
    build_product_entry_readiness as _build_shared_product_entry_readiness,
    build_product_entry_resume_surface as _build_shared_product_entry_resume_surface,
    build_product_entry_shell_catalog as _build_shared_product_entry_shell_catalog,
    build_product_entry_shell_linked_surface as _build_shared_product_entry_shell_linked_surface,
    collect_family_human_gate_ids as _collect_family_human_gate_ids,
    validate_family_product_frontdesk as _validate_shared_family_product_frontdesk,
    validate_family_product_entry_manifest as _validate_shared_family_product_entry_manifest,
)
from opl_harness_shared.product_entry_program_companions import (
    build_detailed_readiness as _build_shared_detailed_readiness,
    build_product_entry_preflight as _build_shared_product_entry_preflight,
    build_workflow_coverage_item as _build_shared_workflow_coverage_item,
)
from opl_harness_shared.runtime_task_companions import (
    build_runtime_inventory as _build_shared_runtime_inventory,
    build_task_lifecycle as _build_shared_task_lifecycle,
)
from opl_harness_shared.status_narration import (
    PROGRESS_ANSWER_CHECKLIST,
    build_status_narration_contract,
)
from opl_harness_shared.skill_catalog import (
    build_skill_catalog as _build_shared_skill_catalog,
    build_skill_descriptor as _build_shared_skill_descriptor,
)


__all__ = [name for name in globals() if not name.startswith("__")]
