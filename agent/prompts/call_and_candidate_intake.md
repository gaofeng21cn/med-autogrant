# Call And Candidate Intake

Establish the exact funding task and a source-grounded applicant/candidate picture that later grant judgments can trust.

Read the call, portal instructions, eligibility and deadline constraints, applicant/team evidence, preliminary work, and candidate project material. Lock a user-selected call; do not silently retarget it. Separate confirmed facts from interpretation and identify the missing evidence that could change eligibility, fit, or feasibility.

A good result gives later stages traceable refs for the call identity, review criteria, required sections and attachments, eligibility, budget/personnel limits, applicant strengths, source gaps, and the questions that fundability review must resolve. Use `mag-strategy-intake-specialist` when the intake requires specialist judgment.

For this Stage, the MAG overlay reads its optional Skill selection and
availability policy from `contracts/scholar_skill_binding_contract.json`.
Invoke only available, compatible, material Skills with the current grant
artifact ref, `source_pack_ref`, and epistemic scope. Their outputs are
refs-only `candidate_refs`, `owner_gate_handoff_ref`, or
`route_back_candidate`; MAG must consume, reject, or route them back. Missing
or incompatible Provider state records only a diagnostic or advisory quality
hint and cannot block install, Stage launch, Stage route, operational
readiness, grant work, or create a typed blocker.

OPL applies the role-specific quality cycle declared for this Stage. Polishing inside the current Codex thread is `in_thread_refinement` only; formal review, repair, and re-review use separate StageAttempts and fresh threads that receive only the exact artifact, source, rubric, and necessary lineage refs.

Return `call_candidate_intake_ready` with body-free handoff refs when the evidence is usable. Missing call identity, eligibility, or required source material becomes an evidence-gap diagnostic and does not block the next stage. Return a typed blocker only for wrong-target identity/currentness, unavailable executor, authority/safety, irreversible action, or explicit human decision. Do not issue fundability, quality, package, or submission verdicts here, and keep grant bodies and receipt instances outside repo source and OPL runtime state.

Handoff to `fundability_strategy` with sources read, unresolved gaps, call-lock status, and the next professional questions.
