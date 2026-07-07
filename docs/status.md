# 当前状态

Owner: `Med Auto Grant`
Purpose: `current_status_and_evidence_boundary`
State: `current`
Machine boundary: 本文是人读状态摘要。机器真相继续归 `contracts/runtime-program/current-program.json`、production acceptance contract、schemas、source、CLI/API 行为、product-entry manifest、runtime receipts 与 workspace/artifact outputs。
Last reviewed: `2026-06-14`

Plugin native profile pointer: `contracts/opl-native-profile.json` 只声明 OPL Flow / OPL Doc 插件同步与 drift 检查所需的 repo-native profile；它不是 grant truth、runtime truth、fundability verdict、artifact/export authority、owner receipt 或 production-ready 证据。

## 当前结论

`Med Auto Grant` 是医学基金申请 domain agent，也是 OPL-compatible Foundry Agent package。Direct app skill / CLI / `MedAutoGrantDomainEntry` 仍是一等入口；任务启动后的默认运行驻留由 OPL/Temporal hosted autonomous runtime 承担。`Codex CLI` 是当前第一公民 stage executor；`Hermes-Agent`、Claude Code 等只作为显式 opt-in executor adapter / proof lane 接入。

Live Evidence 后置 / 功能结构优先是 MAG 日常开发读法。strict source-purity thinning、product/status/user-loop/domain-handler shell 收薄、refs-only lifecycle/package boundary、generated/default caller consumption guard、no-resurrection 和 tombstone/provenance 可以先作为功能/结构 lane 推进；只有实际物理删除 active handler/adapter、写 grant truth、提交包、human gate、quality/export verdict、owner receipt 或 production/release claim 时，才要求对应 owner evidence。Temporal long-soak、submission-ready human-gate receipt、App/operator sustained consumption、真实 workspace receipt scaleout 和 W7 live closing ref 属于后置 Live Evidence / production evidence lane，不能反向阻塞可独立完成的结构清理，也不能由 schema completeness、stage replay、provider completion、product-entry manifest success 或 refs-only accounting 替代。

本轮 executor owner 读法已进一步收窄：`hermes_agent` critique 路径在 MAG 内只作为 OPL `AgentExecutionReceipt` 的显式非默认 receipt lane 消费；批注 metadata 的 owner 是 `OPL executor adapter critique receipt owner`，不是 MAG 持有的 Hermes executor。MAG 不管理 Hermes executor substrate，也不持有 helper/runtime implementation；MAG 只声明和消费 request / receipt / closeout / critique payload vocabulary，并要求显式 lane fail-closed、`receipt_owner=one-person-lab`、`mag_executor_owner=false`。MAG-side Hermes helper/runtime implementation 已按 OPL-owned executor boundary 退役；后续若恢复 `hermes_agent` 执行能力，只能通过 OPL generic executor adapter 提供 request/receipt entry，不得在 MAG 重新引入 backend helper、local config reader 或 provider implementation。

Repo-local `next-step` / `stage-route-report` 当前只作为 MAG transition oracle recommendation 与 checkpoint projection 读取：`current_stage` 是 workspace lifecycle observation，`recommended_stage` 是 transition intent recommendation，二者都不能写 OPL Stage current pointer、terminal state、`current_owner_delta` 或 next-stage decision。Repo-local `critique_loop_controller`、`authoring_mainline_controller` 与 `grant_autonomy_controller` 当前只作为 OPL default StageRun / stage attempt 的 bounded domain authority target 读取；`loop_status` / `controller_status` 是 MAG domain controller result，不是 OPL Stage terminal state。三个入口在执行任何 MAG-side loop/runner 前都必须看到 `one-person-lab` owner、`codex_cli` default executor、OPL StageRun ref、OPL stage attempt lease / receipt 与 `opl_owner_chain_default_caller` caller role；缺失时返回 MAG-owned typed blocker refs，不启动 MAG 私有 durable loop、attempt ledger、scheduler、repo-local runner、private wrapper 或 named legacy guard。显式 `hermes_agent` lane 只保留 OPL executor adapter request/receipt vocabulary，receipt owner 必须是 `one-person-lab`，且 `mag_executor_owner=false`；MAG-side Hermes helper/runtime implementation 不作为 owner surface，后续应迁出或删除。

MAG 与 MAS、RCA、OMA 共享同一 OPL Foundry Agent 生命周期：`domain pack -> stage-led execution -> independent quality/fundability gate -> owner receipt/typed blocker -> handoff`。MAG 的差异只在 grant/fund 材料输入和 grant proposal/package 输出；OPL 只持有 refs、projection 与 runtime 编排，不持有 grant truth 或 grant verdict。

2026-07-07 professional skill 方法层增强：`mag-strategy-intake-specialist` 和 `mag-grant-workflow-specialist` 继续作为两个 workflow-level skill 承载 grant 专业判断，不新增 call-fit / aims / reviewer / rebuttal / package 小 skill。新增读法是把 funder-fit synthesis、specific-aims strategy、reviewer-facing frame、package completeness judgment 和 proceed/repair/retarget/stop action matrix 留在 AI-first skill 层；contracts、scripts、scorecards 和 package refs 只做 identity、locator、no-authority guard 和 traceable return shape。该增强不授权 fundability verdict、quality/export verdict、submission readiness、owner receipt、typed blocker instance 或 package authority。

OPL family `Foundry Agent OS` 目标下，MAG 的 target delta 读 [MAG Foundry Agent OS 目标差异页](./active/foundry-agent-os-target-delta.md)：generic runtime、Pack compiler、generated surfaces、source/package shell、quality/readiness projection、Console/workbench 和 capability registry ABI 上收到 OPL；grant truth、fundability / quality / export verdict、submission/package authority、grant strategy memory accept/reject、owner receipt、typed blocker 和 grant-native helper 保留为 MAG authority kernel。该 target delta 只冻结架构方向，不声明 grant-ready、submission-ready、App sustained-consumption 或 production-ready。

`contracts/foundry-agent-os-domain-kernel-manifest.json` 是 W4 `domain-kernel-manifest` 的 MAG machine-readable 落点。它把 retained Grant Authority Kernel、OPL upcollect surfaces、`current_owner_delta` 默认读根、owner receipt / typed blocker / fundability-quality-export-submission signer 归属和 OPL/Vault/Console/Runway/Pack/Capability Registry false-authority flags 固定为可测试合同；它不声明 grant-ready、fundability-ready、quality-ready、export-ready、submission-ready、production-ready、App release-ready 或 physical delete authority。

`contracts/live_stage_run_progress_evidence.json` 是当前 MAG-owned live stage progress owner answer / typed blocker source of truth。文档层只保留读法：OPL 标准状态是 `owner_typed_blocker_recorded_not_ready_claim`，domain 状态是 `blocked_by_mag_owned_typed_blocker`，`domain_owned_closing_ref=null`；具体 receipt、blocker、human-gate、quality/export、no-regression、long-soak、verification 和 doc refs 由该合同的机器字段持有。`contracts/production_acceptance/mag-production-acceptance.json` 继续作为 production acceptance provenance，不作为 live stage progress owner answer 或 W7 live owner closing ref，也不授权任何 ready claim。

无论从 direct path 还是 OPL 托管 path 进入，执行都必须回到 MAG-owned grant truth、fundability / quality / export verdict、package authority、grant strategy memory accept/reject、owner receipt 和 typed blocker。OPL 持有 Temporal-backed provider runtime、typed queue、scheduler / daemon、attempt ledger、generic transition runner、workspace/source shell、memory locator、artifact/package lifecycle shell、operator projection、observability/SLO、generated wrapper 和 App/workbench shell。

2026-07-07 OPL/App 读回与 MAG owner 裁决：`one-person-lab` 的 `agents default-callers --family-defaults` 对 MAG 显示 `all_deletion_evidence_requirements_observed=true`、`active_deletion_evidence_worklist_count=0`，`runtime app-operator-drilldown --detail full` 显示 MAG manifest sustained-consumption followthrough `verified_ledger_receipt_ref_count=1`、open workorder count `0`；该 refs-only receipt 覆盖 App/operator consumption、default caller consumption、owner payload response、workspace receipt scaleout、continuous no-forbidden-write 与 long-soak typed blocker refs。它关闭 OPL 结构/refs-only followthrough 缺口，但仍不授权 MAG 物理删除：`physical_delete_authorized=false`、`default_caller_delete_ready=false`。MAG owner 已在 `contracts/private_functional_surface_policy.json#/physical_source_morphology_policy/retirement_readback_cleanup_guard/compact_cleanup_readiness_summary/retained_surface_owner_decision` 返回 `keep_as_authority_adapter_ref` 裁决：`product_entry`、`status`、`user_loop`、`domain_handler`、`control_plane`、`lifecycle` 保留为 current thin domain target；这关闭“等待 owner 裁决”的 blocked 状态，但不声明 physical delete、default-caller delete-ready、grant-ready、domain-ready 或 production-ready。

2026-07-07 product-entry manifest source cleanup：manifest builder 到 `opl_substrate_adapter_export` 的 `locals()` 隐式上下文已收薄为显式字段传递；输出 payload contract 仍按 product-entry manifest / focused tests 验证。该 cleanup 不改变 current status：product/status/domain-handler 大 shell 已由 MAG owner 裁决保留为 current thin authority/readback adapters；后续只有新的 explicit physical-delete authorization 或 typed blocker/tombstone 裁决才能改变 physical delete 状态，不声明 readiness 或物理删除完成。

2026-07-07 source facade cleanup：`product_entry_contract_api.py` 与 `workspace_parts.py` 已删除，相关内部 caller 改为直接读取真实 owner module；`cli_rendering.py` facade 也已退役，CLI 错误上下文 helper 回到唯一调用方。该 cleanup 只减少 repo-local bridge，不改变 MAG/OPL authority split。

2026-07-07 wrapper / readback thinning：grouped CLI handler registry 已删除未注册历史 handler wrapper，`receipt-readiness` CLI 直连 leaf projection builder；receipt/readiness/evidence tests 改为直接验证 leaf contract；active-path / functional-closure 结构测试删除完整历史清单和 builder 镜像断言，只保留唯一性、no-resurrection、authority boundary、ref-only handoff、retired facade/no-active-caller、production evidence tail 与 forbidden output class sentinel。该轮是 source/test portfolio 收薄，不改变 retained big shell 的 MAG owner 裁决；`physical_delete_authorized=false`、`default_caller_delete_ready=false` 继续有效。

2026-07-07 evidence read-model wrapper thinning：controlled-soak observability、stage-attempt observability、hosted receipt verification、external evidence ledger、controlled-soak reconciliation proof/inventory 与 continuous reconciliation snapshot 不再通过 `ProductEntryEvidenceMixin` 暴露第二入口；测试和非 CLI caller 直接消费对应 leaf builder。独立 OPL conflict envelope leaf builder 已退役，当前 envelope kind/schema 只由 consumer-thinning manifest projection 承载。保留的是 leaf contract 和 active CLI/domain handler path，不保留为 ProductEntry public wrapper；owner receipt signer 与 retained big-shell physical-delete gate 不变。

2026-07-07 retained shell cleanup：单 caller 的 domain-handler shell/projection helper 文件已折回 `domain_handler.py`，测试组合删除 helper import / re-export / `assertIs` 保活断言；保留 domain-handler export/dispatch 行为、manifest/readback contract 和 OPL caller evidence gate。

2026-07-07 manifest / audit shell cleanup：`product_entry_parts/manifest_shell/*` 单 caller 拆分壳已退役，runtime/task/automation companion 进入 `manifest_runtime_task_surfaces.py`，对应 source-ref contracts 由 `sync_standard_pack()` 重新生成后不再引用 manifest_shell 空 anchor；`consumer_thinning_audit` 删除 `classification.py`、`evidence_gates.py`、`model.py`、`retired_surfaces.py` helper split，静态 catalog 改为 package JSON 数据，`report.py` 只保留 audit read-model 组装。该轮删除的是无独立 owner 的 helper/split 文件，不改变 `product_entry` retained adapter 的 `physical_delete_authorized=false` / `default_caller_delete_ready=false` 裁决。

2026-07-07 closeout projection wrapper thinning：codex stage execution receipt bundle、operator closeout readiness、physical morphology guard 与 executor-first closeout bundle 不再通过 `ProductEntryEvidenceMixin` 暴露 ProductEntry pass-through；CLI/domain_handler closeout caller 直接调用对应 leaf builder。该轮只移除 ProductEntry 第二入口，不改变 command output、owner receipt signer、grant truth、runtime-state 或 retained big-shell physical-delete gate。

2026-07-07 evidence wrapper closeout：OPL owner payload response、manifest sustained-consumption payload response、production-live-acceptance receipt projection、domain memory writeback 与 owner/lifecycle receipt writer 不再通过 `ProductEntryEvidenceMixin` 暴露 ProductEntry pass-through；CLI、domain_handler 与测试 caller 直接调用 leaf builder/writer。`ProductEntryEvidenceMixin` 已退役；domain memory、owner/lifecycle receipt writer 与 production acceptance leaf modules 仍是 retained authority/write/projection surfaces；physical delete gate 仍为未授权。

2026-07-07 single-caller helper cleanup：`workspace_runtime_policy.py`、`workspace_runtime_selection.py`、`grant_quality_issue_builder.py` 与 `funding_landscape_catalog.py` 已删除并并入唯一 active caller；保留的是 workspace validation、grant quality scorecard/diff/dossier 与 funding discovery 的行为 contract，不保留跨文件私有 helper 作为未来扩展点。该轮不改变 grant truth、owner receipt、typed blocker、runtime state、package/export authority 或 retained product-entry physical-delete gate。

2026-07-07 helper/read-model/test thinning：`cli_rendering_labels.py`、`grant_quality_value_helpers.py` 与 `consumer_thinning_pack_evidence.py` 已删除并折回唯一 owner module；CLI label rendering、grant quality value/digest helper 与 consumer-thinning external evidence request pack 不再以单独私有 helper 文件保活。结构测试继续删除实现细节、路径字符串和旧 wrapper/compat 面断言，只保留 source-purity、no-resurrection、authority boundary 与 physical-delete false-ready guards。`consumer_thinning_shell.py` 因仍承载可审查的 consumed-surface/read-model 组装而暂留；本轮不改变 `physical_delete_authorized=false`、`default_caller_delete_ready=false`、owner receipt、typed blocker、runtime state、package/export authority 或 retained product-entry physical-delete gate。

## 当前状态索引

本页只保留当前 owner、gate 和状态读法。Proof-by-proof receipt、payload、workorder、回归细节、dated closeout 流水和 per-surface 细节不在 status 继续展开；分别回到 `contracts/**`、[MAG 理想目标态差距与完善计划](./active/mag-ideal-state-cross-repo-gap-plan.md)、[MAG 私有实现与 OPL 迁移台账](./active/opl-private-implementation-migration-inventory.md)、spec lifecycle map、history 或提交历史。

| Theme | SSOT owner | Status read |
| --- | --- | --- |
| Runtime owner | `contracts/runtime-program/current-program.json` | OPL/Temporal 是任务启动后的默认运行 owner，`codex_cli` 是第一公民 executor；MAG 不实现 daemon、scheduler、attempt loop 或 attempt ledger，只保留 grant authority。 |
| OPL StageRun consumption / grant-ready audit | `contracts/temporal_stage_run_consumption_policy.json` plus `contracts/stage_run_kernel_profile.json` default entry admission policy | MAG 只消费 OPL Temporal StageRun refs；默认 CLI / domain controller entry 必须携带 OPL StageRun ref、owner-chain default-caller role、OPL owner、`codex_cli` executor 与 lease/receipt；provider completion、schema completeness、generated surface ready、manifest success、focused tests、stage replay、package existence 或 scorecard 分数不能声明 grant-ready、quality-ready、export-ready、submission-ready 或 production-ready。 |
| Standard Agent source shape | `contracts/functional_privatization_audit.json`, `contracts/runtime-program/opl-family-contract-adoption.json`, active gap plan | `mag_functional_structure_gap_count=0` / `standard_agent_source_shape_status=landed` 只表示结构分类和 owner intent 已收薄；product/status/user-loop/domain-handler/domain_runtime/autonomy/CLI shell 仍是 `physical-delete-not-authorized` tail。 |
| Private surface classification | `contracts/private_functional_surface_policy.json` and private inventory | Purpose-first thinning、source-ref integrity、source-purity、cleanup readback 和 no-resurrection guard 现在把 OPL/App/default-caller followthrough 读成 `observed_refs_only_not_physical_delete_authority`；MAG owner 对 retained current thin surfaces 的当前裁决是 `keep_as_authority_adapter_observed`。它们不授权 physical delete、default-caller delete-ready、grant-ready 或 production-ready。 |
| Foundry Agent OS target delta | `contracts/foundry-agent-os-domain-kernel-manifest.json` and `docs/active/foundry-agent-os-target-delta.md` | Generic runtime、Pack compiler、generated surfaces、source/package shell、quality/readiness projection、Console/workbench 和 capability registry ABI 上收到 OPL；grant truth、fundability / quality / export verdict、submission/package authority、memory accept/reject、owner receipt 和 typed blocker 留在 MAG authority kernel。 |
| Live progress owner answer | `contracts/live_stage_run_progress_evidence.json` | 当前 OPL 标准状态为 `owner_typed_blocker_recorded_not_ready_claim`，domain 状态为 `blocked_by_mag_owned_typed_blocker`，`domain_owned_closing_ref=null`；production acceptance tail 只作 provenance。 |
| OPL Ledger artifact registration | `contracts/opl_ledger_artifact_registration.json` plus `/product_entry_manifest/artifact_locator_contract/opl_ledger_artifact_registration` | MAG 只给 OPL Ledger 暴露长期 grant deliverable 的 refs-only 登记形状：`artifact_ref`、`artifact_hash`、`index_ref`、`review_ref`、`receipt_ref`。OPL Ledger 只登记 ref/hash/index/review/receipt refs，不读取 artifact body，不写 grant truth，不创建 owner receipt / typed blocker，不签 fundability / quality / export / submission-ready verdict。 |
| Evidence / production / release lanes | evidence contracts, OPL/App read models, and production acceptance refs | App/operator/default-caller sustained-consumption followthrough 已有 OPL verified refs-only ledger 和 App/operator drilldown 读回；Temporal long-soak、submission human gate、W7 closing ref、grant-ready 和 production-ready 仍是后置 owner/runtime 证据 lane。 |
| Human gate | MAG owner surface and active gap plan | `submission_ready_export_gate` 仍是 blocking human gate。Typed blocker 可审计但不是 approval；关闭只能来自真实 human-gate receipt、真实 quality/export / long-soak / owner acceptance evidence，或 MAG-owned typed blocker 更新。 |

## 当前保留面

- `agent/` 是 Declarative Grant Pack：stage prompts、stage policies、domain skill declaration、professional skills、quality gates 和 knowledge refs 是 OPL pack compiler / generated surfaces 的 repo-source 语义输入。
- `agent/primary_skill/SKILL.md` 是 MAG rich primary skill 的标准 OPL repo source，并由 `contracts/capability_map.json#/capabilities?surface_role=primary_skill` 登记；旧 `plugins/med-autogrant/skills/med-autogrant/SKILL.md` 继续作为 Codex plugin carrier / compat mirror，不持有 grant truth、fundability verdict、submission-ready verdict、owner receipt、typed blocker 或 runtime queue。
- `contracts/` 是机器合同、handoff、receipt、external evidence request、production acceptance 和 runtime-program 指针。
- `src/med_autogrant/**` 只作为 domain handler、refs-only adapter、minimal authority function、native helper、diagnostic、migration input 或 tombstone/provenance 支撑读取；不得写成 MAG 私有 runtime platform。
- MAG retained private authority surface 限定为 grant domain truth、fundability / quality / export verdict、package authority、grant strategy memory body 与 accept/reject、owner receipt、transition oracle、grant-native helper 和 focused contract tests。
- Product-entry、domain_handler、grouped CLI/API、projection、lifecycle、memory/package projection 和 status/user-loop 仍可作为 direct domain handler、refs-only adapter、native helper target 或 migration input 暂时存在；长期 owner 是 OPL generated/hosted surface，当前 strict purity 读法是 replacement-ready 但 physical-delete 未授权。per-surface 分类与删除门统一读 [MAG 私有实现与 OPL 迁移台账](./active/opl-private-implementation-migration-inventory.md)，当前 gate 与下一步统一读 [MAG 理想目标态差距与完善计划](./active/mag-ideal-state-cross-repo-gap-plan.md)。
- 当前 active source 中仍可见的 product-entry、domain_runtime、runtime registration、domain_handler、lifecycle、memory/package projection、autonomy loop 和 status/user-loop shell 不是兼容承诺，也不是长期标准智能体组成。机器删除条件以 `contracts/private_functional_surface_policy.json#/purpose_first_owner_delta_domain_thinning_gate`、`contracts/foundry_agent_series.json#/purpose_first_adapter_thinning_policy` 和 manifest/audit surfaces 为准；条件满足后旧 wrapper、alias、facade、patch bridge、compat aggregate test 与 legacy runtime/probe residue 直接删除或归入 history/tombstone，不保留 repo-local compatibility shell。

## 已退役面

Local runtime journal / attempt ledger、repo-owned scheduler daemon、upstream Hermes probe、flat shell alias、facade patch bridge、compat aggregate test、Gateway/local-manager default path 和旧 hosted/provider specs 只能作为 history、tombstone、explicit proof history 或 regression oracle 阅读。无 active caller 后直接删除或归档，不新增 compatibility alias、re-export facade 或 compatibility-only 聚合测试。

当前 legacy/default runtime residue 的当前读法回到 product-entry manifest、repo-source layout audit、private inventory 与 retired-surface provenance：active/default/compat surface 不再保留 Hermes / Gateway / local-manager path；retired refs 只作为 tombstone/provenance，不作为兼容承诺或删除授权。

## 后置证据边界

当前剩余 live / production / release evidence 不再写成 MAG repo 侧结构缺口，也不在本文维护 receipt id、run id、cohort、payload path 或 command transcript。读法统一为：

- OPL-hosted grant-stage attempts、real workspace receipt scaleout、App/operator/release consumption、Temporal provider long soak 和 W7 closing ref 只在对应 evidence contracts、owner receipts、OPL/App read model 或 production acceptance refs 中读取。
- `contracts/live_stage_run_progress_evidence.json` 是当前 live stage progress owner answer；下一次 owner answer 仍应写回该合同，而不是把 status.md 扩成 evidence ledger。
- Physical cleanup / no-resurrection 的关闭条件回到 active gap plan、private inventory 和 machine gates。OPL generated/default-caller、App/operator followthrough、owner receipt / typed blocker roundtrip、continuous no-forbidden-write 与 tombstone/provenance 现按 refs-only evidence observed 读取，但这些读面不能签 MAG physical delete；MAG owner 当前已返回保留裁决 `keep_as_authority_adapter_ref`，所以 retained big-shell tail 不再是等待裁决的 blocker，而是 `physical-delete-not-authorized / keep current thin authority adapter` 状态。

## 当前入口

- 用户路径：`Med Auto Grant app skill -> OPL/App generated status or manifest -> MAG domain-handler export|dispatch target -> workspace progress / workspace cockpit refs -> direct-entry/user-loop action target -> pass / package commands`。
- OPL owner-payload refs：`authority receipt-readiness -> authority owner-payload-response -> authority manifest-consumption-payload -> OPL refs-only owner-payload record/verify`。
- Pre-workspace：`discover-funding-opportunities -> select-project-profile -> initialize-intake-workspace`。
- Grant stage plane：`call_and_candidate_intake`、`fundability_strategy`、`specific_aims_and_structure`、`proposal_authoring`、`review_and_rebuttal`、`package_and_submit_ready`。
- Declarative Grant Pack：`agent/prompts/`、`agent/stages/`、`agent/skills/`、`agent/professional_skills/`、`agent/quality_gates/`、`agent/knowledge/`。
- DomainHandler：`domain handler export` / `dispatch` 只返回 refs、owner receipt、typed blocker、verdict refs 与 authority action metadata；它不是常驻 daemon。

## 当前不能声明

- 不能把 `mag_functional_structure_gap_count=0` 写成 strict source-purity 完成、external production/default caller 完成、真实 App/workbench consumption 或 production long-run soak 已完成。
- 不能把 production acceptance tail 写成 live stage progress owner answer 或 W7 live owner closing ref；当前 live progress source of truth 是 `contracts/live_stage_run_progress_evidence.json`，且状态为 MAG-owned typed blocker，`domain_owned_closing_ref=null`。
- 不能把 descriptor ready、transition oracle smoke、receipt reconciliation proof、external evidence consumption 或 no-regression evidence 写成 provider SLO / live soak 已完成。
- 不能把 OPL provider completion、matrix runner smoke、package existence、schema completeness、quality scorecard 分数或 controller route 写成 fundability-ready、quality-ready、export-ready 或 submission-ready verdict。
- 不能把 stage replay projection、OPL ledger verification、product-entry manifest success、grouped CLI success、stage folder package refs 或 refs-only accounting closeout 写成 grant-ready、fundability-ready、quality-ready、export-ready 或 submission-ready verdict。
- 不能把 OPL Ledger artifact registration 写成真实 grant artifact body、owner receipt、typed blocker、runtime queue、provider attempt、package/export authority verdict 或 submission-ready evidence；它只登记 ref/hash/index/review/receipt refs。
- 不能把 hand-written product-entry / domain_handler / grouped CLI/API / projection / lifecycle wrapper 写成长期合理私有平台。
- 不能把 local journal、attempt ledger、Hermes probe、Gateway/local-manager、flat CLI alias、compatibility aggregate test 或 `codex_cli` executor 写回默认 runtime owner。

## 下一跳

- 目标态：[Med Auto Grant 理想目标态](./references/med-auto-grant-ideal-state.md)
- 差距与顺序：[MAG 理想目标态差距与完善计划](./active/mag-ideal-state-cross-repo-gap-plan.md)
- 文档治理：[MAG 文档组合治理](./docs_portfolio_consolidation.md)
- 过程归档：[MAG standard agent 文档过程归档 2026-05](./history/plans/mag-standard-agent-doc-process-history-2026-05.md)
