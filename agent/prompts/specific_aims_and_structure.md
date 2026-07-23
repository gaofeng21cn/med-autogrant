# Specific Aims And Structure

Turn the accepted fundability basis into a coherent scientific question, aims frame, argument structure, and funder-compliant proposal plan.

Use the call rules, applicant evidence, preliminary data, method constraints, resources, and reviewer risks. Direction, question, argument, and applicant fit are professional dependencies that should converge together; the route does not require a fixed reasoning order or a fixed number of alternatives. Make each aim assessable through its premise, approach, success criteria, risks or alternatives, and evidence needs.

A good result makes the central problem, hypothesis or objective, innovation, expected outcome, applicant advantage, and reviewer-facing logic mutually consistent. Map the resulting structure to the funder's actual sections and identify claims that require evidence or must remain tentative. An outline is a strong default before long-form drafting, but only an explicitly approved outline is frozen; drafting may expose a legitimate route-back.

Use `mag-strategy-intake-specialist` as the MAG overlay. It may selectively
invoke `medical-research-lit`, `medical-statistical-review`,
`medical-methodology-planner`, `medical-evidence-integrity-reviewer`, and
`medical-evidence-synthesis-and-claim-map` from the managed
`mag-medical-grant.v1` profile. Give them only the current grant artifact,
`source_pack_ref`, and epistemic scope. Their `candidate_refs`,
`owner_gate_handoff_ref`, and `route_back_candidate` are refs-only
professional candidates; MAG must consume, reject, or route them back before
accepting aims or changing grant truth. They cannot issue a fundability,
quality, export, readiness, receipt, or blocker decision.

OPL applies the role-specific quality cycle declared for this Stage. Polishing inside the current Codex thread is `in_thread_refinement` only; formal review, repair, and re-review use separate StageAttempts and fresh threads that receive only the exact artifact, source, rubric, and necessary lineage refs.

Return `specific_aims_structure_accepted` with aims, argument, section-map, claim/evidence, and reviewer-risk refs. Missing call fit, evidence, or required format becomes quality debt and a route-back recommendation. Use a typed blocker only for unavailable executor, wrong-target identity/currentness, authority/safety, irreversible action, or explicit human decision. MAG owns aims acceptance; OPL only carries refs and attempts.

Handoff to `proposal_authoring` with the converged design and any unresolved evidence or upstream decision.
