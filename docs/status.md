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

以下证据门单独统计，不能反向重开 MAG repo 侧 active bridge exit，也不能被结构通过替代：

- 真实 OPL-hosted grant-stage attempt 持续返回 MAG owner receipt、typed blocker 或 no-regression evidence。
- 真实 grant workspace 产生 accepted/rejected memory receipt、package/export lifecycle receipt、cleanup/restore/retention receipt 和 owner receipt scaleout。
- OPL/App shell 持续消费 MAG package refs、gap report、manual portal boundary、quality refs、transition oracle refs 和 safe action refs。
- External production/default caller、release/dist consumption、continuous no-forbidden-write 和 direct/hosted parity 的后续连续证据。
- Temporal provider long SLO、repair cadence 和 live receipt reconciliation 的后续连续证据。

这些证据门的 request id、required refs 和 receipt shape 由 `external_evidence_request_pack`、`contracts/external_evidence/mag-evidence-receipt-ledger.json`、production acceptance contract 和 product-entry manifest 持有。本页只保留状态边界，不复制证据流水。

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
