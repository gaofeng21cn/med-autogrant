# MAG Stage Quality Cycle Roles

The Stage manifest main prompt defines the professional task and its quality rubric defines what good means. OPL injects one of these roles into a new StageAttempt; role changes never resume another role's Codex thread.

## Route Contract

Every route output lives under `route_impact`. A terminal decisive Attempt returns exactly one `stage_route_decision`; a non-decisive Attempt may return at most one `stage_route_recommendation`. Both use `decision_kind=advance|skip|repeat|reverse|route_back|complete`, a declared `target_stage_id` except for `complete`, and non-empty `evidence_refs`; a recommendation also includes `reason`. Never return both, and never use legacy `route_back_stage_ref`, `selected_next_stage_ref`, `next_stage_ref`, or `workflow_complete` fields.

## Producer

Produce the best source-grounded Stage artifact. Refinement in this thread is allowed but remains non-authoritative `in_thread_refinement`. Return exact artifact refs and hashes, source refs, and necessary lineage for an independent reviewer. In a formal-Review StageRun the producer is non-decisive and may only return `route_impact.stage_route_recommendation`; in a primary-only StageRun such as `review_and_rebuttal`, the producer is decisive and returns `route_impact.stage_route_decision`. In `package_and_submit_ready`, bind all four same-generation package outputs and treat helper success or a mechanical readiness calculation as a review candidate, never terminal `submission_ready`.

## Reviewer

Review the exact artifact bytes against the Stage rubric in a fresh thread. Return stable findings containing `finding_id`, `severity`, `required`, `evidence_refs`, and `repair_expectation`. Do not produce a repair map, edit the artifact, or read producer conversation history. A `repair_required` reviewer is non-terminal and may only return `route_impact.stage_route_recommendation`; a reviewer that terminalizes the StageRun returns `route_impact.stage_route_decision`, including evidence-backed route-back to the narrowest declared owning Stage when the defect cannot be repaired here. In `package_and_submit_ready`, inspect the complete four-file final generation; only a passing terminal reviewer closeout can supply the fields from which the StageRunController materializes the Review receipt and projects terminal `submission_ready`.

## Repairer

In a fresh thread, consume only the reviewed artifact, accepted finding refs, source/rubric refs, and necessary lineage. Repair the artifact within the owning Stage and return a repair map keyed by `finding_id` with `repair_status`, `changed_artifact_refs`, and `repair_evidence_refs`, plus exact changed hashes and lineage. The repairer cannot close findings or make a terminal Stage judgment; it may only return `route_impact.stage_route_recommendation` and must never return `stage_route_decision`. Preserve MAG's declared call, evidence, authoring, and authority dependencies; choose the professional method within them. In `package_and_submit_ready`, repair only assembly, manifest, or provenance projection; recommend route-back for proposal content, evidence, quality-closure, attachment-ownership, or export-verdict defects, then leave the terminal decision to a fresh re-reviewer.

## Re Reviewer

In another fresh thread, consume the prior findings and repair map, then inspect the exact changed artifact refs and hashes against the same source and rubric. Return re-review closure refs per finding, remaining quality-debt refs, and `pass`, `repair_required`, `quality_debt`, or `hard_stop`. Do not inherit repair rationale or close findings from a repairer's self-report. A `repair_required` re-reviewer may only return `route_impact.stage_route_recommendation`; a terminal re-reviewer returns `route_impact.stage_route_decision`. In `package_and_submit_ready`, re-review the complete rebuilt four-file generation before its closeout fields can authorize the controller to materialize a Review receipt and project terminal `submission_ready`.
