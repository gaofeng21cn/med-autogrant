# 当前状态

Owner: `Med Auto Grant`
Purpose: `current_status_and_evidence_boundary`
State: `current`
Machine boundary: 本文是人读状态摘要。机器真相继续归 `contracts/runtime-program/current-program.json`、production acceptance contract、schemas、source、CLI/API 行为、product-entry manifest、runtime receipts 与 workspace/artifact outputs。
Date: `2026-05-27`

## 当前结论

`Med Auto Grant` 是医学基金申请 domain agent，也是 OPL-compatible Foundry Agent package。Direct app skill / CLI / `MedAutoGrantDomainEntry` 仍是一等入口；任务启动后的默认运行驻留由 OPL/Temporal hosted autonomous runtime 承担。`Codex CLI` 是当前第一公民 stage executor；`Hermes-Agent`、Claude Code 等只作为显式 opt-in executor adapter / proof lane 接入。

无论从 direct path 还是 OPL 托管 path 进入，执行都必须回到 MAG-owned grant truth、fundability / quality / export verdict、package authority、grant strategy memory accept/reject、owner receipt 和 typed blocker。OPL 持有 Temporal-backed provider runtime、typed queue、scheduler / daemon、attempt ledger、generic transition runner、workspace/source shell、memory locator、artifact/package lifecycle shell、operator projection、observability/SLO、generated wrapper 和 App/workbench shell。

## 当前机器事实摘要

- `contracts/runtime-program/current-program.json` 声明 `default_task_runtime_owner=one-person-lab`、`default_runtime_substrate=temporal`、`default_stage_executor=codex_cli`、`mag_implements_daemon=false`、`mag_implements_scheduler=false`、`mag_implements_attempt_loop=false`、`mag_owns_attempt_ledger=false`。
- `mag_functional_structure_gap_count=0` 与 `standard_agent_source_shape_status=landed` 是当前 contracts/read-model 的历史结构分类信号：它只表示 generic owner intent 已被分类和收薄，不表示 strict standard-agent active source 已物理纯净。当前 active caller 的 product-entry、status/user-loop、domain_handler、domain_runtime、lifecycle、projection、autonomy loop 和 CLI shell 仍只能按 MAG domain handler target、refs-only adapter、minimal authority function、diagnostic 或 migration input 读取。
- `claims_opl_descriptor_source_available=true`、`claims_opl_replacement_exists=true`、`claims_domain_repo_physical_delete_authorized=false`、`claims_all_bridge_exits_complete=false`、`claims_production_long_run_soak_complete=false` 共同表示：OPL generated/default caller replacement 与 cutover readiness 已有结构证据，但该证据不授权 MAG repo 物理删除仍被 direct path / domain handler 消费的 active shell，也不关闭 App consumption / live-soak 证据尾项。
- `contracts/external_evidence/mag-evidence-receipt-ledger.json` 已记录 first live production evidence refs；7 个 external evidence request 已全部 refs-only close，包括 generated/hosted caller pack consumption、App/workbench package refs consumption、release/dist consumption、owner receipt / typed blocker roundtrip、continuous no-forbidden-write、direct/hosted parity no-regression 和 Temporal receipt reconciliation ref。该 ledger 仍只保存 refs、receipt shapes、typed blocker / no-regression refs 和 production acceptance refs；`temporal_provider_long_soak_window_evidence` 仍是后续真实证据门。
- Production acceptance tail 已由 MAG-owned owner receipt projection 关闭；这只证明 MAG owner receipt / typed blocker / no-regression evidence 的 refs-only closeout shape，不授权 OPL、Provider、Agent Lab 或 OMA 替 MAG 生成 grant-ready、fundability-ready、quality/export-ready 或 submission-ready verdict。
- `authority receipt-readiness` 是当前 MAG grouped CLI 的 body-free receipt refs readiness 入口，聚合 owner receipt、memory accept/reject receipt、package/export lifecycle handoff 和 cleanup/restore/retention lifecycle receipt refs；它只给 OPL/App/operator closeout 或 executor-first bundle 消费 refs，不声明 grant ready、quality ready、export ready、submission ready、provider long-soak complete 或 production ready。
- `authority owner-payload-response` 是 OPL owner-payload workorder 可消费的 body-free response 入口，聚合 production acceptance owner receipt、grant-stage owner-chain refs、workspace receipt-readiness refs、no-regression refs 与 `submission_ready_export_gate` typed blocker refs，并显式输出 success / typed-blocker payload path；它还从 `grant_stage_controlled_attempt_closeout` 暴露逐 stage expected receipt / monitor freshness / runtime event refs summary，并把 source/runtime live-evidence pending 表达为 MAG-owned typed blocker path。该 response 只解决 OPL 记录 payload 的 return-shape 对齐，不关闭 human gate、domain ready、submission-ready 或 production long-soak。
- OPL `domain-owner-payload-summary` ledger 已记录并验证 7 条 MAG recommended typed-blocker path receipt：`package_and_submit_ready/submission_ready_export_gate` 仍是 human-approval-required，`call_and_candidate_intake`、`fundability_strategy`、`specific_aims_and_structure`、`proposal_authoring`、`review_and_rebuttal` 与 `package_and_submit_ready` 六个 stage expected receipt 仍是 source/runtime-live-evidence pending。该 OPL refs-only verification 只证明 MAG owner-payload response 可被外部 workorder record/verify，不创建 MAG owner receipt、human-gate approval、grant/fundability/export/submission readiness 或 production long-soak closeout。
- Workspace receipt scaleout 已有 repo-tracked body-free snapshot：`contracts/production_acceptance/mag-workspace-receipt-scaleout-evidence-20260527.json` 记录 4 个 MAG workspace 样本通过 MAG-owned owner receipt、memory accept/reject receipt、package/export lifecycle handoff 与 cleanup/restore/retention lifecycle receipt surface 形成 36 条 receipt refs，并进入 `owner-payload-response`；snapshot 同步记录 6-stage expected receipt payload summary 可被 OPL/App 读取。该 snapshot 只证明 MAG app surface 可重复产出 refs-only owner payload；`submission_ready_export_gate` typed blocker 仍阻塞 human gate，不声明 grant-ready、quality-ready、export-ready、submission-ready、provider long-soak complete 或 physical delete authorized。
- Product-entry manifest 默认暴露 `owner_payload_response` 与 `workspace_receipt_scaleout_evidence`，来源限定为 repo-tracked production acceptance、external evidence ledger 和 workspace scaleout snapshot；因此 OPL/App/operator 的默认 manifest consumer 可发现 MAG owner-payload summary，不需要 fixture 注入。`owner_payload_response.manifest_consumer_evidence` 现在把默认 manifest consumer 实际消费的 owner payload refs、stage expected receipt payload、workspace scaleout count-only provenance 和 `submission_ready_export_gate` blocker refs 固化为 machine-readable evidence，并暴露 `sustained_consumption_followthrough_workorder`，要求后续由真实 App/operator 或 release default caller 提交 `app_operator_consumption_ref`、`default_caller_consumption_ref`、owner payload / workspace scaleout refs、no-forbidden-write ref 与 long-soak 或 typed blocker ref。该 manifest 面只提供 body-free refs-only / count-only provenance 和下一步 payload contract，不创建 owner receipt、typed blocker 或 operator payload，不声明 grant-ready、quality-ready、export-ready、submission-ready、provider long-soak complete 或 App sustained-consumption closeout。
- `authority manifest-consumption-payload` 是当前 MAG grouped CLI 的 sustained-consumption payload response 入口，用于校验真实 App/operator 或 release default caller 提交的 `sustained_consumption_followthrough_workorder` payload。该入口只接受 success refs path 或 typed-blocker path，输出 body-free `mag_manifest_sustained_consumption_payload_response` 和 OPL 可记录 refs，不创建 operator payload、不签发 MAG owner receipt、不读取 memory/artifact body，也不声明 App sustained-consumption、grant/submission-ready 或 provider long-soak 完成。
- MAG grant-stage / lifecycle / legacy route-back payload 已可被 OPL refs-only external evidence ledger 记录并验证。该进展只证明 MAG-owned refs、owner-chain refs 与 typed blocker 可被外部 ledger 消费，不授权 OPL 写 grant truth、memory body、artifact body、quality/export verdict，也不声明 submission-ready、production-ready 或 Temporal long-soak complete；具体 attempt、receipt path 和 worklist 过程记录归 [MAG standard agent 文档过程归档 2026-05](./history/plans/mag-standard-agent-doc-process-history-2026-05.md)。
- `contracts/stage_control_plane.json` 已为 6 个 grant stage 的 `stage_contract` 声明 OPL 标准 `user_stage_log_contract`。后续 MAG stage closeout 必须提供面向用户的人话摘要：本 stage 的基金问题、目标、做了什么 grant work、改动 surface、结果、剩余 blocker 和证据 refs；OPL `stage_progress_log.user_stage_log` 只投影这些 MAG-owned 语义和通用 duration/token/cost，不能替 MAG 推断 fundability、quality、export 或 submission-ready 状态。
- `package_and_submit_ready` 的 typed blocker projection 已显式输出 `submission_ready_export_gate`、MAG human-gate owner、`human_gate_receipt` requirement，以及 OPL/provider 不可绕过、不等于 submission/export/production ready 的机器字段；这只让 blocker 更可审计，不关闭 human approval gate。
- OPL external evidence ledger 已把 MAG `package_and_submit_ready` stage production evidence 记录并验证为 stage 专用 receipt：source scope refs 与 `runtime_event:package_and_submit_ready.owner_receipt_recorded` 已被 App/operator 读为 observed，`human_gate:submission_ready_export_gate` expected receipt 与 monitor freshness 继续由 MAG-owned typed blocker 阻塞。该 receipt 只证明 OPL 能消费 MAG stage refs / typed blocker，不是 human approval、submission-ready、export-ready、grant-ready 或 production-ready verdict。
- `physical_skeleton_follow_through` 现在同时暴露 `retired_public_command_scan`，按 `SERVICE_SAFE_DOMAIN_COMMANDS` 与 grouped public CLI catalog 证明 `run-local`、`runtime-run`、`runtime-resume`、`probe-upstream-hermes` 未作为 active public/domain command 复活，并指向对应 fail-closed negative tests。该扫描只证明 repo-local command catalog no-resurrection，不证明 App/workbench 消费、production default caller、physical delete authority 或 Temporal long-soak。

## 当前保留面

- `agent/` 是 Declarative Grant Pack：stage prompts、stage policies、skill declaration、quality gates 和 knowledge refs 是 OPL pack compiler / generated surfaces 的 repo-source 语义输入。
- `contracts/` 是机器合同、handoff、receipt、external evidence request、production acceptance 和 runtime-program 指针。
- `src/med_autogrant/**` 只作为 domain handler、refs-only adapter、minimal authority function、native helper、diagnostic、migration input 或 tombstone/provenance 支撑读取；不得写成 MAG 私有 runtime platform。
- MAG retained private authority surface 限定为 grant domain truth、fundability / quality / export verdict、package authority、grant strategy memory body 与 accept/reject、owner receipt、transition oracle、grant-native helper 和 focused contract tests。
- Product-entry、domain_handler、grouped CLI/API、projection、lifecycle、memory/package projection 和 status/user-loop 仍可作为 direct domain handler、refs-only adapter、native helper target 或 migration input 暂时存在；长期 owner 是 OPL generated/hosted surface，当前 strict purity 读法是 replacement-ready 但 physical-delete 未授权。
- 当前 active source 中仍可见的 product-entry、domain_runtime、runtime registration、domain_handler、lifecycle、memory/package projection、autonomy loop 和 status/user-loop shell 不是兼容承诺，也不是长期标准智能体组成。满足 explicit MAG owner receipt authorizing physical delete、direct/hosted parity、owner receipt roundtrip、no-active-caller 和 no-resurrection guard 后，旧 wrapper、alias、facade、patch bridge、compat aggregate test 与 legacy runtime/probe residue直接删除；历史只进 `docs/history/**`、提交历史或外部 receipt，不保留 repo-local compatibility shell。

## 已退役面

Local runtime journal / attempt ledger、repo-owned scheduler daemon、upstream Hermes probe、flat shell alias、facade patch bridge、compat aggregate test、Gateway/local-manager default path 和旧 hosted/provider specs 只能作为 history、tombstone、explicit proof history 或 regression oracle 阅读。无 active caller 后直接删除或归档，不新增 compatibility alias、re-export facade 或 compatibility-only 聚合测试。

## 当前证据门

当前剩余工作不再写成 MAG repo 侧结构缺口，统一作为证据门管理：

- 真实 OPL-hosted grant-stage attempt 持续返回 MAG owner receipt、typed blocker 或 no-regression evidence。
- 真实 grant workspace 继续产生 accepted/rejected memory receipt、package/export lifecycle receipt、cleanup/restore/retention receipt 和 owner receipt scaleout；当前已有 4 workspace body-free refs-only scaleout snapshot，后续仍需真实 owner human-gate receipt、long-soak 与 sustained App/operator consumption。
- OPL/App/operator closeout 与 executor-first bundle 持续消费 `authority receipt-readiness` 输出，并在真实 workspace 中回连 owner receipt、typed blocker、no-regression evidence 与 lifecycle evidence。
- OPL owner-payload workorder 已消费 `authority owner-payload-response` 的 7 条 recommended typed-blocker path 并完成 refs-only record/verify；后续仍需在真实 stage/workspace target 上持续记录 owner receipt success refs path、stage expected receipt / monitor freshness / runtime event refs，或更新后的 domain-owned typed-blocker path。默认 manifest consumer evidence和 OPL ledger verification 都不能替代真实 owner-chain/domain-ready/production-ready。
- OPL/App shell 持续消费 MAG package refs、gap report、manual portal boundary、quality refs、transition oracle refs 和 safe action refs。
- `submission_ready_export_gate` 仍需要真实 MAG owner human-gate receipt 或人工审批路径证据；当前 typed blocker projection 只表达阻塞原因与越权禁止。
- External production/default caller、release/dist consumption、continuous no-forbidden-write 和 direct/hosted parity 已有首批 refs-only closeout；后续门槛是持续真实消费与 no-regression 证据。
- Temporal provider 已记录 receipt reconciliation ref，但 long-soak window evidence 仍未关闭；后续门槛是 long SLO、repair cadence 和 live receipt reconciliation 的连续证据。
- Physical morphology cleanup 当前按 strict purity 作为结构删除尾项读取：repo-local active path scan 与 retired public command scan 已守住 legacy default caller / retired command 不复活；production default caller、direct/hosted parity、owner receipt roundtrip、continuous evidence、explicit physical delete owner receipt 与 no-active legacy caller scan 稳定后，才能删除仍有 active handler/adapter caller 的旧 wrapper、alias、facade、patch bridge 和 compat aggregate tests，不保留 compatibility shim。

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
- 不能把 hand-written product-entry / domain_handler / grouped CLI/API / projection / lifecycle wrapper 写成长期合理私有平台。
- 不能把 local journal、attempt ledger、Hermes probe、Gateway/local-manager、flat CLI alias、compatibility aggregate test 或 `codex_cli` executor 写回默认 runtime owner。

## 下一跳

- 目标态：[Med Auto Grant 理想目标态](./references/med-auto-grant-ideal-state.md)
- 差距与顺序：[MAG 理想目标态差距与完善计划](./active/mag-ideal-state-cross-repo-gap-plan.md)
- 文档治理：[MAG 文档组合治理](./docs_portfolio_consolidation.md)
- 过程归档：[MAG standard agent 文档过程归档 2026-05](./history/plans/mag-standard-agent-doc-process-history-2026-05.md)
