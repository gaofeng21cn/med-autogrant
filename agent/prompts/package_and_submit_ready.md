# Package And Submit Ready

Apply MAG package authority and export gates to the reviewed local proposal package, without confusing local readiness with portal submission.

Consume the reviewed draft, independent quality verdict, closure evidence, call requirements, attachments, format checks, package identity, and current artifact refs. The producer must bind exact refs and hashes for all four outputs in one generation: `artifact-bundle.json`, `final-package.json`, `hosted-contract-bundle.json`, and `submission-ready-package.json`. Freeze only the exact package bytes covered by authority and fresh proof. Rebuild after any mutation, then review the new bytes; old evidence cannot authorize a changed package.

A good result is a traceable local package whose scientific body, required components, formatting, identity, and export evidence agree. Use the package/export quality gates and keep artifact bodies in the workspace or delivery root.

The fresh reviewer must inspect those four final byte streams as one package generation. A repairer may change only package assembly, manifest, or provenance projection within this Stage. Any defect in proposal content, quality closure, source evidence, attachments owned upstream, or an existing export verdict must route back to the earliest owning Stage instead of being rewritten here.

The producer output is a review candidate even when its mechanical package calculation passes and may only return `route_impact.stage_route_recommendation`. A `repair_required` reviewer is also non-terminal. Only a terminal reviewer or re-reviewer returns `route_impact.stage_route_decision`; its evidence-backed closeout fields allow the StageRunController to materialize `submission_ready_package_receipt_recorded` and project terminal `submission_ready`. No Attempt directly materializes the authoritative receipt. Always materialize a candidate package or no-output diagnostic; corrupt or absent artifacts become quality debt and block quality-ready, export-ready, and submission-ready claims. Use a typed blocker only for unavailable executor, wrong-target identity/currentness, authority/safety/credential, irreversible-action, or explicit human-decision boundaries.

Human portal entry and final submission remain outside autonomous MAG authority and require explicit human authorization. Provider completion, schema validation, package existence, or OPL state cannot cross that gate.
