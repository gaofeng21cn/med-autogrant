**English** | [中文](./domain-positioning.zh-CN.md)

# Med Auto Grant Domain Positioning

## What It Is

`Med Auto Grant` is the document-first scaffold for the future medical implementation of `Grant Foundry`.
Its intended role is an author-side, proposal-facing `Grant Ops` domain gateway and harness for medical grant applications.

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
- one shared base with two modes:
  - `Auto`
  - `Human-in-the-loop`

## Public Surface Status

Current status:

- repository scaffold exists
- top-level public docs exist
- internal Chinese design and plan artifacts exist
- runtime implementation is intentionally deferred until the MVP schema and execution path are frozen

