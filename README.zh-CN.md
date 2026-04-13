<p align="center">
  <a href="./README.md">English</a> | <a href="./README.zh-CN.md"><strong>中文</strong></a>
</p>

# Med Auto Grant

**面向申请人侧 `NSFC` 风格申请的医学基金主线（开发中）**

> 当前状态：仓库现在已经跑在真实上游 `Hermes-Agent` runtime substrate 上，同时把申请人侧 grant domain 语义保留在 repo-local adapter 与 domain logic 中。此前已 absorbed 的 `CLI-first + host-agent` 线继续只作为历史迁移基线 / regression oracle 保留。当前已经能对冻结且材料齐备的 workspace 一键导出本地 `submission-ready` 交付包，但仍不是 actual hosted runtime，也不是会替你完成外部官网提交的自动驾驶产品。

<table>
  <tr>
    <td width="33%" valign="top">
      <strong>面向谁</strong><br/>
      需要准备基金申请的医学研究者、临床团队、青年教师与 PI
    </td>
    <td width="33%" valign="top">
      <strong>公开角色</strong><br/>
      共享 <code>Unified Harness Engineering Substrate</code> 之上的医学基金 authoring <code>Grant Ops</code> <code>Domain Harness OS</code>
    </td>
    <td width="33%" valign="top">
      <strong>在联邦中的位置</strong><br/>
      <code>One Person Lab -> Grant Foundry -> Med Auto Grant</code>；当前活跃的医学 <code>Grant Ops</code> 业务仓主线，而顶层 federation admission / handoff wording 仍在 <code>OPL</code> 单独门控
    </td>
  </tr>
</table>

## 产品定位

如果你的目标是把申请人履历、既有成果、在研项目、预实验结果和候选方向，收敛成一条更像样的 `NSFC` 风格基金申请主线，`Med Auto Grant` 正在被构建成共享 `Unified Harness Engineering Substrate` 之上的医学 `Grant Ops` `Domain Harness OS`，用于承载可治理、可审计、可持续修订、并能显式回看上一轮修订证据的主线流程。

## Runtime 形态（当前与未来）

- 当前可执行 runtime 形态：`CLI-first + real upstream Hermes-Agent runtime substrate`。
- 当前 `hermes_runtime.py` 与 `domain_entry.py` 路径是 repo-side domain/entry adapter；它们**不**替代上游 runtime substrate owner。
- 旧 `Codex-default host-agent runtime` 继续只作为历史 compatibility bridge / regression oracle。
- 其 formal-entry matrix 已固定为：默认正式入口 `CLI`、支持协议层 `MCP`（当前保留为 future layer，尚未 repo-verified）、内部控制面 `controller`。
- 当前仓库主线按 `Auto-only` 理解；未来如果要做 `Human-in-the-loop` 产品，应作为兼容 sibling 或 upper-layer product 复用同一 substrate，而不是把当前仓改成同仓双模。
- 已落地的 service-safe entry：`MedAutoGrantDomainEntry`，它把 CLI 命令面保留成 future gateway caller 可复用的结构化 entry contract。
- 当前 `product entry` shell 与 `executor_routing_contract` 也已经进一步冻结成 schema-backed contract surface，并在生成时 fail-closed。
- 当前诚实的 `P4.E` frontdoor-contract layer 也已经通过 `product-entry-manifest` 与 `product-frontdesk` 落地：两者现在分别由 `product-entry-manifest.schema.json` 与 `product-frontdesk.schema.json` 独立冻结，并在生成时 fail-closed。
- 当前诚实的 `P4.F` local-delivery layer 也已经通过 `build-submission-ready-package` 落地：它会对不完整 frozen workspace fail-closed，只有在必备章节、预实验、代表作、在研项目与冻结 gate 都满足时，才导出本地 `submission_ready_package`。
- 当前 controller-owned 的 direct-product projection `grant-progress` 与 `grant-cockpit` 也已经通过 `grant-progress.schema.json` 与 `grant-cockpit.schema.json` 进一步冻结成 schema-backed contract surface，并在生成时 fail-closed。
- 下一棒诚实的 `P4.B` direct-entry layer 也已经通过 `grant-direct-entry` 落地：它把 `grant-progress`、`grant-cockpit` 和已冻结的 direct / `opl-handoff` `product_entry` envelope 组合成一份 schema-backed、fail-closed 的 direct-entry contract，对应 `grant-direct-entry.schema.json`。
- 当前诚实的 `P4.C` companion layer 也已经通过 `mainline-status`、`mainline-phase` 与 `grant-user-loop` 落地：它把 repo 主线快照和当前 direct grant user loop 收成一处，但仍不发明新的 executor surface；其中 `grant-user-loop` 由 `grant-user-loop.schema.json` 冻结；landed next-action command 现在会带出具体 runtime-state 输出路径，而不是 `<output-path>` 占位符。
- 当前诚实的 `P4.D` authoring executor layer 也已经通过 `execute-direction-screening-pass`、`execute-question-refinement-pass`、`execute-argument-building-pass`、`execute-fit-alignment-pass`、`execute-outline-pass`、`execute-drafting-pass` 与 `execute-freeze-pass` 落地：从 `direction_screening` 到 `frozen` 的 author-side 主线现在都能直接投影为 landed command，而不再依赖 pending handoff。
- `build-hosted-contract-bundle` 导出的托管友好合同现在也已经收口成 schema-backed contract bundle，并为 future hosted / `OPL` caller 显式补出 `domain_entry_contract`、`schema_contract`、`authoring_contract`。
- 这份共享 `domain_entry_contract` 现在还会显式导出 `supported_commands` 与 `command_contracts`，因此外部 caller 已经可以直接按冻结合同拼 request，而不需要 repo-local helper。
- 未来兼容形态：如果核心 domain contract 不变，可迁移到同一 substrate 上的 managed web runtime。
- 当前理想目标也已经明确：`OPL` 继续是 family-level 顶层入口，`Hermes-Agent` 继续是 runtime substrate owner，`Med Auto Grant` 继续是 domain truth / authoring owner；其中 hosted caller / `OPL` consumption proof 现已完成，`P4.A / P4.B / P4.C / P4.D / P4.E / P4.F` 也都已经作为当前 repo-tracked shell / loop / executor tranche 落地，但完整的 mature direct grant product entry 仍是下一阶段。

## 入口分层与产品边界

当前 `Med Auto Grant` 已经有真实的 `operator entry`、`agent entry`，并且轻量结构化 `product entry` shell 已经落地。
但更完整的 grant-facing 产品体验仍要继续补。也就是说：

- `operator entry`：给人类操作同事使用的命令、workspace 准备、检查和显式 gate
- `agent entry`：由 `Codex` 或其他 host-agent 调用的 `CLI + MedAutoGrantDomainEntry`
- `product entry`：`build-product-entry` 现在已经把 direct entry 与 `OPL` handoff 共用的轻量结构化 shell 落到仓库里，但更完整的 grant-facing 产品体验仍要继续补
- `product frontdesk`：`product-frontdesk` 现在又把同一层 shell 上方的 controller-owned direct frontdoor 落到仓库里，而真实 operator loop 仍留在 `grant-user-loop`；它与 `product-entry-manifest` 现在都已经独立 schema-backed、generation-time fail-closed，配套 manifest/frontdesk 也会带出 `grant_authoring_readiness`、quickstart 以及 `build_submission_ready_package` 这个面向用户的本地交付动作，同时继续诚实暴露自动化成熟度、human gate 与 resume 语义
- `product preflight`：`product-preflight` 现在又把同一层 direct frontdoor 的诚实开机前检查落到仓库里，而配套 manifest/frontdesk 也会带出同一份 `product_entry_preflight` companion，供 machine-readable 调用方直接判断
- `product start`：`product-start` 现在又把同一层 shell 的统一启动面落到仓库里，会给出推荐模式、可选模式、resume surface 与 human gate 摘要，并与 manifest/frontdesk 保持同型
- `product projection`：`grant-progress` 与 `grant-cockpit` 现在已经以 schema-backed、generation-time fail-closed 的 contract surface 落第一层 controller-owned、read-only 的 direct-product projection，但它们故意不是新的 `domain_entry_contract` executor command，也不进入 hosted contract bundle 的 command catalog，更不等于成熟前台
- `direct entry composition`：`grant-direct-entry` 现在继续把 `grant-progress`、`grant-cockpit` 与 direct / `opl-handoff` 两份 `product_entry` envelope 收成一层 controller-owned 的 direct-entry 组合面，但它仍然不是新的 service-safe domain executor，也不进入 hosted contract bundle 的 command catalog
- `current user loop`：`mainline-status`、`mainline-phase` 与 `grant-user-loop` 现在会把 repo 主线快照、direct-entry composition 与 route-derived next action 收成当前 inbox-like CLI shell，但这仍然不等于成熟 Web 前台或 hosted runtime

目标中的 domain 级入口形态应是：

`User -> Med Auto Grant Product Entry -> MedAutoGrantDomainEntry -> Hermes Kernel -> Med Auto Grant Domain Harness OS`

而在更大的 `OPL` 家族入口里，应兼容：

`User -> OPL Product Entry -> OPL Gateway -> Hermes Kernel -> Domain Handoff -> Med Auto Grant Product Entry / MedAutoGrantDomainEntry`

这条 handoff 至少共享下面这组最小 envelope：

- `target_domain_id`
- `task_intent`
- `entry_mode`
- `workspace_locator`
- `runtime_session_contract`
- `return_surface_contract`

在这层共享 envelope 之上，`Med Auto Grant` 再补充 `workspace_id`、`draft_id`、`funding_call` 这些 grant domain payload。

这套共享 envelope 现在已经由 `build-product-entry` 在 `direct` 与 `opl-handoff` 两种模式下生成。
因此当前最诚实的判断是：Hermes-backed runtime substrate 与轻量 `product entry` shell 都已落地，但更完整的 grant-facing 产品体验仍要继续补。

## 执行句柄与持久表面

- `grant_run_id`：单次 hydrated grant run 的正式执行句柄
- `workspace_id`：当前 `NSFCWorkspace` 的持久聚合根身份
- `draft_id`：跨 critique / revision 延续的草稿身份，而不是每次 run 重新生成的 ID
- `program_id`：当前 Med Auto Grant active mainline 的 control-plane / report-routing 指针
- 当前 repo-verified 的 durable report / audit surface：`summarize-workspace`、`critique-summary`、`stage-route-report`
- 当前 controller-owned 的只读 product projection surface：`grant-progress` 与 `grant-cockpit`；它们只读取上面的 durable truth 和 `build-product-entry` 的 contract hint，由 `schemas/v1/grant-progress.schema.json` 与 `schemas/v1/grant-cockpit.schema.json` 冻结，并且故意不混入 `domain_entry_contract.supported_commands` 或 hosted contract bundle 的 command catalog
- 当前 controller-owned 的 direct-entry 组合面：`grant-direct-entry`；它会把上面的 projection 与 direct / `opl-handoff` 两份 `product_entry` envelope 组装到一起，由 `schemas/v1/grant-direct-entry.schema.json` 冻结，并且继续不混入 `domain_entry_contract.supported_commands` 或 hosted contract bundle 的 command catalog
- 当前 controller-owned 的 user-loop 组合面：`grant-user-loop`；它会把 `grant-direct-entry`、`mainline-status / mainline-phase` 与 route-derived next action 收在一起，由 `schemas/v1/grant-user-loop.schema.json` 冻结，并且继续不混入 `domain_entry_contract.supported_commands` 或 hosted contract bundle 的 command catalog
- 当前 repo-verified 的 runtime entry 还包括 `probe-upstream-hermes`、`run-local`、`resume-local`、`build-artifact-bundle`、`execute-revision-pass`、`build-final-package`、`build-hosted-contract-bundle`、`build-submission-ready-package` 与 `build-product-entry`；它们分别负责 upstream 依赖证明、本地主循环与恢复、artifact bundle 生产、section-level deterministic revision pass、本地 final package 导出、hosted-friendly contract bundle 导出、fail-closed 的本地 submission-ready 交付包导出，以及 direct / `OPL` handoff 共用的 product shell
- `build-hosted-contract-bundle` 现在会额外导出托管友好的 handoff contract，其中显式携带 `runtime_substrate_contract`、`runtime_state_contract`、`operator_contract`、`domain_entry_contract`、`schema_contract` 与 `authoring_contract`，连同 execution identity、artifact 与 audit surface 一起进入导出面
- `domain_entry_contract` 现在还会一起导出 `supported_commands` 与逐命令的 `command_contracts`，让 hosted caller / 外部 caller 能直接消费相同的 command catalog
- `stage-route-report` 当前还是 machine-readable 的 verification / checkpoint 聚合面，并会输出 `verification_checkpoint` 与 `checkpoint_status`
- `MedAutoGrantDomainEntry` 是当前 CLI 等价 runtime 调用的 service-safe structured adapter，也为 future gateway reuse 预留了同一条 contract
- repo-tracked review truth 与 local durable handoff surfaces 必须分开：前者负责解释 runtime contract，后者负责机器私有的恢复状态

## 它主要想帮你解决什么问题

- 判断一个方向到底是不是“真正的科学问题”，而不是工程任务或泛泛的临床需求。
- 把申请人画像、代表作、在研项目和预实验，组织进同一个可审计的基金工作区。
- 在花大力气写全文之前，先把“必要性与科学价值”这条主线磨清楚。
- 让“为什么是这个申请人来做这个问题”成为显式判断，而不是简历堆砌。
- 用“草稿扩写 + 导师式批注 + 结构化修订 + re-review 证据绑定”替代一次性文本生成。

## 现在已经能做什么

仓库现在已经有一套跑在真实上游 `Hermes-Agent` substrate 之上的 `CLI-first` runtime，同时把冻结的 `NSFCWorkspace` 契约与申请人侧 grant 语义继续保留在 repo-local domain modules 里。此前的 host-agent 线只保留为历史迁移桥 / regression oracle。

当前 runtime 已经可以：

- 通过 `probe-upstream-hermes` 显式证明已落地的 upstream substrate，包括 `hermes`、`hermes acp`、`run_agent.AIAgent`、`hermes_state.SessionDB` 与 `acp_adapter.session.SessionManager`
- 校验已 absorbed 的 `drafting -> critique -> revision` 主线，并保留 `major_reframe / major_revision / minor_revision / ready_for_submission` 的导师 verdict 分叉
- 在 CLI 输出中统一携带稳定的 `grant_run_id`，作为当前 hydrated grant run 的正式执行句柄
- 汇总 direction / question / fit mapping / draft / revision plan 的显式 `current_selection` 绑定
- 通过 `MentorCritique.reviewed_revision_plan_id` 把 re-review 批注显式绑定到上一轮 completed revision evidence
- 根据 `lifecycle_stage`、gates 与 verdict 给出 `major_reframe -> question_refinement`、`major_revision / minor_revision -> revision`、`ready_for_submission -> frozen`，以及 `revision(completed) -> critique -> revision` 的下一步建议
- 把当前 authoring route 聚合成单个 machine-readable `stage-route-report`
- 通过 `verification_checkpoint / checkpoint_status` 把当前 verification、forced rollback 与 frozen gate 语义收进同一个 checkpoint surface
- 输出带有 verdict、当前 `RevisionPlan.execution_status`、reviewed revision evidence、rollback / frozen gate 状态、版本标签和比较证据的 `critique-summary / stage-route-report` 审计面
- 通过 `grant-progress` 与 `grant-cockpit` 输出 direct grant 的 progress / cockpit 投影，复用 `summarize-workspace`、`stage-route-report`、`critique-summary` 与 `build-product-entry` 的合同信息，并把这两条投影面收口成 schema-backed、generation-time fail-closed 的 projection contract，而不新增 service-safe domain-entry executor command 或 hosted bundle command catalog 项
- 通过 `grant-direct-entry` 把 `grant-progress`、`grant-cockpit` 与 direct / `opl-handoff` 两份 `build-product-entry` envelope 收成一份 direct-entry 组合面，并把它收口成 schema-backed、generation-time fail-closed 的 product contract，而不新增 service-safe domain-entry executor command
- 通过 `mainline-status`、`mainline-phase` 与 `grant-user-loop` 暴露 repo 主线快照和当前 direct grant user loop，同时保持这些 surface 继续是 controller-owned，而不是新的 service-safe domain command
- 通过 `run-local` 运行一次 Hermes-backed 本地主循环、派生 machine-readable `stop_reason`、在 `stage_action_required` 分支上生成 machine-readable `stage_action_envelope`、写入 durable run journal、同时把 attempt durability 镜像进 upstream `SessionDB`，并通过 `resume-local` 从该 journal 恢复
- 通过 `build-artifact-bundle` 把当前已选方向、问题、论证链、适配度、提纲与草稿章节打包成 local `artifact_bundle`，并保留 manifest、lineage、version 与 `grant_run_id / workspace_id / draft_id` 身份一致性
- 通过 `execute-revision-pass` 对冻结在 `RevisionPlan` 中的 section-level deterministic mutation 执行本地 revision pass，并保持 draft lineage、rollback gate 与 checkpoint 语义不漂移
- 通过 `build-final-package` 把 freeze-ready / submission-frozen 的 workspace 与 artifact bundle 收成 machine-readable 本地 `final_package`
- 通过 `build-hosted-contract-bundle` 从当前 `final_package` 导出 hosted-friendly 的 session / state / artifact / audit contract bundle，作为托管化 prep 的本地合同产物，并显式携带 `domain_entry_contract`、`schema_contract` 与 `authoring_contract`
- 通过 `build-submission-ready-package` 在 frozen workspace 同时满足必备章节、预实验、代表作与在研项目条件时，一键导出 fail-closed 的本地 `submission_ready_package`
- 通过 hosted caller consumption proof 证明外部 caller 现在已经可以直接读取 `domain_entry_contract`、`schema_contract`、`authoring_contract`、`supported_commands` 与 `command_contracts`，并在不依赖 repo-local helper 的前提下完成已 landed export chain
- 通过 `MedAutoGrantDomainEntry` 把同一组 runtime command surface 暴露成 future gateway caller 可复用的 service-safe structured entry contract
- 通过 `build-product-entry` 构建轻量结构化 `product entry` shell，让 `direct` 与 `opl-handoff` 共用同一套 envelope
- 把已 landed 的 `product entry`、`product-entry-manifest`、`product-frontdesk`、`executor_routing_contract`、全链 authoring command surface 与 hosted contract bundle 一起冻成可供 future `OPL` / gateway 消费的 schema-backed contract

在当前 repo-tracked truth 下，旧的 host-agent 本地 ladder 内已经没有新的 concrete post-`R5.A` runtime delta 可继续隐式推进；因此当前主线前进方式是保持已 landed 的 upstream substrate、service-safe domain entry 与 author-side object boundary 持续全绿，而不是重新打开 repo-local runtime ownership。

## 现在还没有完成什么

下面这些能力仍处于后续 hardening 或 future scope：

- 当前本地 runtime 仍需继续做 submission-grade hardening 与更高判断密度的 authoring runtime 收束，但 canonical 本地 walkthrough 与 revised/final/hosted/submission-ready 输出一致性 truth 已冻结
- 任何进一步的 submission-grade hardening 或更强 authoring-runtime 结论，都需要先新增并冻结 repo-tracked truth，而不是继续沿用隐式的 post-`R5.A` hardening 叙事
- actual hosted runtime、remote execution、Web UI 与 multi-tenant 托管化
- 超出已 landed 轻量结构化 shell 之外、更完整的 grant-facing 产品体验
- 未来 `Human-in-the-loop` sibling 或 upper-layer product 相关表面
- 图件生成、Word/PDF 定稿与最终版式审查仍未产品化
- 外部官网提交流程仍未执行；当前已 landed 的范围止于本地 submission-ready package 导出
- submission-grade 自动驾驶质量与更强的端到端 authoring/runtime 稳定性
- 超出首个 `NSFC` 通用骨架之外的更多基金 family 扩展，以及 `P5` federation

## 最快开始方式：通过你的 Agent

对大多数医学用户来说，最快的入口不是先学习底层命令，而是先把你的申请材料和目标交给自己的 Agent，再让它调用 `Med Auto Grant`。

通常可以这样开始：

1. 准备申请人材料、代表性成果、在研项目、预实验结果和目标基金要求。
2. 让 Agent 先把这些材料整理成结构化、可审计的 grant workspace。
3. 再让 Agent 用 `Med Auto Grant` 去推进科学问题提纯、必要性链条收紧、草稿扩写、导师式批注、修订与 re-review 证据绑定。

如果你想先拿到统一的 machine-readable 启动面，再进入这条 grant loop，可以先读：

`uv run python -m med_autogrant product-start --input <workspace.json> --format json`

你可以直接把下面这段话发给 Agent：

> 请先读取这个工作区里的申请人材料、既有成果、在研项目、预实验结果和目标基金要求，并把它们整理成结构化、可审计的 grant workspace。然后使用 Med Auto Grant 作为医学 Grant Ops 主线来推进这份 NSFC 风格申请。请优先判断科学问题是否成立、必要性与科学价值是否足够、申请人与问题是否真正适配、草稿是否忠实继承已冻结问题、上一轮修订证据是否被当前批注显式承接，再进入 submission-facing 的更后段动作。如果当前方向偏弱，请及时止损、改题或指出缺失证据，而不是机械地把一条弱路线写到底。

## 公开文档

- [文档索引](./docs/README.zh-CN.md)
- [Domain Positioning](./docs/domain-positioning.zh-CN.md)
- [MVP Scope](./docs/mvp-scope.zh-CN.md)
- [轻量产品入口与 OPL Handoff](./docs/references/lightweight_product_entry_and_opl_handoff.md)

## 开发验证

```bash
uv sync --frozen
make test-full
```

本地测试分层入口：

- `make test-fast`：默认开发切片
- `make test-meta`：program control 与 repository hygiene 检查
- `make test-cli-smoke`：CLI 校验与本地 runtime smoke
- `make test-full`：clean-clone 基线使用的完整验证入口

<details>
<summary><strong>技术与 Agent 说明</strong></summary>

### 最小 Runtime 命令

```bash
TMPDIR="$(mktemp -d)"

# 当前 canonical CLI walkthrough（基于已落地的 upstream Hermes substrate）

# 0. 探测真实 upstream Hermes 入口与 runtime root
uv run python -m med_autogrant probe-upstream-hermes --format json

# 1. 对 critique workspace 做 baseline 审计
uv run python -m med_autogrant validate-workspace --input examples/nsfc_workspace_p2c_critique.json --format json
uv run python -m med_autogrant summarize-workspace --input examples/nsfc_workspace_p2c_critique.json --format json
uv run python -m med_autogrant next-step --input examples/nsfc_workspace_p2c_critique.json --format json
uv run python -m med_autogrant critique-summary --input examples/nsfc_workspace_p2c_critique.json --format json
uv run python -m med_autogrant stage-route-report --input examples/nsfc_workspace_p2c_critique.json --format json
uv run python -m med_autogrant mainline-status --format json
uv run python -m med_autogrant mainline-phase --phase current --format json
uv run python -m med_autogrant grant-progress --input examples/nsfc_workspace_p2c_critique.json --format json
uv run python -m med_autogrant grant-cockpit --input examples/nsfc_workspace_p2c_critique.json --format json
uv run python -m med_autogrant grant-direct-entry --input examples/nsfc_workspace_p2c_critique.json --task-intent tighten-grant-mainline --format json
uv run python -m med_autogrant grant-user-loop --input examples/nsfc_workspace_p2c_critique.json --task-intent tighten-grant-mainline --format json
uv run python -m med_autogrant product-start --input examples/nsfc_workspace_p2c_critique.json --format json
uv run python -m med_autogrant build-product-entry --input examples/nsfc_workspace_p2c_critique.json --entry-mode direct --task-intent tighten-grant-mainline --format json

# 2. 执行 deterministic local revision pass
uv run python -m med_autogrant execute-revision-pass --input examples/nsfc_workspace_p2c_critique.json --output "$TMPDIR/r3a-p2c-revised.json" --format json

# 3. 对 generated revised workspace 做 fresh validator / summary / route / checkpoint
uv run python -m med_autogrant validate-workspace --input "$TMPDIR/r3a-p2c-revised.json" --format json
uv run python -m med_autogrant summarize-workspace --input "$TMPDIR/r3a-p2c-revised.json" --format json
uv run python -m med_autogrant next-step --input "$TMPDIR/r3a-p2c-revised.json" --format json
uv run python -m med_autogrant critique-summary --input "$TMPDIR/r3a-p2c-revised.json" --format json
uv run python -m med_autogrant stage-route-report --input "$TMPDIR/r3a-p2c-revised.json" --format json

# 4. re-review revised output 也必须留在同一条本地 ladder 上
uv run python -m med_autogrant execute-revision-pass --input examples/nsfc_workspace_p3b_re_review_major_revision.json --output "$TMPDIR/r3a-p3b-revised.json" --format json
uv run python -m med_autogrant validate-workspace --input "$TMPDIR/r3a-p3b-revised.json" --format json
uv run python -m med_autogrant summarize-workspace --input "$TMPDIR/r3a-p3b-revised.json" --format json
uv run python -m med_autogrant next-step --input "$TMPDIR/r3a-p3b-revised.json" --format json
uv run python -m med_autogrant critique-summary --input "$TMPDIR/r3a-p3b-revised.json" --format json
uv run python -m med_autogrant stage-route-report --input "$TMPDIR/r3a-p3b-revised.json" --format json
uv run python -m med_autogrant build-artifact-bundle --input "$TMPDIR/r3a-p3b-revised.json" --output "$TMPDIR/r3a-p3b-revised-bundle.json" --format json
uv run python -m med_autogrant run-local --input "$TMPDIR/r3a-p3b-revised.json" --journal "$TMPDIR/r3a-p3b-revised-run.json" --format json

# 5. 本地 runtime 入口 / 恢复继续保持 CLI-first
uv run python -m med_autogrant run-local --input examples/nsfc_workspace_p2c_revision.json --journal "$TMPDIR/r1a-revision.json" --format json
uv run python -m med_autogrant resume-local --journal "$TMPDIR/r1a-revision.json" --format json

# 6. 本地 final / hosted-contract 产物链
uv run python -m med_autogrant build-artifact-bundle --input examples/nsfc_workspace_p3c_presubmission_frozen.json --output "$TMPDIR/r5a-bundle.json" --format json
uv run python -m med_autogrant build-final-package --input examples/nsfc_workspace_p3c_presubmission_frozen.json --artifact-bundle "$TMPDIR/r5a-bundle.json" --output "$TMPDIR/r5a-final-package.json" --format json
uv run python -m med_autogrant build-hosted-contract-bundle --final-package "$TMPDIR/r5a-final-package.json" --output "$TMPDIR/r5a-hosted-contract.json" --format json
```

### 当前技术范围

- 基于 schema 的 `NSFCWorkspace` 校验
- runtime / CLI 表面上显式区分 `grant_run_id`、`workspace_id` 与 `draft_id`
- `major_reframe / major_revision / minor_revision / ready_for_submission` 的 machine-readable verdict contract
- 通过 `active_revision_plan_id`、`reviewed_revision_plan_id` 与 `reviewed_revision_evidence` 冻结 machine-readable re-review linkage
- 通过 `forced_rollback_stage`、`forced_rollback_reason` 与 `presubmission_frozen` 冻结 machine-readable rollback / gate contract
- machine-readable 的批注、verdict 与 route artifact
- machine-readable 的 Hermes-backed runtime stop reason、stage-action envelope、durable run-journal recovery，以及 upstream `SessionDB` attempt durability
- 带有 manifest、lineage、version 与 bundle summary 的 machine-readable 本地 artifact bundle 生产
- section-level deterministic 本地 revision executor
- machine-readable 的本地 final package
- hosted-friendly session / state / artifact / audit contract bundle 导出
- fail-closed 的本地 submission-ready package 导出
- controller-owned、read-only 的 direct-product projection：`grant-progress` 与 `grant-cockpit`
- controller-owned 的主线快照 / 当前 user loop surface：`mainline-status`、`mainline-phase` 与 `grant-user-loop`
- 供 CLI 等价 runtime 调用复用的 service-safe structured domain entry
- 覆盖 runtime 与 control-surface 不变量的测试

### 内部文档

- 当前 fast-cutover truth：`/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-12-upstream-hermes-agent-fast-cutover-current-truth.md`
- 当前 lightweight product-entry truth：`/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-12-lightweight-product-entry-and-opl-handoff-current-truth.md`
- 当前 P4.A direct cockpit/progress truth：`/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-12-p4a-direct-grant-cockpit-and-progress-projection-current-truth.md`
- 当前 P4.C mainline status / user loop truth：`/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-12-p4c-mainline-status-and-grant-user-loop-current-truth.md`
- 当前 hosted caller consumption proof：`/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-12-hosted-caller-consumption-proof-current-truth.md`
- 当前真相重置总览：`/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-11-upstream-hermes-agent-truth-reset-current-truth.md`
- 历史本地 runtime program truth：`/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-11-hermes-backed-runtime-substrate-program-current-truth.md`
- 历史本地 runtime capability migration map：`/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-11-hermes-backed-runtime-capability-migration-map-current-truth.md`
- 当前 canonical post-R5A walkthrough truth：`/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-10-post-r5a-local-runtime-walkthrough-and-output-consistency-current-truth.md`
- 当前 post-R5A 本地 runtime 上限 closeout truth：`/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-11-post-r5a-local-runtime-upper-bound-honest-stop-current-truth.md`
- [`docs/domain-harness-os-positioning.md`](./docs/domain-harness-os-positioning.md)
- [`docs/specs/2026-04-06-med-auto-grant-top-level-design.md`](./docs/specs/2026-04-06-med-auto-grant-top-level-design.md)
- [`docs/specs/2026-04-06-nsfc-main-flow-and-critique-loop.md`](./docs/specs/2026-04-06-nsfc-main-flow-and-critique-loop.md)
- [`docs/specs/2026-04-06-object-model-schema-v1.md`](./docs/specs/2026-04-06-object-model-schema-v1.md)
- [`docs/specs/2026-04-07-p2c-draft-critique-revision-skeleton-mainline-current-truth.md`](./docs/specs/2026-04-07-p2c-draft-critique-revision-skeleton-mainline-current-truth.md)
- [`docs/specs/2026-04-07-p3a-mentor-verdict-contract-freeze-current-truth.md`](./docs/specs/2026-04-07-p3a-mentor-verdict-contract-freeze-current-truth.md)
- [`docs/specs/2026-04-08-p3b-revision-transition-and-re-review-hardening-current-truth.md`](./docs/specs/2026-04-08-p3b-revision-transition-and-re-review-hardening-current-truth.md)
- [`docs/specs/2026-04-08-p3c-forced-rollback-and-presubmission-gate-current-truth.md`](./docs/specs/2026-04-08-p3c-forced-rollback-and-presubmission-gate-current-truth.md)
- [`docs/specs/2026-04-09-post-r5a-local-runtime-hardening-brief.md`](./docs/specs/2026-04-09-post-r5a-local-runtime-hardening-brief.md)
- [`docs/specs/2026-04-10-post-r5a-revised-workspace-validator-and-operator-alignment.md`](./docs/specs/2026-04-10-post-r5a-revised-workspace-validator-and-operator-alignment.md)
- [`docs/history/omx/README.zh-CN.md`](./docs/history/omx/README.zh-CN.md)

### 本地运行状态

本地 operator 与 runtime 状态属于机器私有内容，不属于公开 GitHub 源码表面。
</details>
