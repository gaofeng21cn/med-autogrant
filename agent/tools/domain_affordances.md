# MAG Domain Tool Affordances

Owner: `med-autogrant`
Purpose: `domain_tool_affordance_catalog`
State: `advisory_current_contract`
Machine boundary: This file declares available domain tool affordances for MAG stage attempts. It is not a workflow script, executor sequence, quality verdict, export verdict, owner receipt, or grant truth source.

## Boundary

MAG stage attempts may use tools to read grant calls, applicant context, repo contracts, package workspaces, and refs-only evidence. Tool use stays inside the permission, credential, write-scope, side-effect, and forbidden-authority boundaries declared by `contracts/pack_compiler_input.json`, `contracts/stage_control_plane.json`, and `contracts/cognitive_kernel_adoption.json`.

## Affordances

- `grant_source_and_applicant_context_reading`: Read call guidance, applicant materials, eligibility constraints, and source refs needed for grounded grant work.
- `grant_authoring_and_revision_workspace_operation`: Draft and revise grant artifacts only inside owner-authorized workspaces or artifact refs.
- `fundability_quality_and_export_review_support`: Support MAG-owned fundability, quality, and export review attempts without declaring verdicts by tool output alone.
- `refs_only_receipt_and_stage_artifact_materialization`: Materialize manifests, pointers, receipt refs, and typed blocker refs without storing grant bodies in OPL-owned runtime state.

## Forbidden Authority

- Tools do not declare fundability-ready, quality-ready, export-ready, submission-ready, App release ready, or production ready.
- Tools do not write grant truth, strategy memory body, package body, owner receipt, or typed blocker unless the MAG authority surface for that stage explicitly authorizes it.
- Tools do not prescribe executor order, candidate strategy, stage goal, or required parallelism.
