# 项目概览

## 项目定位

`Med Auto Grant` 是独立的医学 `Grant Ops` domain agent，面向 author-side、proposal-facing 的申请人侧写作主线。
当前仓库主线按 `Auto-only` 理解，formal entry 仍是 `CLI`，runtime substrate 已切到真实上游 `Hermes-Agent`；历史本地 runtime 线只保留在归档材料里，而当前 `hermes_runtime.py` 路径应被理解为 repo-side domain adapter。
当前入口已经形成稳定的 `CLI + MedAutoGrantDomainEntry`，`product build-entry` 负责轻量结构化 `product entry` shell，`product manifest` 把这层 shell、shared handoff 模板与当前主线快照冻结成 machine-readable discovery surface；`product frontdesk` 进一步把其上方的 controller-owned direct frontdoor 冻结下来。这层 shell、`product manifest`、`product frontdesk` 及其 `executor_routing_contract` 都已经进一步收口成 schema-backed contract，并在生成时 fail-closed；`package hosted-contract-bundle` 会把 `domain_entry_contract`、`schema_contract`、`authoring_contract` 一起冻结进 hosted-friendly 合同目录；`workspace progress / workspace cockpit`、`product direct-entry`、`mainline status`、维护者参考记录与 `product user-loop` 已经共同构成当前 direct grant product projection 与用户回路；`direction_screening -> frozen` 已进入 landed command catalog；`package submission-ready` 已收口为 fail-closed 的本地 submission-ready 交付面。当前 direct grant loop、frontdoor discovery、route contract、local delivery 与 hosted bundle 已经共享同一份可机读的 authoring record。
当前任务边界锁定在“指定基金任务正文 authoring”：科学完成的可待审包与形式/客观补件完成必须显式分层管理，默认先确保正文科学成立与可审阅，再通过补件队列收口门户前置材料。
按当前定位，这个仓的对外第一身份是“可被通用 agent 直接调用的医学基金 domain agent”：`OPL` 只保留 family-level 的 session/runtime/projection 与 shared modules/contracts/indexes；`Hermes-Agent` 继续负责 runtime substrate；`Med Auto Grant` 继续负责 grant authoring record、domain entry 与 direct grant product entry。
当前统一协作模型是：`Hermes-Agent` 持有 runtime substrate / orchestration，`Med Auto Grant` 持有 grant 对象边界、author-side contract 与 export record，而 route-selected executor 持有具体 authoring execution；`direction_screening -> frozen`、`revision` 与 packaging/export 继续通过 repo-side domain logic 与 executor adapter 落地。
当前 hosted caller / `OPL` caller 已经可以直接消费 `domain_entry_contract`、`schema_contract`、`authoring_contract`，并按 `supported_commands` / `command_contracts` 构造请求。`workspace progress / workspace cockpit` 保持 product-facing read-only projection，`product direct-entry` 负责组合 direct-entry contract，`mainline status`、维护者参考记录与 `product user-loop` 负责投影 repo 主线快照与 route-derived next action。`pass direction-screening`、`pass question-refinement`、`pass argument-building`、`pass fit-alignment`、`pass outline`、`pass drafting` 与 `pass freeze` 已经收口成 landed command catalog，并被 route contract、`product user-loop` 与 hosted bundle 复用。

## 项目目标

- 明确 `CLI / MCP / controller` 的 formal-entry matrix。
- 稳定 `grant_run_id`、`workspace_id`、`draft_id`、`program_id` 与相关 artifact/export surface。
- 在真实上游 `Hermes-Agent` substrate 上延续 author-side grant mainline，并把历史本地 runtime closeout 只保留给归档追溯材料。
- 保持 `CLI` / `MedAutoGrantDomainEntry` 作为稳定 agent entry，使 `Codex`、`OPL` 和其他通用 agent 都能直接按 contract 调用。
- 在已落地 runtime substrate 之上，保持 `product build-entry` 这层共享-envelope lightweight grant `product entry` shell 稳定，并让它同时服务 direct entry 与 `OPL` handoff。
- 在已落地 runtime substrate 与 lightweight shell 之上，通过 `workspace progress / workspace cockpit` 维持 controller-owned、read-only 的 direct grant product projection。
- 保持 `select-project-profile`、`initialize-intake-workspace`、`discover-funding-opportunities` 作为可选 pre-authoring 辅助入口，不把它们写成已指定基金任务内的默认执行阻塞链路。
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
- 通过 `product manifest` 与 `product frontdesk` 把 direct grant frontdoor 收口成独立 schema-backed、generation-time fail-closed 的 contract，并把 `family_orchestration` companion 的 route status 严格对齐到共享 author-side route truth。
- 通过 `package submission-ready` 保持严格的本地 submission-ready 导出面，并明确它与“科学完成可待审包”的 authoring stop 不是同一完成层；同时继续保持“不对外宣称官网已提交”的边界。
- 人工 gate 只覆盖同一基金任务内的作者决策，不扩展成跨 funder 路线重选流程。
- 把 hosted-friendly handoff contract 收口成 caller 可直接消费的 entry / schema / route catalog，并保持与当前 bundle 同步。
- 保持 `gateway / harness` 作为内部架构分层术语，不作为公开第一身份。
- 更远期的 hosted 产品入口演进统一留在 `docs/plans/`，不写进当前主线口径。

## 范围与非目标

- 不把 `MCP` 或 `controller` 解释为已公开支持的 runtime formal entry。
- 不把仓库误写成成熟 autopilot 或 reviewer-owned runtime。
- 不把用户级 runtime-state 或其他 machine-local control-plane 写成 repo-tracked 产品本体。
- 不把 `P5.*` hosted/federation 扩展写成当前已开工的范围。
- 不把同任务内的人工 gate 写成跨 funder 的重选流程。

## 当前形态

- Current public execution line：`direct MAG agent entry / OPL federation handoff -> product frontdesk -> product user-loop -> workspace progress / workspace cockpit -> product direct-entry -> quality governance / autonomy controller -> service-safe pass/package commands`
- Current frontdoor shape：`product frontdesk + product user-loop + workspace progress/workspace cockpit + product direct-entry + package submission-ready`
- Latest absorbed runtime slice：`R5.A / Hosted-Friendly Session Boundary`
- Current owner line：`CLI-first with real upstream Hermes-Agent runtime substrate`
- 默认入口：CLI（validator、summary、route、controller-owned product projection + service-safe domain entry dispatch）
