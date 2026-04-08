**English** | [中文](./domain-positioning.zh-CN.md)

# Med Auto Grant Domain Positioning

## What It Is

`Med Auto Grant` is the author-side, proposal-facing medical `Grant Ops` mainline under the shared `Unified Harness Engineering Substrate`.
Its role is a medical `Grant Ops` domain gateway and harness for medical grant applications, with a minimal runtime baseline already established in the current `Codex-default host-agent runtime` shape.

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
- `supported_protocol_layer`: `MCP` (reserved future layer, not yet repo-verified)
- `internal_controller_surface`: `controller`

## Public Surface Status

Current status:

- top-level public docs exist
- internal Chinese design and current-truth artifacts exist
- a minimal runtime baseline already exists
- the repository remains in `baseline freeze / runtime hardening`, not in a pre-runtime scaffold stage
- a future managed web runtime remains a later deployment evolution on the same substrate, not proof that the project has not started yet
