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

MAG 通过 `product frontdesk`、`product user-loop`、`workspace progress`、`workspace cockpit` 与 `product direct-entry` 映射 `opl_family_product_operator_projection.v1`。这些投影必须保留 source refs、freshness、owner split、next surface ref 和 human gate reason。

## Boundaries

- `OPL` 只消费 MAG projection，不持有 grant truth。
- `OPL` 不关闭 fundability gate 或 submission-ready export gate。
- MAG 不引入 MAS 的 medical publication gate。
- MAG 不引入 RCA 的 visual render/export proof gate。
- `Hermes-Agent` 只保留显式 hosted/proof lane，不成为 OPL 或 MAG 的默认 owner。

