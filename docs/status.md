# 当前状态

Owner: `Med Auto Grant`
Purpose: `current_status_and_evidence_boundary`
State: `current`
Machine boundary: 本文是人读状态摘要。机器真相继续归 `contracts/runtime-program/current-program.json`、production acceptance contract、schemas、source、CLI/API 行为、product-entry manifest、runtime receipts 与 workspace/artifact outputs。
Date: `2026-05-20`

## 当前角色

`Med Auto Grant` 是医学基金申请 domain agent，也是 OPL-compatible Foundry Agent package。Direct app skill / CLI / `MedAutoGrantDomainEntry` 仍是一等入口；OPL-hosted path 可以发现、托管、唤醒和投影 MAG，但必须回到同一套 MAG-owned grant truth、fundability / quality / export verdict、package authority、grant strategy memory accept/reject、owner receipt 和 typed blocker。

OPL Framework 持有通用 provider runtime、typed queue、attempt ledger、generic transition runner、workspace/source shell、memory locator、artifact/package lifecycle shell、operator projection、observability/SLO、generated wrapper 和 App/workbench shell。MAG 仓内 product-entry、sidecar、grouped CLI/API、projection builder、lifecycle adapter、workspace/source intake、package/memory helper 等 surface 只能写成 direct domain handler、refs-only adapter、minimal authority function、diagnostic、migration input 或 history/tombstone，不能写成长期私有平台。

`Codex CLI` 是当前第一公民 executor。`Hermes-Agent`、Claude Code 等只允许作为显式 opt-in executor adapter / proof lane，通过 OPL receipt/audit/fail-closed 边界接入；不承诺行为、质量或 resume 语义等价。

## 当前运行与文档事实

- 单一 `Med Auto Grant` app skill、CLI、`MedAutoGrantDomainEntry`、product status/user-loop/direct-entry、workspace progress/cockpit、product sidecar export/dispatch 和 package submission-ready 是当前 direct path 与 domain handler surface。
- `agent/` 是 repo-source canonical Declarative Grant Pack；`contracts/` 是机器合同和 handoff；`src/med_autogrant/**` 只保留 domain handler、refs-only adapter、minimal authority function、native helper、diagnostic 或 history/tombstone 角色。
- Workspace state、runtime artifact、receipt instance、submission/export package、临时 build/cache/venv/pycache/pytest cache/install sync 副产物进入 workspace/runtime artifact root 或 `$CODEX_HOME/projects/med-autogrant/runtime-state/`，不写回开发 checkout。
- Descriptor ready、transition oracle smoke、receipt reconciliation proof、no-regression evidence 或 external receipt consumption 只能说明可发现、可投影、可对账、可消费 refs；不能写成 MAG 已是纯 knowledge pack、OPL generated/hosted caller 已完成替换、production default caller 已完成迁移，或 grant-ready / fundability-ready / submission-ready。
- 过程性校准、follow-through、receipt proof 和 closeout 流水归档到 [MAG standard agent 文档过程归档 2026-05](./history/plans/mag-standard-agent-doc-process-history-2026-05.md)，不在本页展开。

## 当前收口状态

当前功能/结构收口、物理源码形态和下一步顺序由 [MAG 理想目标态差距与完善计划](./active/mag-ideal-state-cross-repo-gap-plan.md) 维护。当前状态摘要：

- `mag_functional_structure_gap_count=0`，但这只表示当前结构差距按目标态被关闭或移入证据门，不表示 production long-run soak、真实 App/workbench 消费或 grant-stage scaleout 完成。
- Production acceptance tail 已由 MAG-owned `domain_owner_receipt` projection 关闭；对应机器状态以 `contracts/production_acceptance/mag-production-acceptance.json`、product-entry manifest 和 production live acceptance receipt 为准。
- Real target patch-smoke refs 已纳入 production acceptance / product-entry owner receipt projection；这只证明 target owner 对 patch-loop refs 的消费和 closeout shape，不写 grant truth、artifact body、memory body，也不生成 fundability、quality 或 export verdict；OMA 仍只是 work order / typed blocker 生产者，Agent Lab 仍只是 evidence/gate/read-model control plane。
- Executor-first landing program、stage pack enrichment、independent review receipt gate、external evidence consumption ledger、receipt readiness projection、Codex stage receipt ABI、operator closeout projection 和 physical morphology guard 已有 repo-local machine surfaces；这些 surface 只保存 refs、typed blocker、receipt shape、no-regression refs 和 owner boundary，不保存 grant truth、memory body、artifact body、OPL runtime state 或 App workbench state。
- Local runtime journal / attempt ledger、repo-owned scheduler daemon、upstream Hermes probe、flat shell alias、facade patch bridge 和 compat aggregate test 只允许作为 legacy proof、tombstone 或 regression oracle；无 active caller 后直接删除或归档，不保留 compatibility alias。
- MAG retained private surface 限定为 grant domain truth、fundability / quality / export verdict、package authority、grant strategy memory body 与 accept/reject、owner receipt、transition oracle、grant-native helper 和 focused contract tests。

## 当前证据门

MAG repo 侧 handler/ref-only 边界已收薄：product/status/user-loop/sidecar/grouped CLI/projection/lifecycle wrapper 的目标长期 owner 固定为 OPL generated/hosted surface；当前仍由 MAG CLI/product-status/sidecar 触达的 surface 只允许写成 direct domain handler、domain handler target、refs-only adapter、owner receipt、typed blocker、verdict refs、safe action metadata 或 minimal authority function。

2026-05-19 语义包归位：`agent/README.md` 已从 skeleton anchor 升级为 Declarative Grant Pack 入口；`agent/prompts/` 为六个 MAG stage 提供真实 stage prompt；`agent/stages/` 固定 stage policy；`agent/skills/` 固定 domain skill 声明；`agent/quality_gates/` 固定 fundability、quality、export/package、memory/receipt 与 authority 边界；`agent/knowledge/` 固定 grant strategy memory、package authority 与 owner receipt 知识边界。`contracts/stage_control_plane.json` 的 `prompt_refs` 解析到 `agent/prompts/*.md`，`contracts/pack_compiler_input.json` 的 `required_domain_pack_paths` 强制列出完整 pack 文件。

2026-05-20 executor-first 并行落地已完成 repo-local machine surfaces：`contracts/production_acceptance/mag-executor-first-landing.json` 固定 `surface_kind=mag_executor_first_landing_program.v1`、`state=structural_ready_evidence_gated`，并把 `stage_pack_enrichment`、`independent_review_receipt_gate`、`external_evidence_pack_consumption`、`real_workspace_receipt_scaleout` 和 `physical_morphology_hygiene` 五条 lane 机器化。该 program 的策略是 `executor_first` / `default_executor=codex_cli` / `runtime_model=contract_light`，并显式声明 `mag_implements_opl_runtime=false`、`mag_implements_app_workbench=false`、`missing_evidence_claimed_complete=false`。

同日 executor-first landing program 已同步 production acceptance tail 的真实闭环状态：`owner_receipt_scaleout_state=production_acceptance_tail_closed_by_domain_owner_receipt_external_scaleout_gated`，并引用 `receipt:mag/production-live-acceptance/2026-05-20` 与 `/product_entry_manifest/production_live_acceptance_receipt`。Lane 3 已继续把 external evidence ledger 推进到 `state=first_live_production_evidence_consumed_refs_only_long_soak_window_open`：external default caller、Codex App/workbench package refs、owner receipt / typed blocker roundtrip、continuous no-forbidden-write、direct/hosted parity no-regression 和 Temporal reconciliation refs 均以 body-free receipt refs 记录。该状态只表示 MAG 可消费 first live production evidence refs，并保留 `temporal_provider_long_soak_window_evidence` 作为 open 证据门；MAG 仍不声明 OPL provider/domain ready、grant-ready、fundability-ready 或 submission-ready export。

同日 `agent/**` 已从薄 descriptor 扩写为可直接支撑 Codex stage execution 的 richer Declarative Grant Pack：六个 stage prompt、stage policy、quality gate 与 knowledge boundary 都补齐 role、inputs、executor behavior、expected refs、typed blockers、forbidden shortcuts 和 handoff receipt 语义。quality / closure scorecard 已新增 `independent_review_evidence` 合同，要求 execution artifact ref、独立 review artifact ref、review receipt ref、reviewer identity 与 no-shared-context verification；缺少这些 refs 时保持 `projection_only` / `ai_reviewer_required`，不能给出 AI reviewer-backed ready claim。

2026-05-19 stage cohort-loop refs 已补齐：六个 MAG stage 的 `stage_contract` 均声明 source scope、auditable grant cohort query、OPL queue trigger、grant progress / task lifecycle monitor 和 operator freshness metric refs。OPL `stages cohort-loop --domain mag` 读取当前 MAG main 后返回 6/6 `closed_loop_ready`、`blocker_count=0`。该状态只证明 OPL 可消费 MAG declarative launch/readiness 闭环，不表示外部 default caller、真实 App/workbench 消费、grant-stage owner receipt scaleout 或 Temporal long soak 已完成。

2026-05-20 OPL stage production evidence route 已把 MAG stage 的 unobserved expected receipt / monitor freshness 缺口纳入 OPL-owned refs-only `stage_production_evidence_receipt_record|verify` safe action。MAG 不复制该通用 evidence ledger 或 App route；MAG 当前在 `contracts/stage_control_plane.json` 为六个 stage 回填 `expected_receipt_refs`、`monitor_freshness_refs` 和 `stage_production_evidence_closeout`，并在 `contracts/external_evidence/mag-evidence-receipt-ledger.json#/grant_stage_controlled_attempt_closeout` 记录 body-free owner receipt closeout、release/dist consumption、no-forbidden-write、direct/hosted parity 和 Temporal reconciliation refs。OPL receipt verified 仍不等于 grant-ready、fundability-ready、quality/export-ready、submission-ready 或 external production/default caller 成功。

2026-05-21 MAG 已在 `contracts/external_evidence/mag-evidence-receipt-ledger.json#/grant_stage_controlled_attempt_closeout/opl_stage_evidence_receipt_handoff` 声明 stage-level body-free owner receipt handoff refs。OPL 已用这些 MAG-owned receipt refs、App workorder 要求的 exact monitor freshness refs，并为 `package_and_submit_ready` 补充 `human_gate:submission_ready_export_gate`，逐 stage 执行 `stage-production-evidence:medautogrant:<stage>:record|verify`。当前 OPL App/readiness/production closeout 不再把 MAG stage expected receipt / monitor freshness 显示为 open；这只关闭 OPL refs-only workorder accounting，不声明 grant-ready、fundability-ready、quality/export-ready、submission-ready、Temporal long-soak 或真实 App/workbench consumption 完成。

机器面同步到 `mag_handler_boundary_ready_external_caller_evidence_gated` / `mag_handler_boundary_ready_external_evidence_gated`：`functional_privatization_audit`、`product-entry manifest`、`sidecar export`、`current-program` 和 `opl-family-contract-adoption` 均声明 `claims_opl_replacement_exists=false`、`claims_all_bridge_exits_complete=false`、`claims_production_long_run_soak_complete=false`。这表示 MAG repo 侧已把自身 surface 收到 handler/ref-only/authority 边界，不表示外部 production/default caller、真实 App/workbench 消费、全部 bridge exit 或长时 soak 已完成。

`mag_consumer_thinning_contract.generated_surface_handoff.current_mag_path_status` 现在为 generated/bridge surface 的每个 `current_mag_paths` 输出 machine-readable currentness proof；`missing_current_mag_path_count=0`，`stale_path_policy=history_or_source_ref_refresh_only`。该 proof 只证明 MAG 当前 handler/ref-only/authority source refs 存在，不能写成 OPL replacement exists、bridge exit complete 或 production soak complete。

`mag_consumer_thinning_contract.external_evidence_request_pack` 现在把剩余外部证据门机器化为 `mag.external_evidence_request_pack.v1`：OPL generated/hosted caller pack consumption、Codex App workbench package refs consumption、production/default caller release/dist consumption、owner receipt / typed blocker roundtrip、continuous no-forbidden-write、direct/hosted parity 和 Temporal provider long-soak receipt reconciliation。Lane 3 已把 `contracts/external_evidence/mag-evidence-receipt-ledger.json` 从 request-level typed blocker accounting 推进为 first live production evidence refs：7 条 request 都有 verified external receipt ref，`domain_owned_typed_blocker_count=0`，且 `remaining_real_evidence_gap_ids=["temporal_provider_long_soak_window_evidence"]` 继续标记长时 soak 窗口证据未关闭。该 ledger 只保存 refs、receipt shapes、typed blocker / no-regression refs 和 production acceptance refs，不保存 grant truth、memory body、artifact body、OPL runtime state 或 App workbench state。

first live evidence closure 的机器边界是正向但有限的：`claims_external_runtime_evidence_received=true`、`claims_direct_hosted_parity_passed=true`、`temporal_provider_reconciliation_ref_recorded=true` 只属于 MAG 对外部 receipt refs 的 consumption ledger；`claims_temporal_provider_long_soak_complete=false`、`claims_grant_or_fundability_ready=false`，且 authority boundary 继续声明 MAG 不实现 OPL runtime / App workbench、不让 OPL 声明 fundability / quality / export verdict。

MAG product-entry 现在新增五个 repo-local read/guard projection，用于消费这些 refs，而不是替代 OPL/App/runtime。`external_evidence_consumption_ledger` 校验 external evidence request pack 与 incoming receipt 的 `request_id`、`receipt_shape`、`producer_owner` 和 refs-only payload，状态只在 `request_pack_declared_external_evidence_not_claimed` / `partial_consumption_evidence` / `consumed_complete` 之间投影；即使 consumed complete，也不授权 fundability、quality、export 或 submission-ready。`receipt_readiness_projection` 聚合 owner receipt、memory accept/reject receipt、package/export lifecycle receipt 与 cleanup/restore/retention lifecycle receipt 的 coverage，状态只到 `receipt_refs_ready_not_quality_ready`，不能生成质量或提交 ready verdict。`codex_stage_execution_receipt_bundle` 把 Codex-first execution attempt 与独立 review attempt 收成 refs-only ABI，强制 separate invocation、separate task record、independent context；缺 review receipt 时 fail-closed typed blocker required。`operator_closeout_readiness_projection` 把 production acceptance tail、external evidence receipt ledger 与 receipt readiness 合并为 operator closeout read model，明确 request accounting closure、receipt coverage 与 real external evidence / quality readiness 不等价。`physical_morphology_guard_projection` 只读取 source path、module role、evidence refs 与 forbidden role flags，保持 cleanup evidence-gated，不把 role classification 或 cleanup ledger 写成 physical cleanup complete。

local runtime journal / attempt ledger、repo-owned scheduler daemon、upstream Hermes probe、flat shell alias、facade patch bridge 和 compat aggregate test 现在只允许作为 legacy proof / tombstone / regression oracle 存在；无 active caller 后直接删除或归档，不保留 compatibility alias。

2026-05-19 OPL legacy cleanup 读取当前 MAG `physical_skeleton_follow_through` 后返回 `plan_status=ready`、`lifecycle_apply.status=dry_run_ready`、`safe_action_count=3`、`unsafe_action_count=0`；随后 `--mode apply` 已写入 1 条 batch receipt 与 3 条 action receipts，`--mode verify` 可读回 batch / tombstone / handoff receipts 和 2 条 domain owner handoff receipt refs。MAG manifest 已为 physically removed Gateway/local-manager active path 提供 domain owner handoff receipt refs，并提供 replacement parity、no-regression、history 和 tombstone refs。该状态只关闭 OPL cleanup gate / refs-only ledger blocker；外部 production/default caller、真实 App/workbench consumption、grant-stage live soak 和 owner receipt scaleout 仍是证据门。

MAG retained private surface 限定为 grant domain truth、fundability / quality / export verdict、package authority、grant strategy memory body 与 accept/reject、owner receipt、transition oracle、grant-native helper 和 focused contract tests。

Retained private authority surfaces 现在在 `functional_privatization_audit`、product-entry manifest、sidecar export 与 pack compiler input 中携带 AI-first taxonomy、judgment owner、programmatic role、allowed return shapes 和 forbidden output boundary。`fundability_verdict`、`quality_verdict`、`export_verdict` 与 `memory_accept_reject` 是 AI-first judgment surface，程序只 materialize refs / guard / typed blocker；`package_authority`、`owner_receipt_signer` 与 `grant_helper` 是 programmatic authority/helper surface，只能签 receipt、验证 refs 或返回 action metadata。所有 surface 都禁止从 schema completeness、provider completion、package existence、quality scorecard 分数或 generic lifecycle completion 机械生成 ready verdict。

Physical source morphology 当前按同一边界读取：`agent/` 是 Declarative Grant Pack，`contracts/` 是机器合同和 handoff，`src/med_autogrant/**` 中的 product-entry、sidecar、domain_runtime、runtime registration、lifecycle、package/memory projection、observability 或 workbench/scheduler metadata 只能是 direct domain handler、refs-only adapter、minimal authority function、diagnostic 或 history/tombstone。MAG 不再维护 local journal、attempt ledger、repo-owned scheduler daemon、Hermes/Gateway/local-manager probe 或 compatibility facade；后续新增功能默认进入 `agent/` pack、`contracts/`、authority function 或 domain handler，不恢复本地 runtime 平台。

当前物理源码仍不是“新建标准 Agent 模板”形态：`domain_runtime_parts/substrate.py`、`domain_entry.py`、`cli.py`、`product_entry_parts/manifest_builder.py` / `manifest.py` / `sidecar.py` / `runtime_registration.py`、`control_plane.py`、owner receipt helper 和 `grant_autonomy_controller.py` 仍是 active direct path、refs-only adapter、authority refs、regression oracle 或 migration input。它们不能被写成 MAG-owned generic runtime，也不能被写成已经物理清零。后续 cleanup 需要 OPL generated caller / App / production default caller evidence、direct/hosted parity、owner receipt roundtrip、no-forbidden-write 和 active caller migration 同时成立后再改名、迁出、删除或 tombstone。

2026-05-19 fresh cleanup audit 结论：`.worktrees/retire-generic-runtime-surfaces` / `codex/retire-mag-generic-runtime-surfaces` 是 stale lane，分支提交已在当前 `main` 祖先链上，旧 dirty 删除已被当前 `main` 覆盖。该 lane 不再提供可重放代码 cleanup；重新合入会反向带回旧 Hermes/local-runtime 文件并损坏当前 stage runtime event refs 口径。当前应清理 stale worktree / branch，并把剩余 gap 继续限定为外部 OPL/App/production caller evidence gate。

## 当前测试/证据差距

以下证据门单独统计，不能反向重开 MAG repo 侧 active bridge exit：

- 真实 OPL-hosted grant-stage attempt 持续返回 MAG owner receipt、typed blocker 或 no-regression evidence。
- 真实 grant workspace 产生 accepted/rejected memory receipt、package/export lifecycle receipt、cleanup/restore/retention receipt 和 owner receipt scaleout。
- OPL/App shell 持续消费 MAG package refs、gap report、manual portal boundary、quality refs、transition oracle refs 和 safe action refs。
- External production/default caller、release/dist consumption、continuous no-forbidden-write 和 direct/hosted parity 的后续连续证据。
- Temporal provider long SLO、repair cadence 和 live receipt reconciliation 的后续连续证据。

这些证据门已由 `external_evidence_request_pack` 给出 request id、required refs 和 required receipt shapes；production acceptance lane 现在由 `contracts/production_acceptance/mag-production-acceptance.json` 持有 MAG-owned tail 状态。当前不是结构缺口；`domain_owner_live_acceptance_receipt_scaleout_required` 已由 MAG-owned `domain_owner_receipt` projection 关闭，并通过 `tests/test_production_acceptance.py` 与 `tests/product_entry_cases/test_production_live_acceptance.py` 验证 owner boundary。Lane 3 的 first live production evidence refs 已记录外部 default caller、App/workbench consumption、direct/hosted parity、continuous guard 和 Temporal reconciliation 的首轮 receipt refs；Temporal long-soak window evidence 仍 open。这些 receipts 还只是 refs-only acceptance surface，不能替代后续连续生产监控、真实 grant workspace 扩面和 MAG-owned quality/export verdict。

Executor-first landing program 进一步把这些差距收束为可并行推进的 evidence gates：stage pack enrichment、independent review requirement、MAG-owned production acceptance tail closure state sync、external evidence consumption ledger、`contracts/external_evidence/mag-evidence-receipt-ledger.json` first live production evidence closure、grant-stage controlled attempt body-free closeout、receipt readiness projection、Codex stage receipt ABI、operator closeout projection 和 physical morphology guard 已由 MAG repo-local code/schema/tests 落地。当前 7 条 external evidence request 均已记录 verified external receipt refs，且 `temporal_provider_long_soak_window_evidence` 仍 open；physical morphology cleanup 仍需在 active caller migration、continuous evidence 和 owner receipt roundtrip 稳定后推进，不能由 MAG 内部结构通过来替代。

## 当前物理源码形态差距

- product/status/progress/cockpit/direct-entry/user-loop/sidecar 仍由 MAG repo-local handler 暴露；目标是 OPL generated/hosted wrapper default 化，MAG 只保留 grant handler target、receipt、typed blocker、verdict refs 与 action metadata。
- `domain_runtime_parts/substrate.py` 与 `domain_entry.py` 仍像 runtime/domain entry 聚合层；目标是保持 route/authority adapter 与 regression oracle，不承载 generic runner、queue、attempt ledger、session shell 或 workbench shell。
- runtime registration、control plane、lifecycle/memory/package projection 和 owner receipt helper 仍在 MAG 内维护 refs-only envelope；目标是 OPL lifecycle/session/workbench caller 稳定后只保留 grant authority refs。
- autonomy controller 只能表达 grant route / budget / blocker policy；不能用 loop/scheduler 形态替代 OPL provider runtime，也不能用程序分数替代 AI-first fundability、quality 或 export verdict。

## 当前入口

- 用户路径：`Med Auto Grant app skill -> product status -> product user-loop -> workspace progress / workspace cockpit -> product direct-entry -> pass / package commands`。
- Pre-workspace：`discover-funding-opportunities -> select-project-profile -> initialize-intake-workspace`。
- Grant stage plane：`family_stage_control_plane` 暴露 `call_and_candidate_intake`、`fundability_strategy`、`specific_aims_and_structure`、`proposal_authoring`、`review_and_rebuttal`、`package_and_submit_ready`。
- Declarative Grant Pack：`agent/prompts/`、`agent/stages/`、`agent/skills/`、`agent/quality_gates/`、`agent/knowledge/` 是 OPL pack compiler 和 generated surfaces 的 repo-source 语义输入。
- 质量治理：`workspace quality-scorecard`、`workspace quality-closure-dossier`、`workspace quality-diff`；这些是 AI critique-backed aggregator，不是机械 ready verdict。
- Sidecar：`product sidecar export` / `dispatch` 只返回 refs、owner receipt、typed blocker、verdict refs 与 authority action metadata；不是常驻 daemon。

## 当前不能声明

- 不能把 `mag_functional_structure_gap_count=0` 写成 external production/default caller、真实 App/workbench consumption 或 production long-run soak 已完成。
- 不能把 descriptor ready、transition oracle smoke、receipt reconciliation proof、external evidence consumption 或 no-regression evidence 写成 provider SLO / live soak 已完成。
- 不能把 OPL provider completion、matrix runner smoke、package existence、schema completeness、quality scorecard 分数或 controller route 写成 fundability-ready、quality-ready、export-ready 或 submission-ready verdict。
- 不能把 hand-written product-entry / sidecar / grouped CLI/API / projection / lifecycle wrapper 写成长期合理私有平台。
- 不能把 local journal、attempt ledger、Hermes probe、Gateway/local-manager、flat CLI alias、compatibility aggregate test 或 `codex_cli` executor 写回默认 runtime owner。

## 目录与验证口径

- repo-tracked 主线不保留项目级 `.codex/`、`.omx/`、`.runtime-program/`、`.agent-contract-baseline.json` 或 `runtime-state/`；本机 session、prompt、log、report 与 hook 状态统一属于 `$CODEX_HOME/projects/med-autogrant/runtime-state/`。
- Python / pytest lane 必须通过 `scripts/run-python-clean.sh` 或 `scripts/run-pytest-clean.sh`，把 bytecode、pytest cache 和安装/同步副产物导向仓库外部。
- 测试口径只固定 machine-readable contract、schema、CLI/API、generated artifact 结构与污染 guard；`README*`、`docs/**` 和 skill 正文文案不作为稳定断言面。

## 下一跳

- 目标态：[Med Auto Grant 理想目标态](./references/med-auto-grant-ideal-state.md)
- 差距与顺序：[MAG 理想目标态差距与完善计划](./active/mag-ideal-state-cross-repo-gap-plan.md)
- 文档治理：[MAG 文档组合治理](./docs_portfolio_consolidation.md)
- 过程归档：[MAG standard agent 文档过程归档 2026-05](./history/plans/mag-standard-agent-doc-process-history-2026-05.md)
