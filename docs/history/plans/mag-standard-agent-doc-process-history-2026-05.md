# MAG standard agent 文档过程归档 2026-05

Owner: `Med Auto Grant`
Purpose: 保存 2026-05 MAG 向标准 OPL Agent 收敛过程中的文档校准、receipt proof、consumer thinning 和 physical cleanup 摘要，避免主文档被历史演变污染。
State: `history_provenance`
Machine boundary: 本文是人读过程归档，不是 current truth、active plan、runtime contract 或机器接口。当前事实回到核心五件套、`docs/active/mag-ideal-state-cross-repo-gap-plan.md`、contracts、source、CLI/API、product-entry manifest 和 runtime receipts。

## 读取规则

- 本文只解释过程，不决定当前架构或完成状态。
- 当前目标态读 `docs/references/med-auto-grant-ideal-state.md`。
- 当前差距和完善顺序读 `docs/active/mag-ideal-state-cross-repo-gap-plan.md`。
- 如果本文与 current owner 文档冲突，以 current owner 文档和机器面为准。

## 过程摘要

2026-05 中旬，MAG 文档和机器面完成了几类收敛：

- 从“拥有自己的 product/status/user-loop/sidecar/grouped CLI/projection/lifecycle shell”校准为 OPL standard agent consumer。
- `mag_consumer_thinning_contract` 将 MAG adapter 角色收窄为 grant authority pack + thin program surface，只输出 grant-owned refs、owner receipt、typed blocker、verdict refs 和 domain action metadata。
- `privatized_functional_module_audit` 将非知识功能面拆成 declarative pack surface、refs-only adapter、minimal authority function 和 legacy proof tombstone。
- retained private authority functions 后续补齐了 AI-first guard、allowed return shapes 和 forbidden output boundary，用机器面固定 fundability、quality、export、package、memory、owner receipt 与 grant helper 不能由 provider completion、package existence、schema completeness 或 scorecard 分数机械生成 ready verdict。
- `grant_transition_oracle`、receipt reconciliation proof、lifecycle receipt bundle、memory receipt projection、package lifecycle handoff 和 continuous receipt reconciliation 成为 MAG-to-OPL handoff 输入，而不是 production soak success。
- `external_evidence_request_pack` 后续把 OPL generated/hosted caller、Codex App workbench、production/default caller、owner receipt / typed blocker roundtrip、no-forbidden-write、direct/hosted parity 和 Temporal long-soak receipt reconciliation 统一收成 request surface，仍不声明外部证据已收到。
- local runtime journal、attempt ledger、upstream Hermes probe、flat shell alias、facade patch bridge 和 compatibility aggregate test 被降为 cleanup / tombstone / provenance 对象。

## 主文档已迁出的内容类型

以下内容不再放在 MAG ideal/gap/status 主文档中展开：

- 具体日期的 consumer/thinning lane closeout。
- 单次 sidecar export、receipt reconciliation、hosted receipt verification 和 lifecycle receipt proof 命令摘要。
- OPL surface follow-up、functional harness consumer coverage、observability projection 和 conflict envelope 的落地流水。
- physical thinning follow-through 的命令级细节。
- provider / Hermes / Gateway / local-manager 迁移背景的长叙事。

## 当前分工

- `docs/status.md`：当前角色、当前边界、当前 gap 摘要和不能声明的内容。
- `docs/references/med-auto-grant-ideal-state.md`：north-star 目标态和长期 owner boundary。
- `docs/active/mag-ideal-state-cross-repo-gap-plan.md`：当前功能/结构差距、测试/证据差距和完善顺序。
- `docs/docs_portfolio_consolidation.md`：文档生命周期治理。

## 2026-05-22 refs-only ledger 过程记录

MAG grant-stage dispatch tranche 新增 9 条经 OPL safe-action shell 记录并验证的 refs-only receipt：

- `specific_aims_and_structure` attempt `sat_4d81d410694b72fd97413a5b`、`review_and_rebuttal` attempt `sat_4e8877fe031fc912ff53c7a6`、`proposal_authoring` attempt `sat_b0cac25e42955a654147ec00`、`fundability_strategy` attempt `sat_3bc99d526fb23328fdc0377d` 和 `call_and_candidate_intake` attempt `sat_e5d434a883472362dcef5ac3` 消费 MAG owner receipt / owner-chain refs。
- `package_and_submit_ready` lifecycle retention attempt `sat_1e31d809637014a83f8e907c`、restore attempt `sat_dbe416fbd54233172404013c` 与 cleanup attempt `sat_d4d4b1750726a95fae5c77a7` 消费 MAG-owned typed blocker。
- 遗留 `review_and_rebuttal` guarded-run attempt `sat_3c210fbc86393af8d3a0e90c` 消费 MAG-owned runtime-only typed blocker receipt `/Users/gaofeng/.codex/projects/med-autogrant/runtime-state/receipts/owner-receipts/sat_3c210fbc86393af8d3a0e90c-legacy-guarded-run-retired.json`，明确旧 `autonomy-controller/guarded-run` sidecar dispatch 已退役并 route back 到当前 MAG-owned direct / OPL-hosted stage owner surface。
- fresh OPL worklist 中 MAG domain-dispatch group 当前为空。

该 tranche 只把真实 MAG refs / typed blocker 接入 OPL external evidence ledger，不授权 OPL 写 grant truth、memory body、artifact body、quality/export verdict，也不声明 submission-ready、production-ready 或 Temporal long-soak complete。

## 历史不能构成的东西

本文不构成：

- OPL replacement 已生产接入；
- generated surface 已生产消费；
- grant-stage production long-run soak 已完成；
- fundability-ready、quality-ready 或 export-ready；
- 旧 runtime/probe/journal/alias/facade 的兼容保留理由。
