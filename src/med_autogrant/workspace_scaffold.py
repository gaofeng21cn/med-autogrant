from __future__ import annotations

from pathlib import Path
from typing import Any

from med_autogrant import editable_shared_bootstrap as _editable_shared_bootstrap


_editable_shared_bootstrap.ensure_editable_dependency_paths()

from opl_harness_shared.workspace_boundary import (  # noqa: E402
    DEFAULT_WORKSPACE_DOCUMENT,
    WorkspaceScaffoldFile,
    materialize_directory_workspace,
    resolve_workspace_document_path,
)


MAG_WORKSPACE_SCAFFOLD_DIRECTORIES = (
    "artifacts",
    "contracts",
    "drafts",
    "references",
    "runtime",
)
MAG_WORKSPACE_GITIGNORE_ENTRIES = (
    "artifacts/tmp/",
    "runtime/",
    "logs/",
    "tmp/",
)


def resolve_mag_workspace_document_path(input_path: str | Path) -> Path:
    return resolve_workspace_document_path(input_path, default_filename=DEFAULT_WORKSPACE_DOCUMENT)


def resolve_mag_directory_workspace_document_path(workspace_root: str | Path) -> Path:
    return Path(workspace_root).expanduser().resolve() / DEFAULT_WORKSPACE_DOCUMENT


def materialize_mag_directory_workspace(
    *,
    workspace_root: str | Path,
    workspace_document: dict[str, Any],
    initialize_git: bool = True,
) -> dict[str, object]:
    return materialize_directory_workspace(
        workspace_root=workspace_root,
        directories=MAG_WORKSPACE_SCAFFOLD_DIRECTORIES,
        files=(
            WorkspaceScaffoldFile(
                "README.md",
                _render_workspace_readme(workspace_document),
            ),
        ),
        gitignore_entries=MAG_WORKSPACE_GITIGNORE_ENTRIES,
        initialize_git=initialize_git,
    )


def _render_workspace_readme(workspace_document: dict[str, Any]) -> str:
    workspace_id = str(workspace_document.get("workspace_id", "unknown-workspace"))
    grant_run_id = str(workspace_document.get("grant_run_id", "unknown-grant-run"))
    lifecycle_stage = str(workspace_document.get("lifecycle_stage", "unknown-stage"))
    return (
        "# Med Auto Grant Workspace\n"
        "\n"
        f"- workspace_id: `{workspace_id}`\n"
        f"- grant_run_id: `{grant_run_id}`\n"
        f"- lifecycle_stage: `{lifecycle_stage}`\n"
        "\n"
        "`workspace.json` is the canonical Med Auto Grant workspace document. "
        "`contracts/`, `drafts/`, `references/`, and `artifacts/` hold lightweight "
        "authoring truth and deliverables. `runtime/`, `logs/`, and `tmp/` are local "
        "runtime outputs and are ignored by the workspace-local Git boundary.\n"
    )
