# 当前状态

Date: `2026-05-18`

## 当前角色

`Med Auto Grant` 是医学基金申请 domain agent，也是 OPL-compatible Foundry Agent package。Direct app skill / CLI / `MedAutoGrantDomainEntry` 仍是一等入口；OPL-hosted path 可以发现、托管、唤醒和投影 MAG，但必须回到同一套 MAG-owned grant truth、fundability / quality / export verdict、package authority、grant strategy memory accept/reject、owner receipt 和 typed blocker。

OPL Framework 持有通用 provider runtime、typed queue、attempt ledger、generic transition runner、workspace/source shell、memory locator、artifact/package lifecycle shell、operator projection、observability/SLO、generated wrapper 和 App/workbench shell。MAG 的 product-entry、sidecar、grouped CLI/API、projection builder、lifecycle adapter、local journal、attempt ledger、workspace/source intake 或 package/memory helper 只能作为迁移输入、domain handler target、refs-only adapter、authority function 或 history/tombstone，不是长期私有平台。

`Codex CLI` 是当前第一公民 executor。`Hermes-Agent`、Claude Code 等只允许作为显式 opt-in executor adapter / proof lane，通过 OPL receipt/audit/fail-closed 边界接入；不承诺行为、质量或 resume 语义等价。

## 当前运行与文档事实

- 单一 `Med Auto Grant` app skill、CLI、`MedAutoGrantDomainEntry`、product status/user-loop/direct-entry、workspace progress/cockpit、product sidecar export/dispatch 和 package submission-ready 是当前 direct path 与 domain handler surface。
- `contracts/runtime-program/current-program.json`、schemas、product-entry manifest、sidecar receipt、workspace/runtime artifact root、质量报告和导出包是机器真相；`docs/**` 只做解释、导航、治理和 provenance。
- MAG 已声明 domain descriptor、pack compiler input、generated surface handoff、family action catalog、family stage control plane、domain memory descriptor、artifact locator contract、owner receipt contract、functional privatization audit 和 private functional surface policy，可被 OPL 生成/读取 descriptor。
- Descriptor ready、receipt reconciliation proof、transition oracle smoke 或 no-regression evidence 只能说明可发现、可投影、可对账；不能写成生产默认 caller 已迁到 OPL generated/hosted surface，也不能写成 MAG 已是纯 knowledge pack。
- 过程性校准、follow-through、receipt proof 和 closeout 流水归档到 [MAG standard agent 文档过程归档 2026-05](./history/plans/mag-standard-agent-doc-process-history-2026-05.md)，不在本页展开。

## 当前结构收口状态

当前结构收口状态按 [MAG 理想目标态差距与完善计划](./active/mag-ideal-state-cross-repo-gap-plan.md) 维护：

`mag_functional_structure_gap_count=0`

MAG repo 侧 handler/ref-only 边界已收薄：product/status/user-loop/sidecar/grouped CLI/projection/lifecycle wrapper 的目标长期 owner 固定为 OPL generated/hosted surface；当前仍由 MAG CLI/product-status/sidecar 触达的 surface 只允许写成 direct domain handler、domain handler target、refs-only adapter、owner receipt、typed blocker、verdict refs、safe action metadata 或 minimal authority function。

机器面同步到 `mag_handler_boundary_ready_external_caller_evidence_gated` / `mag_handler_boundary_ready_external_evidence_gated`：`functional_privatization_audit`、`product-entry manifest`、`sidecar export`、`current-program` 和 `opl-family-contract-adoption` 均声明 `claims_opl_replacement_exists=false`、`claims_all_bridge_exits_complete=false`、`claims_production_long_run_soak_complete=false`。这表示 MAG repo 侧已把自身 surface 收到 handler/ref-only/authority 边界，不表示外部 production/default caller、真实 App/workbench 消费、全部 bridge exit 或长时 soak 已完成。

local runtime journal / attempt ledger、repo-owned scheduler daemon、upstream Hermes probe、flat shell alias、facade patch bridge 和 compat aggregate test 现在只允许作为 legacy proof / tombstone / regression oracle 存在；无 active caller 后直接删除或归档，不保留 compatibility alias。

MAG retained private surface 限定为 grant domain truth、fundability / quality / export verdict、package authority、grant strategy memory body 与 accept/reject、owner receipt、transition oracle、grant-native helper 和 focused contract tests。

## 当前测试/证据差距

以下证据门单独统计，不能反向重开 MAG repo 侧 active bridge exit：

- 真实 OPL-hosted grant-stage attempt 持续返回 MAG owner receipt、typed blocker 或 no-regression evidence。
- 真实 grant workspace 产生 accepted/rejected memory receipt、package/export lifecycle receipt、cleanup/restore/retention receipt 和 owner receipt scaleout。
- OPL/App shell 真实消费 MAG package refs、gap report、manual portal boundary、quality refs、transition oracle refs 和 safe action refs。
- external production/default caller、release/dist consumption、continuous no-forbidden-write 和 direct/hosted parity 证据。
- Temporal provider long SLO、repair cadence 和 live receipt reconciliation。

## 当前入口

- 用户路径：`Med Auto Grant app skill -> product status -> product user-loop -> workspace progress / workspace cockpit -> product direct-entry -> pass / package commands`。
- Pre-workspace：`discover-funding-opportunities -> select-project-profile -> initialize-intake-workspace`。
- Grant stage plane：`family_stage_control_plane` 暴露 `call_and_candidate_intake`、`fundability_strategy`、`specific_aims_and_structure`、`proposal_authoring`、`review_and_rebuttal`、`package_and_submit_ready`。
- 质量治理：`workspace quality-scorecard`、`workspace quality-closure-dossier`、`workspace quality-diff`；这些是 AI critique-backed aggregator，不是机械 ready verdict。
- Sidecar：`product sidecar export` / `dispatch` 只返回 refs、owner receipt、typed blocker、verdict refs 与 authority action metadata；不是常驻 daemon。

## 当前不能声明

- 不能把 `mag_functional_structure_gap_count=0` 写成 external production/default caller、真实 App/workbench consumption 或 production long-run soak 已完成。
- 不能把 `classification_gap_count=0`、descriptor ready、transition oracle smoke、receipt reconciliation proof 或 no-regression evidence 写成 provider SLO / live soak 已完成。
- 不能把 OPL provider completion、matrix runner smoke、package existence、schema completeness、quality scorecard 分数或 controller route 写成 fundability-ready、quality-ready、export-ready 或 submission-ready verdict。
- 不能把 hand-written product-entry / sidecar / grouped CLI/API / projection / lifecycle wrapper 写成长期合理私有平台。
- 不能把 local journal、attempt ledger、Hermes probe、Gateway/local-manager、flat CLI alias 或 compatibility aggregate test 写回默认 runtime owner。

## 目录与验证口径

- repo-tracked 主线不保留项目级 `.codex/`、`.omx/`、`.runtime-program/`、`.agent-contract-baseline.json` 或 `runtime-state/`；本机 session、prompt、log、report 与 hook 状态统一属于 `$CODEX_HOME/projects/med-autogrant/runtime-state/`。
- Python / pytest lane 必须通过 `scripts/run-python-clean.sh` 或 `scripts/run-pytest-clean.sh`，把 bytecode、pytest cache 和安装/同步副产物导向仓库外部。
- 测试口径只固定 machine-readable contract、schema、CLI/API、generated artifact 结构与污染 guard；`README*`、`docs/**` 和 skill 正文文案不作为稳定断言面。

## 下一跳

- 目标态：[Med Auto Grant 理想目标态](./references/med-auto-grant-ideal-state.md)
- 差距与顺序：[MAG 理想目标态差距与完善计划](./active/mag-ideal-state-cross-repo-gap-plan.md)
- 文档治理：[MAG 文档组合治理](./docs_portfolio_consolidation.md)
- 过程归档：[MAG standard agent 文档过程归档 2026-05](./history/plans/mag-standard-agent-doc-process-history-2026-05.md)
