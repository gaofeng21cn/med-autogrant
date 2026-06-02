# Med Auto Grant Runtime Boundary

Owner: `Med Auto Grant`
Purpose: `runtime_descriptor_boundary`
State: `descriptor_index_surface`
Machine boundary: This human-readable index is not a runtime artifact root, sidecar, scheduler, lifecycle engine, attempt ledger, or OPL runtime implementation. Runtime truth remains in contracts, source, runtime evidence, owner receipts, `$CODEX_HOME/projects/med-autogrant/runtime-state/`, and workspace artifact roots.

This directory keeps the runtime-facing skeleton root explicit for MAG authority references and repo-source layout. MAG exposes grant-domain handler targets, refs-only projections, owner receipt refs, typed blockers, and authority refs for OPL/Temporal to consume; it does not own the generic runtime, queue, scheduler, sidecar, lifecycle engine, App/workbench shell, or attempt ledger.

Real grant artifacts, memory bodies, accepted/rejected receipt instances, runtime state, and submission-ready packages remain outside repo-tracked source.
