# P4.B Verification OS And Checkpoint Surface Current Truth

> 生命周期注记（`2026-05-17`）：这份 dated spec 是 path-stable 的历史/支撑记录；只有 `docs/specs/README.md`、`docs/specs/specs_lifecycle_map.md`、`docs/status.md` 或 `contracts/runtime-program/current-program.json` 明确指定的仍 current subsection 才可作为当前边界阅读。请先读取 `docs/status.md`、核心五件套与 `contracts/runtime-program/current-program.json`。本文中的旧 `Current Truth`、Hermes、OPL Gateway、host-agent 或 federation wording 只作 provenance，不是当前 default owner line。

Date: `2026-04-08`

## Activation Status

- Current phase: `P4 / Verification OS And HITL Layering Preparation`
- Active tranche: `P4.B / Verification OS And Checkpoint Surface`
- Status: `activation-frozen / implementation pending`
- Latest absorbed upstream implementation checkpoint: `P4.A / Verification Gate Surface`（freeze commit `16572e2`，implementation commit `fcf45c0`）

## Goal

在不改写 `CLI` formal entry、不扩 `MCP / controller`、不破坏 `grant_run_id / workspace_id / draft_id / program_id` 边界、也不把 author-side mainline 改写成 reviewer / HITL 产品的前提下，把当前 verification OS 与 checkpoint surface 冻结成同一组 canonical durable surface：明确 `VerificationCheckpoint` 的对象边界、`stage-route-report.verification_checkpoint` 的唯一聚合地位、以及 reports / control surfaces 应如何 durable 地回写 checkpoint truth。

## Hard Boundary Docs

- `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-07-formal-entry-matrix-current-truth.md`
- `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-07-durability-model-clarification.md`
- `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-07-p2b-argument-fit-outline-mainline-current-truth.md`
- `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-07-p2c-draft-critique-revision-skeleton-mainline-current-truth.md`
- `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-07-p3a-mentor-verdict-contract-freeze-current-truth.md`
- `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-08-p3b-revision-transition-and-re-review-hardening-current-truth.md`
- `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-08-p3c-forced-rollback-and-presubmission-gate-current-truth.md`
- `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-08-p4a-verification-gate-surface-current-truth.md`

## Current Hard Boundaries

- 当前 formal entry 仍只有 `CLI`；`MCP / controller` 仍是 `not-yet-supported / future scope`。
- `VerificationCheckpoint` 不是新的 formal entry、不是新的 runtime identity，也不是新的 `controller` capability。
- `grant_run_id / workspace_id / draft_id / program_id` 继续分离；checkpoint 只能回显这些身份，不得替代这些身份。
- 当前 mainline 仍是 author-side、proposal-facing、agent-first 的验证/批注主线，不引入 reviewer-owned surface，也不声明 future `Human-in-the-loop` layer 已经存在。
- team gate 不放宽；`P4.B` activation package 只冻结 truth 与 control surfaces，不扩大 bounded team。
- absorbed `P3.B` 的 `reviewed_revision_plan_id / reviewed_revision_evidence / source_critique_id / active_revision_plan_id` 继续保留。
- absorbed `P3.C` 的 `forced_rollback_stage / forced_rollback_reason / presubmission_frozen` 继续保留。
- absorbed `P4.A` 的 `forward_progress / freeze_ready / rollback_required / submission_frozen` vocabulary 继续保留。

## Object Boundary

### `VerificationCheckpoint`

`P4.B` 当前冻结的 object boundary 是派生 checkpoint 对象 `VerificationCheckpoint`。它当前的 canonical runtime location 仍是：

- `stage-route-report.verification_checkpoint`

它不是：

- `NSFCWorkspace` 新的顶层字段
- 新的 CLI command
- 新的 schema identity object
- 新的 formal entry

当前 `VerificationCheckpoint` 至少继续保留以下字段簇：

- `checkpoint_status`
- `validation_ok`
- `identity`
  - `grant_run_id`
  - `workspace_id`
  - `draft_id`
  - `active_revision_plan_id`
  - `reviewed_revision_plan_id`
- `route_alignment`
  - `lifecycle_stage`
  - `recommended_next_stage`
  - `forced_rollback_stage`
  - `forced_rollback_reason`
  - `presubmission_frozen`
- `review_checkpoint`
  - `critique_id`
  - `reviewed_revision_evidence`
  - `blocking_issue_count`

## Canonical Durable Surface

`P4.B` 把 verification OS 的 canonical durable surface 冻结为三层，但不新增 formal entry：

1. **runtime aggregation surface**
   - `stage-route-report.verification_checkpoint`
2. **repo-tracked current truth**
   - 本文档
   - formal entry / durability current truth
   - bridge / active truth docs
3. **local durable handoff / report surface**
   - `CURRENT_PROGRAM`
   - active `PRD / test-spec / implementation`
   - `LATEST_STATUS / ITERATION_LOG / OPEN_ISSUES`

其中：

- runtime 层只负责输出 canonical checkpoint object
- repo-tracked truth 负责冻结它是什么、它不是什么
- local reports 只负责 durable 回写 checkpoint truth 与 verification snapshot，不发明新的 runtime 成熟度结论

## Relation To Existing CLI Surfaces

- `validate-workspace`
  - 继续提供 validation gate truth
  - 不直接输出 `checkpoint_status`
- `summarize-workspace`
  - 继续提供 state snapshot truth
  - 不直接输出 `checkpoint_status`
- `next-step`
  - 继续提供 route recommendation truth
  - 不直接输出 `checkpoint_status`
- `critique-summary`
  - 继续提供 critique-centered review truth
  - 不直接输出 `checkpoint_status`
- `stage-route-report`
  - 继续作为唯一 canonical route aggregation surface
  - 继续作为唯一 canonical `VerificationCheckpoint` 聚合 surface

禁止把多个 CLI surface 写成各自维护一份独立 checkpoint truth。

## Retain / Lift / Prohibit Rules

### Continue To Retain

- `verification_checkpoint / checkpoint_status`
- `forward_progress / freeze_ready / rollback_required / submission_frozen`
- `reviewed_revision_evidence`
- `forced_rollback_stage / forced_rollback_reason`
- `presubmission_frozen`
- `grant_run_id / workspace_id / draft_id / program_id`

### Lift In P4.B

`P4.B` 只上提两件事：

1. 把 `VerificationCheckpoint` 明确冻结成 author-side checkpoint durable object
2. 把 reports / control surfaces 回写的 durable checkpoint truth 与 runtime checkpoint object 的关系写清楚

### Prohibit Mixing

禁止把下列语义混写进 `checkpoint_status`：

- 新的 formal entry 语义
- 新的 runtime identity 语义
- reviewer / HITL 决策语义
- `MCP / controller` capability maturity
- submission-grade runtime 成熟度宣称
- 与 `lifecycle_stage` 冲突的第二套阶段系统

## Canonical Examples

- `examples/nsfc_workspace_p2c_revision.json`
- `examples/nsfc_workspace_p3b_re_review_major_revision.json`
- `examples/nsfc_workspace_p3c_forced_rollback_argument.json`
- `examples/nsfc_workspace_p3a_ready_for_submission.json`
- `examples/nsfc_workspace_p3c_presubmission_frozen.json`

其中：

- `p2c_revision` 继续代表 `forward_progress`
- `p3c_forced_rollback_argument` 继续代表 `rollback_required`
- `p3a_ready_for_submission` 继续代表 `freeze_ready`
- `p3c_presubmission_frozen` 继续代表 `submission_frozen`

## Required Verification Contract For Activation Package

当前 `P4.B` activation package 继续沿用 repo-native hard gate，不新增 formal entry，也不新增 CLI command：

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

## Enter-Implementation Preconditions

只有以下条件全部满足，才允许进入 `P4.B` implementation：

1. `CURRENT_PROGRAM`、active `PRD / test-spec / implementation`、reports 与 repo-tracked truth 已同步到 `P4.B`
2. `VerificationCheckpoint` 的 object boundary、durable surface、CLI relation 与 excluded scope 已冻结
3. repo-native hard gate 全绿
4. 不需要新增 schema field、formal entry、controller capability、team gate 或 future HITL 解释

## Stop Conditions

若出现以下任一情况，必须停车：

- 无法在当前 truth 内诚实说明 `VerificationCheckpoint` 是 derived checkpoint object，而不是新的 runtime state surface
- 继续实现需要新增 schema field、`MCP / controller` 解释、team gate 扩面、或新的 reviewer / HITL 产品边界
- 必须新增 formal entry 或 submission-grade runtime 宣称才能推进
- reports / control surfaces / repo-tracked truth 之间出现不可裁决冲突

## Excluded Scope

- `MCP` public runtime entry
- `controller` public runtime entry
- future `Human-in-the-loop` layer
- team gate 扩面
- submission-grade runtime 宣称
- reviewer-owned surface
- 新的 CLI command
- 把 `VerificationCheckpoint` 持久写回 `NSFCWorkspace` schema
