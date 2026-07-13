# Export And Package Gate

## Gate Purpose

This gate decides whether MAG can produce a local submission-ready package and export verdict.

## Evidence To Review

- Quality verdict or review gate receipt.
- Final draft refs, package manifest refs, required sections, required attachments, budget/support material refs, and portal instructions.
- Provenance refs tying package artifacts back to accepted drafts, source evidence, and owner receipts.
- Manual portal boundary and human-supervised submission requirements.
- Exact refs and hashes for the same-generation `artifact-bundle.json`, `final-package.json`, `hosted-contract-bundle.json`, and `submission-ready-package.json` final bytes.

## AI/Owner-Backed Judgment Standard

- Submission-ready export requires an exact-byte `opl_stage_review_receipt` plus a MAG-owned package/export verdict or owner receipt.
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

- Terminal reviewer/re-reviewer closeout fields sufficient for the StageRunController to materialize an exact-hash-bound `opl_stage_review_receipt`; and
- A MAG-owned `submission_ready_export_verdict` or owner receipt that consumes that Review receipt and names the current package refs, manual portal boundary, `owner`, `export_verdict_ref`, `source_kind`, and `provenance_ref`; or
- A candidate package or no-output diagnostic with exact missing artifact, quality issue, provenance gap, or manual portal action.

## Final-Byte Review Boundary

- The producer materializes a candidate and cannot close terminal `submission_ready` by self-check or helper success.
- A fresh reviewer must inspect all four final package artifacts and bind the controller-owned Review receipt to their current hashes before MAG owner authority evaluates terminal local readiness.
- Repair inside this Stage is limited to package assembly, manifest, and provenance projection. Proposal content, source evidence, quality-closure, attachment ownership, or export-verdict defects route back to the earliest owning Stage.
- After any local repair, a fresh re-reviewer must inspect the complete rebuilt four-artifact generation; unchanged evidence cannot authorize changed bytes.
- Producer, repairer, and repair-required reviewer/re-reviewer output only `route_impact.stage_route_recommendation`; the terminal reviewer/re-reviewer alone outputs `route_impact.stage_route_decision`. The controller materializes only `opl_stage_review_receipt`; neither it nor the reviewer signs the MAG owner verdict.

## Quality-Debt And Human-Gate Shapes

- `quality_gate_unclosed`.
- `required_artifact_missing`.
- `export_provenance_missing`.
- `manual_portal_action_required`.
- `mechanical_export_ready_attempted`.

Missing artifacts, quality debt, or provenance gaps close submission-ready/export-ready claims but do not block stage transition. Manual portal action is an explicit human gate. Typed blockers are reserved for unavailable executors, wrong-target identity/currentness, authority/safety/permission/credential boundaries, irreversible actions, or explicit human decisions.

## Pass Condition

The exact current package generation has a fresh `opl_stage_review_receipt`, MAG owner authority has consumed that receipt and recorded the local export/readiness verdict, all provenance is traceable, and no external portal action is silently claimed complete.
