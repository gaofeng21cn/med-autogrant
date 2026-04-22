<p align="center">
  <a href="./README.md"><strong>English</strong></a> | <a href="./README.zh-CN.md">中文</a>
</p>

# Med Auto Grant

**An independent medical grant domain agent for investigator-side authoring on a specified funding call**

> `Med Auto Grant` is an independent medical grant domain agent. It keeps specified-funder body authoring, critique, revision, and scientific review-package delivery on one line for investigator-side medical grant applications.

<table>
  <tr>
    <td width="33%" valign="top">
      <strong>Who It Serves</strong><br/>
      Doctors, PIs, faculty members, and medical research teams preparing investigator-side grant applications
    </td>
    <td width="33%" valign="top">
      <strong>What It Organizes</strong><br/>
      A specified funding call, prior work, pilot evidence, draft versions, review comments, and review-package files inside one workspace
    </td>
    <td width="33%" valign="top">
      <strong>How To Start</strong><br/>
      Tell it the target funding call, your current draft/materials, scientific claims to defend, and the review package you need
    </td>
  </tr>
</table>

## One-Sentence Quick Start

You can start with prompts like:

- "Use this NSFC call and this draft to rebuild title, abstract, aims, and methods so the scientific story is internally consistent."
- "Review this current draft for claim-evidence gaps and rewrite the weak sections without changing the target funding call."
- "Review this draft like a grant reviewer, tell me the biggest weaknesses, and show me how to revise them."

## What It Helps With

- Turning prior work, pilot data, and applicant materials into a stronger title, abstract, aims, and research plan under a specified funding call.
- Keeping revision rounds, reviewer-style critique, and version changes traceable inside one workspace.
- Comparing proposal quality across versions through structured scorecards, issue closure, and evidence-gap reports.
- Running longer controller-led authoring cycles that can continue, roll back, or stop with a blocker report.
- Delivering a scientifically complete review-ready package before portal-facing formal checks.
- Tracking formal/objective supplements as explicit TODO wakeups, instead of blocking body authoring by default.

## How It Works

- Applicants provide the target funding call, existing evidence, constraints, and final judgment.
- The AI operator helps with scientific structure, drafting, critique, and revision within that call.
- The workspace keeps comments, versions, and deliverable files together so the proposal line stays reviewable.

## Current Boundary

- `Med Auto Grant` is an independent medical grant domain agent, not an internal module inside the `OPL` workspace.
- It can be called directly by `Codex` or other general agents through `CLI` / `MedAutoGrantDomainEntry`, and can also be federated by `OPL`.
- MAG task scope is locked to body authoring for a specified funding call.
- Scientific completion is delivered as a review-ready package; formal/objective supplements are tracked separately.
- Formal/objective supplements default to `TODO + explicit wakeup` and do not block body authoring unless they directly break scientific validity.
- `OPL` keeps family-level session/runtime/projection and shared modules/contracts/indexes.
- Human gate decisions stay inside the same funding-call task and are author decisions, not cross-funder reselection.
- External funding portal submission stays under human supervision.

## How To Read This Repository

1. Potential users should start here, then continue to the [Docs Guide](./docs/README.md), [Domain Positioning](./docs/domain-positioning.md), and [MVP Scope](./docs/mvp-scope.md).
2. Technical readers and planners should read [Project](./docs/project.md), [Status](./docs/status.md), [Architecture](./docs/architecture.md), [Invariants](./docs/invariants.md), [Decisions](./docs/decisions.md), and [Contracts Overview](./contracts/README.md).
3. Developers and maintainers should continue into `docs/specs/`, `docs/references/`, `docs/plans/`, and [History Archive](./docs/history/README.md).

## Agent And Operator Quick Start

<details>
  <summary><strong>Start here if you are handing this repo to Codex or another agent</strong></summary>

- Read the [Docs Guide](./docs/README.md) first. It summarizes the current technical picture, the formal-entry matrix, and where repo-tracked truth lives.
- Then read [Contracts Overview](./contracts/README.md) and [`contracts/runtime-program/current-program.json`](./contracts/runtime-program/current-program.json). That is the fastest path to the active product-entry shell, schema-backed surfaces, and current mainline pointer.
- Treat [Project](./docs/project.md), [Status](./docs/status.md), [Architecture](./docs/architecture.md), [Invariants](./docs/invariants.md), and [Decisions](./docs/decisions.md) as the public and technical truth set before changing routes or wording.
- The current formal-entry matrix is `CLI`, `MCP`, and `controller`. `CLI` / `MedAutoGrantDomainEntry` are the agent-entry surfaces; `product entry/frontdesk/direct-entry/user-loop` are the lightweight direct-entry and projection shell.
- Current machine-readable governance surfaces include `workspace quality-scorecard`, `workspace quality-diff`, and `pass autonomy-controller`.

</details>

## Further Reading

- [Docs Guide](./docs/README.md)
- [Domain Positioning](./docs/domain-positioning.md)
- [MVP Scope](./docs/mvp-scope.md)
- [Project](./docs/project.md)
- [Status](./docs/status.md)
- [Architecture](./docs/architecture.md)
- [Invariants](./docs/invariants.md)
- [Decisions](./docs/decisions.md)
- [Contracts Overview](./contracts/README.md)
