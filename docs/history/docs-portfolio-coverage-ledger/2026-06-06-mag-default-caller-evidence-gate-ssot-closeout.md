# MAG default caller evidence-gate SSOT closeout

Owner: `Med Auto Grant`
Purpose: `default_caller_evidence_gate_ssot_closeout`
State: `history_provenance`
Machine boundary: 本文是人读 OPL Doc closeout。当前机器真相继续归 MAG `contracts/runtime-program/current-program.json`、`contracts/private_functional_surface_policy.json`、`contracts/foundry_agent_series.json`、product-entry manifest / functional audit、source/tests、runtime receipts，以及 OPL Framework `agents default-callers` read-model。

## Scope

Semantic theme: `default caller / generated caller evidence gate and no-active-caller proof`

This lane audits whether MAG active/support docs still need a rewrite after the fresh OPL default-caller read-model was available.

It does not authorize physical deletion, does not edit MAG source/tests/contracts, and does not claim grant-ready, submission-ready, production-ready, fundability-ready, quality-ready, export-ready or App release ready.

## SSOT Owners

Machine owners:

- `contracts/runtime-program/current-program.json`
- `contracts/private_functional_surface_policy.json#/purpose_first_owner_delta_domain_thinning_gate`
- `contracts/foundry_agent_series.json#/purpose_first_adapter_thinning_policy`
- product-entry manifest `mag_consumer_thinning_contract` and functional privatization audit
- OPL Framework `agents default-callers --agent mag=<repo>` read-model

Human owners:

- `docs/active/mag-ideal-state-cross-repo-gap-plan.md`
- `docs/active/opl-private-implementation-migration-inventory.md`
- `docs/status.md`
- `docs/architecture.md`
- `docs/docs_portfolio_consolidation.md`

Why they win:

- Contracts and product-entry manifest define the current machine gate and the non-authorizing authority boundary.
- OPL Framework read-model reports generated/default caller evidence as refs-only projection and explicitly keeps physical delete unauthorized.
- The active plan already owns the current gap, evidence gates and next prompt.
- The private inventory already owns per-surface active caller, retained MAG authority, OPL replacement target and deletion gate detail.
- Core/support docs already keep summary and pointers; adding the read-model payload there would recreate a second truth source.

## Live OPL Read-Model

Fresh command:

```bash
rtk ./bin/opl agents default-callers --agent mag=/Users/gaofeng/workspace/med-autogrant
```

Observed summary:

| Signal | Value | SSOT readout |
| --- | --- | --- |
| `blocked_count` | `0` | Replacement / default-caller structural projection is not blocked. |
| `deletion_evidence_worklist_count` | `8` | MAG exposes eight default-caller deletion-gate surface summaries. |
| `missing_domain_owner_receipt_or_typed_blocker_count` | `0` | Required refs-only owner typed-blocker/receipt input is present. |
| `missing_no_active_caller_proof_count` | `0` | No-active-caller proof input is present in the projection. |
| `missing_no_forbidden_write_proof_count` | `0` | No-forbidden-write proof input is present. |
| `missing_tombstone_or_provenance_ref_count` | `0` | Tombstone/provenance input is present. |
| `physical_delete_authorized` | `false` | OPL projection does not authorize MAG repo physical delete. |
| `default_caller_delete_ready` | `false` | Zero missing refs still is not delete-ready. |
| `physical_delete_authorization_status` | `not_authorized_by_opl_projection` | Delete authority remains with MAG domain owner after explicit decision. |
| `next_required_owner_action` | `domain_owner_choose_delete_authorize_keep_or_typed_blocker` | MAG owner must choose delete, keep-as-authority-adapter, or typed blocker. |

The read-model also marks these surfaces as non-authorizing: `opl_agents_conformance`, `opl_agents_default_callers_readiness`, `opl_framework_readiness`, `opl_family_runtime_evidence_worklist_refs_only_receipt`, and `opl_runtime_app_operator_drilldown_projection`.

## Peer Doc Classification

| Surface | Classification | Action |
| --- | --- | --- |
| `docs/active/mag-ideal-state-cross-repo-gap-plan.md` | `covered_by_ssot` | No edit. It already says OPL default-caller replacement/cutover readiness is observed while physical delete, production evidence, App/workbench consumption and long-soak remain gated. |
| `docs/active/opl-private-implementation-migration-inventory.md` | `more_specific_detail` | No edit. It remains the right owner for path-level active caller / retained authority / OPL replacement / retirement gate detail. |
| `docs/status.md` | `covered_by_ssot` | No edit. It summarizes replacement-ready but physical-delete-not-authorized and routes detail to active owners. |
| `docs/architecture.md` | `covered_by_ssot` + `architecture_summary_needed` | No edit. It keeps the architecture-level owner split and avoids repeating the deletion-gate payload. |
| `docs/docs_portfolio_consolidation.md` | `covered_by_ssot` | No edit. It already says direct retirement posture is active-plan/private-inventory owned. |
| `docs/specs/README.md` and `docs/specs/specs_lifecycle_map.md` | `support_current_truth` | No edit. They guard dated specs from becoming default caller or physical-delete authority. |
| `docs/references/med-auto-grant-ideal-state.md` | `target_state_reference` | No edit. It defines the target posture and already forbids turning refs-only evidence into production/default caller completion. |
| `one-person-lab` OPL Framework source/tests | `machine_read_model_owner` | No MAG edit. OPL read-model is consumed as live evidence only. |
| `one-person-lab-app` contracts/docs | `app_projection_support` | No MAG edit. App exposes MAG purpose route and workbench projection, but does not own MAG domain truth or physical-delete authority. |

## No-Rewrite Decision

No active or support MAG doc was rewritten in this lane.

Reason:

- The current active plan and private inventory already encode the semantic distinction that matters: generated/default caller replacement evidence can be observed, yet MAG repo physical deletion remains blocked until an explicit MAG owner delete/keep/blocker decision.
- Repeating the eight-surface OPL read-model payload in status, architecture, docs governance or specs would create a second truth source.
- The only durable delta from this lane is provenance: the recommended next lane was executed as a semantic audit, and the outcome is `no_rewrite_no_physical_delete_authorization`.

## Remaining Scope

This lane closes only the MAG default-caller / generated-caller evidence-gate documentation audit.

Still open:

- explicit MAG owner decision after structural refs are observed: physical delete authorization, keep-as-authority-adapter, or typed blocker;
- production/default caller sustained consumption and App/operator release evidence;
- direct/hosted no-regression follow-through in live use;
- Temporal provider long-soak evidence;
- broader MAG docs portfolio governance by semantic theme.

## Verification

Commands run before closeout writing:

```bash
rtk ./bin/opl agents default-callers --agent mag=/Users/gaofeng/workspace/med-autogrant
rtk /Users/gaofeng/.local/bin/opl-doc-doctor doctor . --format json
```

Observed before writing:

- OPL read-model returned `blocked_count=0`, `deletion_evidence_worklist_count=8`, all missing deletion-evidence counts `0`, `physical_delete_authorized=false`, `default_caller_delete_ready=false`, and `physical_delete_authorization_status=not_authorized_by_opl_projection`.
- MAG doctor returned `finding_count=0` and `active_truth_health.status=pass`.

Final commit verification is recorded in the OPL series ledger after this closeout is committed.
