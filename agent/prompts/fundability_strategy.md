# Fundability Strategy

Judge whether the locked call, applicant evidence, and candidate project can support a competitive and honest proposal strategy.

Use the intake evidence and call review criteria to reason across call fit, applicant credibility, novelty, preliminary support, feasibility, impact, reviewer risk, timeline, and required documents. These are interacting judgments, not a prescribed checklist order. Direction, scientific question, argument, and applicant fit may need to co-evolve before the strategy is stable. Distinguish a repairable weakness from a retarget, pause, evidence-collection, or stop recommendation.

A good result states the central grant opportunity, why this applicant can credibly pursue it, the strongest reviewer objections, the mitigation plan, and the evidence or decision still needed. Use `mag-strategy-intake-specialist` for specialist fundability judgment. Memory is advisory context only and must remain subordinate to the current call and source refs.

For this Stage, that MAG overlay may selectively invoke
`medical-research-lit`, `medical-evidence-integrity-reviewer`,
`medical-evidence-synthesis-and-claim-map`, and
`medical-reference-integrity-auditor` from the managed
`mag-medical-grant.v1` profile. Give them only the current grant artifact,
`source_pack_ref`, and epistemic scope. Their `candidate_refs`,
`owner_gate_handoff_ref`, and `route_back_candidate` are refs-only
professional candidates; only MAG may consume them into grant truth or issue
the fundability verdict. They cannot issue a quality, export, readiness,
receipt, or blocker decision.

OPL applies the role-specific quality cycle declared for this Stage. Polishing inside the current Codex thread is `in_thread_refinement` only; formal review, repair, and re-review use separate StageAttempts and fresh threads that receive only the exact artifact, source, rubric, and necessary lineage refs.

Return `fundability_strategy_gate_recorded` and a defensible `fundability_verdict_ref` when the strategy can proceed. Missing/conflicting evidence, eligibility, or call fit becomes quality debt and may route back to intake. Use a typed blocker only for unavailable executor, wrong-target identity/currentness, authority/safety, irreversible action, or explicit human decision. Schema, scorecard, queue, package, provider completion, or accepted memory cannot create readiness.

Handoff to `specific_aims_and_structure` with the call-fit rationale, central claim, reviewer risks, mitigation requirements, evidence needs, and explicit proceed/repair/retarget/stop state.
