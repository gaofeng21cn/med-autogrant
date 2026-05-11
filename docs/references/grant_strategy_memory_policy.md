# Grant Strategy Memory Policy

Status: `active reference`
Date: `2026-05-11`
Owner: `Med Auto Grant`
Purpose: define how reusable grant-writing strategy experience should be captured without turning MAG into a rigid recipe engine.
State: `reference`
Machine boundary: this is a human-readable policy. Machine truth remains in MAG contracts, schemas, source code, workspace records, quality scorecards, closure dossiers, controller reports, stage route reports, and submission-ready package surfaces. The repo-tracked migration/apply/locator surfaces are `contracts/runtime-program/opl-family-contract-adoption.json`, `contracts/runtime-program/domain-memory-seed-fixture.json`, `/product_entry_manifest/domain_memory_descriptor`, and `/product_entry_manifest/domain_memory_descriptor_locator`.

## Conclusion

MAG has several surfaces that look like reusable recipes: fundability strategy, specific aims structure, funder family grammar, reviewer-style critique patterns, template strategy, and closure-package experience.

They should be managed primarily as natural-language strategy memory while they remain exploratory. The memory should help Codex reason inside the relevant MAG stage, not mechanically decide grant strategy before the workspace context is read.

The correct shape is:

- prose-first strategy memory cards;
- minimal searchable metadata;
- stage-specific retrieval;
- writeback proposals from closeout / critique rounds;
- strict separation from quality and export authority.

The incorrect shape is:

- a universal grant recipe engine;
- a prompt stuffed with every funder strategy;
- a rigid schema that decides aims, innovation, or fundability without stage work;
- a scorecard replacement that bypasses MAG quality gates.

## Suitable Memory Content

Good grant strategy memories include:

- funder/call fit lessons that recur across workspaces;
- specific aims patterns that made a biomedical proposal easier to defend;
- reviewer objections that repeatedly require earlier evidence, feasibility, applicant-fit, or risk-mitigation work;
- route pivots that improved fundability within the same funding-call task;
- family-specific strategy caveats for NSFC, NIH R21, Wellcome Discovery, or future admitted profiles;
- closure-package patterns that explain what kind of evidence usually resolves a hard issue.

Bad memory writebacks include:

- the current proposal's claim support;
- private workspace evidence that belongs in the authoring record;
- quality verdicts that belong in `grant-quality-scorecard` or `grant-quality-closure-dossier`;
- submission/export readiness assertions;
- portal checklist state or administrative supplement completion.

## Current Candidates

| surface | memory treatment |
| --- | --- |
| `fundability_strategy` stage lessons | Natural-language memory candidate. |
| `specific_aims_and_structure` stage lessons | Natural-language memory candidate. |
| `grant_family_registry.py` common grant grammar and funder-specific profile split | Keep source as the active structured profile layer; reusable prose around why a profile works can become memory. |
| reviewer-style critique and rebuttal patterns | Natural-language memory candidate, with current-workspace issues staying in quality ledgers. |
| template strategy and proposal structure examples | Natural-language memory unless they become audited export/package templates. |
| `grant-quality-scorecard`, `grant-quality-diff`, `grant-quality-closure-dossier` | Strong schema-backed governance surfaces; not memory. |
| `execute-grant-autonomy-controller` report and blocker queues | Strong controller / runtime surfaces; memory may only reference reusable lessons from closeout. |
| `package submission-ready` | Strong local export surface; not memory authority. |

## Stage Use

Memory should be retrieved in small, relevant sets:

- `call_and_candidate_intake`: retrieve memories about call fit, topic scope, and early red flags.
- `fundability_strategy`: retrieve funder-specific strategy memories and prior fundability failure modes.
- `specific_aims_and_structure`: retrieve aims patterns, innovation framing, and claim-evidence structure lessons.
- `proposal_authoring`: retrieve prose strategy, section-structure caveats, and applicant-fit handling.
- `review_and_rebuttal`: retrieve recurring reviewer objections and closure-package patterns.
- `package_and_submit_ready`: retrieve only export-process lessons that do not override submission-ready gates.

The retrieved memory can influence reasoning and drafting strategy. It cannot issue fundability, quality, or export verdicts.

## OPL Boundary

OPL may index memory refs, carry stage knowledge refs, display consumed-memory provenance, and route writeback receipts. OPL must not own MAG grant strategy content, fundability judgment, authoring quality verdict, or submission-ready export authority.

Family-level governance for this boundary is tracked in `/Users/gaofeng/workspace/one-person-lab/docs/references/operating-governance/family-domain-memory-governance.zh-CN.md`.

## Now / Next / Defer

Now:

- keep this policy as the MAG memory owner reference;
- continue using existing structured quality/controller/export surfaces as authority;
- expose a repo-source migration plan, seed fixture, writeback proposal generator, accept/reject command, receipt locator, controlled consumed-memory proof, writeback receipt proof, and operator receipt projection for domain memory migration without storing real memory entries in repo source.
- expose the top-level `domain_memory_descriptor` as the standard `family_domain_memory_ref.v1` adapter, while keeping `domain_memory_descriptor_locator` as the MAG-owned detailed locator/apply contract.

Next:

- apply real runtime memory writebacks only in workspace/runtime artifact roots after MAG accept/reject decisions;
- extend operator UI consumption of accepted/rejected receipt refs without copying memory body into OPL.

Defer:

- a cross-funder recipe engine;
- automatic aims selection by schema;
- OPL-owned grant strategy content;
- quality or fundability scores generated from memory alone.
