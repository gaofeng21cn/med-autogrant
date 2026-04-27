# AI-first Quality Boundary Current Truth

Date: `2026-04-27`

This note freezes the AI-first quality boundary for `Med Auto Grant`. It captures the cross-project lesson from the RCA fix: schema-backed packs, scorecards, dossiers, gates, and controller reports can preserve structure, evidence references, and mechanical readiness, but they do not own grant-quality judgment. Authoring quality and critique judgment must come from AI-authored author / reviewer artifacts.

## Boundary

- Authoring executor and critique executor own AI-authored prose, scientific critique, reviewer judgment, and revision intent.
- `grant_quality_scorecard` and `grant_quality_closure_dossier` are AI-critique-backed aggregators. They can summarize completeness, structural scores, evidence links, lineage, queues, and blockers.
- Scorecard fields, schema completeness, evidence-link presence, and numeric scores are structural signals. They cannot independently promote a workspace to `near_submission_candidate` or `submission_grade_candidate`.
- Without an active AI-backed critique or equivalent AI-authored quality assessment, the scorecard must stay `assessment_owner=projection_only` with `ai_reviewer_required=true`.

## Candidate status rule

Candidate-ready states are allowed only when the active critique provenance is AI reviewer backed.

Allowed AI-backed critique owners are:

- `Codex CLI critique executor`
- `Hermes-native critique proof executor`

If the active critique is missing, stale, unowned, or not one of those owners:

- `overall_status` must not become `near_submission_candidate`.
- `overall_status` must not become `submission_grade_candidate`.
- Autonomy controller `quality_status` must remain `not_ready`.
- The blocker list must include `ai_reviewer_required` semantics.

## Revision executor rule

`revision_executor` is a mechanical apply layer. It may only apply AI-authored `revision_plan.items[].mutation_payload`.

It must not:

- generate replacement prose itself;
- synthesize fallback text;
- fill missing mutation payloads from templates;
- repair prose by heuristic post-processing.

If the active AI-backed critique or mutation payload is absent, the revision executor must fail closed.

## Development checklist

- Before adding a quality-ready state, identify the AI artifact that owns the judgment.
- Before mapping a scorecard into autonomy status, check `assessment_owner` and `ai_reviewer_required`.
- Before adding revision execution behavior, confirm every prose mutation comes from `mutation_payload`.
- Keep schema/gate/controller code as aggregation and routing layers; do not let them become hidden authors or hidden reviewers.
- Add or update AI-first boundary tests when any scorecard, dossier, critique, revision, or autonomy quality mapping changes.

## Verification

Relevant guardrails:

- `tests/test_ai_first_quality_boundary.py`
- `tests/test_grant_quality.py`
- `tests/test_grant_autonomy_controller.py`
- `tests/test_critique_executor.py`
- `tests/test_revision_executor.py`
- `scripts/verify.sh meta`
- `scripts/verify.sh`
