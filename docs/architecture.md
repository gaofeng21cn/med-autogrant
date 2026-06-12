# 架构概览

Owner: `Med Auto Grant`
Purpose: `architecture_and_owner_boundary`
State: `current`
Machine boundary: 本文是人读架构说明。机器接口与当前 truth surface 继续归 `contracts/`、schemas、source、CLI/API 行为、product-entry manifest、runtime receipts、workspace/artifact roots 与 `contracts/runtime-program/current-program.json`。

## 主链路

当前主链路是“单一 app skill 优先，稳定 capability surface 仍由 CLI / domain entry 承载，任务启动后的默认运行驻留交给 OPL/Temporal hosted autonomous runtime”：

`operator / Codex / OPL / generic agent caller -> single Med Auto Grant app skill -> CLI or MedAutoGrantDomainEntry -> route-selected executor -> MedAutoGrant domain logic -> critique / export / stage surfaces -> durable artifacts`

在 OPL Temporal-backed stage-led agent runtime framework 中，这条链路默认被 OPL 托管为 stage attempt；OPL 持有任务启动后的持久在线调度、queue/wakeup、handoff、receipt、approval/retry/dead-letter、resume、attempt ledger、trace/projection、shared contracts/indexes 与 provider 编排。Agent executor 是 stage 内最小执行单位，`Codex CLI` 是当前第一公民 executor，除非活跃合同显式选择非默认 executor/backend。该默认托管运行口径不会改变 MAG 的 owner 边界：MAG 持有 grant route truth、fundability / authoring quality判断、workspace truth、artifact assembly 和 submission-ready export gate。

formal-entry matrix 继续固定为：`CLI` 是 formal entry，`MCP` 是 supported protocol layer，`controller` 是 internal surface。

当前任务语义固定为“指定基金任务正文 authoring”。架构层显式区分两类完成态：科学完成可待审包，以及形式/客观补件完成。

`Hermes-Agent` 和 `Claude Code` 相关路径当前属于 OPL generic Agent Executor Adapter 的显式 opt-in backend，而不是默认公开 capability contract、公开第一入口或 MAG runtime owner。非默认 executor 也只能挂在同一套 `CLI / MedAutoGrantDomainEntry / route contract / export contract` 下面。

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

`User or agent caller -> OPL Product Entry -> OPL stage-led runtime framework -> MAG product-entry/runtime-control/domain-handler projection -> Domain Handoff -> Med Auto Grant Product Entry / MedAutoGrantDomainEntry`

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
MAG 侧当前实现的是 domain-handler target，而不是旧 product-sidecar wrapper 或长期常驻 daemon。`domain-handler export --input <workspace.json> --format json` 导出 runtime_control、runtime_continuity、TODO/explicit wakeup、autonomy-controller、domain-memory、owner receipt、lifecycle receipt 与 user-loop attention queue；输出 surface kind 是 `mag_product_domain_handler_export`。`domain-handler dispatch --task <task.json> --format json` 只允许 MAG-owned receipt / refs-only domain actions：`domain-memory/propose`、`domain-memory/decide`、`stage-attempt/closeout`、`lifecycle/receipt`、`closeout/codex-stage-receipts`、`closeout/operator-readiness`、`closeout/physical-morphology-guard` 与 `closeout/executor-first-bundle`；输出 surface kind 是 `mag_product_domain_handler_dispatch`。TODO/wakeup 只把 OPL typed queue 指向 `open_grant_user_loop` / user-loop 这个 MAG domain action target，不引入 status/read、notification/receipt 或 autonomy-controller 泛用 dispatch。autonomy-controller 的 domain authority 仍由 `MedAutoGrantDomainEntry` 与 CLI direct path 承载，不经旧 product-sidecar generic wrapper。
`product-entry-manifest.mag_consumer_thinning_contract` 是当前 MAG 侧 consumer/thinning 机器合同。它只声明 MAG 输出 grant-owned refs、owner receipt、typed blocker、verdict refs 与 domain action metadata；workspace/source intake shell、memory locator/writeback transport、package/export lifecycle shell、generic transition runner、operator workbench/observability/SLO 和 agent scaffold checklist 都是 OPL replacement expectation。该合同不会在 MAG 内实现 generic scheduler、queue、attempt ledger、runner 或 App workbench；physical-delete authority、App sustained consumption closeout 与 Temporal long-soak closeout 继续由 active gap plan、private inventory 和 machine gate 判定，不在架构文档复制删除门清单。
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
`family_action_catalog` 是 MAG-owned callable action metadata 单一声明面；repo-root OPL standard pack 把它与 `agent/` Declarative Grant Pack、stage、memory、artifact、receipt 和私有功能审计一起声明为 OPL pack compiler 输入。`OPL` 从该 pack 生成统一 CLI / MCP / Skill / product-entry / tool descriptor bundle，MAG 现有 CLI、`MedAutoGrantDomainEntry`、product-entry/user-loop、domain-handler 和 schema-backed scripts/contracts 作为 generated descriptors 指向的 action target / authority function。当前 MAG 只声明 MCP descriptor/protocol-layer projection，`descriptor_only=true`、`public_runtime=false`；`OPL` 只读取 pack/catalog 做 family-level discovery/export/parity，不持有 grant truth、fundability judgement 或 submission-ready export gate。
`agent/` 是 canonical repo-source semantic pack：`agent/prompts/` 持有六个 stage prompt，`agent/stages/` 持有 stage policy，`agent/skills/` 持有 domain skill declaration，`agent/quality_gates/` 持有 fundability、quality、export/package、memory/receipt 和 authority gate，`agent/knowledge/` 持有 grant strategy memory、package authority 和 owner receipt 知识边界。`src/` 是 domain handler、minimal authority function 和 native helper 层，不再作为 declarative stage semantics 的 canonical 位置。

OPL family `Foundry Agent OS` target delta 当前由 [MAG Foundry Agent OS 目标差异页](./active/foundry-agent-os-target-delta.md) 维护。架构读法是：`OPL Agent OS + Declarative Grant Pack + Grant Authority Kernel + Grant Capability Registry`。Capability Registry 由 OPL `Atlas + Pack + Stagecraft` 承载 catalog / ABI / use policy；MAG 只声明 grant-native capability refs 和 authority guard。默认 reader 必须回到 `current_owner_delta`，OPL generated surface、Vault、Console、Runway、Pack 或 Capability Registry 均不能签 MAG owner receipt、创建 MAG typed blocker 或授权 grant verdict。

`contracts/foundry-agent-os-domain-kernel-manifest.json` 是这条 owner split 的机器合同入口。它把 grant truth、fundability / quality / export / submission verdict、package authority、grant memory decision、owner receipt 与 typed blocker 固定为 MAG kernel，把 runtime、generated surfaces、workspace/source/package shell、projection、Vault lineage 和 capability ABI 固定为 OPL upcollect surface；架构与测试均不得从 OPL refs-only surface 推导 grant verdict。
`contracts/foundry_agent_series.json.series_design_profile` 把 MAG 外显为 MAS/RCA/OMA 同系列 Foundry Agent，且使用同一 canonical `opl_foundry_agent_series_design_profile.v1`：共同 lifecycle、generic input/output slots、stage pack sections、closeout shape 和 authority invariants 与 MAS/RCA/OMA 一致。MAG 的 grant-specific 差异写在 `domain_specific_profile`、stage/action contracts 和 MAG authority refs 中：funding call、applicant profile、grant strategy memory 和 source material refs 进入 grant pack，grant proposal、revision package、submission-ready package 和 receipt/blocker refs 输出。MAG authority 继续覆盖 grant truth、fundability/quality/export/submission verdict、artifact authority、memory accept/reject 和 owner receipt。
`family_stage_control_plane` 同样从 `product-entry-manifest` 暴露，但它只是一组 MAG-owned stage descriptors：每个 stage 都必须携带 stage goal、owner、skills、`allowed_action_refs`、handoff、source refs、freshness、authority boundary 与 `agent/prompts/<stage_id>.md` prompt ref。构建时会把 `allowed_action_refs` 校验到 `family_action_catalog`，从而让 `OPL` 的 discovery smoke 读取同一份 action truth；MAG 继续持有 grant truth、fundability judgment 与 submission-ready export gate。
`controlled_domain_memory_apply_proof` 聚合 consumed grant strategy memory refs、writeback proposal、MAG accept/reject decision、runtime receipt evidence projection、operator receipt projection 与 repo-source layout audit。它是 controlled grant-stage memory apply 的 proof surface：真实 receipt instance 只写到 workspace/runtime root，不写 repo source；真实 memory body、fundability verdict、authoring quality verdict、submission-ready export verdict 和 grant artifact 仍被禁止进入 repo source。OPL generated surfaces 只消费 `agent/` pack refs、contract refs、verdict refs、owner receipt refs 与 typed blockers，不能写 grant body、verdict body、package body、memory body 或 receipt instance。
`mag_consumer_thinning_contract` 进一步把 OPL handoff boundary 机器化：MAG domain-handler/direct path 保持 thin adapter，OPL 才是 generic primitive replacement owner。MAG 当前可交付的是合同、refs、receipt writer、typed blocker、no-forbidden-write guard、focused hosted receipt verification、lifecycle receipt bundle、memory receipt read projection、package lifecycle handoff projection、continuous receipt reconciliation snapshot、`external_evidence_request_pack` 和 refs-only evidence receipt ledger；真实 OPL replacement production consumption、workspace memory body migration、package/lifecycle workspace receipt 泛化和 live soak 是后续 evidence gate。`external_evidence_request_pack` 只列 request ids、required refs、required receipt shapes、forbidden payload classes 和 authority boundary；`contracts/external_evidence/mag-evidence-receipt-ledger.json` 只记录 receipt / typed blocker refs，不在 MAG 内实现 OPL runtime、App workbench、generic runner 或 production caller。per-surface private-platform residue 与删除门由 [MAG 私有实现与 OPL 迁移台账](./active/opl-private-implementation-migration-inventory.md) 承担，本文只保留架构层 owner split。

`mag_consumer_thinning_contract.privatized_functional_module_audit` 是当前 OPL 统一审计读取的功能私有化 closeout 面。它把旧 replacement / tombstone 口径收敛为四类：runtime registration、task lifecycle、source intake 归到 `declarative_pack_surface`；lifecycle adapter、observability、domain-handler/product status、package lifecycle、人用 workbench / scheduler / daemon 归到 `refs_only_adapter`；grant lifecycle stage、fundability / quality / export verdict、package readiness / submission-ready、grant transition oracle、owner receipt 和 grant strategy memory accept/reject 归到 `minimal_authority_function`；旧 Hermes/Gateway/local-manager、local journal / attempt ledger、patch bridge、compat aggregate test、legacy shell alias 和 repo-owned scheduler/daemon 归到 `legacy_proof_tombstone`。这个审计面用于防止误读：MAG 可以提供 declarative pack 和 refs-only adapter，但不能长期私有化通用 runtime；同时不能删除或外包 grant lifecycle、package readiness、fundability、quality、export verdict 或 owner receipt。

该 audit item 现在同时列出代码路径、活跃调用者、调用状态、迁移动作、保留理由和不能上收原因。架构读法是：旧 local journal / attempt ledger 与 Hermes/Gateway/local-manager runtime owner 已从 active source 删除；MAG 当前只保留 workspace/source validation、memory/package/status/domain-handler/CLI target、refs-only runtime_control、显式 executor adapter receipt 相关代码，以及只能在 OPL default stage attempt lease / receipt 下运行的 bounded controller authority target。`critique_loop_controller`、`authoring_mainline_controller` 与 `grant_autonomy_controller` 缺少 `one-person-lab` owner、`codex_cli` default executor 或 OPL attempt lease/receipt 时必须返回 typed blocker，不能启动 MAG-owned durable loop。OPL 应生成或托管通用 ledger、queue、lifecycle、source intake、artifact/package lifecycle、observability、workbench、scheduler/daemon 和 generic runner；MAG 不能外包 grant truth、memory body、fundability/quality/export verdict、submission-ready package authority、grant transition oracle 或 owner receipt。

## Workspace / file lifecycle 结构

MAG repo-source 目录按标准 domain agent 职责分层：

- `agent/`：grant declarative pack，包含 stage prompts、stage policies、skill/knowledge refs 与 quality gate refs。
- `contracts/`：机器合同、schema、descriptor、locator/index contract、receipt ref contract 与 restore/retention policy。
- `runtime/authority_functions/`：最小 grant authority function 的 runtime-facing anchor；只暴露 action metadata、owner receipt refs、typed blocker refs、no-regression refs 或 guarded apply refs，不承载 runtime artifact root。
- `src/`：MAG domain handler、AI-first authority adapter、receipt signer、typed blocker materializer 与 native helper implementation；不能扩展成 generic runner、queue、session store 或 workbench。
- `docs/`：人读治理、当前状态、边界说明和 provenance，不作为机器接口。

真实 workspace/file lifecycle 由 OPL generic lifecycle primitive 与 MAG owner authority 分层完成。OPL 持有通用 locator/index、scheduler/runner/session/workbench shell、retention/restore orchestration 与 projection；MAG repo source 只持有 refs、policy、schema 和 proof。真实 grant workspace、submission/export package、runtime artifact、receipt instance、cache、venv、pycache、pytest cache 和 install sync 副产物必须落在 workspace/runtime artifact root 或 `$CODEX_HOME/projects/med-autogrant/runtime-state/`，不能写回开发 checkout。

MAG 的 authority 边界不因 refs-only lifecycle 上收而外移：grant truth、fundability/quality/export verdict、package authority、grant strategy memory body accept/reject 和 owner receipt 继续由 MAG owner surface 决定；OPL 只能消费 locator、receipt ref、typed blocker 或 no-regression evidence。

这轮对齐不引入 `CrewAI` 依赖，也不把 OPL runtime framework 写成 MAG runtime owner，更不宣称已完成跨仓 runtime core ingest。当前真实状态是 MAG 作为独立 domain agent 维持 family-level contract-first 对齐与 domain-owned truth；OPL 统一 Agent Executor Adapter 的 MAG 边界已经落地，若启用 `Hermes-Agent` 或 `Claude Code`，它也只是显式 opt-in executor backend，要求 receipt/audit/fail-closed，不是默认公开入口。MAG-owned memory、owner/no-regression 与 lifecycle receipt evidence path 已可写 runtime receipt instance；剩余缺口是 OPL-hosted controlled grant stage attempt 在 OPL ledger 与 MAG runtime receipt instance 之间完成真实对账和 live soak。

## OPL Provider、Med Auto Grant 与 concrete executor 的分工

在当前架构里，OPL Temporal-backed stage-led runtime framework 是默认任务运行 owner，并承担：

- session substrate
- runtime state / attempt ledger durability
- interrupt / resume / scheduling 这类长期在线 runtime 能力
- domain-handler dispatch 的在线唤醒 carrier
- stage-led queue、handoff、receipt、retry/dead-letter 与 operator projection

生产在线路径默认要求 Temporal-backed provider ready。上游 Hermes 作为默认 provider 的旧口径只作为 provider-specific 或迁移记录保留。

`Med Auto Grant` 自己继续承担：

- workspace / draft / critique / revision / export 的 domain truth
- author-side object model 与 identity guard
- stage routing、artifact assembly 与 hosted handoff contract

当前 route-selected concrete executor 继续承担：

- 具体 authoring pass 的执行
- 由 route / executor adapter 选中的单步运行时
- 当前默认 `Codex CLI` 执行器，默认模式是 `autonomous`；OPL 持有 generic Agent Executor Adapter / registry
- `hermes_agent` / `claude_code` 是显式 opt-in backend；当前 MAG critique route 对 `hermes_agent` 产出 OPL `AgentExecutionReceipt` 风格 proof，domain-handler dispatch 不会把它设为默认

因此，这里真实成立的是：

- 默认公开 capability contract 先固定在 `CLI` / `MedAutoGrantDomainEntry` / 本地脚本 / schema-backed contract / domain-handler target
- domain governance / truth owner 仍是 `Med Auto Grant`
- concrete executor owner 仍按 route 单独选择，当前默认是 `Codex CLI`

这不等于“所有单步 authoring 都已经迁成 Hermes-native executor”。
如果未来某条 critique / revision / export route 要替换执行器，也必须按 route 单独冻结 truth 与 proof，而不是因为 substrate 已统一就自动把 authoring semantics 一起改掉。

## 入口与执行

入口与执行的当前 SSOT 是 grouped public CLI catalog、`MedAutoGrantDomainEntry` command contract、`MedAutoGrantProductEntry` generated/product projections、schemas、product-entry manifest、source/tests 和 runtime receipts。本文只保留 owner split 与 no-resurrection 边界，不复制完整 command list、schema list 或 builder-by-builder 实现清单。

| Surface | Current owner / role | Architecture boundary |
| --- | --- | --- |
| Repo-local formal entry | CLI + `MedAutoGrantDomainEntry`; grouped command catalog and domain-entry contracts are the machine source. | `foundry *`、`grant` / `work` aliases and route commands read MAG contracts and source; they do not create grant truth paths outside MAG owner surfaces. |
| Product / generated projections | `MedAutoGrantProductEntry` builds `product-entry`, `grant-progress`, `grant-cockpit`, `grant-direct-entry`, `grant-user-loop`, `product-entry-manifest`, `product-status` and hosted contract projections under schema guard. | These are controller-owned or generated refs for OPL/App consumption. They are not repo-local public CLI groups, durable truth surfaces, quality/export verdicts, or App/workbench consumption evidence. |
| Refs-only handoff / evidence | Hosted-receipt, lifecycle, memory, package-lifecycle, continuous-reconciliation, owner-payload and external-evidence surfaces. | They carry refs, receipts, typed blockers, no-regression evidence and count-only provenance. They do not implement generic OPL runtime, memory transport, package lifecycle shell, attempt ledger, repair workbench or production soak. |
| Grant domain execution | Grant pass/package/discovery/selector/initializer commands and route-selected executor adapters. | Domain logic owns inputs, identity guards, authoring/revision/export handoff and MAG authority. Bounded controllers require OPL default stage attempt owner / lease / receipt before running; otherwise they return MAG typed blockers. |
| Non-default executor receipt lane | `hermes_agent` / Claude Code remain explicit OPL Agent Executor Adapter backends; default executor remains `Codex CLI`. | MAG consumes OPL receipt / closeout payloads and helper results only for explicit lanes. Connectivity or receipt proof does not imply provider reasoning quality, default runtime ownership, grant readiness or route migration. |
| Retired runtime/session surfaces | `runtime run`, `runtime resume`, old Hermes probe, local journal, attempt ledger, Gateway/local-manager and facade/compatibility paths. | These stay in history/tombstone/no-resurrection context. Remaining domain runtime code can only be domain handler, grant-native authority, refs-only adapter, diagnostic or explicit executor receipt lane. |

具体 command、schema、builder、payload 和 helper implementation 必须从 source/tests、`domain_entry_contract.supported_commands`、product-entry manifest、schema registry 和 CLI behavior 读取。架构文档不得把 builder presence、schema completeness、grouped CLI success、product-entry manifest success、external evidence ledger 或 provider completion 写成 fundability-ready、quality-ready、export-ready、submission-ready、App sustained-consumption 或 production-ready。

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
- Generated `grant-progress` / `grant-cockpit` 当前属于 controller-owned / read-only product projection；它们不替代 durable truth surface，也不构成新的 service-safe domain entry contract，并且不会被镜像进 repo-local public CLI 或 hosted contract bundle 的 command catalog。
- `workspace quality-scorecard / workspace quality-diff` 当前属于正式 domain entry audit surface，并会进入 hosted contract bundle 的 command catalog 与 schema contract。
- `pass autonomy-controller` 当前属于 formal CLI/domain-entry command surface；它输出 controller-owned report，不改变 `controller` 仍为 internal surface 的 formal-entry matrix。
- Generated `grant-direct-entry` 当前属于 controller-owned 的 direct-entry composition；它不会改写 route owner，也不会被镜像进 repo-local public CLI 或 hosted contract bundle 的 command catalog。
- Generated `grant-user-loop` 当前属于 controller-owned 的 user-loop composition；它不会改写 route owner，也不会被镜像进 repo-local public CLI 或 hosted contract bundle 的 command catalog。
- 人工 gate 当前只覆盖同一基金任务内的作者决策，不把 gate 语义扩展成跨 funder 的重新选题/重选项目流程。
- 形式/客观补件默认是 `TODO + 显式唤醒` 队列项；默认不阻塞正文 authoring 主线。
- 历史 `runtime run / runtime resume` journal 默认落点只作为 `docs/history` / provenance 说明；当前 public surface 与 hosted contract 不再暴露本地 journal 作为 session owner。
- Hermes substrate state db 只在显式 proof lane 使用，默认不要求安装上游 `hermes-agent`；如需显式隔离，可通过 `MED_AUTOGRANT_HERMES_HOME` 覆盖。
- 历史 local host-agent runtime 只保留在归档与 provenance 材料里，不再作为长期产品 runtime owner。

## 文档层次

- Public surface：`README*`、`docs/README*`、`docs/public/domain-positioning.md`、`docs/public/mvp-scope.md`。
- 核心骨架：`docs/project.md`、`docs/architecture.md`、`docs/invariants.md`、`docs/decisions.md`、`docs/status.md`。
- Repo-tracked current truth：核心五件套、`contracts/runtime-program/current-program.json`，以及 `docs/specs/README*` 中列出的 active specs。
- 活跃规划：`docs/active/**`；历史计划与 dated specs 入口：`docs/history/**`。

## 历史边界

- OMX 已退场，仅保留历史入口。
