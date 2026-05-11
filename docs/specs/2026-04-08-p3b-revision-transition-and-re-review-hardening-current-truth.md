# P3.B Revision Transition And Re-Review Hardening Current Truth

> Lifecycle note (`2026-05-11`): this dated spec is a path-stable history/support record unless `docs/specs/README.md`, `docs/specs/specs_lifecycle_map.md`, `docs/status.md`, or `contracts/runtime-program/current-program.json` explicitly names a still-current subsection. Read current MAG state from `docs/status.md`, the core five docs, and `contracts/runtime-program/current-program.json` first. Older `Current Truth`, Hermes, OPL Gateway, host-agent, or federation wording in this file is provenance, not the current default owner line.

Date: `2026-04-08`

## 目标

在不改写 `grant_run_id`、formal entry、durability、`P2.B` argument-fit-outline contract、`P2.C` draft-critique-revision skeleton 与已 absorbed `P3.A` mentor verdict contract 的前提下，把 `P3.B / Revision Transition And Re-Review Hardening` 的 re-review identity、revision evidence linkage、audit surface 与 canonical example 冻结成 repo-tracked current truth。

## 当前指针

- Current phase: `P3 / Mentor Critique And Revision Loop Hardening`
- Active tranche: `P3.B / Revision Transition And Re-Review Hardening`
- Hard boundary docs:
  - `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-07-formal-entry-matrix-current-truth.md`
  - `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-07-durability-model-clarification.md`
  - `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-07-p2b-argument-fit-outline-mainline-current-truth.md`
  - `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-07-p2c-draft-critique-revision-skeleton-mainline-current-truth.md`
  - `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-07-p3a-mentor-verdict-contract-freeze-current-truth.md`

## Canonical Re-Review Contract

`P3.B` 当前冻结的不是新的 formal entry，也不是新的 `current_selection` 总线，而是：

1. `current_selection.active_revision_plan_id`
   - 继续是当前 active revision route 的唯一 machine-readable pointer。
   - 当前 active critique 仍通过 `active_revision_plan_id -> critique_id` 推导，不新增 `active_critique_id`。
2. `MentorCritique.reviewed_revision_plan_id`
   - 当前 critique 若属于 re-review，必须显式引用上一轮已完成的 `RevisionPlan`。
   - 该字段不取代当前 active revision plan，只负责表达“这轮批注审阅的是哪一轮已完成修订证据”。
3. `reviewed_revision_evidence`
   - 由当前 critique 引用的上一轮 completed `RevisionPlan` 派生为 audit surface。
   - 当前必须稳定回显：`revision_plan_id`、`source_critique_id`、`execution_status`、`pre_revision_version_label`、`post_revision_version_label`、`comparison_summary`。

## Validation Contract

当以下条件同时成立时，允许 `lifecycle_stage=critique` 且当前 active draft 已是 `status=revised`：

- 当前 active `RevisionPlan.execution_status=planned`
- 当前 active `MentorCritique.reviewed_revision_plan_id` 非空
- 被引用的 `RevisionPlan` 存在
- 被引用的 `RevisionPlan.execution_status=completed`
- 被引用的 `RevisionPlan.draft_id` 与当前 active draft 一致
- 被引用的 `RevisionPlan.post_revision_version_label` 与当前 active draft `version_label` 一致

这条合同把“当前要执行的新修订计划”和“上一轮已完成修订证据”显式拆开，避免把两者压扁到同一个 active plan 上。

## Canonical Objects

- `ApplicationDraft`
- `MentorCritique`
- `RevisionPlan`
- `NSFCWorkspace.current_selection`

## current_selection Boundary

`P3.B` 继续保留 `P2.C` 的 `current_selection` 最小合同：

- `selected_direction_id`
- `selected_question_id`
- `active_fit_mapping_id`
- `active_draft_id`
- `active_revision_plan_id`

当前 tranche 的新收口点是：

- `current_selection` 不新增 `active_critique_id`
- 当前 active critique 继续由 active `RevisionPlan.critique_id` 推导
- re-review 证据通过 `MentorCritique.reviewed_revision_plan_id` 明确回指上一轮 completed `RevisionPlan`

## Canonical Artifacts

### current critique artifact

- 当前 active `MentorCritique`
- `verdict`
- `reviewed_revision_plan_id`
- `overall_diagnosis`
- `logic_chain_repairs`
- `applicant_fit_repairs`
- `blocking_issues`

### current revision artifact

- 当前 active `RevisionPlan`
- `critique_id` 回指当前 critique
- `execution_status=planned`
- `items[]`
- `next_review_focus[]`

### reviewed revision evidence artifact

- 上一轮 completed `RevisionPlan`
- `source_critique_id`
- `pre_revision_version_label`
- `post_revision_version_label`
- `comparison_summary`

## Canonical Route Contract

当前 `P3.B` 冻结的 route 是：

1. `revision(completed revised switch)`
2. `critique(re-review with reviewed_revision_plan_id)`
3. `revision(new active plan)`

其中：

- `major_reframe -> question_refinement` 与 `ready_for_submission -> frozen` 继续保留为 absorbed `P3.A` branch，不因 `P3.B` 激活而漂移。
- 当前 tranche 只把 `major_revision / minor_revision` 在 re-review 上下文中的 identity 与 evidence contract 收紧；不提前写成 `P3.C` 的 rollback 或 presubmission hard gate。

## CLI / Runtime Audit Surface

当前正式 user-facing runtime entry 仍只有 `CLI`。

当前 audit contract：

- `summarize-workspace`
  - 必须稳定回显 `active_critique.reviewed_revision_plan_id`
  - 必须新增顶层 `reviewed_revision_evidence`
- `critique-summary`
  - 必须稳定回显 `reviewed_revision_plan_id`
  - 必须新增 `reviewed_revision_evidence`
- `stage-route-report`
  - 必须聚合同一份 `reviewed_revision_evidence`
  - 必须同时保留当前 `revision_plan_id` 与上一轮 `reviewed_revision_plan_id`

## Canonical Examples

- `examples/nsfc_workspace_p2c_revision.json`
  - absorbed completed revision 边界
- `examples/nsfc_workspace_p3a_major_reframe.json`
  - absorbed `major_reframe -> question_refinement` branch
- `examples/nsfc_workspace_p3b_re_review_major_revision.json`
  - 当前 re-review major-revision branch
- `examples/nsfc_workspace_p3a_ready_for_submission.json`
  - absorbed `ready_for_submission -> frozen` branch

## Retained Hard Boundary

以下合同继续保持，不因 `P3.B` 激活而漂移：

- `grant_run_id` 继续作为正式 execution handle
- formal entry 仍只有 `CLI`
- `MCP / controller` 仍是 `not-yet-supported / future scope`
- `workspace_id`、`draft_id`、`program_id` 边界不变
- `P2.B` 的 `ArgumentChain / ApplicantFitMapping / ApplicationDraft.outline` 继续作为上游 canonical route
- `P2.C` 的 `RevisionPlan.execution_status / pre_revision_version_label / post_revision_version_label / comparison_summary` 继续作为 revision evidence baseline
- `P3.A` 的 `major_reframe / major_revision / minor_revision / ready_for_submission` verdict branch 继续作为当前 canonical verdict surface

## Explicit Non-goals

- 不进入 `P3.C`
- 不实现 forced rollback
- 不把 `ready_for_submission` 直接写成 `presubmission_frozen` hard gate
- 不扩 `MCP / controller` formal entry
- 不新增 `current_selection.active_critique_id`
- 不重写 `grant_run_id / workspace_id / draft_id / program_id` 的语义边界
