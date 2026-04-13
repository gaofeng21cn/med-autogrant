# 项目概览

## 项目定位

`Med Auto Grant` 是共享 `Unified Harness Engineering Substrate` 上、面向医学 `Grant Ops` 的 author-side、proposal-facing `Domain Harness OS` 方向。
当前仓库主线按 `Auto-only` 理解，formal entry 仍是 `CLI`，但 runtime substrate 已切到真实上游 `Hermes-Agent`；旧 `CLI-first + host-agent` 线只保留为历史迁移基线，而当前 `hermes_runtime.py` 路径应被理解为 repo-side domain adapter。
当前入口真相是：`CLI + MedAutoGrantDomainEntry` 已经构成稳定的 `agent entry`，`build-product-entry` 也已经把轻量结构化 `product entry` shell 落到仓库里，`product-entry-manifest` 则把这层 shell、shared handoff 模板与当前 mainline snapshot 一起冻结成 machine-readable discovery surface；`product-frontdesk` 现在又把其上方的 controller-owned direct frontdoor 冻结下来。当前这层 shell 及其 `executor_routing_contract` 还已经进一步收口成 schema-backed contract，并在生成时 fail-closed；`build-hosted-contract-bundle` 现在也会把 `domain_entry_contract`、`schema_contract`、`authoring_contract` 一起冻结进 hosted-friendly 合同目录；`grant-progress / grant-cockpit` 已经把第一棒 controller-owned、read-only 的 direct grant product projection 落地，并通过 `schemas/v1/grant-progress.schema.json` 与 `schemas/v1/grant-cockpit.schema.json` 收口成 schema-backed、generation-time fail-closed 的 projection contract；`grant-direct-entry` 已把 direct product entry 的第二棒组合面落地，并通过 `schemas/v1/grant-direct-entry.schema.json` 收口成 schema-backed、generation-time fail-closed 的 direct-entry contract；`mainline-status`、`mainline-phase` 与 `grant-user-loop` 则把第三棒 mainline snapshot / current user loop 收到当前 inbox-like shell，并通过 `schemas/v1/grant-user-loop.schema.json` 保持 fail-closed；当前 `P4.D` 又进一步把 `direction_screening -> frozen` 的 author-side 主线收成 landed command catalog，使 direct grant loop、route contract 与 hosted bundle 看到同一份全链 authoring executor truth，但更完整的 grant-facing 产品体验仍未落地。
按 `OPL` 对齐后的理想目标，这个仓最终应收敛成：`OPL` 继续负责 family-level 顶层入口与 gateway，`Hermes-Agent` 继续负责 runtime substrate，`Med Auto Grant` 继续负责 grant authoring truth、domain entry 与 direct grant product entry。
当前统一协作模型是：`Hermes-Agent` 持有 runtime substrate / orchestration，`Med Auto Grant` 持有 grant 对象边界、author-side contract 与 export truth；具体 `direction_screening -> frozen` authoring、`revision` 与 packaging/export 执行继续通过 repo-side domain logic 与 executor adapter 落地，而不是被强行收缩成单一 runtime 脑。
当前 `P3 hosted caller / OPL consumption proof` 也已经 landed：external caller 现在可以直接消费 `domain_entry_contract`、`schema_contract`、`authoring_contract`，并按 `supported_commands` / `command_contracts` 构造请求，而不需要 repo-local helper。
当前 `P4` 的第一棒也已经 landed：`grant-progress / grant-cockpit` 当前只作为 product-facing read-only projection 存在，故意不进入 `domain_entry_contract.supported_commands`，也不进入 hosted contract bundle 的 command catalog，更不把它们写成新的 route executor。
当前 `P4` 的第二棒也已经 landed：`grant-direct-entry` 只负责把 `grant-progress`、`grant-cockpit` 与两份 `product_entry` envelope 组合成 direct-entry contract；它同样不进入 `domain_entry_contract.supported_commands`，也不成为新的 route executor。
当前 `P4` 的第三棒也已经 landed：`mainline-status`、`mainline-phase` 与 `grant-user-loop` 只负责把 repo 主线快照、当前 direct-entry composition 与 route-derived next action 投影成当前用户回路；它们同样不进入 `domain_entry_contract.supported_commands`，也不成为新的 route executor。
当前 `P4` 的第四棒也已经 landed：`execute-direction-screening-pass`、`execute-question-refinement-pass`、`execute-argument-building-pass`、`execute-fit-alignment-pass`、`execute-outline-pass`、`execute-drafting-pass` 与 `execute-freeze-pass` 已把此前 pending 的 authoring 前半程收口成 landed command catalog；这层 landed truth 会同时被 route contract、`grant-user-loop` 与 hosted bundle 复用。

## 项目目标

- 明确 `CLI / MCP / controller` 的 formal-entry matrix。
- 稳定 `grant_run_id`、`workspace_id`、`draft_id`、`program_id` 与相关 artifact/export surface。
- 在 `R1 -> R5.A` 已 absorbed 的前提下，把当前 post-`R5.A` honest stop 作为迁移基线保留，并在真实上游 `Hermes-Agent` substrate 上延续 author-side grant mainline。
- 在已落地 runtime substrate 之上，保持 `build-product-entry` 这层共享-envelope lightweight grant `product entry` shell 稳定，并让它同时服务 direct entry 与 `OPL` handoff。
- 在已落地 runtime substrate 与 lightweight shell 之上，先通过 `grant-progress / grant-cockpit` 落第一棒 controller-owned、read-only 的 direct grant product projection，再继续向更成熟的 grant-facing UX 推进。
- 在 `P4.A` 已 landed 的基础上，通过 `grant-direct-entry` 把 direct grant entry 继续推进到组合式 product contract，而不是另起新的 repo-local helper 或 executor surface。
- 在 `P4.B` 已 landed 的基础上，通过 `mainline-status`、`mainline-phase` 与 `grant-user-loop` 把 repo 主线快照与当前 direct grant user loop 收成当前 inbox-like shell，而不是让用户继续自己拼 program docs 与 route commands。
- 在 `P4.C` 已 landed 的基础上，把 `direction_screening -> frozen` 的 author-side 主线收口为 landed service-safe command surface，让人工国自然写作流程里的方向筛选、问题提纯、立项依据、适配度、提纲、正文起草与送审前冻结都能直接落到同一套 route truth 上。
- 把 hosted-friendly handoff contract 收口成 future caller 可直接消费的 entry / schema / route catalog，而不是在 bundle 外重新发明协作语义。
- 明确这条主线从 “fast cutover 已完成什么” 到 “hosted caller / `OPL` contract consumption proof 已完成什么” 再到 “下一阶段 mature direct product entry” 的阶段顺序，不在理想目标与当前完成态之间反复漂移。

## 范围与非目标

- 不把 `MCP` 或 `controller` 解释为已公开支持的 runtime formal entry。
- 不把仓库误写成成熟 autopilot 或 reviewer-owned runtime。
- 不把用户级 runtime-state 或其他 machine-local control-plane 写成 repo-tracked 产品本体。
- 不把 `P5.*` hosted/federation 扩展写成当前已开工的范围。

## 当前形态

- Current phase：`P4 mature direct grant product entry`
- Active tranche：`P4.D full grant authoring executor landing`
- Latest absorbed runtime slice：`R5.A / Hosted-Friendly Session Boundary`
- Current owner line：`CLI-first with real upstream Hermes-Agent runtime substrate`
- Historical owner line：`post-R5A local runtime closeout / honest stop`
- Previous truthful closeout baseline：`NO_NEW_POST_R5A_LOCAL_RUNTIME_DELTA_HONEST_STOP`
- 默认入口：CLI（validator、summary、route、controller-owned product projection + service-safe domain entry dispatch）
