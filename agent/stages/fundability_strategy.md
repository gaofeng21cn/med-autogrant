# Fundability Strategy Policy

## Entry Conditions

- Intake handoff exists with locked call, applicant context, candidate project direction, and source gaps.
- Call fit and eligibility are not fatally unknown, or the stage is explicitly asked to decide that blocker.
- Required source refs are available through MAG/workspace refs, not OPL runtime truth.

## Stage Work

- Judge fundability using AI-first grant-review reasoning across fit, applicant evidence, novelty, feasibility, impact, reviewer risk, and timeline.
- Decide proceed, repair, retarget, or block with specific evidence.
- Use memory refs only as body-free evidence; accept/reject strategy memory remains MAG authority.

## Exit Conditions

- `fundability_strategy_gate_recorded` exists with an AI-backed fundability verdict ref; or
- A typed blocker records insufficient evidence, rejected call fit, fatal reviewer risk, memory conflict, or mechanical-ready attempt; or
- A MAG owner receipt signs a proceed/repair/stop state.

## Handoff

- Handoff target: `specific_aims_and_structure`.
- Handoff must include verdict ref, call-fit rationale, top reviewer risks, mitigation requirements, accepted strategy, and memory refs used/rejected.
- Proceed handoff must be strong enough for independent critique.

## Independent Review And Gate Expectation

- Independent review should ask whether a skeptical panel reviewer would accept the strategy as competitive.
- Required gate: `fundability`.
- Numeric scorecards, provider completion, schema state, package presence, or queue state are never sufficient.

## OPL Role Boundary

- OPL role: descriptor and receipt consumer.
- OPL can carry refs and attempts, but cannot override MAG fundability judgment.
- Allowed action refs: `open_grant_user_loop`, `inspect_progress`.

## Non-Pass Signals

- The verdict sounds positive but lacks reviewer-risk reasoning.
- The output proceeds by optimism while evidence collection or retargeting is required.
