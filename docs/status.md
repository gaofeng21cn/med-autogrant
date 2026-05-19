# 当前状态

Date: `2026-05-19`

## 当前角色

`Med Auto Grant` 是医学基金申请 domain agent，也是 OPL-compatible Foundry Agent package。Direct app skill / CLI / `MedAutoGrantDomainEntry` 仍是一等入口；OPL-hosted path 可以发现、托管、唤醒和投影 MAG，但必须回到同一套 MAG-owned grant truth、fundability / quality / export verdict、package authority、grant strategy memory accept/reject、owner receipt 和 typed blocker。

OPL Framework 持有通用 provider runtime、typed queue、attempt ledger、generic transition runner、workspace/source shell、memory locator、artifact/package lifecycle shell、operator projection、observability/SLO、generated wrapper 和 App/workbench shell。MAG 的 product-entry、sidecar、grouped CLI/API、projection builder、lifecycle adapter、local journal、attempt ledger、workspace/source intake 或 package/memory helper 只能作为迁移输入、domain handler target、refs-only adapter、authority function 或 history/tombstone，不是长期私有平台。

`Codex CLI` 是当前第一公民 executor。`Hermes-Agent`、Claude Code 等只允许作为显式 opt-in executor adapter / proof lane，通过 OPL receipt/audit/fail-closed 边界接入；不承诺行为、质量或 resume 语义等价。

Product-entry manifest 当前暴露 `opl_provider_runtime_contract`；runtime owner 是 configured OPL/family provider runtime owner，`codex_cli` 只作为默认 executor owner / default executor 出现。

## 当前运行与文档事实

- 单一 `Med Auto Grant` app skill、CLI、`MedAutoGrantDomainEntry`、product status/user-loop/direct-entry、workspace progress/cockpit、product sidecar export/dispatch 和 package submission-ready 是当前 direct path 与 domain handler surface。
- `contracts/runtime-program/current-program.json`、schemas、product-entry manifest、sidecar receipt、workspace/runtime artifact root、质量报告和导出包是机器真相；`docs/**` 只做解释、导航、治理和 provenance。
- MAG 已声明 domain descriptor、pack compiler input、generated surface handoff、family action catalog、family stage control plane、domain memory descriptor、artifact locator contract、owner receipt contract、functional privatization audit 和 private functional surface policy，可被 OPL 生成/读取 descriptor。`agent/` 现在是 repo-source canonical Declarative Grant Pack，包含 stage prompts、stage policies、skill declaration、quality gates 和 knowledge boundaries；`src/` 只保留 domain handler、minimal authority function 与 native helper 角色。
- `runtime`、`opl_provider_runtime_contract`、`runtime_inventory` 和 `runtime_control` 的当前 owner split 已同步：OPL provider runtime 持有通用 runtime，MAG 持有 grant-domain truth，`codex_cli` 持有默认 concrete executor。
- Descriptor ready、receipt reconciliation proof、transition oracle smoke 或 no-regression evidence 只能说明可发现、可投影、可对账；不能写成生产默认 caller 已迁到 OPL generated/hosted surface，也不能写成 MAG 已是纯 knowledge pack。
- 过程性校准、follow-through、receipt proof 和 closeout 流水归档到 [MAG standard agent 文档过程归档 2026-05](./history/plans/mag-standard-agent-doc-process-history-2026-05.md)，不在本页展开。

## 当前结构收口状态

当前结构收口状态按 [MAG 理想目标态差距与完善计划](./active/mag-ideal-state-cross-repo-gap-plan.md) 维护：

`mag_functional_structure_gap_count=0`

MAG repo 侧 handler/ref-only 边界已收薄：product/status/user-loop/sidecar/grouped CLI/projection/lifecycle wrapper 的目标长期 owner 固定为 OPL generated/hosted surface；当前仍由 MAG CLI/product-status/sidecar 触达的 surface 只允许写成 direct domain handler、domain handler target、refs-only adapter、owner receipt、typed blocker、verdict refs、safe action metadata 或 minimal authority function。

2026-05-19 语义包归位：`agent/README.md` 已从 skeleton anchor 升级为 Declarative Grant Pack 入口；`agent/prompts/` 为六个 MAG stage 提供真实 stage prompt；`agent/stages/` 固定 stage policy；`agent/skills/` 固定 domain skill 声明；`agent/quality_gates/` 固定 fundability、quality、export/package、memory/receipt 与 authority 边界；`agent/knowledge/` 固定 grant strategy memory、package authority 与 owner receipt 知识边界。`contracts/stage_control_plane.json` 的 `prompt_refs` 解析到 `agent/prompts/*.md`，`contracts/pack_compiler_input.json` 的 `required_domain_pack_paths` 强制列出完整 pack 文件。

机器面同步到 `mag_handler_boundary_ready_external_caller_evidence_gated` / `mag_handler_boundary_ready_external_evidence_gated`：`functional_privatization_audit`、`product-entry manifest`、`sidecar export`、`current-program` 和 `opl-family-contract-adoption` 均声明 `claims_opl_replacement_exists=false`、`claims_all_bridge_exits_complete=false`、`claims_production_long_run_soak_complete=false`。这表示 MAG repo 侧已把自身 surface 收到 handler/ref-only/authority 边界，不表示外部 production/default caller、真实 App/workbench 消费、全部 bridge exit 或长时 soak 已完成。

`mag_consumer_thinning_contract.generated_surface_handoff.current_mag_path_status` 现在为 generated/bridge surface 的每个 `current_mag_paths` 输出 machine-readable currentness proof；`missing_current_mag_path_count=0`，`stale_path_policy=history_or_source_ref_refresh_only`。该 proof 只证明 MAG 当前 handler/ref-only/authority source refs 存在，不能写成 OPL replacement exists、bridge exit complete 或 production soak complete。

`mag_consumer_thinning_contract.external_evidence_request_pack` 现在把剩余外部证据门机器化为 `mag.external_evidence_request_pack.v1`：OPL generated/hosted caller pack consumption、Codex App workbench package refs consumption、production/default caller release/dist consumption、owner receipt / typed blocker roundtrip、continuous no-forbidden-write、direct/hosted parity 和 Temporal provider long-soak receipt reconciliation。该 pack 只请求 refs、receipt shapes 与 parity evidence，明确 `mag_implements_opl_runtime=false`、`mag_implements_app_workbench=false`、`mag_claims_external_evidence_exists=false`，不能作为外部证据已收到的证明。

local runtime journal / attempt ledger、repo-owned scheduler daemon、upstream Hermes probe、flat shell alias、facade patch bridge 和 compat aggregate test 现在只允许作为 legacy proof / tombstone / regression oracle 存在；无 active caller 后直接删除或归档，不保留 compatibility alias。

2026-05-19 OPL legacy cleanup 读取当前 MAG `physical_skeleton_follow_through` 后返回 `plan_status=ready`、`lifecycle_apply.status=dry_run_ready`、`safe_action_count=3`、`unsafe_action_count=0`；随后 `--mode apply` 已写入 1 条 batch receipt 与 3 条 action receipts，`--mode verify` 可读回 batch / tombstone / handoff receipts 和 2 条 domain owner handoff receipt refs。MAG manifest 已为 physically removed Gateway/local-manager active path 提供 domain owner handoff receipt refs，并提供 replacement parity、no-regression、history 和 tombstone refs。该状态只关闭 OPL cleanup gate / refs-only ledger blocker；外部 production/default caller、真实 App/workbench consumption、grant-stage live soak 和 owner receipt scaleout 仍是证据门。

MAG retained private surface 限定为 grant domain truth、fundability / quality / export verdict、package authority、grant strategy memory body 与 accept/reject、owner receipt、transition oracle、grant-native helper 和 focused contract tests。

Retained private authority surfaces 现在在 `functional_privatization_audit`、product-entry manifest、sidecar export 与 pack compiler input 中携带 AI-first taxonomy、judgment owner、programmatic role、allowed return shapes 和 forbidden output boundary。`fundability_verdict`、`quality_verdict`、`export_verdict` 与 `memory_accept_reject` 是 AI-first judgment surface，程序只 materialize refs / guard / typed blocker；`package_authority`、`owner_receipt_signer` 与 `grant_helper` 是 programmatic authority/helper surface，只能签 receipt、验证 refs 或返回 action metadata。所有 surface 都禁止从 schema completeness、provider completion、package existence、quality scorecard 分数或 generic lifecycle completion 机械生成 ready verdict。

2026-05-19 fresh cleanup audit 结论：`.worktrees/retire-generic-runtime-surfaces` / `codex/retire-mag-generic-runtime-surfaces` 是 stale lane，分支提交已在当前 `main` 祖先链上，旧 dirty 删除已被当前 `main` 覆盖。该 lane 不再提供可重放代码 cleanup；重新合入会反向带回旧 Hermes/local-runtime 文件并损坏当前 stage runtime event refs 口径。当前应清理 stale worktree / branch，并把剩余 gap 继续限定为外部 OPL/App/production caller evidence gate。

## 当前测试/证据差距

以下证据门单独统计，不能反向重开 MAG repo 侧 active bridge exit：

- 真实 OPL-hosted grant-stage attempt 持续返回 MAG owner receipt、typed blocker 或 no-regression evidence。
- 真实 grant workspace 产生 accepted/rejected memory receipt、package/export lifecycle receipt、cleanup/restore/retention receipt 和 owner receipt scaleout。
- OPL/App shell 真实消费 MAG package refs、gap report、manual portal boundary、quality refs、transition oracle refs 和 safe action refs。
- external production/default caller、release/dist consumption、continuous no-forbidden-write 和 direct/hosted parity 证据。
- Temporal provider long SLO、repair cadence 和 live receipt reconciliation。

这些证据门已由 `external_evidence_request_pack` 给出 request id、required refs 和 required receipt shapes；当前状态仍是 `requested_not_received`。

## 当前入口

- 用户路径：`Med Auto Grant app skill -> product status -> product user-loop -> workspace progress / workspace cockpit -> product direct-entry -> pass / package commands`。
- Pre-workspace：`discover-funding-opportunities -> select-project-profile -> initialize-intake-workspace`。
- Grant stage plane：`family_stage_control_plane` 暴露 `call_and_candidate_intake`、`fundability_strategy`、`specific_aims_and_structure`、`proposal_authoring`、`review_and_rebuttal`、`package_and_submit_ready`。
- Declarative Grant Pack：`agent/prompts/`、`agent/stages/`、`agent/skills/`、`agent/quality_gates/`、`agent/knowledge/` 是 OPL pack compiler 和 generated surfaces 的 repo-source 语义输入。
- 质量治理：`workspace quality-scorecard`、`workspace quality-closure-dossier`、`workspace quality-diff`；这些是 AI critique-backed aggregator，不是机械 ready verdict。
- Sidecar：`product sidecar export` / `dispatch` 只返回 refs、owner receipt、typed blocker、verdict refs 与 authority action metadata；不是常驻 daemon。

## 当前不能声明

- 不能把 `mag_functional_structure_gap_count=0` 写成 external production/default caller、真实 App/workbench consumption 或 production long-run soak 已完成。
- 不能把 `classification_gap_count=0`、descriptor ready、transition oracle smoke、receipt reconciliation proof 或 no-regression evidence 写成 provider SLO / live soak 已完成。
- 不能把 OPL provider completion、matrix runner smoke、package existence、schema completeness、quality scorecard 分数或 controller route 写成 fundability-ready、quality-ready、export-ready 或 submission-ready verdict。
- 不能把 hand-written product-entry / sidecar / grouped CLI/API / projection / lifecycle wrapper 写成长期合理私有平台。
- 不能把 local journal、attempt ledger、Hermes probe、Gateway/local-manager、flat CLI alias、compatibility aggregate test 或 `codex_cli` executor 写回默认 runtime owner。
- 不能把 OPL legacy cleanup dry-run / apply / verify ready 写成 MAG 已完成 external production/default caller、真实 App/workbench consumption 或 grant-stage long soak。

## 目录与验证口径

- repo-tracked 主线不保留项目级 `.codex/`、`.omx/`、`.runtime-program/`、`.agent-contract-baseline.json` 或 `runtime-state/`；本机 session、prompt、log、report 与 hook 状态统一属于 `$CODEX_HOME/projects/med-autogrant/runtime-state/`。
- Python / pytest lane 必须通过 `scripts/run-python-clean.sh` 或 `scripts/run-pytest-clean.sh`，把 bytecode、pytest cache 和安装/同步副产物导向仓库外部。
- 测试口径只固定 machine-readable contract、schema、CLI/API、generated artifact 结构与污染 guard；`README*`、`docs/**` 和 skill 正文文案不作为稳定断言面。

## 下一跳

- 目标态：[Med Auto Grant 理想目标态](./references/med-auto-grant-ideal-state.md)
- 差距与顺序：[MAG 理想目标态差距与完善计划](./active/mag-ideal-state-cross-repo-gap-plan.md)
- 文档治理：[MAG 文档组合治理](./docs_portfolio_consolidation.md)
- 过程归档：[MAG standard agent 文档过程归档 2026-05](./history/plans/mag-standard-agent-doc-process-history-2026-05.md)
