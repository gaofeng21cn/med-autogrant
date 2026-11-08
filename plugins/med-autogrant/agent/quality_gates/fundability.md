# Fundability Gate

## Gate Purpose

This gate decides whether the locked grant task is competitively fundable enough to proceed into aims and authoring.

## Evidence To Review

- Funding-call fit, eligibility, mechanism scope, review criteria, deadline, budget, and required materials.
- Applicant/team credibility, preliminary evidence, resources, collaborators, feasibility, and institutional support.
- Scientific novelty, impact, patient/cohort/data access, methods maturity, and funder-specific relevance.
- Reviewer risks, mitigation plan, and any prior strategy memory refs.

## AI-First Judgment Standard

- Fundability requires an AI-authored grant-review artifact, fundability stage artifact, or MAG owner receipt.
- The judgment must explain proceed/repair/retarget/stop and name the top reviewer risks.
- Weak but repairable proposals may pass only with explicit mitigation requirements and handoff conditions.

## Forbidden Decision Sources

- Schema completeness.
- OPL provider completion.
- Generic lifecycle completion.
- Package file presence.
- Numeric scorecard values alone.
- Controller route state.
- Runtime queue state.

## Required Output

- `fundability_verdict_ref` with owner, source refs, evidence summary, risk ranking, and proceed/repair/stop state; or
- A quality-debt or no-output diagnostic with exact missing evidence, rejected fit, or route-back recommendation; or
- MAG owner receipt ref accepting the state.

## Quality-Debt Shapes

- `fundability_evidence_insufficient`.
- `call_fit_rejected`.
- `fatal_review_risk`.
- `strategy_memory_conflict`.
- `mechanical_ready_attempted`.

Typed blockers are reserved for unavailable executors, wrong-target identity/currentness, authority/safety/permission/credential boundaries, irreversible actions, or explicit human decisions. A rejected or weak call fit is a domain result and route-back input, not a stage-transition blocker.

## Pass Condition

The output would survive a skeptical grant reviewer asking: why this applicant, why this call, why now, why fundable, and what risk remains.
