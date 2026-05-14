# MAG 理想目标态差距与完善计划

Owner: `Med Auto Grant`
Purpose: 对照 MAG 理想目标态和 OPL family 各仓当前实际状态，记录差距、OPL Framework 应上收的通用能力，以及 MAG production closure 的分阶段完善计划。
State: `active_plan`
Machine boundary: 本文是人读 gap / completion plan，不是机器真相。机器可读真相继续归 `contracts/`、`schemas/`、源码、CLI/API 行为、OPL runtime ledger、domain-owned manifest、workspace/runtime artifact root、receipt、质量报告和导出包。
Date: `2026-05-14`

## 结论

MAG 的理想目标态已经很清晰：MAG 是医学基金申请 domain agent，持有 grant truth、fundability、specific aims、authoring quality、grant strategy memory body/accept-reject、submission-ready package 与 export authority；OPL Framework 提供长期在线、stage attempt、queue/wakeup、human gate、receipt、retry/dead-letter、operator projection、workspace/artifact lifecycle、shared contracts 和 provider-backed runtime。

当前 MAG 已完成 direct app skill / CLI / `MedAutoGrantDomainEntry` / product-entry / sidecar / 6-stage control plane / domain memory descriptor / owner receipt contract / lifecycle guarded apply / standard skeleton descriptor 等基础面。OPL family 当前也已经能把 MAS/MAG/RCA 三仓识别为 descriptor-level aligned 的 standard domain agents，三仓 stage plane 与 memory descriptor 均 resolved，Temporal provider residency proof 已通过，OPL functional closeout 已进入 `functional_closure_ready_for_live_soak`。

主要差距已经不在概念、命名或 descriptor，而在 production closure：

- MAG 还没有真实 OPL-hosted grant-stage attempt 产出的 MAG domain owner receipt、typed blocker 或 no-regression evidence。
- Grant strategy memory 仍主要停在 descriptor / locator / receipt-evidence contract 层；真实 memory body / writeback apply 的 workspace-runtime 泛化还没有闭合。
- Package/export、artifact lifecycle、restore/retention、operator drilldown、route/decision graph 和 quality/readiness projection 需要由 OPL Framework / App 提供通用壳，MAG 只回传 authority refs、gap report、receipt 和 verdict。
- 物理 skeleton 迁移和旧 Hermes/Gateway/local-manager active-path 物理删除仍需 direct skill path、OPL-hosted path、restore/provenance proof、no-forbidden-write proof 与 no-active-caller proof 稳定后推进。

这份计划的核心判断是：MAG 后续不应继续在仓内重复建设通用运行外围；应把可复用的 transport、lifecycle、projection、operator workbench 能力上收到 OPL Framework，MAG 仓保持 grant-domain authority pack 和薄 adapter。

## Fresh Evidence 2026-05-14

本计划基于本轮只读检查和各仓当前文档/机器面：

| surface | fresh result | 读法 |
| --- | --- | --- |
| `med-autogrant git status --short --branch` | `main...origin/main [ahead 1]`，本轮写文档前无未提交改动 | 本计划可以安全落在 MAG 仓；不混入其他仓未提交变更。 |
| `one-person-lab git status --short --branch` | `main...origin/main [ahead 1]`，存在多处未提交文档/源码改动 | OPL 现状作为 fresh local read 使用；不把未提交状态写成远端发布事实。 |
| `med-autoscience git status --short --branch` | `main...origin/main [ahead 1]`，存在多处未提交文档/源码改动 | MAS 现状作为 sibling input 使用；本计划不修改 MAS。 |
| `redcube-ai git status --short --branch` | `main...origin/main [ahead 1]`，未显示未提交改动 | RCA 现状可作为相对稳定 sibling input。 |
| OPL `agents list --json` | `aligned_count=3`、`missing_count=0`、`drift_detected_count=0`、`physical_skeleton_evidence_observed_count=3`、`physical_skeleton_audit_pending_count=0`、`production_closure_gap_count=12`、`provider_temporal_residency_gap_status=closed_by_fresh_proven_proof` | MAS/MAG/RCA descriptor 与 repo-source anchors 已被 OPL 读模型识别；production closure gap 仍存在。 |
| OPL `stages list --json` | `resolved_planes_count=3`、`stages_count=18` | 三仓各 6 个 stage plane 已可被 OPL 解析。 |
| OPL `domain-memory list --json` | `resolved_memory_descriptor_count=3`、`missing_memory_descriptor_count=0` | 三仓 memory descriptor 已 resolved；OPL 仍只做 descriptor/receipt-locator projection，不写 memory body。 |
| OPL `framework production-closeout --json` | `status=functional_closure_ready_for_live_soak`、`provider_ready=true`、`typed_blocker_count=0`、`live_soak_excluded=true`，runtime ledger queue `total=7/succeeded=7`，stage attempts `total=4/completed=4` | 排除真实长时 soak 后，OPL functional closeout 已无当前 typed blocker；这不等于 MAG grant-stage owner chain 已闭合。 |
| OPL stage attempt evidence | MAG 有 1 条 completed closeout packet，但 `owner_receipt_refs=[]`、`no_regression_evidence_refs=[]`，controlled apply 为 `no_controlled_apply_request` | OPL 已能接收 MAG sidecar attempt 证据；还没有 MAG owner receipt / no-regression 级别的 grant-stage completion evidence。 |

当前状态和目标态的权威入口仍是：

- [MAG 理想目标态](../references/med-auto-grant-ideal-state.zh-CN.md)
- [MAG 当前状态](../status.md)
- [MAG 架构](../architecture.md)
- [MAG 不变量](../invariants.md)
- [MAG 决策记录](../decisions.md)
- [`current-program.json`](../../contracts/runtime-program/current-program.json)

## MAG 理想目标态的 owner 边界

MAG 理想态可以压缩成两条边界。

MAG 必须继续持有：

- funding call / funder family / applicant profile 的解释与任务锁定；
- fundability strategy、specific aims、claim-evidence structure 和 reviewer risk；
- proposal authoring、AI-first critique、revision、quality closure 和 issue lineage；
- grant strategy memory 的正文、检索语义、writeback proposal、accept/reject decision 和 receipt；
- local submission-ready package gate、gap report、export verdict 和 package refs；
- domain owner receipt、typed blocker、no-regression evidence 的 domain meaning；
- direct app skill path 与 OPL-hosted path 共享的 route truth、workspace truth、quality gate 和 export gate。

OPL Framework / One Person Lab App 应提供：

- provider-backed runtime、stage attempt ledger、queue、heartbeat、resume、human gate 和 retry/dead-letter；
- workspace/source intake shell、artifact locator、package/export lifecycle shell、restore/retention 和 migration ledger；
- domain memory locator/index、receipt ref projection、freshness、operator grouping 和 writeback transport 壳；
- route/decision graph、quality/readiness projection shell、attention queue、operator drilldown、repair command projection 和 observability/SLO；
- source fingerprint、idempotency、no-forbidden-write proof、receipt audit 和 provider proof ledger；
- App/workbench 的通用展示与 action routing。

这个 owner split 意味着：MAG 后续新增能力时，凡是 grant 专业判断、正文生成、质量 verdict、memory accept/reject 或 export authority，都留在 MAG；凡是跨 MAS/MAG/RCA 可复用的运行外围、receipt transport、lifecycle、workbench、SLO 和 ref-only projection，都优先上收到 OPL。

## 总体差距矩阵

| 维度 | 理想情况 | 当前实际 | 差距 | 完善方向 |
| --- | --- | --- | --- | --- |
| MAG direct path | 单一 app skill / CLI / domain entry 能独立完成 grant authoring、review、package 和 owner receipt | direct capability surface 已落地，product status / user-loop / direct-entry / package submission-ready / quality surfaces 可调用 | 真实 end-to-end grant workspace 的长期 owner receipt、memory writeback 和 package lifecycle proof 不足 | 选一条真实 grant workspace 跑完整 stage closeout，留下 owner receipt、quality closure、package refs 和 no-forbidden-write proof |
| OPL-hosted MAG path | OPL 托管 stage attempt，MAG 返回 domain receipt、typed blocker 或 no-regression evidence | OPL 可解析 MAG descriptor/stages/memory，已有 1 条 completed MAG sidecar attempt closeout packet | closeout packet 未包含 MAG owner receipt 或 no-regression evidence，不能声明 grant-stage production closure | 建立真实 OPL-hosted controlled grant-stage attempt，并要求 MAG sidecar/direct entry 返回 owner receipt / typed blocker / no-regression evidence |
| Stage-led grant control plane | 6 个 grant stage 具备输入、prompt/skill、knowledge、quality gate、handoff、closeout | OPL `stages list` 可解析 MAG 6-stage plane | stage plane 仍偏 descriptor/projection；真实 provider-hosted stage activity 证据不足 | 对 `fundability_strategy`、`proposal_authoring`、`review_and_rebuttal`、`package_and_submit_ready` 优先跑 controlled attempts |
| Grant strategy memory | stage 检索少量 memory refs，closeout 生成 proposal，MAG owner accept/reject 并写 receipt | OPL memory descriptor resolved；MAG 已有 descriptor、proposal、accept/reject、runtime receipt evidence writer | retrieval/writeback apply、memory body migration 和真实 workspace receipts 未形成长线闭环 | 把真实 memory body 保持在 workspace/runtime root；OPL 只上收 locator/index/receipt projection 和 freshness |
| Package/export lifecycle | MAG 持 export gate，OPL/App 展示 package refs、gap report、restore/provenance 和 manual portal boundary | `package submission-ready` 是 MAG-owned export gate；OPL 只读 package/export refs 的通用壳还不完整 | App/workbench 无通用 package/export lifecycle shell，容易把 provider completion误读成 export ready | OPL 提供 package/export shell；MAG 返回 submission-ready verdict、gap report 和 owner receipt |
| Artifact lifecycle | OPL 管 locator/retention/restore ledger，domain artifact mutation 需 MAG receipt | MAG 已有 lifecycle guarded apply proof；OPL closeout 能读 lifecycle refs | cleanup/restore/retention 的真实 workspace receipt proof 不足 | 在真实 grant workspace 上跑 cleanup/restore/retention guarded apply receipt |
| Quality/readiness projection | App 展示 quality state、issue lineage、closure dossier、next action，但不替 MAG 下 verdict | MAG quality scorecard / closure dossier / diff 已落地 | 通用 quality/readiness drilldown 与 operator action shell 仍需 OPL/App 上收 | OPL 提供 projection shell；MAG 返回 AI critique-backed verdict、issue refs 和 hard blockers |
| Physical skeleton | repo-source 按 `agent/ contracts/ runtime/ docs/` 清晰分层，workspace artifacts 不进 source | MAG 已有 minimum repo-source anchors，OPL 读模型识别为 evidence observed | 更大范围物理迁移仍需 path compatibility、direct/hosted parity、restore/provenance proof | 等 owner receipt 和 no-forbidden-write 证据稳定后逐步迁移，不做破坏性大搬家 |
| Legacy retirement | 旧 Hermes/Gateway/local-manager active path 只保留 history/proof/provenance | MAG status 已记录 tombstone / physically removed evidence | 旧命名和 legacy manager 入口的最终物理删除仍要 no-active-caller proof | 完成 replacement parity 后删除或归档，避免恢复第二套 active path |

## OPL Framework 应上收的 MAG 通用外围

下面这些能力来自 MAG 理想态，但不应长期由 MAG 独自维护。它们的抽象对 MAS/RCA 也成立，应该成为 OPL Framework / App 的 family primitives。

| 应上收能力 | OPL owner surface | MAG 保留内容 | 验收信号 |
| --- | --- | --- | --- |
| Workspace/source intake shell | workspace locator、source receipt、profile/call material intake、freshness、repair command | funding call 解释、profile selection、task lock、funder fit | 同一 intake shell 可服务 MAS study、MAG grant、RCA visual source；domain 返回 selected target 和 domain receipt |
| TODO / human gate / wakeup transport | typed queue、human gate token、resume signal、attention queue、dead-letter | 哪些问题构成 grant blocker，哪些只是 objective TODO | OPL action 只路由；MAG 决定 blocker severity 和 authoring impact |
| Grant strategy memory locator/index | memory descriptor、locator、body-free inventory、freshness、operator grouping | memory body、retrieval semantics、writeback proposal、accept/reject | OPL 不显示 memory body、不接收 writeback，只显示 refs/receipts |
| Memory writeback transport | proposal refs、receipt refs、accepted/rejected projection、SLO | 是否接受写回、写回正文、fundability/quality 影响 | MAG workspace/runtime root 有 accepted/rejected receipt；OPL 只读 receipt ref |
| Artifact/package lifecycle shell | artifact locator、package refs、gap report slot、restore/retention ledger、manual portal boundary | submission-ready verdict、export gate、grant package authority | App 显示 refs/gaps/provenance，但不推断 export readiness |
| Route/decision graph | stage route graph renderer、decision history view、handoff graph | fundability decision、aims strategy、revision rationale | OPL 画图，MAG 输出 route nodes/edges/rationale refs |
| Quality/readiness projection shell | quality panel、issue lineage viewer、closure dossier locator、attention item | AI critique、authoring quality verdict、hard blocker verdict | 无 active AI critique 时 App 只能显示 projection-only |
| Operator observability/SLO | provider proof freshness、attempt age、receipt latency、repair actions | domain success/failure meaning | provider ready 不等于 MAG ready；所有状态轴分开显示 |
| No-forbidden-write / idempotency | source fingerprint、attempt idempotency、forbidden write audit、receipt ledger | workspace mutation permission、artifact write authority | OPL 能证明自己未写 grant truth/artifact/memory body |

这组上收不改变 authority：OPL 提供壳、transport、ledger、projection 和 UI；MAG 继续持有 domain truth、quality/export verdict 和 artifact/memory authority。

## 各仓当前实际状态对 MAG 的影响

### MAG

MAG 当前是 Grant Foundry 的 active domain agent。已成立的部分包括：

- 单一 app skill、CLI、`MedAutoGrantDomainEntry` 和 schema-backed contract；
- 6-stage grant control plane、family action catalog、runtime control/continuity；
- product sidecar export/dispatch、OPL stage runtime registration、standard skeleton descriptor；
- owner receipt contract、controlled domain-memory receipt evidence writer、lifecycle guarded apply proof；
- physical skeleton minimum anchors 和 no-forbidden-write projection。

MAG 当前不能声明：

- OPL-hosted grant-stage production soak 已完成；
- MAG grant-stage owner receipt chain 已闭合；
- grant strategy memory body/writeback apply 已在真实 workspace/runtime root 泛化完成；
- package/export lifecycle shell 已由 OPL/App 产品化；
- legacy active-path residue 已全部物理删除。

### OPL

OPL 当前已经从“descriptor / projection only”推进到更完整的 framework closeout read model：Temporal provider readiness、provider continuous proof、stage attempt ledger、runtime snapshot、domain descriptor aggregation、production closeout gate 都已可读。对 MAG 来说，这证明 OPL 具备托管 MAG 的框架前提，但仍不能替 MAG 产出 grant truth 或 quality/export verdict。

MAG 对 OPL 的依赖重点应转为：

- 真实 OPL-hosted grant-stage attempt 的 attempt/receipt 生命周期；
- generic workspace/source intake、memory locator、artifact/package lifecycle、quality/readiness shell 和 App drilldown；
- provider proof cadence、operator SLO 和 repair command projection；
- no-forbidden-write 和 direct/hosted parity 证据。

### MAS

MAS 当前提供了最接近 production owner-chain 的 sibling 样板：它已经有真实 paper-line proof surface、publication-route memory policy、stage knowledge packet、typed closeout routing、provider proof ingestion 和 body-free inventory/grouping/read-model。但 MAS 仍未声明 production-hosted paper automation 闭合，真实 owner apply receipt chain、human gate/resume、更多 memory receipts 和 legacy cleanup 仍在 production evidence gate。

对 MAG 的启发是：

- MAG 的 grant strategy memory 应采用类似 MAS publication-route memory 的 body-free inventory / receipt projection / owner accept-reject 边界；
- 真实 workspace owner receipt 比 descriptor 更重要，MAG 的下一步也应选真实 grant line 跑 owner receipt；
- human gate、route decision、artifact mutation 必须回到 domain owner，不由 OPL provider completion 推断。

### RCA

RCA 当前提供了 artifact-heavy domain 的 sibling 样板：direct route 已 landed，OPL-hosted route 是 contract/projection landed；image-first/default visual route、artifact locator、controlled memory apply proof、lifecycle guarded apply proof 和 visual no-regression evidence refs 都已形成。它仍缺 visual-stage long soak、artifact-producing owner receipt 和真实 visual memory body writeback。

对 MAG 的启发是：

- package/export lifecycle shell 应按 RCA artifact gallery/handoff 思路上收到 OPL/App，MAG 只返回 export refs、gap report 和 verdict；
- no-regression evidence 可以先作为 controlled attempt 的有效收口形态，但不能替代 domain owner receipt；
- artifact blob / export package / receipt instance 不进入 repo source 的边界必须持续保持。

## 分阶段完善计划

### P0：冻结 MAG 侧 gap plan 与 owner 边界

目标：让 MAG 后续 work 不再散落在对话或相邻仓 dirty docs 中。

动作：

1. 保持本文为 MAG active plan，核心 current truth 继续归 `docs/status.md`、核心五件套和 `current-program.json`。
2. 在后续 MAG work 中优先引用 `docs/references/med-auto-grant-ideal-state.zh-CN.md` 和本文，区分 north-star、current truth 和 active plan。
3. 不在 MAG 文档中把 OPL provider readiness、descriptor aligned 或 closeout packet 写成 grant-stage owner receipt 完成。

验收：

- `docs/plans/README*` 和 docs portfolio 能定位本文；
- `scripts/verify.sh meta` 通过；
- diff 只包含 MAG 文档与文档索引。

### P1：真实 OPL-hosted MAG grant-stage attempt

目标：把 OPL 能托管 MAG 从 descriptor/sidecar closeout 推进到 domain owner receipt / typed blocker / no-regression evidence。

动作：

1. 选一个低风险 grant workspace 或 fixture-backed workspace，优先覆盖 `fundability_strategy` 或 `review_and_rebuttal`。
2. 通过 OPL task-bound provider-backed attempt 触发 MAG sidecar / direct entry。
3. MAG 返回三种之一：`domain_receipt`、`typed_blocker`、`no_regression_evidence`。
4. OPL runtime ledger 与 MAG workspace/runtime root 都能定位同一 receipt ref。
5. 明确证明 OPL 没有写 grant truth、memory body、quality verdict 或 export package。

验收：

- OPL closeout 中 MAG domain breakdown 出现 owner receipt ref、typed blocker 或 no-regression evidence ref；
- MAG workspace/runtime root 有对应 receipt evidence；
- provider completion 和 MAG ready verdict 在 projection 中保持分轴显示。

### P2：OPL generic primitive absorption

目标：把 MAG 理想态中通用外围能力上收到 OPL，而不是继续堆在 MAG 仓。

动作：

1. OPL 定义 workspace/source intake shell，MAG 只提供 funding call/profile/task-lock adapter。
2. OPL 定义 memory locator/index/writeback transport，MAG 只提供 grant strategy memory policy、proposal、accept/reject 和 receipt writer。
3. OPL 定义 package/export lifecycle shell，MAG 只提供 package refs、gap report、submission-ready verdict 和 external portal/manual boundary。
4. OPL/App 定义 route/decision graph、quality/readiness panel、attention queue、repair commands 和 observability/SLO。
5. 所有 generic primitive 都要求 authority boundary 字段：`opl_can_write_domain_truth=false`、`opl_can_write_memory_body=false`、`opl_can_declare_export_ready=false`。

验收：

- 同一 OPL primitive 至少能消费 MAS/MAG/RCA 两个以上 domain 的 refs；
- MAG manifest/sidecar 只输出 refs、receipt、typed blocker、verdict refs，不复制 OPL runtime 逻辑；
- App/workbench 展示 owner、freshness、next action 和 repair command，但不越权下 verdict。

### P3：Grant strategy memory live apply

目标：让 grant strategy memory 从 descriptor-ready 推进到真实 workspace/runtime writeback 闭环。

动作：

1. 对真实 grant stage closeout 生成 writeback proposal。
2. MAG owner accept/reject，并写入 runtime receipt evidence。
3. memory body 仅写入 MAG workspace/runtime memory pack，不进入 repo source 或 OPL state。
4. OPL/App 只显示 consumed refs、proposal refs、accept/reject receipt refs、freshness 和 operator grouping。

验收：

- 至少一条 accepted 与一条 rejected receipt 可由 MAG CLI/API 读取；
- OPL `domain-memory` read model 继续显示 descriptor/receipt-locator，不显示 memory body；
- quality/export verdict 不由 memory receipt 自动产生。

### P4：Package/export 与 lifecycle 生产化

目标：把 MAG submission-ready package 从独立导出命令推进到 OPL/App 可展示、可恢复、可审计的 lifecycle。

动作：

1. MAG 继续持有 `package submission-ready` fail-closed gate。
2. OPL/App 提供 package refs、gap report、restore/provenance、retention、external portal/manual submission boundary 的通用 shell。
3. cleanup/restore/retention guarded apply 在真实 grant workspace 上产出 MAG lifecycle receipt。
4. App action routing 明确指向 OPL ledger 操作、MAG package command 或人工 portal step。

验收：

- App/workbench 可以看到 package state、gap report、owner、freshness、manual portal boundary；
- OPL 只能管理 locator/ledger，不能删除或改写 MAG artifact；
- MAG lifecycle receipt 是 artifact mutation 的唯一授权来源。

### P5：Physical skeleton follow-through 与 legacy retirement

目标：在 direct/hosted parity 稳定后做物理目录迁移和旧面删除。

动作：

1. 对 `agent/ contracts/ runtime/ docs/` 做 path compatibility audit。
2. 验证 direct app skill path、MAG CLI、OPL-hosted path、restore/provenance proof 和 focused tests。
3. 将旧 Hermes/Gateway/local-manager 命名按 no-active-caller proof 删除或迁入 history/tombstone。
4. 保留必要 provenance，但不让旧名重新取得 default runtime 或 public integration authority。

验收：

- OPL `agents list` 继续 `aligned_count=3`、MAG descriptor 无 drift；
- MAG repo 不跟踪真实 workspace artifacts、receipt instances、memory body 或 export packages；
- legacy active-path scan 不再发现默认 caller。

## 当前不做的事

- 不把 MAG 改成 OPL 内部模块。
- 不把 OPL provider completion 写成 MAG fundability-ready、quality-ready 或 export-ready。
- 不把 grant strategy memory body、private evidence、receipt instance 或 export package 放进 repo source。
- 不在 MAG 仓内实现 generic provider runtime、generic executor registry 或 App workbench。
- 不用非默认 executor 的 proof 替代 Codex CLI 默认执行语义。
- 不在缺少 owner receipt / no-regression evidence 的情况下声称 production long-run soak 完成。

## 下一步推荐顺序

1. 在 MAG 选定一个低风险 grant-stage controlled attempt，目标是产出 owner receipt、typed blocker 或 no-regression evidence。
2. 与 OPL 对齐 generic primitive absorption 的最小切片：memory locator/writeback transport、package/export lifecycle shell 和 quality/readiness projection shell。
3. 用真实 workspace 跑 grant strategy memory accepted/rejected receipts。
4. 用真实 workspace 跑 package/export lifecycle 与 cleanup/restore/retention guarded receipts。
5. 等 direct/hosted parity 和 no-forbidden-write proof 稳定后，推进 physical skeleton migration 和 legacy physical retirement。

完成上述步骤后，MAG 才能从 “OPL-compatible descriptor / functional closure ready” 进入更接近 “production-hosted grant agent” 的状态。
