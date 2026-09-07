# AI-first 质量与修订

Owner: `Med Auto Grant`
Purpose: `ai_first_quality_boundary_active_spec`
State: `active_current_spec`
Machine boundary: 本文解释 AI-first quality ownership 与 projection boundary；机器行为归 `src/med_autogrant/ai_first_boundaries.py`、quality source、contracts/schema 与真实 review evidence。

本文冻结 `Med Auto Grant` 的 AI-first 质量边界：schema-backed pack、scorecard、dossier、gate 和 controller report 可以保存结构、证据引用和机械 readiness，但不持有基金写作质量判断或 submission-ready export verdict。写作质量、评审判断和 revision intent 可以来自 AI-authored author / reviewer artifact；submission-ready export verdict 与 owner receipt 必须保持 MAG-owned，并消费对应的独立 Review evidence。

## 边界

- authoring executor 与 critique executor 持有 AI-authored 正文、科学 critique、reviewer judgment 和 revision intent。
- `grant_quality_scorecard` 与 `grant_quality_closure_dossier` 是 AI-critique-backed aggregator；它们可以汇总完整度、结构评分、证据链接、lineage、queue 和 blocker。
- scorecard 字段、schema 完整度、证据链接存在性和数字分数只是结构信号，不能独立把 workspace 提升为 `near_submission_candidate` 或 `submission_grade_candidate`。
- 缺少 active AI-backed critique 或等价 AI-authored quality assessment 时，scorecard 必须保持 `assessment_owner=projection_only` 和 `ai_reviewer_required=true`。
- submission-ready package 的机械完整性只能写入 `mechanical_package_completeness`。Producer package 始终是 `submission_ready=false` 候选；最终 readiness 消费 current scoped evidence、绑定所审 artifact identity 的 Review、独立 exact-byte release integrity 和 MAG-owned export/owner verdict，详见[交付](../delivery/README.md)。

## 候选状态规则

`grant-quality-scorecard` 聚合 workspace-version 的 AI review judgment 与机械结构信号；`grant-quality-closure-dossier` 从同一 scorecard 派生 closure packages；`grant-quality-diff` 比较 score、dimension、issue lineage 和 evidence movement，不建立第二条评分路径。它们的字段由 `schemas/v1/grant-quality-*.schema.json` 定义。多步 critique/revision 和 Stage residency、budget/retry/resume 归 [OPL 运行模型](../runtime/README.md)，MAG single-pass handler 只消费领域结果。

只有 active critique provenance 由 AI reviewer 支撑时，才允许 candidate-ready 状态。

允许的 owner 集合由 `src/med_autogrant/ai_first_boundaries.py` 的 `AI_REVIEWER_BACKED_OWNERS` 持有。除了 active critique owner，还要求互相独立的 execution/review attempt refs、review receipt、`no_shared_context_verified=true` 和 reviewer identity；已知 owner 名称本身不足以建立独立性。

如果 active critique 缺失、过期、无 owner，或不属于上述 owner：

- `overall_status` must not become `near_submission_candidate`.
- `overall_status` must not become `submission_grade_candidate`.
- `assessment_owner` 保持 `projection_only`，`ai_reviewer_required=true`，并返回缺少独立评审的诊断。它限制 ready 声明，不作为 Stage progression gate。

## Revision executor 规则

`revision_executor` 是机械 apply 层，只能应用 AI-authored `revision_plan.items[].mutation_payload`。

它不能：

- 自己生成 replacement prose；
- 合成 fallback text；
- 用模板补齐缺失 mutation payload；
- 用 heuristic post-processing 修正文案。

缺少 active AI-backed critique 或 mutation payload 时，revision executor 必须 fail closed。

## 开发检查

- 新增 quality-ready state 前，先识别持有判断的 AI artifact。
- 消费 scorecard 的 candidate status 前，检查 `assessment_owner` 和 `ai_reviewer_required`。
- Package review currentness 与 readiness 输入以 `contracts/epistemic_review_scope_profile.json` 和 `contracts/owner_receipt_contract.json` 为准。
- 新增 revision execution 行为前，确认每个 prose mutation 都来自 `mutation_payload`。
- schema/gate/controller code 只能作为 aggregation 和 routing layer，不能变成 hidden author 或 hidden reviewer。
- 修改 scorecard、dossier、critique、revision 或 quality mapping 时，验证对应可观察行为；不以文档措辞作为测试断言。

## Verification

Relevant guardrails:

- `tests/test_ai_first_quality_boundary.py`
- `tests/test_grant_quality.py`
- `tests/test_critique_executor.py`
- `tests/test_revision_executor.py`
- `scripts/verify.sh meta`
- `scripts/verify.sh`
