# Proposal Authoring

Create and revise a reviewable proposal body from the accepted aims, source evidence, applicant context, and funder-specific constraints.

Write against the real call and keep every material claim traceable to source or explicitly marked as uncertain. Make significance, innovation, approach, feasibility, risk and alternatives, expected impact, and applicant fit form one reviewer-facing argument. Use `mag-grant-workflow-specialist` for specialist drafting and source-faithful revision.

That MAG overlay may selectively invoke `medical-research-lit`,
`medical-statistical-review`, `medical-methodology-planner`,
`medical-evidence-integrity-reviewer`,
`medical-evidence-synthesis-and-claim-map`, and
`medical-reference-integrity-auditor` from the managed
`mag-medical-grant.v1` profile. Give them only the current grant artifact,
`source_pack_ref`, and epistemic scope. Their `candidate_refs`,
`owner_gate_handoff_ref`, and `route_back_candidate` are refs-only
professional candidates; MAG must consume, reject, or route them back before
changing proposal truth. They cannot issue a fundability, quality, export,
readiness, receipt, or blocker decision.

The current outline is a strong default, not an AI-imposed permanent freeze. Preserve a human-approved outline. Otherwise, when drafting exposes a genuine structural problem, revise the outline or return the smallest upstream route-back instead of forcing prose into a defective plan. Choose section order from the call and argument; there is no global significance-first writing rule.

A good result is concrete, evidence-linked, internally coherent, formatted for the call, and candid about unresolved gaps. Keep grant bodies in the workspace/artifact root and body-free refs in OPL surfaces.

OPL applies the role-specific quality cycle declared for this Stage. Polishing inside the current Codex thread is `in_thread_refinement` only; formal review, repair, and re-review use separate StageAttempts and fresh threads that receive only the exact artifact, source, rubric, and necessary lineage refs.

Return `proposal_draft_reviewable` with draft, section, claim/source, evidence-gap, and critique-target refs. Missing core source or format feasibility becomes quality debt or a no-output diagnostic and may route back. Use a typed blocker only for authority/safety, forbidden fabrication, unavailable executor, wrong-target identity/currentness, irreversible action, or explicit human decision. Do not infer quality from section counts, schema completion, or polished prose.

Handoff the actual draft to `review_and_rebuttal` for independent review.
