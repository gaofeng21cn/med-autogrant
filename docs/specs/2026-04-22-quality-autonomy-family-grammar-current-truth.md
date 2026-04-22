# Quality Governance, Autonomy Controller, And Family Grammar Current Truth

Date: `2026-04-22`

## Landed Scope

- `grant-quality-scorecard` is a formal quality governance surface for a current workspace version.
- `grant-quality-diff` is a formal comparison surface for two workspace versions.
- `execute-grant-autonomy-controller` is a formal long-horizon controller command that can start from `workspace`, `selection_input`, or `discovery_input`, then schedule existing discovery, profile selection, intake initialization, authoring mainline, and quality evaluation callbacks.
- `grant_family_registry.py` owns the common grant grammar / family profile split for profile presets and non-NSFC placeholders.

## Quality Contract

The quality scorecard is schema-backed by `schemas/v1/grant-quality-scorecard.schema.json`.
It covers scientific question validity, necessity/value closure, applicant fit, technical feasibility, claim-evidence coverage, unresolved hard issues, and version issue closure.
It emits structured tracked issues, evidence gaps, unresolved hard issues, and a loop gate that can force rollback or block a stop decision.
Each tracked issue now also carries a formal `lineage_id` plus `lineage_basis`, so quality governance can compare issue continuity through revision rounds without depending only on the current wording of the issue summary.

The quality diff is schema-backed by `schemas/v1/grant-quality-diff.schema.json`.
It reports score deltas, dimension deltas, closed issues, remaining open issues, and newly opened issues.
It compares open issues by lineage first, then surfaces per-version `previous_issue_id` / `current_issue_id` and `previous_summary` / `current_summary`, so a rephrased but still-open hard issue remains part of the same closure line instead of being misreported as a close-and-reopen pair.

## Autonomy Contract

The controller input and report are schema-backed by:

- `schemas/v1/grant-autonomy-controller-input.schema.json`
- `schemas/v1/grant-autonomy-controller-report.schema.json`

The report is fail-closed: success returns a `submission_grade_candidate` or `near_submission_candidate`; failure returns a structured blocker report, unresolved blocker queue, evidence gap queue, action trace, and reselection / rollback decisions.

## Family Grammar Contract

`grant_family_registry.py` separates common grant grammar from funder-specific profile choices.
The landed registry now preserves NSFC, NIH R21, and Wellcome Discovery admitted profile behavior, while still keeping a formal Wellcome discovery placeholder so future funder additions can land through family profile / review grammar / template strategy rather than a rewritten process.
