# Proposal Authoring Policy

## Entry Conditions

- Accepted aims/structure handoff exists with section map and claim/evidence ledger.
- Funding-call format constraints and source material refs are available.
- MAG authority boundary is active for artifact refs and package mutation.

## Stage Work

- Draft proposal sections against the accepted aims, source evidence, and funder review criteria.
- Preserve claim/source traceability and mark unsupported claims.
- Keep grant body artifacts in workspace/artifact roots; `agent/` and OPL surfaces carry refs only.

## Exit Conditions

- `proposal_draft_reviewable` exists with draft refs and critique targets; or
- A quality-debt diagnostic records missing accepted structure, required source, format conflict, or unsupported claim pressure; a typed blocker is reserved for artifact authority or another real hard boundary; or
- A MAG owner receipt signs draft/ref acceptance.

## Handoff

- Handoff target: `review_and_rebuttal`.
- Handoff must include draft refs, section completion state, claim/source gaps, known weak arguments, and format constraints.
- Handoff must invite independent critique rather than declaring quality-ready.

## Independent Review And Gate Expectation

- Independent review should be able to attack the draft using the provided refs and source ledger.
- Required gates: `quality` and `authority_boundaries`.
- Section count, draft existence, or scorecard progress cannot authorize quality readiness.

## OPL Role Boundary

- OPL role: attempt lifecycle, handoff, and projection support.
- Generated surfaces may invoke MAG handlers but cannot store canonical grant body content or mutate package artifacts without MAG receipt.
- Allowed action refs: `open_grant_user_loop`, `build_direct_entry`.

## Non-Pass Signals

- The draft uses polished generic prose where source-specific evidence is missing.
- The handoff asks review to infer claim support without a claim/source ledger.
