# P3.A Mentor Verdict Contract Freeze Current Truth

> 生命周期注记（`2026-05-20`）：这份 dated spec 已归档为 `historical_review_gate_provenance`。当前 verdict / review / quality 边界由核心五件套、AI-first quality active spec、contracts/schema/source 与 `contracts/runtime-program/current-program.json` 持有；本文只保留 2026-04-07 P3.A 形成过程，不再作为 current owner 或兼容接口依据。

Owner: `Med Auto Grant`
Purpose: `historical_review_gate_p3a_provenance`
State: `history`
Machine boundary: 本文是人读历史 spec，保留 2026-04-07 mentor verdict、route recommendation、review-gate audit surface 与 canonical examples 形成过程。当前 verdict/review/quality boundary、AI-first quality gate、OPL/Temporal runtime owner 与机器行为以核心五件套、AI-first quality active spec、`docs/specs/README.md`、`docs/specs/specs_lifecycle_map.md`、contracts、schemas、source、CLI/API 行为与 `contracts/runtime-program/current-program.json` 为准。

Date: `2026-04-07`

## 目标

在不改写 `grant_run_id`、formal entry、durability、`P2.B` argument-fit-outline contract 与 `P2.C` draft-critique-revision skeleton 的前提下，把 `P3.A / Mentor Verdict Contract Freeze` 的 verdict surface、route recommendation、audit surface 与 canonical examples 冻结成 repo-tracked current truth。

## 当前指针

- Current phase: `P3 / Mentor Critique And Revision Loop Hardening`
- Active tranche: `P3.A / Mentor Verdict Contract Freeze`
- Hard boundary docs:
  - `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-07-formal-entry-matrix-current-truth.md`
  - `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-07-durability-model-clarification.md`
  - `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-07-p2b-argument-fit-outline-mainline-current-truth.md`
  - `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-07-p2c-draft-critique-revision-skeleton-mainline-current-truth.md`

## Canonical Verdict Surface

`MentorCritique.verdict` 当前冻结四类 machine-readable verdict：

1. `major_reframe`
   - 含义：当前科学问题已不适合继续在同一 question 上局部修订。
   - route recommendation：`question_refinement`
   - 约束：这是回退到问题提纯的 verdict，不是继续执行 `revision` 的变体。
2. `major_revision`
   - 含义：继续保留当前 question / draft identity，但需要结构性重写。
   - route recommendation：`revision`
3. `minor_revision`
   - 含义：继续保留当前 question / draft identity，只做较小范围但仍结构化的修订。
   - route recommendation：`revision`
4. `ready_for_submission`
   - 含义：当前 authoring loop 已达到可进入送审前冻结的评审结论。
   - route recommendation：`frozen`
   - 边界：这里只冻结 verdict 语义与 route recommendation；真正的 `presubmission_frozen` gate 与 forced rollback 仍留给 `P3.C`。

## Canonical Objects

- `MentorCritique`
- `RevisionPlan`
- `ApplicationDraft`
- `NSFCWorkspace.current_selection`

## Canonical Route Contract

在 `critique / revision` 上下文中，`next-step`、`critique-summary` 与 `stage-route-report` 必须对 verdict 给出一致的 machine-readable route recommendation：

- `major_reframe -> question_refinement`
- `major_revision -> revision`
- `minor_revision -> revision`
- `ready_for_submission -> frozen`

其中：

- `major_reframe` 不得静默降级成 `revision`。
- `ready_for_submission` 当前只冻结为进入 `frozen` 的 transition boundary；不自动宣称 `P3.C` 或 submission-grade surface 已完成。
- `P2.C` 已冻结的 `revision(completed revised switch) -> critique` re-review boundary 继续保留，并作为 `ready_for_submission` verdict 的上游前提来源之一。

## Canonical Artifacts

### critique artifact

- 一个绑定当前 `draft_id` 的 `MentorCritique`
- `verdict`
- `overall_diagnosis`
- `current_scientific_question`
- `suggested_question`
- `logic_chain_repairs`
- `applicant_fit_repairs`
- `blocking_issues`

### verdict-linked revision artifact

- 一个绑定同一 `draft_id + critique_id` 的 `RevisionPlan`
- `major_reframe`
  - `items[]` 可以指向 `question_refinement` 所需的重塑动作
- `major_revision / minor_revision`
  - `items[]` 指向 revision 动作
- `ready_for_submission`
  - 允许保留同一 `RevisionPlan` 作为进入 `frozen` 前的 audit / handoff artifact
  - 但不在本 tranche 内把 `presubmission_frozen` 写成已完成 gate

## CLI / Runtime Audit Surface

当前正式 user-facing runtime entry 仍只有 `CLI`。

P3.A active commands：

- `validate-workspace`
- `summarize-workspace`
- `next-step`
- `critique-summary`
- `stage-route-report`

当前 audit contract：

- `summarize-workspace`
  - 必须继续稳定回显 `grant_run_id / workspace_id / current_selection / active_draft / active_revision_plan / active_critique`
- `critique-summary`
  - 必须稳定回显 `verdict` 与 `recommended_next_stage`
- `stage-route-report`
  - 必须把 `verdict` 分支的 route recommendation 聚合到同一 authoring report

## Canonical Examples

- `examples/nsfc_workspace_p2c_critique.json`
  - `major_revision -> revision`
- `examples/nsfc_workspace_p3a_major_reframe.json`
  - `major_reframe -> question_refinement`
- `examples/nsfc_workspace_p3a_ready_for_submission.json`
  - `ready_for_submission -> frozen`

## Retained Hard Boundary

以下合同继续保持，不因 `P3.A` 激活而漂移：

- `grant_run_id` 继续作为正式 execution handle
- formal entry 仍只有 `CLI`
- `MCP / controller` 仍是 `not-yet-supported / future scope`
- `P2.B` 的 `ArgumentChain / ApplicantFitMapping / ApplicationDraft.outline` 继续作为上游 canonical route
- `P2.C` 的 `drafting -> critique -> revision` skeleton 与 `RevisionPlan.execution_status / pre_revision_version_label / post_revision_version_label / comparison_summary` 继续作为上游 hard boundary

## Explicit Non-goals

- 不把 `ready_for_submission` 直接扩写成已完成的 `presubmission_frozen` gate
- 不在本 tranche 内实现 forced rollback
- 不在本 tranche 内重写 `revision` 版本切换合同
- 不扩 `MCP / controller` formal entry
- 不进入 `P4 / P5`
