**English** | [中文](./domain-positioning.zh-CN.md)

# Med Auto Grant Domain Positioning

## What It Is

`Med Auto Grant` is an independent author-side, proposal-facing medical `Grant Ops` domain agent.
Its public first subject is the single `Med Auto Grant` app skill. Under that skill, `CLI` / `MedAutoGrantDomainEntry` provide the stable agent entry, while product-entry / direct-entry / projection surfaces remain internal command contracts for medical grant applications. The current public capability contract is frozen as `CLI/domain-entry stable capability surface + Codex-default execution + explicit hosted runtime carriers`.
MAG may reuse family-level harness contracts and OPL-side runtime-management conventions, but OPL does not own MAG grant truth, authoring execution, or submission-ready export gates.

## What It Is Not

`Med Auto Grant` is not:

- a paper-writing branch of `Research Ops`
- a reviewer-owned grant review surface
- a template filler that only completes sections
- proof that the full runtime is already implemented

## Boundary

The core boundary is the medical grant-writing loop on the applicant side:

- applicant profile and track record
- reusable project evidence and preliminary results
- direction and topic selection
- scientific-question refinement
- argument-chain construction
- application drafting
- mentor-style critique and revision planning

## Relation To Research Ops

`Med Auto Grant` is expected to reuse many upstream assets from medical `Research Ops`, such as:

- publications and previous outputs
- project evidence
- preliminary experiments
- literature memory
- audit and governance language

But it keeps an independent domain boundary because grant writing is not the same as research execution or manuscript submission.

## Operating Doctrine

The repository follows two shared architectural rules:

- `Agent-first` rather than `fixed-code-first`
- the current repository mainline is `Auto-only`
- any future `Human-in-the-loop` product should reuse the same substrate as a compatible sibling or upper-layer product rather than forcing same-repo dual-mode logic

Its formal-entry matrix is:

- `default_formal_entry`: `CLI`
- `supported_protocol_layer`: `MCP`
- `internal_controller_surface`: `controller`

## Public Surface Status

Current status:

- top-level public docs exist
- internal Chinese design and current-truth artifacts exist
- the stable public capability surface is landed and remains Codex-default by default
- product-entry, frontdesk, direct-entry, and user-loop surfaces remain below the app skill as internal command contracts / direct-product projections
- the current active phase is `P4 mature direct grant product entry`
- the current active tranche is `P4.G authoring-quality-first completion semantics alignment`
- `P3 hosted caller / OPL consumption proof` is already completed and retained as historical landing context
- future hosted product deployment remains a later evolution through the same route/export contracts
