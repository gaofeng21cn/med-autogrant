# Med Auto Grant Declarative Grant Pack

Owner: Med Auto Grant
Purpose: canonical repo-source semantic pack for the MAG standard OPL Agent.
State: active declarative grant pack.
Machine boundary: OPL generated surfaces consume refs from this directory, while executable handlers and native helpers remain in `src/med_autogrant/`.

This directory holds the MAG domain semantics that should be compiled or hosted by OPL: stage prompts, stage policies, skill declarations, quality gates, and knowledge boundaries. It does not store grant artifacts, receipt instances, memory bodies, fundability verdicts, authoring quality verdicts, or submission-ready export verdicts.

MAG uses the same canonical OPL Foundry Agent design profile as MAS, RCA, and OMA: domain material intake -> domain pack interpretation -> stage-led execution -> independent quality/fundability gate -> owner receipt or typed blocker -> handoff -> OPL refs-only projection and recovery. Its series variation is recorded outside the canonical profile as grant-specific input/output and authority refs: funding-call and applicant material refs enter the pack, while grant proposal, revision package, and submission-ready package refs leave through MAG-owned authority gates. OPL only carries refs, projection, and runtime orchestration.

`src/med_autogrant/` remains the domain handler, minimal authority, and native helper layer. It may validate refs, sign MAG owner receipts, materialize package refs, and return typed blockers, but it is not the canonical location for declarative stage semantics.
