# 当前状态

Owner: `Med Auto Grant`
Purpose: `current_status_and_evidence_boundary`
State: `current`
Machine boundary: 本文是人读状态摘要。机器真相继续归 `contracts/runtime-program/current-program.json`、production acceptance contract、schemas、source、CLI/API 行为、product-entry manifest、runtime receipts 与 workspace/artifact outputs。
Date: `2026-06-03`

Plugin native profile pointer: `contracts/opl-native-profile.json` 只声明 OPL Flow / OPL Doc 插件同步与 drift 检查所需的 repo-native profile；它不是 grant truth、runtime truth、fundability verdict、artifact/export authority、owner receipt 或 production-ready 证据。

## 当前结论

`Med Auto Grant` 是医学基金申请 domain agent，也是 OPL-compatible Foundry Agent package。Direct app skill / CLI / `MedAutoGrantDomainEntry` 仍是一等入口；任务启动后的默认运行驻留由 OPL/Temporal hosted autonomous runtime 承担。`Codex CLI` 是当前第一公民 stage executor；`Hermes-Agent`、Claude Code 等只作为显式 opt-in executor adapter / proof lane 接入。

本轮 executor owner 读法已进一步收窄：`hermes_agent` critique 路径在 MAG 内只作为 OPL `AgentExecutionReceipt` 的显式非默认 receipt lane 消费；批注 metadata 的 owner 是 `OPL executor adapter critique receipt owner`，不是 MAG-owned Hermes executor。`src/med_autogrant/opl_hermes_executor_helper.py` 与 `src/med_autogrant/hermes_native_executor.py` 仍有 active focused tests 和 critique receipt caller，因此当前不能物理删除；删除门是 OPL generic executor adapter 提供等价 helper/runtime entry、MAG caller 完成迁移、focused receipt tests 改到 OPL-owned surface、no-active-caller scan 通过，并留下 MAG owner receipt 或 typed blocker。

Repo-local `critique_loop_controller`、`authoring_mainline_controller` 与 `grant_autonomy_controller` 当前只作为 OPL default stage attempt 的 bounded domain authority target 读取。三个入口在执行任何 MAG-side loop/runner 前都必须看到 `one-person-lab` owner、`codex_cli` default executor 与 OPL stage attempt lease / receipt；缺失时返回 MAG-owned typed blocker refs，不启动 MAG 私有 durable loop、attempt ledger、scheduler 或 executor helper。Hermes helper 继续只服务显式 `hermes_agent` 非默认 OPL executor adapter receipt lane，receipt owner 必须是 `one-person-lab`，且 `mag_executor_owner=false`。

MAG 与 MAS、RCA、OMA 共享同一 OPL Foundry Agent 生命周期：`domain pack -> stage-led execution -> independent quality/fundability gate -> owner receipt/typed blocker -> handoff`。MAG 的差异只在 grant/fund 材料输入和 grant proposal/package 输出；OPL 只持有 refs、projection 与 runtime 编排，不持有 grant truth 或 grant verdict。

无论从 direct path 还是 OPL 托管 path 进入，执行都必须回到 MAG-owned grant truth、fundability / quality / export verdict、package authority、grant strategy memory accept/reject、owner receipt 和 typed blocker。OPL 持有 Temporal-backed provider runtime、typed queue、scheduler / daemon、attempt ledger、generic transition runner、workspace/source shell、memory locator、artifact/package lifecycle shell、operator projection、observability/SLO、generated wrapper 和 App/workbench shell。

## 当前机器事实摘要

本页只保留当前 owner、gate 和状态读法；proof-by-proof receipt、payload、workorder、回归细节和 dated closeout 流水归 `contracts/**`、`docs/history/**`、spec lifecycle map 或提交历史。

| 信号 | 当前状态 | 读法 |
| --- | --- | --- |
| Runtime owner | `current-program.json` 声明 `default_task_runtime_owner=one-person-lab`、`default_runtime_substrate=temporal`、`default_stage_executor=codex_cli`，且 MAG 不实现 daemon、scheduler、attempt loop 或 attempt ledger。 | OPL/Temporal 是任务启动后的默认运行 owner；MAG 保留 grant authority。 |
| Standard Agent source shape | `mag_functional_structure_gap_count=0` / `standard_agent_source_shape_status=landed`。 | 这是历史结构分类和 owner intent 收薄信号，不等于 strict source-purity、physical delete、App consumption 或 live soak 完成。 |
| OPL replacement / physical delete | `claims_opl_descriptor_source_available=true`、`claims_opl_replacement_exists=true`、`claims_domain_repo_physical_delete_authorized=false`、`claims_all_bridge_exits_complete=false`、`claims_production_long_run_soak_complete=false`。 | 已有 generated/default caller replacement 结构证据；仍未授权删除 active handler/adapter shell，也未关闭 production evidence tail。 |
| Evidence ledgers | external evidence ledger、production acceptance、workspace receipt scaleout、manifest sustained-consumption、owner-payload response、stage replay/monitor projection 与 owner-chain live progress evidence lane 均只保存 refs、typed blocker、owner-chain refs、quality/export/package receipt refs、no-regression refs 或 count-only provenance。 | 它们证明 refs-only consumption / replay / response shape 可读；owner-chain live progress lane 只记录 MAG-owned accepted ref shapes，不创建真实 grant body，不读取 body，不声明 grant-ready、quality-ready、export-ready、submission-ready、App sustained-consumption 或 provider long-soak 完成。 |
| Stage / progress contract | Foundry Agent series、stage control plane、Progress-First contract、`user_stage_log_contract`、stage-native artifact contract 与 `next_forced_delta` 已对齐；stage-native artifact contract 显式映射 OPL Stage Folder Kernel 的 `stage.json`、`attempt.json`、`manifest.json`、`receipt.json`、`current.json`、canonical/export、lineage、retention 和 conformance refs；package stage folder lifecycle 已投影 `artifact_bundle=stage_output_artifact_ref`、`final_package=canonical_promotion_ref`、`submission_ready_package=export_artifact_ref`。 | OPL/App 能区分 grant deliverable progress、platform repair、typed blocker、human gate、package refs、physical locator/conformance refs、manifest/missing output 和 handoff；不能写 grant truth、解释 grant quality、生成 verdict 或绕过 human gate。 |
| Cognitive Kernel adoption | `contracts/cognitive_kernel_adoption.json`、`contracts/golden_path_profile.json`、`agent/tools/domain_affordances.md`、`contracts/pack_compiler_input.json` 与 `contracts/stage_control_plane.json` 已声明 stage-internal tool affordance、strategy refs、independent gate policy 和 owner-delta handoff。 | 这是 advisory/current contract：工具目录只说明可用 affordance 和 forbidden authority，不规定 executor 顺序，不改变已锁定基金 authoring 流程，不授权 OPL 写 grant truth、quality/export/submission verdict、artifact body、memory body、owner receipt 或 typed blocker。 |
| Purpose-first thinning gate | `contracts/private_functional_surface_policy.json#/purpose_first_owner_delta_domain_thinning_gate` 约束 product-entry、grouped CLI、status/user-loop、domain-handler、runtime/control projection 与 lifecycle shell。 | 暂留 shell 只能产出 MAG owner delta、typed blocker 或 no-regression refs；physical delete 需要 explicit MAG owner receipt 与 no-active-caller / no-forbidden-write / direct-hosted parity 等证据。 |
| Human gate | `submission_ready_export_gate` 是当前 blocking human gate。 | typed blocker 可审计但不是 approval；关闭只能来自真实 human-gate receipt 或 MAG-owned typed blocker 更新。 |

## 当前保留面

- `agent/` 是 Declarative Grant Pack：stage prompts、stage policies、skill declaration、quality gates 和 knowledge refs 是 OPL pack compiler / generated surfaces 的 repo-source 语义输入。
- `contracts/` 是机器合同、handoff、receipt、external evidence request、production acceptance 和 runtime-program 指针。
- `src/med_autogrant/**` 只作为 domain handler、refs-only adapter、minimal authority function、native helper、diagnostic、migration input 或 tombstone/provenance 支撑读取；不得写成 MAG 私有 runtime platform。
- MAG retained private authority surface 限定为 grant domain truth、fundability / quality / export verdict、package authority、grant strategy memory body 与 accept/reject、owner receipt、transition oracle、grant-native helper 和 focused contract tests。
- Product-entry、domain_handler、grouped CLI/API、projection、lifecycle、memory/package projection 和 status/user-loop 仍可作为 direct domain handler、refs-only adapter、native helper target 或 migration input 暂时存在；长期 owner 是 OPL generated/hosted surface，当前 strict purity 读法是 replacement-ready 但 physical-delete 未授权。per-surface 分类与删除门统一读 [MAG 私有实现与 OPL 迁移台账](./active/opl-private-implementation-migration-inventory.md)，当前 gate 与下一步统一读 [MAG 理想目标态差距与完善计划](./active/mag-ideal-state-cross-repo-gap-plan.md)。
- 当前 active source 中仍可见的 product-entry、domain_runtime、runtime registration、domain_handler、lifecycle、memory/package projection、autonomy loop 和 status/user-loop shell 不是兼容承诺，也不是长期标准智能体组成。机器删除条件以 `contracts/private_functional_surface_policy.json#/purpose_first_owner_delta_domain_thinning_gate`、`contracts/foundry_agent_series.json#/purpose_first_adapter_thinning_policy` 和 manifest/audit surfaces 为准；条件满足后旧 wrapper、alias、facade、patch bridge、compat aggregate test 与 legacy runtime/probe residue 直接删除或归入 history/tombstone，不保留 repo-local compatibility shell。

## 已退役面

Local runtime journal / attempt ledger、repo-owned scheduler daemon、upstream Hermes probe、flat shell alias、facade patch bridge、compat aggregate test、Gateway/local-manager default path 和旧 hosted/provider specs 只能作为 history、tombstone、explicit proof history 或 regression oracle 阅读。无 active caller 后直接删除或归档，不新增 compatibility alias、re-export facade 或 compatibility-only 聚合测试。

`physical_skeleton_follow_through.legacy_active_path_residue` 与 `controlled_domain_memory_apply_proof.repo_source_layout_audit.legacy_active_path_residue` 当前均为空；默认 Hermes / Gateway / local-manager path 只保留在 `retired_legacy_default_path_receipts` 里作为 tombstone 或 `mag://owner-handoff/*-retired` refs，不再作为 active/default/compat surface。

## 当前证据门

当前剩余工作不再写成 MAG repo 侧结构缺口，统一作为 evidence gate 管理：

| Gate | 当前状态 | 关闭条件 |
| --- | --- | --- |
| OPL-hosted grant-stage attempts | replay / monitor refs 可被 OPL 读取；owner-chain live progress evidence lane 已记录 MAG 在 OPL-hosted path 下可接受的 owner receipt、typed blocker、quality/export/package receipt 与 no-regression ref shapes；持续 success-rate / long-run evidence 仍开放。 | 真实 OPL-hosted stage attempt 持续返回 MAG owner receipt、typed blocker、quality/export/package receipt 或 no-regression evidence，并形成可重复 success-rate / long-run evidence。 |
| Real workspace receipt scaleout | 已有 body-free refs-only scaleout 与 payload response snapshot；human gate、repeated consumption 和 long-soak 仍开放。 | 真实 workspace 持续产生 owner receipt、memory accept/reject receipt、package/export lifecycle receipt、cleanup/restore/retention receipt、typed blocker 或 no-regression evidence。 |
| App/operator/release consumption | 首批 refs-only evidence 可消费；sustained consumption 未关闭。 | OPL/App/operator closeout、executor-first bundle、release/default caller 持续消费 MAG package refs、quality refs、manual portal boundary、transition oracle refs 和 safe action refs。 |
| Submission-ready human gate | `submission_ready_export_gate` 仍阻塞。 | 真实 MAG owner human-gate receipt，或新的 MAG-owned typed blocker 更新。 |
| Temporal provider long soak | receipt reconciliation refs 已可读；long-soak window evidence 未关闭。 | `temporal_provider_long_soak_window_evidence`、long SLO、repair cadence 和 live receipt reconciliation 的连续证据。 |
| Physical cleanup / no-resurrection | repo-local active path scan 与 retired public command scan 已守住 legacy default caller / retired command 不复活；default Hermes / Gateway / local-manager active residue 已清零，只保留 retired receipt refs。 | 关闭条件回到 active gap plan、private inventory 和 machine gate；满足 generated/default caller consumption、direct/hosted parity、owner receipt/typed blocker roundtrip、no-active-caller、continuous no-forbidden-write 与 physical-delete owner receipt 后，删除仍有 active handler/adapter caller 的旧面。 |

## 当前入口

- 用户路径：`Med Auto Grant app skill -> OPL/App generated status or manifest -> MAG domain-handler export|dispatch target -> workspace progress / workspace cockpit refs -> direct-entry/user-loop action target -> pass / package commands`。
- OPL owner-payload refs：`authority receipt-readiness -> authority owner-payload-response -> authority manifest-consumption-payload -> OPL refs-only owner-payload record/verify`。
- Pre-workspace：`discover-funding-opportunities -> select-project-profile -> initialize-intake-workspace`。
- Grant stage plane：`call_and_candidate_intake`、`fundability_strategy`、`specific_aims_and_structure`、`proposal_authoring`、`review_and_rebuttal`、`package_and_submit_ready`。
- Declarative Grant Pack：`agent/prompts/`、`agent/stages/`、`agent/skills/`、`agent/quality_gates/`、`agent/knowledge/`。
- DomainHandler：`domain handler export` / `dispatch` 只返回 refs、owner receipt、typed blocker、verdict refs 与 authority action metadata；它不是常驻 daemon。

## 当前不能声明

- 不能把 `mag_functional_structure_gap_count=0` 写成 strict source-purity 完成、external production/default caller 完成、真实 App/workbench consumption 或 production long-run soak 已完成。
- 不能把 descriptor ready、transition oracle smoke、receipt reconciliation proof、external evidence consumption 或 no-regression evidence 写成 provider SLO / live soak 已完成。
- 不能把 OPL provider completion、matrix runner smoke、package existence、schema completeness、quality scorecard 分数或 controller route 写成 fundability-ready、quality-ready、export-ready 或 submission-ready verdict。
- 不能把 stage replay projection、OPL ledger verification、product-entry manifest success、grouped CLI success、stage folder package refs 或 refs-only accounting closeout 写成 grant-ready、fundability-ready、quality-ready、export-ready 或 submission-ready verdict。
- 不能把 hand-written product-entry / domain_handler / grouped CLI/API / projection / lifecycle wrapper 写成长期合理私有平台。
- 不能把 local journal、attempt ledger、Hermes probe、Gateway/local-manager、flat CLI alias、compatibility aggregate test 或 `codex_cli` executor 写回默认 runtime owner。

## 下一跳

- 目标态：[Med Auto Grant 理想目标态](./references/med-auto-grant-ideal-state.md)
- 差距与顺序：[MAG 理想目标态差距与完善计划](./active/mag-ideal-state-cross-repo-gap-plan.md)
- 文档治理：[MAG 文档组合治理](./docs_portfolio_consolidation.md)
- 过程归档：[MAG standard agent 文档过程归档 2026-05](./history/plans/mag-standard-agent-doc-process-history-2026-05.md)
