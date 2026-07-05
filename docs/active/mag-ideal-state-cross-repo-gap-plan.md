# MAG 理想目标态差距与完善计划

Owner: `Med Auto Grant`
Purpose: `ideal_state_gap_plan`
State: `active_plan`
Machine boundary: 本文是人读 current gap / completion plan。机器真相继续归 `contracts/runtime-program/current-program.json`、contracts、schemas、source、CLI/API 行为、product-entry manifest、workspace/runtime artifact root、runtime receipts、质量报告和导出包。
Last reviewed: `2026-06-12`

## 读法

本文是 MAG 当前唯一 active gap / plan 入口。目标态读 [Med Auto Grant 理想目标态](../references/med-auto-grant-ideal-state.md)；当前状态读 [当前状态](../status.md)；per-surface 明细读 [MAG 私有实现与 OPL 迁移台账](./opl-private-implementation-migration-inventory.md)；过程流水读 [MAG standard agent 文档过程归档 2026-05](../history/plans/mag-standard-agent-doc-process-history-2026-05.md)。

差距按理想态判断，不按现有 MAG 代码是否还能运行判断。通用 runtime、runner、queue、session、journal、workspace/source intake、memory/package transport、workbench、observability、generic CLI/product-entry/status wrapper 和旧 product-sidecar wrapper 属于 OPL / shared family layer；MAG 只保留 grant authority、domain handler、refs-only adapter、diagnostic、fixture 或 tombstone。

2026-06-30 SSOT refresh：本文的默认 gap 只维护功能面落地、结构收薄和历史遗留清理。Temporal long-soak、submission human-gate、App/operator sustained consumption、real workspace receipt scaleout、W7 closing ref、grant-ready、submission-ready 和 production-ready 不作为本文 active gap 表或 next prompt 的默认 worklist。当前 MAG 仍需关注的缺口是 product/status/user-loop/domain-handler/domain_runtime/autonomy/CLI handler shells 的 physical-delete-not-authorized tail：只有 OPL generated/default caller parity、no-active-caller、MAG owner receipt / typed blocker、no-forbidden-write 和 tombstone/provenance 成立后，才可删除或收薄。本文不再把 live receipt、provider run、release cohort 或 dated proof 流水混入理想态和功能/结构 gap。

2026-06-30 functional closure gate：`contracts/private_functional_surface_policy.json#/physical_source_morphology_policy/retirement_readback_cleanup_guard/compact_cleanup_readiness_summary/retained_surface_owner_decision_gate` 已把 retained current thin surfaces 的删除/收薄门显式化。`product_entry`、`status`、`user_loop`、`domain_handler`、`control_plane`、`lifecycle` 当前只能 `retain_as_current_thin_domain_target`，或在 generated/default caller parity、no-active generic shell caller、owner receipt / typed blocker roundtrip、continuous no-forbidden-write 与 tombstone/provenance pointer 齐备后，由 explicit owner receipt 删除或由 domain typed blocker/owner decision tombstone。该 gate 禁止从 refs-only evidence、`cleanup_candidate_count=0`、contract pass 或 source-purity clean 推导 physical delete、default caller cutover、grant-ready、domain-ready 或 production-ready。

本文执行原则是功能/结构优先：strict source-purity、purpose-first owner-delta / domain-thinning、refs-only package/memory/lifecycle boundary、product/status/user-loop/domain-handler shell 收薄、generated/default caller consumption guard 和 no-resurrection 不等待 Temporal long-soak、submission human-gate、App/operator sustained consumption、real workspace receipt scaleout 或 W7 closing ref。Grant-ready、submission-ready、App sustained-consumption、provider long-soak、production-ready 和 physical delete owner authorization 只在对应声明或不可逆删除前回 owner evidence surface；schema completeness、stage replay projection、OPL ledger verification、provider completion、grouped CLI success、product-entry manifest success 或 refs-only accounting closeout 不能替代它们。

本文不保存长篇执行 prompt、dated closeout checklist、receipt proof 流水、逐日期 command transcript 或 worktree closeout。每轮完成后只把当前状态、仍开放 gap、证据门和近期顺序折回本文；细节进入合同、history、specs lifecycle map 或提交历史。

## 当前唯一真相

MAG 是医学基金申请 domain agent，也是 OPL-compatible Foundry Agent package。Direct app skill / CLI / `MedAutoGrantDomainEntry` 是一等入口；任务启动后的默认运行驻留是 OPL/Temporal hosted autonomous runtime；`Codex CLI` 是当前第一公民 stage executor。

无论 direct path 还是 OPL-hosted path，执行都必须回到 MAG-owned grant truth、fundability / quality / export verdict、package authority、grant strategy memory accept/reject、owner receipt 和 typed blocker。OPL 持有 Temporal provider runtime、typed queue、attempt ledger、generic transition runner、workspace/source shell、memory locator、artifact/package lifecycle shell、operator projection、observability/SLO、generated wrapper 和 App/workbench shell。

当前机器面必须按下面三条同时读取：

| 信号 | 当前值 | 读法 |
| --- | --- | --- |
| `mag_functional_structure_gap_count` / `standard_agent_source_shape_status` | `0` / `landed` | 这是 contracts/read-model 的结构分类信号，只说明 generic owner intent 已被分类和收薄；不表示 strict source-purity 物理完成、生产切换或 live soak 完成。 |
| OPL replacement / physical delete fields | `functional_privatization_audit.json` and `runtime-program/opl-family-contract-adoption.json` | OPL generated/default caller replacement 与 cutover readiness 的机器字段已由合同持有；这些字段不授权 MAG repo 物理删除 active handler/adapter，也不关闭 App/workbench、production/live caller 或 long-soak 证据。 |

当前 `product_entry*`、`product_entry_parts/*`、`domain_runtime*`、runtime registration、domain-handler、lifecycle、memory/package projection、autonomy loop、status/user-loop shell 与部分 CLI/rendering shell 仍可见于 active source。它们只能按 direct handler、refs-only adapter、minimal grant authority function、diagnostic 或 migration input 读取，不能重新写成 MAG 私有 runtime platform；按 strict purity，它们已进入 OPL replacement-ready / physical-delete-not-authorized 状态。当前 `product_entry_parts/manifest_builder.py` 已改为复用 `runtime_surfaces._build_runtime_continuity_surfaces()` 输出 session/progress/artifact/runtime-control quartet，避免在 manifest shell 继续手写同一组 continuity shell。旧 product-sidecar / sidecar CLI wrapper 已从 active caller 口径移除，只能作为 no-resurrection guard 或 history/provenance 词汇出现。

Purpose-first owner-delta / domain-thinning 的当前机器 gate 由 `contracts/private_functional_surface_policy.json#/purpose_first_owner_delta_domain_thinning_gate` 和 `contracts/foundry_agent_series.json#/purpose_first_adapter_thinning_policy` 共同持有。该 gate 把 product-entry、status/user-loop、domain-handler、grouped CLI、runtime/control projection 和 lifecycle shell 统一收敛成 MAG owner delta 输出面；per-surface active caller、路径分类、可迁子域和删除门只在 [MAG 私有实现与 OPL 迁移台账](./opl-private-implementation-migration-inventory.md) 与机器合同维护。

该 gate 明确把 `submission_ready_export_gate` 固定为当前 `blocking_human_gate`。关闭条件是真实 human-gate receipt 或 MAG-owned typed blocker 更新；package existence、schema completeness、stage replay projection、OPL ledger verification、provider completion、grouped CLI success、product-entry manifest success 和 refs-only accounting closeout 都不能作为 grant-ready、fundability-ready、quality-ready、export-ready 或 submission-ready 替代证据。

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

## 当前完成进度

| Layer | 当前状态 | 当前 owner / 读法 |
| --- | --- | --- |
| Identity / runtime owner boundary | `landed` | 核心五件套与 `current-program.json` 固定 MAG 是 grant authority，OPL/Temporal 是默认 task runtime owner。 |
| Declarative Grant Pack | `landed_with_evidence_tail` | `agent/`、stage control plane、quality gates 和 pack compiler input 是 OPL generated surface 输入；stage semantics 仍归 MAG。 |
| Cognitive Kernel adoption | `landed_as_advisory_contract` | `contracts/cognitive_kernel_adoption.json`、`contracts/golden_path_profile.json`、`agent/tools/domain_affordances.md`、`contracts/pack_compiler_input.json` 与 `contracts/stage_control_plane.json` 已把 tool affordance、stage strategy refs、independent gate policy 和 owner-delta handoff 接入 grant stage pack。工具 catalog 不是 workflow script，不改变已指定 funder / grant authoring 默认链路，也不授权 OPL 或 provider completion 生成 fundability / quality / export / submission verdict。 |
| Retained authority taxonomy | `landed_with_guard_tail` | fundability、quality、export、package、memory、owner receipt、grant helper 已分成 AI-first judgment surface 与 programmatic guard surface。 |
| Purpose-first adapter thinning | `machine_guard_landed_evidence_tail_remaining` | `contracts/foundry_agent_series.json#/purpose_first_adapter_thinning_policy` 和 `tests/test_opl_standard_pack.py` 固定 retained shell 只能作为 refs-only adapter、domain handler target、minimal authority function、migration input 或 tombstone/provenance 读取；默认下一跳是 MAG owner delta 或 MAG-owned typed blocker。 |
| Temporal StageRun consumption / grant-ready completion audit | `machine_guard_landed_evidence_tail_remaining` | `contracts/temporal_stage_run_consumption_policy.json`、`contracts/stage_run_kernel_profile.json#/default_entry_admission_policy`、action catalog、generated surface handoff、runtime_control、product-status 与 stage closeout 投影同一个 `grant_ready_completion_audit`：MAG 只消费 OPL Temporal StageRun/provider attempt refs，不拥有 runtime；默认 CLI / domain controller entry 必须通过 StageRun ref、owner-chain default-caller role、OPL owner、`codex_cli` executor 与 lease/receipt admission；provider completion、schema completeness、generated surface ready、manifest success、focused tests、stage replay、package existence 与 scorecard 分数都不能关 grant-ready / quality-ready / export-ready / submission-ready。 |
| Consumer thinning / refs-only boundary | `landed_with_external_gate` | `mag_consumer_thinning_contract`、domain-handler、receipt projection、lifecycle/package/memory refs 只输出 refs、typed blocker、owner receipt 与 action metadata。 |
| Submission-ready human gate blocker projection | `landed_as_blocker_projection` | `package_and_submit_ready` 的 typed blocker 已显式投影 `submission_ready_export_gate`、MAG human-gate owner、`human_gate_receipt` requirement 与 OPL/provider 不可绕过字段；该 projection 不关闭人工审批，不声明 submission/export/production ready。 |
| External evidence request accounting | `refs_only_closed` | `mag-evidence-receipt-ledger.json` 持有 request-level refs-only closure 摘要；active plan 不冻结 request/receipt 计数。剩余真实证据门是 `temporal_provider_long_soak_window_evidence` 和持续 no-regression / consumption。 |
| Standard OPL Agent source shape | `replacement_ready_physical_delete_not_authorized` | `agent/`、stage control plane、quality gates、pack compiler input 和 MAG owner boundary 已是当前默认语义结构；OPL standard pack 入口已拆成 `build/sync` owner、series profile owner 和 source-policy owner，消除了 `opl_standard_pack.py` 单文件结构 advisory。OPL default-caller replacement/cutover readiness 已观测，但 product/status/user-loop/domain-handler/domain_runtime/autonomy/CLI target 仍作为 handler/adapter target 暂留，不声明 grant-ready、submission-ready、production-ready 或 physical-delete-ready。 |
| Foundry Agent series pin contract | `done_for_structural_conformance` | `contracts/foundry_agent_series.json`、`src/med_autogrant/opl_standard_pack.py`、`src/med_autogrant/opl_standard_pack_profiles.py`、`src/med_autogrant/opl_standard_pack_source_policy.py`、`tests/test_opl_standard_pack.py`、OPL family conformance | `contract_version_policy`、`shared_release_pin_strategy` 与 canonical `shared_policy_release` 已对齐 OPL standard scaffold / Foundry policy release artifact；这只关闭 structural blocker，不授权 domain ready、quality/export verdict、owner receipt 或 default promotion。 |
| Runtime / product shell thinning | `refs_only_handler_target_until_owner_delete_receipt` | product/status/user-loop/domain-handler/domain_runtime 面只能作为 direct handler、refs-only adapter、minimal authority function、diagnostic 或 migration input；不再作为长期 MAG surface 读取。 |
| Purpose-first owner-delta / domain-thinning gate | `landed_as_contract_gate` | `private_functional_surface_policy.json` 与 `foundry_agent_series.json` 已把 product-entry、grouped CLI、status/user-loop、domain-handler、runtime/control projection 与 lifecycle shell 固定为 owner-delta 输出面。该 gate 只允许 MAG owner receipt、MAG-owned typed blocker 或 no-regression evidence 作为下一步 return shape，并把 `submission_ready_export_gate` 保持为 human-gate blocker。 |
| Evidence accounting surfaces | `refs_only_closed_with_followthrough_open` | external ledger、owner-payload response、workspace receipt scaleout、manifest sustained-consumption、stage replay/monitor projection 均按 body-free refs-only / count-only provenance 读取；真实 App/operator sustained consumption、human gate、stage success-rate 和 Temporal long soak 仍开放。 |
| Human gate projection | `explicit_blocker_not_approval` | `submission_ready_export_gate` 是 MAG-owned typed blocker authority boundary；真实 human approval receipt 仍未形成。 |
| Docs lifecycle | `single_active_gap_owner` | 本文只持有 open gap、证据门、近期顺序和禁止误写；proof 流水、receipt ids、dated coverage 和旧路线归 history/specs/provenance。 |

## 功能/结构差距

按 strict standard-agent purity，当前 MAG repo 侧 active source 已完成 replacement-ready 分类，但未获得 physical delete authority。`mag_functional_structure_gap_count=0` 只表示历史合同分类闭合，不代表 active shell 已清零。`opl_standard_pack.py` 的结构 advisory 已通过 focused owner modules 消除；这不改变 product/status/user-loop/domain-handler/domain_runtime/autonomy/CLI handler/adapter shell 的删除门。`generated_surface_bridge_exit`、`legacy_runtime_session_lifecycle_exit`、`package_memory_lifecycle_refs_only_boundary`、`private_authority_ai_first_guard` 和 `physical_morphology_tail` 必须继续守住 OPL generated/default caller 接管证据与 repo-local wrapper 删除门。

当前 active plan 只维护仍开放的结构 gap 与下一步门槛；路径级 inventory 和 retired-surface 来源不在本文展开：

| Gap | 本文保留的当前口径 | 细节 owner |
| --- | --- | --- |
| `purpose_first_owner_delta_domain_thinning_gate` | 暂留 shell 只能产出 MAG owner delta、typed blocker 或 no-regression refs；新增能力只能服务 MAG owner delta、OPL generated/default caller parity 或 no-resurrection proof，不扩写 MAG-owned generic shell。 | `contracts/private_functional_surface_policy.json#/purpose_first_owner_delta_domain_thinning_gate`、`contracts/foundry_agent_series.json#/purpose_first_adapter_thinning_policy`、private inventory |
| `package_memory_lifecycle_refs_only_boundary` | Memory/package/lifecycle/domain-handler 输出保持 body-free refs、owner receipt、verdict refs、typed blocker 和 safe action metadata。 | owner receipt / memory / package / lifecycle contracts、domain-handler source/tests、private inventory |
| `private_authority_ai_first_guard` | Fundability、quality、export、memory accept/reject 仍是 MAG AI-first judgment surface；程序面只做 validator、materializer、receipt signer、guard 或 refs projection。 | core five docs、quality/export/package source/tests、private inventory |
| `generated_default_caller_cutover` | OPL generated/default caller replacement 已有结构证据；retired/tombstone surface 的 no-active-caller evidence 已进入 `functional_privatization_audit.json` 与 `runtime-program/opl-family-contract-adoption.json`。`source-purity` strict readback 现在还暴露 body-free `owner_delta_work_order_pack`；当前 `cleanup_candidate_count=0`、`owner_delta_route_count=0`，旧 7 个面已按 strict readback 转为 migrated non-candidate 或 retained current thin surfaces。production default caller、direct/hosted parity、owner receipt roundtrip、continuous no-forbidden-write 和 App/workbench consumption 仍未授权 MAG 物理删除。 | private inventory path-level table、functional privatization audit、runtime-program adoption contract、production acceptance contracts、focused tests |
| `opl_non_default_executor_receipt_tail` | `hermes_agent` critique 路径只作为 OPL-owned non-default executor receipt lane 读取；MAG 消费 receipt / closeout / critique payload。当前 helper 有 active caller，不能按旧 Hermes/Gateway residue 删除。 | executor receipt source/tests、OPL adapter owner evidence、history/provenance |
| `current_role_guard_cleanup_tail` | 已退役 local journal、attempt ledger、Hermes probe、Gateway/local-manager、flat CLI alias、facade patch bridge 和 compatibility aggregate test 只保留 tombstone/provenance 或 current role guard，不恢复 compatibility surface。 | `docs/history/docs-portfolio-coverage-ledger/retired-surface-provenance.md`、retired public command scan、negative tests |

## Ready / Submission 声明边界

本文不维护 ready / production evidence worklist。grant-ready、fundability-ready、quality-ready、export-ready、submission-ready、App/operator sustained consumption、Temporal long-soak、W7 owner evidence 和 human-gate receipt 只在单独 evidence lane 或 owner contract 中读取；它们不得反向重开 MAG repo 侧功能/结构 backlog。

Active plan 只保留当前可落地的非 live 缺口：product/status/user-loop/domain-handler/domain_runtime/autonomy/CLI handler shells 的 physical-delete-not-authorized tail、strict source-purity / no-resurrection guard、refs-only package/memory/lifecycle boundary、AI-first authority guard 和 legacy wrapper/alias/facade/compat aggregate test 清理。涉及 evidence lane 时，只能在本文保留 false-ready 禁止边界，不列 receipt id、run id、cohort、long-soak、human-gate 或 ready-claim worklist。

## 下一轮 Agent prompt

- Write scope: MAG active truth owner、current status summary、Declarative Grant Pack、
  product/status/user-loop/domain-handler/CLI refs-only adapter boundary、AI-first authority
  guard、default-caller thinning、strict source-purity/no-resurrection 和 docs lifecycle foldback。
- Non-goals: 不把 OPL provider completion、stage replay projection、package existence、
  schema completeness、scorecard 分数、grouped CLI success、product-entry manifest success、
  refs-only accounting 或 doctor pass 写成 grant-ready、fundability-ready、quality-ready、
  export-ready、submission-ready 或 production-ready；不扩写 MAG-owned generic shell、compat
  alias、facade、wrapper 或 fallback 文案。
- Live truth inputs: 读取 `contracts/runtime-program/current-program.json`、MAG
  contracts/schemas/source/tests、product-entry manifest、domain-handler/action metadata、
  owner receipt / memory / package / lifecycle contracts、OPL/App read-model shape、runtime
  boundary contracts、workspace/package refs 和 docs portfolio；dated proof、receipt id、payload
  path、command transcript 和 old worktree closeout 只作 provenance。
- Required actions:
  1. 保持 `agent/` Declarative Grant Pack、cognitive-kernel adoption、stage control plane、
     contracts、quality gates、memory policy 与当前 source/contract 对齐；新增 tool
     affordance 只能进入 affordance catalog / boundary，不写成 executor sequence、authoring
     workflow 或 readiness verdict。
  2. 保持 product/status/user-loop/domain-handler/CLI shell 的 refs-only adapter 或 direct
     handler target 边界；新增能力优先服务 OPL generated/default caller parity，不扩写
     MAG-owned shell。
  3. 对 AI-first authority guard 做回归维护：任何 fundability / quality / export /
     submission-ready claim 必须回到 MAG owner surface 或 AI-backed artifact。
  4. 不在本文推进 live / production evidence tail；遇到 release、submission、
     human-gate、long-soak 或 grant-ready claim 时，路由到 owner evidence lane，并在本文只保留 false-ready 禁止边界。
  5. 在 generated/default caller parity、no-active-caller、no-forbidden-write、
     tombstone/provenance 与 explicit physical-delete owner decision 成立后，删除旧 wrapper、alias、
     facade、patch bridge、compat aggregate test 和 legacy runtime/probe residue；需要追溯只留
     history/provenance，测试改为断言 current contract、schema、CLI/API、manifest、owner
     receipt、typed blocker、fail-closed 或 tombstone semantics。
- Verification commands: docs-only 维护运行 `rtk git diff --check`、
  `rtk rg -n "<<<<<<<|>>>>>>>|=======" docs` 和 docs inventory sanity；触及
  source/contracts/tests 时运行 `rtk ./scripts/verify.sh` 或 focused pytest。
- Completion gate: 本轮只能在 active plan、docs portfolio、contracts/source/tests 与 fresh
  read-model 一致，且 live / production evidence 未被误写成 ready verdict 后关闭；
  generated/default caller parity、direct/hosted parity、owner receipt / typed blocker roundtrip、
  no-forbidden-write、tombstone/provenance 与 explicit MAG physical-delete owner decision 未满足前，不授权 physical delete。
- Foldback target: durable 当前结论折回本文、核心五件套、`docs/specs/README.md`、
  specs lifecycle map 或 machine contracts；执行 prompt、worktree/branch 状态、命令
  transcript、receipt id、payload path、proof closeout 和 dated coverage 进入
  `docs/history/**`、ledger、contracts 或提交历史。

## 后续工作准入

后续 agent / maintainer 继续处理 production evidence、default caller 或 no-resurrection 尾项时，只在确认以下 source of truth 后更新本文：核心五件套、MAG ideal-state reference、`contracts/runtime-program/current-program.json`、private/functional surface contracts、owner receipt / memory / package / lifecycle contracts、domain-handler/product-entry/action metadata、focused repo-native verification 和 OPL/App fresh read-model。

可写入本文的内容只包括仍开放 gap、证据门状态变化、近期顺序和禁止误写口径。执行 prompt、worktree/branch 状态、命令 transcript、receipt id、payload path、proof-by-proof closeout 和 dated coverage 进入 `docs/history/**`、ledger、contracts 或提交历史。

Docs-only 验证使用 `rtk git diff --check`、`rtk rg -n "<<<<<<<|>>>>>>>|=======" docs` 与 docs inventory sanity；触及 source/contracts/tests 时再运行 `rtk ./scripts/verify.sh` 或 focused pytest。

## 合理重构巡检口径

2026-06-15 的 OPL family 合理重构快照把 MAG 归为 `watch_only / contract-generated` 为主的仓库，而不是源码拆分优先仓。当前 repo-native line budget 通过，源码和测试没有新的 `>=1000` 行强拆信号；接近预算的 `tests/test_final_package.py` 与 `tests/test_cli_validate_workspace.py` 仍按场景聚合读取，只有在继续增长、churn 叠加或测试定位成本上升时才按 existing `product_entry_cases/` 模式 case 化。

大体量文件主要是 `schemas/v1/product-entry-manifest.schema.json`、`contracts/functional_privatization_audit.json`、`contracts/stage_control_plane.json` 和 `contracts/runtime-program/opl-family-contract-adoption.json` 这类 schema / contract / generated aggregate。它们不按普通源码行数盲拆；后续只在 source parts、generator、schema index 或 check 命令不清晰时治理生成链路。`<40` 行的 `__init__`、public entry marker、schema loader、workspace helper、test support 和 `product_entry.py` 这类薄入口默认保留；只有 deletion test 证明它只是单 caller pass-through 且删除后复杂度不会分散时，才合并或内联。

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
