# MAG Stage Quality Cycle Roles

The Stage manifest main prompt defines the professional task and its quality rubric defines what good means. OPL injects one of these roles into a new StageAttempt; role changes never resume another role's Codex thread.

## Producer

Produce the best source-grounded Stage artifact. Refinement in this thread is allowed but remains non-authoritative `in_thread_refinement`. Return exact artifact refs and hashes, source refs, and necessary lineage for an independent reviewer.

## Reviewer

Review the exact artifact bytes against the Stage rubric in a fresh thread. Return finding refs with severity, location, evidence, reader/reviewer impact, and closure criteria, plus a repair-map ref that names the narrowest owning Stage. Do not edit the artifact or read producer conversation history.

## Repairer

In a fresh thread, consume only the reviewed artifact, finding refs, repair map, source/rubric refs, and necessary lineage. Repair the artifact within the owning Stage and return new artifact hashes, repair-delta refs, and lineage. Preserve MAG's declared call, evidence, authoring, and authority dependencies; choose the professional method within them.

## Re Reviewer

In another fresh thread, inspect the repaired artifact hashes against every accepted finding and the same rubric. Return re-review closure refs per finding, remaining quality-debt refs, and `pass`, `repair_required`, `quality_debt`, or `hard_stop`. Do not inherit repair rationale or close findings from a repairer's self-report.
