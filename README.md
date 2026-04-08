<p align="center">
  <a href="./README.md"><strong>English</strong></a> | <a href="./README.zh-CN.md">中文</a>
</p>

# Med Auto Grant

**An in-development medical grant authoring mainline for investigator-side `NSFC`-style applications**

> Status: active development. The repository remains in `P3 / Mentor Critique And Revision Loop Hardening`, with `P3.C / Forced Rollback And Presubmission Gate` currently active; this is still not a production-grade grant-writing system or a submission-ready autopilot.

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
      Minimal runtime baseline is retained, and the active tranche is now <code>P3.C / Forced Rollback And Presubmission Gate</code>
    </td>
  </tr>
</table>

## One-Line Position

If your goal is to turn applicant background, prior work, preliminary evidence, and a candidate topic into a stronger `NSFC`-style proposal direction, `Med Auto Grant` is being built as a medical `Grant Ops` `Domain Harness OS` on the shared `Unified Harness Engineering Substrate` for governed question refinement, argument sharpening, draft expansion, mentor-style critique, structured revision, re-review evidence binding, and explicit verdict gating.

## Runtime Shape (Current And Future)

- Current default local execution shape: `Codex-default host-agent runtime`.
- This repository's current baseline is validated in that host-agent shape.
- Its formal-entry matrix is fixed as: default formal entry `CLI`, supported protocol layer `MCP` (reserved future layer, not yet repo-verified), internal control surface `controller`.
- The current repository mainline is `Auto-only`; any future `Human-in-the-loop` product should reuse the same substrate as a compatible sibling or upper-layer product rather than split this repository into same-repo dual-mode logic.
- Future compatible shape: a managed web runtime on the same substrate, if the core domain contract stays unchanged.

## What It Is Designed To Help With

- Clarify whether a proposed topic is a real scientific question rather than an engineering task or a vague clinical need.
- Organize applicant profile, prior outputs, active projects, and preliminary evidence into one auditable grant workspace.
- Strengthen the necessity and scientific-value chain before spending effort on full drafting.
- Keep applicant-problem fit visible instead of reducing grant writing to template filling.
- Support draft expansion, mentor-style critique, structured revision, and explicit re-review evidence rather than one-shot text generation.

## What Is Already Working

The repository already contains a minimal executable baseline around a frozen `NSFCWorkspace` contract under the current `Codex-default host-agent runtime`.

Today, the runtime can:

- validate structured `NSFC` workspaces across the absorbed `drafting -> critique -> revision` mainline while retaining `major_reframe / major_revision / minor_revision / ready_for_submission` verdict branches
- carry a stable `grant_run_id` across CLI outputs as the formal execution handle for the current hydrated grant run
- summarize explicit `current_selection` bindings for direction, question, fit mapping, draft, and revision-plan identity
- bind a re-review critique to prior completed revision evidence through `MentorCritique.reviewed_revision_plan_id`
- recommend the next stage across `major_reframe -> question_refinement`, `major_revision / minor_revision -> revision`, `ready_for_submission -> frozen`, plus `revision(completed) -> critique -> revision` in the re-review loop
- aggregate the current authoring route into one machine-readable `stage-route-report`
- expose structured `critique-summary` and `stage-route-report` audit data including verdict, current `RevisionPlan.execution_status`, reviewed revision evidence, version labels, and comparison evidence

## What Is Still In Progress

The following pieces are planned but not yet complete:

- forced rollback and presubmission hard gates are the current active hardening tranche and are not fully absorbed yet
- any future `Human-in-the-loop` sibling or upper-layer product surfaces, plus submission-grade delivery
- broader grant-family expansion beyond the first `NSFC` generic skeleton

## Fastest Way To Start

For most medical users, the best entry is through your own agent rather than low-level commands.

Typical flow:

1. Prepare applicant materials, representative outputs, active projects, preliminary evidence, and the target funding brief in one workspace.
2. Ask your agent to first organize them into a structured, auditable grant workspace.
3. Ask your agent to use `Med Auto Grant` to refine the scientific question, tighten the argument chain, expand draft sections, produce critique, drive revision, and keep prior revision evidence visible during re-review.

You can give your agent an instruction like this:

> Read the applicant materials, prior outputs, active projects, preliminary evidence, and the target funding requirements in this workspace first. Organize them into a structured, auditable grant workspace. Then use Med Auto Grant as the medical Grant Ops mainline for an NSFC-style application. Prioritize scientific-question quality, necessity and scientific value, applicant-problem fit, draft consistency, mentor-style critique, and explicit revision evidence before trying to complete submission-facing packaging. If the direction is weak, stop, reframe, or request missing evidence instead of pushing a weak proposal forward.

## Public Docs

- [Docs Index](./docs/README.md)
- [Domain Positioning](./docs/domain-positioning.md)
- [MVP Scope](./docs/mvp-scope.md)

<details>
<summary><strong>Technical And Agent Notes</strong></summary>

### Minimal Runtime Commands

```bash
PYTHONPATH=src python3 -m med_autogrant validate-workspace --input examples/nsfc_workspace_p3c_forced_rollback_argument.json
PYTHONPATH=src python3 -m med_autogrant summarize-workspace --input examples/nsfc_workspace_p3c_forced_rollback_argument.json
PYTHONPATH=src python3 -m med_autogrant next-step --input examples/nsfc_workspace_p3c_forced_rollback_argument.json
PYTHONPATH=src python3 -m med_autogrant critique-summary --input examples/nsfc_workspace_p3c_forced_rollback_argument.json
PYTHONPATH=src python3 -m med_autogrant stage-route-report --input examples/nsfc_workspace_p3c_forced_rollback_argument.json
PYTHONPATH=src python3 -m med_autogrant validate-workspace --input examples/nsfc_workspace_p3c_presubmission_frozen.json
```

### Current Technical Scope

- schema-backed `NSFCWorkspace` validation
- explicit `grant_run_id` / `workspace_id` / `draft_id` separation for runtime and CLI surfaces
- machine-readable mentor verdict contract across `major_reframe / major_revision / minor_revision / ready_for_submission`
- machine-readable re-review linkage through `active_revision_plan_id`, `reviewed_revision_plan_id`, and `reviewed_revision_evidence`
- machine-readable forced rollback and presubmission gate fields through `forced_rollback_stage`, `forced_rollback_reason`, and `presubmission_frozen`
- machine-readable critique, verdict, and route artifacts
- tests covering runtime and control-surface invariants

### Internal Docs

- [`docs/domain-harness-os-positioning.md`](./docs/domain-harness-os-positioning.md)
- [`docs/specs/2026-04-06-med-auto-grant-top-level-design.md`](./docs/specs/2026-04-06-med-auto-grant-top-level-design.md)
- [`docs/specs/2026-04-06-nsfc-main-flow-and-critique-loop.md`](./docs/specs/2026-04-06-nsfc-main-flow-and-critique-loop.md)
- [`docs/specs/2026-04-06-object-model-schema-v1.md`](./docs/specs/2026-04-06-object-model-schema-v1.md)
- [`docs/specs/2026-04-06-med-autogrant-mainline-and-omx-bridge.md`](./docs/specs/2026-04-06-med-autogrant-mainline-and-omx-bridge.md)
- [`docs/specs/2026-04-07-p2c-draft-critique-revision-skeleton-mainline-current-truth.md`](./docs/specs/2026-04-07-p2c-draft-critique-revision-skeleton-mainline-current-truth.md)
- [`docs/specs/2026-04-07-p3a-mentor-verdict-contract-freeze-current-truth.md`](./docs/specs/2026-04-07-p3a-mentor-verdict-contract-freeze-current-truth.md)
- [`docs/specs/2026-04-08-p3b-revision-transition-and-re-review-hardening-current-truth.md`](./docs/specs/2026-04-08-p3b-revision-transition-and-re-review-hardening-current-truth.md)
- [`docs/specs/2026-04-08-p3c-forced-rollback-and-presubmission-gate-current-truth.md`](./docs/specs/2026-04-08-p3c-forced-rollback-and-presubmission-gate-current-truth.md)

### Local Operator State

Local operator and runtime state remains machine-specific and is intentionally excluded from the public GitHub-facing source surface.
</details>
