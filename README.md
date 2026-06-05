<p align="center">
  <img src="assets/branding/medautogrant-logo.png" alt="Med Auto Grant logo" width="132" />
</p>

<p align="center">
  <a href="./README.md"><strong>English</strong></a> | <a href="./README.zh-CN.md">中文</a>
</p>

<!--
Owner: Med Auto Grant
Purpose: public repository entry
State: current_public
Machine boundary: Human-readable entry only. Machine truth remains in contracts, schemas, source, CLI/API behavior, product-entry manifest, runtime receipts, and grant workspace artifacts.
-->

# Med Auto Grant

**An AI grant-writing workspace for medical teams, keeping topic framing, body drafting, critique, revision, and review-package delivery on one traceable application line.**

A medical grant proposal is more than a form to fill in. A review-ready application needs the target call, research foundation, scientific question, technical route, applicant fit, and reviewer concerns to stay aligned across many rounds of work.

Once AI moves from "polish this paragraph" to "help me finish this proposal," several problems show up quickly:

- The funding call is fixed, but how should prior papers, pilot evidence, and applicant strengths become one clear scientific story?
- After many revisions, which version solved which problem, and which hard issues remain open?
- Can the system review the draft like a grant reviewer and turn critique into the next revision?
- Can portal forms and objective supplements stay separate from the scientific body instead of blocking the writing loop?
- Can longer writing and revision work continue while the user is away, with progress and blockers left behind for review?

`Med Auto Grant` is built around those questions. For a specified funding task, it keeps material organization, proposal drafting, reviewer-style critique, revision rounds, and review-package delivery inside one workspace so a draft can move toward a version worth showing to experts.

It does not treat grant writing as fixed-template filling. A proposal can keep comparing narrative options, checking claims against evidence, absorbing reviewer-style critique, and producing the next stronger body and review package under the same funding call.

<table>
  <tr>
    <td width="33%" valign="top">
      <strong>Who It Serves</strong><br/>
      Doctors, PIs, faculty members, and medical research teams preparing researcher-led medical grant applications
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

<p align="center">
  <img src="assets/branding/medautogrant-overview-v2.png" alt="Med Auto Grant overview" width="100%" />
</p>

## Core Highlights

**Continuous Writing Around One Funding Call**<br/>
It does not give generic advice. It keeps working under the same target call, organizing materials, rewriting the body, closing issues, and advancing versions.

**From Materials To A Review Package**<br/>
Papers, pilot evidence, applicant background, and constraints are shaped into title, abstract, aims, research plan, technical route, and applicant narrative, then collected into a review-ready proposal package.

**Reviewer-Style Critique That Turns Into Revision**<br/>
Each round can examine scientific question, significance, novelty, technical route, applicant fit, and evidence gaps, then turn the critique into the next draft.

**Traceable Progress And Versions**<br/>
The workspace keeps drafts, comments, version changes, quality scorecards, and evidence-gap reports together so the team can see where the proposal stands.

**Scientific Writing And Portal Supplements Stay Separate**<br/>
Portal submission, formal forms, and objective supplements are tracked as their own follow-up work. The default focus is to make the scientific body reviewable first.

**Room For Judgment And Revision**<br/>
The system does not mechanically revise in a fixed order. It can generate options, compare versions, locate hard weaknesses, rewrite weak sections, and keep the change history plus quality movement in one workspace.

## One-Sentence Quick Start

You can start with prompts like:

- "Use this NSFC call and this draft to rebuild title, abstract, aims, and methods so the scientific story is internally consistent."
- "Review this current draft for claim-evidence gaps and rewrite the weak sections without changing the target funding call."
- "Review this draft like a grant reviewer, tell me the biggest weaknesses, and show me how to revise them."

## What It Helps With

- Turning prior work, pilot data, and applicant materials into a stronger title, abstract, aims, and research plan under a specified funding call.
- Keeping revision rounds, reviewer-style critique, and version changes traceable inside one workspace.
- Comparing proposal quality across versions through structured scorecards, issue closure, and evidence-gap reports.
- Running longer writing and revision cycles that can continue, roll back, or stop with a blocker report.
- Delivering a scientifically complete review-ready package before portal-facing formal checks.
- Tracking formal/objective supplements as explicit follow-up work, instead of blocking body authoring by default.

## How It Works

- Applicants provide the target funding call, existing evidence, constraints, and final judgment.
- The AI operator helps with scientific structure, drafting, critique, and revision within that call.
- The workspace keeps comments, versions, and deliverable files together so the proposal line stays reviewable.
- New intake workspaces are directory scaffolds: `workspace.json` is the canonical document, while lightweight contracts/artifacts can be Git-tracked and local runtime outputs remain ignored.

## Current Boundary

- `Med Auto Grant` is an independent medical grant domain agent, not an internal module inside the `OPL` workspace.
- Its first public surface is the single Med Auto Grant app skill; `Codex`, `OPL`, and other general agents can reach stable capabilities through that skill.
- MAG owns the grant-writing work itself: funding-call understanding, proposal structure, scientific questions, evidence organization, drafting, revision, and review-ready delivery packages. One Person Lab handles hosted runtime, progress display, recovery/retry, and the cross-agent product entry.
- It can be used as the Grant Foundry inside One Person Lab, and it can also be called directly by Codex or another agent through stable capability entries.
- MAG task scope is locked to body authoring for a specified funding call.
- Scientific completion is delivered as a review-ready package; formal/objective supplements are tracked separately.
- Formal/objective supplements default to `TODO + explicit wakeup` and do not block body authoring unless they directly break scientific validity.
- Human gate decisions stay inside the same funding-call task and are author decisions, not cross-funder reselection.
- External funding portal submission stays under human supervision.

<details>
  <summary><strong>Technical OPL / executor boundary</strong></summary>

- `OPL` is the stage-led agent runtime framework that can host MAG as an external domain dependency.
- Within that framework, an Agent executor is the minimum execution unit. `Codex CLI` is the current first-class executor; Hermes-Agent and similar executors are explicit opt-in adapters that must produce auditable receipts and are not assumed to match Codex CLI behavior or quality.
- OPL can schedule stages, wakeups, handoffs, receipts, retries, and projections, while MAG keeps the grant stage pack, prompts, skills, fundability/authoring quality gates, authoring truth, and submission-ready export authority.
- A MAG stage pack gives the executor a goal, context, authority boundary, skills, knowledge refs, tool affordances, and quality gate. The route manages owner and recovery boundaries; it does not pre-script the grant-authoring cognitive strategy.
- MAG's tool catalog is an affordance catalog, not a workflow script: it declares what a tool can do, where it may write, where credentials are bounded, and what authority it cannot sign. The executor decides during the attempt what to read first, whether to run in parallel, which tools to use or skip, and when to ask for a human gate or reviewer.
- MAG remains the owner for grant truth, fundability verdicts, authoring quality verdicts, route ownership, and submission/export authority.
- Domain memory and owner/lifecycle receipt apply are limited to consumed memory refs, writeback proposals, MAG accept/reject decisions, owner/no-regression receipt refs, lifecycle receipt refs, runtime receipt evidence, operator receipt projections, and repo-source layout audit. They do not write fundability verdicts, real grant artifacts, memory bodies, export verdicts, or receipt instances into repo source.
- Historical `OPL Runtime Manager`, Hermes-first, gateway, and local-host runtime wording is provenance or an implementation-provider detail. Temporal's required OPL production-substrate role is owned by OPL Framework and is the default hosted autonomous runtime substrate after task start; it does not become MAG grant-domain runtime truth. MAG remains the grant-truth and authoring-contract owner.

</details>

## How To Read This Repository

1. Potential users should start here, then continue to the [Docs Guide](./docs/README.md), [Domain Positioning](./docs/public/domain-positioning.md), and [MVP Scope](./docs/public/mvp-scope.md).
2. Technical readers and planners should read [Project](./docs/project.md), [Status](./docs/status.md), [Architecture](./docs/architecture.md), [Invariants](./docs/invariants.md), [Decisions](./docs/decisions.md), and [Contracts Overview](./contracts/README.md).
3. Developers and maintainers should continue into `docs/active/`, `docs/specs/`, `docs/references/`, and [History Archive](./docs/history/README.md).

## Agent And Operator Quick Start

<details>
  <summary><strong>Start here if you are handing this repo to Codex or another agent</strong></summary>

- No. Cloning this repo does not auto-install OPL Framework or the hosted runtime. To make MAG usable, first make the current `one-person-lab` checkout or release bundle available, then use the repo-local clean runner commands below to inspect the skill surface or export the domain handler.
- Read the [Docs Guide](./docs/README.md) first. It summarizes the current technical picture, the formal-entry matrix, the stable capability surface, and where repo-tracked truth lives.
- Then read [Contracts Overview](./contracts/README.md) and [`contracts/runtime-program/current-program.json`](./contracts/runtime-program/current-program.json). That is the fastest path to the active product-entry shell, schema-backed surfaces, and current mainline pointer.
- Treat [Project](./docs/project.md), [Status](./docs/status.md), [Architecture](./docs/architecture.md), [Invariants](./docs/invariants.md), and [Decisions](./docs/decisions.md) as the public and technical truth set before changing routes or wording.
- The current formal-entry matrix is `CLI`, `MCP`, and `controller`, but under strict OPL Agent purity those entry shells are cutover surfaces, not final repo-owned control plane. `CLI` / `MedAutoGrantDomainEntry` must shrink to grant-domain handler targets; `product entry/product status/direct-entry/user-loop`, plus local scripts/contracts when schema-backed, are migration inputs or direct projections under the app skill until OPL generated/default callers replace them. OPL/Temporal hosted autonomous runtime is the default post-start runtime posture. Non-default executor or proof backends remain explicit opt-in integration lanes.
- MAG can be invoked directly through its Codex app skill or through OPL. Both routes must converge on the same MAG-owned route, quality, workspace, and export surfaces.
- When an external agent or OPL wants the repo-tracked handler surface directly, use the repo-local clean runner `<med-autogrant-repo>/scripts/run-python-clean.sh -m med_autogrant.cli domain-handler export --input <input_path> --format json`; it returns the MAG domain-handler export, authority refs, typed blocker refs, and generated-surface handoff refs without writing Python artifacts into the checkout.
- For pre-authoring intake, use `<med-autogrant-repo>/scripts/run-python-clean.sh -m med_autogrant.cli workspace initialize-intake --input <selection_input> --workspace-root <workspace_dir> --format json`; the directory gets a workspace-local Git boundary and `workspace.json` becomes the canonical MAG document.
- The single skill descriptor now carries a `runtime_continuity` envelope for direct family-caller consumption, reusing existing `session_continuity` / `progress_projection` / `artifact_inventory` / `runtime_control.semantic_closure` truth for authoring continuity, funding-call lock, quality closure, and the stricter submission-ready gate.
- The product-entry manifest also carries `controlled_domain_memory_apply_proof`, `owner_receipt_contract`, and `lifecycle_guarded_apply_proof`, which let OPL or a direct caller audit consumed grant-strategy memory refs, writeback proposal, accept/reject decision, owner/no-regression receipt refs, lifecycle receipt refs, runtime receipt evidence, operator receipt projection, and repo-source layout without receiving memory body or grant artifacts.
- Current machine-readable governance surfaces include `workspace quality-scorecard`, `workspace quality-diff`, and `pass autonomy-controller`.

</details>

## Maintainer Verification

- Use `./scripts/verify.sh` for the default local gate. It runs the line-budget check, the minimal smoke lane, and the fast non-regression core lane.
- Makefile Python and pytest lanes run through `scripts/run-python-clean.sh` / `scripts/run-pytest-clean.sh`, which route bytecode and pytest cache outside the checkout.
- Use `./scripts/verify.sh smoke` or `make test-cli-smoke` for quick CLI/product/runtime entry health checks.
- Use `./scripts/verify.sh regression` for heavier matrix, product-entry, runtime/session, hosted/export, and regression coverage. Product-entry cases live under `tests/product_entry_cases/` as directly collected regression tests; the old `tests/test_product_entry.py` aggregation surface has been removed.
- Use `./scripts/verify.sh meta`, `./scripts/verify.sh structure`, and `./scripts/verify.sh full` for repo governance, architecture checks, and clean-clone/full-suite baselines.

## Further Reading

- [Docs Guide](./docs/README.md)
- [Domain Positioning](./docs/public/domain-positioning.md)
- [MVP Scope](./docs/public/mvp-scope.md)
- [Project](./docs/project.md)
- [Status](./docs/status.md)
- [Architecture](./docs/architecture.md)
- [Invariants](./docs/invariants.md)
- [Decisions](./docs/decisions.md)
- [Contracts Overview](./contracts/README.md)
