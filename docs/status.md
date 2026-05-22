# 当前状态

Owner: `Med Auto Grant`
Purpose: `current_status_and_evidence_boundary`
State: `current`
Machine boundary: 本文是人读状态摘要。机器真相继续归 `contracts/runtime-program/current-program.json`、production acceptance contract、schemas、source、CLI/API 行为、product-entry manifest、runtime receipts 与 workspace/artifact outputs。
Date: `2026-05-22`

## 当前结论

`Med Auto Grant` 是医学基金申请 domain agent，也是 OPL-compatible Foundry Agent package。Direct app skill / CLI / `MedAutoGrantDomainEntry` 仍是一等入口；任务启动后的默认运行驻留由 OPL/Temporal hosted autonomous runtime 承担。`Codex CLI` 是当前第一公民 stage executor；`Hermes-Agent`、Claude Code 等只作为显式 opt-in executor adapter / proof lane 接入。

无论从 direct path 还是 OPL 托管 path 进入，执行都必须回到 MAG-owned grant truth、fundability / quality / export verdict、package authority、grant strategy memory accept/reject、owner receipt 和 typed blocker。OPL 持有 Temporal-backed provider runtime、typed queue、scheduler / daemon、attempt ledger、generic transition runner、workspace/source shell、memory locator、artifact/package lifecycle shell、operator projection、observability/SLO、generated wrapper 和 App/workbench shell。

## 当前机器事实摘要

- `contracts/runtime-program/current-program.json` 声明 `default_task_runtime_owner=one-person-lab`、`default_runtime_substrate=temporal`、`default_stage_executor=codex_cli`、`mag_implements_daemon=false`、`mag_implements_scheduler=false`、`mag_implements_attempt_loop=false`、`mag_owns_attempt_ledger=false`。
- `mag_functional_structure_gap_count=0` 表示 MAG repo 侧当前 surface 已收到 handler / refs-only / authority 边界；它不表示 OPL generated caller、真实 App/workbench 消费、全部 bridge exit 或 production long-run soak 已完成。
- `claims_opl_replacement_exists=false`、`claims_all_bridge_exits_complete=false`、`claims_production_long_run_soak_complete=false` 仍是当前机器面必须保留的限制。
- `contracts/external_evidence/mag-evidence-receipt-ledger.json` 已记录 first live production evidence refs；当前仍只保存 refs、receipt shapes、typed blocker / no-regression refs 和 production acceptance refs。Temporal long-soak window evidence 仍是后续证据门。
- Production acceptance tail 已由 MAG-owned owner receipt projection 关闭；这只证明 MAG owner receipt / typed blocker / no-regression evidence 的 refs-only closeout shape，不授权 OPL、Provider、Agent Lab 或 OMA 替 MAG 生成 grant-ready、fundability-ready、quality/export-ready 或 submission-ready verdict。

## 当前保留面

- `agent/` 是 Declarative Grant Pack：stage prompts、stage policies、skill declaration、quality gates 和 knowledge refs 是 OPL pack compiler / generated surfaces 的 repo-source 语义输入。
- `contracts/` 是机器合同、handoff、receipt、external evidence request、production acceptance 和 runtime-program 指针。
- `src/med_autogrant/**` 只作为 domain handler、refs-only adapter、minimal authority function、native helper、diagnostic、migration input 或 tombstone/provenance 支撑读取；不得写成 MAG 私有 runtime platform。
- MAG retained private authority surface 限定为 grant domain truth、fundability / quality / export verdict、package authority、grant strategy memory body 与 accept/reject、owner receipt、transition oracle、grant-native helper 和 focused contract tests。
- Product-entry、sidecar、grouped CLI/API、projection、lifecycle、memory/package projection 和 status/user-loop 仍可作为 direct domain handler 或 refs-only adapter 暂时存在；长期 owner 是 OPL generated/hosted surface，active 迁移顺序回到 active gap plan。

## 已退役面

Local runtime journal / attempt ledger、repo-owned scheduler daemon、upstream Hermes probe、flat shell alias、facade patch bridge、compat aggregate test、Gateway/local-manager default path 和旧 hosted/provider specs 只能作为 history、tombstone、explicit proof history 或 regression oracle 阅读。无 active caller 后直接删除或归档，不新增 compatibility alias、re-export facade 或 compatibility-only 聚合测试。

## 当前证据门

当前剩余工作不再写成 MAG repo 侧结构缺口，统一作为证据门管理：

- 真实 OPL-hosted grant-stage attempt 持续返回 MAG owner receipt、typed blocker 或 no-regression evidence。
- 真实 grant workspace 产生 accepted/rejected memory receipt、package/export lifecycle receipt、cleanup/restore/retention receipt 和 owner receipt scaleout。
- OPL/App shell 持续消费 MAG package refs、gap report、manual portal boundary、quality refs、transition oracle refs 和 safe action refs。
- External production/default caller、release/dist consumption、continuous no-forbidden-write 和 direct/hosted parity 产生连续证据。
- Temporal provider long SLO、repair cadence 和 live receipt reconciliation 产生连续证据。
- Physical morphology cleanup 在 active caller migration、direct/hosted parity、owner receipt roundtrip、continuous evidence 和 no-active compatibility alias scan 稳定后继续推进。

## 当前入口

- 用户路径：`Med Auto Grant app skill -> product status -> product user-loop -> workspace progress / workspace cockpit -> product direct-entry -> pass / package commands`。
- Pre-workspace：`discover-funding-opportunities -> select-project-profile -> initialize-intake-workspace`。
- Grant stage plane：`call_and_candidate_intake`、`fundability_strategy`、`specific_aims_and_structure`、`proposal_authoring`、`review_and_rebuttal`、`package_and_submit_ready`。
- Declarative Grant Pack：`agent/prompts/`、`agent/stages/`、`agent/skills/`、`agent/quality_gates/`、`agent/knowledge/`。
- Sidecar：`product sidecar export` / `dispatch` 只返回 refs、owner receipt、typed blocker、verdict refs 与 authority action metadata；它不是常驻 daemon。

## 当前不能声明

- 不能把 `mag_functional_structure_gap_count=0` 写成 external production/default caller、真实 App/workbench consumption 或 production long-run soak 已完成。
- 不能把 descriptor ready、transition oracle smoke、receipt reconciliation proof、external evidence consumption 或 no-regression evidence 写成 provider SLO / live soak 已完成。
- 不能把 OPL provider completion、matrix runner smoke、package existence、schema completeness、quality scorecard 分数或 controller route 写成 fundability-ready、quality-ready、export-ready 或 submission-ready verdict。
- 不能把 hand-written product-entry / sidecar / grouped CLI/API / projection / lifecycle wrapper 写成长期合理私有平台。
- 不能把 local journal、attempt ledger、Hermes probe、Gateway/local-manager、flat CLI alias、compatibility aggregate test 或 `codex_cli` executor 写回默认 runtime owner。

## 下一跳

- 目标态：[Med Auto Grant 理想目标态](./references/med-auto-grant-ideal-state.md)
- 差距与顺序：[MAG 理想目标态差距与完善计划](./active/mag-ideal-state-cross-repo-gap-plan.md)
- 文档治理：[MAG 文档组合治理](./docs_portfolio_consolidation.md)
- 过程归档：[MAG standard agent 文档过程归档 2026-05](./history/plans/mag-standard-agent-doc-process-history-2026-05.md)
