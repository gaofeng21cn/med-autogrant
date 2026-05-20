# P2.B Argument-Fit-Outline Mainline Current Truth

> 生命周期注记（`2026-05-20`）：这份 dated spec 已归档为 `historical_authoring_flow_provenance`。当前 argument / outline route truth 由核心五件套、`docs/specs/README.md` 列出的 active specs、contracts/schema/source 与 `contracts/runtime-program/current-program.json` 持有；本文只保留 2026-04-07 P2.B 形成过程，不再作为 current owner 或兼容接口依据。

Date: `2026-04-07`

## 目标

在不改写 `grant_run_id`、formal entry、durability 边界与 `P2.A` upstream binding 的前提下，把 `P2.B / Argument-Fit-Outline Mainline` 的 route、objects、artifacts 与 CLI/runtime transitions 冻结成 repo-tracked canonical surface。

## 当前指针

- Frozen in phase: `P2 / NSFC Authoring Mainline Freeze`
- Frozen tranche: `P2.B / Argument-Fit-Outline Mainline`
- Current role under active mainline: upstream canonical boundary retained under `P3.B / Revision Transition And Re-Review Hardening`
- Hard boundary docs:
  - `docs/specs/2026-04-07-formal-entry-matrix-current-truth.md`
  - `docs/specs/2026-04-07-durability-model-clarification.md`
  - `docs/specs/2026-04-07-p2a-intake-direction-question-mainline-current-truth.md`

## Canonical Route

1. `argument_building`
2. `fit_alignment`
3. `outline`
4. current transition boundary: `outline -> drafting`

当前 tranche 只冻结这三段与到 `drafting` 的 transition contract，不进入 `P2.C` 实现。

## Canonical Objects

- `ArgumentChain`
- `ApplicantFitMapping`
- `ApplicationDraft`
- `NSFCWorkspace.current_selection`

## current_selection Contract

`current_selection` 在 P2.B 继续承担 upstream binding + downstream selection 句柄，当前冻结字段为：

- `selected_direction_id`
- `selected_question_id`
- `active_fit_mapping_id`
- `active_draft_id`
- `active_revision_plan_id`

阶段相关解释如下：

- `argument_building`
  - 必须显式携带 `selected_direction_id + selected_question_id`
- `fit_alignment`
  - 必须显式携带 `selected_direction_id + selected_question_id + active_fit_mapping_id`
  - `active_fit_mapping_id` 必须回指当前问题下唯一激活的 `ApplicantFitMapping`
- `outline`
  - 必须显式携带 `selected_direction_id + selected_question_id + active_fit_mapping_id + active_draft_id`
  - `active_draft_id` 必须回指当前 `status=outline` 的 `ApplicationDraft`
- `active_revision_plan_id`
  - 保留为 downstream identity 槽位
  - 不属于当前 P2.B hard gate

## Canonical Artifacts

### argument_building artifact

- 一个显式绑定到 `selected_question_id` 的 `ArgumentChain`
- `background_claim`
- `field_gap`
- `necessity_claim`
- `uniqueness_claim`
- `route_justification`
- `non_arbitrary_route_reason`
- `if_not_done_loss`

### fit_alignment artifact

- 一个显式绑定到 `selected_question_id + argument_chain_id` 的 `ApplicantFitMapping`
- `applicant_fit_summary`
- `unique_advantage`
- `methods_readiness`
- `resource_readiness`
- `risk_mitigation`
- `linked_evidence_ids`

### outline artifact

- 一个 `status=outline` 的 `ApplicationDraft`
- `frozen_question_id`
- `outline[]`
- 每个关键 section 的 `linked_object_ids`
- 至少显式链接当前 `ScientificQuestionCard / ArgumentChain / ApplicantFitMapping`

## CLI / Runtime Transition Contract

当前正式 user-facing runtime entry 仍只有 `CLI`。

P2.B active commands：

- `validate-workspace`
- `summarize-workspace`
- `next-step`
- `stage-route-report`

当前 transition truth：

- `question_refinement -> argument_building`
- `argument_building -> fit_alignment`
- `fit_alignment -> outline`
- `outline -> drafting`

`critique-summary` 仍是后段 workspace CLI surface；不是当前 P2.B hard gate。

## Outline Freeze Contract

- `gates.argument_chain_frozen=true` 是进入 `fit_alignment` 的前提。
- `gates.fit_alignment_frozen=true` 是进入 `outline` 的前提。
- `gates.outline_frozen=true` 只表示 outline contract 已稳定，可进入 `drafting` transition。
- `outline_frozen=true` 不等于 `P2.C` 已自动激活。

## Grant Run Boundary

- `grant_run_id`：当前正式 execution handle
- `workspace_id`：聚合根身份
- `draft_id`：草稿身份
- `program_id`：program / report routing 身份

这四类 ID 在 P2.B 内继续保持分离，不互相替代。

## Explicit Non-goals

- 不把 formal entry 扩成 `MCP / controller`
- 不进入 `P2.C / P3`
- 不实现 `draft -> revised`
- 不做 verdict hardening、forced rollback、federation
- 不做 write / export / HITL skeleton
