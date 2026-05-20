# Authority Boundaries

## Gate Purpose

This gate keeps MAG domain authority separate from OPL provider/runtime authority during every Codex stage attempt.

## MAG-Owned Authority

- Grant truth, funding-call interpretation, applicant/task lock, aims route, and proposal body truth.
- Fundability, authoring quality, export/package verdicts, and reviewer-style closure.
- Grant strategy memory body, accept/reject decision, and writeback receipt.
- Package authority, owner receipts, transition oracle semantics, typed blockers, safe action refs, and grant-native helpers.

## OPL-Owned Authority

- Generated surfaces, provider runtime, queue, attempt ledger, generic transition runner, workspace/source shell, memory locator transport, artifact/package lifecycle shell, operator projection, observability, and App/workbench shell.
- OPL may carry refs, host attempts, project status, and return receipts or blockers.
- OPL cannot write MAG grant truth, memory bodies, artifact bodies, or ready verdicts.

## Allowed Programmatic Role

- Validate refs, materialize refs, sign receipts, return typed blockers, run deterministic grant helpers, and expose action metadata.
- Programmatic code may organize evidence and guard output boundaries.
- Programmatic code may not compute fundability-ready, quality-ready, or export-ready states without AI/owner-backed stage evidence.

## Required Checks

- Each stage output names its MAG owner, source refs, and next-stage handoff state.
- Any readiness claim traces to AI-first stage artifact, owner receipt, or typed blocker resolution.
- Body-bearing grant artifacts and memory bodies stay out of repo source and OPL generated surfaces.
- Forbidden writes to OPL runtime state or generic lifecycle surfaces are blocked.

## Blocker Shapes

- `authority_owner_mismatch`: output assigns MAG truth or verdict to OPL/provider/runtime.
- `forbidden_truth_write`: output writes grant truth, memory body, artifact body, or verdict body to disallowed surfaces.
- `mechanical_ready_verdict`: output derives readiness from schema, queue, lifecycle, package existence, or score alone.
- `missing_owner_receipt`: package mutation, memory accept/reject, or authority action lacks MAG receipt.

## Pass Condition

The stage can pass only when the output is refs-first, MAG-owned where judgment is required, and explicit about blockers instead of implying readiness from runtime progress.
