# R3.A Critique Revision Executor Surface Activation Package

Date: `2026-04-08`

## Activation Status

- Active phase: `Runtime Productization Program`
- Active tranche: `R3 / Critique Revision Autoloop`
- Active slice: `R3.A / Critique Revision Executor Surface`
- Status: `frozen / implementation pending`
- Upstream prerequisite:
  - `R1.A / Local Main Loop Entry And Stop Reason` 已 absorbed（freeze `38b5347`；implementation `8e087dc`）
  - `R1.B / Stage Action Executor Envelope` 已 absorbed（freeze `2b193da`；implementation `2953026`）
  - `R2.A / Artifact Bundle Production Surface` 已 absorbed（freeze `424ded0`；implementation `e8b9fe4`）
  - 当前 active hard gate 必须继续全绿

## Goal

在不改写 `CLI` formal entry、不把 `MCP / controller` 写成已支持 public runtime、不破坏 `grant_run_id / workspace_id / draft_id / program_id` 边界、也不把 author-side mainline 改写成 reviewer / HITL / hosted runtime 产品的前提下，冻结 `R3.A` 的首个 honest executor contract：

- 把当前 active `MentorCritique + RevisionPlan + ApplicationDraft` 收成一个 **CLI-first local revision execution pass**
- 让本地 runtime 第一次具备“围绕已有 critique / revision context 产生 revised workspace candidate”的 author-side 机器可读执行面
- 把 `reviewed_revision_plan_id / reviewed_revision_evidence / source_critique_id / active_revision_plan_id / pre_revision_version_label / post_revision_version_label / comparison_summary / forced_rollback_stage / presubmission_frozen` 保持在同一个 durable workspace mutation contract 内

这里冻结的不是“已经有 critique synthesis / web runtime / hosted runtime”的事实，而是：

- `R3.A` 的第一棒只允许打开 **revision-side executor**
- 新的 critique synthesis / re-review critique generation 仍属于 `R3.A` 内后续 bounded slice，不在这次 activation package 里偷跑
- final export / freeze manifest / hostedization 继续留在 `R4 / R5`

这里的 formal-entry 口径继续固定为：

- `CLI`：当前唯一 formal entry
- `MCP`：future protocol layer / `not-yet-supported`
- `controller`：internal surface / `not-yet-supported` public formal entry

## Hard Boundary Docs

必须同时服从：

- `/Users/gaofeng/workspace/med-autogrant/AGENTS.md`
- `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-08-runtime-first-productization-program.md`
- `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-08-runtime-first-r1-to-r5-boundary-map.md`
- `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-07-p2c-draft-critique-revision-skeleton-mainline-current-truth.md`
- `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-07-p3a-mentor-verdict-contract-freeze-current-truth.md`
- `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-08-p3b-revision-transition-and-re-review-hardening-current-truth.md`
- `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-08-p3c-forced-rollback-and-presubmission-gate-current-truth.md`
- `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-07-formal-entry-matrix-current-truth.md`
- `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-07-durability-model-clarification.md`
- `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-09-r3a-machine-applicable-revision-mutation-contract.md`

## Object Boundary

`R3.A` 当前冻结的对象边界是一个 **CLI-first local revision execution write pass**：

1. 从当前 workspace 的 `current_selection` 中定位：
   - `selected_direction_id`
   - `selected_question_id`
   - `active_fit_mapping_id`
   - `active_draft_id`
   - `active_revision_plan_id`
2. 读取当前 canonical objects：
   - 当前 active `ApplicationDraft`
   - 当前 active `RevisionPlan`
   - 当前 active `MentorCritique`
   - `reviewed_revision_plan_id`（若存在）
   - `reviewed_revision_evidence`（若存在）
3. 只在以下前提下允许进入 revision-side executor：
   - 当前 active `MentorCritique.verdict` 属于 `major_revision / minor_revision`
   - 当前 active `RevisionPlan.execution_status=planned`
   - `forced_rollback_stage` 为空
   - `presubmission_frozen=false`
4. 把结果写成 machine-readable local revised workspace candidate

这意味着：

- `R3.A` 第一棒只允许执行 revision-side pass
- `R3.A` 不允许在这次 activation package 里把 critique synthesis、final export、hosted session boundary 混写进来
- `R3.A` 产物必须仍是 author-side workspace candidate，而不是 reviewer surface 或 submission package

## Canonical CLI Surface

`R3.A` 一旦进入实现，只允许先新增一个 `CLI-first` 本地 revision executor 命令：

1. `execute-revision-pass`
   - 输入：`--input <workspace-json>`
   - 输出路径：`--output <workspace-json-path>`
   - 输出：本次 revision execution 的 machine-readable payload

约束：

- 新命令仍属于 `CLI` formal entry，不新增第二 formal entry
- 旧五个 commands、`runtime-run / runtime-resume` 与 `build-artifact-bundle` 继续作为 verifier / audit baseline
- `execute-revision-pass` 不得替代 `validate-workspace / summarize-workspace / next-step / critique-summary / stage-route-report`
- `execute-revision-pass` 只写 revised workspace candidate output，不写 `.runtime-program/**`

## Revision Executor Contract

`R3.A` 当前最小 durable surface 冻结为：

- `grant_run_id`
- `workspace_id`
- `draft_id`
- `lifecycle_stage`
- `revision_execution`
  - `active_revision_plan_id`
  - `reviewed_revision_plan_id`
  - `source_critique_id`
  - `reviewed_revision_evidence`
  - `pre_revision_version_label`
  - `post_revision_version_label`
  - `comparison_summary`
- `revised_workspace`

冻结语义：

- `draft_id` 必须继续沿用当前 active `ApplicationDraft`
- `frozen_question_id` 必须继续沿用同一冻结问题，不得因 revision 变更
- `post_revision_version_label` 必须不同于 `pre_revision_version_label`
- `comparison_summary` 必须是 revision execution 的 machine-readable evidence，不得为空
- 当 `reviewed_revision_plan_id / reviewed_revision_evidence` 已存在时，新的 revision execution 不得覆盖或混写上一轮 re-review linkage / evidence
- 当 `forced_rollback_stage` 存在、或 `ready_for_submission + presubmission_frozen` 已进入冻结门时，`execute-revision-pass` 必须 fail-closed，而不是伪装继续执行

## Machine-Applicable Mutation Contract

`R3.A` 当前不再允许依赖未冻结的 authoring semantics。

进入 implementation 时，active `RevisionPlan.items[]` 必须满足：

- 只允许 section-level executable subset
- 每个 executable item 都显式携带 `mutation_payload`
- mutation 目标必须与当前 active `ApplicationDraft.sections[].section_key` 精确匹配
- 同一轮 execution 不允许 duplicate target section

精确语义以以下文档为准：

- `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-09-r3a-machine-applicable-revision-mutation-contract.md`

## Local Output Contract

`R3.A` 的本地 output 只能是调用方显式提供的 revised workspace path：

- `--output <workspace-json-path>` 为必填
- 若 output 已存在且其 `grant_run_id / workspace_id / draft_id / active_revision_plan_id` 与当前不一致，必须 fail-closed
- revised workspace output 是产品 runtime 的本地 durable artifact，不替代 `.runtime-program/reports/**`

## Relation To Existing Canonical Surfaces

`R3.A` 必须继续围绕以下 surfaces 聚合，不得重写它们的 canonical 语义：

- `validate-workspace`
- `summarize-workspace`
- `next-step`
- `critique-summary`
- `stage-route-report`
- `runtime-run`
- `runtime-resume`
- `build-artifact-bundle`
- `verification_checkpoint`
- `checkpoint_status`

关系冻结如下：

- `stage-route-report` 继续是 route / checkpoint aggregation 的 canonical baseline
- `runtime-run / runtime-resume / stage_action_envelope` 继续只处理 runtime orchestration
- `build-artifact-bundle` 继续只打包当前对象，不执行 revision mutation
- `execute-revision-pass` 只负责 revision-side workspace mutation contract，不覆盖 checkpoint / stop reason / artifact bundle semantics

## Required Verification

### Activation Package Freeze Gate

在 `OMX` 允许进入 `R3.A` implementation 前，必须同时满足：

1. active `CURRENT_PROGRAM / PRD / test-spec / implementation / reports` 已显式指向本 activation package
2. `tests/test_program_control_surfaces.py` 已对本 activation package 的存在性与控制面对齐做出断言
3. baseline hard gate 继续全绿：
   - `python3 -m unittest discover -s tests -p 'test_*.py'`
   - `python3 -m unittest discover -s tests -p 'test_program_control_surfaces.py'`
   - `python3 -m unittest discover -s tests -p 'test_local_runtime.py'`
   - 当前 canonical CLI examples（旧五个 surfaces + `runtime-run / runtime-resume` + `build-artifact-bundle`）
   - `git diff --check`

### Implementation Promotion Gate

当 `R3.A` 进入实现时，必须补齐并通过以下新增验证：

1. 新的 revision executor contract regression tests
2. `draft_id / frozen_question_id / pre_revision_version_label / post_revision_version_label / comparison_summary` 一致性 tests
3. `reviewed_revision_plan_id / reviewed_revision_evidence / source_critique_id / active_revision_plan_id` 保留 tests，以及 `forced_rollback_stage / presubmission_frozen` fail-closed tests
4. `mutation_payload / target_ref / section_key` 对齐 tests
5. `PYTHONPATH=src python3 -m med_autogrant execute-revision-pass --input examples/nsfc_workspace_p2c_critique.json --output "$TMPDIR/r3a-p2c-revised.json" --format json`
6. `PYTHONPATH=src python3 -m med_autogrant execute-revision-pass --input examples/nsfc_workspace_p3b_re_review_major_revision.json --output "$TMPDIR/r3a-p3b-revised.json" --format json`
7. `git diff --check`

## Promotion Invariants

- 不得改写 `grant_run_id / workspace_id / draft_id / program_id`
- 不得改写 `frozen_question_id`
- 不得在 revision executor 阶段生成 final package / freeze manifest / export summary
- 不得新增 `MCP / controller` formal entry
- 不得把 revised workspace output 写成 `.omx` control-plane report
- 不得把 same-repo HITL、reviewer surface 或 hosted runtime 偷写成 `R3.A`

## Enter-Implementation Preconditions

只有以下条件全部满足，才允许进入 `R3.A` implementation：

1. `R1.A / R1.B / R2.A` 已 absorbed
2. active `CURRENT_PROGRAM / PRD / test-spec / implementation / reports` 已把 `R3.A` 写成当前 active next slice
3. 这次新增能力仍然只属于 critique/revision executor，而不是 final export / hostedization / `P5`
4. `RevisionPlan.items[].mutation_payload` 的 repo-tracked contract 已冻结，且 current executable examples 已对齐
5. 当前 baseline hard gate 继续全绿

## Stop Conditions

以下情况出现时，必须诚实停车：

- 当前看似要做的能力其实已经需要 final export / freeze manifest / hosted-friendly session contract
- 必须改写 formal entry、`MCP`、`controller`、或 `P5` 才能让 `R3.A` 成立
- 必须依赖未冻结的 mutation semantics、仓外 authoring engine、或 repo-未验证的外部 runtime 语义，才能让 revision executor 成立
- 必须把 critique synthesis / reviewer decision / hosted runtime 混入第一棒 revision-side executor，才能让这一 tranche 继续

## Excluded Scope

- 新 critique synthesis
- final package / freeze manifest / export summary
- hostedization
- second-family / federation
- same-repo HITL
