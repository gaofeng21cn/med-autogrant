from __future__ import annotations

from med_autogrant.public_cli import public_cli_command


def build_source_provenance_surface() -> dict[str, object]:
    return {
        "surface_kind": "source_provenance",
        "summary": (
            "MAG exposes grant-source provenance as OPL-indexable body-free refs only; "
            "these refs do not transfer source truth, workspace intake, runtime, "
            "quality verdict, or export authority to OPL."
        ),
        "source_provenance_ref": {
            "surface_kind": "mag_source_provenance",
            "ref": "docs/source/README.md",
        },
        "historical_fixture_ref": {
            "surface_kind": "mag_historical_fixture_ref",
            "ref": "examples/nsfc_workspace_p2c_critique.json",
        },
        "explicit_archive_import_ref": {
            "surface_kind": "mag_explicit_archive_import_ref",
            "command": public_cli_command(
                "workspace-initialize-intake",
                "--input",
                "<selection_input>",
                "--workspace-root",
                "<workspace_dir>",
                "--format",
                "json",
            ),
        },
        "parity_oracle_ref": {
            "surface_kind": "mag_parity_oracle_ref",
            "ref": "program:mag_declared_grant_pack_source_refs",
        },
        "authority_boundary": [
            "source_refs_do_not_contain_source_body",
            "opl_projection_reads_refs_only",
            "workspace_source_intake_shell_owner_is_one_person_lab",
            "grant_source_truth_owner_is_med_autogrant",
            "fundability_quality_export_verdict_owner_is_med_autogrant",
            "no_runtime_workbench_ledger_or_scheduler_authority_transferred",
        ],
        "capability_classification": "source_provenance_only",
        "recommended_audit_command": public_cli_command(
            "product-entry-manifest",
            "--input",
            "examples/nsfc_workspace_p2c_critique.json",
            "--format",
            "json",
        ),
    }
