# Authoring Quality Gate

## Gate Purpose

This gate decides whether the proposal draft has passed independent reviewer-style critique and issue closure.

## Evidence To Review

- Reviewable draft refs, accepted aims, section map, and claim/source ledger.
- AI-authored critique artifacts, reviewer feedback, quality-diff refs, issue matrix, and closure dossier.
- Funder review criteria, call fit, reviewer risks, unsupported claims, and package-facing gaps.

## AI-First Judgment Standard

- Quality readiness requires independent critique and closure evidence.
- Scorecards can organize severity and completion, but cannot independently authorize readiness.
- Each major issue must have evidence, affected section, required fix, closure criterion, and post-revision status.
- Residual risk may remain only if explicitly judged non-blocking for the call and package stage.

## Forbidden Outputs

- AI-free quality verdicts.
- Schema-completeness ready verdicts.
- Generic lifecycle completion verdicts.
- Section-count or word-count readiness claims.
- Grant artifact mutation without MAG authority.

## Required Output

- `quality_verdict_ref` with critique refs, closure state, residual risk, and owner/provenance refs; or
- Typed blocker with exact unclosed issues; or
- MAG owner receipt ref accepting quality state.

## Blocker Shapes

- `review_artifact_missing`.
- `major_issue_unclosed`.
- `quality_verdict_mechanical`.
- `claim_source_mismatch`.
- `rebuttal_plan_incomplete`.

## Pass Condition

An independent reviewer could inspect the refs and understand why each material weakness is closed or why the stage remains blocked.
