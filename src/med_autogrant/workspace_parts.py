from __future__ import annotations

from med_autogrant.workspace_runtime_constraints import _validate_runtime_constraints
from med_autogrant.workspace_stage_validation import (
    _validate_forced_rollback_contract,
    _validate_presubmission_gate_contract,
    _validate_revision_transition_contract,
    _validate_stage_requirements,
)
from med_autogrant.workspace_reference_validation import (
    _collect_known_ids,
    _draft_links_argument_chain,
    _draft_links_fit_mapping,
    _draft_sections_link_object,
    _validate_reference_list,
    _validate_reference_sets,
)

REVIEW_CONTEXT_STAGES = {"critique", "revision", "frozen"}
