# Export And Package Gate

## Gate Purpose

This gate decides whether MAG can produce a local submission-ready package and export verdict.

## Evidence To Review

- Quality verdict or review gate receipt.
- Final draft refs, package manifest refs, required sections, required attachments, budget/support material refs, and portal instructions.
- Provenance refs tying package artifacts back to accepted drafts, source evidence, and owner receipts.
- Manual portal boundary and human-supervised submission requirements.
- Exact refs and hashes for the same-generation `artifact-bundle.json`, `final-package.json`, `hosted-contract-bundle.json`, and `submission-ready-package.json` final bytes, used for transport identity and separate release integrity rather than as content-review authority.
- Currentness evaluations for the content, methodology, reference, display, export, and package dependency scopes declared in `contracts/epistemic_review_scope_profile.json`.

## AI/Owner-Backed Judgment Standard

- Submission-ready export requires an identity-bound `opl_stage_review_receipt`, current evidence for every declared semantic scope, separate exact-byte release-integrity evidence, and a MAG-owned package/export verdict or owner receipt.
- Mechanical package completeness is a lower-bound check only.
- Package mutation and release require MAG package authority.

## Forbidden Decision Sources

- Package file presence.
- Generic lifecycle completion.
- OPL provider completion.
- Schema completeness.
- Quality scorecard values without review closure.
- External portal assumptions without human-supervised receipt.

## Required Output

- Terminal reviewer/re-reviewer closeout fields sufficient for the StageRunController to materialize an identity-bound `opl_stage_review_receipt` over the reviewed dependency scopes; and
- A MAG-owned `submission_ready_export_verdict` or owner receipt that consumes that Review receipt and names the current package refs, manual portal boundary, `owner`, `export_verdict_ref`, `source_kind`, and `provenance_ref`; or
- A candidate package or no-output diagnostic with exact missing artifact, quality issue, provenance gap, or manual portal action.

## Final-Byte Review Boundary

- The producer materializes a candidate and cannot close terminal `submission_ready` by self-check or helper success.
- A fresh reviewer must verify the four final artifact identities, then inspect only scopes without current evidence or with changed declared dependencies. A whole-generation hash change is a stale hint, not automatic content, methodology, or reference invalidation.
- Repair inside this Stage is limited to package assembly, manifest, and provenance projection. Proposal content, source evidence, quality-closure, attachment ownership, or export-verdict defects route back to the earliest owning Stage.
- After a local repair, a fresh re-reviewer must inspect the affected dependency scopes. Governance metadata and locator-only changes do not stale epistemic evidence; layout changes stale display evidence; package composition or wrapper changes stale package evidence. Separate release-integrity evidence must always cover the exact rebuilt bytes.
- Producer and repairer output at most `route_impact.stage_route_recommendation`. Under `same_stage_repair_required`, assembly/manifest/provenance repair remains non-terminal and continues this Stage while budget remains. Under `cross_stage_route_back_before_budget_exhaustion`, a reviewer/re-reviewer may return terminal `repair_required + stage_route_decision(decision_kind=route_back)` only when the earliest canonical owner is a different declared Stage; no other pre-exhaustion terminal route is allowed. At final budget with consumable exact bytes, that reviewer/re-reviewer keeps outcome `repair_required` and returns the terminal `route_impact.stage_route_decision`; the controller projects `completed_with_quality_debt`. The controller materializes only `opl_stage_review_receipt`; neither it nor the reviewer signs the MAG owner verdict.

## Quality-Debt And Human-Gate Shapes

- `quality_gate_unclosed`.
- `required_artifact_missing`.
- `export_provenance_missing`.
- `manual_portal_action_required`.
- `mechanical_export_ready_attempted`.

Missing artifacts, quality debt, or provenance gaps close submission-ready/export-ready claims but do not block stage transition. Manual portal action is an explicit human gate. Typed blockers are reserved for unavailable executors, wrong-target identity/currentness, authority/safety/permission/credential boundaries, irreversible actions, or explicit human decisions.

## Pass Condition

Every declared dependency scope is current, the exact current package generation has separate release-integrity evidence, a fresh `opl_stage_review_receipt` covers the scopes reviewed in this StageAttempt, MAG owner authority has consumed the required evidence and recorded the local export/readiness verdict, all provenance is traceable, and no external portal action is silently claimed complete.
