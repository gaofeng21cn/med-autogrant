<p align="center">
  <a href="./README.md"><strong>English</strong></a> | <a href="./README.zh-CN.md">中文</a>
</p>

# Med Auto Grant

**A medical grant-writing workspace for investigators preparing structured proposal packages**

> `Med Auto Grant` keeps topic selection, evidence gathering, drafting, critique, revision, and local submission preparation on one line for investigator-side medical grant applications.

<table>
  <tr>
    <td width="33%" valign="top">
      <strong>Who It Serves</strong><br/>
      Doctors, PIs, faculty members, and medical research teams preparing investigator-side grant applications
    </td>
    <td width="33%" valign="top">
      <strong>What It Organizes</strong><br/>
      Topic ideas, prior work, pilot evidence, draft versions, review comments, and application files inside one workspace
    </td>
    <td width="33%" valign="top">
      <strong>How To Start</strong><br/>
      Tell it the grant program, the direction you want to pursue, the materials you already have, and the package you want to prepare
    </td>
  </tr>
</table>

## One-Sentence Quick Start

You can start with prompts like:

- "Help me turn this idea into an NSFC-style application. First judge whether the question is worth writing, then draft the title, abstract, and research aims."
- "Based on my papers, pilot data, and background, give me three grant directions worth pursuing and explain the upside and risk of each."
- "Review this draft like a grant reviewer, tell me the biggest weaknesses, and show me how to revise them."

## What It Helps With

- Narrowing several possible directions into a proposal line worth writing.
- Turning prior work, pilot data, and applicant materials into a stronger title, abstract, aims, and research plan.
- Keeping revision rounds, reviewer-style critique, and version changes traceable inside one workspace.
- Preparing a more complete local package before final human review and portal submission.

## How It Works

- Applicants provide the target program, existing evidence, constraints, and final judgment.
- The AI operator helps with topic refinement, structure, drafting, critique, and revision.
- The workspace keeps comments, versions, and deliverable files together so the proposal line stays reviewable.

## Current Boundary

- `Med Auto Grant` focuses on investigator-side medical grant writing inside the broader `OPL` workspace.
- It covers topic refinement, proposal drafting, revision, and local submission-package preparation.
- Final direction choice, application strategy, and submission decisions stay with the applicant team.
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
- The current formal-entry matrix is `CLI`, `MCP`, and `controller`. The main machine-readable public shell centers on `product build-entry`, `product manifest`, `product frontdesk`, `product direct-entry`, `product user-loop`, and `package submission-ready`.

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
