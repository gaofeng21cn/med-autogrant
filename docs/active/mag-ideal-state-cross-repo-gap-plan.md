# MAG 理想目标态差距与完善计划

Owner: `Med Auto Grant`
Purpose: `ideal_state_gap_plan`
State: `active_plan`
Machine boundary: 本文是人读 gap / completion plan。机器真相继续归 `contracts/`、`schemas/`、源码、CLI/API 行为、product-entry manifest、workspace/runtime artifact root、receipt、质量报告和导出包。
Date: `2026-05-23`

## 读法

本文只维护 MAG 当前定位、owner 边界、功能/结构差距、测试/证据差距和完善顺序。MAG north-star 目标态回到 [Med Auto Grant 理想目标态](../references/med-auto-grant-ideal-state.md)。过程性校准、receipt proof、closeout 流水和一次性 lane 记录归档到 [MAG standard agent 文档过程归档 2026-05](../history/plans/mag-standard-agent-doc-process-history-2026-05.md) 或提交历史。

差距按目标态判断，不按当前 MAG 代码是否仍可运行判断。通用 runtime、runner、queue、session、journal、workspace/source intake、memory/package transport、workbench、observability、CLI/product-entry/sidecar/status wrapper 必须进入 OPL 上收、generated surface 替换、refs-only 收薄或退役分类。过时模块、接口、测试、fixture、CLI alias、facade、wrapper 和 docs 入口不保留兼容面。

当前 source scan 确认：`product_entry*`、`product_entry_parts/*`、`domain_runtime*`、runtime registration、sidecar、lifecycle、memory/package projection、status/user-loop shell 仍是 active source；它们只能作为 direct handler、refs-only adapter、minimal grant authority function、diagnostic、migration input 或 tombstone/provenance 支撑读取。旧 local journal、attempt ledger、scheduler daemon、Hermes/Gateway/local-manager probe、flat alias、patch bridge、compat aggregate test 和旧 hosted/provider specs，一旦 active caller 迁出且 direct/hosted parity、owner receipt roundtrip、no-resurrection guard 成立，直接删除、archive 或 tombstone，不保留 compatibility shim。

本文是 MAG 的 single Active Truth plan。`docs/active/README.md` 只做索引，`opl-private-implementation-migration-inventory.md` 只做 physical morphology 明细台账；二者不另建进度、差距或下一轮 prompt。若未来新增 active packet，完成后必须折回本文、核心五件套或 `docs/history/**`，不能在 active path 保留执行流水。

模板映射：

| Active Truth section | 本文落点 |
| --- | --- |
| Ideal-state reference | `读法`、`当前定位` 与 [Med Auto Grant 理想目标态](../references/med-auto-grant-ideal-state.md) |
| Current completion progress | `当前完成进度`、`当前结构收口状态` |
| Functional / structural gaps | `功能/结构差距`、`当前物理源码形态差距`、`Retained Private Authority Surfaces` |
| Test / evidence gaps | `测试/证据差距` |
| Next-round agent prompt | `下一轮 /goal prompt` |
| History / tombstone foldback | `历史 / tombstone 折返`、[MAG standard agent 文档过程归档 2026-05](../history/plans/mag-standard-agent-doc-process-history-2026-05.md) |

## 当前定位

MAG 是医学基金申请 domain agent，也是 OPL-compatible Foundry Agent package。Direct app skill / CLI / `MedAutoGrantDomainEntry` 是一等入口；任务启动后的默认运行驻留是 OPL/Temporal hosted autonomous runtime。OPL-hosted path 与 direct path 必须回到同一套 MAG-owned grant truth、fundability / quality / export verdict、package authority、grant strategy memory accept/reject、owner receipt 和 typed blocker。

OPL Framework / shared family layer 持有通用 provider runtime、typed queue、attempt ledger、generic transition runner、workspace/source shell、memory locator、artifact/package lifecycle shell、operator projection、observability/SLO、generated wrapper 和 App/workbench shell。MAG 不把这些通用能力继续写成长期私有平台。

当前 product-entry manifest / schema / tests 的 runtime contract 字段为 `opl_provider_runtime_contract`。该字段指向 OPL/configured family provider runtime owner；`codex_cli` 只保留为默认 executor owner / default executor，不再作为 active runtime owner。

## 当前完成进度

| Area | 当前状态 | 当前证据 | 说明 |
| --- | --- | --- | --- |
| Identity / owner boundary | `done` | 核心五件套、`contracts/runtime-program/current-program.json` | MAG 是 grant domain agent；OPL/Temporal 是默认 task runtime owner；MAG 保留 grant authority。 |
| Declarative Grant Pack | `done_with_evidence_tail` | `agent/`、contracts、stage control plane、quality gates | repo-source semantic pack 已作为 OPL pack compiler / generated surface 输入；后续证据看真实 generated/default caller 消费。 |
| MAG retained authority | `done_with_guard_tail` | `runtime/authority_functions/`、owner receipt / typed blocker / quality/export refs | grant truth、fundability / quality / export verdict、package authority、memory accept/reject 和 owner receipt 留在 MAG；程序面只做 guard、materialize、receipt、refs projection。 |
| Product/status/user-loop/sidecar shell | `partial_migration_input` | `product_entry*`、`product_entry_parts/*`、sidecar、status/user-loop shell、product-entry manifest | 当前仍可作为 direct handler 或 refs-only adapter；长期 default shell 归 OPL generated/hosted surface。 |
| Runtime/session/lifecycle residue | `retirement_tail` | `domain_runtime*`、runtime registration、lifecycle / memory / package projection | 只能按 route/authority adapter、diagnostic、migration input 或 tombstone 阅读；不能重建 MAG-owned generic runtime。 |
| External evidence / production soak | `evidence_gap` | external evidence ledger、production acceptance refs、`product receipt-readiness` | first live production evidence refs 已被 external ledger 全部 refs-only close；真实 workspace scaleout、持续 App/workbench / release-default caller consumption、Temporal long-soak window 和 production SLO 仍需连续证据。 |

## 当前结构收口状态

当前机器状态：

`mag_functional_structure_gap_count=0`

该值只表示 MAG repo 侧当前 surface 已收到 handler / refs-only / authority 边界。它不表示：

- OPL generated/hosted production default caller 已完成生产 cutover；
- 真实 App/workbench 用户路径已完成持续 production consumption；
- 全部 bridge exit 已完成；
- production long-run soak 或 Temporal long-soak window evidence 已关闭；
- MAG 已经变成纯 knowledge pack；
- physical source tree 已完全变成新建标准 Agent 模板。

当前 `claims_opl_replacement_exists=false`、`claims_all_bridge_exits_complete=false`、`claims_production_long_run_soak_complete=false` 仍是 active evidence gates。Production acceptance tail 与 external evidence request accounting 的具体 refs 由机器合同维护，不在本文重复。

## MAG 必须保留的 authority

MAG 必须持有：

- funding call 解释、profile/task lock、fundability strategy、specific aims 和 proposal route truth；
- grant stage pack、prompt/skill、policy table、domain transition oracle、quality/review/export gate；
- grant strategy memory body、accept/reject decision、writeback receipt 和 owner boundary；
- submission-ready package、gap report、manual portal boundary、package/export authority 和 owner receipt；
- typed blocker、safe action refs、no-forbidden-write guard 和 MAG domain projection refs。

这些 authority 不迁给 OPL，也不能由 schema completeness、scorecard 分数、package existence、provider completion、queue completion 或 controller route 机械生成 ready verdict。

## 功能/结构差距

当前功能/结构差距已经从“未分类大块功能”收敛为以下 owner / shape tail：

1. `generated_surface_bridge_exit`
   Product/status/user-loop/sidecar/grouped CLI/projection/lifecycle surface 当前仍可作为 MAG direct handler 或 refs-only adapter 存在。目标是 OPL generated/hosted caller 成为 default product/status/workbench/sidecar shell；MAG 只保留 grant handler target、owner receipt、typed blocker、verdict refs 与 action metadata。

2. `legacy_runtime_session_lifecycle_exit`
   Local runtime journal / attempt ledger、repo-owned scheduler daemon、upstream Hermes probe、flat shell alias、facade patch bridge 和 compat aggregate test 只允许作为 legacy proof / tombstone / regression oracle。无 active caller 后删除或归档，不新增旧兼容别名。

3. `package_memory_lifecycle_refs_only_boundary`
   Memory receipt projection、package lifecycle handoff、lifecycle receipt bundle、continuous receipt reconciliation 和 sidecar export 只输出 body-free refs、owner receipt、verdict refs、typed blocker 和 safe action metadata；不输出 memory body、grant artifact/private evidence 或 OPL ledger state。

4. `private_authority_ai_first_guard`
   Fundability、quality、export、package、memory、transition oracle、owner receipt 和 grant helper 是 MAG retained authority。AI-first judgment 必须来自 grant stage artifact 或 AI critique artifact；程序只做 validator、materializer、receipt signer、guard 和 refs projection。

5. `contract_source_ref_refresh`
   privatized audit、generated-surface handoff 和 consumer/thinning contract 中的 code path / source_ref 必须与当前 physical source tree 对齐。漂移路径只能进入 source-ref refresh、history/provenance 或 tombstone，不能用漂移路径证明当前状态。

6. `physical_morphology_tail`
   product-entry、sidecar、domain_runtime、runtime/lifecycle/workbench 命名必须持续被合同约束为 domain handler、refs-only adapter、minimal authority function、diagnostic 或 tombstone；不能让命名重新表达 MAG-owned generic runtime。

当前直接退役优先级：

| surface | 当前实际状态 | 下一步动作 |
| --- | --- | --- |
| `product_entry*` / product status / user-loop / sidecar export | active direct path 与 OPL handoff 输入仍存在。 | OPL generated product/status/workbench/sidecar shell 成为 default caller 后，只保留 grant handler target、owner receipt、typed blocker、quality/export refs；删除旧 wrapper 与只保护旧输出的测试。 |
| `domain_runtime*` / runtime registration / control-plane projection | 仍是 route / authority adapter 与 regression oracle 形态。 | 不再扩写 generic runtime substrate；replacement parity 成立后删除或 tombstone runtime/session/journal/probe envelope。 |
| lifecycle / memory / package projection helpers | 当前输出 body-free refs、receipt、typed blocker 或 action metadata。 | OPL lifecycle/session/workbench caller 稳定后迁出 generic envelope，只保留 MAG package / memory / owner authority function。 |
| autonomy loop / report-resume shell | 当前只能作为 grant route / budget / blocker policy thin handler 或 OPL attempt lifecycle 迁移输入。 | OPL generated operator loop / attempt lifecycle 接管后删除 generic loop/scheduler-like envelope。 |
| legacy alias / facade / patch bridge / compat aggregate tests | 只允许 history、tombstone、explicit proof history 或 regression oracle。 | active caller 清零后删除源码、CLI/API 入口和旧 aggregate test；保留测试只断言 current contract、no-resurrection、fail-closed 或 tombstone guard。 |

## 测试/证据差距

以下证据门单独统计，不能反向重开 MAG repo 侧 active bridge exit：

- 真实 OPL-hosted grant-stage attempt 持续返回 MAG owner receipt、typed blocker 或 no-regression evidence。
- 真实 grant workspace 产生 accepted/rejected memory receipt、package/export lifecycle receipt、cleanup/restore/retention receipt 和 owner receipt scaleout。
- `product receipt-readiness` grouped CLI 已可把 owner receipt、memory accept/reject receipt、package/export lifecycle handoff 和 cleanup/restore/retention lifecycle receipt refs 聚合成 body-free readiness projection；后续证据门是 OPL/App/operator closeout 与 executor-first bundle 在真实 workspace 中持续消费该 projection 并回连 owner-chain / typed blocker / no-regression refs，不能把该入口本身写成 grant ready、quality ready、export ready、submission ready 或 production ready。
- MAG grant-stage / lifecycle / legacy route-back payload 已可被 OPL refs-only external evidence ledger 记录并验证：coverage 包括 grant stage owner receipt / owner-chain refs、`package_and_submit_ready` lifecycle typed blocker refs，以及旧 `autonomy-controller/guarded-run` route-back typed blocker。当前 active plan 不保存具体 attempt、receipt path 或 worklist 数字；这些过程证据归 OPL ledger、提交历史和 [MAG standard agent 文档过程归档 2026-05](../history/plans/mag-standard-agent-doc-process-history-2026-05.md)。该进展只收窄 dispatch accounting、旧 route-back 和 lifecycle blocker consumption，不关闭真实 grant workspace memory/package/lifecycle receipt scaleout、App user path、Temporal long-soak、fundability / quality / export verdict 或 submission-ready gate。
- External evidence ledger 已 refs-only close 7 个 request：generated/hosted caller pack consumption、App/workbench package refs consumption、release/dist consumption、owner receipt / typed blocker roundtrip、continuous no-forbidden-write、direct/hosted parity no-regression 和 Temporal receipt reconciliation ref。该 closeout 不把 refs-only accounting 升级为 grant-ready、quality-ready、export-ready、submission-ready、production-ready 或 Temporal long-soak complete。
- OPL/App shell 持续消费 MAG package refs、gap report、manual portal boundary、quality refs、transition oracle refs 和 safe action refs。
- External production/default caller、release/dist consumption、continuous no-forbidden-write 和 direct/hosted parity 已有首批 refs-only evidence；后续门槛是持续真实 workspace/App/operator/release consumption 与 no-regression evidence。
- Temporal provider 已记录 receipt reconciliation ref；后续门槛是 `temporal_provider_long_soak_window_evidence`、long SLO、repair cadence 和 live receipt reconciliation 的连续证据。
- Physical morphology cleanup 在 active caller migration、direct/hosted parity、owner receipt roundtrip、continuous evidence 和 no-active legacy caller / no-resurrection scan 稳定后继续推进；满足门槛即删除旧 wrapper、alias、facade、patch bridge 和 compat aggregate tests，不保留 compatibility shim。

这些 gap 只能通过真实 external receipt、typed blocker 或 no-regression evidence 关闭。Request accounting closure、refs-only ledger verification、OPL workorder closeout 或 source ref declaration 不能替代真实 workspace / App / provider evidence。

## 当前物理源码形态差距

这部分是 physical morphology hygiene tail，不能被 `mag_functional_structure_gap_count=0` 或 OPL cleanup ledger apply/verify 写成已经完成。

- `product_entry_parts/*`、product status、grant progress / cockpit / direct-entry / user-loop 与 sidecar export 仍是 repo-local wrapper 形态；目标是 OPL generated product/status/workbench/sidecar shell 成为 production/default caller。
- `domain_runtime_parts/*`、`domain_entry.py` 和 grouped CLI command catalog 仍容易被读成 MAG runtime substrate；目标是保持 route/authority adapter 与 regression oracle，不持有 generic runner、queue、attempt ledger 或 session shell。
- `runtime_registration.py`、control plane、lifecycle receipt bundle、memory/package projection 和 owner receipt helper 只允许输出 body-free refs、receipt、typed blocker 或 action metadata；目标是 OPL lifecycle/session/workbench caller 稳定后迁出 generic envelope。
- autonomy controller 只能作为 grant route / budget / blocker policy 的 thin direct handler；generic loop/scheduler-like envelope、report/resume envelope 和 operator-loop report shell 是 OPL attempt lifecycle / generated operator loop 的迁移输入。

详细 per-surface inventory 见 [MAG 私有实现与 OPL 迁移台账](./opl-private-implementation-migration-inventory.md)。

## Retained Private Authority Surfaces

| Authority surface | Work mode | Judgment owner | 程序角色 |
| --- | --- | --- | --- |
| `fundability_verdict` | AI-first judgment | grant-review / fundability stage artifact 判断 call fit、applicant evidence 和 reviewer risk。 | validator / verdict ref materializer |
| `quality_verdict` | AI-first judgment | AI-authored critique、quality closure dossier 或 reviewer artifact；scorecard 不能单独给出 ready。 | aggregator / guard |
| `export_verdict` | AI-first judgment | package/export stage artifact；artifact existence 或 generic lifecycle completion 不能声明 submission-ready。 | package gate ref validator |
| `memory_accept_reject` | AI-first judgment | grant strategy memory stage 判断 memory 对 fundability / quality 的意义。 | receipt writer / refs projection |
| `package_authority` | Programmatic guard | MAG owner receipt 或 package stage authority。 | materializer / receipt signer |
| `owner_receipt_signer` | Programmatic guard | MAG receipt schema 与 domain provenance。 | receipt signer |
| `grant_helper` | Programmatic guard | deterministic grant metadata、route 和 blocker policy。 | helper implementation / guard |

## 完善顺序

1. 保持 `agent/` Declarative Grant Pack、contracts、stage control plane、quality gates 和 memory policy 与当前 source/contract 对齐。
2. 继续把 hand-written product/status/user-loop/sidecar/CLI shell 降为 refs-only adapter 或 direct handler target；新增能力优先服务 OPL generated/default caller parity。
3. 继续维护 AI-first authority guard：任何 fundability / quality / export / submission-ready claim 必须回到 MAG owner surface 或 AI-backed artifact。
4. 保持 first live production evidence refs 的 refs-only closeout 与 active source/contract 对齐；后续只用持续真实 workspace/App/operator/release evidence 和 Temporal long-soak window evidence 关闭 production evidence tail。
5. 在 active caller 迁出且 no-resurrection guard 成立后，删除或 tombstone 旧 wrapper、alias、facade、patch bridge、compat aggregate test 和 legacy runtime/probe residue；测试同步改成 current machine contract、schema、CLI/API、manifest、owner receipt、typed blocker、fail-closed 或 tombstone semantics，不维护旧调用路径。

## 下一轮 /goal prompt

Objective:

使用 OPL Doc Governance 继续推进 MAG standard OPL Agent 收敛。以 `/Users/gaofeng/workspace/med-autogrant` 为唯一写入范围，重读 `AGENTS.md`、`TASTE.md`、`README*`、`docs/README.md`、核心五件套、`docs/references/med-auto-grant-ideal-state.md`、本文、`docs/active/opl-private-implementation-migration-inventory.md`、`contracts/runtime-program/current-program.json`、product-entry manifest / external evidence / production acceptance contracts、相关 source/tests；根据 live repo truth 更新本文的当前完成进度、功能/结构差距、测试/证据差距，并把 completed process fold back 到核心文档或 `docs/history/**`。

Write scope:

- MAG 本仓文档、contracts、schemas、source、tests 中与 generated/default caller parity、refs-only adapter thinning、AI-first authority guard、evidence gate 或 stale active wording 直接相关的文件。
- 首选更新 `docs/active/mag-ideal-state-cross-repo-gap-plan.md`，必要时同步核心五件套、`docs/specs/README.md`、`docs/specs/specs_lifecycle_map.md`、`docs/history/**` 和相关 machine-readable contracts/tests。

Non-goals:

- 不修改 `/Users/gaofeng/workspace/one-person-lab`、MAS、RCA 或其他 repo。
- 不把 OPL generic scheduler、runner、queue、attempt ledger、session store、workbench、observability/SLO 或 App shell 实现在 MAG。
- 不新增旧兼容别名、re-export facade、flat CLI alias、compat aggregate test 或旧 runtime/probe wrapper。
- 不把 refs-only ledger verification、schema completeness、scorecard 分数、provider completion 或 package existence 写成 fundability-ready、quality-ready、export-ready、submission-ready、production-ready 或 Temporal long-soak complete。

Live truth inputs:

- `contracts/runtime-program/current-program.json`
- `contracts/external_evidence/mag-evidence-receipt-ledger.json`
- `contracts/production_acceptance/mag-production-acceptance.json`
- `agent/` Declarative Grant Pack、`runtime/authority_functions/`、`src/med_autogrant/**`、`tests/**`
- `docs/status.md`、`docs/architecture.md`、`docs/invariants.md`、`docs/decisions.md`、本文与 private implementation inventory
- fresh doctor output: `python3 /Users/gaofeng/workspace/opl-doc-governance/scripts/opl_doc_doctor.py doctor . --format json`

Required actions:

- 先确认 current active caller、direct/hosted parity、owner receipt roundtrip、no-resurrection guard 与 evidence ledger 状态，再决定是否删除、tombstone 或继续收薄旧 wrapper / alias / facade / runtime residue。
- 若有新的真实 OPL/App/production caller 或 Temporal long-soak window 证据，关闭对应测试/证据 gap；若只是 refs-only accounting、preflight、workorder 或 process closeout，保留为 evidence tail，不重开 MAG repo 侧结构缺口。
- 若修改公开边界、machine-readable contract、command surface 或 default runtime/executor wording，同步更新核心五件套、contracts/schema/source/tests 和 specs lifecycle guard。
- 每轮完成后重写本文：closed gap 删除或改写为当前进度，过程证据进入 `docs/history/**` 或外部 ledger，下一轮 prompt 只保留剩余 work。

Verification commands:

```bash
python3 /Users/gaofeng/workspace/opl-doc-governance/scripts/opl_doc_doctor.py doctor . --format json
./scripts/verify.sh
```

Completion / foldback gate:

- doctor 不再报告本轮应处理的 stale active wording；若只剩 reference header 信息项，明确说明为何不机械补齐。
- `scripts/verify.sh` 通过，且开发 checkout 不产生 `.venv`、`__pycache__`、`.pytest_cache` 或 `*.egg-info` 副产物。
- 本文保留唯一 active truth owner 地位；active path 不保存完成流水或重复计划。
- 所有旧 Hermes/Gateway/local-manager/旧前门/兼容词汇都被改写为 current owner truth、history/provenance 或 tombstone 读法。
- 最终在当前 `main` 上提交，提交信息按任务要求使用 `docs: refresh active truth governance`。

## 历史 / tombstone 折返

- 过程性校准、receipt proof、closeout 流水和一次性 worklist 归 [MAG standard agent 文档过程归档 2026-05](../history/plans/mag-standard-agent-doc-process-history-2026-05.md)、external evidence ledger 或提交历史。
- 旧 local runtime journal / attempt ledger、repo-owned scheduler daemon、upstream Hermes probe、Gateway/local-manager path、flat shell alias、facade patch bridge、compat aggregate test 和旧 hosted/provider specs 只作为 history、tombstone、explicit proof history 或 regression oracle 阅读。
- No-resurrection guard：active docs、contracts、tests 和 command catalog 不新增旧 alias/facade/wrapper；若历史文件仍含旧词，必须有 lifecycle note 或 history path，不能作为 current owner surface。

## 禁止误写

- 不能把 `mag_functional_structure_gap_count=0` 写成 external production/default caller、真实 App/workbench consumption 或 production long-run soak 已完成。
- 不能把 descriptor ready、transition oracle smoke、receipt reconciliation proof、external evidence consumption 或 no-regression evidence 写成 provider SLO / live soak 已完成。
- 不能把 OPL provider completion、matrix runner smoke、package existence、schema completeness、quality scorecard 分数或 controller route 写成 fundability-ready、quality-ready、export-ready 或 submission-ready verdict。
- 不能把 hand-written product-entry / sidecar / grouped CLI/API / projection / lifecycle wrapper 写成长期合理私有平台。
- 不能把 local journal、attempt ledger、Hermes probe、Gateway/local-manager、flat CLI alias、compatibility aggregate test 或 `codex_cli` executor 写回默认 runtime owner。
