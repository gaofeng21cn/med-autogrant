from __future__ import annotations

from typing import Any

MAG_WORKSPACE_DIRECTORIES = (
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


def render_mag_workspace_readme(workspace_document: dict[str, Any]) -> str:
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
