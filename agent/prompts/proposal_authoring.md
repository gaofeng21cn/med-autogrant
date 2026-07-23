# Proposal Authoring

Create and revise a reviewable proposal body from the accepted aims, source evidence, applicant context, and funder-specific constraints.

Write against the real call and keep every material claim traceable to source or explicitly marked as uncertain. Make significance, innovation, approach, feasibility, risk and alternatives, expected impact, and applicant fit form one reviewer-facing argument. Use `mag-grant-workflow-specialist` for specialist drafting and source-faithful revision.

That MAG overlay reads this Stage's optional Skill selection and availability
policy from `contracts/scholar_skill_binding_contract.json`. Invoke only
available, compatible, material Skills with the current grant artifact ref,
`source_pack_ref`, and epistemic scope. Their outputs are refs-only
`candidate_refs`, `owner_gate_handoff_ref`, or `route_back_candidate`; MAG
must consume, reject, or route them back before changing proposal truth.
Missing or incompatible Provider state records only a diagnostic or advisory
quality hint and cannot block install, Stage launch, Stage route, operational
readiness, authoring, quality work, or create a typed blocker.

The current outline is a strong default, not an AI-imposed permanent freeze. Preserve a human-approved outline. Otherwise, when drafting exposes a genuine structural problem, revise the outline or return the smallest upstream route-back instead of forcing prose into a defective plan. Choose section order from the call and argument; there is no global significance-first writing rule.

A good result is concrete, evidence-linked, internally coherent, formatted for the call, and candid about unresolved gaps. Keep grant bodies in the workspace/artifact root and body-free refs in OPL surfaces.

OPL applies the role-specific quality cycle declared for this Stage. Polishing inside the current Codex thread is `in_thread_refinement` only; formal review, repair, and re-review use separate StageAttempts and fresh threads that receive only the exact artifact, source, rubric, and necessary lineage refs.

Return `proposal_draft_reviewable` with draft, section, claim/source, evidence-gap, and critique-target refs. Missing core source or format feasibility becomes quality debt or a no-output diagnostic and may route back. Use a typed blocker only for authority/safety, forbidden fabrication, unavailable executor, wrong-target identity/currentness, irreversible action, or explicit human decision. Do not infer quality from section counts, schema completion, or polished prose.

Handoff the actual draft to `review_and_rebuttal` for independent review.
