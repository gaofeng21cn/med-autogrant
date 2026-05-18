# Med Auto Grant Declarative Grant Pack

Owner: Med Auto Grant
Purpose: canonical repo-source semantic pack for the MAG standard OPL Agent.
State: active declarative grant pack.
Machine boundary: OPL generated surfaces consume refs from this directory, while executable handlers and native helpers remain in `src/med_autogrant/`.

This directory holds the MAG domain semantics that should be compiled or hosted by OPL: stage prompts, stage policies, skill declarations, quality gates, and knowledge boundaries. It does not store grant artifacts, receipt instances, memory bodies, fundability verdicts, authoring quality verdicts, or submission-ready export verdicts.

`src/med_autogrant/` remains the domain handler, minimal authority, and native helper layer. It may validate refs, sign MAG owner receipts, materialize package refs, and return typed blockers, but it is not the canonical location for declarative stage semantics.
