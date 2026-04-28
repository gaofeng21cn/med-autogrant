from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

from med_autogrant.hermes_runtime_parts.io import (
    _guard_artifact_bundle_output_identity,
    _write_artifact_bundle_output,
)
from med_autogrant.workspace import WorkspaceStateError, _build_workspace_state


BUNDLE_VERSION = 1
BUNDLE_KIND = "artifact_bundle"


def build_artifact_bundle_document(*, document: dict[str, Any]) -> dict[str, Any]:
    state = _build_workspace_state(document)

    if (
        state.selected_direction is None
        or state.selected_question is None
        or state.active_argument_chain is None
        or state.active_fit_mapping is None
        or state.active_draft is None
    ):
        raise WorkspaceStateError(
            "lifecycle_stage: 当前 workspace 尚未具备 artifact bundle 所需的完整对象上下文。",
            errors=[],
            grant_run_id=document.get("grant_run_id"),
            workspace_id=document.get("workspace_id"),
            lifecycle_stage=document.get("lifecycle_stage"),
        )

    return {
        "bundle_version": BUNDLE_VERSION,
        "bundle_kind": BUNDLE_KIND,
        "grant_run_id": document["grant_run_id"],
        "workspace_id": document["workspace_id"],
        "draft_id": state.active_draft["draft_id"],
        "lifecycle_stage": document["lifecycle_stage"],
        "selection": {
            "selected_direction_id": state.current_selection.get("selected_direction_id"),
            "selected_question_id": state.current_selection.get("selected_question_id"),
            "active_fit_mapping_id": state.current_selection.get("active_fit_mapping_id"),
            "active_draft_id": state.current_selection.get("active_draft_id"),
        },
        "manifest": {
            "direction_id": state.selected_direction["direction_id"],
            "question_id": state.selected_question["question_id"],
            "argument_chain_id": state.active_argument_chain["argument_chain_id"],
            "fit_mapping_id": state.active_fit_mapping["fit_mapping_id"],
            "draft_id": state.active_draft["draft_id"],
            "draft_version_label": state.active_draft["version_label"],
            "draft_status": state.active_draft["status"],
        },
        "lineage": {
            "frozen_question_id": state.active_draft["frozen_question_id"],
            "argument_chain_id": state.active_argument_chain["argument_chain_id"],
            "fit_mapping_id": state.active_fit_mapping["fit_mapping_id"],
            "draft_id": state.active_draft["draft_id"],
        },
        "bundle_summary": {
            "outline_count": len(state.active_draft.get("outline", [])),
            "section_count": len(state.active_draft.get("sections", [])),
        },
        "artifacts": {
            "selected_direction": deepcopy(state.selected_direction),
            "selected_question": deepcopy(state.selected_question),
            "argument_chain": deepcopy(state.active_argument_chain),
            "fit_mapping": deepcopy(state.active_fit_mapping),
            "draft_outline": deepcopy(state.active_draft.get("outline", [])),
            "draft_sections": deepcopy(state.active_draft.get("sections", [])),
        },
    }


def build_artifact_bundle_payload(
    document: dict[str, Any],
    *,
    output_path: str | Path,
) -> dict[str, Any]:
    bundle = build_artifact_bundle_document(document=document)
    resolved_output_path = Path(output_path).expanduser().resolve()
    _guard_output_identity(
        resolved_output_path,
        grant_run_id=bundle["grant_run_id"],
        workspace_id=bundle["workspace_id"],
        draft_id=bundle["draft_id"],
        lifecycle_stage=bundle["lifecycle_stage"],
    )
    _write_bundle(resolved_output_path, bundle)

    return {
        "ok": True,
        "command": "build-artifact-bundle",
        "grant_run_id": bundle["grant_run_id"],
        "workspace_id": bundle["workspace_id"],
        "draft_id": bundle["draft_id"],
        "lifecycle_stage": bundle["lifecycle_stage"],
        "output_path": str(resolved_output_path),
        "bundle": bundle,
    }


def _guard_output_identity(
    output_path: Path,
    *,
    grant_run_id: str,
    workspace_id: str,
    draft_id: str,
    lifecycle_stage: str,
) -> None:
    _guard_artifact_bundle_output_identity(
        output_path,
        grant_run_id=grant_run_id,
        workspace_id=workspace_id,
        draft_id=draft_id,
        lifecycle_stage=lifecycle_stage,
    )


def _write_bundle(output_path: Path, bundle: dict[str, Any]) -> None:
    _write_artifact_bundle_output(output_path, bundle)
