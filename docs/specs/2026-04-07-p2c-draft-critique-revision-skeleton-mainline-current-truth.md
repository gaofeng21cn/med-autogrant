# P2.C Draft-Critique-Revision Skeleton Mainline Current Truth

Date: `2026-04-07`

## 目标

在不改写 `grant_run_id`、formal entry、durability 与 `P2.B` 已冻结 argument-fit-outline 合同的前提下，把 `P2.C / Draft-Critique-Revision Skeleton` 的 route、objects、artifacts 与 CLI/runtime audit surface 冻结成 repo-tracked canonical surface。

## 当前指针

- Frozen in phase: `P2 / NSFC Authoring Mainline Freeze`
- Frozen tranche: `P2.C / Draft-Critique-Revision Skeleton`
- Current role under active mainline: upstream canonical boundary retained under `P3.B / Revision Transition And Re-Review Hardening`
- Hard boundary docs:
  - `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-07-formal-entry-matrix-current-truth.md`
  - `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-07-durability-model-clarification.md`
  - `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-07-p2a-intake-direction-question-mainline-current-truth.md`
  - `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-07-p2b-argument-fit-outline-mainline-current-truth.md`

## Canonical Route

1. `drafting`
2. `critique`
3. `revision`
4. current re-review boundary: `revision(completed revised switch) -> critique`

当前 tranche 冻结这三段与 completed revision 回到 critique 的最小 route；更强的 `major_reframe / ready_for_submission / forced rollback / presubmission gate` 仍留给 `P3`。

## Canonical Objects

- `ApplicationDraft`
- `MentorCritique`
- `RevisionPlan`
- `NSFCWorkspace.current_selection`

## current_selection Contract

`current_selection` 在 P2.C 继续承担 upstream binding + downstream selection 句柄，当前冻结字段为：

- `selected_direction_id`
- `selected_question_id`
- `active_fit_mapping_id`
- `active_draft_id`
- `active_revision_plan_id`

阶段相关解释如下：

- `drafting`
  - 必须显式携带 `selected_direction_id + selected_question_id + active_fit_mapping_id + active_draft_id`
  - `active_draft_id` 必须回指当前 `status=draft` 的 `ApplicationDraft`
- `critique`
  - 必须继续显式携带上述四个 ID，并新增 `active_revision_plan_id`
  - 当前激活 `MentorCritique` 通过 `active_revision_plan_id -> critique_id` 推导，不新增 `active_critique_id`
- `revision`
  - 必须继续复用同一 `active_draft_id + active_revision_plan_id`
  - `draft_id` 仍保持单草稿身份，不因 revision 生成新的 draft identity

## Canonical Artifacts

### drafting artifact

- 一个 `status=draft` 的 `ApplicationDraft`
- `frozen_question_id`
- `outline[]`
- 非空 `sections[]`
- `sections[].linked_object_ids` 必须显式链接当前 `ScientificQuestionCard / ArgumentChain / ApplicantFitMapping`

### critique artifact

- 一个绑定到当前 `draft_id` 的 `MentorCritique`
- `overall_diagnosis`
- `current_scientific_question`
- `suggested_question`
- `verdict`
- `necessity_scientific_value / applicant_fit / feasibility`
- `logic_chain_repairs / applicant_fit_repairs / blocking_issues`
- 一个绑定到同一 `draft_id + critique_id` 的 `RevisionPlan`
- `items[]`
- `next_review_focus`

### revision artifact

- 同一 `draft_id` 上的 `RevisionPlan`
- `execution_status`
- `pre_revision_version_label`
- `post_revision_version_label`
- `comparison_summary`
- completed 时复用同一 `draft_id` 的 `ApplicationDraft.status=revised`

## CLI / Runtime Transition Contract

当前正式 user-facing runtime entry 仍只有 `CLI`。

P2.C active commands：

- `validate-workspace`
- `summarize-workspace`
- `next-step`
- `critique-summary`
- `stage-route-report`

当前 transition truth：

- `outline -> drafting`
- `drafting -> critique`
- `critique -> revision`
- `revision(completed revised switch) -> critique`

## Record / Audit Surface

- `summarize-workspace`
  - 必须稳定输出 `grant_run_id / workspace_id / current_selection / active_draft / active_revision_plan / active_critique`
  - `active_draft` 至少回显 `status / version_label / section_count`
- `critique-summary`
  - 必须稳定输出 `draft_id / critique_id / revision_plan_id / verdict / execution_status`
  - completed revision 时必须回显 `pre_revision_version_label / post_revision_version_label / comparison_summary`
- `stage-route-report`
  - drafting 阶段聚合 `validate-workspace + summarize-workspace + next-step`
  - critique / revision 阶段追加 `critique_summary`

## Retained Hard Boundary

以下合同继续保留，但不被扩写成新的 `P3` 语义：

- `grant_run_id` 继续作为正式 execution handle
- `outline_frozen=true` 仍是进入 `drafting` 的上游前提
- `RevisionPlan.execution_status` 是 revision 完成显式切换的唯一 gate
- `pre_revision_version_label`
- `post_revision_version_label`
- `comparison_summary`
- `draft_id`
- `frozen_question_id`
- `major_reframe / ready_for_submission / presubmission_frozen` 仍是 retained / future scope，不是当前 P2.C hard gate

## Explicit Non-goals

- 不进入 `P3`
- 不把 `major_reframe` 写成当前 tranche 必须收通的语义
- 不把 `ready_for_submission`、`frozen` 或 presubmission gate 写成当前 tranche hard gate
- 不扩 `MCP / controller` formal entry
- 不做 submission-facing write / export / HITL skeleton
