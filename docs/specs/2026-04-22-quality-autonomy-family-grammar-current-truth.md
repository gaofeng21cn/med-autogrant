# Quality Governance, Autonomy Controller, And Family Grammar Current Truth

Owner: `Med Auto Grant`
Purpose: `quality_autonomy_family_grammar_active_spec`
State: `active_current_spec`
Machine boundary: 本文是人读 active spec，只冻结 quality governance、autonomy controller 与 family grammar 边界。当前产品状态、runtime owner、App/workbench 和 evidence gate 继续归核心五件套、active gap plan、contracts/schema/source 与 `contracts/runtime-program/current-program.json`。
Date: `2026-04-22`

## Landed Scope

- `grant-quality-scorecard` is a formal quality governance surface for a current workspace version.
- `grant-quality-closure-dossier` is a formal closure surface derived from the current quality scorecard.
- `grant-quality-diff` is a formal comparison surface for two workspace versions.
- `execute-grant-autonomy-controller` is a formal long-horizon controller command that can start from `workspace`, `selection_input`, or `discovery_input`, then schedule existing discovery, profile selection, intake initialization, authoring mainline, and quality evaluation callbacks.
- `execute-critique-revision-loop` and `execute-authoring-mainline-loop` now emit `grant_quality_scorecard` plus `grant_quality_closure_dossier` directly in their loop reports.
- `grant-autonomy-controller-report` now carries dossier-driven planning state: `latest_quality_closure_dossier`, `closure_package_queue`, `active_closure_package`, and per-tranche quality summary / active-package refs.
- `grant_family_registry.py` plus `grant_governance_adapter.py` own the common grant grammar / family profile split and the family-aware governance adapter for profile presets and non-NSFC placeholders.

## Quality Contract

The quality scorecard is schema-backed by `schemas/v1/grant-quality-scorecard.schema.json`.
It covers scientific question validity, necessity/value closure, applicant fit, technical feasibility, claim-evidence coverage, unresolved hard issues, and version issue closure.
It emits structured tracked issues, evidence gaps, unresolved hard issues, and a loop gate that can force rollback or block a stop decision.
Each tracked issue now also carries a formal `lineage_id` plus `lineage_basis`, so quality governance can compare issue continuity through revision rounds without depending only on the current wording of the issue summary.

The quality diff is schema-backed by `schemas/v1/grant-quality-diff.schema.json`.
It reports score deltas, dimension deltas, closed issues, remaining open issues, and newly opened issues.
It compares open issues by lineage first, then surfaces per-version `previous_issue_id` / `current_issue_id` and `previous_summary` / `current_summary`, so a rephrased but still-open hard issue remains part of the same closure line instead of being misreported as a close-and-reopen pair.

The quality closure dossier is schema-backed by `schemas/v1/grant-quality-closure-dossier.schema.json`.
It is derived directly from the scorecard instead of introducing a second scoring path.
It emits `quality_summary`, `evidence_supply_queue_summary`, and `closure_packages`, where each closure package is keyed by issue lineage or queue-only gap id and carries the action, target stage, required inputs, evidence refs, blocking reasons, evidence obligations, and acceptance signals needed to close that package.
The critique-loop and mainline-loop reports now embed this same scorecard plus dossier surface, so each loop round/cycle exposes the same quality ledger instead of only a route decision summary.

## Autonomy Contract

The controller input and report are schema-backed by:

- `schemas/v1/grant-autonomy-controller-input.schema.json`
- `schemas/v1/grant-autonomy-controller-report.schema.json`

The report is fail-closed: success returns a `submission_grade_candidate` or `near_submission_candidate`; failure returns a structured blocker report, unresolved blocker queue, evidence gap queue, action trace, and reselection / rollback decisions.
Within MAG's current task boundary, `near_submission_candidate` and `submission_grade_candidate` mean the narrative is scientifically reviewable for applicant-side inspection. They do not imply that every administrative supplement, portal form, signature, or local `submission-ready` export prerequisite is already complete.
Objective supplements and formality-review items therefore stay on a TODO / explicit wake-up follow-up line unless their absence directly invalidates scientific claims already used in the current narrative.
The controller now also supports `start.mode=controller_report`, so a later run can resume from a prior report instead of restarting from workspace / selection / discovery inputs.
The report now emits `controller_checkpoint`, which freezes the resume start mode, workspace identity, completed cycle count, and next controller action as a stable checkpoint surface.
The controller now consumes `grant_quality_closure_dossier` as its primary quality-planning input, prioritizes a formal closure package queue, and records the active closure package plus quality summary in `controller_plan`, `decision_basis`, and `tranche_history`.

## Family Grammar Contract

`grant_family_registry.py` separates common grant grammar from funder-specific profile choices.
`grant_governance_adapter.py` now hydrates controller defaults and closure-package ordering from the workspace family governance policy, so family-specific stop targets, rollback preference, and governance entry points are consumed through one adapter surface rather than controller-local branching.
Discovery and profile selection remain the place where MAG can compare compatible grant families before a task is locked. Once the caller or selected workspace has explicitly locked a target family, downstream controller and human-gate semantics stay within that grant task instead of opportunistically switching funders mid-authoring.
The landed registry now preserves NSFC, NIH R21, and Wellcome Discovery admitted profile behavior, while still keeping a formal Wellcome discovery placeholder so future funder additions can land through family profile / review grammar / template strategy rather than a rewritten process.
