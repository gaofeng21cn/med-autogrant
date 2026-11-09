---
name: med-autogrant
description: Use Med Auto Grant (MAG) for medical grant strategy, proposal drafting, review, revision, or local submission-package preparation tied to a funding call or grant workspace. Research papers and standalone document formatting use their own capabilities.
---

# Med Auto Grant

Canonical OPL Agent and Package id is `mag`; `med-autogrant` is the repository, distribution, plugin, and Skill locator. Use only the installed OPL-generated MAG actions as user entrypoints.

## Admission

- Admit MAG when the requested outcome is a grant application or grant-specific strategy/review/package tied to a funding call or an identifiable grant workspace.
- Route research study and paper production to MAS, visual presentations to RCA, and generic document formatting to the relevant document capability unless they are subordinate artifacts of the grant workflow.
- Bind the current funding call, applicant/project context, exact workspace/input refs, task intent, and any accepted upstream decisions. Missing call material is a typed source gap for intake, not permission to invent sponsor requirements.
- Keep sponsor-portal submission, certification, signatures, and other irreversible external actions behind explicit human authority. `submission-ready` means a local package passed MAG gates; it does not mean submitted.

## Action Routing

Use one of the three public actions declared in `contracts/action_catalog.json`:

- `open_grant_user_loop`: default end-to-end entry. Use for a new or continuing funding-call workflow spanning intake, fundability strategy, aims/structure, proposal authoring, and review/rebuttal.
- `build_direct_entry`: enter `proposal_authoring` directly only when the current workspace already contains sufficient accepted call, strategy, and structure refs for the requested bounded authoring task.
- `build_submission_ready_package`: enter `package_and_submit_ready` only when the user explicitly requests a local submission package, provides an output directory, and the human `submission_ready_export_gate` can be satisfied.

Do not expose repo-local CLI commands, `MedAutoGrantDomainEntry`, domain-handler dispatch/export, private scanners, or source-purity wrappers as user entrypoints. They are implementation details or authority targets behind OPL-generated surfaces.

## Default Workflow

1. Select `open_grant_user_loop` unless accepted upstream refs justify a bounded direct authoring or package action.
2. Keep one funding-call identity and OPL StageRun lineage across `call_and_candidate_intake -> fundability_strategy -> specific_aims_and_structure -> proposal_authoring -> review_and_rebuttal -> package_and_submit_ready`.
3. At each Stage, read the current grant artifact, route/quality findings, sponsor requirements, owner decisions, and exact source refs before writing.
4. Let the decisive Codex Attempt route forward, repeat, or return to the highest owning Stage; OPL materializes the transition and MAG retains grant truth and verdict authority.
5. Build the local submission package only after current review evidence, package requirements, output target, and explicit human export approval are present.

## Quality And Hard Stops

- Treat any readable grant draft, fundability judgment, review finding, negative result, partial package, failed attempt, or diagnostic as progress and valid route context.
- Retry, review, and repair counts are quality budgets. On exhaustion, preserve the best artifact and continue as `completed_with_quality_debt`; do not loop until validators clear.
- Static transition tables, schemas, normalizers, validators, generated receipts, provider completion, and tests cannot overrule the decisive semantic route or establish `grant-ready` / `submission-ready`.
- Quality debt closes fundable, grant-ready, submission-ready, export-ready, accepted, and production-ready claims while allowing later declared stages to consume the artifact.
- Only executor unavailability, wrong-target identity/currentness, permission/safety/authority boundaries, missing protected credentials/material, irreversible external submission, or an explicit owner/human decision may hard-stop progress.

## Output Expectations

- Return the selected public action, funding-call/workspace/input identity, exact grant artifact refs, review and package findings, owner/human-gate refs, typed blockers, remaining quality debt, and next owning Stage.
- Distinguish strategy, aims/structure, proposal draft, reviewed candidate, and local submission-ready package. Never describe a package as submitted without exact external human-authorized evidence.
- Preserve MAG-owned fundability, quality, artifact/package, memory, and owner-receipt authority. OPL-generated status or scanner conformance proves transport/structure only.
- Use OPL-generated status/workbench surfaces for progress and resume; do not create a second MAG runtime, queue, session, or lifecycle model.

## References

- `contracts/action_catalog.json`
- `agent/stages/manifest.json`
- `contracts/stage_quality_cycle_policy.json`
- `contracts/owner_receipt_contract.json`
- `contracts/runtime-program/current-program.json`
- `docs/project.md`
- `docs/status.md`

## Durable Knowledge And Source Ownership

Use Framework knowledge preparation and read-context with the authorized
workspace and project bindings. Read the selected bodies and cite knowledge
IDs, scopes and digests. The hosted StageRun freezes one selection for its
producer, reviewer and repair roles; a receipt alone does not load the body.
Hosted actions require workspace_root and project_id resolved from the
workspace inventory; input_path identifies grant materials, not execution
scope. A proposed target_scope never grants source access.

Product methods live in agent/knowledge/, indexed by the v2
contracts/durable_knowledge_catalog.json. Owner/team policies, reusable grant
topic lessons and individual proposal decisions use separate owner, topic and
project scopes. Their content_kind identifies mechanism, policy, state or
decision independently of scope and storage. A current funding call can be a
dated state item without becoming a new memory layer.

Bind existing Obsidian or other Markdown sources in place. Without a personal
library, the workspace's ordinary Markdown directories are the canonical
sources; both modes can be mixed in one task. Do not create another editable
personal library or a compulsory intermediate body projection. Framework
owns source/version/access checks, snapshots and mechanical writeback; the
knowledge owner retains the body, sharing decision and semantic acceptance.

Keep expired, superseded, revoked or source-drifted items out of current use.
Optional strategy gaps permit independent work; required applicant, call or
owner constraints must be resolved before the dependent decision. Recheck
action-critical constraints before export or another consequential action.
Propose lessons to their actual owner and scope, then use the shared accepted
writeback route. Acceptance alone does not prove persistence, and a private
project result is never automatically promoted into the product package.
