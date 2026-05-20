# Med Auto Grant 理想目标态

Owner: `Med Auto Grant`
Purpose: `north_star_reference`
State: `active_support`
Machine boundary: 本文是人读目标态参考。机器真相继续归 `contracts/`、`schemas/`、源码、CLI/API 行为、workspace/runtime artifact root、receipt、质量报告、导出包和 `contracts/runtime-program/current-program.json`。
Date: `2026-05-21`

## 文档读法

- 本文只写 MAG 的 north-star 目标态和长期 owner boundary；当前差距、执行顺序和证据缺口回到 [MAG 理想目标态差距与完善计划](../active/mag-ideal-state-cross-repo-gap-plan.md)。
- 过程性校准、follow-through、receipt proof 和 closeout 流水归档到 [MAG standard agent 文档过程归档 2026-05](../history/plans/mag-standard-agent-doc-process-history-2026-05.md)。
- 目标态优先于当前实现。当前 MAG 内已经存在的 product-entry、sidecar、grouped CLI/API、projection builder、lifecycle adapter、local journal、attempt ledger、workspace/source intake 或 package/memory helper 只能作为迁移输入，不是长期架构约束。
- 目标态不承诺旧 runtime / journal / probe / alias 兼容。旧模块、旧接口、旧测试和旧 docs 入口在 replacement、owner receipt parity 与 no-active-caller proof 成立后直接移除或进入 history/tombstone；MAG 不再新增 compatibility facade 来照顾过时调用方。

## 目标结论

理想状态下，`Med Auto Grant` 是生产级医学基金申请 domain agent。它可以被用户通过单一 `Med Auto Grant` app skill 直接调用，也可以作为 `OPL Framework` 上的 admitted Foundry Agent 被发现、托管、唤醒、恢复和投影。

MAG 的核心价值是 grant truth、fundability strategy、specific aims、正文写作、AI-first review/revision、quality closure、submission-ready package、grant strategy memory body / accept-reject 和 owner receipt。

MAG 的理想形态是：

```text
Declarative Grant Pack
  + OPL generated/hosted surfaces
  + minimal grant authority functions
```

MAG 不应长期维护独立 agent runtime platform，也不长期维护 generic scheduler、daemon、lifecycle owner、queue、attempt ledger、generic state-machine runner、workspace/source intake shell、memory locator、artifact/package lifecycle、observability、App/workbench runtime，或手写 generic CLI/product-entry/sidecar/status wrapper。

只有 fundability verdict、authoring quality/export verdict、package readiness、grant memory accept/reject、owner receipt signer、grant transition oracle 和 grant-native helper 这类无法声明化的 authority function 可以留在 MAG。

理想物理源码形态应直接体现这条分层：`agent/` 是 Declarative Grant Pack；`contracts/` 是 pack compiler、stage/action/memory/artifact/receipt、handoff 和 evidence request 的机器面；`src/med_autogrant/**` 只保留 grant domain handler、minimal authority function、refs-only adapter、native helper、fixture 或 diagnostic。`product-entry`、`sidecar`、`status/user-loop`、`domain_runtime_parts`、`runtime_registration`、`lifecycle`、`memory receipt projection`、`package lifecycle`、`observability` 或 `human workbench / scheduler` 这类路径即使仍在 active source 中，也必须让读者看到它们只是 OPL generated/hosted surface target 或 grant authority refs，不是 MAG 私有 runtime platform。local journal、attempt ledger、repo-owned scheduler daemon、Hermes/Gateway/local-manager probe、flat alias 和 compatibility facade 不属于理想源码形态。

## 产品分层

1. `Med Auto Grant App Skill`
   用户和 Codex 看到的单一领域入口，展示 status、user loop、workspace progress、direct entry、质量状态和交付状态。

2. `MAG Domain Agent Package`
   grant-domain 专业包，提供 stage pack、prompt/skill、route truth、quality gate、domain transition oracle、memory policy、artifact locator contract、submission/export authority、receipt schemas、policy tables 和 authority function manifest。

3. `OPL Framework Hosted Path`
   family-level runtime，提供 stage attempt ledger、typed queue、provider-backed runtime、resume/human gate、receipt、retry/dead-letter、workspace/artifact lifecycle、operator projection 和 App 投影协议。

   MAG manifest 对这层的长期机器字段是 `opl_provider_runtime_contract`；它描述 OPL/configured family provider runtime owner。`Codex CLI` 在该分层中只作为默认 Agent executor / executor owner，不再承担 runtime owner 语义。

4. `Grant Workspace`
   真实任务与文件生命周期承载点，保存用户材料、workspace truth、草稿、审稿意见、修订记录、质量报告、receipt、memory writeback、artifact deltas 和本地提交包。

## MAG 长期职责

MAG 持有所有 grant-specific、author-side、submission-facing 的专业判断与交付权威：

- funding call、funder family、applicant profile、项目基础、材料证据和约束；
- fundability strategy、specific aims、申请人/平台适配、创新性、可行性和 reviewer risk；
- 正文写作、论证闭合、claim-evidence coverage、AI-first critique、review/revision 和 closure dossier；
- package/export authority、本地 submission-ready gate、gap report、manual portal boundary；
- grant transition table / oracle fixtures、typed blocker、owner action 和 owner receipt；
- grant strategy memory body、retrieval semantics、writeback proposal、accept/reject decision 和 runtime receipt。

MAG 程序可以校验 schema、持久化 domain truth、签 owner receipt、暴露 refs 和阻止越权写入；不能为了运行便利复制 OPL generic runtime。

## OPL 长期职责

OPL 负责通用运行外围和工作台：

- stage attempt ledger、queue、retry/dead-letter、heartbeat、resume、human gate；
- provider-backed long-run runtime；
- generic state-machine runner、transition schema、matrix runner 和 transition bridge evidence refs-only drilldown；
- workspace/source intake shell、memory locator/index、artifact/package lifecycle shell、restore/retention ledger；
- operator projection、observability/SLO、App attention queue 和 action routing；
- generated CLI/product-entry/sidecar/status/workbench/harness wrapper。

OPL 不能写 grant truth、memory body、fundability verdict、authoring quality verdict、submission-ready verdict、package authority 或 owner receipt。

OPL 也可以把 MAG stage 的 expected receipt / monitor freshness 缺口转成 refs-only `record` / `verify` evidence route；该 route 只记录或验证 MAG/App/live refs、typed blocker refs、no-regression refs 或 owner-chain refs，不替 MAG 签 owner receipt、不声明 grant stage complete、不授权 fundability/quality/export/submission readiness。Record route 必须提供 payload workorder / preflight；production closeout 应在缺口出现时把 missing workorder 聚合成按 domain/stage 分组的 `stage_evidence_workorder_packet`，方便 App/operator 审计下一步。MAG 只提交真实 owner receipt instance、monitor evidence、typed blocker 或 no-regression refs；声明型占位 ref、OPL ledger receipt ref、workorder packet、grant truth/package/memory body 不能被当作成功 payload。当前 `contracts/stage_control_plane.json` 已为六个 stage 暴露 expected receipt 与 monitor freshness refs，`contracts/external_evidence/mag-evidence-receipt-ledger.json#/grant_stage_controlled_attempt_closeout` 记录 body-free closeout refs。

OPL 可以持有 MAG legacy cleanup 的 refs-only lifecycle ledger，并消费 MAG 提供的 replacement parity、no-regression、history/tombstone 和 owner handoff receipt refs；该 ledger 不授权 OPL 删除 MAG repo 文件，也不能替代真实 grant-stage owner receipt、App/workbench 消费或 production long-soak。

## 理想 Stage Pack

MAG 的 stage pack 应贴近真实基金申请专家工作：

| Stage | MAG domain authority | 典型输出 |
| --- | --- | --- |
| `call_and_candidate_intake` | funding call、profile、材料池与 workspace 初始化 | candidate pool、selected profile、input workspace |
| `fundability_strategy` | fundability、项目适配、评审风险与 route strategy | strategy memo、risk queue、go/no-go or refine receipt |
| `specific_aims_and_structure` | 科学问题、aims、创新点、claim-evidence structure | aims outline、argument map、section skeleton |
| `proposal_authoring` | 正文草稿、段落论证、申请人/平台适配 | draft artifact、progress projection、TODO queue |
| `review_and_rebuttal` | AI-first critique、issue lineage、revision plan | critique report、closure dossier、revision packet |
| `package_and_submit_ready` | freeze、artifact assembly、本地 submission-ready gate | final package、gap report、export receipt |

每个 stage 至少声明 goal、inputs、entry conditions、executor requirements、prompt refs、skill refs、knowledge refs、quality gates、outputs、handoff、source scope、cohort query、OPL queue trigger、monitor 和 dashboard freshness metric refs。OPL 负责发现、排队、恢复、唤醒和投影；MAG 负责 stage 内专家判断、正文生成、quality verdict、route truth 和最终交付 authority。

## Memory 与 Workspace 边界

MAG 的 memory 是 grant strategy memory，不是机械 recipe engine。OPL 可以持有 memory descriptor、locator、consumed refs、writeback proposal refs 和 receipt refs；MAG 持有 memory body、accept/reject authority、fundability/quality 影响判断和 owner receipt。

真实 grant run 必须有明确 workspace 和 runtime artifact root。Workspace 保存用户输入、call materials、draft、critique、revision plan、quality closure dossier、stage receipts、owner receipts、final package、export gap report、accepted/rejected memory writeback receipt 和 restore proof。Repo source 只保存源码、schema、contract、stage definition、prompt、skill、quality gate、projection builder、fixtures 和 docs。

## App 与用户工作台目标

面向用户的 MAG 工作台应优先呈现申请任务本身，而不是 runtime 内部细节：

- `Status`：当前 grant line、target funder、stage、owner、freshness、blocker 和 next action。
- `Workspace`：输入材料、call/profile、draft 状态、evidence gaps、TODO 和显式唤醒。
- `Quality`：scorecard、closure dossier、issue lineage、AI reviewer status 和 unresolved hard issues。
- `Artifacts`：draft、review packet、revision packet、final package、export receipts 和 gap report。
- `Memory`：consumed strategy refs、writeback proposal、accept/reject receipt 和 provenance。
- `Attention Queue`：用户确认、材料补件、重新评审、OPL repair 或 provider wait。
- `Operator Drilldown`：receipt、source refs、repair command、stage handoff 和 owner boundary。

App 可以触发 OPL framework action、MAG guarded dispatch 或 direct domain entry；ready verdict、quality verdict、fundability verdict 和 export verdict 都必须回到 MAG-owned surface。

## 理想完成门槛

- Direct MAG app skill path 与 OPL-hosted path 使用同一 MAG owner surfaces。
- Pack compiler input 只能用 `canonical_semantic_pack_root="agent/"` 与 `canonical_semantic_pack_role="repo_source_declarative_grant_pack"` 表达 canonical grant semantic pack；旧 `canonical_repo_source_semantic_pack`、`domain_pack_root` 或 README-based root signal 不再作为机器接口。`required_domain_pack_paths` 只列真实 prompt / stage / skill / quality gate / knowledge 文件，不能包含 `agent/README.md`。
- Product-entry manifest、schema 和 tests 使用 `opl_provider_runtime_contract` 表达 OPL provider runtime owner；`codex_cli` 仅保留为默认 executor owner / default executor。
- OPL generated / hosted surfaces 是 MAG generic wrapper/caller 的长期 owner；MAG 手写 shell 只保留 domain handler、authority function、refs-only adapter、diagnostic cleanup 或 provenance fixture。MAG repo 侧 bridge 退出必须经过 generated-surface bridge exit gate 或 legacy exit gate；外部 production/default caller 和 live soak 另走证据门。
- OPL standard conformance gate 必须保持通过。2026-05-19 fresh family defaults 已显示 MAG structural conformance `passed`；旧 local journal / attempt ledger / repo scheduler / executor probe / compat alias 的 active exact residue 不允许复活，只能在 history/tombstone/provenance 或 negative guard 中出现。
- `mag_functional_structure_gap_count=0` 只表示 MAG repo 侧 active bridge exit 已闭合，不表示 external production/default caller、真实 App/workbench consumption 或 production long-run soak 已完成。
- OPL `stages cohort-loop --domain mag` 能把六个 MAG stage 都读成 closed-loop ready；该门槛只证明声明式 launch/readiness loop 可被 OPL 消费，不替代 grant-stage owner receipt、App consumption、direct/hosted parity 或 Temporal long soak。
- MAG retained private authority surfaces 完成逐项 AI-first 审计：fundability、authoring quality/export 和 grant strategy memory accept/reject 是 AI-first judgment surface，必须回到 grant stage output 或 AI critique artifact；package authority、owner receipt 和 grant helper 是 programmatic guard surface，只能依 owner receipt、typed blocker、refs 和 action metadata 工作。程序只做 schema validator、materializer、receipt signer、guard 和 refs projection，不能机械生成 ready verdict。
- privatized audit 与 generated-surface handoff 中的 code path / source_ref 与当前 physical source tree 对齐；漂移路径只能进入 history/tombstone/source-ref refresh，不作为完成证明。
- physical source tree 中的 product-entry、sidecar、domain_runtime、runtime/lifecycle/workbench 命名必须持续被合同约束为 domain handler、refs-only adapter、minimal authority function、diagnostic 或 tombstone；不能让命名重新表达 MAG-owned generic runtime。
- 根层 `functional_privatization_audit.mag_consumer_thinning_contract.active_path_scan_state` 必须来自真实 `physical_skeleton_follow_through.active_path_scan_no_legacy_default_caller`，不能停留在 `not_available`。active source scan 只证明 legacy default caller / retired path 在 repo source 中没有复活；它不证明外部 production caller、App/workbench 消费或 Temporal long soak。
- `contracts/production_acceptance/mag-production-acceptance.json` 必须持有 MAG-owned production acceptance evidence tail。该 surface 可以记录 structural / physical conformance passed 和 production-like grant receipt chain refs present；它必须继续声明 OPL/provider/conformance/Agent Lab/meta-agent 不可授权 grant/domain/fundability/submission readiness。若缺少真实 MAG owner receipt scaleout，状态必须是 typed blocker 并携带下一跳 verification refs；若关闭，只能指向 MAG-owned `domain_owner_receipt` refs。
- `contracts/production_acceptance/mag-executor-first-landing.json` 必须保持 executor-first / Codex-first / contract-light 的 active landing program 口径：它可以记录 stage pack enrichment、independent review evidence gate 和并行 evidence lane，但不能把 missing external evidence、direct/hosted parity、App/workbench consumption、owner receipt scaleout、physical morphology cleanup 或 production long-soak 写成已完成。
- Product-entry read/guard surfaces 必须保持 executor-first / refs-only：`codex_stage_execution_receipt_bundle` 只证明 Codex execution + independent review receipt ABI，`operator_closeout_readiness_projection` 只区分 accounting / evidence / quality-readiness，`physical_morphology_guard_projection` 只约束 source role 与 forbidden ownership flags；这些 surface 都不能生成 grant-ready、fundability-ready、quality-ready、export-ready 或 submission-ready。
- OPL refs-only external evidence ledger 可以记录 MAG typed blocker / owner receipt ref roundtrip。2026-05-20 Lane 3 已把 `contracts/external_evidence/mag-evidence-receipt-ledger.json` 推进为 `first_live_production_evidence_consumed_refs_only_long_soak_window_open`：全部 7 条 external evidence request 都有 verified external receipt refs，覆盖 owner receipt roundtrip、default caller、App/workbench consumption、direct/hosted parity no-regression、continuous guard 和 Temporal reconciliation refs；Temporal long-soak window evidence 仍 open。它只证明 first live production evidence refs 可消费，不替代真实 grant workspace 扩面、MAG-owned grant/fundability/export verdict 或 submission-ready export。
- 真实 grant workspace 产生 owner receipt、quality movement、package/export receipt、memory receipt、lifecycle receipt、typed blocker 或 no-regression evidence。
- Legacy Hermes/Gateway/local-manager/journal/probe/compat residue 完成 no-active-caller scan、replacement proof、history/provenance 分类和 physical retirement。

## 2026-05-19 fresh residue audit

`codex/retire-mag-generic-runtime-surfaces` worktree 停在 `fd48dc6`，该提交已是当前 `main` 的祖先。旧 worktree 的未提交删除项会移除 `src/med_autogrant/upstream_hermes.py`、`tests/test_local_runtime.py`、`tests/test_upstream_hermes.py` 以及 local journal / attempt ledger 辅助代码；这些删除已被当前 `main` 的 `7d877b8 Retire MAG local runtime surfaces` 覆盖。旧分支若重新合入会反向带回旧 Hermes/local-runtime 文件，并会丢失当前 `stage_control_plane` event refs，因此只可清理，不可重放。

本轮 fresh scan 后，MAG active source 的标准 agent residue 分类如下：

- 已物理退役 / history-only：`upstream_hermes.py`、`test_local_runtime.py`、`test_upstream_hermes.py`、`runtime-run`、`runtime-resume`、`probe-upstream-hermes`、local journal / attempt ledger owner。
- OPL-owned generated/hosted target，MAG 仅保留 refs-only adapter：product-entry、sidecar、status/user-loop、runtime registration、lifecycle receipt bundle、memory receipt projection、package lifecycle handoff、continuous reconciliation、observability refs、safe action metadata。
- MAG retained private authority：grant truth、fundability / quality / export verdict refs、submission-ready package authority、grant strategy memory body 与 accept/reject、grant transition oracle、owner receipt signer、typed blocker 和 grant-native helper。
- production acceptance evidence tail 已由 `contracts/production_acceptance/mag-production-acceptance.json` 记录为 MAG-owned owner receipt closure；关闭链路为标准 OPL Agent Lab target-agent production evidence suite result、opl-meta-agent no-patch coordination 和 MAG `domain_owner_receipt` projection。MAG 只提供标准 Agent Lab / OMA 可消费 refs、receipt 与 handoff 接口，保留 domain owner receipt、quality/export 和 package authority；Agent Lab/OMA 不提供 MAG-specific suite、command 或 owner authority。MAG 还可作为真实 target smoke refs-only 消费 OMA patch-loop closeout refs，并输出 owner receipt / typed blocker projection；该 smoke 只证明 handoff/closeout shape，不授权 grant-ready、fundability-ready、quality/export-ready 或 submission-ready。`contracts/external_evidence/mag-evidence-receipt-ledger.json` 当前把 external request accounting 闭合为 verified external receipt refs，并补齐 grant-stage controlled attempt closeout 所需 expected receipt / monitor freshness refs。后续仍需连续生产监控、真实 grant workspace 扩面与 MAG-owned quality/export verdict；这些不是 MAG repo 侧功能/结构差距。

## 当前差距入口

当前功能/结构差距、测试/证据差距、完善顺序和禁止误写口径由 [MAG 理想目标态差距与完善计划](../active/mag-ideal-state-cross-repo-gap-plan.md) 维护。本文不双写 active plan。
