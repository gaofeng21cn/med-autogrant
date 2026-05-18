# Med Auto Grant 理想目标态

Owner: `Med Auto Grant`
Purpose: `north_star_reference`
State: `active_support`
Machine boundary: 本文是人读目标态参考。机器真相继续归 `contracts/`、`schemas/`、源码、CLI/API 行为、workspace/runtime artifact root、receipt、质量报告、导出包和 `contracts/runtime-program/current-program.json`。
Date: `2026-05-19`

## 文档读法

- 本文只写 MAG 的 north-star 目标态和长期 owner boundary；当前差距、执行顺序和证据缺口回到 [MAG 理想目标态差距与完善计划](../active/mag-ideal-state-cross-repo-gap-plan.md)。
- 过程性校准、follow-through、receipt proof 和 closeout 流水归档到 [MAG standard agent 文档过程归档 2026-05](../history/plans/mag-standard-agent-doc-process-history-2026-05.md)。
- 目标态优先于当前实现。当前 MAG 内已经存在的 product-entry、sidecar、grouped CLI/API、projection builder、lifecycle adapter、local journal、attempt ledger、workspace/source intake 或 package/memory helper 只能作为迁移输入，不是长期架构约束。

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

每个 stage 至少声明 goal、inputs、entry conditions、executor requirements、prompt refs、skill refs、knowledge refs、quality gates、outputs 和 handoff。OPL 负责发现、排队、恢复、唤醒和投影；MAG 负责 stage 内专家判断、正文生成、quality verdict、route truth 和最终交付 authority。

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
- Product-entry manifest、schema 和 tests 使用 `opl_provider_runtime_contract` 表达 OPL provider runtime owner；`codex_cli` 仅保留为默认 executor owner / default executor。
- OPL generated / hosted surfaces 是 MAG generic wrapper/caller 的长期 owner；MAG 手写 shell 只保留 domain handler、authority function、refs-only adapter、diagnostic cleanup 或 provenance fixture。MAG repo 侧 bridge 退出必须经过 generated-surface bridge exit gate 或 legacy exit gate；外部 production/default caller 和 live soak 另走证据门。
- `mag_functional_structure_gap_count=0` 只表示 MAG repo 侧 active bridge exit 已闭合，不表示 external production/default caller、真实 App/workbench consumption 或 production long-run soak 已完成。
- MAG retained private authority surfaces 完成逐项 AI-first 审计：fundability、authoring quality/export 和 grant strategy memory accept/reject 是 AI-first judgment surface，必须回到 grant stage output 或 AI critique artifact；package authority、owner receipt 和 grant helper 是 programmatic guard surface，只能依 owner receipt、typed blocker、refs 和 action metadata 工作。程序只做 schema validator、materializer、receipt signer、guard 和 refs projection，不能机械生成 ready verdict。
- privatized audit 与 generated-surface handoff 中的 code path / source_ref 与当前 physical source tree 对齐；漂移路径只能进入 history/tombstone/source-ref refresh，不作为完成证明。
- 真实 grant workspace 产生 owner receipt、quality movement、package/export receipt、memory receipt、lifecycle receipt、typed blocker 或 no-regression evidence。
- Legacy Hermes/Gateway/local-manager/journal/probe/compat residue 完成 no-active-caller scan、replacement proof、history/provenance 分类和 physical retirement。

## 2026-05-19 fresh residue audit

`codex/retire-mag-generic-runtime-surfaces` worktree 停在 `fd48dc6`，该提交已是当前 `main` 的祖先。旧 worktree 的未提交删除项会移除 `src/med_autogrant/upstream_hermes.py`、`tests/test_local_runtime.py`、`tests/test_upstream_hermes.py` 以及 local journal / attempt ledger 辅助代码；这些删除已被当前 `main` 的 `7d877b8 Retire MAG local runtime surfaces` 覆盖。旧分支若重新合入会反向带回旧 Hermes/local-runtime 文件，并会丢失当前 `stage_control_plane` event refs，因此只可清理，不可重放。

本轮 fresh scan 后，MAG active source 的标准 agent residue 分类如下：

- 已物理退役 / history-only：`upstream_hermes.py`、`test_local_runtime.py`、`test_upstream_hermes.py`、`runtime-run`、`runtime-resume`、`probe-upstream-hermes`、local journal / attempt ledger owner。
- OPL-owned generated/hosted target，MAG 仅保留 refs-only adapter：product-entry、sidecar、status/user-loop、runtime registration、lifecycle receipt bundle、memory receipt projection、package lifecycle handoff、continuous reconciliation、observability refs、safe action metadata。
- MAG retained private authority：grant truth、fundability / quality / export verdict refs、submission-ready package authority、grant strategy memory body 与 accept/reject、grant transition oracle、owner receipt signer、typed blocker 和 grant-native helper。
- 仍未关闭的不是 MAG repo 侧功能差距，而是外部证据门：OPL generated/hosted caller、App/workbench consumption、production/default caller、direct/hosted parity、Temporal long soak 与 live receipt reconciliation。

## 当前差距入口

当前功能/结构差距、测试/证据差距、完善顺序和禁止误写口径由 [MAG 理想目标态差距与完善计划](../active/mag-ideal-state-cross-repo-gap-plan.md) 维护。本文不双写 active plan。
