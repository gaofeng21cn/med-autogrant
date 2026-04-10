from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
# Post-R5A control surfaces are untracked `.omx/` local state anchored to the
# root checkout, while repo-tracked docs under test still come from this worktree.
CANONICAL_ROOT = Path("/Users/gaofeng/workspace/med-autogrant")
CONTROL_ROOT = CANONICAL_ROOT
README_EN = REPO_ROOT / "README.md"
README_ZH = REPO_ROOT / "README.zh-CN.md"
DOCS_README_EN = REPO_ROOT / "docs" / "README.md"
DOCS_README_ZH = REPO_ROOT / "docs" / "README.zh-CN.md"
PROJECT_TRUTH = REPO_ROOT / "contracts" / "project-truth" / "AGENTS.md"
POSITIONING_DOC = REPO_ROOT / "docs" / "domain-harness-os-positioning.md"
TOP_LEVEL_DESIGN = REPO_ROOT / "docs" / "specs" / "2026-04-06-med-auto-grant-top-level-design.md"
CURRENT_PROGRAM = CONTROL_ROOT / ".omx" / "context" / "CURRENT_PROGRAM.md"
PROGRAM_ROUTING = CONTROL_ROOT / ".omx" / "context" / "PROGRAM_ROUTING.md"
TEAM_PROMPT = CONTROL_ROOT / ".omx" / "context" / "OMX_TEAM_PROMPT.md"
EXECUTION_PROMPT = CONTROL_ROOT / ".omx" / "context" / "OMX_EXECUTION_PROMPT.md"
OMX_BRIDGE = REPO_ROOT / "docs" / "specs" / "2026-04-06-med-autogrant-mainline-and-omx-bridge.md"
RUNTIME_FIRST_PROGRAM = REPO_ROOT / "docs" / "specs" / "2026-04-08-runtime-first-productization-program.md"
RUNTIME_BOUNDARY_MAP = REPO_ROOT / "docs" / "specs" / "2026-04-08-runtime-first-r1-to-r5-boundary-map.md"
R1A_ACTIVATION_PACKAGE = REPO_ROOT / "docs" / "specs" / "2026-04-08-r1a-local-main-loop-entry-and-stop-reason-activation-package.md"
R1B_ACTIVATION_PACKAGE = REPO_ROOT / "docs" / "specs" / "2026-04-08-r1b-stage-action-executor-envelope-activation-package.md"
R2A_ACTIVATION_PACKAGE = REPO_ROOT / "docs" / "specs" / "2026-04-08-r2a-artifact-bundle-production-surface-activation-package.md"
R3A_ACTIVATION_PACKAGE = REPO_ROOT / "docs" / "specs" / "2026-04-08-r3a-critique-revision-executor-surface-activation-package.md"
R3A_MUTATION_CONTRACT = REPO_ROOT / "docs" / "specs" / "2026-04-09-r3a-machine-applicable-revision-mutation-contract.md"
R4A_ACTIVATION_PACKAGE = REPO_ROOT / "docs" / "specs" / "2026-04-09-r4a-final-freeze-and-export-package-activation-package.md"
R5A_ACTIVATION_PACKAGE = REPO_ROOT / "docs" / "specs" / "2026-04-09-r5a-hosted-friendly-session-boundary-activation-package.md"
POST_R5A_HARDENING_SPEC = REPO_ROOT / "docs" / "specs" / "2026-04-10-post-r5a-revised-workspace-validator-and-operator-alignment.md"
POST_R5A_WALKTHROUGH_CURRENT_TRUTH = (
    REPO_ROOT
    / "docs"
    / "specs"
    / "2026-04-10-post-r5a-local-runtime-walkthrough-and-output-consistency-current-truth.md"
)
POST_R5A_STAGE_ROUTE_REPORT_CHECKPOINT_STATUS_PACKAGE = (
    REPO_ROOT
    / "docs"
    / "specs"
    / "2026-04-10-post-r5a-stage-route-report-checkpoint-status-output-consistency-activation-package.md"
)
POST_R5A_WORKTREE_CONTROL_PLANE_ROOT_PACKAGE = (
    REPO_ROOT
    / "docs"
    / "specs"
    / "2026-04-10-post-r5a-worktree-aware-hosted-contract-control-plane-root-resolution-activation-package.md"
)
POST_R5A_LOCAL_RUNTIME_VALIDATION_FAILED_SHAPE_PACKAGE = (
    REPO_ROOT
    / "docs"
    / "specs"
    / "2026-04-10-post-r5a-local-runtime-validation-failed-route-checkpoint-shape-alignment-activation-package.md"
)
POST_R5A_FINAL_PACKAGE_MALFORMED_ARTIFACT_BUNDLE_PACKAGE = (
    REPO_ROOT
    / "docs"
    / "specs"
    / "2026-04-10-post-r5a-final-package-malformed-artifact-bundle-fail-closed-activation-package.md"
)
POST_R5A_HOSTED_CONTRACT_MALFORMED_FINAL_PACKAGE_PACKAGE = (
    REPO_ROOT
    / "docs"
    / "specs"
    / "2026-04-10-post-r5a-hosted-contract-bundle-malformed-final-package-fail-closed-activation-package.md"
)
POST_R5A_HOSTED_CONTRACT_FINAL_PACKAGE_REQUIRED_SCALARS_PACKAGE = (
    REPO_ROOT
    / "docs"
    / "specs"
    / "2026-04-10-post-r5a-hosted-contract-bundle-final-package-required-scalar-fields-fail-closed-activation-package.md"
)
POST_R5A_HOSTED_CONTRACT_FINAL_PACKAGE_REQUIRED_NESTED_FIELDS_PACKAGE = (
    REPO_ROOT
    / "docs"
    / "specs"
    / "2026-04-10-post-r5a-hosted-contract-bundle-final-package-required-nested-fields-fail-closed-activation-package.md"
)
POST_R5A_HOSTED_CONTRACT_FINAL_PACKAGE_CHECKPOINT_SEMANTICS_PACKAGE = (
    REPO_ROOT
    / "docs"
    / "specs"
    / "2026-04-10-post-r5a-hosted-contract-bundle-final-package-checkpoint-semantics-fail-closed-activation-package.md"
)
POST_R5A_HOSTED_CONTRACT_FINAL_PACKAGE_FREEZE_MANIFEST_VALUE_TYPES_PACKAGE = (
    REPO_ROOT
    / "docs"
    / "specs"
    / "2026-04-10-post-r5a-hosted-contract-bundle-final-package-freeze-manifest-value-types-fail-closed-activation-package.md"
)
POST_R5A_FINAL_PACKAGE_ARTIFACT_BUNDLE_REQUIRED_NESTED_FIELDS_PACKAGE = (
    REPO_ROOT
    / "docs"
    / "specs"
    / "2026-04-10-post-r5a-final-package-artifact-bundle-required-nested-fields-fail-closed-activation-package.md"
)
POST_R5A_FINAL_PACKAGE_ARTIFACT_BUNDLE_REQUIRED_SCALAR_VALUE_TYPES_PACKAGE = (
    REPO_ROOT
    / "docs"
    / "specs"
    / "2026-04-10-post-r5a-final-package-artifact-bundle-required-scalar-value-types-fail-closed-activation-package.md"
)
POST_R5A_FINAL_PACKAGE_ARTIFACT_BUNDLE_SUMMARY_COUNT_VALUE_TYPES_PACKAGE = (
    REPO_ROOT
    / "docs"
    / "specs"
    / "2026-04-10-post-r5a-final-package-artifact-bundle-summary-count-value-types-fail-closed-activation-package.md"
)
POST_R5A_FINAL_PACKAGE_ARTIFACT_BUNDLE_ARTIFACT_LIST_VALUE_TYPES_PACKAGE = (
    REPO_ROOT
    / "docs"
    / "specs"
    / "2026-04-10-post-r5a-final-package-artifact-bundle-artifacts-list-value-types-fail-closed-activation-package.md"
)
POST_R5A_FINAL_PACKAGE_ARTIFACT_BUNDLE_ARTIFACT_OBJECT_VALUE_TYPES_PACKAGE = (
    REPO_ROOT
    / "docs"
    / "specs"
    / "2026-04-10-post-r5a-final-package-artifact-bundle-artifacts-object-value-types-fail-closed-activation-package.md"
)
POST_R5A_FINAL_PACKAGE_ARTIFACT_BUNDLE_ARTIFACT_OBJECT_PRIMARY_ID_FIELDS_PACKAGE = (
    REPO_ROOT
    / "docs"
    / "specs"
    / "2026-04-10-post-r5a-final-package-artifact-bundle-artifacts-object-primary-id-fields-fail-closed-activation-package.md"
)
POST_R5A_FINAL_PACKAGE_ARTIFACT_BUNDLE_ARTIFACT_LIST_ELEMENT_SHAPES_PACKAGE = (
    REPO_ROOT
    / "docs"
    / "specs"
    / "2026-04-10-post-r5a-final-package-artifact-bundle-artifacts-list-element-shapes-fail-closed-activation-package.md"
)
POST_R5A_FINAL_PACKAGE_ARTIFACT_BUNDLE_ARTIFACT_OBJECT_LINKAGE_ID_FIELDS_PACKAGE = (
    REPO_ROOT
    / "docs"
    / "specs"
    / "2026-04-10-post-r5a-final-package-artifact-bundle-artifacts-object-linkage-id-fields-fail-closed-activation-package.md"
)
POST_R5A_FINAL_PACKAGE_ARTIFACT_BUNDLE_ARTIFACT_OBJECT_REQUIRED_STRING_FIELDS_PACKAGE = (
    REPO_ROOT
    / "docs"
    / "specs"
    / "2026-04-10-post-r5a-final-package-artifact-bundle-artifacts-object-required-string-fields-fail-closed-activation-package.md"
)
POST_R5A_HOSTED_CONTRACT_FINAL_PACKAGE_LINEAGE_VALUE_TYPES_PACKAGE = (
    REPO_ROOT
    / "docs"
    / "specs"
    / "2026-04-10-post-r5a-hosted-contract-bundle-final-package-lineage-value-types-fail-closed-activation-package.md"
)
OBJECT_MODEL_SCHEMA = REPO_ROOT / "docs" / "specs" / "2026-04-06-object-model-schema-v1.md"
FORMAL_ENTRY_MATRIX = REPO_ROOT / "docs" / "specs" / "2026-04-07-formal-entry-matrix-current-truth.md"
DURABILITY_MODEL = REPO_ROOT / "docs" / "specs" / "2026-04-07-durability-model-clarification.md"
P2B_CURRENT_TRUTH = REPO_ROOT / "docs" / "specs" / "2026-04-07-p2b-argument-fit-outline-mainline-current-truth.md"
P2C_CURRENT_TRUTH = REPO_ROOT / "docs" / "specs" / "2026-04-07-p2c-draft-critique-revision-skeleton-mainline-current-truth.md"
P3A_CURRENT_TRUTH = REPO_ROOT / "docs" / "specs" / "2026-04-07-p3a-mentor-verdict-contract-freeze-current-truth.md"
P3B_CURRENT_TRUTH = REPO_ROOT / "docs" / "specs" / "2026-04-08-p3b-revision-transition-and-re-review-hardening-current-truth.md"
P3C_CURRENT_TRUTH = REPO_ROOT / "docs" / "specs" / "2026-04-08-p3c-forced-rollback-and-presubmission-gate-current-truth.md"
P4A_CURRENT_TRUTH = REPO_ROOT / "docs" / "specs" / "2026-04-08-p4a-verification-gate-surface-current-truth.md"
P4B_CURRENT_TRUTH = REPO_ROOT / "docs" / "specs" / "2026-04-08-p4b-verification-os-and-checkpoint-surface-current-truth.md"
P5A_ACTIVATION_PACKAGE = REPO_ROOT / "docs" / "specs" / "2026-04-08-p5a-second-grant-family-onboarding-activation-package.md"
P5B_ACTIVATION_PACKAGE = REPO_ROOT / "docs" / "specs" / "2026-04-08-p5b-federation-contract-freeze-activation-package.md"
P2C_CRITIQUE_EXAMPLE = REPO_ROOT / "examples" / "nsfc_workspace_p2c_critique.json"
P3B_RE_REVIEW_EXAMPLE = REPO_ROOT / "examples" / "nsfc_workspace_p3b_re_review_major_revision.json"
WORKSPACE_EXAMPLE = REPO_ROOT / "examples" / "nsfc_workspace_minimal.json"
WORKSPACE_SCHEMA = REPO_ROOT / "schemas" / "v1" / "nsfc-workspace.schema.json"
PRD = CONTROL_ROOT / ".omx" / "plans" / "prd-med-autogrant-mainline.md"
TEST_SPEC = CONTROL_ROOT / ".omx" / "plans" / "test-spec-med-autogrant-mainline.md"
IMPLEMENTATION = CONTROL_ROOT / ".omx" / "plans" / "implementation-med-autogrant-mainline.md"
PROGRAM_OPERATING_MODEL = CONTROL_ROOT / ".omx" / "plans" / "spec-program-operating-model.md"
REPORT_DIR = CONTROL_ROOT / ".omx" / "reports" / "med-autogrant-mainline"
LATEST_STATUS = REPORT_DIR / "LATEST_STATUS.md"
ITERATION_LOG = REPORT_DIR / "ITERATION_LOG.md"
OPEN_ISSUES = REPORT_DIR / "OPEN_ISSUES.md"
REPORT_README = REPORT_DIR / "README.md"
LATEST_ABSORBED_RUNTIME_SLICE_ACTIVATION_PACKAGE = R5A_ACTIVATION_PACKAGE
CURRENT_ACTIVE_RUNTIME_SLICE_ACTIVATION_PACKAGE = (
    POST_R5A_FINAL_PACKAGE_ARTIFACT_BUNDLE_ARTIFACT_OBJECT_REQUIRED_STRING_FIELDS_PACKAGE
)

REQUIRED_COMMAND_SNIPPETS = (
    "python3 -m unittest discover -s tests -p 'test_*.py'",
    "python3 -m unittest discover -s tests -p 'test_program_control_surfaces.py'",
    "python3 -m unittest discover -s tests -p 'test_local_runtime.py'",
    "python3 -m unittest discover -s tests -p 'test_artifact_bundle.py'",
    "PYTHONPATH=src python3 -m med_autogrant validate-workspace --input examples/nsfc_workspace_p2c_revision.json --format json",
    "PYTHONPATH=src python3 -m med_autogrant validate-workspace --input examples/nsfc_workspace_p3b_re_review_major_revision.json --format json",
    "PYTHONPATH=src python3 -m med_autogrant validate-workspace --input examples/nsfc_workspace_p3c_forced_rollback_argument.json --format json",
    "PYTHONPATH=src python3 -m med_autogrant validate-workspace --input examples/nsfc_workspace_p3c_presubmission_frozen.json --format json",
    "PYTHONPATH=src python3 -m med_autogrant summarize-workspace --input examples/nsfc_workspace_p2c_revision.json --format json",
    "PYTHONPATH=src python3 -m med_autogrant summarize-workspace --input examples/nsfc_workspace_p3b_re_review_major_revision.json --format json",
    "PYTHONPATH=src python3 -m med_autogrant summarize-workspace --input examples/nsfc_workspace_p3c_forced_rollback_argument.json --format json",
    "PYTHONPATH=src python3 -m med_autogrant summarize-workspace --input examples/nsfc_workspace_p3c_presubmission_frozen.json --format json",
    "PYTHONPATH=src python3 -m med_autogrant next-step --input examples/nsfc_workspace_p2c_revision.json --format json",
    "PYTHONPATH=src python3 -m med_autogrant next-step --input examples/nsfc_workspace_p3b_re_review_major_revision.json --format json",
    "PYTHONPATH=src python3 -m med_autogrant next-step --input examples/nsfc_workspace_p3c_forced_rollback_argument.json --format json",
    "PYTHONPATH=src python3 -m med_autogrant next-step --input examples/nsfc_workspace_p3c_presubmission_frozen.json --format json",
    "PYTHONPATH=src python3 -m med_autogrant critique-summary --input examples/nsfc_workspace_p2c_revision.json --format json",
    "PYTHONPATH=src python3 -m med_autogrant critique-summary --input examples/nsfc_workspace_p3b_re_review_major_revision.json --format json",
    "PYTHONPATH=src python3 -m med_autogrant critique-summary --input examples/nsfc_workspace_p3c_forced_rollback_argument.json --format json",
    "PYTHONPATH=src python3 -m med_autogrant critique-summary --input examples/nsfc_workspace_p3c_presubmission_frozen.json --format json",
    "PYTHONPATH=src python3 -m med_autogrant stage-route-report --input examples/nsfc_workspace_p2c_revision.json --format json",
    "PYTHONPATH=src python3 -m med_autogrant stage-route-report --input examples/nsfc_workspace_p3b_re_review_major_revision.json --format json",
    "PYTHONPATH=src python3 -m med_autogrant stage-route-report --input examples/nsfc_workspace_p3c_forced_rollback_argument.json --format json",
    "PYTHONPATH=src python3 -m med_autogrant stage-route-report --input examples/nsfc_workspace_p3c_presubmission_frozen.json --format json",
    "PYTHONPATH=src python3 -m med_autogrant validate-workspace --input examples/nsfc_workspace_p3a_ready_for_submission.json --format json",
    "PYTHONPATH=src python3 -m med_autogrant summarize-workspace --input examples/nsfc_workspace_p3a_ready_for_submission.json --format json",
    "PYTHONPATH=src python3 -m med_autogrant next-step --input examples/nsfc_workspace_p3a_ready_for_submission.json --format json",
    "PYTHONPATH=src python3 -m med_autogrant critique-summary --input examples/nsfc_workspace_p3a_ready_for_submission.json --format json",
    "PYTHONPATH=src python3 -m med_autogrant stage-route-report --input examples/nsfc_workspace_p3a_ready_for_submission.json --format json",
    "PYTHONPATH=src python3 -m med_autogrant run-local --input examples/nsfc_workspace_p2c_revision.json --journal \"$TMPDIR/r1a-revision.json\" --format json",
    "PYTHONPATH=src python3 -m med_autogrant run-local --input examples/nsfc_workspace_p3b_re_review_major_revision.json --journal \"$TMPDIR/r1b-major-revision.json\" --format json",
    "PYTHONPATH=src python3 -m med_autogrant run-local --input examples/nsfc_workspace_p3c_forced_rollback_argument.json --journal \"$TMPDIR/r1a-rollback.json\" --format json",
    "PYTHONPATH=src python3 -m med_autogrant run-local --input examples/nsfc_workspace_p3a_ready_for_submission.json --journal \"$TMPDIR/r1a-freeze-ready.json\" --format json",
    "PYTHONPATH=src python3 -m med_autogrant run-local --input examples/nsfc_workspace_p3c_presubmission_frozen.json --journal \"$TMPDIR/r1a-frozen.json\" --format json",
    "PYTHONPATH=src python3 -m med_autogrant resume-local --journal \"$TMPDIR/r1a-revision.json\" --format json",
    "PYTHONPATH=src python3 -m med_autogrant build-artifact-bundle --input examples/nsfc_workspace_p2b_outline.json --output \"$TMPDIR/r2a-outline-bundle.json\" --format json",
    "PYTHONPATH=src python3 -m med_autogrant build-artifact-bundle --input examples/nsfc_workspace_p2c_revision.json --output \"$TMPDIR/r2a-revision-bundle.json\" --format json",
    "PYTHONPATH=src python3 -m med_autogrant execute-revision-pass --input examples/nsfc_workspace_p2c_critique.json --output \"$TMPDIR/r3a-p2c-revised.json\" --format json",
    "PYTHONPATH=src python3 -m med_autogrant execute-revision-pass --input examples/nsfc_workspace_p3b_re_review_major_revision.json --output \"$TMPDIR/r3a-p3b-revised.json\" --format json",
    "PYTHONPATH=src python3 -m med_autogrant validate-workspace --input \"$TMPDIR/r3a-p2c-revised.json\" --format json",
    "PYTHONPATH=src python3 -m med_autogrant summarize-workspace --input \"$TMPDIR/r3a-p2c-revised.json\" --format json",
    "PYTHONPATH=src python3 -m med_autogrant next-step --input \"$TMPDIR/r3a-p2c-revised.json\" --format json",
    "PYTHONPATH=src python3 -m med_autogrant critique-summary --input \"$TMPDIR/r3a-p2c-revised.json\" --format json",
    "PYTHONPATH=src python3 -m med_autogrant stage-route-report --input \"$TMPDIR/r3a-p2c-revised.json\" --format json",
    "PYTHONPATH=src python3 -m med_autogrant validate-workspace --input \"$TMPDIR/r3a-p3b-revised.json\" --format json",
    "PYTHONPATH=src python3 -m med_autogrant stage-route-report --input \"$TMPDIR/r3a-p3b-revised.json\" --format json",
    "PYTHONPATH=src python3 -m med_autogrant build-artifact-bundle --input examples/nsfc_workspace_p3a_ready_for_submission.json --output \"$TMPDIR/r4a-freeze-ready-bundle.json\" --format json",
    "PYTHONPATH=src python3 -m med_autogrant build-final-package --input examples/nsfc_workspace_p3a_ready_for_submission.json --artifact-bundle \"$TMPDIR/r4a-freeze-ready-bundle.json\" --output \"$TMPDIR/r4a-freeze-ready-package.json\" --format json",
    "PYTHONPATH=src python3 -m med_autogrant build-artifact-bundle --input examples/nsfc_workspace_p3c_presubmission_frozen.json --output \"$TMPDIR/r4a-frozen-bundle.json\" --format json",
    "PYTHONPATH=src python3 -m med_autogrant build-final-package --input examples/nsfc_workspace_p3c_presubmission_frozen.json --artifact-bundle \"$TMPDIR/r4a-frozen-bundle.json\" --output \"$TMPDIR/r4a-frozen-package.json\" --format json",
    "PYTHONPATH=src python3 -m med_autogrant build-artifact-bundle --input examples/nsfc_workspace_p3c_presubmission_frozen.json --output \"$TMPDIR/r5a-bundle.json\" --format json",
    "PYTHONPATH=src python3 -m med_autogrant build-final-package --input examples/nsfc_workspace_p3c_presubmission_frozen.json --artifact-bundle \"$TMPDIR/r5a-bundle.json\" --output \"$TMPDIR/r5a-final-package.json\" --format json",
    "PYTHONPATH=src python3 -m med_autogrant build-hosted-contract-bundle --final-package \"$TMPDIR/r5a-final-package.json\" --output \"$TMPDIR/r5a-hosted-contract.json\" --format json",
    "git diff --check",
)

POST_R5A_WALKTHROUGH_SNIPPETS = (
    "docs/specs/2026-04-10-post-r5a-revised-workspace-validator-and-operator-alignment.md",
    "PYTHONPATH=src python3 -m med_autogrant validate-workspace --input examples/nsfc_workspace_p2c_critique.json --format json",
    "PYTHONPATH=src python3 -m med_autogrant summarize-workspace --input examples/nsfc_workspace_p2c_critique.json --format json",
    "PYTHONPATH=src python3 -m med_autogrant next-step --input examples/nsfc_workspace_p2c_critique.json --format json",
    "PYTHONPATH=src python3 -m med_autogrant critique-summary --input examples/nsfc_workspace_p2c_critique.json --format json",
    "PYTHONPATH=src python3 -m med_autogrant stage-route-report --input examples/nsfc_workspace_p2c_critique.json --format json",
    "PYTHONPATH=src python3 -m med_autogrant execute-revision-pass --input examples/nsfc_workspace_p2c_critique.json --output \"$TMPDIR/r3a-p2c-revised.json\" --format json",
    "PYTHONPATH=src python3 -m med_autogrant validate-workspace --input \"$TMPDIR/r3a-p2c-revised.json\" --format json",
    "PYTHONPATH=src python3 -m med_autogrant summarize-workspace --input \"$TMPDIR/r3a-p2c-revised.json\" --format json",
    "PYTHONPATH=src python3 -m med_autogrant next-step --input \"$TMPDIR/r3a-p2c-revised.json\" --format json",
    "PYTHONPATH=src python3 -m med_autogrant critique-summary --input \"$TMPDIR/r3a-p2c-revised.json\" --format json",
    "PYTHONPATH=src python3 -m med_autogrant stage-route-report --input \"$TMPDIR/r3a-p2c-revised.json\" --format json",
    "PYTHONPATH=src python3 -m med_autogrant execute-revision-pass --input examples/nsfc_workspace_p3b_re_review_major_revision.json --output \"$TMPDIR/r3a-p3b-revised.json\" --format json",
    "PYTHONPATH=src python3 -m med_autogrant validate-workspace --input \"$TMPDIR/r3a-p3b-revised.json\" --format json",
    "PYTHONPATH=src python3 -m med_autogrant summarize-workspace --input \"$TMPDIR/r3a-p3b-revised.json\" --format json",
    "PYTHONPATH=src python3 -m med_autogrant next-step --input \"$TMPDIR/r3a-p3b-revised.json\" --format json",
    "PYTHONPATH=src python3 -m med_autogrant critique-summary --input \"$TMPDIR/r3a-p3b-revised.json\" --format json",
    "PYTHONPATH=src python3 -m med_autogrant stage-route-report --input \"$TMPDIR/r3a-p3b-revised.json\" --format json",
    "PYTHONPATH=src python3 -m med_autogrant build-artifact-bundle --input \"$TMPDIR/r3a-p3b-revised.json\" --output \"$TMPDIR/r3a-p3b-revised-bundle.json\" --format json",
    "PYTHONPATH=src python3 -m med_autogrant run-local --input \"$TMPDIR/r3a-p3b-revised.json\" --journal \"$TMPDIR/r3a-p3b-revised-run.json\" --format json",
    "PYTHONPATH=src python3 -m med_autogrant build-artifact-bundle --input examples/nsfc_workspace_p3c_presubmission_frozen.json --output \"$TMPDIR/r5a-bundle.json\" --format json",
    "PYTHONPATH=src python3 -m med_autogrant build-final-package --input examples/nsfc_workspace_p3c_presubmission_frozen.json --artifact-bundle \"$TMPDIR/r5a-bundle.json\" --output \"$TMPDIR/r5a-final-package.json\" --format json",
    "PYTHONPATH=src python3 -m med_autogrant build-hosted-contract-bundle --final-package \"$TMPDIR/r5a-final-package.json\" --output \"$TMPDIR/r5a-hosted-contract.json\" --format json",
)

FUTURE_TRANCHE_SNIPPETS = (
    "P2.A / Intake-Direction-Question Mainline",
    "P2.B / Argument-Fit-Outline Mainline",
    "P2.C / Draft-Critique-Revision Skeleton",
    "P3.A / Mentor Verdict Contract Freeze",
    "P3.B / Revision Transition And Re-Review Hardening",
    "P3.C / Forced Rollback And Presubmission Gate",
    "P4.A / Verification Gate Surface",
    "P4.B / Verification OS And Checkpoint Surface",
    "P5.A / Second Grant Family Onboarding",
    "P5.B / Federation Contract Freeze",
)

REVISION_TRANSITION_SNIPPETS = (
    "RevisionPlan.execution_status",
    "pre_revision_version_label",
    "post_revision_version_label",
    "comparison_summary",
    "draft_id",
    "frozen_question_id",
)

RE_REVIEW_TRANSITION_SNIPPETS = (
    "reviewed_revision_plan_id",
    "reviewed_revision_evidence",
    "source_critique_id",
    "active_revision_plan_id",
)

ROLLBACK_GATE_SNIPPETS = (
    "forced_rollback_stage",
    "forced_rollback_reason",
    "presubmission_frozen",
)

EXECUTION_HANDLE_SNIPPETS = (
    "grant_run_id",
    "workspace_id",
    "draft_id",
    "program_id",
)

EXECUTION_HANDLE_REVIEW_SURFACES = (
    README_EN,
    README_ZH,
    PROJECT_TRUTH,
    POSITIONING_DOC,
    OMX_BRIDGE,
    OBJECT_MODEL_SCHEMA,
    FORMAL_ENTRY_MATRIX,
    DURABILITY_MODEL,
    P2B_CURRENT_TRUTH,
    P2C_CURRENT_TRUTH,
    P3A_CURRENT_TRUTH,
    P3B_CURRENT_TRUTH,
    P3C_CURRENT_TRUTH,
    P4A_CURRENT_TRUTH,
    P4B_CURRENT_TRUTH,
    WORKSPACE_EXAMPLE,
    WORKSPACE_SCHEMA,
)

DURABLE_REPORT_SURFACE_SNIPPETS = (
    "summarize-workspace",
    "critique-summary",
    "stage-route-report",
)

VERIFICATION_CHECKPOINT_SNIPPETS = (
    "verification_checkpoint",
    "checkpoint_status",
)

P5_ACTIVATION_SECTION_SNIPPETS = (
    "## Activation Status",
    "## Required Verification",
    "## Promotion Invariants",
    "## Excluded Scope",
)

P5A_ACTIVATION_SNIPPETS = (
    "SecondGrantFamilyAdmissionPackage",
    "repo-tracked second-family source packet",
    "CLI-first",
)

P5B_ACTIVATION_SNIPPETS = (
    "GrantOpsFederationContractPackage",
    "admitted families exact-set",
    "Grant Foundry",
)

R1A_ACTIVATION_SNIPPETS = (
    "run-local",
    "resume-local",
    "stop_reason",
    "latest_route_report",
    "latest_stop_reason",
    "validation_failed",
    "rollback_required",
    "freeze_ready",
    "presubmission_frozen",
    "stage_action_required",
    "grant_run_id",
    "workspace_id",
    "draft_id",
    "program_id",
    "CLI",
    "MCP",
    "controller",
    "not-yet-supported",
)

R1A_RUNTIME_SURFACE_SNIPPETS = (
    "run-local",
    "resume-local",
    "stop_reason",
    "journal",
)

R1B_RUNTIME_SURFACE_SNIPPETS = (
    "stage_action_envelope",
    "latest_stage_action_envelope",
    "action_items",
    "route_reason",
    "resume_decision",
)

R2A_RUNTIME_SURFACE_SNIPPETS = (
    "build-artifact-bundle",
    "artifact bundle",
    "manifest",
    "lineage",
    "bundle summary",
)

R1B_ACTIVATION_SNIPPETS = (
    "stage_action_envelope",
    "latest_stage_action_envelope",
    "stage_action_required",
    "current_selection",
    "resume-local",
    "action_items",
    "route_reason",
    "append_attempt",
    "reuse_grant_run_id",
    "CLI",
    "MCP",
    "controller",
    "not-yet-supported",
)

R2A_ACTIVATION_SNIPPETS = (
    "build-artifact-bundle",
    "artifact_bundle",
    "bundle_version",
    "bundle_kind",
    "grant_run_id",
    "workspace_id",
    "draft_id",
    "program_id",
    "selected_direction_id",
    "selected_question_id",
    "active_fit_mapping_id",
    "active_draft_id",
    "manifest",
    "lineage",
    "bundle_summary",
    "outline_count",
    "section_count",
    "selected_direction",
    "selected_question",
    "argument_chain",
    "fit_mapping",
    "draft_outline",
    "draft_sections",
    "frozen_question_id",
    "CLI",
    "MCP",
    "controller",
    "not-yet-supported",
)

R3A_ACTIVATION_SNIPPETS = (
    "execute-revision-pass",
    "active_revision_plan_id",
    "reviewed_revision_plan_id",
    "reviewed_revision_evidence",
    "source_critique_id",
    "pre_revision_version_label",
    "post_revision_version_label",
    "comparison_summary",
    "forced_rollback_stage",
    "presubmission_frozen",
    "CLI",
    "MCP",
    "controller",
    "not-yet-supported",
)

R3A_IMPLEMENTATION_PROMOTION_SNIPPETS = (
    "## R3.A Implementation Promotion Contract",
    "execute-revision-pass --input examples/nsfc_workspace_p2c_critique.json",
    "execute-revision-pass --input examples/nsfc_workspace_p3b_re_review_major_revision.json",
    "reviewed_revision_plan_id / reviewed_revision_evidence / source_critique_id / active_revision_plan_id",
    "mutation_payload / target_ref / section_key",
)

R3A_MUTATION_CONTRACT_SNIPPETS = (
    "mutation_payload",
    "replace_draft_section",
    "target_section_key",
    "replacement_text",
    "replacement_core_claim",
    "linked_object_ids",
    "section:<section_key>",
    "duplicate target section",
)

R4A_ACTIVATION_SNIPPETS = (
    "build-final-package",
    "final_package",
    "freeze_manifest",
    "checkpoint_summary",
    "export_summary",
    "artifact_bundle_manifest",
    "CLI",
    "MCP",
    "controller",
    "not-yet-supported",
)

R5A_ACTIVATION_SNIPPETS = (
    "build-hosted-contract-bundle",
    "hosted_contract_bundle",
    "formal_entry_matrix",
    "execution_identity",
    "execution_identity.program_id",
    "session_contract",
    "state_contract",
    "artifact_contract",
    "audit_contract",
    "CLI",
    "MCP",
    "controller",
    "not-yet-supported",
)

RUNTIME_BOUNDARY_MAP_SNIPPETS = (
    "R1.B / Stage Action Executor Envelope",
    "R2.A / Artifact Bundle Production Surface",
    "R3.A / Critique Revision Executor Surface",
    "R4.A / Final Freeze And Export Package",
    "R5.A / Hosted-Friendly Session Boundary",
    "One-Shot Autonomous Continuation Contract",
    "Honest Reclassification Rules",
    "当前 latest absorbed runtime slice：`R5.A / Hosted-Friendly Session Boundary`",
    "post-`R5.A` local runtime hardening / truth-sync",
)

RUNTIME_FIRST_SNIPPETS = (
    "R1 / Autonomous Main Loop",
    "R2 / Artifact Production Surface",
    "R3 / Critique Revision Autoloop",
    "R4 / Finalization And Export Surface",
    "R5 / Hostedization Prep",
    "latest absorbed runtime slice 已是 `R5.A / Hosted-Friendly Session Boundary`",
    "post-`R5.A` local runtime hardening",
)

RUNTIME_BOUNDARY_CONTROL_SURFACES = (
    CURRENT_PROGRAM,
    PROGRAM_ROUTING,
    TEAM_PROMPT,
    EXECUTION_PROMPT,
    PRD,
    TEST_SPEC,
    IMPLEMENTATION,
    LATEST_STATUS,
)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def canonical_repo_path(path: Path) -> str:
    try:
        return str(CANONICAL_ROOT / path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def extract_phase_pointer(document: str) -> tuple[str, str]:
    match = re.search(r"## Current Phase\s*\n\n(.+?)(?:\n## |\Z)", document, re.MULTILINE | re.DOTALL)
    if match is None:
        raise AssertionError("CURRENT_PROGRAM.md 缺少可解析的 Current Phase 段落。")

    phase = None
    tranche = None
    for raw_line in match.group(1).splitlines():
        line = raw_line.strip()
        if not line.startswith("- "):
            continue
        if phase is None:
            phase_match = re.search(r"`([^`]+)`", line)
            if phase_match is not None:
                phase = phase_match.group(1)
                continue
        if "当前唯一活跃子线：" in line or "latest absorbed tranche 为" in line:
            tranche_matches = re.findall(r"`([^`]+)`", line)
            if tranche_matches:
                tranche = tranche_matches[-1]
                break

    if phase is None or tranche is None:
        raise AssertionError("CURRENT_PROGRAM.md 缺少可解析的 Current Phase 段落。")
    return phase, tranche


def extract_truth_sources(document: str) -> list[Path]:
    match = re.search(r"## Governing Truth Sources\s+(.+?)\n## ", document, re.MULTILINE | re.DOTALL)
    if match is None:
        raise AssertionError("CURRENT_PROGRAM.md 缺少 Governing Truth Sources 段落。")

    paths: list[Path] = []
    for raw_line in match.group(1).splitlines():
        line = raw_line.strip()
        if not line.startswith("- "):
            continue
        value = line[2:].strip().strip("`")
        paths.append(Path(value))
    return paths


def extract_section(document: str, title: str) -> list[str]:
    match = re.search(rf"## {re.escape(title)}\n\n(.+?)(?:\n## |\Z)", document, re.MULTILINE | re.DOTALL)
    if match is None:
        raise AssertionError(f"OPEN_ISSUES.md 缺少 {title} 段落。")
    return [line.strip() for line in match.group(1).splitlines() if line.strip().startswith("- ")]


def assert_labeled_path(document: str, label: str, path: Path) -> None:
    expected = f"- {label}：\n  - `{canonical_repo_path(path)}`"
    if expected not in document:
        raise AssertionError(f"段落 {label} 未指向期望路径: {path}")


def assert_labeled_text(document: str, label: str, snippet: str) -> None:
    match = re.search(rf"- {re.escape(label)}：\n  - (.+)", document)
    if match is None or snippet not in match.group(1):
        raise AssertionError(f"段落 {label} 未包含期望文本: {snippet}")


class ProgramControlSurfaceTest(unittest.TestCase):
    def test_current_program_truth_sources_exist(self) -> None:
        document = read_text(CURRENT_PROGRAM)
        for path in extract_truth_sources(document):
            with self.subTest(path=str(path)):
                self.assertTrue(path.exists(), f"truth source 不存在: {path}")

    def test_active_pointer_is_repeated_across_control_surfaces(self) -> None:
        current_program = read_text(CURRENT_PROGRAM)
        phase, tranche = extract_phase_pointer(current_program)

        for path in (
            TEAM_PROMPT,
            EXECUTION_PROMPT,
            OMX_BRIDGE,
            PRD,
            TEST_SPEC,
            IMPLEMENTATION,
            LATEST_STATUS,
            ITERATION_LOG,
            OPEN_ISSUES,
        ):
            with self.subTest(path=path.name):
                text = read_text(path)
                self.assertIn(phase, text, f"{path.name} 缺少当前 phase 指针")
                self.assertIn(tranche, text, f"{path.name} 缺少当前 tranche 指针")

    def test_required_control_surfaces_exist(self) -> None:
        for path in (
            CURRENT_PROGRAM,
            PROGRAM_ROUTING,
            TEAM_PROMPT,
            EXECUTION_PROMPT,
            PROGRAM_OPERATING_MODEL,
            PRD,
            TEST_SPEC,
            IMPLEMENTATION,
            REPORT_README,
            LATEST_STATUS,
            ITERATION_LOG,
            OPEN_ISSUES,
            TOP_LEVEL_DESIGN,
            RUNTIME_FIRST_PROGRAM,
            RUNTIME_BOUNDARY_MAP,
            R1A_ACTIVATION_PACKAGE,
            R1B_ACTIVATION_PACKAGE,
            R2A_ACTIVATION_PACKAGE,
            R3A_ACTIVATION_PACKAGE,
            R3A_MUTATION_CONTRACT,
            R4A_ACTIVATION_PACKAGE,
            R5A_ACTIVATION_PACKAGE,
            POST_R5A_HARDENING_SPEC,
            POST_R5A_WORKTREE_CONTROL_PLANE_ROOT_PACKAGE,
            POST_R5A_LOCAL_RUNTIME_VALIDATION_FAILED_SHAPE_PACKAGE,
            POST_R5A_FINAL_PACKAGE_MALFORMED_ARTIFACT_BUNDLE_PACKAGE,
            POST_R5A_HOSTED_CONTRACT_MALFORMED_FINAL_PACKAGE_PACKAGE,
            POST_R5A_HOSTED_CONTRACT_FINAL_PACKAGE_REQUIRED_SCALARS_PACKAGE,
            POST_R5A_HOSTED_CONTRACT_FINAL_PACKAGE_REQUIRED_NESTED_FIELDS_PACKAGE,
            POST_R5A_HOSTED_CONTRACT_FINAL_PACKAGE_CHECKPOINT_SEMANTICS_PACKAGE,
            POST_R5A_HOSTED_CONTRACT_FINAL_PACKAGE_FREEZE_MANIFEST_VALUE_TYPES_PACKAGE,
            POST_R5A_FINAL_PACKAGE_ARTIFACT_BUNDLE_REQUIRED_NESTED_FIELDS_PACKAGE,
            POST_R5A_FINAL_PACKAGE_ARTIFACT_BUNDLE_REQUIRED_SCALAR_VALUE_TYPES_PACKAGE,
            POST_R5A_FINAL_PACKAGE_ARTIFACT_BUNDLE_SUMMARY_COUNT_VALUE_TYPES_PACKAGE,
            POST_R5A_FINAL_PACKAGE_ARTIFACT_BUNDLE_ARTIFACT_LIST_VALUE_TYPES_PACKAGE,
            POST_R5A_FINAL_PACKAGE_ARTIFACT_BUNDLE_ARTIFACT_OBJECT_VALUE_TYPES_PACKAGE,
            POST_R5A_FINAL_PACKAGE_ARTIFACT_BUNDLE_ARTIFACT_OBJECT_PRIMARY_ID_FIELDS_PACKAGE,
            POST_R5A_FINAL_PACKAGE_ARTIFACT_BUNDLE_ARTIFACT_LIST_ELEMENT_SHAPES_PACKAGE,
            POST_R5A_FINAL_PACKAGE_ARTIFACT_BUNDLE_ARTIFACT_OBJECT_LINKAGE_ID_FIELDS_PACKAGE,
            POST_R5A_FINAL_PACKAGE_ARTIFACT_BUNDLE_ARTIFACT_OBJECT_REQUIRED_STRING_FIELDS_PACKAGE,
            POST_R5A_HOSTED_CONTRACT_FINAL_PACKAGE_LINEAGE_VALUE_TYPES_PACKAGE,
            P5A_ACTIVATION_PACKAGE,
            P5B_ACTIVATION_PACKAGE,
        ):
            with self.subTest(path=path.name):
                self.assertTrue(path.exists(), f"control surface 不存在: {path}")

    def test_execution_entry_and_test_spec_share_required_commands(self) -> None:
        execution_prompt_text = read_text(EXECUTION_PROMPT)
        test_spec_text = read_text(TEST_SPEC)
        latest_status_text = read_text(LATEST_STATUS)

        for snippet in REQUIRED_COMMAND_SNIPPETS:
            with self.subTest(command=snippet):
                self.assertIn(snippet, execution_prompt_text)
                self.assertIn(snippet, test_spec_text)

        self.assertIn("Verification Snapshot", latest_status_text)
        for keyword in ("validate-workspace", "summarize-workspace", "next-step", "critique-summary", "stage-route-report"):
            with self.subTest(keyword=keyword):
                self.assertIn(keyword, latest_status_text)

    def test_formal_entry_and_durability_current_truth_are_frozen(self) -> None:
        formal_entry_text = read_text(FORMAL_ENTRY_MATRIX)
        durability_text = read_text(DURABILITY_MODEL)

        for path in (
            FORMAL_ENTRY_MATRIX,
            DURABILITY_MODEL,
            P2B_CURRENT_TRUTH,
            P2C_CURRENT_TRUTH,
            P3A_CURRENT_TRUTH,
            P3B_CURRENT_TRUTH,
            P3C_CURRENT_TRUTH,
            P4A_CURRENT_TRUTH,
            P4B_CURRENT_TRUTH,
        ):
            with self.subTest(path=path.name):
                self.assertTrue(path.exists(), f"current truth doc 不存在: {path}")

        for snippet in (
            "CLI",
            "developer control-plane entry",
            "recovery / resume entry",
            "MCP",
            "controller",
            "not-yet-supported",
        ):
            with self.subTest(snippet=snippet):
                self.assertIn(snippet, formal_entry_text)

        for snippet in (
            "repo-tracked review surfaces",
            "local durable handoff surfaces",
            "grant_run_id",
            "workspace_id",
            "draft_id",
            "program_id",
        ):
            with self.subTest(snippet=snippet):
                self.assertIn(snippet, durability_text)

    def test_post_r5a_hardening_spec_and_public_walkthrough_are_aligned(self) -> None:
        spec_text = read_text(POST_R5A_HARDENING_SPEC)
        for snippet in (
            "execute-revision-pass",
            "validate-workspace",
            "stage-route-report",
            "build-final-package",
            "build-hosted-contract-bundle",
        ):
            with self.subTest(spec_snippet=snippet):
                self.assertIn(snippet, spec_text)

        for path in (README_EN, README_ZH):
            text = read_text(path)
            for snippet in POST_R5A_WALKTHROUGH_SNIPPETS:
                with self.subTest(path=path.name, snippet=snippet):
                    self.assertIn(snippet, text)

        spec_path_text = f"./specs/{POST_R5A_HARDENING_SPEC.name}"
        for path in (DOCS_README_EN, DOCS_README_ZH):
            with self.subTest(path=path.name, spec_path=spec_path_text):
                self.assertIn(spec_path_text, read_text(path))

        formal_entry_text = read_text(FORMAL_ENTRY_MATRIX)
        durability_text = read_text(DURABILITY_MODEL)
        for text, path in ((formal_entry_text, FORMAL_ENTRY_MATRIX), (durability_text, DURABILITY_MODEL)):
            for snippet in ("execute-revision-pass", "build-final-package", "build-hosted-contract-bundle"):
                with self.subTest(path=path.name, landed_snippet=snippet):
                    self.assertIn(snippet, text)
            with self.subTest(path=path.name, outdated_not_landed=False):
                self.assertNotIn("execute-revision-pass` 仍未 landed", text)
            with self.subTest(path=path.name, outdated_activation_only=False):
                self.assertNotIn("尚未把 revision executor 误写成 landed runtime surface", text)

        current_program_text = read_text(CURRENT_PROGRAM)
        execution_prompt_text = read_text(EXECUTION_PROMPT)
        team_prompt_text = read_text(TEAM_PROMPT)
        for path in (
            FORMAL_ENTRY_MATRIX,
            DURABILITY_MODEL,
            P2B_CURRENT_TRUTH,
            P2C_CURRENT_TRUTH,
            P3A_CURRENT_TRUTH,
            P3B_CURRENT_TRUTH,
            P3C_CURRENT_TRUTH,
            P4A_CURRENT_TRUTH,
            P4B_CURRENT_TRUTH,
        ):
            path_text = canonical_repo_path(path)
            with self.subTest(current_program_path=path.name):
                self.assertIn(path_text, current_program_text)
            with self.subTest(execution_prompt_path=path.name):
                self.assertIn(path_text, execution_prompt_text)
            with self.subTest(team_prompt_path=path.name):
                self.assertIn(path_text, team_prompt_text)

    def test_report_surface_documents_required_files_and_sync_rule(self) -> None:
        report_text = read_text(REPORT_README)
        for required_name in ("LATEST_STATUS.md", "ITERATION_LOG.md", "OPEN_ISSUES.md"):
            with self.subTest(file=required_name):
                self.assertIn(required_name, report_text)
                self.assertTrue((REPORT_DIR / required_name).exists())

        self.assertIn("current pointer", report_text.lower())
        self.assertIn("promotion", report_text.lower())

    def test_open_issues_blockers_section_only_contains_active_blockers(self) -> None:
        blockers = extract_section(read_text(OPEN_ISSUES), "blockers")
        self.assertTrue(blockers, "OPEN_ISSUES.md 的 blockers 段落不能为空。")

        if len(blockers) == 1 and "无 active blocker" in blockers[0]:
            return

        rejected_markers = ("无硬 blocker", "无新增 blocker", "已修复", "已将")
        for line in blockers:
            with self.subTest(line=line):
                self.assertFalse(any(marker in line for marker in rejected_markers), "blockers 段落只能保留当前 active blocker。")
                self.assertTrue(
                    any(keyword in line for keyword in ("P3.B", "P3.C", "promotion", "tranche", "phase boundary", "rollback", "presubmission")),
                    "blockers 段落必须只记录与当前 pointer 或 promotion 直接相关的 active blocker。",
                )

    def test_future_tranche_map_and_same_phase_autopromotion_are_frozen(self) -> None:
        current_program_text = read_text(CURRENT_PROGRAM)
        prd_text = read_text(PRD)
        implementation_text = read_text(IMPLEMENTATION)
        bridge_text = read_text(OMX_BRIDGE)

        for snippet in FUTURE_TRANCHE_SNIPPETS:
            for path, text in (
                (CURRENT_PROGRAM, current_program_text),
                (PRD, prd_text),
                (IMPLEMENTATION, implementation_text),
                (OMX_BRIDGE, bridge_text),
            ):
                with self.subTest(path=path.name, snippet=snippet):
                    self.assertIn(snippet, text)

        for path in (CURRENT_PROGRAM, PROGRAM_OPERATING_MODEL, PRD, TEST_SPEC, IMPLEMENTATION, OMX_BRIDGE):
            with self.subTest(path=path.name):
                self.assertIn("same-phase auto-promotion", read_text(path))

    def test_prefrozen_p5_activation_packages_have_required_sections(self) -> None:
        for path, unique_snippets in (
            (P5A_ACTIVATION_PACKAGE, P5A_ACTIVATION_SNIPPETS),
            (P5B_ACTIVATION_PACKAGE, P5B_ACTIVATION_SNIPPETS),
        ):
            text = read_text(path)
            for snippet in P5_ACTIVATION_SECTION_SNIPPETS:
                with self.subTest(path=path.name, snippet=snippet):
                    self.assertIn(snippet, text)
            for snippet in unique_snippets:
                with self.subTest(path=path.name, unique_snippet=snippet):
                    self.assertIn(snippet, text)

    def test_prefrozen_p5_activation_package_paths_are_wired_into_control_surfaces(self) -> None:
        for package in (P5A_ACTIVATION_PACKAGE, P5B_ACTIVATION_PACKAGE):
            package_path = canonical_repo_path(package)
            for path in (
                CURRENT_PROGRAM,
                PROGRAM_ROUTING,
                TEAM_PROMPT,
                EXECUTION_PROMPT,
                OMX_BRIDGE,
                PRD,
                TEST_SPEC,
                IMPLEMENTATION,
                LATEST_STATUS,
            ):
                with self.subTest(package=package.name, path=path.name):
                    self.assertIn(package_path, read_text(path))

    def test_runtime_first_program_is_repo_tracked_and_wired(self) -> None:
        runtime_program_path = canonical_repo_path(RUNTIME_FIRST_PROGRAM)
        runtime_program_text = read_text(RUNTIME_FIRST_PROGRAM)

        for snippet in RUNTIME_FIRST_SNIPPETS:
            with self.subTest(snippet=snippet):
                self.assertIn(snippet, runtime_program_text)

        for path in (PROJECT_TRUTH, TOP_LEVEL_DESIGN, OMX_BRIDGE, CURRENT_PROGRAM):
            with self.subTest(path=path.name):
                self.assertIn(runtime_program_path, read_text(path))

        combined = "\n".join(read_text(path) for path in (PROJECT_TRUTH, TOP_LEVEL_DESIGN, OMX_BRIDGE))
        self.assertIn("runtime-first", combined)
        self.assertIn("CLI-first + host-agent", combined)

    def test_runtime_boundary_map_is_repo_tracked_and_wired(self) -> None:
        boundary_map_path = canonical_repo_path(RUNTIME_BOUNDARY_MAP)
        boundary_map_text = read_text(RUNTIME_BOUNDARY_MAP)

        for snippet in RUNTIME_BOUNDARY_MAP_SNIPPETS:
            with self.subTest(snippet=snippet):
                self.assertIn(snippet, boundary_map_text)

        for path in (PROJECT_TRUTH, TOP_LEVEL_DESIGN, RUNTIME_FIRST_PROGRAM, OMX_BRIDGE):
            with self.subTest(path=path.name):
                self.assertIn(boundary_map_path, read_text(path))

    def test_runtime_boundary_map_is_wired_into_active_control_surfaces(self) -> None:
        boundary_map_path = canonical_repo_path(RUNTIME_BOUNDARY_MAP)
        for path in RUNTIME_BOUNDARY_CONTROL_SURFACES:
            with self.subTest(path=path.name):
                self.assertIn(boundary_map_path, read_text(path))

    def test_post_r5a_walkthrough_truth_is_repo_tracked_and_wired(self) -> None:
        truth_path = canonical_repo_path(POST_R5A_WALKTHROUGH_CURRENT_TRUTH)
        truth_text = read_text(POST_R5A_WALKTHROUGH_CURRENT_TRUTH)

        for snippet in (
            "execute-revision-pass",
            "validate-workspace --input \"$TMPDIR/r3a-p2c-revised.json\"",
            "stage-route-report --input \"$TMPDIR/r3a-p2c-revised.json\"",
            "build-final-package",
            "build-hosted-contract-bundle",
            "grant_run_id",
            "workspace_id",
            "draft_id",
            "program_id",
            "verification_checkpoint",
            "checkpoint_status",
            "CLI",
            "MCP",
            "controller",
        ):
            with self.subTest(snippet=snippet):
                self.assertIn(snippet, truth_text)

        for path in (
            README_EN,
            README_ZH,
            CURRENT_PROGRAM,
            PROGRAM_ROUTING,
            PRD,
            TEST_SPEC,
            IMPLEMENTATION,
            LATEST_STATUS,
            OPEN_ISSUES,
        ):
            with self.subTest(path=path.name):
                self.assertIn(truth_path, read_text(path))

    def test_post_r5a_hardening_truth_does_not_reopen_landed_p3b_validator_delta(self) -> None:
        truth_text = read_text(POST_R5A_HARDENING_SPEC)
        self.assertNotIn("当前会被上述 surfaces 拒绝", truth_text)
        self.assertNotIn("re-review 批注引用的 RevisionPlan 必须与当前激活草稿版本一致。", truth_text)
        self.assertIn("当前 absorbed baseline 已能通过上述 surfaces", truth_text)

    def test_post_r5a_stage_route_report_checkpoint_status_package_is_repo_tracked_and_wired(self) -> None:
        package_text = read_text(POST_R5A_STAGE_ROUTE_REPORT_CHECKPOINT_STATUS_PACKAGE)
        for snippet in (
            "stage-route-report",
            "checkpoint_status",
            "verification_checkpoint.checkpoint_status",
            "唯一 canonical checkpoint aggregation object",
        ):
            with self.subTest(snippet=snippet):
                self.assertIn(snippet, package_text)

        package_path = canonical_repo_path(POST_R5A_STAGE_ROUTE_REPORT_CHECKPOINT_STATUS_PACKAGE)
        for path in (PRD, TEST_SPEC, IMPLEMENTATION):
            with self.subTest(path=path.name):
                self.assertIn(package_path, read_text(path))

    def test_post_r5a_worktree_control_plane_root_package_is_repo_tracked_and_wired(self) -> None:
        package_text = read_text(POST_R5A_WORKTREE_CONTROL_PLANE_ROOT_PACKAGE)
        for snippet in (
            "build-hosted-contract-bundle",
            "CURRENT_PROGRAM.md",
            "git worktree list --porcelain",
            "branch refs/heads/main",
            "program_id",
            "fail-closed",
        ):
            with self.subTest(snippet=snippet):
                self.assertIn(snippet, package_text)

        package_path = canonical_repo_path(POST_R5A_WORKTREE_CONTROL_PLANE_ROOT_PACKAGE)
        for path in (
            CURRENT_PROGRAM,
            PROGRAM_ROUTING,
            PRD,
            TEST_SPEC,
            IMPLEMENTATION,
            LATEST_STATUS,
            ITERATION_LOG,
            OPEN_ISSUES,
        ):
            with self.subTest(path=path.name):
                self.assertIn(package_path, read_text(path))

    def test_post_r5a_local_runtime_validation_failed_shape_package_is_repo_tracked_and_wired(self) -> None:
        package_text = read_text(POST_R5A_LOCAL_RUNTIME_VALIDATION_FAILED_SHAPE_PACKAGE)
        for snippet in (
            "run-local / resume-local",
            "validation_failed",
            "verification_checkpoint",
            "checkpoint_status = null",
            "stage_action_envelope = null",
            "stage-route-report",
        ):
            with self.subTest(snippet=snippet):
                self.assertIn(snippet, package_text)

        package_path = canonical_repo_path(POST_R5A_LOCAL_RUNTIME_VALIDATION_FAILED_SHAPE_PACKAGE)
        for path in (
            CURRENT_PROGRAM,
            PROGRAM_ROUTING,
            PRD,
            TEST_SPEC,
            IMPLEMENTATION,
            LATEST_STATUS,
            ITERATION_LOG,
            OPEN_ISSUES,
        ):
            with self.subTest(path=path.name):
                self.assertIn(package_path, read_text(path))

    def test_post_r5a_final_package_malformed_artifact_bundle_package_is_repo_tracked_and_wired(self) -> None:
        package_text = read_text(POST_R5A_FINAL_PACKAGE_MALFORMED_ARTIFACT_BUNDLE_PACKAGE)
        for snippet in (
            "build-final-package",
            "manifest",
            "artifacts",
            "WorkspaceStateError",
            "fail-open",
            "R2.A -> R4.A",
        ):
            with self.subTest(snippet=snippet):
                self.assertIn(snippet, package_text)

        package_path = canonical_repo_path(POST_R5A_FINAL_PACKAGE_MALFORMED_ARTIFACT_BUNDLE_PACKAGE)
        for path in (
            CURRENT_PROGRAM,
            PROGRAM_ROUTING,
            PRD,
            TEST_SPEC,
            IMPLEMENTATION,
            LATEST_STATUS,
            ITERATION_LOG,
            OPEN_ISSUES,
        ):
            with self.subTest(path=path.name):
                self.assertIn(package_path, read_text(path))

    def test_post_r5a_hosted_contract_bundle_malformed_final_package_package_is_repo_tracked_and_wired(self) -> None:
        package_text = read_text(POST_R5A_HOSTED_CONTRACT_MALFORMED_FINAL_PACKAGE_PACKAGE)
        for snippet in (
            "build-hosted-contract-bundle",
            "freeze_manifest",
            "checkpoint_summary",
            "lineage",
            "WorkspaceStateError",
            "fail-open",
        ):
            with self.subTest(snippet=snippet):
                self.assertIn(snippet, package_text)

        package_path = canonical_repo_path(POST_R5A_HOSTED_CONTRACT_MALFORMED_FINAL_PACKAGE_PACKAGE)
        for path in (
            CURRENT_PROGRAM,
            PROGRAM_ROUTING,
            PRD,
            TEST_SPEC,
            IMPLEMENTATION,
            LATEST_STATUS,
            ITERATION_LOG,
            OPEN_ISSUES,
        ):
            with self.subTest(path=path.name):
                self.assertIn(package_path, read_text(path))

    def test_post_r5a_hosted_contract_bundle_required_scalar_fields_package_is_repo_tracked_and_wired(self) -> None:
        package_text = read_text(POST_R5A_HOSTED_CONTRACT_FINAL_PACKAGE_REQUIRED_SCALARS_PACKAGE)
        for snippet in (
            "build-hosted-contract-bundle",
            "package_version",
            "lifecycle_stage",
            "grant_run_id",
            "workspace_id",
            "draft_id",
            "fail-open",
        ):
            with self.subTest(snippet=snippet):
                self.assertIn(snippet, package_text)

        package_path = canonical_repo_path(POST_R5A_HOSTED_CONTRACT_FINAL_PACKAGE_REQUIRED_SCALARS_PACKAGE)
        for path in (
            CURRENT_PROGRAM,
            PROGRAM_ROUTING,
            PRD,
            TEST_SPEC,
            IMPLEMENTATION,
            LATEST_STATUS,
            ITERATION_LOG,
            OPEN_ISSUES,
        ):
            with self.subTest(path=path.name):
                self.assertIn(package_path, read_text(path))

    def test_post_r5a_hosted_contract_bundle_required_nested_fields_package_is_repo_tracked_and_wired(self) -> None:
        package_text = read_text(POST_R5A_HOSTED_CONTRACT_FINAL_PACKAGE_REQUIRED_NESTED_FIELDS_PACKAGE)
        for snippet in (
            "build-hosted-contract-bundle",
            "freeze_manifest",
            "checkpoint_summary",
            "lineage",
            "draft_status",
            "verification_checkpoint",
            "revision_plan_id",
        ):
            with self.subTest(snippet=snippet):
                self.assertIn(snippet, package_text)

        package_path = canonical_repo_path(POST_R5A_HOSTED_CONTRACT_FINAL_PACKAGE_REQUIRED_NESTED_FIELDS_PACKAGE)
        for path in (
            CURRENT_PROGRAM,
            PROGRAM_ROUTING,
            PRD,
            TEST_SPEC,
            IMPLEMENTATION,
            LATEST_STATUS,
            ITERATION_LOG,
            OPEN_ISSUES,
        ):
            with self.subTest(path=path.name):
                self.assertIn(package_path, read_text(path))

    def test_post_r5a_hosted_contract_bundle_checkpoint_semantics_package_is_repo_tracked_and_wired(self) -> None:
        package_text = read_text(POST_R5A_HOSTED_CONTRACT_FINAL_PACKAGE_CHECKPOINT_SEMANTICS_PACKAGE)
        for snippet in (
            "build-hosted-contract-bundle",
            "freeze_manifest.draft_status",
            "freeze_manifest.checkpoint_status",
            "checkpoint_summary.checkpoint_status",
            "verification_checkpoint.checkpoint_status",
            "checkpoint_status 不一致",
        ):
            with self.subTest(snippet=snippet):
                self.assertIn(snippet, package_text)

        package_path = canonical_repo_path(POST_R5A_HOSTED_CONTRACT_FINAL_PACKAGE_CHECKPOINT_SEMANTICS_PACKAGE)
        for path in (
            CURRENT_PROGRAM,
            PROGRAM_ROUTING,
            PRD,
            TEST_SPEC,
            IMPLEMENTATION,
            LATEST_STATUS,
            ITERATION_LOG,
            OPEN_ISSUES,
        ):
            with self.subTest(path=path.name):
                self.assertIn(package_path, read_text(path))

    def test_post_r5a_hosted_contract_bundle_lineage_value_types_package_is_repo_tracked_and_wired(self) -> None:
        package_text = read_text(POST_R5A_HOSTED_CONTRACT_FINAL_PACKAGE_LINEAGE_VALUE_TYPES_PACKAGE)
        for snippet in (
            "build-hosted-contract-bundle",
            "lineage.frozen_question_id",
            "lineage.selected_direction_id",
            "lineage.selected_question_id",
            "lineage.active_fit_mapping_id",
            "lineage.draft_id",
            "lineage.revision_plan_id",
        ):
            with self.subTest(snippet=snippet):
                self.assertIn(snippet, package_text)

        package_path = canonical_repo_path(POST_R5A_HOSTED_CONTRACT_FINAL_PACKAGE_LINEAGE_VALUE_TYPES_PACKAGE)
        for path in (
            CURRENT_PROGRAM,
            PROGRAM_ROUTING,
            PRD,
            TEST_SPEC,
            IMPLEMENTATION,
            LATEST_STATUS,
            ITERATION_LOG,
            OPEN_ISSUES,
        ):
            with self.subTest(path=path.name):
                self.assertIn(package_path, read_text(path))

    def test_post_r5a_hosted_contract_bundle_freeze_manifest_value_types_package_is_repo_tracked_and_wired(self) -> None:
        package_text = read_text(POST_R5A_HOSTED_CONTRACT_FINAL_PACKAGE_FREEZE_MANIFEST_VALUE_TYPES_PACKAGE)
        for snippet in (
            "build-hosted-contract-bundle",
            "freeze_manifest.draft_version_label",
            "freeze_manifest.active_revision_plan_id",
            "freeze_manifest.critique_id",
            "freeze_manifest.presubmission_frozen",
        ):
            with self.subTest(snippet=snippet):
                self.assertIn(snippet, package_text)

        package_path = canonical_repo_path(POST_R5A_HOSTED_CONTRACT_FINAL_PACKAGE_FREEZE_MANIFEST_VALUE_TYPES_PACKAGE)
        for path in (
            CURRENT_PROGRAM,
            PROGRAM_ROUTING,
            PRD,
            TEST_SPEC,
            IMPLEMENTATION,
            LATEST_STATUS,
            ITERATION_LOG,
            OPEN_ISSUES,
        ):
            with self.subTest(path=path.name):
                self.assertIn(package_path, read_text(path))

    def test_post_r5a_final_package_artifact_bundle_required_nested_fields_package_is_repo_tracked_and_wired(self) -> None:
        package_text = read_text(POST_R5A_FINAL_PACKAGE_ARTIFACT_BUNDLE_REQUIRED_NESTED_FIELDS_PACKAGE)
        for snippet in (
            "build-final-package",
            "selection.selected_direction_id",
            "manifest.direction_id",
            "lineage.frozen_question_id",
            "bundle_summary.outline_count",
            "artifacts.selected_direction",
        ):
            with self.subTest(snippet=snippet):
                self.assertIn(snippet, package_text)

        package_path = canonical_repo_path(POST_R5A_FINAL_PACKAGE_ARTIFACT_BUNDLE_REQUIRED_NESTED_FIELDS_PACKAGE)
        for path in (
            CURRENT_PROGRAM,
            PROGRAM_ROUTING,
            PRD,
            TEST_SPEC,
            IMPLEMENTATION,
            LATEST_STATUS,
            ITERATION_LOG,
            OPEN_ISSUES,
        ):
            with self.subTest(path=path.name):
                self.assertIn(package_path, read_text(path))

    def test_post_r5a_final_package_artifact_bundle_required_scalar_value_types_package_is_repo_tracked_and_wired(self) -> None:
        package_text = read_text(POST_R5A_FINAL_PACKAGE_ARTIFACT_BUNDLE_REQUIRED_SCALAR_VALUE_TYPES_PACKAGE)
        for snippet in (
            "build-final-package",
            'selection.selected_direction_id=""',
            "manifest.draft_version_label=None",
            "manifest.draft_status={}",
            "lineage.argument_chain_id={}",
            "以上字段都必须是**非空字符串**",
        ):
            with self.subTest(snippet=snippet):
                self.assertIn(snippet, package_text)

        package_path = canonical_repo_path(POST_R5A_FINAL_PACKAGE_ARTIFACT_BUNDLE_REQUIRED_SCALAR_VALUE_TYPES_PACKAGE)
        for path in (
            CURRENT_PROGRAM,
            PROGRAM_ROUTING,
            PRD,
            TEST_SPEC,
            IMPLEMENTATION,
            LATEST_STATUS,
            ITERATION_LOG,
            OPEN_ISSUES,
        ):
            with self.subTest(path=path.name):
                self.assertIn(package_path, read_text(path))

    def test_post_r5a_final_package_artifact_bundle_summary_count_value_types_package_is_repo_tracked_and_wired(self) -> None:
        package_text = read_text(POST_R5A_FINAL_PACKAGE_ARTIFACT_BUNDLE_SUMMARY_COUNT_VALUE_TYPES_PACKAGE)
        for snippet in (
            "build-final-package",
            'bundle_summary.outline_count="2"',
            "bundle_summary.outline_count=-1",
            "bundle_summary.outline_count=False",
            "bundle_summary.section_count=None",
            "以上字段都必须是**非负整数**",
        ):
            with self.subTest(snippet=snippet):
                self.assertIn(snippet, package_text)

        package_path = canonical_repo_path(POST_R5A_FINAL_PACKAGE_ARTIFACT_BUNDLE_SUMMARY_COUNT_VALUE_TYPES_PACKAGE)
        for path in (
            CURRENT_PROGRAM,
            PROGRAM_ROUTING,
            PRD,
            TEST_SPEC,
            IMPLEMENTATION,
            LATEST_STATUS,
            ITERATION_LOG,
            OPEN_ISSUES,
        ):
            with self.subTest(path=path.name):
                self.assertIn(package_path, read_text(path))

    def test_post_r5a_final_package_artifact_bundle_artifact_list_value_types_package_is_repo_tracked_and_wired(self) -> None:
        package_text = read_text(POST_R5A_FINAL_PACKAGE_ARTIFACT_BUNDLE_ARTIFACT_LIST_VALUE_TYPES_PACKAGE)
        for snippet in (
            "build-final-package",
            "artifacts.draft_outline={}",
            'artifacts.draft_outline="oops"',
            "artifacts.draft_sections={}",
            "artifacts.draft_sections=None",
            "以上字段都必须是 `list`",
        ):
            with self.subTest(snippet=snippet):
                self.assertIn(snippet, package_text)

        package_path = canonical_repo_path(POST_R5A_FINAL_PACKAGE_ARTIFACT_BUNDLE_ARTIFACT_LIST_VALUE_TYPES_PACKAGE)
        for path in (
            CURRENT_PROGRAM,
            PROGRAM_ROUTING,
            PRD,
            TEST_SPEC,
            IMPLEMENTATION,
            LATEST_STATUS,
            ITERATION_LOG,
            OPEN_ISSUES,
        ):
            with self.subTest(path=path.name):
                self.assertIn(package_path, read_text(path))


    def test_post_r5a_final_package_artifact_bundle_artifact_object_value_types_package_is_repo_tracked_and_wired(self) -> None:
        package_text = read_text(POST_R5A_FINAL_PACKAGE_ARTIFACT_BUNDLE_ARTIFACT_OBJECT_VALUE_TYPES_PACKAGE)
        for snippet in (
            "build-final-package",
            "artifacts.selected_direction=[]",
            'artifacts.selected_question="oops"',
            "artifacts.argument_chain=None",
            "artifacts.fit_mapping=[]",
            "以上字段都必须是 `dict`",
        ):
            with self.subTest(snippet=snippet):
                self.assertIn(snippet, package_text)

        package_path = canonical_repo_path(POST_R5A_FINAL_PACKAGE_ARTIFACT_BUNDLE_ARTIFACT_OBJECT_VALUE_TYPES_PACKAGE)
        for path in (
            CURRENT_PROGRAM,
            PROGRAM_ROUTING,
            PRD,
            TEST_SPEC,
            IMPLEMENTATION,
            LATEST_STATUS,
            ITERATION_LOG,
            OPEN_ISSUES,
        ):
            with self.subTest(path=path.name):
                self.assertIn(package_path, read_text(path))


    def test_post_r5a_final_package_artifact_bundle_artifact_object_primary_id_fields_package_is_repo_tracked_and_wired(self) -> None:
        package_text = read_text(POST_R5A_FINAL_PACKAGE_ARTIFACT_BUNDLE_ARTIFACT_OBJECT_PRIMARY_ID_FIELDS_PACKAGE)
        for snippet in (
            "build-final-package",
            "artifacts.selected_direction.direction_id=None",
            'artifacts.selected_question.question_id=""',
            "artifacts.argument_chain.argument_chain_id=None",
            'artifacts.fit_mapping.fit_mapping_id=""',
            "以上字段都必须是非空字符串",
        ):
            with self.subTest(snippet=snippet):
                self.assertIn(snippet, package_text)

        package_path = canonical_repo_path(POST_R5A_FINAL_PACKAGE_ARTIFACT_BUNDLE_ARTIFACT_OBJECT_PRIMARY_ID_FIELDS_PACKAGE)
        for path in (
            CURRENT_PROGRAM,
            PROGRAM_ROUTING,
            PRD,
            TEST_SPEC,
            IMPLEMENTATION,
            LATEST_STATUS,
            ITERATION_LOG,
            OPEN_ISSUES,
        ):
            with self.subTest(path=path.name):
                self.assertIn(package_path, read_text(path))

    def test_post_r5a_final_package_artifact_bundle_artifacts_list_element_shapes_package_is_repo_tracked_and_wired(self) -> None:
        package_text = read_text(POST_R5A_FINAL_PACKAGE_ARTIFACT_BUNDLE_ARTIFACT_LIST_ELEMENT_SHAPES_PACKAGE)
        for snippet in (
            "build-final-package",
            "artifacts.draft_outline[0]={}",
            "artifacts.draft_sections[0]={}",
            "artifacts.draft_outline[0].section_key",
            "artifacts.draft_sections[0].text",
            "每个 list element 都必须是 object，并保留当前 required fields",
        ):
            with self.subTest(snippet=snippet):
                self.assertIn(snippet, package_text)

        package_path = canonical_repo_path(POST_R5A_FINAL_PACKAGE_ARTIFACT_BUNDLE_ARTIFACT_LIST_ELEMENT_SHAPES_PACKAGE)
        for path in (
            CURRENT_PROGRAM,
            PROGRAM_ROUTING,
            PRD,
            TEST_SPEC,
            IMPLEMENTATION,
            LATEST_STATUS,
            ITERATION_LOG,
            OPEN_ISSUES,
        ):
            with self.subTest(path=path.name):
                self.assertIn(package_path, read_text(path))

    def test_post_r5a_final_package_artifact_bundle_artifact_object_linkage_id_fields_package_is_repo_tracked_and_wired(self) -> None:
        package_text = read_text(POST_R5A_FINAL_PACKAGE_ARTIFACT_BUNDLE_ARTIFACT_OBJECT_LINKAGE_ID_FIELDS_PACKAGE)
        for snippet in (
            "build-final-package",
            "artifacts.selected_question.parent_direction_id=None",
            'artifacts.argument_chain.scientific_question_id=""',
            "artifacts.fit_mapping.scientific_question_id=None",
            'artifacts.fit_mapping.argument_chain_id=""',
            "以上字段都必须是非空字符串",
        ):
            with self.subTest(snippet=snippet):
                self.assertIn(snippet, package_text)

        package_path = canonical_repo_path(POST_R5A_FINAL_PACKAGE_ARTIFACT_BUNDLE_ARTIFACT_OBJECT_LINKAGE_ID_FIELDS_PACKAGE)
        for path in (
            CURRENT_PROGRAM,
            PROGRAM_ROUTING,
            PRD,
            TEST_SPEC,
            IMPLEMENTATION,
            LATEST_STATUS,
            ITERATION_LOG,
            OPEN_ISSUES,
        ):
            with self.subTest(path=path.name):
                self.assertIn(package_path, read_text(path))

    def test_post_r5a_final_package_artifact_bundle_artifact_object_required_string_fields_package_is_repo_tracked_and_wired(self) -> None:
        package_text = read_text(POST_R5A_FINAL_PACKAGE_ARTIFACT_BUNDLE_ARTIFACT_OBJECT_REQUIRED_STRING_FIELDS_PACKAGE)
        for snippet in (
            "build-final-package",
            "artifacts.selected_direction.title=None",
            'artifacts.selected_question.core_question=""',
            "artifacts.argument_chain.necessity_claim=None",
            'artifacts.fit_mapping.applicant_fit_summary=""',
            "以上字段都必须是非空字符串",
        ):
            with self.subTest(snippet=snippet):
                self.assertIn(snippet, package_text)

        package_path = canonical_repo_path(POST_R5A_FINAL_PACKAGE_ARTIFACT_BUNDLE_ARTIFACT_OBJECT_REQUIRED_STRING_FIELDS_PACKAGE)
        for path in (
            CURRENT_PROGRAM,
            PROGRAM_ROUTING,
            PRD,
            TEST_SPEC,
            IMPLEMENTATION,
            LATEST_STATUS,
            ITERATION_LOG,
            OPEN_ISSUES,
        ):
            with self.subTest(path=path.name):
                self.assertIn(package_path, read_text(path))

    def test_r1a_activation_package_is_wired_into_active_control_surfaces(self) -> None:
        package_path = canonical_repo_path(R1A_ACTIVATION_PACKAGE)
        self.assertTrue(R1A_ACTIVATION_PACKAGE.exists(), f"R1.A activation package 不存在: {R1A_ACTIVATION_PACKAGE}")

        for path in (
            CURRENT_PROGRAM,
            PROGRAM_ROUTING,
            TEAM_PROMPT,
            EXECUTION_PROMPT,
            PRD,
            TEST_SPEC,
            IMPLEMENTATION,
            LATEST_STATUS,
        ):
            with self.subTest(path=path.name):
                self.assertIn(package_path, read_text(path))

    def test_r1b_activation_package_is_wired_into_active_control_surfaces(self) -> None:
        package_path = canonical_repo_path(R1B_ACTIVATION_PACKAGE)
        self.assertTrue(R1B_ACTIVATION_PACKAGE.exists(), f"R1.B activation package 不存在: {R1B_ACTIVATION_PACKAGE}")

        for path in (
            CURRENT_PROGRAM,
            PROGRAM_ROUTING,
            TEAM_PROMPT,
            EXECUTION_PROMPT,
            PRD,
            TEST_SPEC,
            IMPLEMENTATION,
            LATEST_STATUS,
        ):
            with self.subTest(path=path.name):
                self.assertIn(package_path, read_text(path))

    def test_r2a_activation_package_is_wired_into_active_control_surfaces(self) -> None:
        package_path = canonical_repo_path(R2A_ACTIVATION_PACKAGE)
        self.assertTrue(R2A_ACTIVATION_PACKAGE.exists(), f"R2.A activation package 不存在: {R2A_ACTIVATION_PACKAGE}")

        for path in (
            CURRENT_PROGRAM,
            PROGRAM_ROUTING,
            TEAM_PROMPT,
            EXECUTION_PROMPT,
            PRD,
            TEST_SPEC,
            IMPLEMENTATION,
            LATEST_STATUS,
            ITERATION_LOG,
            OPEN_ISSUES,
        ):
            with self.subTest(path=path.name):
                self.assertIn(package_path, read_text(path))

    def test_r3a_activation_package_is_wired_into_active_control_surfaces(self) -> None:
        package_path = canonical_repo_path(R3A_ACTIVATION_PACKAGE)
        self.assertTrue(R3A_ACTIVATION_PACKAGE.exists(), f"R3.A activation package 不存在: {R3A_ACTIVATION_PACKAGE}")

        for path in (
            CURRENT_PROGRAM,
            PROGRAM_ROUTING,
            TEAM_PROMPT,
            EXECUTION_PROMPT,
            PRD,
            TEST_SPEC,
            IMPLEMENTATION,
            LATEST_STATUS,
            ITERATION_LOG,
            OPEN_ISSUES,
        ):
            with self.subTest(path=path.name):
                self.assertIn(package_path, read_text(path))

    def test_latest_absorbed_and_current_active_runtime_slice_paths_are_aligned(self) -> None:
        for path in (PROGRAM_ROUTING, LATEST_STATUS):
            text = read_text(path)
            with self.subTest(path=path.name, label="latest absorbed runtime slice activation package"):
                assert_labeled_path(
                    text,
                    "latest absorbed runtime slice activation package",
                    LATEST_ABSORBED_RUNTIME_SLICE_ACTIVATION_PACKAGE,
                )
            with self.subTest(path=path.name, label="current active runtime slice activation package"):
                assert_labeled_path(
                    text,
                    "current active runtime slice activation package",
                    CURRENT_ACTIVE_RUNTIME_SLICE_ACTIVATION_PACKAGE,
                )

    def test_r1a_activation_package_freezes_local_main_loop_contract(self) -> None:
        text = read_text(R1A_ACTIVATION_PACKAGE)
        for snippet in R1A_ACTIVATION_SNIPPETS:
            with self.subTest(snippet=snippet):
                self.assertIn(snippet, text)

    def test_r1b_activation_package_freezes_stage_action_envelope_contract(self) -> None:
        text = read_text(R1B_ACTIVATION_PACKAGE)
        for snippet in R1B_ACTIVATION_SNIPPETS:
            with self.subTest(snippet=snippet):
                self.assertIn(snippet, text)

    def test_r2a_activation_package_freezes_artifact_bundle_contract(self) -> None:
        text = read_text(R2A_ACTIVATION_PACKAGE)
        for snippet in R2A_ACTIVATION_SNIPPETS:
            with self.subTest(snippet=snippet):
                self.assertIn(snippet, text)

    def test_r3a_activation_package_freezes_revision_executor_contract(self) -> None:
        text = read_text(R3A_ACTIVATION_PACKAGE)
        for snippet in R3A_ACTIVATION_SNIPPETS:
            with self.subTest(snippet=snippet):
                self.assertIn(snippet, text)

    def test_r3a_mutation_contract_is_repo_tracked_and_wired(self) -> None:
        contract_path = canonical_repo_path(R3A_MUTATION_CONTRACT)
        self.assertTrue(R3A_MUTATION_CONTRACT.exists(), f"R3.A mutation contract 不存在: {R3A_MUTATION_CONTRACT}")

        contract_text = read_text(R3A_MUTATION_CONTRACT)
        for snippet in R3A_MUTATION_CONTRACT_SNIPPETS:
            with self.subTest(snippet=snippet):
                self.assertIn(snippet, contract_text)

        for path in (
            PROJECT_TRUTH,
            TOP_LEVEL_DESIGN,
            OMX_BRIDGE,
            OBJECT_MODEL_SCHEMA,
            R3A_ACTIVATION_PACKAGE,
            RUNTIME_FIRST_PROGRAM,
            RUNTIME_BOUNDARY_MAP,
            CURRENT_PROGRAM,
            PROGRAM_ROUTING,
            TEAM_PROMPT,
            EXECUTION_PROMPT,
            PRD,
            TEST_SPEC,
            IMPLEMENTATION,
        ):
            with self.subTest(path=path.name):
                self.assertIn(contract_path, read_text(path))

    def test_r4a_activation_package_is_repo_tracked_and_wired(self) -> None:
        package_path = canonical_repo_path(R4A_ACTIVATION_PACKAGE)
        self.assertTrue(R4A_ACTIVATION_PACKAGE.exists(), f"R4.A activation package 不存在: {R4A_ACTIVATION_PACKAGE}")

        text = read_text(R4A_ACTIVATION_PACKAGE)
        for snippet in R4A_ACTIVATION_SNIPPETS:
            with self.subTest(snippet=snippet):
                self.assertIn(snippet, text)

        for path in (
            PROJECT_TRUTH,
            TOP_LEVEL_DESIGN,
            OMX_BRIDGE,
            RUNTIME_FIRST_PROGRAM,
            RUNTIME_BOUNDARY_MAP,
            CURRENT_PROGRAM,
            PROGRAM_ROUTING,
            TEAM_PROMPT,
            EXECUTION_PROMPT,
            PRD,
            TEST_SPEC,
            IMPLEMENTATION,
            LATEST_STATUS,
        ):
            with self.subTest(path=path.name):
                self.assertIn(package_path, read_text(path))

    def test_r5a_activation_package_is_repo_tracked_and_wired(self) -> None:
        package_path = canonical_repo_path(R5A_ACTIVATION_PACKAGE)
        self.assertTrue(R5A_ACTIVATION_PACKAGE.exists(), f"R5.A activation package 不存在: {R5A_ACTIVATION_PACKAGE}")

        text = read_text(R5A_ACTIVATION_PACKAGE)
        for snippet in R5A_ACTIVATION_SNIPPETS:
            with self.subTest(snippet=snippet):
                self.assertIn(snippet, text)

        for path in (
            PROJECT_TRUTH,
            TOP_LEVEL_DESIGN,
            OMX_BRIDGE,
            RUNTIME_FIRST_PROGRAM,
            RUNTIME_BOUNDARY_MAP,
            CURRENT_PROGRAM,
            PROGRAM_ROUTING,
            TEAM_PROMPT,
            EXECUTION_PROMPT,
            PRD,
            TEST_SPEC,
            IMPLEMENTATION,
            LATEST_STATUS,
        ):
            with self.subTest(path=path.name):
                self.assertIn(package_path, read_text(path))

    def test_r3a_implementation_promotion_contract_is_frozen_in_active_test_spec(self) -> None:
        text = read_text(TEST_SPEC)
        for snippet in R3A_IMPLEMENTATION_PROMOTION_SNIPPETS:
            with self.subTest(snippet=snippet):
                self.assertIn(snippet, text)

    def test_r3a_machine_applicable_examples_are_frozen(self) -> None:
        cases = (
            (P2C_CRITIQUE_EXAMPLE, "revision-v1", "v0.3", "v0.4"),
            (P3B_RE_REVIEW_EXAMPLE, "revision-v2", "v0.4", "v0.5"),
        )

        for path, revision_plan_id, expected_pre, expected_post in cases:
            document = json.loads(path.read_text(encoding="utf-8"))
            current_selection = document["current_selection"]
            draft = next(item for item in document["application_drafts"] if item["draft_id"] == current_selection["active_draft_id"])
            section_keys = {item["section_key"] for item in draft["sections"]}
            outline_keys = {item["section_key"] for item in draft["outline"]}
            revision_plan = next(item for item in document["revision_plans"] if item["revision_plan_id"] == revision_plan_id)

            with self.subTest(path=path.name, field="execution_status"):
                self.assertEqual(revision_plan["execution_status"], "planned")
            with self.subTest(path=path.name, field="pre_revision_version_label"):
                self.assertEqual(revision_plan["pre_revision_version_label"], expected_pre)
            with self.subTest(path=path.name, field="post_revision_version_label"):
                self.assertEqual(revision_plan["post_revision_version_label"], expected_post)

            seen_targets: set[str] = set()
            for item in revision_plan["items"]:
                payload = item["mutation_payload"]
                with self.subTest(path=path.name, item=item["item_id"], field="operation"):
                    self.assertEqual(payload["operation"], "replace_draft_section")
                target_ref = item["target_ref"]
                self.assertTrue(target_ref.startswith("section:"))
                target_section_key = target_ref.split(":", 1)[1]
                with self.subTest(path=path.name, item=item["item_id"], field="target_consistency"):
                    self.assertEqual(payload["target_section_key"], target_section_key)
                    self.assertIn(target_section_key, section_keys)
                    self.assertNotIn(target_section_key, seen_targets)
                seen_targets.add(target_section_key)
                if target_section_key in outline_keys:
                    with self.subTest(path=path.name, item=item["item_id"], field="replacement_core_claim"):
                        self.assertTrue(payload["replacement_core_claim"])
                with self.subTest(path=path.name, item=item["item_id"], field="linked_object_ids"):
                    self.assertTrue(set(item["required_input_ids"]).issubset(set(payload["linked_object_ids"])))

    def test_r1a_runtime_surface_is_explicit_in_public_and_truth_docs(self) -> None:
        combined = "\n".join(
            read_text(path)
            for path in (
                README_EN,
                README_ZH,
                FORMAL_ENTRY_MATRIX,
                DURABILITY_MODEL,
                R1A_ACTIVATION_PACKAGE,
            )
        )
        for snippet in R1A_RUNTIME_SURFACE_SNIPPETS:
            with self.subTest(snippet=snippet):
                self.assertIn(snippet, combined)

    def test_r1b_runtime_surface_is_explicit_in_public_and_truth_docs(self) -> None:
        combined = "\n".join(
            read_text(path)
            for path in (
                README_EN,
                README_ZH,
                FORMAL_ENTRY_MATRIX,
                DURABILITY_MODEL,
                R1B_ACTIVATION_PACKAGE,
            )
        )
        for snippet in R1B_RUNTIME_SURFACE_SNIPPETS:
            with self.subTest(snippet=snippet):
                self.assertIn(snippet, combined)

    def test_r2a_runtime_surface_is_explicit_in_public_and_truth_docs(self) -> None:
        combined = "\n".join(
            read_text(path)
            for path in (
                README_EN,
                README_ZH,
                FORMAL_ENTRY_MATRIX,
                DURABILITY_MODEL,
                R2A_ACTIVATION_PACKAGE,
            )
        )
        for snippet in R2A_RUNTIME_SURFACE_SNIPPETS:
            with self.subTest(snippet=snippet):
                self.assertIn(snippet, combined)

    def test_revision_transition_contract_is_frozen_in_active_truth_surfaces(self) -> None:
        for path in (OMX_BRIDGE, PRD, TEST_SPEC, IMPLEMENTATION):
            text = read_text(path)
            for snippet in REVISION_TRANSITION_SNIPPETS:
                with self.subTest(path=path.name, snippet=snippet):
                    self.assertIn(snippet, text)

    def test_re_review_transition_contract_is_frozen_in_active_truth_surfaces(self) -> None:
        for path in (OBJECT_MODEL_SCHEMA, FORMAL_ENTRY_MATRIX, DURABILITY_MODEL, OMX_BRIDGE, PRD, TEST_SPEC, IMPLEMENTATION, P3B_CURRENT_TRUTH):
            text = read_text(path)
            for snippet in RE_REVIEW_TRANSITION_SNIPPETS:
                with self.subTest(path=path.name, snippet=snippet):
                    self.assertIn(snippet, text)

    def test_grant_run_id_contract_is_frozen_across_runtime_and_control_surfaces(self) -> None:
        for path in EXECUTION_HANDLE_REVIEW_SURFACES:
            text = read_text(path)
            with self.subTest(path=path.name):
                self.assertIn("grant_run_id", text)

        boundary_text = "\n".join(
            read_text(path)
            for path in (OMX_BRIDGE, OBJECT_MODEL_SCHEMA)
        )
        for snippet in EXECUTION_HANDLE_SNIPPETS:
            with self.subTest(snippet=snippet):
                self.assertIn(snippet, boundary_text)

        bridge_text = read_text(OMX_BRIDGE)
        self.assertIn("repo-tracked review surfaces", bridge_text)
        self.assertIn("local durable handoff surfaces", bridge_text)

    def test_execution_handle_and_durable_report_surfaces_are_explicit_in_public_and_truth_docs(self) -> None:
        combined = "\n".join(
            read_text(path)
            for path in (
                README_EN,
                README_ZH,
                PROJECT_TRUTH,
                POSITIONING_DOC,
                FORMAL_ENTRY_MATRIX,
                DURABILITY_MODEL,
            )
        )

        for snippet in EXECUTION_HANDLE_SNIPPETS:
            with self.subTest(snippet=snippet):
                self.assertIn(snippet, combined)

        for snippet in DURABLE_REPORT_SURFACE_SNIPPETS:
            with self.subTest(report_surface=snippet):
                self.assertIn(snippet, combined)

    def test_verification_checkpoint_surface_is_explicit_in_public_and_truth_docs(self) -> None:
        combined = "\n".join(
            read_text(path)
            for path in (
                README_EN,
                README_ZH,
                PROJECT_TRUTH,
                POSITIONING_DOC,
                FORMAL_ENTRY_MATRIX,
                DURABILITY_MODEL,
                P3C_CURRENT_TRUTH,
                P4A_CURRENT_TRUTH,
                P4B_CURRENT_TRUTH,
            )
        )

        for snippet in VERIFICATION_CHECKPOINT_SNIPPETS:
            with self.subTest(snippet=snippet):
                self.assertIn(snippet, combined)

    def test_p3a_p3b_and_p3c_current_truth_docs_are_referenced_in_active_control_surfaces(self) -> None:
        p3a_path_text = canonical_repo_path(P3A_CURRENT_TRUTH)
        p3b_path_text = canonical_repo_path(P3B_CURRENT_TRUTH)
        p3c_path_text = canonical_repo_path(P3C_CURRENT_TRUTH)
        for path in (CURRENT_PROGRAM, PROGRAM_ROUTING, PRD, TEST_SPEC, IMPLEMENTATION):
            with self.subTest(path=path.name):
                self.assertIn(p3a_path_text, read_text(path))
                self.assertIn(p3b_path_text, read_text(path))
                self.assertIn(p3c_path_text, read_text(path))

    def test_p4a_current_truth_doc_is_referenced_in_active_control_surfaces(self) -> None:
        p4a_path_text = canonical_repo_path(P4A_CURRENT_TRUTH)
        for path in (CURRENT_PROGRAM, PROGRAM_ROUTING, PRD, TEST_SPEC, IMPLEMENTATION):
            with self.subTest(path=path.name):
                self.assertIn(p4a_path_text, read_text(path))

    def test_p4b_current_truth_doc_is_referenced_in_active_control_surfaces(self) -> None:
        p4b_path_text = canonical_repo_path(P4B_CURRENT_TRUTH)
        for path in (CURRENT_PROGRAM, PROGRAM_ROUTING, PRD, TEST_SPEC, IMPLEMENTATION):
            with self.subTest(path=path.name):
                self.assertIn(p4b_path_text, read_text(path))

    def test_p4b_current_truth_freezes_checkpoint_surface_boundary(self) -> None:
        text = read_text(P4B_CURRENT_TRUTH)
        for snippet in (
            "VerificationCheckpoint",
            "validate-workspace",
            "summarize-workspace",
            "next-step",
            "critique-summary",
            "stage-route-report",
            "verification_checkpoint",
            "checkpoint_status",
            "author-side",
            "proposal-facing",
            "CLI",
            "MCP",
            "controller",
            "not-yet-supported",
            "grant_run_id",
            "workspace_id",
            "draft_id",
            "program_id",
        ):
            with self.subTest(snippet=snippet):
                self.assertIn(snippet, text)

    def test_object_model_and_p3_current_truth_freeze_verdict_re_review_and_rollback_gate_contract(self) -> None:
        combined = "\n".join(
            read_text(path)
            for path in (
                OBJECT_MODEL_SCHEMA,
                P2C_CURRENT_TRUTH,
                P3A_CURRENT_TRUTH,
                P3B_CURRENT_TRUTH,
                P3C_CURRENT_TRUTH,
                P4A_CURRENT_TRUTH,
                P4B_CURRENT_TRUTH,
            )
        )
        for snippet in (
            "current_selection",
            "selected_direction_id",
            "selected_question_id",
            "active_fit_mapping_id",
            "active_draft_id",
            "active_revision_plan_id",
            "critique",
            "revision",
            "MentorCritique",
            "RevisionPlan",
            "major_reframe",
            "major_revision",
            "minor_revision",
            "ready_for_submission",
            "question_refinement",
            "frozen",
            "reviewed_revision_plan_id",
            "reviewed_revision_evidence",
            "source_critique_id",
            "forced_rollback_stage",
            "forced_rollback_reason",
            "presubmission_frozen",
        ):
            with self.subTest(snippet=snippet):
                self.assertIn(snippet, combined)

    def test_rollback_and_presubmission_gate_contract_is_frozen_in_active_truth_surfaces(self) -> None:
        for path in (OBJECT_MODEL_SCHEMA, FORMAL_ENTRY_MATRIX, DURABILITY_MODEL, OMX_BRIDGE, PRD, TEST_SPEC, IMPLEMENTATION, P3C_CURRENT_TRUTH):
            text = read_text(path)
            for snippet in ROLLBACK_GATE_SNIPPETS:
                with self.subTest(path=path.name, snippet=snippet):
                    self.assertIn(snippet, text)

    def test_external_verifier_is_not_current_hard_gate(self) -> None:
        current_program_text = read_text(CURRENT_PROGRAM)
        test_spec_text = read_text(TEST_SPEC)
        latest_status_text = read_text(LATEST_STATUS)
        open_issues_text = read_text(OPEN_ISSUES)

        for text in (current_program_text, test_spec_text, latest_status_text, open_issues_text):
            self.assertIn("advisory", text)

        self.assertNotIn(
            "python3 /Users/gaofeng/workspace/app/omx-project-installer/skills/omx-project-installer/scripts/omx_project_installer.py diff --target /Users/gaofeng/workspace/med-autogrant",
            test_spec_text,
        )


if __name__ == "__main__":
    unittest.main()
