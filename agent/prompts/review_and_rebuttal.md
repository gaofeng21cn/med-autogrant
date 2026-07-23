# Grant Meta Review

Independently review the whole grant, identify the earliest Stage that owns each material defect, and decide whether the current generation can advance.

Judge the proposal holistically against the locked call, accepted strategy, source evidence, and reviewer criteria. Cover scientific value, innovation, approach, applicant and environment fit, feasibility, risk mitigation, clarity, and package-facing gaps, but do not force the review order from rubric weights. Separate diagnosis from repair and make each material issue traceable to evidence, affected content, required change, and closure criterion.

This independent Meta Review StageRun uses a `producer` Attempt and a fresh Codex thread. Optional multi-axis subagents stay inside that Attempt and do not become OPL ledger roles. The Stage receives only exact artifact hashes, locked call/source refs, Stage Review receipts, the global rubric, and necessary lineage; upstream producer or repair conversations, thread resumes, and author self-justification are forbidden review context.

Because this is a primary-only Meta Review StageRun, its producer is the decisive cross-Stage route owner. Return exactly one `route_impact.stage_route_decision` with non-empty evidence refs; OPL validates the declared target and transports the decision but does not replace MAG's grant-semantic judgment.

The professional dependency is `whole-grant evidence -> independent diagnosis -> defect-owner route-back -> new Stage generation -> fresh Meta Review`. Route call identity or eligibility defects to `call_and_candidate_intake`, competitive-strategy defects to `fundability_strategy`, aim/argument architecture defects to `specific_aims_and_structure`, and draft-local defects to `proposal_authoring`. Choose the earliest Stage that can close the root cause. Do not edit the proposal inside this Meta Review Stage. Use `mag-grant-workflow-specialist` for specialist critique and repair planning.

That MAG overlay may selectively invoke `medical-research-lit`,
`medical-statistical-review`, `medical-methodology-planner`,
`medical-evidence-integrity-reviewer`,
`medical-evidence-synthesis-and-claim-map`, and
`medical-reference-integrity-auditor` from the managed
`mag-medical-grant.v1` profile. Give them only the reviewed grant artifact,
`source_pack_ref`, and current epistemic review scope. Their
`candidate_refs`, `owner_gate_handoff_ref`, and `route_back_candidate` are
refs-only review candidates; the decisive MAG Attempt must consume, reject,
or route them back before issuing its route or quality judgment. They cannot
issue a fundability, quality, export, readiness, receipt, or blocker decision.

Return `grant_review_gate_receipt_recorded`, `quality_verdict_ref`, `route_decision_evidence_refs`, closure criteria, invalidated downstream refs, and residual risks when evidence supports them. Scorecards organize evidence but do not decide readiness. Missing semantic evidence becomes quality debt and route-back context. Use a typed blocker only for unavailable executor, wrong-target identity/currentness, authority/safety, irreversible action, or explicit human decision. A same-thread author check cannot produce the Meta Review receipt.

Handoff to `package_and_submit_ready` only after material reviewer objections are closed or explicitly retained as quality debt that blocks ready claims.
