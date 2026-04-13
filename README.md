<p align="center">
  <a href="./README.md"><strong>English</strong></a> | <a href="./README.zh-CN.md">中文</a>
</p>

# Med Auto Grant

**An in-development medical grant authoring mainline for investigator-side `NSFC`-style applications**

> Status: active development. The repository now runs on a real upstream `Hermes-Agent` runtime substrate while preserving the author-side grant domain in repo-local adapters and domain logic. The previously absorbed `CLI-first + host-agent` line remains only as a historical migration baseline / regression oracle. One-click local `submission-ready` package export is now landed for frozen, evidence-complete workspaces, but the project is still neither an actual hosted runtime nor an external-submission autopilot.

<table>
  <tr>
    <td width="33%" valign="top">
      <strong>Who It Serves</strong><br/>
      Medical researchers, clinical teams, and faculty members preparing investigator-side grant applications
    </td>
    <td width="33%" valign="top">
      <strong>What It Is</strong><br/>
      An author-side, proposal-facing medical <code>Grant Ops</code> <code>Domain Harness OS</code> direction built on the shared <code>Unified Harness Engineering Substrate</code>
    </td>
    <td width="33%" valign="top">
      <strong>Current Maturity</strong><br/>
      A real upstream <code>Hermes-Agent</code> runtime substrate is now landed; the absorbed <code>R5.A</code> host-agent ladder survives only as a historical regression oracle, while the current <code>hermes_runtime.py</code> and <code>domain_entry.py</code> paths should be read as repo-side domain/entry adapters
    </td>
  </tr>
</table>

## One-Line Position

If your goal is to turn applicant background, prior work, preliminary evidence, and a candidate topic into a stronger `NSFC`-style proposal direction, `Med Auto Grant` is being built as a medical `Grant Ops` `Domain Harness OS` on the shared `Unified Harness Engineering Substrate` for governed question refinement, argument sharpening, draft expansion, mentor-style critique, structured revision, re-review evidence binding, and explicit verdict gating.

## Runtime Shape (Current And Future)

- Current executable runtime shape: `CLI-first + real upstream Hermes-Agent runtime substrate`.
- The current `hermes_runtime.py` and `domain_entry.py` paths are repo-side domain/entry adapters; they do **not** replace the upstream runtime substrate owner.
- The previous `Codex-default host-agent runtime` remains a historical compatibility bridge / regression oracle.
- Its formal-entry matrix is fixed as: default formal entry `CLI`, supported protocol layer `MCP` (reserved future layer, not yet repo-verified), internal control surface `controller`.
- The current repository mainline is `Auto-only`; any future `Human-in-the-loop` product should reuse the same substrate as a compatible sibling or upper-layer product rather than split this repository into same-repo dual-mode logic.
- Landed service-safe entry: `MedAutoGrantDomainEntry`, which preserves the CLI command surface as a structured domain-entry contract for future gateway callers.
- The current `product entry` shell and `executor_routing_contract` are now also frozen as schema-backed contract surfaces under `schemas/v1/`, with fail-closed validation at generation time.
- The current honest `P4.E` frontdoor-contract layer is now also landed through `product-entry-manifest` and `product-frontdesk`; both are now independently frozen by `product-entry-manifest.schema.json` and `product-frontdesk.schema.json`, with generation-time fail-closed validation.
- The current honest `P4.F` local-delivery layer is now also landed through `build-submission-ready-package`; it fail-closes on incomplete frozen workspaces and only exports a local `submission_ready_package` when mandatory sections, evidence, outputs, projects, and freeze gates are all satisfied.
- The current controller-owned direct-product projections `grant-progress` and `grant-cockpit` are now also frozen as schema-backed contract surfaces under `schemas/v1/` through `grant-progress.schema.json` and `grant-cockpit.schema.json`, with fail-closed validation at generation time.
- The next honest `P4.B` direct-entry layer is now also landed through `grant-direct-entry`, which composes `grant-progress`, `grant-cockpit`, and the already frozen direct / `opl-handoff` `product_entry` envelopes into one schema-backed, fail-closed direct-entry contract under `grant-direct-entry.schema.json`.
- The current honest `P4.C` companion layer is now also landed through `mainline-status`, `mainline-phase`, and `grant-user-loop`; together they expose the repo mainline snapshot plus the current direct grant user loop without minting a new executor surface, and `grant-user-loop` is now frozen by `grant-user-loop.schema.json`; landed next-action commands now include concrete runtime-state output paths rather than `<output-path>` placeholders.
- The current honest `P4.D` authoring executor layer is now also landed through `execute-direction-screening-pass`, `execute-question-refinement-pass`, `execute-argument-building-pass`, `execute-fit-alignment-pass`, `execute-outline-pass`, `execute-drafting-pass`, and `execute-freeze-pass`; the author-side route ladder from `direction_screening` to `frozen` is now exposed as landed commands rather than pending handoff.
- The hosted-friendly `build-hosted-contract-bundle` export is now also frozen as a schema-backed contract bundle, and it explicitly adds `domain_entry_contract`, `schema_contract`, and `authoring_contract` for future hosted / `OPL` callers.
- The shared `domain_entry_contract` now also exports `supported_commands` and `command_contracts`, so an external caller can construct requests from the frozen contract catalog without repo-local helper code.
- Future compatible shape: a managed web runtime on the same substrate, if the core domain contract stays unchanged.
- Repo-tracked current-program truth now lives at `contracts/runtime-program/current-program.json`; machine-local session, report, prompt, and hook state live under `$CODEX_HOME/projects/med-autogrant/runtime-state/`.
- The ideal target is now explicit: `OPL` remains the family-level top entry, `Hermes-Agent` remains the runtime substrate owner, and `Med Auto Grant` remains the domain truth / authoring owner. The hosted caller / `OPL` consumption proof is now completed, `P4.A / P4.B / P4.C / P4.D / P4.E / P4.F` are now landed as the current shell / loop / executor tranches, and the mature direct grant product entry still remains the next full phase.

## Entry Modes And Product Boundary

Today, `Med Auto Grant` already has real `operator entry` and `agent entry`, and the lightweight structured `product entry` shell is now landed.
A mature grant-facing product experience still remains future work.
That means:

- `operator entry`: human/operator commands, workspace preparation, inspection, and explicit gating
- `agent entry`: `CLI` plus the landed `MedAutoGrantDomainEntry`, called by `Codex` or another host-agent
- `product entry`: `build-product-entry` now lands the lightweight structured shell for both direct entry and `OPL` handoff, while richer grant-facing product UX still remains future work
- `product frontdesk`: `product-frontdesk` now lands the controller-owned direct front door above the same shell, while the actual operator loop still lives in `grant-user-loop`; together with `product-entry-manifest`, it is now independently schema-backed and fail-closed, and the paired manifest/frontdesk now also carry `grant_authoring_readiness`, quickstart guidance, and `build_submission_ready_package` as a user-facing local delivery action while still keeping the maturity boundary honest
- `product preflight`: `product-preflight` now lands the honest startup-check surface for that same direct frontdoor, and the paired manifest/frontdesk now also carry the same `product_entry_preflight` companion for machine-readable callers
- `product start`: `product-start` now exposes one schema-backed start surface with the recommended mode, available modes, resume surface, and human-gate summary aligned with the same direct-entry shell
- `product projection`: `grant-progress` and `grant-cockpit` now land the first controller-owned, read-only direct-product projection as schema-backed, generation-time fail-closed contract surfaces, but they are intentionally not new `domain_entry_contract` executor commands, do not enter the hosted contract bundle command catalog, and do not yet constitute a mature frontend
- `direct entry composition`: `grant-direct-entry` now lands the next controller-owned direct-entry composition surface by reusing `grant-progress`, `grant-cockpit`, and both `build-product-entry` modes, but it still does not become a new service-safe domain executor or hosted bundle command
- `current user loop`: `mainline-status`, `mainline-phase`, and `grant-user-loop` now package the repo mainline snapshot, current direct-entry composition, and route-derived next action into the current inbox-like CLI shell, but they still do not claim a mature web frontend or hosted runtime

The target domain-facing shape is:

`User -> Med Auto Grant Product Entry -> MedAutoGrantDomainEntry -> Hermes Kernel -> Med Auto Grant Domain Harness OS`

Inside the broader `OPL` family, the compatible top-level route is:

`User -> OPL Product Entry -> OPL Gateway -> Hermes Kernel -> Domain Handoff -> Med Auto Grant Product Entry / MedAutoGrantDomainEntry`

That handoff should carry one shared minimum envelope:

- `target_domain_id`
- `task_intent`
- `entry_mode`
- `workspace_locator`
- `runtime_session_contract`
- `return_surface_contract`

On top of that, `Med Auto Grant` adds domain payload such as `workspace_id`, `draft_id`, and `funding_call`.

That shared envelope is now built by `build-product-entry` in both `direct` and `opl-handoff` modes.
So the current honest claim is: the Hermes-backed runtime substrate and the lightweight structured `product entry` shell are landed, while richer grant-facing product experience still remains future work.

## Execution Handle And Durable Surfaces

- `grant_run_id` is the formal execution handle for one hydrated grant run.
- `workspace_id` is the durable aggregate-root identity for the current `NSFCWorkspace`.
- `draft_id` is the draft identity carried across critique and revision rather than regenerated per run.
- `program_id` is the control-plane and report-routing pointer for the active Med Auto Grant mainline.
- Current repo-verified durable report and audit surfaces are `summarize-workspace`, `critique-summary`, and `stage-route-report`.
- Current controller-owned read-only product projection surfaces are `grant-progress` and `grant-cockpit`; they only read the durable truth above plus `build-product-entry` contract hints, they are frozen by `schemas/v1/grant-progress.schema.json` and `schemas/v1/grant-cockpit.schema.json`, and they are intentionally separate from `domain_entry_contract.supported_commands` and the hosted contract bundle command catalog.
- Current controller-owned direct-entry composition surface is `grant-direct-entry`; it packages the read-only projections above together with the direct / `opl-handoff` `product_entry` envelopes, is frozen by `schemas/v1/grant-direct-entry.schema.json`, and still stays outside `domain_entry_contract.supported_commands` and the hosted contract bundle command catalog.
- Current controller-owned user-loop surface is `grant-user-loop`; it packages `grant-direct-entry` together with `mainline-status` / `mainline-phase` and a route-derived next-action card, is frozen by `schemas/v1/grant-user-loop.schema.json`, and still stays outside `domain_entry_contract.supported_commands` and the hosted contract bundle command catalog.
- Current repo-verified runtime entry also includes `probe-upstream-hermes`, `run-local`, `resume-local`, `build-artifact-bundle`, `execute-revision-pass`, `build-final-package`, `build-hosted-contract-bundle`, `build-submission-ready-package`, and `build-product-entry`; together they cover upstream dependency proof, local loop entry and recovery, artifact-bundle production, section-level deterministic revision execution, local final-package export, hosted-friendly contract export, fail-closed local submission-ready package export, and the shared direct / `OPL` handoff shell.
- `build-hosted-contract-bundle` now exports a hosted-friendly handoff contract that explicitly carries `runtime_substrate_contract`, `runtime_state_contract`, `operator_contract`, `domain_entry_contract`, `schema_contract`, and `authoring_contract` alongside execution identity, artifact, and audit surfaces.
- `domain_entry_contract` now also exports `supported_commands` plus per-command `command_contracts`, so an external caller can consume the same catalog from `product_entry` and the hosted bundle.
- `stage-route-report` is the current machine-readable verification/checkpoint aggregation surface and now emits `verification_checkpoint` plus `checkpoint_status`.
- `MedAutoGrantDomainEntry` is the current service-safe structured adapter for CLI-equivalent runtime calls and future gateway reuse.
- Repo-tracked review truth and local durable handoff surfaces stay separate: the former explains the runtime contract, while the latter carries machine-specific resume state.

## What It Is Designed To Help With

- Clarify whether a proposed topic is a real scientific question rather than an engineering task or a vague clinical need.
- Organize applicant profile, prior outputs, active projects, and preliminary evidence into one auditable grant workspace.
- Strengthen the necessity and scientific-value chain before spending effort on full drafting.
- Keep applicant-problem fit visible instead of reducing grant writing to template filling.
- Support draft expansion, mentor-style critique, structured revision, and explicit re-review evidence rather than one-shot text generation.

## What Is Already Working

The repository now contains a landed `CLI-first` runtime on top of a real upstream `Hermes-Agent` substrate while keeping the frozen `NSFCWorkspace` contract and author-side grant semantics in repo-local domain modules. The previous host-agent line is retained only as a historical bridge / regression oracle.

Today, the runtime can:

- prove the landed upstream substrate through `probe-upstream-hermes`, including `hermes`, `hermes acp`, `run_agent.AIAgent`, `hermes_state.SessionDB`, and `acp_adapter.session.SessionManager`
- validate structured `NSFC` workspaces across the absorbed `drafting -> critique -> revision` mainline while retaining `major_reframe / major_revision / minor_revision / ready_for_submission` verdict branches
- carry a stable `grant_run_id` across CLI outputs as the formal execution handle for the current hydrated grant run
- summarize explicit `current_selection` bindings for direction, question, fit mapping, draft, and revision-plan identity
- bind a re-review critique to prior completed revision evidence through `MentorCritique.reviewed_revision_plan_id`
- recommend the next stage across `major_reframe -> question_refinement`, `major_revision / minor_revision -> revision`, `ready_for_submission -> frozen`, plus `revision(completed) -> critique -> revision` in the re-review loop
- aggregate the current authoring route into one machine-readable `stage-route-report`
- emit `verification_checkpoint` / `checkpoint_status` so the current verification, rollback, and frozen-gate semantics stay on one canonical checkpoint surface
- expose structured `critique-summary` and `stage-route-report` audit data including verdict, current `RevisionPlan.execution_status`, reviewed revision evidence, rollback / frozen gate state, version labels, and comparison evidence
- project a direct grant progress / cockpit surface through `grant-progress` and `grant-cockpit`, reusing `summarize-workspace`, `stage-route-report`, `critique-summary`, and `build-product-entry` contract hints as schema-backed, generation-time fail-closed projection contracts without minting new service-safe domain-entry executor commands or hosted bundle command catalog entries
- compose a direct grant entry surface through `grant-direct-entry`, reusing `grant-progress`, `grant-cockpit`, and the direct / `opl-handoff` `build-product-entry` envelopes as one schema-backed, generation-time fail-closed product contract without minting a new service-safe domain-entry executor command
- expose the repo mainline snapshot and the current direct grant user loop through `mainline-status`, `mainline-phase`, and `grant-user-loop`, while keeping them controller-owned and outside the service-safe domain command catalog
- run one Hermes-backed local main-loop pass through `run-local`, derive a machine-readable `stop_reason`, emit a machine-readable `stage_action_envelope` for `stage_action_required`, write a durable local run journal, mirror attempt durability into upstream `SessionDB`, and re-enter that journal through `resume-local`
- write the currently selected direction, question, argument chain, fit mapping, outline, and draft sections into a local `artifact_bundle` through `build-artifact-bundle`, while preserving manifest, lineage, version, and `grant_run_id / workspace_id / draft_id` identity
- execute the frozen section-level deterministic revision contract through `execute-revision-pass` without breaking draft lineage, rollback semantics, or checkpoint boundaries
- assemble a machine-readable local `final_package` through `build-final-package` for freeze-ready / submission-frozen workspaces
- export a hosted-friendly session / state / artifact / audit contract bundle from a landed local final package through `build-hosted-contract-bundle`, with explicit `domain_entry_contract`, `schema_contract`, and `authoring_contract` for future hosted / `OPL` callers
- export a fail-closed local `submission_ready_package` through `build-submission-ready-package` when the frozen workspace also has all mandatory sections, preliminary evidence, representative outputs, and active projects in place
- dispatch the same runtime command set through `MedAutoGrantDomainEntry` as a service-safe structured entry contract for future gateway callers
- build a lightweight structured `product entry` shell through `build-product-entry`, reusing one shared envelope across `direct` and `opl-handoff`
- freeze the landed `product entry`, `product-entry-manifest`, `product-frontdesk`, `executor_routing_contract`, pending handoff surfaces, and hosted contract bundle as schema-backed contract surfaces for future `OPL` / gateway consumption

Within the current repo-tracked truth, there is no further concrete post-`R5.A` local-runtime delta inside the old host-agent line. The current forward path is to keep the landed upstream substrate, service-safe domain entry, and author-side object boundaries green, not to reopen repo-local runtime ownership.

## What Is Still In Progress

The following areas still remain for further hardening or future scope:

- the runtime still needs stronger submission-grade hardening and higher-density authoring judgment, even though the canonical local walkthrough and revised/final/hosted/submission-ready output-consistency truth is now frozen
- any further submission-grade hardening or stronger authoring-runtime claims require newly frozen repo-tracked truth rather than another implicit post-`R5.A` continuation
- actual hosted runtime, remote execution, Web UI, and multi-tenant hostedization
- a richer grant-facing product experience beyond the landed lightweight structured shell
- any future `Human-in-the-loop` sibling or upper-layer product surface
- Word/PDF finalization, figure generation, and final format checking are still not productized
- external funding-portal submission is still not performed; the landed scope stops at local submission-ready package export
- submission-grade autopilot quality and stronger end-to-end runtime stability
- broader grant-family expansion beyond the first `NSFC` generic skeleton, including `P5` federation

## Fastest Way To Start

For most medical users, the best entry is through your own agent rather than low-level commands.

Typical flow:

1. Prepare applicant materials, representative outputs, active projects, preliminary evidence, and the target funding brief in one workspace.
2. Ask your agent to first organize them into a structured, auditable grant workspace.
3. Ask your agent to use `Med Auto Grant` to refine the scientific question, tighten the argument chain, expand draft sections, produce critique, drive revision, and keep prior revision evidence visible during re-review.

If you want one machine-readable start surface before entering that loop, read:

`uv run python -m med_autogrant product-start --input <workspace.json> --format json`

You can give your agent an instruction like this:

> Read the applicant materials, prior outputs, active projects, preliminary evidence, and the target funding requirements in this workspace first. Organize them into a structured, auditable grant workspace. Then use Med Auto Grant as the medical Grant Ops mainline for an NSFC-style application. Prioritize scientific-question quality, necessity and scientific value, applicant-problem fit, draft consistency, mentor-style critique, and explicit revision evidence before trying to complete submission-facing packaging. If the direction is weak, stop, reframe, or request missing evidence instead of pushing a weak proposal forward.

## Public Docs

- [Docs Index](./docs/README.md)
- [Domain Positioning](./docs/domain-positioning.md)
- [MVP Scope](./docs/mvp-scope.md)
- [Lightweight product entry and OPL handoff](./docs/references/lightweight_product_entry_and_opl_handoff.md) (Chinese only)

## Development Verification

```bash
uv sync --frozen
make test-full
```

Layered local test entrypoints:

- `make test-fast`: default developer slice
- `make test-meta`: program-control and repository-hygiene checks
- `make test-cli-smoke`: CLI validation and local runtime smoke
- `make test-full`: full clean-clone baseline

<details>
<summary><strong>Technical And Agent Notes</strong></summary>

### Minimal Runtime Commands

```bash
TMPDIR="$(mktemp -d)"

# Canonical CLI walkthrough on the landed upstream Hermes substrate

# 0. Probe real upstream Hermes entrypoints and runtime root
uv run python -m med_autogrant probe-upstream-hermes --format json

# 1. Baseline audit for a critique workspace
uv run python -m med_autogrant validate-workspace --input examples/nsfc_workspace_p2c_critique.json --format json
uv run python -m med_autogrant summarize-workspace --input examples/nsfc_workspace_p2c_critique.json --format json
uv run python -m med_autogrant next-step --input examples/nsfc_workspace_p2c_critique.json --format json
uv run python -m med_autogrant critique-summary --input examples/nsfc_workspace_p2c_critique.json --format json
uv run python -m med_autogrant stage-route-report --input examples/nsfc_workspace_p2c_critique.json --format json
uv run python -m med_autogrant mainline-status --format json
uv run python -m med_autogrant mainline-phase --phase current --format json
uv run python -m med_autogrant grant-progress --input examples/nsfc_workspace_p2c_critique.json --format json
uv run python -m med_autogrant grant-cockpit --input examples/nsfc_workspace_p2c_critique.json --format json
uv run python -m med_autogrant grant-direct-entry --input examples/nsfc_workspace_p2c_critique.json --task-intent tighten-grant-mainline --format json
uv run python -m med_autogrant grant-user-loop --input examples/nsfc_workspace_p2c_critique.json --task-intent tighten-grant-mainline --format json
uv run python -m med_autogrant product-start --input examples/nsfc_workspace_p2c_critique.json --format json
uv run python -m med_autogrant build-product-entry --input examples/nsfc_workspace_p2c_critique.json --entry-mode direct --task-intent tighten-grant-mainline --format json

# 2. Deterministic local revision pass
uv run python -m med_autogrant execute-revision-pass --input examples/nsfc_workspace_p2c_critique.json --output "$TMPDIR/r3a-p2c-revised.json" --format json

# 3. Fresh validator / summary / route / checkpoint on the generated revised workspace
uv run python -m med_autogrant validate-workspace --input "$TMPDIR/r3a-p2c-revised.json" --format json
uv run python -m med_autogrant summarize-workspace --input "$TMPDIR/r3a-p2c-revised.json" --format json
uv run python -m med_autogrant next-step --input "$TMPDIR/r3a-p2c-revised.json" --format json
uv run python -m med_autogrant critique-summary --input "$TMPDIR/r3a-p2c-revised.json" --format json
uv run python -m med_autogrant stage-route-report --input "$TMPDIR/r3a-p2c-revised.json" --format json

# 4. Re-review revised-output follow-up must stay on the same local ladder
uv run python -m med_autogrant execute-revision-pass --input examples/nsfc_workspace_p3b_re_review_major_revision.json --output "$TMPDIR/r3a-p3b-revised.json" --format json
uv run python -m med_autogrant validate-workspace --input "$TMPDIR/r3a-p3b-revised.json" --format json
uv run python -m med_autogrant summarize-workspace --input "$TMPDIR/r3a-p3b-revised.json" --format json
uv run python -m med_autogrant next-step --input "$TMPDIR/r3a-p3b-revised.json" --format json
uv run python -m med_autogrant critique-summary --input "$TMPDIR/r3a-p3b-revised.json" --format json
uv run python -m med_autogrant stage-route-report --input "$TMPDIR/r3a-p3b-revised.json" --format json
uv run python -m med_autogrant build-artifact-bundle --input "$TMPDIR/r3a-p3b-revised.json" --output "$TMPDIR/r3a-p3b-revised-bundle.json" --format json
uv run python -m med_autogrant run-local --input "$TMPDIR/r3a-p3b-revised.json" --journal "$TMPDIR/r3a-p3b-revised-run.json" --format json

# 5. Local runtime entry / recovery remains CLI-first
uv run python -m med_autogrant run-local --input examples/nsfc_workspace_p2c_revision.json --journal "$TMPDIR/r1a-revision.json" --format json
uv run python -m med_autogrant resume-local --journal "$TMPDIR/r1a-revision.json" --format json

# 6. Local final / hosted-contract chain
uv run python -m med_autogrant build-artifact-bundle --input examples/nsfc_workspace_p3c_presubmission_frozen.json --output "$TMPDIR/r5a-bundle.json" --format json
uv run python -m med_autogrant build-final-package --input examples/nsfc_workspace_p3c_presubmission_frozen.json --artifact-bundle "$TMPDIR/r5a-bundle.json" --output "$TMPDIR/r5a-final-package.json" --format json
uv run python -m med_autogrant build-hosted-contract-bundle --final-package "$TMPDIR/r5a-final-package.json" --output "$TMPDIR/r5a-hosted-contract.json" --format json
```

### Current Technical Scope

- schema-backed `NSFCWorkspace` validation
- explicit `grant_run_id` / `workspace_id` / `draft_id` separation for runtime and CLI surfaces
- machine-readable mentor verdict contract across `major_reframe / major_revision / minor_revision / ready_for_submission`
- machine-readable re-review linkage through `active_revision_plan_id`, `reviewed_revision_plan_id`, and `reviewed_revision_evidence`
- machine-readable forced rollback and presubmission gate fields through `forced_rollback_stage`, `forced_rollback_reason`, and `presubmission_frozen`
- machine-readable critique, verdict, and route artifacts
- machine-readable Hermes-backed runtime stop reasons, stage-action envelopes, durable run-journal recovery, and upstream `SessionDB` attempt durability
- machine-readable local artifact bundle production with manifest, lineage, version, and bundle summary
- a section-level deterministic local revision executor
- a machine-readable local final package
- hosted-friendly session / state / artifact / audit contract bundle export
- fail-closed local submission-ready package export
- a hosted caller contract proof that lets an external caller consume `domain_entry_contract`, `schema_contract`, `authoring_contract`, `supported_commands`, and `command_contracts` without repo-local helper code
- controller-owned read-only direct-product projections through `grant-progress` and `grant-cockpit`
- controller-owned mainline snapshot / current user loop surfaces through `mainline-status`, `mainline-phase`, and `grant-user-loop`
- a service-safe structured domain entry for CLI-equivalent runtime calls
- tests covering runtime and control-surface invariants

### Internal Docs

- Current fast-cutover truth: `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-12-upstream-hermes-agent-fast-cutover-current-truth.md`
- Current lightweight product-entry truth: `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-12-lightweight-product-entry-and-opl-handoff-current-truth.md`
- Current P4.A direct cockpit/progress truth: `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-12-p4a-direct-grant-cockpit-and-progress-projection-current-truth.md`
- Current P4.C mainline status / user loop truth: `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-12-p4c-mainline-status-and-grant-user-loop-current-truth.md`
- Current hosted caller consumption proof: `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-12-hosted-caller-consumption-proof-current-truth.md`
- Current truth-reset overview: `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-11-upstream-hermes-agent-truth-reset-current-truth.md`
- Historical local runtime program truth: `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-11-hermes-backed-runtime-substrate-program-current-truth.md`
- Historical local runtime capability migration map: `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-11-hermes-backed-runtime-capability-migration-map-current-truth.md`
- Current canonical post-R5A walkthrough truth: `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-10-post-r5a-local-runtime-walkthrough-and-output-consistency-current-truth.md`
- Current post-R5A upper-bound closeout truth: `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-11-post-r5a-local-runtime-upper-bound-honest-stop-current-truth.md`
- [`docs/domain-harness-os-positioning.md`](./docs/domain-harness-os-positioning.md)
- [`docs/specs/2026-04-06-med-auto-grant-top-level-design.md`](./docs/specs/2026-04-06-med-auto-grant-top-level-design.md)
- [`docs/specs/2026-04-06-nsfc-main-flow-and-critique-loop.md`](./docs/specs/2026-04-06-nsfc-main-flow-and-critique-loop.md)
- [`docs/specs/2026-04-06-object-model-schema-v1.md`](./docs/specs/2026-04-06-object-model-schema-v1.md)
- [`docs/specs/2026-04-07-p2c-draft-critique-revision-skeleton-mainline-current-truth.md`](./docs/specs/2026-04-07-p2c-draft-critique-revision-skeleton-mainline-current-truth.md)
- [`docs/specs/2026-04-07-p3a-mentor-verdict-contract-freeze-current-truth.md`](./docs/specs/2026-04-07-p3a-mentor-verdict-contract-freeze-current-truth.md)
- [`docs/specs/2026-04-08-p3b-revision-transition-and-re-review-hardening-current-truth.md`](./docs/specs/2026-04-08-p3b-revision-transition-and-re-review-hardening-current-truth.md)
- [`docs/specs/2026-04-08-p3c-forced-rollback-and-presubmission-gate-current-truth.md`](./docs/specs/2026-04-08-p3c-forced-rollback-and-presubmission-gate-current-truth.md)
- [`docs/specs/2026-04-09-post-r5a-local-runtime-hardening-brief.md`](./docs/specs/2026-04-09-post-r5a-local-runtime-hardening-brief.md)
- [`docs/specs/2026-04-10-post-r5a-revised-workspace-validator-and-operator-alignment.md`](./docs/specs/2026-04-10-post-r5a-revised-workspace-validator-and-operator-alignment.md)
- [`docs/history/omx/README.md`](./docs/history/omx/README.md)

### Local Operator State

Local operator and runtime state remains machine-specific and is intentionally excluded from the public GitHub-facing source surface.
</details>
