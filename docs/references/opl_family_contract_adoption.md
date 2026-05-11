# MAG Adoption of OPL Family Contracts

## Purpose

这份薄适配声明说明 `Med Auto Grant` 如何满足 `OPL` Codex-first、stage-led runtime framework 的 family runtime / quality / incident / operator projection 合同。OPL 可以把 MAG 作为外部领域依赖托管、唤醒和投影；它不把 `OPL` 变成 grant authoring owner，也不把医学论文质量门或视觉交付 proof 引入 MAG。

## Runtime Attempt Projection

MAG 通过 `runtime_control`、`runtime_continuity`、`grant-autonomy-controller-report` 和 `workspace progress` 映射 `opl_family_runtime_attempt_contract.v1`。这些 surface 可以向 `OPL` 投影 attempt state、retry/backoff、workspace boundary、failure reason、reconciliation status 和 last observed projection。

OPL 只能读取、索引、排队、唤醒、回执和投影；grant authoring runtime、route truth、workspace write authority 继续由 MAG 持有。

## Quality Projection

MAG 通过以下 surface 映射 `opl_family_domain_quality_projection_contract.v1`：

- `grant_quality_scorecard`
- `grant_quality_closure_dossier`
- grant review
- fundability gate
- submission-ready export gate

MAG 的质量门是 grant-specific：正文科学性、论证适配、fundability、authoring completion 和 submission-ready export。`claim-only ready`、generic persona QA、medical publication gate、visual render/export proof gate、OPL projection-only 状态都不能成为 MAG grant quality authority。

## Incident Projection

MAG 通过 `controller_report`、`runtime_control.semantic_closure`、`workspace cockpit` 和 explicit wakeup/TODO queue 映射 `opl_family_incident_learning_loop.v1`。真实 incident 必须回流成 guard、test、contract、runbook、taxonomy update 或 operator projection；domain-specific failure 必须有 MAG-owned closure ref。

## Product Operator Projection

MAG 通过 `product status`、`product user-loop`、`workspace progress`、`workspace cockpit` 与 `product direct-entry` 映射 `opl_family_product_operator_projection.v1`。这些投影必须保留 source refs、freshness、owner split、next surface ref 和 human gate reason。

## Stage Control Projection

MAG 的 OPL family stage pack 是 descriptor/projection，不是新的 controller 或 route truth。它把 OPL family Stage Control Plane 的六个 stage 映射回 MAG 已有 surface：

| OPL family stage | MAG-owned surfaces |
| --- | --- |
| `call_and_candidate_intake` | `discover-funding-opportunities`、`select-project-profile`、`initialize-intake-workspace`、`input_intake` |
| `fundability_strategy` | `direction_screening`、`fit_alignment`、`grant_quality_scorecard`、fundability gate |
| `specific_aims_and_structure` | `question_refinement`、`argument_building`、`outline` |
| `proposal_authoring` | `drafting`、`revision`、`grant-progress`、`grant-user-loop` |
| `review_and_rebuttal` | `critique`、review、`grant_quality_closure_dossier`、`quality-diff` |
| `package_and_submit_ready` | `freeze` / `frozen`、`package submission-ready`、submission-ready export gate |

这层只让 OPL 读取 MAG 的 stage descriptor、operator projection 和下一步定位。`product-entry-manifest` 中的 `family_stage_control_plane` 为 OPL discovery smoke 固定 stage goal、owner、skills、allowed action refs、handoff、source refs、freshness 与 authority boundary；`allowed_action_refs` 必须对齐同一 manifest 内的 `family_action_catalog`。MAG 继续持有 author-side grant truth、fundability judgment、route truth、quality closure 与 submission-ready export gate；外部 portal submission 继续由人工监督。

## Standard Domain-Agent Skeleton

MAG 现在通过 `product-entry-manifest` 导出 `standard_domain_agent_skeleton`。这是一层标准 skeleton adapter/manifest，不是物理目录重组，也不把 runtime 写成新的 grant executor。

- repo-source 边界固定为 `agent`、`contracts`、`runtime`、`docs`。
- `runtime` 边界只声明 `sidecar`、`projection_builder`、`lifecycle_adapter`。
- `artifact_locator_contract` 只给 OPL 读取 locator/ref；真实申请书、receipt 实例、中间产物和 submission-ready export 都属于 workspace 或 `$CODEX_HOME/projects/med-autogrant/runtime-state/artifacts/<grant_run_id>/`。
- `controlled_stage_attempt_projection` 只暴露 attempt descriptor、source refs、runtime status projection、receipt refs 和 OPL-hosted controlled stage attempt proof refs。
- OPL 只消费 descriptor/refs，不持有 fundability verdict、authoring quality verdict、submission-ready export verdict 或 canonical grant artifact content。

## Domain Memory Descriptor / Locator

MAG 通过顶层 `domain_memory_descriptor` 暴露 OPL 可解析的 `family_domain_memory_ref.v1`，并通过 `domain_memory_descriptor_locator` 保留 grant strategy memory 的 MAG-owned 详细定位面。它引用 `docs/references/grant_strategy_memory_policy.md`，并把六个 stage 的 memory context 绑定到 `family_stage_control_plane`，但 repo manifest 只携带 descriptor、policy ref、stage descriptor refs、locator template、controlled consumed-memory proof refs 与 writeback receipt proof refs。

实际 memory content、accepted/rejected writeback、fundability strategy、authoring quality verdict 和 submission-ready export verdict 继续由 MAG 持有。OPL 可以索引 locator/ref、展示 consumed-memory provenance、路由 writeback receipt；它不能保存 MAG memory content，不能接受或拒绝 MAG memory writeback，也不能用 memory 产生 fundability、authoring quality 或 export verdict。

2026-05-11 状态：MAG 本仓的 migration/proposal/receipt surface、controlled consumed-memory proof、writeback receipt proof、OPL-hosted controlled grant stage attempt proof descriptor 和标准 `family_domain_memory_ref.v1` adapter 已落地。`domain_memory_descriptor` 是给 OPL family memory index 的薄引用面；`domain_memory_descriptor_locator` 仍是 MAG 侧 memory locator、migration plan、proposal、accept/reject、receipt 与 operator projection 的详细合同面。当前是 repo-source proof contract / descriptor landed，不是 production provider-hosted grant soak completed；真实 proof instance、accepted/rejected receipt instance 和 memory body 仍由 workspace/runtime artifact root 产生，不进入 repo source。

## Lifecycle Adapter

MAG 的 `opl_stage_runtime_registration` 现在携带 `family_lifecycle_adapter`。这层只把已有 `runtime_control`、`session_continuity`、`grant-progress/user-loop` 与 `artifact_inventory` 映射为 OPL family persistence、lifecycle、owner-route discovery 和 adoption projection：

- persistence：只给 OPL native/index lifecycle 建索引输入，write policy 固定为 `opl_index_only_no_domain_truth_writes`。
- lifecycle：映射 `opl_family_runtime_attempt_contract.v1` 的 attempt state、workspace boundary、owner repo、failure/reconciliation 和 last observed projection 字段。
- owner-route discovery：从 skill catalog / stage runtime registration registration 发现 product status、operator loop、progress 和 resume route；route truth owner 仍是 MAG。
- adoption：映射 `opl_family_product_operator_projection.v1` 的 source refs、freshness、owner split、next surface ref 与 human gate reason。

这层不重塑 MAG runtime，不引入 SQLite 深迁移，也不把 OPL 写成 grant truth、fundability 或 submission-ready gate owner。字段名仍可保留 `opl_stage_runtime_registration` 作为兼容 envelope，但当前语义是 OPL stage-led runtime framework 的 MAG 侧注册/投影输入。

## Boundaries

- `OPL` 只消费 MAG projection，不持有 grant truth。
- `OPL` 不关闭 fundability gate 或 submission-ready export gate。
- MAG 不引入 MAS 的 medical publication gate。
- MAG 不引入 RCA 的 visual render/export proof gate。
- `Hermes-Agent` 只保留显式 hosted/proof lane，不成为 OPL 或 MAG 的默认 owner。
