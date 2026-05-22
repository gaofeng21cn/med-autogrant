# MAG 私有实现与 OPL 迁移台账

Owner: `Med Auto Grant`
Purpose: `opl_private_implementation_migration_inventory`
State: `active_inventory`
Machine boundary: 本文是 human-readable 迁移治理台账。机器真相继续归 `contracts/`、schemas、CLI/API 行为、product-entry manifest、sidecar export/dispatch、runtime receipts、workspace artifact 与 MAG owner receipt。
Date: `2026-05-22`

## 读法

本文只维护当前 private-platform residue 的分类、active caller、MAG 必须保留的 authority、可上收到 OPL 的 generic 子域和退役门槛。它不保存逐日拆文件 closeout、line-count ledger 或 receipt/proof 流水；这些过程记录进入 `docs/history/**` 或代码提交历史。当前功能/结构差距、测试/证据差距和执行顺序仍由 [MAG 理想目标态差距与完善计划](./mag-ideal-state-cross-repo-gap-plan.md) 维护。

## 当前 clean truth

MAG 是 OPL-compatible grant domain agent。OPL Framework 持有通用 provider runtime、queue、attempt ledger、generic transition runner、workspace/source shell、memory locator、artifact/package lifecycle shell、generated wrapper、observability/SLO 和 App/workbench shell。MAG 必须保留 grant truth、fundability / quality / export verdict、package authority、grant strategy memory body 与 accept/reject decision、owner receipt、transition oracle、typed blocker 和 grant-native helper。

当前风险集中在 hand-written product-entry / sidecar / CLI / autonomy controller / domain-runtime 命名和聚合文件，容易被误读成 MAG 私有平台。所有这类 surface 只能按 direct domain handler、refs-only adapter、minimal authority function、diagnostic、migration input 或 history/tombstone 读取。

## 分类词表

| Class | 含义 |
| --- | --- |
| `domain_authority_retained` | MAG 必须保留的 grant truth、AI-first verdict、package/memory/receipt authority 或 grant-native helper。 |
| `opl_framework_migration_candidate` | 当前手写外壳长期应由 OPL generated/hosted surface 或 shared primitive 承担。 |
| `already_thin_adapter` | 已收薄为 refs-only adapter/projection/diagnostic，仍因 direct path 或 evidence caller 暂留。 |
| `legacy_proof_tombstone` | 已退役或只作 regression/provenance 的旧 runtime、probe、alias、patch bridge 或 compat surface。 |

## 当前 Inventory

| Surface family | Current active caller | 当前分类 | MAG 必须保留的 authority | 可迁往 OPL 的 generic 子域 | 迁移/退役门槛 |
| --- | --- | --- | --- | --- | --- |
| `product_entry_parts/manifest_builder*` | product-entry manifest/status、direct entry、sidecar export、product-entry tests | `already_thin_adapter` + `opl_framework_migration_candidate`；`shell_assembly.py` 与 `runtime_task_shell.py` 已把 product/status/user-loop shell、runtime inventory、task lifecycle、automation companion 从入口拆出，`manifest_builder.py` 继续只作为 manifest orchestration 迁移输入 | grant workspace/mainline refs、route verification refs、domain memory refs、receipt refs、transition oracle refs、quality/export verdict refs | generated product-entry/status/workbench manifest shell、App operator projection shell、family product-entry manifest assembly、runtime inventory / task lifecycle / automation companion 默认 caller | OPL generated/default caller 消费同一 pack/action/stage refs；direct/hosted parity、owner receipt/typed blocker roundtrip、no-forbidden-write 关闭后删除或 tombstone MAG handwritten shell。当前拆分不声明 OPL production default caller 已接管。 |
| `product_entry_parts/sidecar*` | `product sidecar export|dispatch`、OPL family provider bridge、sidecar tests | `already_thin_adapter` + `opl_framework_migration_candidate`；`sidecar_shell_projection.py` 已承接 caller/substrate/control-plane/todo/attention 等 generic shell projection assembly，`sidecar.py` 继续只组装 manifest 与 MAG authority refs | package authority refs、grant memory accept/reject receipt、owner receipt、typed blocker、safe action metadata | generated sidecar wrapper、typed queue dispatch shell、generic lifecycle/memory/package transport envelope、App workbench sidecar projection | 仍需 OPL generated/hosted sidecar caller evidence、owner receipt roundtrip、direct/hosted no-regression、no-active compat alias；当前不声明 OPL 已完全接管，也不迁移 grant truth、fundability/quality/export verdict 或 package authority。 |
| `product_entry_parts/runtime_surfaces.py`、`runtime_registration.py` | manifest/status/sidecar runtime projection、skill catalog domain projection、runtime registration tests | `already_thin_adapter` + `opl_framework_migration_candidate` | domain entry target refs、resume/progress command refs、grant truth owner boundary | runtime/readiness projection owner、helper implementation selection、indexer registry、runtime/watch helper owner、lifecycle/session indexing implementation | 保持 `opl_provider_runtime_contract`；OPL helper/index registry 成为 default owner 后，MAG 只保留 consumed refs / authority boundary。 |
| `product_entry_parts/consumer_thinning*` | pack compiler / manifest read projection、functional audit read model | `already_thin_adapter` | minimal authority taxonomy、declarative grant pack compiler input、generated surface handoff、bridge exit gate、retired/tombstone audit refs | OPL generated surface compiler/read model、external evidence request primitive、default caller proof shell、legacy tombstone catalog | 不写 production/default caller complete；OPL compile/readiness proof、external evidence receipt parity、no-resurrection guard 成立后继续收薄。 |
| `product_entry_parts/functional_closure*`、`domain_agent_skeleton.py`、`domain_agent_projection_surfaces.py` | product-entry manifest、sidecar export、functional closure tests、OPL family contract adoption | `already_thin_adapter` + `opl_framework_migration_candidate` | owner receipt contract refs、lifecycle guarded apply refs、grant transition oracle refs、quality/export/fundability owner refs、memory/artifact/receipt authority refs | generated manifest closure shell、lifecycle/source-layout projection assembly、standard-agent skeleton wrapper、artifact/memory locator、controlled attempt lifecycle projection | OPL generated/default caller parity、artifact/memory locator parity、owner receipt/typed blocker roundtrip、no-forbidden-write proof 后继续收薄；owner receipt signer 和 MAG verdict owner 不迁移。 |
| `loop_contracts.py`、`loop_route_shell.py` | grant direct-entry、grant user-loop、product-entry manifest/status validation | `already_thin_adapter` + `opl_framework_migration_candidate` | grant route truth alignment、domain action target refs、typed blocker / owner receipt return boundary、quality/export/package authority refs by reference only | generated user-loop/product-route command shell、runtime report locator shell、App/operator route projection | OPL product user-loop generated/default caller parity、direct/hosted no-regression、owner receipt/typed blocker roundtrip、no-forbidden-write proof；MAG route truth 不迁移。 |
| `grant_autonomy_controller.py`、`grant_autonomy_loop_shell.py`、`grant_autonomy_loop_parts.py`、`grant_autonomy_report_resume.py`、`grant_autonomy_common.py` | autonomy controller command、controller tests、controller resume path | `opl_framework_migration_candidate` | grant route/budget/blocker policy refs、typed blocker return shape、owner receipt handoff refs、AI-first review/export verdict refs | generated controller entry shell、attempt lifecycle caller、generic attempt report envelope、resume seed parser、operator loop shell | OPL generated/default caller、provider/attempt parity、owner receipt/typed blocker roundtrip、continuous no-forbidden-write、no scheduler owner claim。 |
| `grant_autonomy_controller_plan.py`、`grant_autonomy_quality_payload.py` | controller plan / quality closure payload validation | `domain_authority_retained` | grant route/budget/blocker/evidence-gap policy refs、quality closure dossier refs、closure package queue semantics、AI reviewer/export verdict refs | OPL can host callback lifecycle and pass refs; cannot generate quality verdict | 不迁 authority；只在 MAG owner receipt / direct-hosted parity / no-regression 证明下改名或进一步拆 report projection。 |
| `cli.py` | direct MAG CLI、product/user-loop/status/sidecar commands | `opl_framework_migration_candidate` | direct domain entry、owner receipt reader、grant command target | generated CLI/MCP/product shell | generated caller parity、no old alias/facade active caller、direct path no-regression。 |
| `domain_runtime_parts/*`、`domain_entry.py` | domain entry direct path、workspace/package IO helpers、service-safe catalog | `already_thin_adapter` | route/authority adapter、package/source IO validation、identity guard | generic workspace/source locator、generated domain-entry shell | OPL locator/generated entry parity before shell migration；package/export authority remains MAG. |
| `owner_receipt_common.py`、`owner_receipt_writers.py`、`owner_receipt_reconciliation.py`、`production_live_acceptance.py`、`stage_control_plane.py`、`opl_standard_pack.py`、`opl_standard_pack_private_policy.py` | owner receipt / lifecycle receipt / reconciliation / production acceptance / sidecar closeout、pack/conformance tests、stage readiness | `domain_authority_retained`；旧 `owner_receipts.py` 聚合文件已拆分并退役 | owner receipt signing、stage prompt/skill/quality gate semantics、transition oracle、private authority taxonomy、no-resurrection policy | OPL receipt ledger/index and pack compiler only consume refs | 不迁 signer、stage semantics 或 verdict owner；只保持合同无漂移。 |

## Path-Level Current Checkpoints

| path | lines | class | current active caller | 当前实际职责 | MAG 必须保留的 authority | 可迁往 OPL 的 generic 子域 | 迁移/退役门槛 | 推荐验证入口 |
| --- | ---: | --- | --- | --- | --- | --- | --- | --- |
| `src/med_autogrant/product_entry_parts/owner_receipt_writers.py` | 151 | `domain_authority_retained` | `MedAutoGrantProductEntry.write_owner_receipt_evidence`、`write_lifecycle_receipt_evidence`、CLI/sidecar receipt paths | 写 MAG owner receipt 与 lifecycle receipt instance 到 runtime-state，显式 no repo/truth/artifact/memory/verdict write | owner receipt signing、lifecycle receipt signing、typed blocker/no-regression return shape | OPL receipt ledger/index、generic lifecycle/package shell 只消费 refs | OPL receipt ledger/default caller 可消费 refs；MAG receipt schema 与 forbidden-write proof 不漂移 | `tests/product_entry_cases/test_functional_closure.py`、`tests/product_entry_cases/test_lifecycle_receipt_bundle.py` |
| `src/med_autogrant/product_entry_parts/owner_receipt_reconciliation.py` | 248 | `already_thin_adapter` | controlled soak reconciliation proof/inventory、receipt observability、continuous reconciliation | body-free receipt reconciliation proof/inventory；只比较 receipt refs、typed blockers 和 no-regression refs | owner receipt ref validation、typed blocker refs、no-regression refs ownership boundary | OPL observability/read-model and receipt ledger reconciliation shell | OPL observability consumes same refs；no grant truth/artifact/memory/verdict body projected | `tests/product_entry_cases/test_controlled_soak.py`、`tests/product_entry_cases/test_receipt_observability.py` |
| `src/med_autogrant/product_entry_parts/production_live_acceptance.py` | 282 | `domain_authority_retained` | production-live-acceptance receipt CLI、production acceptance tests | 将 MAG owner receipt 与 OPL Agent Lab / OMA refs 对齐为 production acceptance receipt projection；不把 external pass 当 grant ready | MAG owner receipt authority、typed blocker closeout、fundability/quality/export verdict boundary | OPL Agent Lab / OMA work-order consumption shell and expected receipt ledger | Agent Lab/OMA 只能消费 refs；不能签发 MAG owner receipt 或声明 fundability/export ready | `tests/product_entry_cases/test_production_live_acceptance.py`、`tests/test_production_acceptance.py` |
| `src/med_autogrant/product_entry_parts/owner_receipt_common.py` | 121 | `already_thin_adapter` | receipt writer/reconciliation/production acceptance modules | shared constants、validation、forbidden-write proof 和 runtime root resolver | receipt identity validation、forbidden-write guard | OPL receipt envelope schema constants 可上收；MAG-specific validation remains local | shared OPL receipt envelope schema pinned 后，只保留 MAG-specific owner validation | same focused receipt tests |
| `src/med_autogrant/product_entry_parts/manifest_builder.py` | 561 | `already_thin_adapter` + `opl_framework_migration_candidate` | product-entry manifest/status/direct-entry/sidecar export 与 manifest/status tests | 串接 grant progress、workspace summary、route report、readiness、runtime/shell/helper parts 和 final shared manifest；不拥有 generic runtime 或 App/workbench | grant workspace identity、route verification refs、domain memory/receipt/verdict refs、transition oracle refs | OPL generated product-entry/status/workbench manifest shell、family manifest assembly、default caller | OPL generated/default caller 与 App/workbench consumption 产生 direct/hosted parity、owner receipt/typed blocker roundtrip、no-forbidden-write proof 后退役手写 shell；当前仅完成自然拆分 | `tests/product_entry_cases/test_manifest_and_status.py`、`tests/test_opl_standard_pack.py` |
| `src/med_autogrant/product_entry_parts/manifest_builder_parts/runtime_task_shell.py` | 298 | `opl_framework_migration_candidate` | product-entry manifest builder | 组装 runtime inventory、task lifecycle 和 automation companion；只消费 MAG refs，不写 runtime state 或 verdict | 只保留 MAG owner refs、submission/package authority refs 和 route/receipt references | OPL runtime/read-model/default automation companion primitive | OPL default runtime/task/automation caller consumption 与 domain receipt parity 后，替换为 generated surface 或删除；不能扩写为 MAG scheduler、attempt ledger、watch daemon | `tests/product_entry_cases/test_manifest_and_status.py`、`tests/product_entry_cases/test_runtime_registration.py` |
| `src/med_autogrant/product_entry_parts/manifest_builder_parts/shell_assembly.py` | 450 | `already_thin_adapter` + `opl_framework_migration_candidate` | product-entry manifest builder | 组装 product/status/user-loop/cockpit/direct-entry shell、action catalog projection、quickstart/overview/operator surface | MAG action metadata、transition oracle refs、human gate refs | OPL generated product/status/user-loop/workbench shell and projection shell | OPL generated/default caller 证明后只保留 action/stage refs 与 MAG handler target | `tests/product_entry_cases/test_manifest_and_status.py`、`tests/test_opl_standard_pack.py` |
| local runtime journal / attempt ledger、repo scheduler、upstream Hermes probe、Gateway/local-manager default path、flat alias、facade patch bridge、compat aggregate test | none after retirement; negative guard / tombstone only | `legacy_proof_tombstone` | none | history/provenance, no-resurrection guard | 不恢复 active caller；不新增 compatibility shell、alias、facade 或 aggregate test。 |

## Bad-smell flags

- Hand-written product/status/user-loop/sidecar/CLI shell 继续扩张。
- refs-only adapter 输出 grant truth、memory body、artifact body、OPL runtime state 或 App workbench state。
- standard skeleton / locator projection shell 变成 MAG-owned runner、queue、attempt ledger、workbench、artifact indexer 或 memory store。
- active caller 仍在 MAG，却写成 OPL generated/default caller 已完成迁移。
- package existence、quality scorecard、schema completeness、controller route 或 queue completion 被写成 fundability/quality/export verdict。
- 旧 local runtime / Hermes / Gateway / compatibility wording 被恢复为当前目标、默认 owner 或兼容保留理由。

## OPL primitive dependencies

- generated product/status/workbench/sidecar default caller；
- generated product user-loop route-command projection and runtime report locator shell；
- typed queue and sidecar dispatch shell with owner receipt roundtrip；
- OPL wakeup/provider queue shell consuming `open_grant_user_loop` refs；
- generic lifecycle/session/package locator shell；
- standard-agent skeleton / artifact locator / domain memory locator / controlled attempt lifecycle projection primitives；
- App/operator read model consuming MAG refs without grant verdict generation；
- production/default caller and Temporal long-soak evidence from OPL/App side。

## 禁止声明

- `mag_functional_structure_gap_count=0` 不表示 physical source cleanup complete。
- OPL stage evidence receipt verified 不表示 grant-ready 或 submission-ready。
- package existence、quality scorecard、schema completeness、controller route 或 queue completion 不能成为 fundability / quality / export verdict。
- active caller still in MAG means OPL has not fully taken over that surface。
