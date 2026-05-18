# 架构概览

## 主链路

当前主链路是“单一 app skill 优先，稳定 capability surface 仍由 CLI / domain entry 承载，OPL 托管或 hosted backend 显式可选”：

`operator / Codex / OPL / generic agent caller -> single Med Auto Grant app skill -> CLI or MedAutoGrantDomainEntry -> route-selected executor -> MedAutoGrant domain logic -> critique / export / stage surfaces -> durable artifacts`

在 OPL stage-led agent runtime framework 中，这条链路可以被 OPL 托管为 stage attempt；Agent executor 是 stage 内最小执行单位，`Codex CLI` 是当前第一公民 executor，除非活跃合同显式选择其他 provider。OPL 可以提供 stage lifecycle、queue/wakeup、handoff、receipt、approval/retry、trace/projection、shared contracts/indexes 与外部 provider 编排，但不会改变 MAG 的 owner 边界：MAG 持有 grant route truth、fundability / authoring quality判断、workspace truth、artifact assembly 和 submission-ready export gate。

formal-entry matrix 继续固定为：`CLI` 是 formal entry，`MCP` 是 supported protocol layer，`controller` 是 internal surface。

当前任务语义固定为“指定基金任务正文 authoring”。架构层显式区分两类完成态：科学完成可待审包，以及形式/客观补件完成。

如果显式启用 hosted runtime carrier，它也只能挂在同一套 `CLI / MedAutoGrantDomainEntry / route contract / export contract` 下面；`Hermes-Agent` 和 `Claude Code` 相关路径当前属于 OPL generic Agent Executor Adapter 的显式 opt-in backend，而不是默认公开 capability contract 或公开第一入口。

## 入口 taxonomy 与 OPL handoff

当前需要明确区分三层入口：

- `operator entry`
  - 给人类操作同事使用的命令、workspace 准备、检查与显式 gate
- `agent entry`
  - 给 `Codex`、Claude Code、OpenClaw 等通用 agent host 使用的 `CLI` / `MedAutoGrantDomainEntry`
- `product entry`
  - 给单一 app skill 使用的内部产品入口 shell

当前真实状态是：前两层已经存在，第三层的轻量结构化 shell 与第一棒 read-only product projection 也已经 landed，但它们仍是 app skill 下的内部 command contract；成熟用户级前台仍未落地。
stage-led framework / domain harness 在这里继续作为内部架构分层术语，不作为对外第一身份。

在进入 repo-tracked workspace 之前，仍保留 pre-workspace intake 入口作为可选辅助：

`selection_input materials -> select-project-profile -> initialize-intake-workspace -> input_intake workspace directory / workspace.json`

在这层之前，也保留 funding discovery 作为可选辅助：

`discovery_input materials -> discover-funding-opportunities -> funding_opportunity_pool -> select-project-profile`

当前 `discover-funding-opportunities` 有两种 source mode：

- `catalog_static`
  使用 repo 内冻结 catalog，保证离线稳定与测试可重复。
- `official_live`
  直接读取官方页面并即时形成候选池。当前接入的官方入口是：
  - NIH Parent Announcements: [grants.nih.gov/funding/explore-nih-opportunities/parent-announcements](https://grants.nih.gov/funding/explore-nih-opportunities/parent-announcements)
  - NSFC 项目指南列表: [nsfc.gov.cn/p1/3381/2824/zntg.html](https://www.nsfc.gov.cn/p1/3381/2824/zntg.html)
  - NSFC 医学科学部指南页: [nsfc.gov.cn/p1/2931/3971/3975/3991/yxkxb22222.html](https://www.nsfc.gov.cn/p1/2931/3971/3975/3991/yxkxb22222.html)
- `official_cached`
  读取 machine-local funding cache，而不是再次访问网络。缓存通过 `refresh-funding-opportunities-cache` 刷新，默认落点是 `$CODEX_HOME/projects/med-autogrant/runtime-state/funding-landscape/cache/latest.json`。
  refresh 同时会写出同目录的 `latest.diff.json`，用于对比本轮和上一轮 cache。

这层入口的职责是：

- 作为 pre-authoring 准备工具，为 caller 提供可复用材料池、profile 与 funding 线索
- 输出可落到 `input_intake -> ... -> frozen` 主线的 workspace 真相
- 在任务已锁定指定基金后，不再作为默认阻塞链路触发跨 funder 重选

目标中的 domain 级链路应是：

`User or agent caller -> Med Auto Grant Product Entry -> MedAutoGrantDomainEntry -> route-selected executor or optional hosted runtime carrier -> Med Auto Grant domain logic`

与 `OPL` 的家族级衔接应是：

`User or agent caller -> OPL Product Entry -> OPL stage-led runtime framework -> MAG product-entry/runtime-control/sidecar projection -> Domain Handoff -> Med Auto Grant Product Entry / MedAutoGrantDomainEntry`

`OPL -> Med Auto Grant` 的最小 handoff envelope 至少包括：

- `target_domain_id`
- `task_intent`
- `entry_mode`
- `workspace_locator`
- `runtime_session_contract`
- `return_surface_contract`

在这层公共 envelope 之上，grant 域继续补充 `workspace_id`、`draft_id`、`funding_call` 等 domain payload。

按当前定位，这条链路的 owner 固定为：

- `OPL`：stage-led agent runtime framework owner，负责 family-level session/runtime/projection、stage attempt lifecycle、queue/wakeup/handoff/receipt、shared modules/contracts/indexes 与外部 provider 编排
- `Codex CLI`：当前第一公民 Agent executor，承担未显式切换 provider 时的具体 stage attempt 执行
- `Med Auto Grant App Skill`：domain direct entry owner
- `OPL family runtime provider`：OPL production online runtime 使用 Temporal-backed provider 作为必需 substrate；Hermes-Agent / Claude Code 当前只作为显式 executor adapter backend 接入，local provider 只用于 dev/CI/offline diagnostics
- `Med Auto Grant`：author-side grant truth / route / export owner

当前并不宣称 `OPL` family orchestration surface 已在本仓实现；当前只是在为 future caller 冻结稳定 contract。
MAG 侧当前实现的是 product sidecar adapter，而不是长期常驻 sidecar daemon。`product sidecar export --input <workspace.json> --format json` 导出 runtime_control、runtime_continuity、TODO/explicit wakeup、autonomy-controller、domain-memory、owner receipt、lifecycle receipt 与 user-loop attention queue；`product sidecar dispatch --task <task.json> --format json` 只允许 MAG-owned guarded actions：`status/read`、`user-loop/wakeup`、`autonomy-controller/dry-run`、`autonomy-controller/guarded-run`、`domain-memory/propose`、`domain-memory/decide`、`stage-attempt/closeout`、`lifecycle/receipt` 与 `notification/receipt`。
`product-entry-manifest.mag_consumer_thinning_contract` 是当前 MAG 侧 consumer/thinning 机器合同。它只声明 MAG 输出 grant-owned refs、owner receipt、typed blocker、verdict refs 与 domain action metadata；workspace/source intake shell、memory locator/writeback transport、package/export lifecycle shell、generic transition runner、operator workbench/observability/SLO 和 agent scaffold checklist 都是 OPL replacement expectation。该合同不会在 MAG 内实现 generic scheduler、queue、attempt ledger、runner 或 App workbench，也不声明 OPL replacement 已存在。
Codex App direct skill 调用与 OPL 托管调用必须在 `MedAutoGrantDomainEntry` / product-entry command contract 后收敛；OPL stage metadata 不能成为第二 route truth、第二 quality owner 或第二 export authority。

## OPL family orchestration contracts（adoption 方向）

`OPL` 在 family-level 继续冻结 5 类 contracts：

- family event envelope
- family checkpoint lineage
- family action graph
- family human gate
- family product-entry manifest v2
- OPL stage-led runtime registration/projection envelope

对 `Med Auto Grant` 来说，优先 adoption 的面是 `workspace progress / workspace cockpit / product direct-entry / product user-loop`，并与 family action graph / family human gate / family product-entry manifest v2 对齐；这些面仍属于 app skill 下的内部 command contract，domain 侧继续保持 `workspace / draft / program` 的真相边界。
`family_action_catalog` 是 MAG-owned callable action metadata 单一声明面；repo-root OPL standard pack 把它与 stage、memory、artifact、receipt 和私有功能审计一起声明为 OPL pack compiler 输入。`OPL` 从该 pack 生成统一 CLI / MCP / Skill / product-entry / tool descriptor bundle，MAG 现有 CLI、`MedAutoGrantDomainEntry`、product-entry/user-loop、sidecar 和 schema-backed scripts/contracts 作为 generated descriptors 指向的 action target / authority function。当前 MAG 只声明 MCP descriptor/protocol-layer projection，`descriptor_only=true`、`public_runtime=false`；`OPL` 只读取该 pack/catalog 做 family-level discovery/export/parity，不持有 grant truth、fundability judgement 或 submission-ready export gate。
`family_stage_control_plane` 同样从 `product-entry-manifest` 暴露，但它只是一组 MAG-owned stage descriptors：每个 stage 都必须携带 stage goal、owner、skills、`allowed_action_refs`、handoff、source refs、freshness 与 authority boundary。构建时会把 `allowed_action_refs` 校验到 `family_action_catalog`，从而让 `OPL` 的 discovery smoke 读取同一份 action truth；MAG 继续持有 grant truth、fundability judgment 与 submission-ready export gate。
`controlled_domain_memory_apply_proof` 聚合 consumed grant strategy memory refs、writeback proposal、MAG accept/reject decision、runtime receipt evidence projection、operator receipt projection 与 repo-source layout audit。它是 controlled grant-stage memory apply 的 proof surface：真实 receipt instance 只写到 workspace/runtime root，不写 repo source；真实 memory body、fundability verdict、authoring quality verdict、submission-ready export verdict 和 grant artifact 仍被禁止进入 repo source。
`mag_consumer_thinning_contract` 进一步把 OPL handoff boundary 机器化：MAG sidecar/direct path 保持 thin adapter，OPL 才是 generic primitive replacement owner。MAG 当前可交付的是合同、refs、receipt writer、typed blocker、no-forbidden-write guard、focused hosted receipt verification、lifecycle receipt bundle、memory receipt read projection、package lifecycle handoff projection、continuous receipt reconciliation snapshot 和 `external_evidence_request_pack`；真实 OPL replacement production consumption、workspace memory body migration、package/lifecycle workspace receipt 泛化和 live soak 是后续 evidence gate。`external_evidence_request_pack` 只列 request ids、required refs、required receipt shapes、forbidden payload classes 和 authority boundary，不在 MAG 内实现 OPL runtime、App workbench、generic runner 或 production caller。

`mag_consumer_thinning_contract.privatized_functional_module_audit` 是当前 OPL 统一审计读取的功能私有化 closeout 面。它把旧 replacement / tombstone 口径收敛为四类：runtime registration、task lifecycle、source intake 归到 `declarative_pack_surface`；lifecycle adapter、observability、sidecar/product status、package lifecycle、人用 workbench / scheduler / daemon 归到 `refs_only_adapter`；grant lifecycle stage、fundability / quality / export verdict、package readiness / submission-ready、grant transition oracle、owner receipt 和 grant strategy memory accept/reject 归到 `minimal_authority_function`；旧 Hermes/Gateway/local-manager、local journal / attempt ledger、patch bridge、compat aggregate test、legacy shell alias 和 repo-owned scheduler/daemon 归到 `legacy_proof_tombstone`。这个审计面用于防止误读：MAG 可以提供 declarative pack 和 refs-only adapter，但不能长期私有化通用 runtime；同时不能删除或外包 grant lifecycle、package readiness、fundability、quality、export verdict 或 owner receipt。

该 audit item 现在同时列出代码路径、活跃调用者、调用状态、迁移动作、保留理由和不能上收原因。架构读法是：MAG 当前仍有本地 journal / attempt ledger、controller/loop、workspace/source validation、memory/package/status/sidecar/CLI wrapper 与 optional `Hermes-Agent` proof state-db 相关代码；其中旧 local journal / attempt ledger 与 Hermes/Gateway/local-manager 只能作为 no-active-caller proof/tombstone 或 regression oracle 读取，不能作为 MAG-owned runtime owner 续命。OPL 应生成或托管通用 ledger、queue、lifecycle、source intake、artifact/package lifecycle、observability、workbench、scheduler/daemon 和 generic runner；MAG 不能外包 grant truth、memory body、fundability/quality/export verdict、submission-ready package authority、grant transition oracle 或 owner receipt。

这轮对齐不引入 `CrewAI` 依赖，也不把 OPL runtime framework 写成 MAG runtime owner，更不宣称已完成跨仓 runtime core ingest。当前真实状态是 MAG 作为独立 domain agent 维持 family-level contract-first 对齐与 domain-owned truth；OPL 统一 Agent Executor Adapter 的 MAG 边界已经落地，若启用 `Hermes-Agent` 或 `Claude Code`，它也只是显式 opt-in executor backend，要求 receipt/audit/fail-closed，不是默认公开入口。MAG-owned memory、owner/no-regression 与 lifecycle receipt evidence path 已可写 runtime receipt instance；剩余缺口是 OPL-hosted controlled grant stage attempt 在 OPL ledger 与 MAG runtime receipt instance 之间完成真实对账和 live soak。

## OPL Provider、Med Auto Grant 与 concrete executor 的分工

在当前架构里，OPL stage-led runtime framework 和它选定的 provider 可以承担：

- session substrate
- runtime state / attempt ledger durability
- interrupt / resume / scheduling 这类长期在线 runtime 能力
- sidecar dispatch 的在线唤醒 carrier
- stage-led queue、handoff、receipt、retry/dead-letter 与 operator projection

provider 选择由 OPL 框架显式声明；生产在线路径要求 Temporal-backed provider ready。Hermes-first 口径只作为 provider-specific 或迁移记录保留。

`Med Auto Grant` 自己继续承担：

- workspace / draft / critique / revision / export 的 domain truth
- author-side object model 与 identity guard
- stage routing、artifact assembly 与 hosted handoff contract

当前 route-selected concrete executor 继续承担：

- 具体 authoring pass 的执行
- 由 route / executor adapter 选中的单步运行时
- 当前默认 `Codex CLI` 执行器，默认模式是 `autonomous`；OPL 持有 generic Agent Executor Adapter / registry
- `hermes_agent` / `claude_code` 是显式 opt-in backend；当前 MAG critique route 对 `hermes_agent` 产出 OPL `AgentExecutionReceipt` 风格 proof，sidecar dispatch 不会把它设为默认

因此，这里真实成立的是：

- 默认公开 capability contract 先固定在 `CLI` / `MedAutoGrantDomainEntry` / 本地脚本 / schema-backed contract / product sidecar adapter
- domain governance / truth owner 仍是 `Med Auto Grant`
- concrete executor owner 仍按 route 单独选择，当前默认是 `Codex CLI`

这不等于“所有单步 authoring 都已经迁成 Hermes-native executor”。
如果未来某条 critique / revision / export route 要替换执行器，也必须按 route 单独冻结 truth 与 proof，而不是因为 substrate 已统一就自动把 authoring semantics 一起改掉。

## 入口与执行

- CLI 仍是唯一 formal entry：`workspace validate`、`workspace summarize`、`workspace intake-audit`、`workspace evidence-grounding`、`workspace quality-scorecard`、`workspace quality-diff`、`workspace next-step`、`workspace critique-summary`、`workspace route-report`、`mainline status`、`mainline phase`、`workspace progress`、`workspace cockpit`、`product direct-entry`、`product user-loop`，以及 `pass direction-screening`、`pass question-refinement`、`pass argument-building`、`pass fit-alignment`、`pass outline`、`pass drafting`、`pass critique`、`pass critique-loop`、`pass mainline-loop`、`pass autonomy-controller`、`pass revision`、`pass freeze`、`package artifact-bundle`、`package final-package`、`package hosted-contract-bundle`、`package submission-ready`。
- `src/med_autogrant/domain_entry.py` 现在提供结构化 `MedAutoGrantDomainEntry`，把 CLI 与 future framework caller 收口到同一条 service-safe command contract。
- `src/med_autogrant/product_entry.py` 现在提供 `MedAutoGrantProductEntry`；`product build-entry` 通过 `MedAutoGrantDomainEntry` 复用已 landed 的 route / summary / runtime contract，统一生成 `direct` 与 `opl-handoff` 共用的 shared envelope，并显式导出 `executor_routing_contract`。
- `MedAutoGrantProductEntry` 现在还提供 `workspace progress` 与 `workspace cockpit`：它们是 controller-owned、read-only 的 product projection，复用 `workspace summarize`、`workspace route-report`、`workspace critique-summary` 与 `product build-entry` contract 信息，并分别受 `schemas/v1/grant-progress.schema.json` 与 `schemas/v1/grant-cockpit.schema.json` 约束、在生成时 fail-closed，但故意不进入 `domain_entry_contract.supported_commands` 或 hosted contract bundle 的 command catalog。
- `MedAutoGrantProductEntry` 现在还提供 MAG-owned production functional closure projection：`product domain-memory-proposal` 生成 writeback proposal envelope，`product domain-memory-decision` 生成 accept/reject decision 与 operator receipt projection，`product domain-memory-receipt-evidence` 把 MAG decision 写成 runtime receipt evidence instance；`product-entry-manifest` 额外暴露 `owner_receipt_contract`、`controlled_domain_memory_apply_proof`、`lifecycle_guarded_apply_proof`、`physical_skeleton_follow_through` 与 `repo_source_layout_audit`。这些面只投影 runtime/writeback refs、owner receipt refs、lifecycle typed blockers 和 repo-source audit，不把真实 memory entry、grant artifact 或 receipt instance 写入 repo。
- `MedAutoGrantProductEntry` 现在还提供 MAG-owned refs-only handoff surfaces：`product hosted-receipt-verification`、`product lifecycle-receipt-bundle`、`product memory-receipt-projection`、`product package-lifecycle-handoff` 与 `product continuous-receipt-reconciliation`。它们用于让 OPL shell/read model 消费 MAG receipt refs、memory refs、package/export verdict refs、manual portal boundary、typed blocker 和 reconciliation counts；它们不实现 OPL memory transport、package/artifact lifecycle shell、generic runner、attempt ledger、repair/workbench 或 live reconciliation daemon，也不产生 fundability-ready、quality-ready、export-ready 或 production soak verdict。
- `product-entry-manifest.mag_consumer_thinning_contract.external_evidence_request_pack` 是剩余 OPL/App/production 证据门的请求面：它要求外部 caller 返回 generated/hosted caller consumption、workbench refs consumption、release/dist consumption、owner receipt / typed blocker roundtrip、no-forbidden-write、direct/hosted parity 和 long-soak receipt reconciliation evidence。该面所有 request 当前都是 `requested_not_received`，不能作为 production consumption 或 long-run soak 成功证明。
- `MedAutoGrantProductEntry` 现在还提供 `product direct-entry`：它会把 `workspace progress`、`workspace cockpit` 与 direct / `opl-handoff` 两份 `product_entry` envelope 收成一份 controller-owned 的 direct-entry composition，并受 `schemas/v1/grant-direct-entry.schema.json` 约束、在生成时 fail-closed；它同样不进入 `domain_entry_contract.supported_commands` 或 hosted contract bundle 的 command catalog。
- `mainline status` 现在把 `current-program` 里的 current line、current focus、completed records 与 remaining gaps 投影成 repo 级 controller surface；`mainline phase` 继续保留为维护者参考记录查询；`product user-loop` 则把这份 mainline snapshot、`product direct-entry` 与 route-derived next action 收成当前 inbox-like user loop，并受 `schemas/v1/grant-user-loop.schema.json` 约束、在生成时 fail-closed；它同样不进入 `domain_entry_contract.supported_commands` 或 hosted contract bundle 的 command catalog。
- `product manifest` 与 `product status` 现在也由 `MedAutoGrantProductEntry` 输出为 MAG domain handler / refs-only contract，并分别受 `schemas/v1/product-entry-manifest.schema.json` 与 `schemas/v1/product-status.schema.json` 约束、在生成时 fail-closed；它们的 target caller 是 OPL generated/hosted status surface，但当前 active caller 仍是 MAG handler，外部 caller evidence 与 live soak 不由本仓声明。
- `product build-entry.product_entry` 与 route-selected executor contract 现在都已经收口成 schema-backed contract：前者对应 `schemas/v1/product-entry.schema.json`，后者对应 `schemas/v1/executor-routing-contract.schema.json`，并且两者都会在生成时 fail-closed；退役的 `runtime run / runtime resume` public CLI 不再作为当前 executor routing evidence。
- `product build-entry.product_entry.return_surface_contract.domain_entry_contract` 现在会与 hosted bundle 共享同一份 command catalog，并显式固定 `supported_commands` 与每个 command 的 `command_contracts`。
- `src/med_autogrant/upstream_hermes.py` 只保留为显式 proof / provenance / diagnostic 依赖探测与历史 state-db 参考，不是 MAG 当前 public runtime owner。
- 旧 `runtime run` 与 `runtime resume` journal 串联语义已从 MAG public CLI、domain-entry catalog、product-entry session continuity 和 hosted bundle 中退役；session/resume 改由 OPL generated surface refs 与 MAG owner receipt / typed blocker refs 表达。
- 对 valid workspace，Hermes session handle 继续沿用 `grant_run_id`；对 `validation_failed` path，只允许使用 journal-scoped substrate session handle 持续 durability，不得伪造新的 domain `grant_run_id`。
- `src/med_autogrant/domain_runtime.py` 现在应被理解为 repo-side domain adapter / orchestrator，而不是 runtime substrate owner。
- OPL stage-led runtime framework 只消费 `runtime_control.semantic_closure`、`skill_catalog.domain_projection.runtime_continuity`、`workspace progress / cockpit`、hosted contract bundle 与 artifact/wakeup locator；高频索引可由 OPL Rust native helper 执行，并通过 `native_helper_consumption.proof_surface` 固定 workspace/session/artifact/TODO-wakeup/runtime-health coverage 与 `opl_index_only` 写入边界，但它不写 MAG authoring truth，也不替代 route-selected executor。
- `runtime run` / `runtime resume` 不再作为 MAG public direct runtime loop。仍保留的 domain runtime code 只可作为 domain handler、regression oracle、diagnostic/provenance 或 explicit proof lane 读取，不得重新写成 MAG-owned generic runtime surface。
- `pass direction-screening`、`pass question-refinement`、`pass argument-building`、`pass fit-alignment`、`pass outline`、`pass drafting`、`pass critique`、`pass revision`、`pass freeze`、`package artifact-bundle`、`package final-package`、`package hosted-contract-bundle`、`package submission-ready` 继续由 repo-side domain logic 持有输入加载、identity guard 与输出 handoff。
- `select-project-profile` 与 `initialize-intake-workspace` 由 repo-side selector/initializer contract 持有材料池解析、profile/funding 匹配与 input-intake workspace 生成；新建 workspace 默认是目录型 scaffold，`workspace.json` 是 canonical document，workspace-local Git boundary 来自 `OPL` shared helper；在任务已锁定指定基金后，它们只作为显式唤醒的准备工具。
- `discover-funding-opportunities` 由 repo-side funding landscape discovery contract 持有显式 catalog、机器可读过滤规则与候选池输出；默认不进入已锁定任务的正文 authoring gate。
- `refresh-funding-opportunities-cache` 由 repo-side funding sync contract 持有官方来源抓取、按 source 增量刷新、cache snapshot 写入与 provenance 证据保留；它服务候选池维护，不直接定义正文完成态。
- `funding_landscape_diff_report` 则承担 refresh 前后差异、`withdrawn_or_not_listed` 检测与变化摘要。
- `pass critique` 当前默认走 `Codex CLI` 的 `autonomous` 模式：具体由 `critique_executor.py -> run_codex_exec(...)` 调起 `codex exec`，默认 `model / reasoning` 都继承本机 Codex 默认（`inherit_local_codex_default`），只有显式环境变量覆盖才会传 override。
- `execute-critique-revision-loop` 在现有 `execute-critique-pass` 与 `execute-revision-pass` 之上复用同一份 route truth；它不会改写单步 pass 语义，只负责多轮闭环调度、每轮产物落盘与 stop condition 汇总。
- `execute-authoring-mainline-loop` 在 `determine_next_step(...)` 与单步 pass builder 之上进一步向上扩，把 rollback 到 `direction_screening / question_refinement / argument_building / fit_alignment` 的重建也纳入同一条自治调度线。
- `grant-quality-scorecard` 与 `grant-quality-diff` 在 intake/evidence/critique truth 之上形成质量治理层，并把质量 gate 注入 `execute-authoring-mainline-loop` 的 route resolver，作为 stop / continue / rollback 的依据之一。scorecard / closure dossier 本身不持有 grant reviewer 判断；它们只能在 active critique 明确来自 `Codex CLI critique executor` 或带 OPL receipt 的 `Hermes-Agent` critique executor 时把结构化分数聚合为 candidate 质量状态，否则只能输出 projection-only / AI reviewer required。
- `pass revision` 继续是机械 apply 层，只能应用 AI-authored `revision_plan.items[].mutation_payload`；它不得自行生成 replacement prose，也不得用 fallback prose 补正文。
- `execute-grant-autonomy-controller` 位于已有 discovery / selector / initializer / mainline loop / quality surface 之上，负责预算、轮次、blocker 队列、evidence gap 队列、同一基金任务内的 rollback/continue 决策记录与 fail-closed 报告，不替代下游单步 pass。
- 同一条 `pass critique` 现在也支持显式 `executor_kind=hermes_agent`：这条 receipt lane 会通过 OPL `executor run` 进入 `one-person-lab` 持有的 Agent Executor Adapter；MAG 只提供 OPL 可调用的 domain closeout helper，并消费 OPL `AgentExecutionReceipt` 与 `mag_critique_closeout_packet`。helper 内部会读取本机 `~/.hermes/config.yaml` 的 model/provider/base_url/api_mode/reasoning_effort 并调用上游 Hermes full agent loop；只有在完成整轮 loop、拿到真实工具事件、合法 domain closeout 和 OPL receipt 时才通过，否则 fail-closed。
- `package hosted-contract-bundle` 继续把 `runtime_substrate_contract`、`runtime_state_contract` 与 `operator_contract` 一并导出，并额外显式导出 `domain_entry_contract`、`schema_contract`、`authoring_contract`，形成 future host / `OPL` caller 可直接消费的 integration/reference contract catalog。
- `package submission-ready` 继续复用 `artifact_bundle -> final_package -> hosted_contract_bundle` 这条导出链，并维持完整材料下的严格 fail-closed 本地导出 gate；它与“科学完成可待审包”的 authoring stop 语义分层存在，不替代外部官网提交，也不定义补件 TODO 队列本身。
- 当前 external caller 只需要读取 `domain_entry_contract.supported_commands` 与 `domain_entry_contract.command_contracts`，就能按统一 contract 构造 request，而不需要 repo-local helper。
- 当前 direct-product projection caller 则可以读取 `workspace progress / workspace cockpit` 的只读投影结果，先看当前 grant 主线、blocker 与 direct / `OPL` entry command catalog，再决定是否进入真正的 domain entry / product entry 调用。
- `package hosted-contract-bundle.hosted_contract_bundle` 现在也受 `schemas/v1/hosted-contract-bundle.schema.json` 约束，并在写出前执行 schema + 冻结 truth 的 fail-closed 校验；它保持 integration/reference 角色，不改写公开第一入口。
- 当前 author-side executor routing 继续按 route 单独冻结：`direction_screening / question_refinement / argument_building / fit_alignment / outline / drafting / critique / revision / frozen / artifact_bundle / final_package / hosted_contract_bundle` 现在都已经有 landed service-safe command surface，并共享同一份 route catalog truth。
- `product-status.schema.json` 继续只承担历史兼容与旧真相追溯角色；当前 schema contract 与 route output 都已经收口为 landed route catalog。
- `workspace critique-summary` 继续只在 source workspace 已经位于 `critique / revision / frozen` review context 时作为 review-context audit surface 有意义；当前 full landed authoring catalog 不再依赖 pending handoff contract 才能进入 `critique`。
- 这里的 `critique` landed 只表示当前第一公民 concrete executor 已统一到 `codex_cli` / `Codex CLI`，默认模式是 `autonomous`；现在虽然已经有一条 `hermes_agent` explicit receipt lane，但它只证明 connectivity / lifecycle / receipt / audit 能成立，chat relay 不算，且不证明 provider 侧 reasoning 语义或结果质量等价于 Codex CLI。
- 产物面：`package artifact-bundle`、`pass revision`、`package final-package`、`package hosted-contract-bundle`、`package submission-ready`。

## 数据与对象模型

- `schemas/v1/nsfc-workspace.schema.json` 定义 workspace 结构与关键对象。
- `schemas/v1/project-profile-selection-input.schema.json` 与 `schemas/v1/project-profile-selection.schema.json` 定义 pre-workspace profile selection 输入/输出。
- `schemas/v1/funding-landscape-discovery-input.schema.json` 与 `schemas/v1/funding-landscape-discovery.schema.json` 定义 funding discovery 输入/输出。
- `schemas/v1/critique-loop-report.schema.json` 定义多轮 critique/revision loop 的报告面。
- `schemas/v1/authoring-mainline-loop-report.schema.json` 定义跨 rollback 重建的 mainline loop 报告面。
- `schemas/v1/grant-quality-scorecard.schema.json` 与 `schemas/v1/grant-quality-diff.schema.json` 定义质量治理与版本比较报告面。
- `schemas/v1/grant-autonomy-controller-input.schema.json` 与 `schemas/v1/grant-autonomy-controller-report.schema.json` 定义长期自治 controller 的请求与 fail-closed 报告面。
- `schemas/v1/service-safe-domain-surface.schema.json`、`schemas/v1/executor-routing-contract.schema.json`、`schemas/v1/product-entry.schema.json`、`schemas/v1/product-entry-manifest.schema.json`、`schemas/v1/product-status.schema.json`、`schemas/v1/grant-progress.schema.json`、`schemas/v1/grant-cockpit.schema.json`、`schemas/v1/grant-direct-entry.schema.json`、`schemas/v1/grant-user-loop.schema.json`、`schemas/v1/hosted-contract-bundle.schema.json` 与 `schemas/v1/submission-ready-package.schema.json` 定义当前 product entry / product entry discovery / landed route catalog / direct projection / direct-entry composition / direct user loop / hosted bundle / local submission-ready delivery / service-safe surface 的 schema-backed contract。
- `grant_run_id` 仅作为执行句柄；`workspace_id`、`draft_id`、`program_id` 保持边界分离。
- `workspace.py`、`stage_router.py`、`revision_executor.py`、`final_package.py` 等继续承载 MedAutoGrant 的 author-side domain logic；它们不应被未来的上游 substrate 目标或当前 repo-local helper 偷换成新的 authoring semantics。

## 控制面与报告

- `contracts/runtime-program/current-program.json` 是 repo-tracked current-program pointer。
- 机器本地 runtime state 统一下沉到 `$CODEX_HOME/projects/med-autogrant/runtime-state/`，用于 session / log / report / prompt 等非仓库真相面状态。
- `workspace progress / workspace cockpit` 当前属于 controller-owned / read-only product projection；它们不替代 durable truth surface，也不构成新的 service-safe domain entry contract，并且不会被镜像进 hosted contract bundle 的 command catalog。
- `workspace quality-scorecard / workspace quality-diff` 当前属于正式 domain entry audit surface，并会进入 hosted contract bundle 的 command catalog 与 schema contract。
- `pass autonomy-controller` 当前属于 formal CLI/domain-entry command surface；它输出 controller-owned report，不改变 `controller` 仍为 internal surface 的 formal-entry matrix。
- `product direct-entry` 当前属于 controller-owned 的 direct-entry composition；它不会改写 route owner，也不会被镜像进 hosted contract bundle 的 command catalog。
- `product user-loop` 当前属于 controller-owned 的 user-loop composition；它不会改写 route owner，也不会被镜像进 hosted contract bundle 的 command catalog。
- 人工 gate 当前只覆盖同一基金任务内的作者决策，不把 gate 语义扩展成跨 funder 的重新选题/重选项目流程。
- 形式/客观补件默认是 `TODO + 显式唤醒` 队列项；默认不阻塞正文 authoring 主线。
- 历史 `runtime run / runtime resume` journal 默认落点 `$CODEX_HOME/projects/med-autogrant/runtime-state/sessions/<grant_run_id>.json` 只作为 legacy/provenance 说明；当前 public surface 不再依赖本地 journal 作为 session owner。
- Hermes substrate state db 只在显式 proof lane 使用，默认不要求安装上游 `hermes-agent`；如需显式隔离，可通过 `MED_AUTOGRANT_HERMES_HOME` 覆盖。
- 历史 local host-agent runtime 只保留在归档与 provenance 材料里，不再作为长期产品 runtime owner。

## 文档层次

- Public surface：`README*`、`docs/README*`、`docs/domain-positioning*`、`docs/mvp-scope*`。
- 核心骨架：`docs/project.md`、`docs/architecture.md`、`docs/invariants.md`、`docs/decisions.md`、`docs/status.md`。
- Repo-tracked current truth：核心五件套、`contracts/runtime-program/current-program.json`，以及 `docs/specs/README*` 中列出的 active specs。
- 活跃规划：`docs/active/**`；历史计划与 dated specs 入口：`docs/history/**`。

## 历史边界

- OMX 已退场，仅保留历史入口。
