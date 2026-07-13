# Memory And Receipt Gate

## Gate Purpose

This gate ensures grant strategy memory and owner receipts remain MAG-owned, body-safe, and useful for stage handoff.

## Memory Rules

- Strategy memory accept/reject is an AI-first MAG decision over relevance, recency, call fit, applicant context, and reviewer risk.
- OPL memory transport may carry body-free refs, locator results, and writeback proposals.
- OPL cannot store memory bodies, accept/reject memory, or turn memory transport into grant truth.
- Strategy memory is advisory-by-default and claim-gated-only: it may inform Codex reasoning, reviewer-risk attention, and route-back suggestions, but it cannot authorize fundability, quality, export, package, submission, owner receipt, or typed blocker claims.
- Missing or stale memory should normally produce advisory notes, route-back suggestions, or reviewer attention. It fails closed only when a memory-derived claim is being used for a hard owner gate or when memory conflicts with locked source/call/owner evidence.

## Receipt Rules

- Owner receipts can sign domain actions, blockers, no-regression results, memory decisions, lifecycle refs, package refs, safe action refs, and handoff state.
- Receipts are refs and runtime evidence, not grant artifacts or memory bodies.
- Receipts cannot create fundability, quality, or export readiness from runtime state.

## Required Checks

- Any memory used by a stage is cited by body-free ref and classified as accepted, rejected, stale, conflicting, or pending.
- Any authority action has its required receipt ref or a real hard-boundary typed blocker. An ordinary stage handoff missing a receipt records quality debt and continues with the available artifact or a no-output diagnostic.
- Receipt refs include owner, action/blocker kind, source refs, provenance, and next-stage effect.

## Blocker Shapes

- `memory_body_exposed`: output leaks body-bearing memory into repo source or OPL surface.
- `memory_accept_reject_missing`: memory is used without MAG accept/reject state.
- `memory_authority_overclaim`: memory refs are used as a fundability scorer, route controller, export/submission gate, or package readiness authority.
- `receipt_ref_missing`: handoff lacks an expected receipt and must close stronger claims; an authority action without its mandatory receipt remains unauthorized.
- `receipt_claims_ready_mechanically`: receipt tries to declare verdict from runtime state.

## Pass Condition

Memory and receipts remain refs-first, MAG-owned, and limited to evidence/provenance rather than becoming hidden grant truth or mechanical readiness.

## Reviewer Checklist

- Can the next executor see which memory refs were accepted, rejected, stale, conflicting, or pending?
- Does every handoff-critical decision have a receipt ref, quality-debt diagnostic, route-back, human gate, or true hard-boundary typed blocker?
- Are receipt claims limited to authority acceptance rather than hidden readiness verdicts?
