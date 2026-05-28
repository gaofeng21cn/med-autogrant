# MAG 理想目标态差距与完善计划

Owner: `Med Auto Grant`
Purpose: `ideal_state_gap_plan`
State: `active_plan`
Machine boundary: 本文是人读 current gap / completion plan。机器真相继续归 `contracts/runtime-program/current-program.json`、contracts、schemas、source、CLI/API 行为、product-entry manifest、workspace/runtime artifact root、runtime receipts、质量报告和导出包。
Date: `2026-05-28`

## 读法

本文是 MAG 当前唯一 active gap / plan 入口。目标态读 [Med Auto Grant 理想目标态](../references/med-auto-grant-ideal-state.md)；当前状态读 [当前状态](../status.md)；per-surface 明细读 [MAG 私有实现与 OPL 迁移台账](./opl-private-implementation-migration-inventory.md)；过程流水读 [MAG standard agent 文档过程归档 2026-05](../history/plans/mag-standard-agent-doc-process-history-2026-05.md)。

差距按理想态判断，不按现有 MAG 代码是否还能运行判断。通用 runtime、runner、queue、session、journal、workspace/source intake、memory/package transport、workbench、observability、generic CLI/product-entry/status wrapper 和旧 product-sidecar wrapper 属于 OPL / shared family layer；MAG 只保留 grant authority、domain handler、refs-only adapter、diagnostic、fixture 或 tombstone。

本文不保存长篇执行 prompt、dated closeout checklist 或 receipt proof 流水。每轮完成后只把当前 truth、剩余 gap、证据门和近期计划折回本文；细节进入合同、history、specs lifecycle map 或提交历史。

## 当前唯一真相

MAG 是医学基金申请 domain agent，也是 OPL-compatible Foundry Agent package。Direct app skill / CLI / `MedAutoGrantDomainEntry` 是一等入口；任务启动后的默认运行驻留是 OPL/Temporal hosted autonomous runtime；`Codex CLI` 是当前第一公民 stage executor。

无论 direct path 还是 OPL-hosted path，执行都必须回到 MAG-owned grant truth、fundability / quality / export verdict、package authority、grant strategy memory accept/reject、owner receipt 和 typed blocker。OPL 持有 Temporal provider runtime、typed queue、attempt ledger、generic transition runner、workspace/source shell、memory locator、artifact/package lifecycle shell、operator projection、observability/SLO、generated wrapper 和 App/workbench shell。

当前机器面必须按下面三条同时读取：

| 信号 | 当前值 | 读法 |
| --- | --- | --- |
| `mag_functional_structure_gap_count` / `standard_agent_source_shape_status` | `0` / `landed` | 这是 contracts/read-model 的结构分类信号，只说明 generic owner intent 已被分类和收薄；不表示 strict source-purity 物理完成、生产切换或 live soak 完成。 |
| `claims_opl_descriptor_source_available` / `claims_opl_replacement_exists` / `claims_domain_repo_physical_delete_authorized` | `true` / `true` / `false` | OPL generated/default caller replacement 与 cutover readiness 已有结构证据；该证据不授权 MAG repo 物理删除 active handler/adapter，也不关闭 App/workbench、production/live caller 或 long-soak 证据。 |
| `claims_all_bridge_exits_complete` / `claims_production_long_run_soak_complete` | `false` | bridge physical deletion 与 Temporal long-soak 仍是 production evidence / cleanup tail。 |

当前 `product_entry*`、`product_entry_parts/*`、`domain_runtime*`、runtime registration、domain-handler、lifecycle、memory/package projection、autonomy loop、status/user-loop shell 与部分 CLI/rendering shell 仍可见于 active source。它们只能按 direct handler、refs-only adapter、minimal grant authority function、diagnostic 或 migration input 读取，不能重新写成 MAG 私有 runtime platform；按 strict purity，它们已进入 OPL replacement-ready / physical-delete-not-authorized 状态。旧 product-sidecar / sidecar CLI wrapper 已从 active caller 口径移除，只能作为 no-resurrection guard 或 history/provenance 词汇出现。

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
| Consumer thinning / refs-only boundary | `landed_with_external_gate` | `mag_consumer_thinning_contract`、domain-handler、receipt projection、lifecycle/package/memory refs 只输出 refs、typed blocker、owner receipt 与 action metadata。 |
| Submission-ready human gate blocker projection | `landed_as_blocker_projection` | `package_and_submit_ready` 的 typed blocker 已显式投影 `submission_ready_export_gate`、MAG human-gate owner、`human_gate_receipt` requirement 与 OPL/provider 不可绕过字段；该 projection 不关闭人工审批，不声明 submission/export/production ready。 |
| External evidence request accounting | `refs_only_closed` | `mag-evidence-receipt-ledger.json` 已记录 7 个 request refs-only close；剩余真实证据门是 `temporal_provider_long_soak_window_evidence` 和持续 no-regression / consumption。 |
| OPL owner-payload response | `return_shape_landed_manifest_consumption_workorder_landed` | `authority owner-payload-response` 现在输出 OPL owner-payload workorder 可消费的 `domain_owner_receipt_refs`、`owner_chain_refs`、`no_regression_evidence_refs`、`typed_blocker_refs`、success / typed-blocker payload path、required return shapes 和 legacy alias；同时暴露逐 stage expected receipt / monitor freshness / runtime event refs summary，并把 source/runtime live-evidence pending 表达为 MAG-owned typed blocker path。Product-entry manifest 默认暴露 `owner_payload_response` 与 `workspace_receipt_scaleout_evidence`，让 OPL/App/operator manifest consumer 可发现该 owner-payload summary；`manifest_consumer_evidence.sustained_consumption_followthrough_workorder` 现在把后续真实 App/operator 或 release default caller payload 需求显式化。`authority receipt-readiness` 仍是当前 MAG-owned receipt refs 前置入口，`submission_ready_export_gate` typed blocker 仍是 blocker，不是 approval 或 ready verdict。 |
| Manifest sustained-consumption payload response | `payload_validation_landed_fail_closed_not_closeout` | `authority manifest-consumption-payload` 校验真实 App/operator 或 release default caller 提交的 sustained-consumption payload，只接受 success refs path 或 typed-blocker path，拒绝未声明 operator payload 字段，并输出 body-free response 给 OPL refs-only record/verify。该入口不生成 operator payload、不创建 MAG owner receipt、不关闭 App sustained-consumption、human gate、submission-ready 或 Temporal long-soak。 |
| Process/history foldback | `landed` | dated closeout、receipt proof、provider/Gateway/local-manager 背景已回到 history/specs/provenance，不再作为 active plan 流水。 |

## 当前完成进度

| Area | 当前进度 | 当前读法 |
| --- | --- | --- |
| Standard OPL Agent source shape | `replacement_ready_physical_delete_not_authorized` | `agent/`、stage control plane、quality gates、pack compiler input 和 MAG owner boundary 已是当前默认语义结构；OPL default-caller replacement/cutover readiness 已观测，但 product/status/user-loop/domain-handler/domain_runtime/autonomy/CLI target 仍作为 handler/adapter target 暂留，不声明 grant-ready、submission-ready、production-ready 或 physical-delete-ready。 |
| Runtime / product shell thinning | `refs_only_handler_target_until_owner_delete_receipt` | product/status/user-loop/domain-handler/domain_runtime 面只能作为 direct handler、refs-only adapter、minimal authority function、diagnostic 或 migration input；不再作为长期 MAG surface 读取。 |
| Evidence accounting | `refs_only_closed_owner_payload_record_verify_followthrough_payload_validation_fail_closed` | MAG evidence request ledger 已闭合 refs-only accounting；`authority owner-payload-response` 已把 MAG owner refs、stage expected receipt / monitor freshness / runtime event refs 和 typed blocker refs 整理成 OPL owner-payload workorder 可记录的 response；4 个 workspace 的 owner receipt、memory accept/reject、package/export lifecycle 和 cleanup/restore/retention lifecycle refs 已形成 repo-tracked scaleout snapshot。Product-entry manifest 默认暴露这些 body-free refs-only / count-only provenance，并通过 `manifest_consumer_evidence` 证明 App/operator 默认 manifest consumer 已消费 owner payload、stage expected receipt payload、workspace scaleout count-only provenance 和 `submission_ready_export_gate` blocker refs；同一 evidence 暴露 sustained consumption follow-through workorder，且 `authority manifest-consumption-payload` 已能按 allowlist 校验真实 payload 或 typed blocker refs、拒绝未声明字段，但该入口不自带 payload 或 closeout。OPL `domain-owner-payload-summary` ledger 已记录并验证 7 条 MAG recommended typed-blocker path receipt，其中 submission gate 仍 human-approval-required，六个 stage expected receipt 仍 source/runtime-live-evidence pending。真实 OPL-hosted grant-stage attempt 持续证据、submission human-gate receipt、App/operator sustained consumption 和 Temporal long soak 仍是证据尾项。 |
| Human gate projection | `explicit_blocker_not_approval` | Submission-ready export human gate 现在作为 MAG-owned typed blocker authority boundary 暴露给 domain-handler 与 receipt reconciliation；真实 human approval receipt 仍未形成。 |
| Docs lifecycle | `single_active_truth_owner` | 本文持有 current truth、gap、计划和下一轮 prompt；历史 proof、receipt 流水和旧路线继续留在 history/specs/provenance。 |

## 功能/结构差距

按 strict standard-agent purity，当前 MAG repo 侧 active source 已完成 replacement-ready 分类，但未获得 physical delete authority。`mag_functional_structure_gap_count=0` 只表示历史合同分类闭合，不代表 active shell 已清零。`generated_surface_bridge_exit`、`legacy_runtime_session_lifecycle_exit`、`package_memory_lifecycle_refs_only_boundary`、`private_authority_ai_first_guard` 和 `physical_morphology_tail` 必须继续守住 OPL generated/default caller 接管证据与 repo-local wrapper 删除门。

当前必须推进或守住的结构项：

1. `package_memory_lifecycle_refs_only_boundary`
   Memory receipt projection、package lifecycle handoff、lifecycle receipt bundle、continuous receipt reconciliation 和 domain-handler export 必须保持 body-free refs、owner receipt、verdict refs、typed blocker 和 safe action metadata，不输出 memory body、grant artifact/private evidence 或 OPL ledger state。

2. `private_authority_ai_first_guard`
   Fundability、quality、export、memory accept/reject 是 AI-first judgment surface；package authority、owner receipt signer 和 grant helper 是 programmatic guard surface。程序只能 validator / materializer / receipt signer / guard / refs projection，不能机械生成 ready verdict。

3. `generated_default_caller_cutover`
   `product_entry_parts/*`、`domain_runtime_parts/*`、runtime registration、autonomy loop/report shell、lifecycle/memory/package helpers、CLI/rendering shell 等 active path 必须持续被合同约束为 handler、refs-only adapter、minimal authority function、diagnostic 或 migration input。default caller、direct/hosted parity、owner receipt roundtrip 与 no-active-caller 证据成立后删除旧 wrapper、alias、facade、patch bridge、compat aggregate test 和 legacy runtime/probe residue；详细 path-level inventory 归 [MAG 私有实现与 OPL 迁移台账](./opl-private-implementation-migration-inventory.md)。

4. `no_resurrection_cleanup_tail`
   已退役 local journal、attempt ledger、Hermes probe、Gateway/local-manager、flat CLI alias、facade patch bridge 和 compatibility aggregate test 不能恢复为 compatibility shim、re-export facade 或 active caller。`physical_skeleton_follow_through.retired_public_command_scan` 已把 `run-local`、`runtime-run`、`runtime-resume`、`probe-upstream-hermes` 对照 `SERVICE_SAFE_DOMAIN_COMMANDS` 与 grouped public CLI catalog 做成 repo-local no-resurrection receipt，并指向 fail-closed negative tests；历史只保留在 `docs/history/**`、tombstone/provenance 或 negative guard。

## 证据差距

以下 gap 只通过真实 external receipt、typed blocker、owner receipt 或 no-regression evidence 关闭；不能反向重开 MAG repo 侧结构缺口：

| Evidence gate | 当前状态 | 关闭条件 |
| --- | --- | --- |
| OPL-hosted grant-stage attempt | `needs_continuous_real_attempts` | 真实 OPL-hosted stage attempt 持续返回 MAG owner receipt、typed blocker 或 no-regression evidence。 |
| Package stage source/runtime evidence | `blocked_by_submission_gate_typed_blocker` | `package_and_submit_ready` stage production evidence 已被 OPL external evidence ledger verified；App/operator 读到 source scope 与 runtime event observed，expected receipt / monitor freshness 仍由 `submission_ready_export_gate` typed blocker 阻塞。关闭条件仍是真实 MAG owner human-gate receipt 或可重复 no-regression / monitor freshness evidence，不是 OPL receipt 本身。 |
| Real workspace memory/package/lifecycle scaleout | `refs_only_scaleout_observed_owner_payload_recorded_followthrough_open` | 4 个 MAG workspace 样本已通过 MAG-owned owner receipt、memory accept/reject receipt、package/export lifecycle handoff 与 cleanup/restore/retention lifecycle receipt surface 形成 36 条 body-free receipt refs，并进入 `owner-payload-response`；同一 response 已暴露 6-stage expected receipt payload summary，供 OPL/App 读取 success refs path 或 typed-blocker path。OPL 已验证 7 条 owner-payload-summary typed-blocker path receipt，证明外部 workorder 可消费这些 body-free blocker refs；关闭条件仍要求真实 owner human-gate receipt、持续 App/operator consumption、long-soak 与 no-regression follow-through，不能把 refs-only scaleout 或 OPL ledger verification 写成 artifact authority、quality/export verdict 或 production ready。 |
| Submission-ready human gate receipt | `blocked_on_real_human_gate_receipt` | `submission_ready_export_gate` typed blocker 已可机读；关闭条件仍是真实 MAG owner human-gate receipt 或人工审批路径证据。 |
| App/operator/release consumption | `payload_validation_fail_closed_sustained_consumption_open` | Product-entry manifest 已默认暴露 `owner_payload_response` 与 `workspace_receipt_scaleout_evidence`，让 OPL/App/operator default manifest path 可发现 MAG owner-payload summary；`manifest_consumer_evidence` 已固定默认 manifest consumer 消费的 refs、counts 和 human-gate blocker path，并提供 `sustained_consumption_followthrough_workorder`。`authority manifest-consumption-payload` 现在可按 allowlist 校验真实 `app_operator_consumption_ref`、`default_caller_consumption_ref`、owner payload / workspace scaleout refs、no-forbidden-write ref 与 long-soak 或 typed blocker ref，或接收 App/operator typed blocker path，并对未声明字段 fail-closed；该 validation 只形成 body-free refs response，不声明成功。OPL `domain-owner-payload-summary` ledger 已把 7 条 MAG typed-blocker path 记录并验证为 refs-only receipt；关闭条件仍是 OPL/App/operator closeout、executor-first bundle、release/default caller 持续消费 MAG package refs、quality refs、manual portal boundary、transition oracle refs、safe action refs 和 `authority owner-payload-response` 的 owner receipt success refs path、stage expected receipt / monitor freshness / runtime event refs、typed-blocker payload path。 |
| Temporal provider long soak | `open` | `temporal_provider_long_soak_window_evidence`、long SLO、repair cadence 和 live receipt reconciliation 形成连续证据。 |
| Physical cleanup / no-resurrection | `replacement_ready_delete_authority_open` | repo-local active path scan 与 retired public command scan 已形成 no-resurrection 结构输入；production default caller、direct/hosted parity、owner receipt roundtrip、continuous evidence、App/workbench consumption 与 no-active legacy caller scan 仍未授权删除 active handler/adapter shell。删除旧 wrapper、alias、facade、patch bridge 和 compat aggregate tests 仍需要 explicit MAG owner receipt authorizing physical delete。 |

Refs-only ledger verification、request accounting closure、OPL workorder closeout、source ref declaration、schema completeness、scorecard 分数、package existence 或 provider completion 都不能替代真实 workspace / App / provider evidence，也不能声明 grant-ready、fundability-ready、quality-ready、export-ready、submission-ready 或 production-ready。

## 近期完善计划

1. 保持 `agent/` Declarative Grant Pack、stage control plane、contracts、quality gates、memory policy 与当前 source/contract 对齐。
2. 保持 product/status/user-loop/domain-handler/CLI shell 的 refs-only adapter 或 direct handler target 边界；新增能力优先服务 OPL generated/default caller parity，不扩写 MAG-owned shell。
3. 对 AI-first authority guard 做回归维护：任何 fundability / quality / export / submission-ready claim 必须回到 MAG owner surface 或 AI-backed artifact。
4. 只用持续真实 workspace/App/operator/release evidence 与 Temporal long-soak window evidence 关闭 production evidence tail；refs-only accounting 和 workspace receipt scaleout snapshot 只进入 ledger/history 或 body-free production-acceptance snapshot。
5. 在 production default caller 与 no-resurrection guard 成立后，删除旧 wrapper、alias、facade、patch bridge、compat aggregate test 和 legacy runtime/probe residue；需要追溯只留 history/provenance，测试改为断言 current contract、schema、CLI/API、manifest、owner receipt、typed blocker、fail-closed 或 tombstone semantics。

## 下一轮 Agent prompt

Objective:

- 继续治理 `/Users/gaofeng/workspace/med-autogrant` 的 MAG 标准 OPL Agent production evidence / default caller / no-resurrection 尾项；保持 grant authority 留在 MAG，通用 runtime / generated/default caller 留在 OPL。

Write scope:

- `docs/active/mag-ideal-state-cross-repo-gap-plan.md`、`docs/status.md`、`docs/active/opl-private-implementation-migration-inventory.md`、MAG contracts/source/tests 中仍影响 owner boundary、generated/default caller 或 no-resurrection 的 surface。

Live truth inputs:

- `AGENTS.md`、`TASTE.md`、核心五件套、本文、MAG ideal-state reference。
- `contracts/runtime-program/current-program.json`、functional/private surface contracts、owner receipt / memory / package / lifecycle contracts、domain-handler/product-entry/action metadata。
- Focused pytest、`scripts/verify.sh`、OPL `agents interfaces --domain mag --json`、OPL framework readiness / App drilldown 中 MAG refs-only evidence 读面。

Required actions:

- 核实 production default caller、App/workbench consumption、direct/hosted parity、owner receipt roundtrip、Temporal long-soak 与 no-resurrection 证据。
- 若 default caller / receipt / no-active-caller proof 成立，直接删除、archive 或 tombstone 旧 wrapper、alias、facade、patch bridge 和 compatibility aggregate test。
- 把已关闭项折回本文或核心五件套；把 proof 流水折回 history/provenance。

Non-goals:

- 不把 scorecard、schema completeness、package existence、provider completion、queue completion 或 refs-only accounting 写成 fundability-ready、grant-ready、quality-ready、export-ready、submission-ready 或 production-ready。
- 不把 memory body、grant artifact/private evidence、owner receipt authority 或 quality verdict 上收到 OPL。
- 不新增 compatibility shim、facade、alias 或旧 runtime/probe fallback。

Verification commands:

- Docs-only：`rtk git diff --check`、`rtk rg -n "<<<<<<<|>>>>>>>|=======" docs`。
- 触及 source/contracts/tests：`rtk ./scripts/verify.sh` 或相关 focused `rtk python -m pytest ...`。

Completion gate:

- Current plan 只保留 still-open gap 和下一步；closed gap 已重写为完成进度或移入 history/provenance。
- main checkout 上完成触及面验证；worktree/branch 已吸收清理，或明确因近期写入/未提交改动保留。

Foldback target:

- Durable current truth 折回本文、核心五件套、private inventory 或 machine-readable contracts；过程命令、receipt id、旧路线和 closeout 流水进入 `docs/history/**`、ledger 或提交历史。

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

- 不能把 `mag_functional_structure_gap_count=0` 写成 strict source-purity 完成、external production/default caller、真实 App/workbench consumption、bridge exit 或 production long-run soak 已完成。
- 不能把 descriptor ready、transition oracle smoke、receipt reconciliation proof、external evidence consumption 或 no-regression evidence 写成 provider SLO / live soak 已完成。
- 不能把 OPL provider completion、matrix runner smoke、package existence、schema completeness、quality scorecard 分数或 controller route 写成 fundability-ready、quality-ready、export-ready 或 submission-ready verdict。
- 不能把 hand-written product-entry / old product-sidecar / grouped CLI/API / projection / lifecycle wrapper 写成长期合理私有平台。
- 不能把 local journal、attempt ledger、Hermes probe、Gateway/local-manager、flat shell alias、compatibility aggregate test 或 `codex_cli` executor 写回默认 runtime owner。
