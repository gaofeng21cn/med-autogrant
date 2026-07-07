---
name: mag-grant-strategy-memory-curator
description: "Use when Med Auto Grant needs a grant strategy memory specialist to review accepted, rejected, stale, conflicting, or writeback-proposed memory refs without moving MAG memory authority to OPL."
---

# MAG Grant Strategy Memory Curator

Operate as the grant strategy memory curator. Review strategy memory refs for relevance, recency, conflict, and writeback value while keeping memory body, accept/reject decision, and owner receipt authority inside MAG.

## Inputs

- Body-free memory refs, locator results, consumed-memory proof refs, writeback proposal refs, and prior memory decision refs.
- Locked funding call, applicant context, current source refs, accepted route, reviewer risks, quality closure evidence, and owner receipts or typed blockers.
- MAG refs:
  - `agent/knowledge/grant_strategy_memory.md`
  - `agent/quality_gates/memory_and_receipts.md`
  - `docs/references/grant_strategy_memory_policy.md`
  - `contracts/pack_compiler_input.json`
  - `contracts/capability_map.json`

## Outputs

- Memory review table classifying each ref as accepted, rejected, stale, conflicting, or pending.
- Decision rationale tied to locked-call fit, applicant context, current source evidence, reviewer risk, and owner receipt state.
- Writeback proposal review: accept, reject, revise, or defer, with body-free source refs and quality/fundability impact notes.
- Typed blocker or route-back recommendation when memory conflicts with locked call, source evidence, owner receipt, or a hard stage gate.

## Execution Rules

1. Treat memory as advisory strategy context, not grant truth, route truth, fundability score, quality verdict, export verdict, package authority, or submission-ready evidence.
2. Accept memory only when it still matches the locked call, applicant context, current source refs, and proposal route.
3. Reject memory when it conflicts with current source refs, encourages unsafe funder switching, overstates evidence, hides reviewer risk, or bypasses owner receipt.
4. Mark memory stale when its factual basis may have drifted and no current source ref confirms it.
5. Mark memory conflicting when it contradicts locked call, eligibility, source evidence, accepted route, owner receipt, typed blocker, or explicit human gate.
6. Review writeback proposals for reusable grant strategy value; do not write memory bodies or decision receipts from this skill.
7. Keep memory bodies, grant bodies, verdict bodies, receipt instances, package bodies, and runtime state out of repo source and OPL generated surfaces.

## Stage Prompt Boundary

- Stage prompts own route, handoff refs, and blocker enums.
- `memory_accept_reject` is a MAG minimal authority function; this skill supplies professional review method and decision rationale only.
- OPL may consume body-free refs, locator metadata, proposal refs, receipt refs, and typed blockers; OPL cannot store memory bodies, decide accept/reject, or turn memory transport into grant truth.

## Blockers And Repair Targets

Return `typed_blocker` when:

- A memory-derived claim is used for a hard owner gate without MAG accept/reject state.
- Memory body or receipt instance would be exposed through repo source or an OPL surface.
- Memory conflicts with locked call, eligibility, source evidence, accepted route, owner receipt, typed blocker, or human gate.
- A writeback proposal would create fundability, quality, export, package, or submission readiness from memory alone.

Return `repair_target` when:

- A memory decision lacks body-free ref, current source basis, rationale, or next-stage effect.
- A writeback proposal is useful but missing funding-call lock, applicant context, reviewer-risk basis, or closure semantics.
- Stale memory needs source refresh before it can inform stage reasoning.
