# 决策记录

Owner: `Med Auto Grant`
Purpose: `current_decision_log`
State: `current`
Machine boundary: 本文是人读决策记录。机器真相继续归 contracts、schemas、source、CLI/API 行为、product-entry manifest、runtime receipts 与 workspace/artifact outputs；历史决策若与当前 status/current-program 冲突，以当前 owner surfaces 为准。
Date: `2026-05-22`

## 读法

本文只保留当前仍有效、会影响后续维护判断的决策。2026-05 的 consumer thinning、receipt proof、external evidence closeout、physical cleanup、stale worktree closeout 等过程性增量，统一回到 [MAG standard agent 文档过程归档 2026-05](./history/plans/mag-standard-agent-doc-process-history-2026-05.md)。当前差距和执行顺序回到 [MAG 理想目标态差距与完善计划](./active/mag-ideal-state-cross-repo-gap-plan.md)。

## 当前有效决策

### OPL/Temporal 是默认任务运行 owner，MAG 保留 grant authority

- 决策：任务启动后的默认运行 owner 是 OPL/Temporal hosted autonomous runtime；MAG 不实现 daemon、scheduler、attempt loop 或 attempt ledger；`Codex CLI` 是默认 stage executor。
- 理由：标准 OPL Agent 应提交 declarative pack、domain handler、refs、typed blocker、owner receipt 和 grant authority surface。持久在线调度、唤醒、retry、resume、attempt ledger 和 long-running provider residency 是 OPL/Temporal 职责。
- 影响：Direct app skill / CLI / `MedAutoGrantDomainEntry` 仍是一等入口；MAG 继续持有 grant truth、fundability / quality / export verdict、package authority、memory accept/reject 和 owner receipt authority。该决策不声明 Temporal long-soak window evidence 已关闭。

### MAG 目标形态是 Declarative Grant Pack + OPL generated/hosted surfaces + minimal authority functions

- 决策：MAG 以 `agent/` declarative pack、contracts、domain handler、refs-only adapter 和最小 authority function 作为长期形态；product-entry、sidecar、grouped CLI/API、projection builder、lifecycle adapter、memory/package helper、workspace/source intake 和 status/user-loop wrapper 只能作为 direct handler、refs-only adapter、migration input、diagnostic 或 tombstone 阅读。
- 理由：通用 runtime、queue、attempt ledger、workspace/source shell、memory locator、artifact/package lifecycle、operator workbench、observability/SLO、generated wrapper 和 App/workbench shell 归 OPL Framework / shared family layer；MAG 的核心价值在 grant-specific judgment 和交付 authority。
- 影响：旧 module/interface/test/docs entry 若只服务 local runtime、Hermes/Gateway/local-manager、patch bridge、flat alias 或 compatibility aggregate test，active caller 迁出后直接退役或归档，不新增 compatibility shim、re-export facade 或 compatibility-only test。

### AI-first authority surface 不由程序机械生成 ready verdict

- 决策：fundability、quality、export、memory accept/reject 是 AI-first judgment surface；package authority、owner receipt 和 grant helper 是 programmatic guard surface。程序只能验证、物化 refs、签 receipt、返回 typed blocker 或 safe action metadata。
- 理由：schema completeness、scorecard 分数、package existence、provider completion 或 controller route 都不能替代 grant reviewer / authoring executor / MAG owner 的判断。
- 影响：缺少 AI-authored artifact、independent review receipt、owner receipt 或等价 owner-backed export artifact 时，fundability-ready、quality-ready、export-ready 和 submission-ready 都必须 fail-closed。

### External evidence ledger 是 refs-only consumption surface，不是 production completion claim

- 决策：external evidence request pack 和 `contracts/external_evidence/mag-evidence-receipt-ledger.json` 只记录外部 caller/App/workbench/owner receipt roundtrip/no-forbidden-write/direct-hosted parity/Temporal reconciliation 的 refs、receipt shapes、typed blocker 和 no-regression evidence。
- 理由：MAG 可以消费外部证据 refs，但不能在仓内伪造 OPL generated caller、Codex App workbench、production/default caller、continuous guard 或 Temporal long-soak 成功。
- 影响：first live production evidence refs 可消费不等于真实 grant workspace 扩面、App 用户路径、Temporal long soak、grant-ready、fundability-ready、quality/export-ready 或 submission-ready 完成。

### Domain memory 只由 MAG 决定 body 与 accept/reject

- 决策：OPL 可以索引 memory refs、携带 consumed refs、显示 provenance 和路由 writeback receipts；MAG 持有 grant strategy memory body、accept/reject authority、fundability/quality 影响判断和 owner receipt。
- 理由：grant strategy memory 是辅助 Codex stage reasoning 的自然语言经验，不是跨 funder recipe engine 或 quality/export verdict generator。
- 影响：真实 memory store、receipt instance 和 workspace artifact 只进入 workspace/runtime artifact root 或 `$CODEX_HOME/projects/med-autogrant/runtime-state/`；repo source 只保存 descriptor、schema、locator、fixture 模板和 proof surface。

### Submission-ready package 是本地交付 gate，不等于官网提交或正文质量完成

- 决策：`package submission-ready` 保留为严格 fail-closed 的本地 package/export surface；authoring 主任务完成语义仍以正文科学性、authoring quality 和 owner-backed export verdict 为准。
- 理由：材料完整性、导出包存在和 portal checklist 状态不能替代正文科学闭合、review/revision closure 或申请人侧质量判断。
- 影响：外部官网提交、人工 portal gate、形式补件和客观材料补齐继续独立表达；缺少 MAG owner 或 AI-backed export verdict 时，submission-ready 必须 fail-closed。

### 文档生命周期按 owner surface 分层，不保留旧 specs 兼容层

- 决策：核心五件套承载 current 人读 truth；`docs/active/` 承载当前 gap / 完善计划；`docs/specs/` 只保留 active specs、support current-truth records 和 integration references；纯历史 activation package、provider proof、local-runtime closeout、future-P5 和 superseded hosted/handoff specs 进入 `docs/history/`。
- 理由：dated spec 标题里的 `Current Truth` 容易被 direct-file reader 误读为当前完整产品状态；生命周期必须由 owner/purpose/state/machine boundary 和 specs lifecycle map 约束。
- 影响：旧 OPL Runtime Manager、Hermes-first、Gateway/federation、local journal、attempt ledger、patch bridge、compatibility alias 或 legacy hosted wording 只能作为 provenance 读，不再定义当前目标、默认 runtime owner 或兼容保留理由。

## Superseded 决策入口

以下旧决策只作为历史背景，不再承担 current owner：

- 旧 OPL Runtime Manager 薄管理层口径：已被 OPL stage-led framework + Temporal default runtime owner 取代。
- Hermes-first sidecar adapter：已被 Temporal-backed OPL hosted autonomy 和显式 executor adapter/proof lane 口径取代。
- local runtime / journal / attempt ledger closeout：已归入 history/provenance；当前测试明确拒绝 `runtime-run`、`runtime-resume` 和 `probe-upstream-hermes`。
- 旧 domain runtime facade patch bridge、flat alias、compat aggregate test：active caller 迁出后直接退役，当前不保留 compatibility surface。
- 2026-05 的 step-by-step receipt/proof/lane closeout：统一从 history 归档读取，不作为当前状态页或决策页的增量 ledger。
