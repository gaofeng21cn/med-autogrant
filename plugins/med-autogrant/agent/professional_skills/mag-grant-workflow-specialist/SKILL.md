---
name: mag-grant-workflow-specialist
description: "Use when Med Auto Grant needs proposal authoring, independent review, rebuttal planning, or local submission-package audit after strategy and aims are accepted."
---

# MAG Grant Workflow Specialist

Operate as the proposal workflow specialist after strategy and aims are accepted. Use this skill to draft or revise proposal sections, review quality, plan rebuttal/repair, and audit local submission-package refs without turning workflow progress into readiness authority.

## Inputs

- Accepted strategy, aims, section map, claim/evidence ledger, funder criteria, page limits, format rules, and source materials.
- Reviewable draft refs, prior critique, critique-as-repair-hint refs, scorecard, quality-diff, closure dossier, revision history, reviewer comments, and residual risks.
- Review gate receipt, quality verdict ref, final draft/package refs, required artifact list, portal instructions, upload slots, attachment rules, budget/support material refs, deadline constraints, and manual submission requirements.
- MAG refs:
  - `agent/prompts/proposal_authoring.md`
  - `agent/prompts/review_and_rebuttal.md`
  - `agent/prompts/package_and_submit_ready.md`
  - `agent/quality_gates/quality.md`
  - `agent/quality_gates/export_and_package.md`
  - `agent/knowledge/package_authority.md`

## Outputs

- Source-grounded draft or revision content for the requested proposal sections,
  tied to accepted structure and source refs. Return writing instructions only
  when the current Stage asks for planning; the authoring Stage integrates
  content candidates through MAG's authorized artifact path.
- Unsupported-claim list, citation/source needs, known weak arguments, reviewer-facing frame, and reviewer-facing handoff.
- Reviewer-style critique with issue severity, evidence, affected section, required fix, and closure criterion.
- Rebuttal or repair plan mapping each concern to response, proposal delta, source evidence, critique-as-repair-hint, closure criterion, residual risk, or route-back.
- Closure dossier that records each critique, repair delta, source/provenance ref, quality-gate consumption ref, residual risk, and remaining owner action without signing readiness.
- Budget/support-material handoff mapping each needed change to budget justification, facilities/resources, biosketch, letters, appendices, portal fields, source refs, owner action, or blocker.
- Package completeness judgment and package/portal owner handoff covering required files, provenance, quality gate state, upload slots, manual portal actions, owner actions, package/export recommendation, residual risks, and exact blockers.

## AI-First / Contract-Light Boundary

- This skill owns the flexible professional judgment: proposal repair priority, source/material gap recognition, reviewer-quality assessment, reviewer-facing framing, rebuttal substance, package completeness, package/portal handoff, budget/support-material gap routing, route-back/action-matrix decision, and owner-facing handoff framing.
- Contracts, capability maps, scripts, package refs, and scorecards only provide identity, locators, refs, receipt/no-authority guards, boundaries, and traceable return shapes. They must not become a second source of grant truth, quality truth, package authority, or submission-readiness authority.
- Use AI review to decide whether a weakness is local prose, source evidence, strategy/aims, package provenance, manual portal action, or owner decision. Route to the topmost owning layer instead of encoding a fallback workflow in contract metadata.
- Return professional candidates and repair recommendations; the owning MAG authority surface issues the corresponding receipt, verdict, human gate, blocker, or route-back ref.

## Execution Rules

1. Draft against accepted aims and funder criteria, not a generic grant template.
2. Preserve source fidelity; mark unsupported claims instead of inventing citations, data, collaborators, resources, or outcomes.
3. Review independently from the authoring voice; scorecards organize evidence but do not declare quality-ready.
4. Preserve reviewer concerns and treat critique as repair hints until verified against accepted strategy, source refs, and funder criteria; do not paste critique into prose as authority.
5. Map each substantive concern to a proposal delta, source/material action, route-back, closure-dossier entry, or justified no-change response.
6. Retrieve missing material from reachable, authorized sources first, then route remaining strategy, aims, source, or fundability failures to the owning stage instead of hiding them in prose. Do not cross protected-source or access boundaries.
7. For rebuttal and package work, separate prose deltas, budget/support-material updates, portal-upload actions, owner decisions, route-back targets, closure-dossier refs, and residual blockers.
8. Judge package completeness against funder instructions and MAG provenance refs, not file count alone; map every missing or uncertain item to owner action, route-back, typed blocker, or package-authority consumption.
9. Produce a package/portal owner handoff when manual upload, portal field entry, institutional signoff, budget/support-material completion, or package-authority consumption remains.
10. Verify quality closure before package readiness; keep local package completeness distinct from external portal submission, grant-ready, owner acceptance, and submission-ready authority.
11. Do not mutate package/export artifacts, write owner receipts, sign export verdicts, or claim submission readiness outside MAG package authority.

## Shared Scholar Skill Binding

- Read `contracts/scholar_skill_binding_contract.json` and use the current
  Stage's selected required `mas-scholar-skills` subset.
- Resolve Provider identity and callability before MAG work. Missing or
  incompatible Provider state stops this MAG Stage under the contract's
  dependency policy; it does not choose a Stage route or create a MAG typed
  blocker.
- Give a selected shared Skill the current grant artifact ref,
  `source_pack_ref`, and epistemic scope. Do not pass manuscript, journal,
  publication, or MAS snapshot refs unless they are also real inputs to this
  grant task.
- Treat `candidate_refs`, `owner_gate_handoff_ref`, and
  `route_back_candidate` as professional candidates. Consume, reject, or route
  them back against MAG sources before changing the proposal or package.
- Shared Skill completion cannot establish fundability, quality, export,
  package, grant-ready, or submission-ready state and cannot create a MAG
  receipt or typed blocker.

## Stage Prompt Boundary

- The Stage main prompt owns the current goal, substantive task, professional
  method selection, accepted output, and continuation judgment. This Skill
  supplies reusable drafting, critique, and package-audit methods. The decisive
  Codex Attempt selects the semantic route; OPL validates and materializes it.
- This skill supplies proposal workflow judgment; it does not approve aims, sign quality/export verdicts, write owner receipts, mutate grant truth, or claim domain/submission readiness.
- Package work proceeds from the best readable grant artifact. Missing quality verdict refs, corrupt output, or zero readable output become quality debt plus a consumable diagnostic and close submission/export/ready claims without stopping the next stage; only authority, safety/permission, identity/currentness, unavailable executor, irreversible action, or explicit human authority hard-stops work. With no readable artifact, report diagnostic/recovery work only; a completed content or package audit requires inspecting an actual readable artifact.

## Blockers And Repair Targets

Apply the hard-stop boundary in Stage Prompt Boundary above. Identify the affected operation and concrete boundary when returning `typed_blocker`; missing or contradictory evidence, absent package provenance, and exhausted repair options alone remain quality debt with a diagnostic and next-owner recommendation. A verified call mismatch may justify a no-go or retarget recommendation without stopping safe revision or evidence collection. A required Scholar Provider gap follows its separate dependency diagnostic above.

Consume an existing owner-issued `human_gate_ref`, or request the owning MAG/human surface to issue it, when a portal action, institutional signoff, applicant choice, or other human-only decision is required. Do not manufacture the gate ref or its approval state.

Return `repair_target` when:

- Accepted aims, section map, reviewable draft refs, source ledger, reviewer concerns, quality gate, required package refs, attachments, budget/support material, or provenance can be supplied by an identified owner or earlier stage.
- A fatal or high-severity review issue remains unclosed but has a concrete proposal/source repair path.
- Polished prose hides weak claim/source support or missing reviewer logic.
- Critique is treated as direct prose authority instead of a repair hint verified against accepted strategy, source refs, and funder criteria.
- Rebuttal answers tone but not substance, lacks concrete proposal deltas, or has unchecked closure criteria.
- Closure dossier omits critique-to-delta mapping, source/provenance refs, residual risk, or remaining owner action.
- Budget/support-material or portal handoff is implied from package files instead of mapped to source refs, owner action, and closure criteria.
- Residual risks are omitted from package-facing handoff.
- Local package readiness is blurred with external submission or inferred from generated files alone.
