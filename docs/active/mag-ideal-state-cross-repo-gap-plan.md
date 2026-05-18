# MAG 理想目标态差距与完善计划

Owner: `Med Auto Grant`
Purpose: `ideal_state_gap_plan`
State: `active_plan`
Machine boundary: 本文是人读 gap / completion plan。机器真相继续归 `contracts/`、`schemas/`、源码、CLI/API 行为、product-entry manifest、workspace/runtime artifact root、receipt、质量报告和导出包。
Date: `2026-05-18`

## 文档读法

- 本文只维护 MAG 当前定位、owner 边界、功能/结构差距、测试/证据差距和完善顺序。
- MAG 的 north-star 目标态回到 [Med Auto Grant 理想目标态](../references/med-auto-grant-ideal-state.md)。
- dated 过程校准、follow-through、receipt proof 和 closeout 记录归档到 [MAG standard agent 文档过程归档 2026-05](../history/plans/mag-standard-agent-doc-process-history-2026-05.md)。
- 差距按目标态判断，不按当前 MAG 代码是否仍可运行判断。通用 runtime、runner、queue、session、journal、workspace/source intake、memory/package transport、workbench、observability、CLI/product-entry/sidecar/status wrapper 必须进入 OPL 上收、generated surface 替换、refs-only 收薄或退役分类。

## 当前定位

MAG 是医学基金申请 domain agent，也是 OPL-compatible Foundry Agent package。Direct app skill / CLI / `MedAutoGrantDomainEntry` 是一等入口；OPL-hosted path 可以发现、托管、唤醒和投影 MAG，但必须回到同一套 MAG-owned grant truth、fundability / quality / export verdict、package authority、grant strategy memory accept/reject、owner receipt 和 typed blocker。

OPL Framework / shared family layer 持有通用 provider runtime、typed queue、attempt ledger、generic transition runner、workspace/source shell、memory locator、artifact/package lifecycle shell、operator projection、observability/SLO、generated wrapper 和 App/workbench shell。MAG 不把这些通用能力继续写成长期私有平台。

## 当前边界

MAG 必须持有：

- funding call 解释、profile/task lock、fundability strategy、specific aims 和 proposal route truth。
- grant stage pack、prompt/skill、policy table、domain transition oracle、quality/review/export gate。
- grant strategy memory body、accept/reject decision、writeback receipt 和 owner boundary。
- submission-ready package、gap report、manual portal boundary、package/export authority 和 owner receipt。
- typed blocker、safe action refs、no-forbidden-write guard 和 MAG domain projection refs。

OPL 必须持有：

- stage attempt lifecycle、queue/wakeup、provider workflow、retry/dead-letter、human gate transport 和 attempt ledger。
- generic transition runner、workspace/source shell、memory/artifact locator、package/export lifecycle shell、observability/SLO 和 App/workbench shell。
- CLI/product-entry/sidecar/status/workbench/harness wrapper 的 generated/hosted surface，除非 MAG 明确保留为 direct domain handler、refs-only adapter、authority function 或迁移桥。

## 当前功能/结构差距

当前必须保留：

`mag_functional_structure_gap_count=4`

1. `generated_surface_production_consumption`
   OPL generated / hosted product status、user-loop、sidecar、grouped CLI/API、projection、lifecycle adapter、workbench 和 harness 还没有成为 MAG 生产默认 caller。MAG hand-written shell 仍是迁移桥。

2. `generic_shell_handoff_to_opl`
   workspace/source intake shell、grant strategy memory locator/writeback transport、package/export lifecycle shell、route/quality/status/product wrapper、operator workbench、observability/SLO 和 generic transition runner 仍需由 OPL/App 承接或生成。MAG 只输出 refs、verdict refs、owner receipt、typed blocker 和 safe action metadata。

3. `package_memory_lifecycle_refs_only_thinning`
   MAG 已有 memory receipt projection、package lifecycle handoff、lifecycle receipt bundle 和 receipt reconciliation read surfaces，但它们仍需收薄成 OPL shell 可消费的 refs-only handoff，并切走长期 active caller。

4. `legacy_runtime_journal_probe_cleanup`
   local runtime journal、attempt ledger、upstream Hermes probe、flat shell alias、facade patch bridge、compat aggregate tests 和旧 runtime owner wording 仍需 no-active-caller scan、replacement parity、provenance proof 和 physical cleanup。无 active owner 后直接删除或 tombstone，不保留 compatibility alias。

## 当前测试/证据差距

以下是目标结构边界正确后的证据门，不能替代上面的功能/结构收口：

- 真实 OPL-hosted grant-stage attempt 持续返回 MAG owner receipt、typed blocker 或 no-regression evidence。
- 真实 grant workspace 产生 accepted/rejected grant strategy memory receipt、package/export lifecycle receipt、cleanup/restore/retention receipt 和 owner receipt scaleout。
- OPL/App shell 真实消费 MAG package refs、gap report、manual portal boundary、quality refs、transition oracle refs 和 safe action refs。
- generated surface caller migration 后的 direct/hosted parity、no-forbidden-write、release/dist consumption 和 no-regression proof。
- Temporal provider long SLO、repair cadence 和 live receipt reconciliation。

## 完善顺序

1. `generated_surface_production_consumption`
   让 OPL generated / hosted product-entry、sidecar、status、workbench、CLI/API wrapper 和 harness 成为 MAG 生产消费面。

2. `generic_shell_handoff_to_opl`
   将 workspace/source、memory locator/writeback transport、package/export lifecycle、generic transition runner、operator workbench、observability/SLO 等通用 shell 迁到 OPL/App。

3. `package_memory_lifecycle_refs_only_thinning`
   保留 MAG grant authority 和 owner receipt，把 package/memory/lifecycle projection 收薄成 body-free、artifact-free、refs-only handoff。

4. `legacy_runtime_journal_probe_cleanup`
   对 local runtime journal、attempt ledger、Hermes probe、旧 alias/facade/aggregate tests 做 physical retirement 或 tombstone。

5. `grant_stage_evidence_scaleout`
   在结构收口后推进真实 grant-stage attempt、memory/package/lifecycle receipt、continuous receipt reconciliation、no-forbidden-write 和 provider SLO long soak。

## 当前不能写成

- 不能写成 OPL provider completion、receipt reconciliation proof 或 no-regression evidence 等于 fundability-ready、quality-ready、export-ready 或 production long-run soak。
- 不能写成 MAG 已经是纯知识文件仓；MAG 仍持有 grant authority functions、domain entry、receipt schema/writer、transition oracle、quality/export verdict、package authority、memory accept/reject 和 focused contract tests。
- 不能把 generated surface production consumption、active caller cutover、package/export lifecycle shell、memory/package/lifecycle handoff 或 legacy physical cleanup 写成纯测试/证据缺口。
- 不能把 local journal、attempt ledger、Hermes probe、Gateway/local-manager、flat CLI alias 或 compatibility aggregate test 写回默认 runtime owner。
- 不能为了兼容保留旧模块、旧接口、旧测试、旧 CLI alias、facade 或 wrapper；active caller 迁走后直接删除或进入 history/tombstone。
