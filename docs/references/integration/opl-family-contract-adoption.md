# MAG Adoption of OPL Family Contracts

Owner: `Med Auto Grant`
Purpose: `opl_family_contract_adoption_reference`
State: `reference`
Machine boundary: 本文是人读集成参考。机器真相继续归 `contracts/runtime-program/current-program.json`、`contracts/generated_surface_handoff.json`、`contracts/action_catalog.json`、`agent/stages/manifest.json`、schemas、source、CLI/API 行为、runtime receipts 与 workspace/artifact outputs。

## Purpose

这份薄适配声明说明 `Med Auto Grant` 如何接入 `OPL` stage-led、以 Agent executor 为最小执行单位的 family runtime、quality、incident 与 operator projection 合同。OPL 托管、唤醒和投影 MAG；grant authoring authority 归 MAG。

## Runtime Attempt Projection

OPL 持有 runtime attempt、retry/resume、queue、reconciliation 与 stage transport；decisive Codex Attempt 给出语义 stage route，OPL StageRun controller 校验并物化 transition。MAG 通过 current-program、Stage Pack、domain handler、workspace refs 和 owner receipt / typed blocker refs 提供领域输入与 closeout。

OPL 只能读取、索引、排队、唤醒、回执和投影；grant truth、authoring outputs、quality/fundability/export/package authority 与 workspace body write authority 继续由 MAG 持有。

## Quality Projection

MAG 通过以下 surface 映射 `opl_family_domain_quality_projection_contract.v1`：

- `grant_quality_scorecard`
- `grant_quality_closure_dossier`
- grant review
- fundability gate
- submission-ready export gate

MAG 的质量门覆盖正文科学性、论证适配、fundability、authoring completion 和 submission-ready export；对应 verdict 与 receipt 由 MAG authority surface 产生。

## Incident Projection

MAG 通过 owner receipt、typed blocker、quality closure dossier 与 source refs 返回 domain-specific failure；OPL 负责 incident projection、recovery 和 operator routing。

## Product Operator Projection

Product status、user-loop、progress、cockpit 与 direct-entry 均由 OPL generated surfaces 从 MAG refs 投影，并保留 source refs、freshness、owner split、next surface ref 和 human gate reason。

## Stage Control Projection

MAG 的 OPL family Stage Pack 把 Stage Control Plane 的六个 Stage 映射到 MAG-owned surface：

| OPL family stage | MAG-owned surfaces |
| --- | --- |
| `call_and_candidate_intake` | `discover-funding-opportunities`、`select-project-profile`、`initialize-intake-workspace`、`input_intake` |
| `fundability_strategy` | `direction_screening`、`fit_alignment`、`grant_quality_scorecard`、fundability gate |
| `specific_aims_and_structure` | `question_refinement`、`argument_building`、`outline` |
| `proposal_authoring` | `drafting`、`revision`、`grant-progress`、`grant-user-loop` |
| `review_and_rebuttal` | `critique`、review、`grant_quality_closure_dossier`、`quality-diff` |
| `package_and_submit_ready` | `freeze` / `frozen`、`package submission-ready`、submission-ready export gate |

OPL 从 `agent/stages/manifest.json`、`contracts/action_catalog.json`、pack input 与 current-program refs 生成 `family_stage_control_plane`，组装 Stage goal、owner、skills、allowed action refs、handoff、freshness 与 authority boundary。MAG 持有 author-side grant truth、fundability judgment、route truth、quality closure 与 submission-ready export gate；外部 portal submission 由人工监督。

## Declarative Grant Pack

MAG 的 Declarative Grant Pack 位于 `agent/`，通过 current-program、capability/action/stage contracts 交给 OPL 生成 standard domain agent surfaces。`agent/` 是 repo-source canonical semantic pack。

- repo-source 边界固定为 `agent`、`contracts`、`runtime`、`docs`。
- `agent/prompts/` 持有六个 stage prompt：`call_and_candidate_intake`、`fundability_strategy`、`specific_aims_and_structure`、`proposal_authoring`、`review_and_rebuttal`、`package_and_submit_ready`。
- `agent/stages/` 持有对应 stage policy。
- `agent/skills/` 持有 MAG grant authoring skill declaration。
- `agent/quality_gates/` 持有 fundability、quality、export/package、memory/receipt 和 authority boundary。
- `agent/knowledge/` 持有 grant strategy memory、package authority 和 owner receipt 知识边界。
- `runtime` 边界只声明 `domain_handler`、`projection_builder`、`lifecycle_adapter`。
- `artifact_locator_contract` 只给 OPL 读取 locator/ref；真实申请书、receipt 实例、中间产物和 submission-ready export 都属于 workspace 或 `$CODEX_HOME/projects/med-autogrant/runtime-state/artifacts/<grant_run_id>/`。
- `controlled_stage_attempt_projection` 只暴露 attempt descriptor、source refs、runtime status projection、receipt refs 和 OPL-hosted controlled stage attempt proof refs。
- `controlled_domain_memory_apply_proof.repo_source_layout_audit` 暴露 `agent`、`contracts`、`runtime`、`docs` source refs，用于审计当前 repo-source layout。
- OPL 只消费 descriptor/refs，不持有 fundability verdict、authoring quality verdict、submission-ready export verdict 或 canonical grant artifact content。
- `agent/stages/manifest.json` 的 `prompt_ref`、knowledge、quality gate 与 action refs 必须可解析；`contracts/pack_compiler_input.json` 的 `required_domain_pack_paths` 必须列出完整 `agent/` pack 文件，且不把 `agent/README.md` 当成机器 required semantic pack path。
- `contracts/runtime-program/current-program.json` 与 `contracts/pack_compiler_input.json` 使用 `canonical_semantic_pack_root="agent/"` 与 `canonical_semantic_pack_role="repo_source_declarative_grant_pack"`。

## OPL Domain Handler Export

MAG 只在 `domain-handler export` 中返回 OPL 可消费的 body-free refs。该薄导出面给 OPL 建 workspace/source/artifact/memory/lifecycle/projection 索引，不再复制 product-entry manifest 或 runtime platform body：

- 顶层 `source_provenance` 同步暴露 OPL `substrate projections` 可直接解析的 body-free source refs：source policy/support doc ref、historical fixture ref、explicit archive/import command ref 与 parity oracle ref。
- workspace 只给 opaque ref、workspace locator、session/ref 与 restore/progress ref。
- source 只给 JSON pointer refs，不给 source body。
- artifact 只给 artifact locator、inventory ref 与 runtime artifact root ref，不给 package body 或 canonical grant artifact content。
- memory 只给 domain memory descriptor/locator、receipt locator 与 writeback receipt refs，不给 memory body，也不让 OPL accept/reject memory writeback。
- lifecycle/owner receipt 只给 receipt refs、owner receipt contract ref 与 guarded lifecycle proof ref，不转移 owner receipt authority。

这层不声明 OPL 替代 MAG 的 grant truth、fundability verdict、authoring quality verdict、submission-ready export verdict、package body、memory body 或 owner receipt authority。它的作用是把现有 domain-handler/product-entry/export/contract surface 收成一个 OPL 可直接消费的 opaque/index-only substrate adapter。

## Domain Memory Descriptor / Locator

MAG 通过顶层 `domain_memory_descriptor` 暴露 OPL 可解析的 `family_domain_memory_ref.v1`，并通过 `domain_memory_descriptor_locator` 保留 grant strategy memory 的 MAG-owned 详细定位面。它引用 `docs/references/grant_strategy_memory_policy.md`，并把六个 stage 的 memory context 绑定到 `family_stage_control_plane`，但 repo manifest 只携带 descriptor、policy ref、stage descriptor refs、locator template、controlled consumed-memory proof refs 与 writeback receipt proof refs。

实际 memory content、accepted/rejected writeback、fundability strategy、authoring quality verdict 和 submission-ready export verdict 继续由 MAG 持有。OPL 可以索引 locator/ref、展示 consumed-memory provenance、路由 writeback receipt；它不能保存 MAG memory content，不能接受或拒绝 MAG memory writeback，也不能用 memory 产生 fundability、authoring quality 或 export verdict。

当前读法：`domain_memory_descriptor` 是给 OPL family memory index 的薄引用面；`domain_memory_descriptor_locator` 仍是 MAG 侧 memory locator、migration plan、proposal、accept/reject、receipt 与 operator projection 的详细合同面。OPL 可把 MAG 解析为 resolved descriptor，MAG 提供 accepted/rejected receipt evidence 写入路径；external evidence 和 grant-stage controlled attempt closeout 的具体 refs 由机器合同维护。真实 memory body 仍由 workspace/runtime artifact root 产生，不进入 repo source；后续 OPL-hosted controlled grant stage soak 必须继续返回 MAG owner receipt、typed blocker 或 no-regression evidence，且不能替代 MAG-owned grant/fundability/export verdict。

## Lifecycle Adapter

MAG 的 `opl_stage_runtime_registration` 现在携带 `family_lifecycle_adapter`。这层只把已有 `runtime_control`、`session_continuity`、`grant-progress/user-loop` 与 `artifact_inventory` 映射为 OPL family persistence、lifecycle、owner-route discovery 和 adoption projection：

- persistence：只给 OPL native/index lifecycle 建索引输入，write policy 固定为 `opl_index_only_no_domain_truth_writes`。
- lifecycle：映射 `opl_family_runtime_attempt_contract.v1` 的 attempt state、workspace boundary、owner repo、failure/reconciliation 和 last observed projection 字段。
- owner-route discovery：从 skill catalog / stage runtime registration registration 发现 product status、operator loop、progress 和 resume route；route truth owner 仍是 MAG。
- adoption：映射 `opl_family_product_operator_projection.v1` 的 source refs、freshness、owner split、next surface ref 与 human gate reason。

`opl_stage_runtime_registration` 是 OPL stage-led runtime framework 的 MAG 侧注册与投影输入；grant truth、fundability 与 submission-ready gate 仍归 MAG owner。

## Authority Boundary

- OPL 持有 runtime、transport、recovery 和 generated projection。
- MAG 持有 grant truth、fundability、quality、export、package、memory 与 owner receipt authority。
- 外部 portal submission 由人工授权。
