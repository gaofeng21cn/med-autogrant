from __future__ import annotations

from pathlib import Path
from typing import Any

from med_autogrant.grant_quality import (
    build_grant_quality_closure_dossier,
    build_grant_quality_diff,
    build_grant_quality_scorecard,
)
from med_autogrant.domain_runtime_parts.contracts import (
    validate_contract_schema as _validate_contract_schema,
)
from med_autogrant.domain_runtime_parts.io import _read_active_draft_id
from med_autogrant.domain_runtime_parts.shared import (
    GRANT_QUALITY_CLOSURE_DOSSIER_SCHEMA_FILE,
    GRANT_QUALITY_DIFF_SCHEMA_FILE,
    GRANT_QUALITY_SCORECARD_SCHEMA_FILE,
)


def grant_quality_scorecard(self, *, input_path: str | Path) -> dict[str, Any]:
    document = self._load_workspace(input_path)
    payload = {
        "ok": True,
        "command": "grant-quality-scorecard",
        "grant_run_id": document["grant_run_id"],
        "workspace_id": document["workspace_id"],
        "draft_id": _read_active_draft_id(document),
        "lifecycle_stage": document["lifecycle_stage"],
        "input_path": str(Path(input_path).expanduser().resolve()),
        "grant_quality_scorecard": build_grant_quality_scorecard(document),
    }
    _validate_contract_schema(
        payload,
        schema_file=GRANT_QUALITY_SCORECARD_SCHEMA_FILE,
        context="grant_quality_scorecard",
        grant_run_id=document["grant_run_id"],
        workspace_id=document["workspace_id"],
        lifecycle_stage=document["lifecycle_stage"],
    )
    return payload

def grant_quality_diff(
    self,
    *,
    input_path: str | Path,
    previous_input_path: str | Path,
) -> dict[str, Any]:
    current_document = self._load_workspace(input_path)
    previous_document = self._load_workspace(previous_input_path)
    payload = {
        "ok": True,
        "command": "grant-quality-diff",
        "grant_run_id": current_document["grant_run_id"],
        "workspace_id": current_document["workspace_id"],
        "draft_id": _read_active_draft_id(current_document),
        "lifecycle_stage": current_document["lifecycle_stage"],
        "input_path": str(Path(input_path).expanduser().resolve()),
        "previous_input_path": str(Path(previous_input_path).expanduser().resolve()),
        "grant_quality_diff": build_grant_quality_diff(
            current_document=current_document,
            previous_document=previous_document,
        ),
    }
    _validate_contract_schema(
        payload,
        schema_file=GRANT_QUALITY_DIFF_SCHEMA_FILE,
        context="grant_quality_diff",
        grant_run_id=current_document["grant_run_id"],
        workspace_id=current_document["workspace_id"],
        lifecycle_stage=current_document["lifecycle_stage"],
    )
    return payload

def grant_quality_closure_dossier(self, *, input_path: str | Path) -> dict[str, Any]:
    document = self._load_workspace(input_path)
    payload = {
        "ok": True,
        "command": "grant-quality-closure-dossier",
        "grant_run_id": document["grant_run_id"],
        "workspace_id": document["workspace_id"],
        "draft_id": _read_active_draft_id(document),
        "lifecycle_stage": document["lifecycle_stage"],
        "input_path": str(Path(input_path).expanduser().resolve()),
        "grant_quality_closure_dossier": build_grant_quality_closure_dossier(document),
    }
    _validate_contract_schema(
        payload,
        schema_file=GRANT_QUALITY_CLOSURE_DOSSIER_SCHEMA_FILE,
        context="grant_quality_closure_dossier",
        grant_run_id=document["grant_run_id"],
        workspace_id=document["workspace_id"],
        lifecycle_stage=document["lifecycle_stage"],
    )
    return payload
