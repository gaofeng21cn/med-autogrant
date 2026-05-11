# R1.B Stage Action Executor Envelope Activation Package

> Lifecycle note (`2026-05-11`): this dated spec is a path-stable history/support record unless `docs/specs/README.md`, `docs/specs/specs_lifecycle_map.md`, `docs/status.md`, or `contracts/runtime-program/current-program.json` explicitly names a still-current subsection. Read current MAG state from `docs/status.md`, the core five docs, and `contracts/runtime-program/current-program.json` first. Older `Current Truth`, Hermes, OPL Gateway, host-agent, or federation wording in this file is provenance, not the current default owner line.

Date: `2026-04-08`

## Activation Status

- Active phase: `Runtime Productization Program`
- Active tranche: `R1 / Autonomous Main Loop`
- Active slice: `R1.B / Stage Action Executor Envelope`
- Status: `frozen / implementation pending`
- Upstream prerequisite:
  - `R1.A / Local Main Loop Entry And Stop Reason` 已 absorbed（freeze `38b5347`；implementation `8e087dc`）
  - 当前 active hard gate 必须继续全绿

## Goal

在不改写 `CLI` formal entry、不把 `MCP / controller` 写成已支持 public runtime、不破坏 `grant_run_id / workspace_id / draft_id / program_id` 边界、也不把 author-side mainline 改写成 reviewer / HITL / hosted runtime 产品的前提下，冻结 `R1.B` 的最小实现合同：

- 把 `runtime-run` 已得到的 `stage_action_required` 类 stop reason 收紧成 machine-readable `stage_action_envelope`
- 让 runtime 对“下一动作是什么”形成稳定、结构化、可恢复的执行 envelope
- 把 envelope durable 写入当前 run journal，供后续 `runtime-resume` 与 runtime orchestration 使用

这里的 formal-entry 口径继续固定为：

- `CLI`：当前唯一 formal entry
- `MCP`：future protocol layer / `not-yet-supported`
- `controller`：internal surface / `not-yet-supported` public formal entry

`R1.B` 当前冻结的不是“已经执行 stage action”的事实，而是：

- 对 `stage_action_required` 的 machine-readable envelope contract
- 对 runtime route continuation / journal append / resume decision 的最小 durable surface
- 对 `R1` 与 `R2 / R3 / R4 / R5` 的 object boundary

## Hard Boundary Docs

必须同时服从：

- `/Users/gaofeng/workspace/med-autogrant/AGENTS.md`
- `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-08-runtime-first-productization-program.md`
- `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-08-runtime-first-r1-to-r5-boundary-map.md`
- `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-08-r1a-local-main-loop-entry-and-stop-reason-activation-package.md`
- `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-08-p4b-verification-os-and-checkpoint-surface-current-truth.md`

## Object Boundary

`R1.B` 冻结的对象边界是一个 **runtime-only stage action envelope pass**：

1. 从现有 `runtime-run / runtime-resume` 产出的 `route_report + stop_reason` 中识别 `stage_action_required`
2. 仅在 `stop_reason.code=stage_action_required` 时派生 machine-readable `stage_action_envelope`
3. 把 envelope 与当前 run journal append 绑定，使恢复与后续编排有稳定 durable surface
4. 不执行任何 stage action 本身，不生成新的 artifact，不改写 workspace 内容对象

这意味着：

- `R1.B` 只允许结构化“应该做什么”
- `R1.B` 不允许实际去做“把内容写出来 / 改出来 / 导出来”

## Canonical CLI Surface

`R1.B` 一旦进入实现，只允许扩展现有两个 `CLI-first` runtime commands 的输出：

1. `runtime-run`
2. `runtime-resume`

允许新增的 surface 仅限：

- payload 内新增 `stage_action_envelope`
- run journal 内新增 `latest_stage_action_envelope`
- 当前 attempt 内新增 `stage_action_envelope`

不允许新增新的 public command。

## Stage Action Envelope Contract

`R1.B` 的 `stage_action_envelope` 必须是 machine-readable object；最小字段集冻结为：

- `envelope_version`
- `status`
- `grant_run_id`
- `workspace_id`
- `draft_id`
- `current_stage`
- `recommended_next_stage`
- `checkpoint_status`
- `requires_human_confirmation`
- `selection`
  - `selected_direction_id`
  - `selected_question_id`
  - `active_fit_mapping_id`
  - `active_draft_id`
  - `active_revision_plan_id`
- `action_items`
  - 每项都必须包含：
    - `index`
    - `instruction`
- `route_reason`
- `resume_decision`
  - `command`
  - `journal_path`
  - `append_attempt`
  - `reuse_grant_run_id`

冻结语义：

- `status` 当前固定为 `action_required`
- `draft_id` 必须来自 `verification_checkpoint.identity.draft_id`
- `selection` 必须来自当前 workspace 的 `current_selection`
- `action_items` 只能结构化 `next-step.actions`，不得发明新的执行内容
- `resume_decision.command` 当前固定为 `runtime-resume`
- `resume_decision.append_attempt` 当前固定为 `true`
- `resume_decision.reuse_grant_run_id` 当前固定为 `true`

## Journal Contract

`R1.B` 的 durable run journal 必须在 `R1.A` 既有 surface 之上追加：

- `latest_stage_action_envelope`

并要求每个 attempt 允许记录：

- `stage_action_envelope`

冻结语义：

- 只有当 `stop_reason.code=stage_action_required` 时，`latest_stage_action_envelope` 与 attempt 级 `stage_action_envelope` 才允许为 object
- 其他 stop reason 下必须显式为 `null`
- `latest_stage_action_envelope` 不能替代 `latest_stop_reason` 或 `latest_route_report`

## Relation To Existing Canonical Surfaces

`R1.B` 必须继续围绕以下 surfaces 聚合，不得重写它们的 canonical 语义：

- `validate-workspace`
- `summarize-workspace`
- `next-step`
- `critique-summary`
- `stage-route-report`
- `verification_checkpoint`
- `checkpoint_status`
- `stop_reason`
- `run journal`

关系冻结如下：

- `stage-route-report` 继续是 route / checkpoint aggregation 的 canonical baseline
- `stop_reason` 继续表达“为什么停”
- `stage_action_envelope` 只补充表达“当前可恢复地应该做什么”
- `stage_action_envelope` 不能覆盖 `stop_reason`、也不能覆盖 `verification_checkpoint`

## Required Verification

### Activation Package Freeze Gate

在 `OMX` 允许进入 `R1.B` implementation 前，必须同时满足：

1. `python3 -m unittest discover -s tests -p 'test_program_control_surfaces.py'`
2. `python3 -m unittest discover -s tests -p 'test_*.py'`
3. 当前 active test spec 中列出的 canonical CLI examples
4. `git diff --check`

### Implementation Promotion Gate

当 `R1.B` 进入实现时，必须补齐并通过以下新增验证：

1. `python3 -m unittest discover -s tests -p 'test_local_runtime.py'`
2. revision canonical example 必须证明 `stage_action_required` 会生成 `stage_action_envelope`
3. critique-major-revision canonical example 必须证明 `stage_action_required` 会生成 `stage_action_envelope`
4. rollback / freeze-ready / presubmission-frozen canonical examples 必须证明 `stage_action_envelope` 为 `null`
5. `runtime-resume` 必须证明 envelope 可随 journal 继续 durable 回写

## Promotion Invariants

- 不生成新的方向、问题、论证链、提纲、草稿内容
- 不执行 critique / revision 内容改写
- 不改变 `ApplicationDraft` 内容层对象
- `grant_run_id / workspace_id / draft_id / program_id` 边界不漂移
- `verification_checkpoint / checkpoint_status` 不得被 `stage_action_envelope` 覆盖
- `RevisionPlan.execution_status / pre_revision_version_label / post_revision_version_label / comparison_summary / frozen_question_id` 不漂移
- `reviewed_revision_plan_id / reviewed_revision_evidence / source_critique_id / active_revision_plan_id` 不漂移
- `forced_rollback_stage / forced_rollback_reason / presubmission_frozen` 不漂移

## Enter-Implementation Preconditions

只有以下条件全部满足，才允许进入 `R1.B` implementation：

1. `R1.A` 已 absorbed
2. active `CURRENT_PROGRAM / PRD / test-spec / implementation / reports` 已写清楚 `R1.B` 是当前 active next slice
3. 这次新增能力仍然只属于 runtime execution envelope，而不是 artifact writing / revision execution / final export / hostedization
4. 当前 baseline hard gate 继续全绿

## Stop Conditions

以下情况出现时，必须诚实停车：

- 当前看似要做的能力其实已经需要生成或更新 artifact 内容
- 当前看似要做的能力其实已经需要执行 critique / revision / re-review
- 当前看似要做的能力其实已经需要 final export / hosted-friendly session contract
- 必须改写 formal entry、`MCP`、`controller`、或 `P5` 才能让 `R1.B` 成立

## Excluded Scope

- artifact writing
- revision execution
- final export
- hostedization
- second-family / federation
- same-repo HITL
