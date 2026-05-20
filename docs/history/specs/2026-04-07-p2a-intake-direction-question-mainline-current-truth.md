# P2.A Intake-Direction-Question Mainline Current Truth

> 生命周期注记（`2026-05-20`）：这份 dated spec 已归档为 `historical_authoring_flow_provenance`。当前 route truth、authoring pass 和 executor 边界由核心五件套、`docs/specs/README.md` 列出的 active specs、contracts/schema/source 与 `contracts/runtime-program/current-program.json` 持有；本文只保留 2026-04-07 P2.A 形成过程，不再作为 current owner 或兼容接口依据。

Date: `2026-04-07`

## 目标

在不改写 `grant_run_id`、formal entry、durability 边界的前提下，把 `P2.A / Intake-Direction-Question Mainline` 的 route、objects、artifacts 与 CLI/runtime transitions 冻结成 repo-tracked canonical surface。

## 当前指针

- Frozen in phase: `P2 / NSFC Authoring Mainline Freeze`
- Frozen tranche: `P2.A / Intake-Direction-Question Mainline`
- Current role under active mainline: upstream canonical boundary retained under `P3.B / Revision Transition And Re-Review Hardening`
- Hard boundary docs:
  - `docs/specs/2026-04-07-formal-entry-matrix-current-truth.md`
  - `docs/specs/2026-04-07-durability-model-clarification.md`

## Canonical Route

1. `input_intake`
2. `direction_screening`
3. `question_refinement`
4. current transition boundary: `question_refinement -> argument_building`

当前 tranche 只冻结这三段与到 `argument_building` 的 transition contract，不进入 `P2.B` 实现。

## Canonical Objects

### Upstream Intake Objects

- `ApplicantProfile`
- `TrackRecord`
- `ActiveProjectSet`
- `PreliminaryEvidencePack`
- `FundingOpportunityBrief`

### P2.A Core Objects

- `DirectionHypothesis[]`
- `ScientificQuestionCard[]`
- `NSFCWorkspace.current_selection`

## current_selection Contract

`current_selection` 是当前 P2.A 的显式选择句柄，当前冻结字段为：

- `selected_direction_id`
- `selected_question_id`
- `active_draft_id`
- `active_revision_plan_id`

阶段相关解释如下：

- `input_intake`
  - 允许空 `current_selection`
- `direction_screening`
  - 必须显式携带 `selected_direction_id`
  - 当前 direction 候选集保留 `2~5` 个 `DirectionHypothesis`
  - 必须且只能有一个 `decision_status=selected`
- `question_refinement`
  - 必须显式携带 `selected_direction_id + selected_question_id`
  - `selected_question_id` 必须回指当前方向下的 `ScientificQuestionCard`
- `active_draft_id / active_revision_plan_id`
  - 保留为 downstream identity 槽位
  - 不属于当前 P2.A hard gate

## Canonical Artifacts

### input_intake artifact

- intake snapshot
- 代表作数量、在研项目数量、预实验数量
- funding brief identity

### direction_screening artifact

- `2~5` 个 `DirectionHypothesis`
- 一个显式选中的 direction
- 每个方向的 `knowledge_gap_summary / applicant_fit_summary / risk_summary`

### question_refinement artifact

- 一个显式绑定到当前 direction 的 `ScientificQuestionCard`
- `knowledge_boundary`
- `unknown_mechanism`
- `falsifiable_statement`
- `proposed_breakthrough_angle`
- `current_selection.selected_direction_id`
- `current_selection.selected_question_id`

## CLI / Runtime Transition Contract

当前正式 user-facing runtime entry 仍只有 `CLI`。

P2.A active commands：

- `validate-workspace`
- `summarize-workspace`
- `next-step`
- `stage-route-report`

当前 transition truth：

- `input_intake -> direction_screening`
- `direction_screening -> question_refinement`
- `question_refinement -> argument_building`

`critique-summary` 仍是后段 workspace CLI surface；不是当前 P2.A hard gate。

## Downstream Exclusion Boundary

当前 P2.A runtime 不得无条件依赖以下对象：

- `ArgumentChain`
- `ApplicationDraft`
- `MentorCritique`
- `RevisionPlan`

这些对象继续保留在 schema / object model / future tranche map 中，但不作为当前 early-stage hard gate。

## Grant Run Boundary

- `grant_run_id`：当前正式 execution handle
- `workspace_id`：聚合根身份
- `draft_id`：草稿身份
- `program_id`：program / report routing 身份

这四类 ID 在 P2.A 内继续保持分离，不互相替代。

## Explicit Non-goals

- 不把 formal entry 扩成 `MCP / controller`
- 不进入 `P2.B / P2.C`
- 不做 verdict hardening、forced rollback、federation
- 不做 write / export / HITL skeleton
