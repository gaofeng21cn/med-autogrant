# Med Auto Grant 理想目标态

Owner: `Med Auto Grant`
Purpose: `north_star_reference`
State: `active_support`
Machine boundary: 本文是人读目标态参考。机器可读真相继续归 `contracts/`、`schemas/`、源码、CLI/API 行为、workspace/runtime artifact root、receipt、质量报告、导出包和 `contracts/runtime-program/current-program.json`。
Date: `2026-05-17`

## 文档读法

- `定位`：本文只写 MAG 的 north-star 目标态和长期 owner boundary；当前差距、执行顺序和 production evidence 缺口回到 `mag-ideal-state-cross-repo-gap-plan.md`。
- `当前实态校准`：带日期的校准段只记录当前 repo surface 或 fresh evidence，不把目标态写成已完成事实。
- `Owner 边界`：MAG 持有 grant truth、fundability/quality/export verdict、grant strategy memory body/accept-reject、package authority 和 owner receipt；OPL 持有 provider runtime、queue、attempt ledger、workspace/source intake shell、memory locator、package/artifact lifecycle、quality/readiness projection 和 App/workbench shell。
- `目标态优先`：MAG 当前已存在的 product-entry、sidecar、grouped CLI/API、projection builder、lifecycle adapter、local journal、attempt ledger、workspace/source intake 或 package/memory helper 只能作为迁移输入，不是理想态约束。理想 MAG 是标准 OPL Agent：声明式 grant pack + OPL generated/hosted surfaces + 最小 grant authority functions。
- `最短路径`：MAG consumer/thin adapter 功能面已经把 workspace/source intake、memory locator/writeback transport、package/export lifecycle、route/decision/workbench、observability/SLO 和 scaffold/template 规则归位为 OPL Framework / App replacement expectation；2026-05-17 后目标进一步收紧为 OPL pack compiler / generated surface，且 `functional_structure_gap_zero_classification` 已把 MAG repo 侧功能/结构差距收口为 `0`。MAG 默认提交声明式 grant pack 和少量 grant authority functions，CLI/product-entry/sidecar/status/workbench 外壳由 OPL 生成或托管；后续用真实 workspace/runtime evidence、focused verification 的真实 OPL-hosted production attempt 证据和 live soak 验收。
- `禁写口径`：MAG 当前 skeleton anchors 不是完整新 Agent 目录模板；OPL provider completion、receipt reconciliation proof 或 no-regression evidence 都不能写成 fundability-ready、quality-ready、export-ready 或 production long-run soak 完成。

## 结论

理想状态下，`Med Auto Grant` 是生产级医学基金申请 domain agent。它可以被用户通过单一 `Med Auto Grant` app skill 直接调用，也可以作为 `OPL Framework` 上的 admitted Foundry Agent 被发现、托管、唤醒、恢复和投影。

MAG 的核心价值是基金申请专业性：它持有 funding-call 语境、fundability strategy、specific aims、正文写作、AI-first review/revision、quality closure、submission-ready package 与 grant strategy memory 的 domain truth。OPL Framework 负责长期在线、stage attempt 生命周期、queue/wakeup、handoff、receipt、retry/dead-letter、operator projection、artifact/file lifecycle、shared contracts 和 provider-backed runtime。两者通过 descriptor、projection、receipt 和 owner boundary 协作。

因此，MAG 的理想形态是医学基金 `Declarative Grant Pack + minimal authority functions`。MAG 不维护独立 agent runtime platform，也不长期维护 generic scheduler、generic daemon、generic lifecycle owner、generic queue、generic attempt ledger、generic state-machine runner、generic workspace/source intake shell、generic memory locator、generic artifact/package lifecycle、generic observability、通用 App/workbench runtime，或手写的 generic CLI/product-entry/sidecar/status wrapper。MAG 的 descriptor、contract/schema、domain transition spec/table、quality gate、artifact locator、receipt schema、tests、grant policy tables 和 authority function manifest 只负责把 grant stage pack、fundability/quality/export authority、typed blocker、owner receipt、artifact locator、safe action refs 和 domain transition spec 暴露给 OPL；当前 thin consumer contract 明确声明消费 OPL `family_scheduler_replacement`。product sidecar、projection builder、lifecycle adapter 和 grouped CLI/API 长期应成为 OPL pack compiler 的生成目标或显式迁移桥；只有 fundability verdict、authoring quality/export verdict、package readiness、grant memory accept/reject、owner receipt signer 和 grant-native helper 这类无法声明化的 authority function 可以留在 MAG。

这条目标态不受当前实现分布限制。MAG 今天能运行的 local journal、attempt ledger、user-loop、sidecar dispatch、package lifecycle helper、memory receipt writer、projection builder 或 grouped CLI，不因为已经存在就成为长期架构。必要时可以革命式重构 MAG，而不是在现状上做保守改革。凡属于跨 domain transport、ledger、index、lifecycle、workbench、observability、runner、generated wrapper 或 App shell 的部分，都应上收到 OPL primitive / pack compiler 或收薄为 refs-only adapter；凡只是旧入口或旧测试保护层，迁移 active caller 后直接退役。

MAG 可以保留的私有程序面必须小到能解释为 grant authority function 或 grant-native helper：funding call 解释、fundability verdict、specific aims/quality/export verdict、package authority、memory accept/reject、owner receipt signing。保留项必须声明接口、receipt schema、active caller 和无法上收原因，不能以“MAG 需要完整写作流程”为理由保留一整套私有运行平台。

本文描述目标态，不替代当前状态判断。当前落地程度以 [当前状态](../status.md)、[架构](../architecture.md)、[不变量](../invariants.md)、[OPL Family Contract Adoption](./opl_family_contract_adoption.md) 与 [`current-program.json`](../../contracts/runtime-program/current-program.json) 为准。

2026-05-15 当前代码已把 MAG 侧 receipt reconciliation 推进到 repo-local proof surface：`controlled-soak-receipt-reconciliation-proof` 可以读取 MAG owner receipt evidence 或 sidecar `stage-attempt/closeout` result，并与外部 OPL ledger ref 对账，输出 owner receipt、typed blocker 或 no-regression evidence probe payload；`controlled-soak-receipt-reconciliation-inventory` 则在不写 receipt instance 的前提下汇总多条 owner receipt evidence 的 reconciliation status、typed blocker 和 no-regression refs。该能力是理想态中 OPL-hosted attempt 对账面的前置形状证明，不是 production long-run soak；真实 grant-stage owner chain、memory body apply 和 package/export verdict 仍必须由 MAG workspace/runtime owner surface 产生。

2026-05-16 校准：MAG 当前目录和 contract 已经比早期更接近 OPL Foundry Agent 范本：repo 根层具备 `agent/`、`contracts/runtime-program/`、`plugins/mag`、`runtime/`、`schemas/`、`docs/active|public|product|runtime|delivery|source|policies|specs|references|history` 和单一 app skill/CLI/product-entry 面。当前 `standard skeleton` 的真实状态应读作 `minimum anchors / descriptor-index surface`：`agent/` 与 `runtime/` 主要提供 stage descriptor、skill/knowledge/quality gate 索引、projection builder / lifecycle adapter 索引和 no-artifact-boundary，不表示全仓已经完成理想物理迁移。MAG 适合作为“grant-domain authority pack 如何接入 OPL”的范本，但还不是可复制的新 Agent 物理 skeleton 模板：Python package、historical docs、runtime proof surface 和 grant-specific schemas 仍带有 MAG 语境。新 Agent 应复用 MAG 的 owner-boundary、receipt/schema、docs taxonomy、descriptor/action/stage/memory/artifact locator 纪律，而不是直接复制整棵目录。

同日 fresh sidecar evidence 显示，正确入口 `uv run python -m med_autogrant.cli product sidecar-export --input examples/nsfc_workspace_p2c_critique.json --format json` 会投影 `mag_consumer_thinning_contract`：`adapter_role=domain_authority_pack_with_thin_program_surface`、`consumes_opl_family_primitive=family_scheduler_replacement`、`claims_opl_replacement_exists=false`、`claims_production_long_run_soak_complete=false`。合同同时固定 MAG 不持 generic scheduler、daemon、lifecycle owner、queue、attempt ledger、generic state-machine runner、generic workbench、generic memory transport 或 generic artifact lifecycle owner role；MAG 保留 grant-owned refs、owner receipt、typed blocker、verdict refs 和 domain action metadata。`consumed_opl_standard_surfaces` 明确 MAG 消费 OPL standard scaffold、OPL generic primitives 与 OPL functional harness，并保留 grant truth、fundability/quality/export verdict、memory body accept/reject、package authority 和 owner receipt；`functional_harness_consumer_coverage` 明确 MAG 作为 consumer 覆盖 memory refs-only writeback chain、queue/stage attempt/typed closeout、generic transition runner、restart/dead-letter/repair/human gate 状态链，同时 fail-closed 禁止把 OPL harness pass 写成 grant-ready 或 export-ready；`thin_surface_output_guard` 把 sidecar 输出限制为 refs / receipts / blockers / verdict refs / action metadata，并禁止 generic runtime state、functional harness runtime state、generic workbench state、generic memory transport state、generic artifact lifecycle state、grant artifact content 和 memory body；`standard_agent_scaffold_alignment` 则明确 MAG 仍保留 domain entry、schema、sidecar、projection builder、receipt writer 和 focused tests，不退化为纯知识文件仓。

同日 OPL surface follow-up 后，MAG 对 OPL 新增的 family conflict envelope、stage-attempt usage/control-loop、runtime observability export 与 product-operator projection 的姿态是 `consume/read-only/project refs`。MAG 可以把 owner receipt refs、typed blocker refs、artifact locator refs、memory receipt refs、grant transition oracle ref 和 safe action refs 投影给 OPL；不能写 OPL stage-attempt ledger，不能执行 OPL repair，不能把 provider completion 写成 grant-ready，也不能从 observability 或 conflict envelope 生成 fundability、quality 或 export verdict。

同日 privatized functional module audit closeout 后，MAG 把非知识功能面进一步落成机器可读分类：runtime registration、task lifecycle、session ledger / attention queue、lifecycle adapter、observability、sidecar/product status、package lifecycle、source intake、人用 workbench / scheduler / daemon 是 OPL-owned generic primitive consumer；grant lifecycle stage、fundability / quality / export verdict、package readiness / submission-ready、grant transition oracle、owner receipt / no-regression evidence、grant strategy memory accept/reject 是 MAG-owned grant truth / receipt / verdict；默认 Hermes/Gateway/local-manager runtime owner、domain runtime patch bridge、compatibility aggregate test、legacy flat shell alias 和 repo-owned scheduler/daemon 是 retire/tombstone。该审计面用于 OPL 统一读取，不能被用来删除 grant `lifecycle_stage`、package readiness、submission-ready、fundability、quality、export verdict 或 owner receipt。

该审计面现在逐项列出 `code_paths`、`active_callers`、`active_caller_status`、`migration_action`、`retention_reason` 和 `cannot_absorb_reason`。当前目标态不是把 MAG 压成纯知识文件仓：`MedAutoGrantDomainEntry`、receipt schema/writer、grant transition oracle、fundability / quality / export verdict、package authority、memory accept/reject、owner receipt signer 和 focused contract tests 仍是 MAG 必要 domain authority surface。product-entry manifest builder、product sidecar adapter、refs-only projection builder、grouped CLI/API 和 lifecycle adapter 当前可以作为迁移桥存在，但长期应成为 OPL pack compiler / generated surface 的输出。需要从 MAG 私有实现中继续抽离到 OPL 的，是 local journal / attempt ledger、attention queue、generic stage-attempt ledger、workspace/source intake shell、artifact/package lifecycle shell、operator workbench、runtime observability/SLO、scheduler/daemon、generic transition runner 和 generated wrapper owner。optional `Hermes-Agent` / `hermes_state.SessionDB` 只保留为显式 proof/provenance lane，不是默认 runtime owner，也不是 MAG 要继续私有化维护的 provider substrate。

同日 thin output guard follow-through 后，MAG 的 sidecar / manifest 输出层也被锁定：local runtime journal state、local attempt ledger state、attention queue state、stage attempt ledger state、package lifecycle state、source intake state、operator workbench state、scheduler daemon state 和 Hermes state-db runtime state 都是 forbidden output class。理想态下 MAG 可以保留 grant domain thin adapter 和 explicit proof/provenance lane，但不能把这些私有功能状态作为 MAG-owned runtime surface 输出给 OPL 或 App。

执行顺序上，MAG 理想态的已知功能面上收和收薄在 MAG 仓内已经完成为 consumer follow-through；2026-05-17 后 `functional_structure_gap_zero_classification` 进一步把 P1-P4 功能/结构差距收口为 MAG repo 侧 `0`。workspace/source intake、memory locator/writeback transport、package/export lifecycle、route/decision/workbench、observability/SLO、scaffold/template 规则和 generated wrapper owner 都回到 OPL Framework / App replacement expectation，MAG 保留 grant authority pack、policy/schema/fixtures 和少量 authority function。剩余工作是外部 OPL pack compiler / replacement 证据、真实 workspace/runtime memory-package-lifecycle receipt、focused OPL-hosted verification 的真实 grant-stage attempt 证据和 live soak；其中 live soak 是后置生产验收。

## 产品分层

目标产品认知保持四层：

1. `Med Auto Grant App Skill`
   用户和 Codex 看到的单一领域入口。它展示 product status、user loop、workspace progress/cockpit、direct entry、可调用 command catalog、质量状态和交付状态。
2. `MAG Domain Agent Package`
   grant-domain 专业包。它提供 stage pack、prompt/skill、family profile、route truth、quality gate、domain transition spec、domain memory policy、artifact locator contract、submission/export authority、receipt schemas、policy tables 和 authority function manifest；product sidecar adapter 和 status/product wrappers 默认由 OPL generated surface 承担。
3. `OPL Framework Hosted Path`
   family-level runtime。它提供 stage attempt ledger、typed queue、provider-backed runtime、resume/human gate、receipt、retry/dead-letter、workspace/artifact lifecycle、operator projection 和 App 投影协议。
4. `Grant Workspace`
   真实任务与文件生命周期承载点。它保存用户材料、workspace truth、草稿、审稿意见、修订记录、质量报告、receipt、memory writeback、artifact deltas 和本地提交包。

目标链路如下：

```text
User / Codex / One Person Lab App
  -> Med Auto Grant app skill
  -> product status / user-loop / direct-entry
  -> MedAutoGrantDomainEntry
  -> MAG stage pack and route truth
  -> Codex CLI or explicit OPL executor adapter
  -> MAG quality gate / controller / package gate
  -> workspace artifacts and owner receipts
```

OPL 托管链路如下：

```text
User / One Person Lab App
  -> OPL Framework
  -> stage attempt / typed queue / provider-backed runtime
  -> MAG-owned descriptor and sidecar projection
  -> Med Auto Grant app skill or MedAutoGrantDomainEntry
  -> MAG-owned domain truth, quality verdict, and export authority
```

## MAG 的理想职责

MAG 的长期职责是持有所有 grant-specific、author-side、submission-facing 的专业判断与交付权威。

### Funding 与任务锁定

- 读取 call、funder family、applicant profile、项目基础、材料证据和约束。
- 在 pre-authoring 阶段支持 funding discovery、profile selection 和 input-intake workspace 初始化。
- 一旦用户或 workspace 锁定指定基金任务，后续 authoring、review、revision 和 package 都在同一任务内闭环推进。
- 跨 funder 调整必须作为显式重规划事件处理，并留下新的 route/owner receipt。

### Fundability 与 aims strategy

- 持有 fundability strategy stage，判断科学问题、申请人基础、基金适配、创新性、可行性、风险缓释和 reviewer risk。
- 把 reusable strategy 沉淀为自然语言 grant strategy memory，供 stage 检索和推理使用。
- 保持 memory、scorecard、controller 和 export gate 的边界：memory 可以影响策略，不产生 fundability verdict、authoring quality verdict 或 export verdict。

### 正文写作主线

- 持有 `question_refinement`、`argument_building`、`fit_alignment`、`outline`、`drafting`、`revision`、`freeze/frozen` 的 route truth。
- 以正文科学性、论证闭合、claim-evidence coverage 和 applicant/funder fit 作为主任务完成判断。
- 保持“科学完成可待审包”和“形式/客观补件完成”分层；portal 前置材料默认进入 TODO 与显式唤醒队列。

### AI-first 评审与质量治理

- 质量判断由 AI-authored critique、review/revision artifact、scorecard、closure dossier 和 issue lineage 共同支撑。
- `workspace quality-scorecard`、`quality-diff`、`quality-closure-dossier` 和 autonomy controller 聚合证据、问题队列和闭合进度。
- schema、controller 和 projection 只能表达结构化状态；没有 active AI critique 或 AI-authored quality assessment 时，质量状态必须保持 projection-only。

### Package 与 export authority

- `package submission-ready` 是本地严格导出 gate，负责 frozen workspace、材料完整性、artifact bundle、hosted contract bundle 和 final package 的 fail-closed 导出。
- 本地 submission-ready package 不等于外部官网 portal submission 已完成；官网提交继续是人工监督步骤。
- export verdict、package refs、gap report 和 owner receipt 由 MAG 持有，OPL/App 只展示这些 refs 和下一步动作。

## 理想 Stage Pack

MAG 的 stage pack 应贴近真实基金申请专家工作，而不是把 grant authoring 拆成机械脚本节点。

每个 stage 至少声明：

- `goal`：本阶段的专家目标。
- `inputs`：call、workspace、draft、profile、evidence、review comments、memory refs 和上游 handoff。
- `entry_conditions`：允许进入阶段的 workspace、identity、route 和 evidence 条件。
- `executor_requirements`：默认 `Codex CLI`，以及显式可选 executor adapter 需要的 receipt 条件。
- `prompt_refs`：stage prompt、review prompt、revision prompt 和角色策略。
- `skill_refs`：MAG skill、Codex skill、OPL skill 和工具入口。
- `knowledge_refs`：grant strategy memory、funder family grammar、template strategy、historical issue patterns 和 closure lessons。
- `quality_gates`：fundability、authoring quality、review closure、package/export gate。
- `outputs`：artifact deltas、quality reports、stage closeout、owner receipt、typed blocker、human gate 或 next-stage handoff。

目标 stage 映射如下：

| Stage | MAG domain authority | 典型输出 |
| --- | --- | --- |
| `call_and_candidate_intake` | funding call、profile、材料池与 workspace 初始化 | candidate pool、selected profile、input workspace |
| `fundability_strategy` | fundability、项目适配、评审风险与 route strategy | strategy memo、risk queue、go/no-go or refine receipt |
| `specific_aims_and_structure` | 科学问题、aims、创新点、claim-evidence structure | aims outline、argument map、section skeleton |
| `proposal_authoring` | 正文草稿、段落论证、申请人/平台适配 | draft artifact、progress projection、TODO queue |
| `review_and_rebuttal` | AI-first critique、issue lineage、revision plan | critique report、closure dossier、revision packet |
| `package_and_submit_ready` | freeze、artifact assembly、本地 submission-ready gate | final package、gap report、export receipt |

OPL 负责 stage 的发现、排队、恢复、唤醒、投影和 receipt 汇总。MAG 负责 stage 内的专家判断、正文生成、质量 verdict、route truth 和最终交付 authority。

## Runtime 与执行器边界

理想 MAG 不维护通用长期在线 runtime 或通用运行平台。它暴露 OPL 可消费的 descriptor、contract/schema、artifact locator、owner receipt contract、domain transition spec/table、focused tests、policy tables 和 authority function manifest。sidecar projection、guarded dispatch、status/read model、projection builder、grouped CLI/API 和 lifecycle adapter 默认由 OPL pack compiler 生成或托管；MAG 手写实现只作为迁移桥或 grant authority function。

默认 concrete executor 是 `Codex CLI`。非默认 executor，例如 `Hermes-Agent` 或 `Claude Code`，只能通过 OPL generic Agent Executor Adapter 显式选择，并产生可审计 receipt。非默认 executor 的 proof 只证明 connectivity、lifecycle、receipt、audit 和 fail-closed；结果质量和行为语义必须回到 MAG quality gate 验收。

生产级托管时，OPL 可以承担：

- stage attempt ledger、queue、retry、dead-letter、heartbeat、resume 和 human gate；
- provider-backed long-run runtime；
- generic state-machine runner、transition schema、matrix runner 和 transition bridge evidence refs-only workbench drilldown；
- workspace/artifact lifecycle locator；
- operator projection 和 App attention queue；
- framework-level no-forbidden-write、source fingerprint、attempt replay safety 和 receipt audit。

MAG 保持：

- grant route truth；
- workspace、draft、review、revision 和 package truth；
- fundability、authoring quality 和 submission/export verdict；
- domain memory accept/reject；
- stage closeout 和 owner receipt；
- grant transition table / oracle fixtures：把 funding call、fundability、specific aims、review/rebuttal、package/export 和 human gate 状态映射为下一 owner、typed blocker、repair action 或 closeout receipt。OPL runner 可执行这份 spec，但不能解释 fundability-ready、quality-ready 或 export-ready。

## Domain Memory 理想态

MAG 的 memory 是 grant strategy memory，不是机械 recipe engine。

理想 memory flow：

1. Stage 根据 call、funder family、workspace state 和 current blocker 检索少量相关 memory refs。
2. Executor 在 fundability、aims、authoring、review 或 package stage 中使用这些 refs 推理。
3. closeout 或 review 阶段提出 writeback proposal。
4. MAG owner 接受或拒绝 writeback，并写出 runtime receipt evidence。
5. OPL/App 只显示 consumed-memory refs、writeback proposal refs、accept/reject receipt refs 和 freshness。

真实 memory body、private evidence、fundability verdict、authoring quality verdict、submission-ready verdict 和 grant artifact 不进入 repo source，也不由 OPL 持有。

## Workspace 与文件生命周期

理想情况下，每个 grant run 都有明确 workspace 和 runtime artifact root。

Workspace 应保存：

- 用户输入、call materials、profile、source receipts 和 ingest records。
- workspace truth、draft、critique、revision plan、issue lineage 和 quality closure dossier。
- stage attempt receipts、domain owner receipts、typed blockers、human gate receipts。
- intermediate artifacts、final package、export gap report 和 provenance。
- accepted/rejected memory writeback receipt 和 restore proof。

Repo source 应保存：

- domain source、schema、contract、stage definition、prompt、skill、quality gate、projection builder、fixtures 和 docs。
- 小型测试 fixture 与 seed template，但不保存真实 workspace artifact、private evidence、receipt instance 或 export package。

OPL 应保存或索引：

- workspace locator、artifact locator、runtime root locator、stage attempt metadata、queue metadata、receipt refs、freshness、repair hints 和 operator projection。
- transition execution metadata、dispatch receipt refs、owner receipt refs、no-regression evidence refs、typed blocker refs、human gate refs、retry/dead-letter refs、matrix-runner audit refs 和 transition evidence operator projection；grant transition truth、fundability verdict、quality verdict 和 export verdict 仍归 MAG。

这个边界让仓库保持可审查、可发布，运行文件保持可恢复、可清理、可迁移。

## App 与用户工作台理想态

面向用户的 MAG 工作台应优先呈现申请任务本身，而不是 runtime 内部细节。

理想视图包括：

- `Status`：当前 grant line、target funder、stage、owner、freshness、blocker 和 next action。
- `Workspace`：输入材料、call/profile、draft 状态、evidence gaps、TODO 和显式唤醒。
- `Quality`：scorecard、closure dossier、issue lineage、AI reviewer status 和 unresolved hard issues。
- `Artifacts`：draft、review packet、revision packet、final package、export receipts 和 gap report。
- `Memory`：consumed strategy refs、writeback proposal、accept/reject receipt 和 provenance。
- `Attention Queue`：需要用户确认、需要材料补件、需要重新评审、需要 OPL repair 或等待 provider 的事项。
- `Operator Drilldown`：receipt、source refs、repair command、stage handoff 和 owner boundary。

App 可以触发 OPL framework action、MAG guarded dispatch 或 direct domain entry；ready verdict、quality verdict、fundability verdict 和 export verdict 都必须回到 MAG-owned surface。

## 标准 Repo Skeleton 理想态

MAG 作为 OPL-compatible Foundry Agent package，理想 repo-source skeleton 应保持清晰边界：

```text
med-autogrant/
  agent/
    stages/
    prompts/
    skills/
    knowledge/
    quality_gates/
  contracts/
    runtime-program/
    domain descriptors
    receipt schemas
    artifact locator contracts
  runtime/
    authority_functions/
    native_helpers/
    receipt_evidence_writers/
  src/
    med_autogrant/
  schemas/
  tests/
  docs/
    project.md
    status.md
    architecture.md
    invariants.md
    decisions.md
```

该 skeleton 是发现、验证、托管和审计边界。`runtime/authority_functions` 只放无法声明化的 fundability / quality / export verdict、package authority、memory accept/reject、owner receipt signer 或 grant-native helper；sidecar、projection builder、lifecycle adapter、status wrapper 和 product shell 长期由 OPL 生成或托管。内部实现可以继续按 Python package 和现有模块组织，只要外部 descriptor、contract、policy、authority manifest 和 tests 保持稳定。

## 理想完成门槛

MAG 达到理想生产级状态时，应满足以下门槛：

- Direct app skill path 与 OPL-hosted path 都回到同一套 MAG route truth、workspace truth、quality gate 和 export gate。
- 每个 stage attempt 都有 typed closeout、owner receipt、typed blocker、human gate receipt 或 no-regression evidence。
- 真实 OPL-hosted controlled grant-stage attempt 能返回 MAG domain owner receipt、typed blocker 或 no-regression evidence，并能被 OPL workbench refs-only 展示。
- Receipt reconciliation proof / inventory 必须能从 repo-local probe 推进到真实 OPL-hosted grant-stage line 的持续对账，但不能把 no-regression evidence 或 typed blocker 写成 grant quality verdict，也不能把 read projection 写成 runtime receipt instance。
- Domain memory 检索、writeback proposal、MAG accept/reject、runtime receipt evidence 和 operator projection 在真实 workspace/runtime root 中可运行。
- `package submission-ready` 对 frozen workspace fail-closed，并明确区分本地提交包与外部 portal submission。
- AI-first quality gate 在没有 active critique 时保持 projection-only，在有 AI-authored review 时输出可追溯 closure dossier。
- OPL/App 只消费 refs、receipt、freshness、locator 和 projection；grant truth、fundability、quality verdict 和 export authority 留在 MAG。
- MAG repo 内仍保留的非知识代码均能归类为 authority function 或迁移桥；每项都有 active caller、cannot-absorb reason、receipt/schema 边界和 OPL generated/replacement expectation。能由 OPL pack compiler 生成的 CLI/product-entry/sidecar/status/projection/harness 不再作为 MAG 长期私有实现扩展。
- Repo source 不写入真实 runtime artifacts、private evidence、receipt instance、memory body 或 export package。
- 旧 local host-agent runtime、Gateway/local-manager、Hermes-first 默认路径和旧 product-status traces 保持 history/provenance/explicit proof 语境，不回到 active path。

## 当前使用方式

本文适合用于规划 MAG 下一阶段 production closure、设计 MAG App/OPL workbench、评估新 grant family 接入、判断 shared module 上收范围，以及审阅 future hosted/runtime work 是否越过 MAG owner boundary。

实际实施时按当前状态递进：

- 当前 truth 读核心五件套和 `current-program.json`。
- OPL family adoption 读 `docs/references/opl_family_contract_adoption.md`。
- Grant strategy memory 读 `docs/references/grant_strategy_memory_policy.md`。
- 机器接口写入 `contracts/`、`schemas/`、源码、CLI/API 行为或 MAG-owned manifest。
- 目标态和 north-star 讨论可以引用本文，但不得把本文当作已落地证明。
