# 项目概览

## 项目定位

`Med Auto Grant` 是独立的医学 `Grant Ops` domain agent，面向 author-side、proposal-facing 的申请人侧写作主线。
对外第一主语是单一 `Med Auto Grant` app skill；当前仓库主线按 `Auto-only` 理解，formal entry 仍是 `CLI`。默认公开 capability surface 收口为 `CLI + MedAutoGrantDomainEntry + 本地脚本 + schema-backed contract`，默认正文执行继续继承本机 `Codex CLI` / `codex_cli` 配置；在 OPL 托管语境中，Agent executor 也是 stage attempt 的最小执行单位，`Codex CLI` 是当前第一公民 executor。`product entry/product status/direct-entry/user-loop`、`product build-entry`、`product manifest`、`runtime_control` 与 `package hosted-contract-bundle` 仍然保留，但它们只作为 app skill 下的内部 command contract、direct-product projection 或 integration/reference surface，不再作为对外第一主语。历史本地 runtime 线只保留在归档材料里，而 `Hermes-Agent` 相关路径与 `domain_runtime.py` 只应被理解为显式 hosted/proof backend 或 repo-side domain adapter，不是默认公开 runtime owner；默认安装不拉取 `hermes-agent`。
当前入口已经形成稳定的 `CLI + MedAutoGrantDomainEntry`；`product build-entry` 负责轻量结构化 `product entry` shell，`product manifest` 把这层 shell、shared handoff 模板与当前主线快照冻结成 machine-readable discovery surface。`product status` 进一步把其上方的 controller-owned direct product entry 冻结下来。这层 shell、`product manifest`、`product status` 及其 `executor_routing_contract` 都已经进一步收口成 schema-backed contract，并在生成时 fail-closed。`package hosted-contract-bundle` 会把 `domain_entry_contract`、`schema_contract`、`authoring_contract` 一起冻结进 hosted-friendly 合同目录，但只作为 integration/reference surface。`workspace progress / workspace cockpit`、`product direct-entry`、`mainline status`、维护者参考记录与 `product user-loop` 已经共同构成当前 direct grant product projection 与用户回路，但都属于 app skill 下的内部 command contract。`direction_screening -> frozen` 已进入 landed command catalog；`package submission-ready` 已收口为 fail-closed 的本地 submission-ready 交付面。当前 direct grant loop、product entry discovery、route contract、local delivery 与 hosted bundle 已经共享同一份可机读的 authoring record。
当前任务边界锁定在“指定基金任务正文 authoring”：科学完成的可待审包与形式/客观补件完成必须显式分层管理，默认先确保正文科学成立与可审阅，再通过补件队列收口门户前置材料。
按当前定位，这个仓的对外第一身份是“通过单一 app skill 暴露的独立医学基金 domain agent”：`OPL` 是 stage-led 的完整智能体运行框架，可以把 MAG 作为外部领域依赖托管、唤醒和投影。OPL 负责 stage attempt 生命周期、queue、wakeup、handoff、receipt、approval/retry/dead-letter、operator projection、shared modules/contracts/indexes 与外部 provider 编排；MAG 继续负责 grant authoring record、domain entry、direct grant product entry、fundability judgment、quality gate 和 submission-ready export authority。显式 hosted/proof backend 只能挂在同一套 route/export contract 之下，并且只保证可接入、可回执、可审计。
在 OPL stage-led family agent framework 中，MAG 是 admitted domain agent，不是 OPL 内部模块。OPL 可以读取 MAG stage/action/projection descriptor，负责编排和观测；MAG 继续持有 call intake、fundability strategy、specific aims、proposal authoring、review/rebuttal、package gate 等 stage 语义，以及 authoring truth、quality gate 和 submission-ready export authority。
当前 stage-led 对齐已经落到 MAG-owned descriptor/projection 层：`family_action_catalog`、`family_stage_control_plane`、`runtime_control`、`runtime_continuity`、`product sidecar export/dispatch` 与 `opl_stage_runtime_registration`。这些 surface 让 OPL 能做 discovery、typed queue、wakeup、handoff、receipt 和 operator projection；它们不让 OPL 生成 grant route、fundability verdict、authoring quality verdict 或 export readiness。
当前 domain memory apply 闭环也落在同一边界上：MAG 暴露 writeback proposal generator、accept/reject decision projection、runtime receipt evidence writer、operator receipt projection 与 `controlled_domain_memory_apply_proof`；真实 memory store、receipt 实例和 grant artifact 仍属于 workspace / `$CODEX_HOME/projects/med-autogrant/runtime-state/`，repo 只保存 descriptor、schema、locator、fixture 模板和 repo-source layout audit。
当前统一协作模型是：稳定可调用面先固定在单一 app skill、`CLI`、`MedAutoGrantDomainEntry`、本地脚本、product-entry/projection commands 与 schema-backed contract；当前第一公民 concrete executor 继续继承本机 `Codex`；如果显式启用 hosted/proof backend，它也必须服从同一套 route truth、author-side contract 与 export record，并且只承诺接入、回执和审计。`direction_screening -> frozen`、`revision` 与 packaging/export 继续通过 repo-side domain logic 与 executor adapter 落地。
当前 hosted caller / `OPL` caller 若需要 machine-readable handoff，可以消费 `domain_entry_contract`、`schema_contract`、`authoring_contract`，并按 `supported_commands` / `command_contracts` 构造请求。`workspace progress / workspace cockpit` 保持 product-facing read-only projection，`product direct-entry` 负责组合 direct-entry contract，`mainline status`、维护者参考记录与 `product user-loop` 负责投影 repo 主线快照与 route-derived next action。`pass direction-screening`、`pass question-refinement`、`pass argument-building`、`pass fit-alignment`、`pass outline`、`pass drafting` 与 `pass freeze` 已经收口成 landed command catalog，并被 route contract、`product user-loop` 与 hosted bundle 复用。

## 项目目标

- 明确 `CLI / MCP / controller` 的 formal-entry matrix。
- 稳定 `grant_run_id`、`workspace_id`、`draft_id`、`program_id` 与相关 artifact/export surface。
- 在不改写 domain truth 的前提下保持默认 `Codex` 执行路径与显式 hosted/proof backend 并存，并把历史本地 runtime closeout 只保留给归档追溯材料。
- 在 OPL 目标形态中只把 MAG projection 注册给 OPL stage-led runtime framework；OPL 可以管理 provider-backed family runtime 与状态索引，但不得替代 MAG author-side truth、quality gate、submission-ready export gate 或 route-selected executor。
- 保持 Codex App direct skill path 与 OPL 托管 path 的语义等价：两条路径都必须回到 MAG-owned route truth、workspace truth、quality surfaces 和 export gate。
- 保持 `CLI` / `MedAutoGrantDomainEntry` 作为稳定 agent entry，使 `Codex`、`OPL` 和其他通用 agent 都能直接按 contract 调用。
- 在已落地 runtime substrate 之上，保持 `product build-entry` 这层共享-envelope lightweight grant `product entry` shell 稳定，并让它同时服务 direct entry 与 `OPL` handoff。
- 在已落地 runtime substrate 与 lightweight shell 之上，通过 `workspace progress / workspace cockpit` 维持 controller-owned、read-only 的 direct grant product projection。
- 保持 `select-project-profile`、`initialize-intake-workspace`、`discover-funding-opportunities` 作为可选 pre-authoring 辅助入口；`initialize-intake-workspace` 默认生成目录型 workspace scaffold，并以 `workspace.json` 作为 canonical document，不把它们写成已指定基金任务内的默认执行阻塞链路。
- 把“科学完成可交付待审包”与“形式/客观补件完成”显式分层，避免把门户前置材料与正文科学语义混写成单一完成态。
- 形式/客观补件默认进入 `TODO + 显式唤醒` 队列；只有直接破坏正文科学成立时，才升级为正文 authoring blocker。
- 通过 `product direct-entry` 把 direct grant entry 继续推进到组合式 product contract，并保持当前 controller-owned direct-entry 语义稳定。
- 通过 `mainline status`、维护者参考记录与 `product user-loop` 把 repo 主线快照与当前 direct grant user loop 收成当前 inbox-like shell。
- 把 `direction_screening -> frozen` 的 author-side 主线持续收口为 landed service-safe command surface，其中已指定基金任务的默认正文主线聚焦 `question_refinement -> frozen` 的科学写作与修订。
- 通过 `execute-critique-revision-loop` 把“批注 -> 修订 -> re-review”的长时自治闭环收口成可机读 command surface，并保持 major reframe / forced rollback / max rounds 的 fail-closed 语义。
- 通过 `execute-authoring-mainline-loop` 把 rollback 后的 `question_refinement / argument_building / fit_alignment` 重建也纳入同一条自治主线，而不是只在 critique/revision 层内循环。
- 通过 `grant-quality-scorecard` 与 `grant-quality-diff` 把申请书质量收口成可机读治理面，覆盖科学问题、必要性/价值闭合、申请人适配、技术路线、claim-evidence coverage、未关闭硬伤和版本间问题关闭进度。
- 通过 `execute-grant-autonomy-controller` 把长期自治控制层收口成正式 command surface，使系统在同一基金任务内调度 mainline loop 与质量 gate；selection/discovery 仅作为可选输入上下文，不触发默认跨 funder 重选。
- 通过 `grant_family_registry.py` 把通用 grant grammar、review grammar、template strategy 与 funder-specific family profile 分开，避免把新增基金类型散落进主流程。
- 通过 `product manifest` 与 `product status` 把 direct grant product entry 作为 app skill 下的内部 contract 收口成独立 schema-backed、generation-time fail-closed 的 contract，并把 `family_orchestration` companion 的 route status 严格对齐到共享 author-side route truth。
- 通过 `package submission-ready` 保持严格的本地 submission-ready 导出面，并明确它与“科学完成可待审包”的 authoring stop 不是同一完成层；同时继续保持“不对外宣称官网已提交”的边界。
- 人工 gate 只覆盖同一基金任务内的作者决策，不扩展成跨 funder 路线重选流程。
- 把 hosted-friendly handoff contract 收口成 caller 可直接消费的 integration/reference catalog，并保持与当前 bundle 同步。
- 保持 stage-led framework / domain harness 作为内部架构分层术语，不作为公开第一身份。
- 更远期的 hosted 产品入口演进在活跃阶段统一留在 `docs/active/`，完成后归入 `docs/history/`，不写进当前主线口径。

## 范围与非目标

- 不把 `MCP` 或 `controller` 解释为已公开支持的 runtime formal entry。
- 不把仓库误写成成熟 autopilot 或 reviewer-owned runtime。
- 不把用户级 runtime-state 或其他 machine-local control-plane 写成 repo-tracked 产品本体。
- 不把 `P5.*` hosted/federation 扩展写成当前已开工的范围。
- 不把同任务内的人工 gate 写成跨 funder 的重选流程。
- 不把 OPL runtime framework、旧 `OPL Runtime Manager` 口径或未来 OPL sidecar 写成 MAG 的默认公开入口、grant truth owner、authoring executor 或 repository-local Hermes fork。
- 不把已经退役到 provenance / regression oracle 的旧 local runtime、旧 `OPL Gateway` wording、旧五个 canonical verifier baseline 或旧 product-status traces 重新提升为默认 owner。

## 当前形态

- Current execution line：`single Med Auto Grant app skill / CLI / MedAutoGrantDomainEntry -> internal product status / user-loop / direct-entry contracts -> workspace progress / workspace cockpit -> quality governance / autonomy controller -> service-safe pass/package commands`
- Current product entry shape：`internal product status + internal user-loop + workspace progress/workspace cockpit + internal direct-entry + package submission-ready`
- Latest absorbed runtime slice：`R5.A / Hosted-Friendly Session Boundary`
- Current owner line：`CLI/domain-entry stable capability surface with Codex-default execution and optional hosted backend lanes`
- 默认入口：CLI（validator、summary、route、controller-owned product projection + service-safe domain entry dispatch）
