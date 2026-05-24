# MAG 理想目标态差距与完善计划

Owner: `Med Auto Grant`
Purpose: `ideal_state_gap_plan`
State: `active_plan`
Machine boundary: 本文是人读 current gap / completion plan。机器真相继续归 `contracts/runtime-program/current-program.json`、contracts、schemas、source、CLI/API 行为、product-entry manifest、workspace/runtime artifact root、runtime receipts、质量报告和导出包。
Date: `2026-05-24`

## 读法

本文是 MAG 当前唯一 active gap / plan 入口。目标态读 [Med Auto Grant 理想目标态](../references/med-auto-grant-ideal-state.md)；当前状态读 [当前状态](../status.md)；per-surface 明细读 [MAG 私有实现与 OPL 迁移台账](./opl-private-implementation-migration-inventory.md)；过程流水读 [MAG standard agent 文档过程归档 2026-05](../history/plans/mag-standard-agent-doc-process-history-2026-05.md)。

差距按理想态判断，不按现有 MAG 代码是否还能运行判断。通用 runtime、runner、queue、session、journal、workspace/source intake、memory/package transport、workbench、observability、generic CLI/product-entry/sidecar/status wrapper 属于 OPL / shared family layer；MAG 只保留 grant authority、domain handler、refs-only adapter、diagnostic、fixture 或 tombstone。

本文不保存长篇执行 prompt、dated closeout checklist 或 receipt proof 流水。每轮完成后只把当前 truth、剩余 gap、证据门和近期计划折回本文；细节进入合同、history、specs lifecycle map 或提交历史。

## 当前唯一真相

MAG 是医学基金申请 domain agent，也是 OPL-compatible Foundry Agent package。Direct app skill / CLI / `MedAutoGrantDomainEntry` 是一等入口；任务启动后的默认运行驻留是 OPL/Temporal hosted autonomous runtime；`Codex CLI` 是当前第一公民 stage executor。

无论 direct path 还是 OPL-hosted path，执行都必须回到 MAG-owned grant truth、fundability / quality / export verdict、package authority、grant strategy memory accept/reject、owner receipt 和 typed blocker。OPL 持有 Temporal provider runtime、typed queue、attempt ledger、generic transition runner、workspace/source shell、memory locator、artifact/package lifecycle shell、operator projection、observability/SLO、generated wrapper 和 App/workbench shell。

当前机器面必须按下面三条同时读取：

| 信号 | 当前值 | 读法 |
| --- | --- | --- |
| `mag_functional_structure_gap_count` | `0` | MAG repo 侧当前 surface 已收到 handler / refs-only / authority 边界；不表示生产切换或 live soak 完成。 |
| `claims_opl_replacement_exists` | `false` | OPL generated/default caller、App/workbench 和 production caller 仍需要真实消费证据。 |
| `claims_all_bridge_exits_complete` / `claims_production_long_run_soak_complete` | `false` | bridge exit、physical cleanup 与 Temporal long-soak 仍是 evidence / cleanup gate。 |

当前 `product_entry*`、`product_entry_parts/*`、`domain_runtime*`、runtime registration、sidecar、lifecycle、memory/package projection、status/user-loop shell 仍可见于 active source。它们只能按 direct handler、refs-only adapter、minimal grant authority function、diagnostic、migration input 或 tombstone/provenance 读取，不能重新写成 MAG 私有 runtime platform。

## 目标态

MAG 的理想形态是：

```text
Declarative Grant Pack
  + OPL generated/hosted surfaces
  + minimal grant authority functions
```

`agent/` 是 declarative grant pack；`contracts/` 是 pack compiler、stage/action/memory/artifact/receipt、handoff 与 evidence request 的机器面；`src/med_autogrant/**` 只保留 grant domain handler、minimal authority function、refs-only adapter、native helper、fixture 或 diagnostic。

MAG 必须保留的 authority：

- funding call 解释、profile/task lock、fundability strategy、specific aims 和 proposal route truth；
- grant stage pack、prompt/skill、policy table、domain transition oracle、quality/review/export gate；
- grant strategy memory body、accept/reject decision、writeback receipt 和 owner boundary；
- submission-ready package、gap report、manual portal boundary、package/export authority 和 owner receipt；
- typed blocker、safe action refs、no-forbidden-write guard 和 MAG domain projection refs。

这些 authority 不迁给 OPL，也不能由 schema completeness、scorecard 分数、package existence、provider completion、queue completion 或 controller route 机械生成 ready verdict。

## 已落地

| Area | 当前状态 | 当前 owner / evidence |
| --- | --- | --- |
| Identity / runtime owner boundary | `landed` | 核心五件套与 `current-program.json` 已固定 MAG 是 grant authority，OPL/Temporal 是默认 task runtime owner。 |
| Declarative Grant Pack | `landed_with_evidence_tail` | `agent/`、stage control plane、quality gates、pack compiler input 已作为 OPL generated surface 输入。 |
| Retained authority taxonomy | `landed_with_guard_tail` | fundability、quality、export、package、memory、owner receipt、grant helper 已分成 AI-first judgment surface 与 programmatic guard surface。 |
| Consumer thinning / refs-only boundary | `landed_with_external_gate` | `mag_consumer_thinning_contract`、sidecar、receipt projection、lifecycle/package/memory refs 只输出 refs、typed blocker、owner receipt 与 action metadata。 |
| External evidence request accounting | `refs_only_closed` | `mag-evidence-receipt-ledger.json` 已记录 7 个 request refs-only close；剩余真实证据门是 `temporal_provider_long_soak_window_evidence` 和持续 no-regression / consumption。 |
| Process/history foldback | `landed` | dated closeout、receipt proof、provider/Gateway/local-manager 背景已回到 history/specs/provenance，不再作为 active plan 流水。 |

## 功能/结构差距

当前没有未分类的大块 MAG 功能缺口；剩余结构差距是 owner shape 与 physical cleanup tail：

1. `generated_surface_bridge_exit`
   OPL generated/hosted caller 尚未成为所有 product/status/workbench/sidecar shell 的默认生产 caller。MAG hand-written shell 暂时保留为 direct handler target 或 refs-only adapter；default caller 证据成立后继续删除或 tombstone wrapper。

2. `legacy_runtime_session_lifecycle_exit`
   旧 local runtime journal、attempt ledger、repo-owned scheduler daemon、Hermes/Gateway/local-manager probe、flat shell alias、facade patch bridge 和 compat aggregate test 只能作为 history、tombstone、explicit proof history 或 regression oracle。active caller 清零后直接退役，不新增 compatibility shim。

3. `package_memory_lifecycle_refs_only_boundary`
   Memory receipt projection、package lifecycle handoff、lifecycle receipt bundle、continuous receipt reconciliation 和 sidecar export 必须保持 body-free refs、owner receipt、verdict refs、typed blocker 和 safe action metadata，不输出 memory body、grant artifact/private evidence 或 OPL ledger state。

4. `private_authority_ai_first_guard`
   Fundability、quality、export、memory accept/reject 是 AI-first judgment surface；package authority、owner receipt signer 和 grant helper 是 programmatic guard surface。程序只能 validator / materializer / receipt signer / guard / refs projection，不能机械生成 ready verdict。

5. `physical_morphology_tail`
   `product_entry_parts/*`、`domain_runtime_parts/*`、runtime registration、autonomy loop/report shell、lifecycle/memory/package helpers 等 active path 必须持续被合同约束为 handler、refs-only adapter、minimal authority function、diagnostic 或 tombstone。详细 path-level inventory 归 [MAG 私有实现与 OPL 迁移台账](./opl-private-implementation-migration-inventory.md)。

## 证据差距

以下 gap 只通过真实 external receipt、typed blocker、owner receipt 或 no-regression evidence 关闭；不能反向重开 MAG repo 侧结构缺口：

| Evidence gate | 当前状态 | 关闭条件 |
| --- | --- | --- |
| OPL-hosted grant-stage attempt | `needs_continuous_real_attempts` | 真实 OPL-hosted stage attempt 持续返回 MAG owner receipt、typed blocker 或 no-regression evidence。 |
| Real workspace memory/package/lifecycle scaleout | `needs_real_workspace_scaleout` | 真实 grant workspace 产生 accepted/rejected memory receipt、package/export lifecycle receipt、cleanup/restore/retention receipt 和 owner receipt scaleout。 |
| App/operator/release consumption | `needs_sustained_consumption` | OPL/App/operator closeout、executor-first bundle、release/default caller 持续消费 MAG package refs、quality refs、manual portal boundary、transition oracle refs 和 safe action refs。 |
| Temporal provider long soak | `open` | `temporal_provider_long_soak_window_evidence`、long SLO、repair cadence 和 live receipt reconciliation 形成连续证据。 |
| Physical cleanup / no-resurrection | `cleanup_tail` | active caller migration、direct/hosted parity、owner receipt roundtrip、continuous evidence 与 no-active legacy caller scan 稳定后删除旧 wrapper、alias、facade、patch bridge 和 compat aggregate tests。 |

Refs-only ledger verification、request accounting closure、OPL workorder closeout、source ref declaration、schema completeness、scorecard 分数、package existence 或 provider completion 都不能替代真实 workspace / App / provider evidence，也不能声明 grant-ready、fundability-ready、quality-ready、export-ready、submission-ready 或 production-ready。

## 近期完善计划

1. 保持 `agent/` Declarative Grant Pack、stage control plane、contracts、quality gates、memory policy 与当前 source/contract 对齐。
2. 继续把 product/status/user-loop/sidecar/CLI shell 收薄为 refs-only adapter 或 direct handler target；新增能力优先服务 OPL generated/default caller parity。
3. 对 AI-first authority guard 做回归维护：任何 fundability / quality / export / submission-ready claim 必须回到 MAG owner surface 或 AI-backed artifact。
4. 只用持续真实 workspace/App/operator/release evidence 与 Temporal long-soak window evidence 关闭 production evidence tail；refs-only accounting 只进入 ledger/history。
5. 在 active caller 迁出且 no-resurrection guard 成立后，删除或 tombstone 旧 wrapper、alias、facade、patch bridge、compat aggregate test 和 legacy runtime/probe residue；测试改为断言 current contract、schema、CLI/API、manifest、owner receipt、typed blocker、fail-closed 或 tombstone semantics。

## 历史索引

| 内容类型 | 当前落点 |
| --- | --- |
| MAG north-star 目标态 | [Med Auto Grant 理想目标态](../references/med-auto-grant-ideal-state.md) |
| 当前角色、边界、入口、证据门 | [当前状态](../status.md)、[架构概览](../architecture.md)、[不变量](../invariants.md)、[决策记录](../decisions.md) |
| per-surface private platform residue | [MAG 私有实现与 OPL 迁移台账](./opl-private-implementation-migration-inventory.md) |
| 2026-05 receipt proof / closeout 流水 | [MAG standard agent 文档过程归档 2026-05](../history/plans/mag-standard-agent-doc-process-history-2026-05.md) |
| active/support specs 生命周期 | [Specs 索引](../specs/README.md)、[Specs 生命周期地图](../specs/specs_lifecycle_map.md) |
| retired provider / Gateway / local runtime / hosted handoff specs | [历史 specs](../history/specs/README.md) |
| 机器证据与 acceptance refs | `contracts/external_evidence/mag-evidence-receipt-ledger.json`、`contracts/production_acceptance/`、`contracts/runtime-program/current-program.json` |

## 禁止误写

- 不能把 `mag_functional_structure_gap_count=0` 写成 external production/default caller、真实 App/workbench consumption、bridge exit 或 production long-run soak 已完成。
- 不能把 descriptor ready、transition oracle smoke、receipt reconciliation proof、external evidence consumption 或 no-regression evidence 写成 provider SLO / live soak 已完成。
- 不能把 OPL provider completion、matrix runner smoke、package existence、schema completeness、quality scorecard 分数或 controller route 写成 fundability-ready、quality-ready、export-ready 或 submission-ready verdict。
- 不能把 hand-written product-entry / sidecar / grouped CLI/API / projection / lifecycle wrapper 写成长期合理私有平台。
- 不能把 local journal、attempt ledger、Hermes probe、Gateway/local-manager、flat shell alias、compatibility aggregate test 或 `codex_cli` executor 写回默认 runtime owner。
