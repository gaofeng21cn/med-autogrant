# Memory And Receipt Gate

## Gate Purpose

This gate ensures grant strategy memory and owner receipts remain MAG-owned, body-safe, and useful for stage handoff.

## Memory Rules

- Strategy memory accept/reject is an AI-first MAG decision over relevance, recency, call fit, applicant context, and reviewer risk.
- OPL memory transport may carry body-free refs, locator results, and writeback proposals.
- OPL cannot store memory bodies, accept/reject memory, or turn memory transport into grant truth.

## Receipt Rules

- Owner receipts can sign domain actions, blockers, no-regression results, memory decisions, lifecycle refs, package refs, safe action refs, and handoff state.
- Receipts are refs and runtime evidence, not grant artifacts or memory bodies.
- Receipts cannot create fundability, quality, or export readiness from runtime state.

## Required Checks

- Any memory used by a stage is cited by body-free ref and classified as accepted, rejected, stale, conflicting, or pending.
- Any stage handoff or authority action has a receipt ref or typed blocker.
- Receipt refs include owner, action/blocker kind, source refs, provenance, and next-stage effect.

## Blocker Shapes

- `memory_body_exposed`: output leaks body-bearing memory into repo source or OPL surface.
- `memory_accept_reject_missing`: memory is used without MAG accept/reject state.
- `receipt_ref_missing`: handoff or authority action lacks owner receipt or typed blocker.
- `receipt_claims_ready_mechanically`: receipt tries to declare verdict from runtime state.

## Pass Condition

Memory and receipts remain refs-first, MAG-owned, and limited to evidence/provenance rather than becoming hidden grant truth or mechanical readiness.

## Reviewer Checklist

- Can the next executor see which memory refs were accepted, rejected, stale, conflicting, or pending?
- Does every handoff-critical decision have a receipt ref or typed blocker?
- Are receipt claims limited to authority acceptance rather than hidden readiness verdicts?
