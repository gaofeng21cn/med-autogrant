# R1.A Local Main Loop Entry And Stop Reason Activation Package

Date: `2026-04-08`

## Activation Status

- Active phase: `Runtime Productization Program`
- Active tranche: `R1 / Autonomous Main Loop`
- Active slice: `R1.A / Local Main Loop Entry And Stop Reason`
- Status: `frozen / implementation pending`
- Upstream prerequisite: 当前 runtime-first control surfaces、baseline hard gate、以及旧五个 canonical CLI surfaces 必须继续保持全绿

## Goal

在不改写 `CLI` formal entry、不把 `MCP / controller` 写成已支持 public runtime、不破坏 `grant_run_id / workspace_id / draft_id / program_id` 边界、也不把 author-side mainline 改写成 reviewer / HITL / hosted runtime 产品的前提下，冻结 `R1.A` 的最小实现合同：

- 增加一个本地 `runtime-run` 主循环入口
- 增加一个 `runtime-resume` 恢复入口
- 把 stop reason 冻结成 machine-readable object
- 把同一 `grant_run_id` 的本地 run journal 冻结成 durable machine-readable journal surface

`R1.A` 当前冻结的不是“已经实现”的事实，而是：

- 首个本地主循环切片的 object boundary
- CLI entry / journal / stop reason / resume 的最小 canonical surface
- 进入实现前必须满足的 verification、excluded scope 与 invariants

## Hard Boundary Docs

- `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-08-runtime-first-productization-program.md`
- `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-07-formal-entry-matrix-current-truth.md`
- `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-07-durability-model-clarification.md`
- `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-08-p3b-revision-transition-and-re-review-hardening-current-truth.md`
- `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-08-p3c-forced-rollback-and-presubmission-gate-current-truth.md`
- `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-08-p4a-verification-gate-surface-current-truth.md`
- `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-08-p4b-verification-os-and-checkpoint-surface-current-truth.md`

## Object Boundary

`R1.A` 冻结的对象边界是一个 **read-only local runtime pass**：

`workspace input -> validate-workspace -> summarize-workspace -> next-step -> critique-summary -> stage-route-report -> stop_reason`

它当前负责：

1. 调用并聚合旧五个 canonical CLI surfaces 的既有语义
2. 从 `stage-route-report` 与 `verification_checkpoint` 派生 machine-readable `stop_reason`
3. 把本次 run 的 route snapshot、checkpoint 与 stop_reason durable 写入 run journal
4. 允许之后通过 `runtime-resume` 沿用同一 journal 与同一 `grant_run_id` 重新进入

它当前**不**负责：

1. 自动修改 workspace
2. 自动推进到下一 stage 的写操作
3. 产出 artifact bundle
4. critique / revision autoloop 的真正写入执行
5. finalization / export

## Canonical CLI Surface

`R1.A` 一旦进入实现，只允许增加以下两个新的 `CLI-first` runtime commands：

1. `runtime-run`
   - 输入：`--input <workspace-json>`
   - 可选 durable output：`--journal <journal-json-path>`
   - 输出：本次 local runtime pass 的 machine-readable payload
2. `runtime-resume`
   - 输入：`--journal <journal-json-path>`
   - 输出：沿用 journal 中的 workspace input 与 `grant_run_id` 重新执行一次 local runtime pass 的 machine-readable payload

约束：

- 新命令仍属于 `CLI` formal entry，不新增第二 formal entry
- 旧五个 commands 继续作为 verifier / audit baseline
- `runtime-run` / `runtime-resume` 不能替代 `validate-workspace / summarize-workspace / next-step / critique-summary / stage-route-report`
- `MCP / controller` 继续属于 `not-yet-supported / future scope`

## Stop Reason Contract

`R1.A` 的 `stop_reason` 必须是 machine-readable object，最小字段集冻结为：

- `code`
- `reason`
- `current_stage`
- `recommended_next_stage`
- `checkpoint_status`
- `requires_human_confirmation`
- `forced_rollback_stage`
- `forced_rollback_reason`

冻结的最小 `code` vocabulary：

- `validation_failed`
- `rollback_required`
- `freeze_ready`
- `human_confirmation_required`
- `presubmission_frozen`
- `stage_action_required`

派生约束：

- `rollback_required`
  - 必须保留 `forced_rollback_stage / forced_rollback_reason`
- `freeze_ready`
  - 必须与 `verification_checkpoint.checkpoint_status=freeze_ready` 保持一致
- `presubmission_frozen`
  - 必须与 `verification_checkpoint.checkpoint_status=submission_frozen` 保持一致
- `stage_action_required`
  - 只能表达“当前 runtime 识别出下一 stage/action，但当前 slice 还未实现该写入动作”
- `validation_failed`
  - 必须 fail-closed，不得降级为自由文本说明

## Run Journal Contract

`R1.A` 的 durable run journal 必须是单个 machine-readable JSON 文件。它是本地 runtime state，不是 `.runtime-program/reports/**` 的替代物。

最小 durable surface 冻结为：

- `journal_version`
- `grant_run_id`
- `workspace_id`
- `input_path`
- `latest_stop_reason`
- `latest_route_report`
- `attempts`

其中每个 `attempt` 至少包含：

- `attempt_index`
- `trigger`（`runtime-run` 或 `runtime-resume`）
- `timestamp`
- `lifecycle_stage`
- `checkpoint_status`
- `stop_reason`

约束：

- journal 必须对同一 `grant_run_id` 连续回写
- journal 只能 durable 回写本地 runtime snapshot，不得冒充新的 `program_id` report surface
- 若 `--journal` 指向的现有文件与当前 `grant_run_id / workspace_id / input_path` 不一致，必须 fail-closed

## Resume Contract

`runtime-resume` 必须只依赖 journal 本身即可恢复：

1. 从 journal 读取 `input_path`
2. 重新运行同一条 `R1.A` local runtime pass
3. 继续沿用同一 `grant_run_id / workspace_id`
4. 在同一 journal 里 append 新 `attempt`

当前 `R1.A` 不要求：

- 跨机器同步 journal
- 从 `.runtime-program/**` 恢复产品 runtime
- 直接恢复到“下一 stage 已执行完”的写入后状态

## Relation To Existing Canonical Surfaces

`R1.A` 必须继续围绕以下 surfaces 聚合，不得重写它们的 canonical 语义：

- `validate-workspace`
- `summarize-workspace`
- `next-step`
- `critique-summary`
- `stage-route-report`
- `verification_checkpoint`
- `checkpoint_status`

更具体地说：

- `stage-route-report` 继续是 route / checkpoint aggregation 的 canonical baseline
- `runtime-run` 只是在其上增加 runtime entry、stop reason 与 journal
- `runtime-resume` 只是在 `runtime-run` 的 journal contract 上增加恢复入口

## Required Verification

### Activation Package Freeze Gate

在 `OMX` 允许进入 `R1.A` implementation 前，必须同时满足：

1. active `PRD / test-spec / implementation`、`CURRENT_PROGRAM` 与 reports 已显式引用本 activation package
2. `tests/test_program_control_surfaces.py` 已对本 activation package 的存在性与控制面对齐做出断言
3. baseline hard gate 继续全绿：
   - `python3 -m unittest discover -s tests -p 'test_*.py'`
   - 五个 canonical CLI surfaces 对五个 canonical workspaces 的 JSON 命令
   - `git diff --check`

### Implementation Promotion Gate

当 `R1.A` 进入实现时，必须补齐并通过以下新增验证：

1. `python3 -m unittest discover -s tests -p 'test_local_runtime.py'`
2. `PYTHONPATH=src python3 -m med_autogrant runtime run --input examples/nsfc_workspace_p2c_revision.json --journal "$TMPDIR/r1a-revision.json" --format json`
3. `PYTHONPATH=src python3 -m med_autogrant runtime run --input examples/nsfc_workspace_p3c_forced_rollback_argument.json --journal "$TMPDIR/r1a-rollback.json" --format json`
4. `PYTHONPATH=src python3 -m med_autogrant runtime run --input examples/nsfc_workspace_p3a_ready_for_submission.json --journal "$TMPDIR/r1a-freeze-ready.json" --format json`
5. `PYTHONPATH=src python3 -m med_autogrant runtime run --input examples/nsfc_workspace_p3c_presubmission_frozen.json --journal "$TMPDIR/r1a-frozen.json" --format json`
6. `PYTHONPATH=src python3 -m med_autogrant runtime resume --journal "$TMPDIR/r1a-revision.json" --format json`

这里的 `$TMPDIR` 指一个调用方显式提供的临时目录；`R1.A` 不得依赖 repo 内临时写入来通过验证。

## Promotion Invariants

- formal entry 继续固定为 `CLI`
- `MCP` 仍只是 future protocol layer，`controller` 仍只是 internal surface
- `grant_run_id / workspace_id / draft_id / program_id` 边界不得塌缩
- 旧五个 canonical CLI surfaces 继续作为 verifier / audit baseline
- `RevisionPlan.execution_status`、`pre_revision_version_label`、`post_revision_version_label`、`comparison_summary`、`frozen_question_id` 不得漂移
- `reviewed_revision_plan_id / reviewed_revision_evidence / source_critique_id / active_revision_plan_id` 不得漂移
- `forced_rollback_stage / forced_rollback_reason / presubmission_frozen` 不得漂移
- `verification_checkpoint / checkpoint_status` 不得被 run journal 或 stop reason 重写

## Enter-Implementation Preconditions

只有以下条件全部满足，才允许进入 `R1.A` implementation：

1. baseline hard gate 全绿
2. active `PRD / test-spec / implementation` 已写清楚 `runtime-run / runtime-resume / stop_reason / journal` 的最小合同
3. 继续推进不需要新的 formal entry、external credentials、web runtime、hosted runtime、same-repo HITL、second-family 或 federation truth

## Stop Conditions

若出现以下任一情况，必须停车：

- 识别到的“下一步”其实需要新的 public formal entry 或新的平台语义
- 必须新增 schema field 才能让 `R1.A` 成立
- 需要把 `.runtime-program/reports/**` 误写成产品 run journal
- 需要把 `runtime-run` 混写成 artifact writing、revision execution、export、web runtime 或 federation surface

## Excluded Scope

- artifact bundle / manifest / version export
- critique / revision autoloop 写入执行
- finalization / export package
- second-family / federation
- same-repo `Human-in-the-loop`
- `MCP / controller` public runtime surface
- hosted runtime / web runtime / remote session orchestration
