# Med Auto Grant Principles

Owner: `med-autogrant`
Purpose: grant-domain specialization of the OPL standard-agent AI-first principle pack.
State: `active_domain_specialization`
Machine boundary: this is a human-readable domain specialization. Machine-readable adoption is in `contracts/standard-agent-principles-adoption.json`; runtime and package truth remain in MAG contracts, source, receipts, and verification outputs.

MAG adopts the OPL principles as a grant authoring agent, not as a new workflow engine:

- Intake is the `call_and_candidate_intake` stage and its prompt, not a standalone Skill. The stage decides what the current owner needs to answer next and returns a grant ref, route-back, owner receipt, human gate, or MAG typed blocker.
- Fundability, proposal quality, export readiness, package authority, grant strategy memory accept/reject, and owner receipt signing stay MAG-owned. OPL may project refs and run stage infrastructure, but cannot issue grant-ready, fundability-ready, quality-ready, export-ready, submission-ready, or production-ready claims.
- `agent/stages/`, `agent/prompts/`, `agent/skills/`, `agent/quality_gates/`, `agent/knowledge/`, and `agent/tools/domain_affordances.md` remain the declarative grant pack. `src/med_autogrant/` remains the minimal authority and native helper layer.
- Scorecards, schema completeness, generated surfaces, read models, provider completion, and conformance results are evidence or blocker localization only. Independent grant review, MAG owner receipt, typed blocker, route-back, or human gate closes the domain judgment.
- Legacy product-entry, sidecar, local journal, attempt ledger, workspace/source intake, and package helpers are migration inputs only unless a current MAG authority surface says otherwise.

This specialization keeps the grant loop AI-first while preserving the authority line: OPL hosts and projects the stage shell; MAG owns the grant decision.
