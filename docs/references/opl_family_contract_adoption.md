# MAG Adoption of OPL Family Contracts

## Purpose

这份薄适配声明说明 `Med Auto Grant` 如何满足 `OPL` family runtime / quality / incident / operator projection 合同。它不把 `OPL` 变成 grant authoring owner，也不把医学论文质量门或视觉交付 proof 引入 MAG。

## Runtime Attempt Projection

MAG 通过 `runtime_control`、`runtime_continuity`、`grant-autonomy-controller-report` 和 `workspace progress` 映射 `opl_family_runtime_attempt_contract.v1`。这些 surface 可以向 `OPL` 投影 attempt state、retry/backoff、workspace boundary、failure reason、reconciliation status 和 last observed projection。

`OPL Runtime Manager` 只能读取和索引；grant authoring runtime、route truth、workspace write authority 继续由 MAG 持有。

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

## Lifecycle Adapter

MAG 的 `opl_runtime_manager_registration` 现在携带 `family_lifecycle_adapter`。这层只把已有 `runtime_control`、`session_continuity`、`grant-progress/user-loop` 与 `artifact_inventory` 映射为 OPL family persistence、lifecycle、owner-route discovery 和 adoption projection：

- persistence：只给 OPL native/index lifecycle 建索引输入，write policy 固定为 `opl_index_only_no_domain_truth_writes`。
- lifecycle：映射 `opl_family_runtime_attempt_contract.v1` 的 attempt state、workspace boundary、owner repo、failure/reconciliation 和 last observed projection 字段。
- owner-route discovery：从 skill catalog / runtime manager registration 发现 product status、operator loop、progress 和 resume route；route truth owner 仍是 MAG。
- adoption：映射 `opl_family_product_operator_projection.v1` 的 source refs、freshness、owner split、next surface ref 与 human gate reason。

这层不重塑 runtime，不引入 SQLite 深迁移，也不把 OPL 写成 grant truth、fundability 或 submission-ready gate owner。

## Boundaries

- `OPL` 只消费 MAG projection，不持有 grant truth。
- `OPL` 不关闭 fundability gate 或 submission-ready export gate。
- MAG 不引入 MAS 的 medical publication gate。
- MAG 不引入 RCA 的 visual render/export proof gate。
- `Hermes-Agent` 只保留显式 hosted/proof lane，不成为 OPL 或 MAG 的默认 owner。
