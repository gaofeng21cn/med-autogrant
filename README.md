<p align="center">
  <a href="./README.md"><strong>English</strong></a> | <a href="./README.zh-CN.md">中文</a>
</p>

# Med Auto Grant

**An in-development medical grant authoring mainline for investigator-side `NSFC`-style applications**

> Status: active development. The repository has entered `P2 / NSFC Authoring Mainline Freeze`, with `P2.A / Intake-Direction-Question Mainline` currently active; this is still not a production-grade grant-writing system or a submission-ready autopilot.

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
      Minimal runtime baseline is retained, and the active tranche is now <code>P2.A / Intake-Direction-Question Mainline</code>
    </td>
  </tr>
</table>

## One-Line Position

If your goal is to turn applicant background, prior work, preliminary evidence, and a candidate topic into a stronger `NSFC`-style proposal direction, `Med Auto Grant` is being built as a medical `Grant Ops` `Domain Harness OS` on the shared `Unified Harness Engineering Substrate` for governed question refinement, argument sharpening, mentor-style critique, and revision.

## Runtime Shape (Current And Future)

- Current default local execution shape: `Codex-default host-agent runtime`.
- This repository's current baseline is validated in that host-agent shape.
- Future compatible shape: a managed web runtime on the same substrate, if the core domain contract stays unchanged.

## What It Is Designed To Help With

- Clarify whether a proposed topic is a real scientific question rather than an engineering task or a vague clinical need.
- Organize applicant profile, prior outputs, active projects, and preliminary evidence into one auditable grant workspace.
- Strengthen the necessity and scientific-value chain before spending effort on full drafting.
- Keep applicant-problem fit visible instead of reducing grant writing to template filling.
- Support mentor-style critique and structured revision rather than one-shot text generation.

## What Is Already Working

The repository already contains a minimal executable baseline around a frozen `NSFCWorkspace` contract under the current `Codex-default host-agent runtime`.

Today, the runtime can:

- validate structured `NSFC` workspaces for `input_intake`, `direction_screening`, and `question_refinement`
- carry a stable `grant_run_id` across CLI outputs as the formal execution handle for the current hydrated grant run
- summarize intake artifacts plus explicit `current_selection` bindings for direction and question
- recommend the next stage across `input_intake -> direction_screening -> question_refinement -> argument_building`
- aggregate the early-stage route into one machine-readable `stage-route-report`
- retain later-stage critique/revision baseline checks and structured `critique-summary` support when a downstream workspace is present

## What Is Still In Progress

The following pieces are planned but not yet complete:

- the full end-to-end authoring loop from argument building to stable draft
- explicit modeling of `revision`-internal draft version transitions
- human-in-the-loop gate surfaces and submission-grade delivery
- broader grant-family expansion beyond the first `NSFC` generic skeleton

## Fastest Way To Start

For most medical users, the best entry is through your own agent rather than low-level commands.

Typical flow:

1. Prepare applicant materials, representative outputs, active projects, preliminary evidence, and the target funding brief in one workspace.
2. Ask your agent to first organize them into a structured, auditable grant workspace.
3. Ask your agent to use `Med Auto Grant` to refine the scientific question, tighten the argument chain, produce critique, and drive revision.

You can give your agent an instruction like this:

> Read the applicant materials, prior outputs, active projects, preliminary evidence, and the target funding requirements in this workspace first. Organize them into a structured, auditable grant workspace. Then use Med Auto Grant as the medical Grant Ops mainline for an NSFC-style application. Prioritize scientific-question quality, necessity and scientific value, applicant-problem fit, and mentor-style critique before trying to complete full draft text. If the direction is weak, stop, reframe, or request missing evidence instead of pushing a weak proposal forward.

## Public Docs

- [Docs Index](./docs/README.md)
- [Domain Positioning](./docs/domain-positioning.md)
- [MVP Scope](./docs/mvp-scope.md)

<details>
<summary><strong>Technical And Agent Notes</strong></summary>

### Minimal Runtime Commands

```bash
PYTHONPATH=src python3 -m med_autogrant validate-workspace --input examples/nsfc_workspace_minimal.json
PYTHONPATH=src python3 -m med_autogrant summarize-workspace --input examples/nsfc_workspace_minimal.json
PYTHONPATH=src python3 -m med_autogrant next-step --input examples/nsfc_workspace_minimal.json
PYTHONPATH=src python3 -m med_autogrant critique-summary --input examples/nsfc_workspace_minimal.json
PYTHONPATH=src python3 -m med_autogrant stage-route-report --input examples/nsfc_workspace_minimal.json
```

### Current Technical Scope

- schema-backed `NSFCWorkspace` validation
- explicit `grant_run_id` / `workspace_id` / `draft_id` separation for runtime and CLI surfaces
- runtime route checks for critique, revision, and frozen-stage consistency
- machine-readable critique and route artifacts
- tests covering runtime and control-surface invariants

### Internal Docs

- [`docs/domain-harness-os-positioning.md`](./docs/domain-harness-os-positioning.md)
- [`docs/specs/2026-04-06-med-auto-grant-top-level-design.md`](./docs/specs/2026-04-06-med-auto-grant-top-level-design.md)
- [`docs/specs/2026-04-06-nsfc-main-flow-and-critique-loop.md`](./docs/specs/2026-04-06-nsfc-main-flow-and-critique-loop.md)
- [`docs/specs/2026-04-06-object-model-schema-v1.md`](./docs/specs/2026-04-06-object-model-schema-v1.md)
- [`docs/specs/2026-04-06-med-autogrant-mainline-and-omx-bridge.md`](./docs/specs/2026-04-06-med-autogrant-mainline-and-omx-bridge.md)
- [`docs/plans/2026-04-06-med-autogrant-minimal-scaffold-plan.md`](./docs/plans/2026-04-06-med-autogrant-minimal-scaffold-plan.md)

### Local Operator State

Local operator and runtime state remains machine-specific and is intentionally excluded from the public GitHub-facing source surface.

</details>
