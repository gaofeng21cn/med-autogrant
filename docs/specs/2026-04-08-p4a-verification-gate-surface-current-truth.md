# P4.A Verification Gate Surface Current Truth

Date: `2026-04-08`

## Activation Status

- Current phase: `P4 / Verification OS And HITL Layering Preparation`
- Active tranche: `P4.A / Verification Gate Surface`
- Status: `canonical behavior implemented / hard-gate verified`
- Latest absorbed upstream tranche before P4.A: `P3.C / Forced Rollback And Presubmission Gate`（commit `52b18fe`）

## Goal

在不改写 `grant_run_id`、formal entry、durability、team gate 与已 absorbed `P2.A / P2.B / P2.C / P3.A / P3.B / P3.C` 合同的前提下，把当前 author-side mainline 的 verification gate surface 冻结成一组 canonical machine-readable behavior：围绕 `validate-workspace`、`summarize-workspace`、`next-step`、`critique-summary`、`stage-route-report` 收紧 validation、checkpoint、route aggregation 与 frozen gate 语义。

## Hard Boundary Docs

- `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-07-formal-entry-matrix-current-truth.md`
- `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-07-durability-model-clarification.md`
- `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-07-p2b-argument-fit-outline-mainline-current-truth.md`
- `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-07-p2c-draft-critique-revision-skeleton-mainline-current-truth.md`
- `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-07-p3a-mentor-verdict-contract-freeze-current-truth.md`
- `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-08-p3b-revision-transition-and-re-review-hardening-current-truth.md`
- `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-08-p3c-forced-rollback-and-presubmission-gate-current-truth.md`

## Current Hard Boundaries

- `grant_run_id` 继续是当前正式 execution handle；必须与 `workspace_id`、`draft_id`、`program_id` 分离。
- 当前 formal entry 仍只有 `CLI`；`MCP / controller` 仍是 `not-yet-supported / future scope`。
- `validate-workspace` 仍是 validation surface，不是新的 execution handle，也不是新的 formal entry。
- absorbed `P3.B` 的 `reviewed_revision_plan_id / reviewed_revision_evidence / source_critique_id / active_revision_plan_id` 继续保留。
- absorbed `P3.C` 的 `forced_rollback_stage / forced_rollback_reason / presubmission_frozen` 继续保留。
- 不在本 tranche 内改写 team gate，不把 future `Human-in-the-loop` layer 或 `MCP / controller` 写成当前已支持。

## Canonical Verification Gate Surface

### 1. `validate-workspace`

- 负责输出 workspace 是否通过当前 repo-native validation gate。
- 必须稳定回显：`ok / grant_run_id / workspace_id / lifecycle_stage / error_count / errors[]`。
- structured JSON failure envelope 继续保留；它回答的是 validation 是否通过，不代替 checkpoint aggregation。

### 2. `summarize-workspace`

- 负责输出当前 verification gate 依赖的 state snapshot。
- 必须稳定回显：`grant_run_id / workspace_id / gates / current_selection / active_draft / active_revision_plan / active_critique / reviewed_revision_evidence`。
- 在 gate-open `ready_for_submission` 语境下，必须把 `gates.presubmission_frozen=false` 与 `active_critique.verdict=ready_for_submission` 同时暴露出来。

### 3. `next-step`

- 负责输出当前 canonical route recommendation。
- 必须稳定回显：`grant_run_id / workspace_id / current_stage / recommended_stage / reason / actions / requires_human_confirmation / presubmission_frozen`。
- 若存在 forced rollback，则继续回显 `forced_rollback_stage`。
- 对 `ready_for_submission + presubmission_frozen=false` 的 gate-open 状态，必须稳定推荐 `recommended_stage=frozen`。

### 4. `critique-summary`

- 负责输出当前 critique-centered verification audit。
- 必须稳定回显：`draft_id / critique_id / revision_plan_id / verdict / reviewed_revision_plan_id / reviewed_revision_evidence / forced_rollback_stage / forced_rollback_reason / presubmission_frozen / recommended_next_stage`。
- gate-open `ready_for_submission` example 必须明确保持 `presubmission_frozen=false`，避免与真正 frozen 的 presubmission gate 混写。

### 5. `stage-route-report`

- 是当前 canonical machine-readable route aggregation surface。
- 必须聚合：`validate-workspace`、`summarize-workspace`、`next-step`、`critique-summary`。
- 必须输出：`verification_checkpoint` 与 `checkpoint_status`。
- `verification_checkpoint` 当前至少继续聚合：`validation_ok`、identity、route alignment、review checkpoint、reviewed revision evidence、forced rollback 与 frozen gate 语义。
- 对 `ready_for_submission + presubmission_frozen=false` 的 gate-open canonical example，`checkpoint_status` 现已实现为 `freeze_ready`，不再落入 generic `forward_progress`。

## Checkpoint Vocabulary Freeze

`P4.A` activation package 先冻结以下 `checkpoint_status` 词汇表，再由实现把它们收紧成 canonical behavior：

- `forward_progress`
- `freeze_ready`
- `rollback_required`
- `submission_frozen`

其中：

- `freeze_ready` 专门保留给 `ready_for_submission + presubmission_frozen=false` 的 gate-open author-side 状态；它不能继续被 generic `forward_progress` 吞掉。
- `submission_frozen` 只保留给 `presubmission_frozen=true + lifecycle_stage=frozen` 的 gate-closed 状态。

## Canonical Examples

- `examples/nsfc_workspace_p2c_revision.json`
- `examples/nsfc_workspace_p3b_re_review_major_revision.json`
- `examples/nsfc_workspace_p3c_forced_rollback_argument.json`
- `examples/nsfc_workspace_p3a_ready_for_submission.json`
- `examples/nsfc_workspace_p3c_presubmission_frozen.json`

其中：

- `examples/nsfc_workspace_p3a_ready_for_submission.json` 是当前 `P4.A` 新冻结的 gate-open canonical example。
- `examples/nsfc_workspace_p3c_presubmission_frozen.json` 继续作为 gate-closed frozen canonical example。

## Required Verification Contract

当前 tranche 以以下 repo-native commands 作为 freeze 与 implementation 共用的 hard gate：

1. `python3 -m unittest discover -s tests -p 'test_*.py'`
2. `PYTHONPATH=src python3 -m med_autogrant validate-workspace --input examples/nsfc_workspace_p2c_revision.json --format json`
3. `PYTHONPATH=src python3 -m med_autogrant validate-workspace --input examples/nsfc_workspace_p3b_re_review_major_revision.json --format json`
4. `PYTHONPATH=src python3 -m med_autogrant validate-workspace --input examples/nsfc_workspace_p3c_forced_rollback_argument.json --format json`
5. `PYTHONPATH=src python3 -m med_autogrant validate-workspace --input examples/nsfc_workspace_p3a_ready_for_submission.json --format json`
6. `PYTHONPATH=src python3 -m med_autogrant validate-workspace --input examples/nsfc_workspace_p3c_presubmission_frozen.json --format json`
7. `PYTHONPATH=src python3 -m med_autogrant summarize-workspace --input examples/nsfc_workspace_p2c_revision.json --format json`
8. `PYTHONPATH=src python3 -m med_autogrant summarize-workspace --input examples/nsfc_workspace_p3b_re_review_major_revision.json --format json`
9. `PYTHONPATH=src python3 -m med_autogrant summarize-workspace --input examples/nsfc_workspace_p3c_forced_rollback_argument.json --format json`
10. `PYTHONPATH=src python3 -m med_autogrant summarize-workspace --input examples/nsfc_workspace_p3a_ready_for_submission.json --format json`
11. `PYTHONPATH=src python3 -m med_autogrant summarize-workspace --input examples/nsfc_workspace_p3c_presubmission_frozen.json --format json`
12. `PYTHONPATH=src python3 -m med_autogrant next-step --input examples/nsfc_workspace_p2c_revision.json --format json`
13. `PYTHONPATH=src python3 -m med_autogrant next-step --input examples/nsfc_workspace_p3b_re_review_major_revision.json --format json`
14. `PYTHONPATH=src python3 -m med_autogrant next-step --input examples/nsfc_workspace_p3c_forced_rollback_argument.json --format json`
15. `PYTHONPATH=src python3 -m med_autogrant next-step --input examples/nsfc_workspace_p3a_ready_for_submission.json --format json`
16. `PYTHONPATH=src python3 -m med_autogrant next-step --input examples/nsfc_workspace_p3c_presubmission_frozen.json --format json`
17. `PYTHONPATH=src python3 -m med_autogrant critique-summary --input examples/nsfc_workspace_p2c_revision.json --format json`
18. `PYTHONPATH=src python3 -m med_autogrant critique-summary --input examples/nsfc_workspace_p3b_re_review_major_revision.json --format json`
19. `PYTHONPATH=src python3 -m med_autogrant critique-summary --input examples/nsfc_workspace_p3c_forced_rollback_argument.json --format json`
20. `PYTHONPATH=src python3 -m med_autogrant critique-summary --input examples/nsfc_workspace_p3a_ready_for_submission.json --format json`
21. `PYTHONPATH=src python3 -m med_autogrant critique-summary --input examples/nsfc_workspace_p3c_presubmission_frozen.json --format json`
22. `PYTHONPATH=src python3 -m med_autogrant stage-route-report --input examples/nsfc_workspace_p2c_revision.json --format json`
23. `PYTHONPATH=src python3 -m med_autogrant stage-route-report --input examples/nsfc_workspace_p3b_re_review_major_revision.json --format json`
24. `PYTHONPATH=src python3 -m med_autogrant stage-route-report --input examples/nsfc_workspace_p3c_forced_rollback_argument.json --format json`
25. `PYTHONPATH=src python3 -m med_autogrant stage-route-report --input examples/nsfc_workspace_p3a_ready_for_submission.json --format json`
26. `PYTHONPATH=src python3 -m med_autogrant stage-route-report --input examples/nsfc_workspace_p3c_presubmission_frozen.json --format json`
27. `git diff --check`

这些命令共同证明：

- CLI formal entry 未漂移；`grant_run_id / workspace_id / draft_id / program_id` 边界继续稳定。
- `validate-workspace / summarize-workspace / next-step / critique-summary / stage-route-report` 继续构成当前 author-side verification gate surface。
- gate-open `ready_for_submission` 与 gate-closed `presubmission_frozen` 已被同时纳入 machine-readable hard gate。
- absorbed `P3.B / P3.C` 的 reviewed revision evidence、forced rollback 与 frozen gate 语义继续保留。

## Non-goals

- 不进入 `P4.B / Verification OS And Checkpoint Surface`
- 不扩 `MCP / controller` formal entry
- 不把 future `Human-in-the-loop` layer 写成当前产品 runtime
- 不把 CLI-only current truth 改写成 submission-grade mature runtime

## Exit Criteria

`P4.A` 只有在以下条件都满足时才算完成：

1. active `test-spec` 中的 repo-native commands 全绿。
2. `freeze_ready / rollback_required / submission_frozen` checkpoint 语义与 canonical examples 一致。
3. `CURRENT_PROGRAM`、`PROGRAM_ROUTING`、active `PRD / test-spec / implementation` 与 reports 一致表述 `P4.A`，历史 OMX prompt 不再作为活跃校验面。
4. formal entry、durability、team gate、ID-boundary 与 absorbed upstream truth surfaces 均未漂移。
