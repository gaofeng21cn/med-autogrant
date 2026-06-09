# R3.A Machine-Applicable Revision Mutation Contract

> 生命周期注记（`2026-05-17`）：这份 dated spec 是 path-stable 的历史/支撑记录；只有 `docs/specs/README.md`、`docs/specs/specs_lifecycle_map.md`、`docs/status.md` 或 `contracts/runtime-program/current-program.json` 明确指定的仍 current subsection 才可作为当前边界阅读。请先读取 `docs/status.md`、核心五件套与 `contracts/runtime-program/current-program.json`。本文中的旧 `Current Truth`、Hermes、OPL Gateway、host-agent 或 federation wording 只作 provenance，不是当前 default owner line。

Owner: `Med Auto Grant`
Purpose: `historical_r3a_revision_mutation_contract_provenance`
State: `history`
Machine boundary: 本文是人读历史 spec，保留 2026-04-09 R3.A machine-applicable revision mutation contract 的形成过程。当前 revision、quality verdict、route truth、Codex CLI default executor、OPL/Temporal runtime owner 与机器行为以核心五件套、AI-first quality active spec、`docs/specs/README.md`、`docs/specs/specs_lifecycle_map.md`、contracts、schemas、source、CLI/API 行为与 `contracts/runtime-program/current-program.json` 为准；本文不是当前 runtime queue、attempt ledger 或 hosted runtime owner。

Date: `2026-04-09`

## Purpose

这份文档把 `R3.A / Critique Revision Executor Surface` 当前真正缺失的实现合同补齐为 repo-tracked truth：

- 不再让 `execute-revision-pass` 依赖未冻结的 authoring semantics
- 不再让 revision mutation 依赖仓外 authoring engine
- 明确什么样的 `RevisionPlan` item 才是 machine-applicable
- 明确 revision-side write pass 究竟如何 deterministically 改写 workspace

这里冻结的是 **machine-applicable revision mutation contract**，不是新的 LLM 写作模式，也不是新的 formal entry。

## Hard Boundary Docs

必须同时服从：

- `/Users/gaofeng/workspace/med-autogrant/AGENTS.md`
- `/Users/gaofeng/workspace/med-autogrant/docs/history/specs/README.md` 中的 runtime-first R1-R5 compression record；原 R3.A activation package 与 R1-R5 boundary map 长正文已删除，精确正文只从 git history 读取
- `/Users/gaofeng/workspace/med-autogrant/docs/history/specs/README.md` 中的 P2/P3/P4 authoring-review-verification compression record；原 P2.C / P3.B / P3.C 长正文只从 git history 读取
- `/Users/gaofeng/workspace/med-autogrant/docs/history/specs/README.md` 中的 Foundation / object model 压缩记录，以及当前 schema/source/contracts owner

## Contract Scope

`R3.A` 第一棒当前只冻结 **section-level revision mutation**：

- 只处理 current active `ApplicationDraft.sections[]` 与对应 `outline[]`
- 只处理 current active `RevisionPlan.items[]` 中可 machine-apply 的 section rewrite items
- 只产生 revised workspace candidate
- 只把 `revision -> critique` 的 completed revised switch 收成 deterministic runtime behavior

当前明确不在本合同内：

- `question:<id>` 级别的 reframe mutation
- `argument:<id>` 级别的 argument graph rebuild
- critique synthesis
- re-review critique generation
- final package / freeze manifest / export summary
- hosted-friendly session boundary

## Eligible Revision Item Subset

只有同时满足以下条件的 active `RevisionPlan.items[]`，才允许被 `execute-revision-pass` 机械执行：

1. 当前 active `MentorCritique.verdict` 属于 `major_revision / minor_revision`
2. 当前 active `RevisionPlan.execution_status=planned`
3. `forced_rollback_stage` 为空
4. `gates.presubmission_frozen=false`
5. `item.action_type` 属于：
   - `rebuild_argument`
   - `rewrite_section`
   - `add_evidence`
   - `tighten_fit`
6. `item.target_ref` 必须满足：
   - 形如 `section:<section_key>`
   - `<section_key>` 必须与当前 active `ApplicationDraft.sections[].section_key` 精确匹配
7. 每个 executable item 都必须携带 `mutation_payload`

如果任一 active item 不满足以上条件，`execute-revision-pass` 必须 fail-closed。

## Mutation Payload V1

`RevisionPlan.items[].mutation_payload` 的 repo-frozen 最小字段集固定为：

- `operation`
  - 当前只允许：`replace_draft_section`
- `target_section_key`
  - 必须与 `item.target_ref=section:<section_key>` 中的 `<section_key>` 精确一致
- `replacement_text`
  - 用于替换 active `ApplicationDraft.sections[].text`
- `replacement_core_claim`
  - 当 active `ApplicationDraft.outline[]` 中存在同一 `section_key` 时必填
- `linked_object_ids`
  - non-empty string list
  - 必须包含 `item.required_input_ids` 中全部 id

当前不允许：

- 多种 operation 并存
- partial patch / diff patch / heuristic merge
- 没有 `replacement_text` 的自由文本“建议”
- 引用 workspace 中不存在的 object id

## Target Resolution Rules

对于每个 executable item：

1. 从 `item.target_ref` 解析出 `target_section_key`
2. 定位当前 active `ApplicationDraft.sections[]` 中同名 section
3. 若不存在，fail-closed
4. 定位当前 active `ApplicationDraft.outline[]` 中同名 section
5. 若存在 outline section，则 `mutation_payload.replacement_core_claim` 必须存在

当前不允许同一轮 execution 中两个 item 指向同一个 `target_section_key`。
如果发现 duplicate target section，必须 fail-closed，而不是隐式合并。

## Deterministic Apply Semantics

`execute-revision-pass` 一旦进入实现，必须按以下 deterministic sequence 执行：

1. 读取 input workspace
2. 定位 current active：
   - `draft_id`
   - `active_revision_plan_id`
   - `MentorCritique`
3. 校验：
   - `draft_id / workspace_id / grant_run_id` 一致
   - active critique / revision plan linkage 一致
   - `pre_revision_version_label / post_revision_version_label` 已显式存在
4. 拷贝 input workspace 为 revised workspace candidate
5. 按 `RevisionPlan.items[]` 原顺序逐条应用 executable item：
   - 替换目标 `sections[].text`
   - 替换目标 `sections[].linked_object_ids`
   - 如存在同名 `outline[]`，替换其 `core_claim`
   - 如存在同名 `outline[]`，替换其 `linked_object_ids`
6. 完成全部 mutation 后，回写 active draft：
   - `version_label = post_revision_version_label`
   - `status = revised`
   - `draft_id / project_title / frozen_question_id` 保持不变
7. 回写 active revision plan：
   - `execution_status = completed`
   - `comparison_summary` 按下面的 deterministic format 生成
8. 回写 workspace stage：
   - `lifecycle_stage = critique`

## Deterministic Comparison Summary Format

`comparison_summary` 当前不允许依赖自由生成。

第一版固定格式为：

`Applied revision plan <revision_plan_id>: updated sections [<section_key_1>, <section_key_2>, ...]; draft version <pre_revision_version_label> -> <post_revision_version_label>.`

约束：

- section key 列表必须按 `RevisionPlan.items[]` 的执行顺序输出
- 不得额外加入自然语言评价
- 不得覆盖上一轮 `reviewed_revision_evidence`

## Revised Workspace Output Rules

输出 revised workspace candidate 时，必须继续保持：

- `grant_run_id` 不变
- `workspace_id` 不变
- `draft_id` 不变
- `program_id` 不进入 workspace
- `frozen_question_id` 不变
- `reviewed_revision_plan_id / reviewed_revision_evidence / source_critique_id / active_revision_plan_id` 不漂移
- `verification_checkpoint / checkpoint_status` 不在这一层被重写

## Failure Conditions

以下情况必须 fail-closed：

- 缺少 `mutation_payload`
- `target_ref` 与 `mutation_payload.target_section_key` 不一致
- duplicate `target_section_key`
- `linked_object_ids` 未覆盖 `required_input_ids`
- target section 不存在
- outline 存在但缺少 `replacement_core_claim`
- `pre_revision_version_label == post_revision_version_label`
- 当前 active `RevisionPlan.execution_status != planned`
- 当前 active critique verdict 不属于 `major_revision / minor_revision`
- `forced_rollback_stage` 非空
- `gates.presubmission_frozen=true`

## Canonical Example Inputs

当前 repo-tracked canonical executable examples 至少包括：

- `/Users/gaofeng/workspace/med-autogrant/examples/nsfc_workspace_p2c_critique.json`
- `/Users/gaofeng/workspace/med-autogrant/examples/nsfc_workspace_p3b_re_review_major_revision.json`

这些 example 必须显式携带可 machine-apply 的 `mutation_payload`，不得再依赖自由 authoring semantics。

## Excluded Scope

- `question:<id>` 级别 mutation
- `argument:<id>` 级别 mutation
- critique synthesis
- final package / freeze manifest / export summary
- hosted-friendly contract bundle
- web runtime / hosted runtime
