# 当前状态

Owner: `Med Auto Grant`
Purpose: `current_status_and_evidence_boundary`
State: `current`
Machine boundary: 本文是人读状态摘要。机器真相继续归 `contracts/runtime-program/current-program.json`、production acceptance contract、schemas、source、CLI/API 行为、product-entry manifest、runtime receipts 与 workspace/artifact outputs。
Date: `2026-05-25`

## 当前结论

`Med Auto Grant` 是医学基金申请 domain agent，也是 OPL-compatible Foundry Agent package。Direct app skill / CLI / `MedAutoGrantDomainEntry` 仍是一等入口；任务启动后的默认运行驻留由 OPL/Temporal hosted autonomous runtime 承担。`Codex CLI` 是当前第一公民 stage executor；`Hermes-Agent`、Claude Code 等只作为显式 opt-in executor adapter / proof lane 接入。

无论从 direct path 还是 OPL 托管 path 进入，执行都必须回到 MAG-owned grant truth、fundability / quality / export verdict、package authority、grant strategy memory accept/reject、owner receipt 和 typed blocker。OPL 持有 Temporal-backed provider runtime、typed queue、scheduler / daemon、attempt ledger、generic transition runner、workspace/source shell、memory locator、artifact/package lifecycle shell、operator projection、observability/SLO、generated wrapper 和 App/workbench shell。

## 当前机器事实摘要

- `contracts/runtime-program/current-program.json` 声明 `default_task_runtime_owner=one-person-lab`、`default_runtime_substrate=temporal`、`default_stage_executor=codex_cli`、`mag_implements_daemon=false`、`mag_implements_scheduler=false`、`mag_implements_attempt_loop=false`、`mag_owns_attempt_ledger=false`。
- `mag_functional_structure_gap_count=0` 与 `standard_agent_source_shape_status=landed` 是当前 contracts/read-model 的历史结构分类信号：它只表示 generic owner intent 已被分类和收薄，不表示 strict standard-agent active source 已物理纯净。当前 active caller 的 product-entry、status/user-loop、sidecar、domain_runtime、lifecycle、projection、autonomy loop 和 CLI shell 仍只能按 MAG domain handler target、refs-only adapter、minimal authority function、diagnostic 或 migration input 读取。
- `claims_opl_descriptor_source_available=true`、`claims_opl_replacement_exists=true`、`claims_domain_repo_physical_delete_authorized=false`、`claims_all_bridge_exits_complete=false`、`claims_production_long_run_soak_complete=false` 共同表示：OPL generated/default caller replacement 与 cutover readiness 已有结构证据，但该证据不授权 MAG repo 物理删除仍被 direct path / domain handler 消费的 active shell，也不关闭 App consumption / live-soak 证据尾项。
- `contracts/external_evidence/mag-evidence-receipt-ledger.json` 已记录 first live production evidence refs；7 个 external evidence request 已全部 refs-only close，包括 generated/hosted caller pack consumption、App/workbench package refs consumption、release/dist consumption、owner receipt / typed blocker roundtrip、continuous no-forbidden-write、direct/hosted parity no-regression 和 Temporal receipt reconciliation ref。该 ledger 仍只保存 refs、receipt shapes、typed blocker / no-regression refs 和 production acceptance refs；`temporal_provider_long_soak_window_evidence` 仍是后续真实证据门。
- Production acceptance tail 已由 MAG-owned owner receipt projection 关闭；这只证明 MAG owner receipt / typed blocker / no-regression evidence 的 refs-only closeout shape，不授权 OPL、Provider、Agent Lab 或 OMA 替 MAG 生成 grant-ready、fundability-ready、quality/export-ready 或 submission-ready verdict。
- `product receipt-readiness` 是当前 MAG product grouped CLI 的 body-free receipt refs readiness 入口，聚合 owner receipt、memory accept/reject receipt、package/export lifecycle handoff 和 cleanup/restore/retention lifecycle receipt refs；它只给 OPL/App/operator closeout 或 executor-first bundle 消费 refs，不声明 grant ready、quality ready、export ready、submission ready、provider long-soak complete 或 production ready。
- `product opl-owner-payload-response` 是 OPL owner-payload workorder 可消费的 body-free response 入口，聚合 production acceptance owner receipt、grant-stage owner-chain refs、workspace receipt-readiness refs、no-regression refs 与 `submission_ready_export_gate` typed blocker refs，并显式输出 success / typed-blocker payload path；该 response 只解决 OPL 记录 payload 的 return-shape 对齐，不关闭 human gate、domain ready、submission-ready 或 production long-soak。
- MAG grant-stage / lifecycle / legacy route-back payload 已可被 OPL refs-only external evidence ledger 记录并验证。该进展只证明 MAG-owned refs、owner-chain refs 与 typed blocker 可被外部 ledger 消费，不授权 OPL 写 grant truth、memory body、artifact body、quality/export verdict，也不声明 submission-ready、production-ready 或 Temporal long-soak complete；具体 attempt、receipt path 和 worklist 过程记录归 [MAG standard agent 文档过程归档 2026-05](./history/plans/mag-standard-agent-doc-process-history-2026-05.md)。
- `package_and_submit_ready` 的 typed blocker projection 已显式输出 `submission_ready_export_gate`、MAG human-gate owner、`human_gate_receipt` requirement，以及 OPL/provider 不可绕过、不等于 submission/export/production ready 的机器字段；这只让 blocker 更可审计，不关闭 human approval gate。
- `physical_skeleton_follow_through` 现在同时暴露 `retired_public_command_scan`，按 `SERVICE_SAFE_DOMAIN_COMMANDS` 与 grouped public CLI catalog 证明 `run-local`、`runtime-run`、`runtime-resume`、`probe-upstream-hermes` 未作为 active public/domain command 复活，并指向对应 fail-closed negative tests。该扫描只证明 repo-local command catalog no-resurrection，不证明 App/workbench 消费、production default caller、physical delete authority 或 Temporal long-soak。

## 当前保留面

- `agent/` 是 Declarative Grant Pack：stage prompts、stage policies、skill declaration、quality gates 和 knowledge refs 是 OPL pack compiler / generated surfaces 的 repo-source 语义输入。
- `contracts/` 是机器合同、handoff、receipt、external evidence request、production acceptance 和 runtime-program 指针。
- `src/med_autogrant/**` 只作为 domain handler、refs-only adapter、minimal authority function、native helper、diagnostic、migration input 或 tombstone/provenance 支撑读取；不得写成 MAG 私有 runtime platform。
- MAG retained private authority surface 限定为 grant domain truth、fundability / quality / export verdict、package authority、grant strategy memory body 与 accept/reject、owner receipt、transition oracle、grant-native helper 和 focused contract tests。
- Product-entry、sidecar、grouped CLI/API、projection、lifecycle、memory/package projection 和 status/user-loop 仍可作为 direct domain handler、refs-only adapter、native helper target 或 migration input 暂时存在；长期 owner 是 OPL generated/hosted surface，当前 strict purity 读法是 replacement-ready 但 physical-delete 未授权。
- 当前 active source 中仍可见的 product-entry、domain_runtime、runtime registration、sidecar、lifecycle、memory/package projection、autonomy loop 和 status/user-loop shell 不是兼容承诺，也不是长期标准智能体组成。满足 explicit MAG owner receipt authorizing physical delete、direct/hosted parity、owner receipt roundtrip、no-active-caller 和 no-resurrection guard 后，旧 wrapper、alias、facade、patch bridge、compat aggregate test 与 legacy runtime/probe residue直接删除；历史只进 `docs/history/**`、提交历史或外部 receipt，不保留 repo-local compatibility shell。

## 已退役面

Local runtime journal / attempt ledger、repo-owned scheduler daemon、upstream Hermes probe、flat shell alias、facade patch bridge、compat aggregate test、Gateway/local-manager default path 和旧 hosted/provider specs 只能作为 history、tombstone、explicit proof history 或 regression oracle 阅读。无 active caller 后直接删除或归档，不新增 compatibility alias、re-export facade 或 compatibility-only 聚合测试。

## 当前证据门

当前剩余工作不再写成 MAG repo 侧结构缺口，统一作为证据门管理：

- 真实 OPL-hosted grant-stage attempt 持续返回 MAG owner receipt、typed blocker 或 no-regression evidence。
- 真实 grant workspace 产生 accepted/rejected memory receipt、package/export lifecycle receipt、cleanup/restore/retention receipt 和 owner receipt scaleout。
- OPL/App/operator closeout 与 executor-first bundle 持续消费 `product receipt-readiness` 输出，并在真实 workspace 中回连 owner receipt、typed blocker、no-regression evidence 与 lifecycle evidence。
- OPL owner-payload workorder 持续消费 `product opl-owner-payload-response` 输出，并在真实 stage/workspace target 上记录 success refs path 或 domain-owned typed-blocker path；空模板或 typed blocker refs 不得被读成 owner-chain/domain-ready/production-ready。
- OPL/App shell 持续消费 MAG package refs、gap report、manual portal boundary、quality refs、transition oracle refs 和 safe action refs。
- `submission_ready_export_gate` 仍需要真实 MAG owner human-gate receipt 或人工审批路径证据；当前 typed blocker projection 只表达阻塞原因与越权禁止。
- External production/default caller、release/dist consumption、continuous no-forbidden-write 和 direct/hosted parity 已有首批 refs-only closeout；后续门槛是持续真实消费与 no-regression 证据。
- Temporal provider 已记录 receipt reconciliation ref，但 long-soak window evidence 仍未关闭；后续门槛是 long SLO、repair cadence 和 live receipt reconciliation 的连续证据。
- Physical morphology cleanup 当前按 strict purity 作为结构删除尾项读取：repo-local active path scan 与 retired public command scan 已守住 legacy default caller / retired command 不复活；production default caller、direct/hosted parity、owner receipt roundtrip、continuous evidence、explicit physical delete owner receipt 与 no-active legacy caller scan 稳定后，才能删除仍有 active handler/adapter caller 的旧 wrapper、alias、facade、patch bridge 和 compat aggregate tests，不保留 compatibility shim。

## 当前入口

- 用户路径：`Med Auto Grant app skill -> product status -> product user-loop -> workspace progress / workspace cockpit -> product direct-entry -> pass / package commands`。
- OPL owner-payload refs：`product receipt-readiness -> product opl-owner-payload-response -> OPL refs-only owner-payload record/verify`。
- Pre-workspace：`discover-funding-opportunities -> select-project-profile -> initialize-intake-workspace`。
- Grant stage plane：`call_and_candidate_intake`、`fundability_strategy`、`specific_aims_and_structure`、`proposal_authoring`、`review_and_rebuttal`、`package_and_submit_ready`。
- Declarative Grant Pack：`agent/prompts/`、`agent/stages/`、`agent/skills/`、`agent/quality_gates/`、`agent/knowledge/`。
- Sidecar：`product sidecar export` / `dispatch` 只返回 refs、owner receipt、typed blocker、verdict refs 与 authority action metadata；它不是常驻 daemon。

## 当前不能声明

- 不能把 `mag_functional_structure_gap_count=0` 写成 strict source-purity 完成、external production/default caller 完成、真实 App/workbench consumption 或 production long-run soak 已完成。
- 不能把 descriptor ready、transition oracle smoke、receipt reconciliation proof、external evidence consumption 或 no-regression evidence 写成 provider SLO / live soak 已完成。
- 不能把 OPL provider completion、matrix runner smoke、package existence、schema completeness、quality scorecard 分数或 controller route 写成 fundability-ready、quality-ready、export-ready 或 submission-ready verdict。
- 不能把 hand-written product-entry / sidecar / grouped CLI/API / projection / lifecycle wrapper 写成长期合理私有平台。
- 不能把 local journal、attempt ledger、Hermes probe、Gateway/local-manager、flat CLI alias、compatibility aggregate test 或 `codex_cli` executor 写回默认 runtime owner。

## 下一跳

- 目标态：[Med Auto Grant 理想目标态](./references/med-auto-grant-ideal-state.md)
- 差距与顺序：[MAG 理想目标态差距与完善计划](./active/mag-ideal-state-cross-repo-gap-plan.md)
- 文档治理：[MAG 文档组合治理](./docs_portfolio_consolidation.md)
- 过程归档：[MAG standard agent 文档过程归档 2026-05](./history/plans/mag-standard-agent-doc-process-history-2026-05.md)
