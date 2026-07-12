# Fundability Strategy

Judge whether the locked call, applicant evidence, and candidate project can support a competitive and honest proposal strategy.

Use the intake evidence and call review criteria to reason across call fit, applicant credibility, novelty, preliminary support, feasibility, impact, reviewer risk, timeline, and required documents. These are interacting judgments, not a prescribed checklist order. Direction, scientific question, argument, and applicant fit may need to co-evolve before the strategy is stable. Distinguish a repairable weakness from a retarget, pause, evidence-collection, or stop recommendation.

A good result states the central grant opportunity, why this applicant can credibly pursue it, the strongest reviewer objections, the mitigation plan, and the evidence or decision still needed. Use `mag-strategy-intake-specialist` for specialist fundability judgment. Memory is advisory context only and must remain subordinate to the current call and source refs.

Return `fundability_strategy_gate_recorded` and a defensible `fundability_verdict_ref` when the strategy can proceed. Use route-back for ordinary repair. Use a typed blocker only when missing or conflicting evidence, authority, eligibility, or call fit leaves no legal repair route. Schema, scorecard, queue, package, provider completion, or accepted memory cannot create readiness.

Handoff to `specific_aims_and_structure` with the call-fit rationale, central claim, reviewer risks, mitigation requirements, evidence needs, and explicit proceed/repair/retarget/stop state.
