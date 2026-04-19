# 项目概览

## 项目定位

`Med Auto Grant` 是共享 `Unified Harness Engineering Substrate` 上、面向医学 `Grant Ops` 的 author-side、proposal-facing `Domain Harness OS` 方向。
当前仓库主线按 `Auto-only` 理解，formal entry 仍是 `CLI`，runtime substrate 已切到真实上游 `Hermes-Agent`；历史本地 runtime 线只留在归档 current-truth 与 closeout 材料里，而当前 `hermes_runtime.py` 路径应被理解为 repo-side domain adapter。
当前入口真相是：`CLI + MedAutoGrantDomainEntry` 已经构成稳定的 `agent entry`，`product build-entry` 也已经把轻量结构化 `product entry` shell 落到仓库里，`product manifest` 则把这层 shell、shared handoff 模板与当前 mainline snapshot 一起冻结成 machine-readable discovery surface；`product frontdesk` 进一步把其上方的 controller-owned direct frontdoor 冻结下来。这层 shell、`product manifest`、`product frontdesk` 及其 `executor_routing_contract` 都已经进一步收口成 schema-backed contract，并在生成时 fail-closed；`package hosted-contract-bundle` 会把 `domain_entry_contract`、`schema_contract`、`authoring_contract` 一起冻结进 hosted-friendly 合同目录；`workspace progress / workspace cockpit`、`product direct-entry`、`mainline status` / `mainline phase` / `product user-loop` 已经共同构成当前 direct grant product projection 与用户回路；`direction_screening -> frozen` 已进入 landed command catalog；`package submission-ready` 已收口为 fail-closed 的本地 submission-ready 交付面。当前 direct grant loop、frontdoor discovery、route contract、local delivery 与 hosted bundle 已经共享同一份可机读的 authoring truth。
按 `OPL` 对齐后的理想目标，这个仓最终应收敛成：`OPL` 继续负责 family-level 顶层入口与 gateway，`Hermes-Agent` 继续负责 runtime substrate，`Med Auto Grant` 继续负责 grant authoring truth、domain entry 与 direct grant product entry。
当前统一协作模型是：`Hermes-Agent` 持有 runtime substrate / orchestration，`Med Auto Grant` 持有 grant 对象边界、author-side contract 与 export truth，而 route-selected executor 持有具体 authoring execution；`direction_screening -> frozen`、`revision` 与 packaging/export 继续通过 repo-side domain logic 与 executor adapter 落地，而不是被强行收缩成单一 runtime 脑。
当前 hosted caller / `OPL` caller 已经可以直接消费 `domain_entry_contract`、`schema_contract`、`authoring_contract`，并按 `supported_commands` / `command_contracts` 构造请求。`workspace progress / workspace cockpit` 保持 product-facing read-only projection，`product direct-entry` 负责组合 direct-entry contract，`mainline status` / `mainline phase` / `product user-loop` 负责投影 repo 主线快照与 route-derived next action。`pass direction-screening`、`pass question-refinement`、`pass argument-building`、`pass fit-alignment`、`pass outline`、`pass drafting` 与 `pass freeze` 已经收口成 landed command catalog，并被 route contract、`product user-loop` 与 hosted bundle 复用。

## 项目目标

- 明确 `CLI / MCP / controller` 的 formal-entry matrix。
- 稳定 `grant_run_id`、`workspace_id`、`draft_id`、`program_id` 与相关 artifact/export surface。
- 在真实上游 `Hermes-Agent` substrate 上延续 author-side grant mainline，并把历史本地 runtime closeout 只保留给归档追溯材料。
- 在已落地 runtime substrate 之上，保持 `product build-entry` 这层共享-envelope lightweight grant `product entry` shell 稳定，并让它同时服务 direct entry 与 `OPL` handoff。
- 在已落地 runtime substrate 与 lightweight shell 之上，先通过 `workspace progress / workspace cockpit` 落第一棒 controller-owned、read-only 的 direct grant product projection，再继续向更成熟的 grant-facing UX 推进。
- 通过 `product direct-entry` 把 direct grant entry 继续推进到组合式 product contract，并保持当前 controller-owned direct-entry 语义稳定。
- 通过 `mainline status`、`mainline phase` 与 `product user-loop` 把 repo 主线快照与当前 direct grant user loop 收成当前 inbox-like shell。
- 把 `direction_screening -> frozen` 的 author-side 主线持续收口为 landed service-safe command surface，让人工国自然写作流程里的方向筛选、问题提纯、立项依据、适配度、提纲、正文起草与送审前冻结都能直接落到同一套 route truth 上。
- 通过 `product manifest` 与 `product frontdesk` 把 direct grant frontdoor 收口成独立 schema-backed、generation-time fail-closed 的 contract，并把 `family_orchestration` companion 的 route status 严格对齐到共享 author-side route truth。
- 通过 `package submission-ready` 把本地 submission-ready 交付目录收口成正式 command surface，并保持“缺材料就 fail-closed、不对外宣称官网已提交”的边界。
- 把 hosted-friendly handoff contract 收口成 future caller 可直接消费的 entry / schema / route catalog，而不是在 bundle 外重新发明协作语义。
- 明确这条主线从 “fast cutover 已完成什么” 到 “hosted caller / `OPL` contract consumption proof 已完成什么” 再到 “下一阶段 mature direct product entry” 的阶段顺序，不在理想目标与当前完成态之间反复漂移。

## 范围与非目标

- 不把 `MCP` 或 `controller` 解释为已公开支持的 runtime formal entry。
- 不把仓库误写成成熟 autopilot 或 reviewer-owned runtime。
- 不把用户级 runtime-state 或其他 machine-local control-plane 写成 repo-tracked 产品本体。
- 不把 `P5.*` hosted/federation 扩展写成当前已开工的范围。

## 当前形态

- Current public execution line：`OPL shell + MAG domain agent + Codex default execution + Hermes-Agent backup gateway`
- Current frontdoor shape：`product frontdesk + product user-loop + workspace progress/workspace cockpit + product direct-entry + package submission-ready`
- Latest absorbed runtime slice：`R5.A / Hosted-Friendly Session Boundary`
- Current owner line：`CLI-first with real upstream Hermes-Agent runtime substrate`
- 默认入口：CLI（validator、summary、route、controller-owned product projection + service-safe domain entry dispatch）
