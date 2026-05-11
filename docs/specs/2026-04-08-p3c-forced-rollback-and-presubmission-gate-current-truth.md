# P3.C Forced Rollback And Presubmission Gate Current Truth

> Lifecycle note (`2026-05-11`): this dated spec is a path-stable history/support record unless `docs/specs/README.md`, `docs/specs/specs_lifecycle_map.md`, `docs/status.md`, or `contracts/runtime-program/current-program.json` explicitly names a still-current subsection. Read current MAG state from `docs/status.md`, the core five docs, and `contracts/runtime-program/current-program.json` first. Older `Current Truth`, Hermes, OPL Gateway, host-agent, or federation wording in this file is provenance, not the current default owner line.

Date: `2026-04-08`

## 目标

在不改写 `grant_run_id`、formal entry、durability、已 absorbed `P2.A / P2.B / P2.C / P3.A / P3.B` 合同的前提下，把 `P3.C / Forced Rollback And Presubmission Gate` 的强制回退条件、`ready_for_submission -> frozen` hard gate、route recommendation、validation surface 与 canonical examples 冻结成 repo-tracked current truth。

## 当前指针

- Current phase: `P3 / Mentor Critique And Revision Loop Hardening`
- Active tranche: `P3.C / Forced Rollback And Presubmission Gate`
- Hard boundary docs:
  - `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-07-formal-entry-matrix-current-truth.md`
  - `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-07-durability-model-clarification.md`
  - `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-07-p2b-argument-fit-outline-mainline-current-truth.md`
  - `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-07-p2c-draft-critique-revision-skeleton-mainline-current-truth.md`
  - `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-07-p3a-mentor-verdict-contract-freeze-current-truth.md`
  - `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-08-p3b-revision-transition-and-re-review-hardening-current-truth.md`

## Canonical Forced Rollback Contract

`P3.C` 新冻结的不是新的 formal entry，而是 `MentorCritique` 上对“不能继续局部修订”这一判断的 machine-readable 收口：

1. `MentorCritique.forced_rollback_stage`
   - 可选字段；若存在，当前 critique 不得继续按局部 `revision` 前进，而必须回退到更早的 authoring stage。
   - 允许值：
     - `direction_screening`
     - `question_refinement`
     - `argument_building`
     - `fit_alignment`
2. `MentorCritique.forced_rollback_reason`
   - 当 `forced_rollback_stage` 存在时必须非空。
   - 它回答“为什么当前 loop 必须回退”，而不是继续局部润色。
3. `RevisionPlan.items[]`
   - 继续保留为执行 artifact。
   - 但当 `forced_rollback_stage` 存在时，计划内容必须与回退目标同轴，而不是伪装成局部 rewrite。

## Rollback Target / Verdict Boundary

`forced_rollback_stage` 与已 absorbed `P3.A` verdict contract 的边界固定如下：

- `direction_screening`
  - 仅允许与 `verdict=major_reframe` 组合出现
  - 语义：当前方向本身已不足以承载科学问题，必须回到方向筛选
- `question_refinement`
  - 仅允许与 `verdict=major_reframe` 组合出现
  - 语义：当前核心科学问题不成立，必须回到问题提纯
- `argument_building`
  - 仅允许与 `verdict=major_revision` 组合出现
  - 语义：问题可保留，但立项依据/必要性链条已失真，必须回到论证主链重建
- `fit_alignment`
  - 仅允许与 `verdict=major_revision` 组合出现
  - 语义：问题可保留，但申请人适配度或关键证据链不能靠局部改写补平，必须回到适配度重建

若 `forced_rollback_stage` 缺失，则仍沿用 absorbed `P3.A / P3.B` 的默认 route：

- `major_reframe -> question_refinement`
- `major_revision / minor_revision -> revision`
- `ready_for_submission -> frozen`

## Presubmission Hard Gate Contract

`P3.C` 把 `ready_for_submission -> frozen` 从 transition boundary 收紧成 hard gate：

进入 `lifecycle_stage=frozen` 时，必须同时满足：

1. `gates.presubmission_frozen=true`
2. 当前 active `MentorCritique.verdict=ready_for_submission`
3. 当前 active `MentorCritique.forced_rollback_stage` 为空
4. 当前 active `ApplicationDraft.status=frozen`
5. 当前 active `RevisionPlan.execution_status=completed`
6. 当前 active `RevisionPlan.post_revision_version_label` 与 frozen draft `version_label` 一致
7. 当前 active critique 的：
   - `blocking_issues=[]`
   - `necessity_scientific_value.blocking_issues=[]`
   - `applicant_fit.blocking_issues=[]`
   - `feasibility.blocking_issues=[]`

这里冻结的是 presubmission hard gate，不等于已经进入 submission-facing external surface。

## Canonical Route Contract

当前 `P3.C` 冻结以下 route：

1. `critique(major_reframe + forced_rollback_stage=direction_screening) -> direction_screening`
2. `critique(major_reframe + forced_rollback_stage=question_refinement) -> question_refinement`
3. `critique(major_revision + forced_rollback_stage=argument_building) -> argument_building`
4. `critique(major_revision + forced_rollback_stage=fit_alignment) -> fit_alignment`
5. `critique(ready_for_submission) -> frozen`
6. `frozen(presubmission hard gate satisfied) -> frozen`

其中：

- `minor_revision` 不得携带 `forced_rollback_stage`
- `ready_for_submission` 不得携带 `forced_rollback_stage`
- `frozen` 阶段只表示 presubmission 版本已冻结，不等于 submission-grade autopilot 已完成

## Canonical Objects

- `MentorCritique`
- `RevisionPlan`
- `ApplicationDraft`
- `NSFCWorkspace.current_selection`

## Canonical Artifacts

### forced rollback critique artifact

- 当前 active `MentorCritique`
- `verdict`
- `forced_rollback_stage`
- `forced_rollback_reason`
- `blocking_issues`

### rollback-aligned revision artifact

- 当前 active `RevisionPlan`
- `critique_id` 回指当前 critique
- `items[]`
- `next_review_focus[]`

### presubmission frozen artifact

- 当前 active `ApplicationDraft.status=frozen`
- `gates.presubmission_frozen=true`
- 当前 active `RevisionPlan.execution_status=completed`
- 当前 active `MentorCritique.verdict=ready_for_submission`

## CLI / Runtime Audit Surface

当前正式 user-facing runtime entry 仍只有 `CLI`。

当前 audit contract：

- `summarize-workspace`
  - 必须继续稳定回显 `grant_run_id / workspace_id / current_selection / active_draft / active_revision_plan / active_critique`
  - 必须新增 `active_critique.forced_rollback_stage`
  - 必须新增 `active_critique.forced_rollback_reason`
  - 必须稳定回显 `gates.presubmission_frozen`
- `critique-summary`
  - 必须新增 `forced_rollback_stage`
  - 必须新增 `forced_rollback_reason`
  - 必须新增 `presubmission_frozen`
- `stage-route-report`
  - 必须聚合 forced rollback route recommendation
  - 必须聚合 `presubmission_frozen`
  - 必须新增 `verification_checkpoint`
  - 必须新增 `checkpoint_status`
  - `verification_checkpoint` 内必须继续聚合 reviewed revision evidence、forced rollback 与 frozen gate 语义

## Canonical Examples

- `examples/nsfc_workspace_p3b_re_review_major_revision.json`
  - absorbed `P3.B` re-review major-revision branch
- `examples/nsfc_workspace_p3c_forced_rollback_argument.json`
  - `major_revision + forced_rollback_stage=argument_building`
- `examples/nsfc_workspace_p3c_presubmission_frozen.json`
  - `ready_for_submission + presubmission_frozen=true + lifecycle_stage=frozen`

## Retained Hard Boundary

以下合同继续保持，不因 `P3.C` 激活而漂移：

- `grant_run_id` 继续作为正式 execution handle
- formal entry 仍只有 `CLI`
- `MCP / controller` 仍是 `not-yet-supported / future scope`
- `workspace_id`、`draft_id`、`program_id` 边界不变
- `P2.B` 的 `ArgumentChain / ApplicantFitMapping / ApplicationDraft.outline` 继续作为上游 canonical route
- `P2.C` 的 `drafting -> critique -> revision` skeleton 与 revision evidence baseline 继续保留
- `P3.A` 的 verdict vocabulary 不扩成新的 reviewer-owned surface
- `P3.B` 的 `reviewed_revision_plan_id / reviewed_revision_evidence / source_critique_id / active_revision_plan_id` 不漂移

## Explicit Non-goals

- 不进入 `P4`
- 不扩 `MCP / controller` formal entry
- 不实现 submission-facing write / export / HITL external surface
- 不宣称 managed web runtime 已完成
- 不把控制面成熟度写成产品 runtime 已成熟
