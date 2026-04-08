# Durability Model Clarification

Date: `2026-04-07`

## 目标

在当前 active mainline 下，把 repo-durable review truth、local durable handoff truth 与对象身份边界写清楚，避免 review、恢复和 runtime identity 三类语义继续混写。

## 当前指针

- Current phase: `Runtime Productization Program`
- Active tranche: `R1 / Autonomous Main Loop`
- Active slice: `R1.B / Stage Action Executor Envelope`

## repo-tracked review surfaces

当前 reviewer 应能仅凭以下 repo-tracked surfaces 理解 runtime baseline 的正式合同：

- `README.md`
- `README.zh-CN.md`
- `docs/specs/2026-04-06-med-autogrant-mainline-and-omx-bridge.md`
- `docs/specs/2026-04-06-object-model-schema-v1.md`
- `docs/specs/2026-04-07-formal-entry-matrix-current-truth.md`
- `docs/specs/2026-04-07-durability-model-clarification.md`
- `docs/specs/2026-04-07-p2b-argument-fit-outline-mainline-current-truth.md`
- `docs/specs/2026-04-07-p2c-draft-critique-revision-skeleton-mainline-current-truth.md`
- `docs/specs/2026-04-07-p3a-mentor-verdict-contract-freeze-current-truth.md`
- `docs/specs/2026-04-08-p3b-revision-transition-and-re-review-hardening-current-truth.md`
- `docs/specs/2026-04-08-p3c-forced-rollback-and-presubmission-gate-current-truth.md`
- `docs/specs/2026-04-08-p4a-verification-gate-surface-current-truth.md`
- `docs/specs/2026-04-08-p4b-verification-os-and-checkpoint-surface-current-truth.md`
- `docs/specs/2026-04-08-r1a-local-main-loop-entry-and-stop-reason-activation-package.md`
- `schemas/v1/nsfc-workspace.schema.json`
- `schemas/v1/application-draft.schema.json`
- `schemas/v1/mentor-critique.schema.json`
- `schemas/v1/revision-plan.schema.json`
- `examples/nsfc_workspace_minimal.json`
- `examples/nsfc_workspace_p2c_revision.json`
- `examples/nsfc_workspace_p3a_ready_for_submission.json`
- `examples/nsfc_workspace_p3b_re_review_major_revision.json`
- `examples/nsfc_workspace_p3c_forced_rollback_argument.json`
- `examples/nsfc_workspace_p3c_presubmission_frozen.json`
- `tests/test_cli_validate_workspace.py`
- `tests/test_stage_router.py`
- `tests/test_workspace_summary.py`
- `tests/test_program_control_surfaces.py`
- `tests/test_local_runtime.py`

这些 surface 承担的是 review truth 职责：

- formal entry 是什么
- 哪些能力当前正式支持
- 哪些语义是 future scope
- `grant_run_id / workspace_id / draft_id / program_id` 的边界
- 当前 repo-native hard gate 命令是什么
- `ApplicationDraft.sections`、`MentorCritique`、`RevisionPlan` 是否进入当前 canonical route
- `major_reframe / major_revision / minor_revision / ready_for_submission` 是否进入当前 canonical verdict surface
- `current_selection.active_revision_plan_id` 是否继续作为当前 active route pointer
- `reviewed_revision_plan_id / reviewed_revision_evidence / source_critique_id` 是否进入当前 canonical re-review surface
- `forced_rollback_stage / forced_rollback_reason / presubmission_frozen` 是否进入当前 canonical rollback / gate surface
- `stage-route-report.verification_checkpoint / checkpoint_status` 是否成为当前 canonical verification aggregation surface
- `ready_for_submission + presubmission_frozen=false` 是否作为当前 canonical gate-open checkpoint surface
- `VerificationCheckpoint` 是否继续只是 derived checkpoint object，而不是新的 formal entry、identity 或 controller capability
- `run-local / resume-local`、machine-readable `stop_reason`、`stage_action_envelope`、以及 local run journal 是否进入当前 canonical local runtime surface

## local durable handoff surfaces

当前恢复与连续执行依赖以下 local durable handoff surfaces：

- `.omx/context/CURRENT_PROGRAM.md`
- `.omx/context/PROGRAM_ROUTING.md`
- `.omx/context/OMX_TEAM_PROMPT.md`
- `.omx/context/OMX_EXECUTION_PROMPT.md`
- `.omx/plans/spec-program-operating-model.md`
- `.omx/plans/prd-med-autogrant-mainline.md`
- `.omx/plans/test-spec-med-autogrant-mainline.md`
- `.omx/plans/implementation-med-autogrant-mainline.md`
- `.omx/reports/med-autogrant-mainline/LATEST_STATUS.md`
- `.omx/reports/med-autogrant-mainline/ITERATION_LOG.md`
- `.omx/reports/med-autogrant-mainline/OPEN_ISSUES.md`

这些 surface 承担的是 handoff / resume truth 职责：

- 当前 phase / tranche pointer
- 当前 hard gate 与 exit criteria
- 当前 verification snapshot
- 当前 active blocker / risk
- 恢复执行的读取顺序

## local runtime durable surface

除 `.omx/**` 的 control-plane durable handoff 之外，当前产品 runtime 还新增一层 machine-local durable runtime surface：

- `run-local --journal ...`
- `resume-local --journal ...`
- local run journal JSON

这层负责：

- 为同一 `grant_run_id` durable 回写 `latest_stop_reason`
- 为 `stage_action_required` 类 stop reason durable 回写 `latest_stage_action_envelope`
- durable 回写 `latest_route_report`
- 通过 `attempts` 记录 `run-local / resume-local` 的本地 runtime 进入历史，包括 attempt 级 `stage_action_envelope`

它不负责：

- 充当 repo-tracked review truth
- 替代 `.omx/reports/**`
- 发明新的 `program_id` 或 controller pointer

## 哪些结论必须 repo-native

以下结论如果要成为正式 review truth，必须进入 repo-tracked surface，而不能只留在 `.omx/**`：

- formal entry matrix
- durability model clarification
- verification contract 中的 hard gate 命令集合
- `grant_run_id / workspace_id / draft_id / program_id` 的正式语义边界
- `CLI`、`MCP`、`controller` 各自是否正式支持
- `ApplicationDraft.sections`、`MentorCritique`、`RevisionPlan` 是否进入当前 canonical route
- `major_reframe / major_revision / minor_revision / ready_for_submission` 是否进入当前 canonical verdict surface
- `current_selection.active_revision_plan_id` 是否继续作为当前 active route pointer
- `reviewed_revision_plan_id / reviewed_revision_evidence / source_critique_id` 是否进入当前 canonical re-review surface
- `forced_rollback_stage / forced_rollback_reason / presubmission_frozen` 是否进入当前 canonical rollback / gate surface
- `stage-route-report.verification_checkpoint / checkpoint_status` 是否成为当前 canonical verification aggregation surface
- `ready_for_submission + presubmission_frozen=false` 是否成为当前 canonical gate-open checkpoint surface
- `VerificationCheckpoint` 是否作为当前 canonical durable checkpoint object 被冻结
- `run-local / resume-local / stop_reason / stage_action_envelope / local run journal` 是否成为当前 canonical local runtime surface

## 哪些状态允许只留在 local handoff surfaces

以下信息可以继续只由 `.omx/**` 承担：

- 当前 active program / phase / tranche pointer
- 当前最新 verification snapshot
- 当前 open risks / blockers
- 当前 resume 顺序与执行提示
- 当前一次 closeout 的 leader notes 与 iteration log

但 `.omx/**` 不能单独发明新的 formal entry、verification hard gate 或 identity semantics。

## Identity Boundary Contract

- `grant_run_id`
  - 语义：单次 grant run 的稳定执行句柄
  - 落点：runtime output、CLI output、reports、recovery context 回显
- `workspace_id`
  - 语义：`NSFCWorkspace` 聚合根身份
  - 落点：workspace object identity
- `draft_id`
  - 语义：`ApplicationDraft` 身份
  - 落点：draft / critique / revision 链接身份
  - 约束：`revision` 完成后仍沿用同一 `draft_id`
- `program_id`
  - 语义：control-plane / report-routing 身份
  - 落点：`.omx/reports/<program_id>/` 与 active mainline pointer

这四类 ID 不得互相替代。

## Verification Boundary Contract

- 当前 tranche hard gate：只看 repo-native commands 与 repo-native tests
- external verifier `omx_project_installer.py diff --target ...`
  - 当前仅为 advisory external check
  - 失败必须在 reports 中被记录
  - 但在没有显式改写 active truth surfaces 前，不得重新写成 current hard gate

## 当前 freeze 结论

- formal entry 真相已进入 repo-durable current truth
- durability model 真相已进入 repo-durable current truth
- `grant_run_id / workspace_id / draft_id / program_id` 边界已在 docs / schema / example / CLI / tests / reports 中一致
- `P2.B` 的 `ArgumentChain / ApplicantFitMapping / ApplicationDraft.outline` 继续作为上游 canonical route 保留
- `P2.C` 已把 `ApplicationDraft / MentorCritique / RevisionPlan` 冻结成 absorbed canonical route
- `P3.A` 已把 `major_reframe / major_revision / minor_revision / ready_for_submission` 冻结成当前 canonical verdict surface
- `P3.B` 已把 `current_selection.active_revision_plan_id`、`MentorCritique.reviewed_revision_plan_id`、`reviewed_revision_evidence`、`source_critique_id` 与当前 active `RevisionPlan` 的边界冻结成当前 canonical re-review surface
- `P3.C` 已把 `forced_rollback_stage / forced_rollback_reason / presubmission_frozen` 的 rollback / gate surface 冻结进 current truth
- `P4.A` 已把 `ready_for_submission + presubmission_frozen=false` 的 gate-open verification surface 冻结进 current truth，并把 `examples/nsfc_workspace_p3a_ready_for_submission.json` 纳入 hard gate
- `P4.B` 已冻结 `VerificationCheckpoint` 的 canonical durable surface，并明确 `stage-route-report.verification_checkpoint / checkpoint_status` 与 reports / control surfaces 的 durable 对齐关系
- `R1.A` 已把 `run-local / resume-local`、machine-readable `stop_reason` 与 local run journal 冻结成当前 local runtime surface
- `R1.B` 已把 `stage_action_required` 分支上的 machine-readable `stage_action_envelope` 与 `latest_stage_action_envelope` 冻结成当前 local runtime orchestration surface
