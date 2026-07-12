# Call And Candidate Intake

Establish the exact funding task and a source-grounded applicant/candidate picture that later grant judgments can trust.

Read the call, portal instructions, eligibility and deadline constraints, applicant/team evidence, preliminary work, and candidate project material. Lock a user-selected call; do not silently retarget it. Separate confirmed facts from interpretation and identify the missing evidence that could change eligibility, fit, or feasibility.

A good result gives later stages traceable refs for the call identity, review criteria, required sections and attachments, eligibility, budget/personnel limits, applicant strengths, source gaps, and the questions that fundability review must resolve. Use `mag-strategy-intake-specialist` when the intake requires specialist judgment.

Return `call_candidate_intake_ready` with body-free handoff refs when the evidence is usable. Return a typed blocker only when call identity, eligibility, required source material, authority, or currentness prevents a legal handoff; otherwise preserve uncertainty as an evidence gap. Do not issue fundability, quality, package, or submission verdicts here, and keep grant bodies and receipt instances outside repo source and OPL runtime state.

Handoff to `fundability_strategy` with sources read, unresolved gaps, call-lock status, and the next professional questions.
