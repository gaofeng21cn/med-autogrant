# Call And Candidate Intake Policy

## Entry Conditions

- A user or caller has provided a grant request, candidate call, locked call, or project profile.
- Source refs can point to call guidance, applicant/team context, candidate project notes, and workspace state.
- OPL may schedule or host the attempt, but MAG is available as domain owner for intake truth and receipts.

## Stage Work

- Read funding-call source, eligibility, deadlines, format constraints, review criteria, and applicant/project context.
- Produce traceable intake refs and source gaps for later fundability review.
- Keep all grant truth in MAG/workspace-controlled refs; stage policy files only describe behavior.

## Exit Conditions

- `call_candidate_intake_ready` exists with source refs sufficient for fundability review; or
- A typed blocker records missing call identity, eligibility, source material, conflicting constraints, or forbidden write pressure; or
- A MAG owner receipt signs the accepted intake state.

## Handoff

- Handoff target: `fundability_strategy`.
- Handoff must include call lock state, source refs read, eligibility status, unresolved gaps, and fundability questions.
- No handoff may imply fundability-ready status.

## Independent Review And Gate Expectation

- Intake can be reviewed by checking whether another executor can reconstruct call requirements and gaps from refs alone.
- Required gates: `memory_and_receipts` and `authority_boundaries`.
- A missing source or eligibility uncertainty blocks the next stage until made explicit.

## OPL Role Boundary

- OPL role: descriptor, queue, wakeup, handoff, receipt, and projection consumer.
- OPL cannot write grant truth, choose a new locked call, or infer readiness from descriptor validation.
- Allowed action refs: `inspect_progress`, `inspect_cockpit`.

## Non-Pass Signals

- Intake refs cannot support a fundability reviewer without rereading private prose.
- The output changes the locked call or hides eligibility uncertainty.
