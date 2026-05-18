# Med Auto Grant 轻量产品入口与 OPL Handoff

> 历史参考说明：当前 landed route catalog 与 direct-entry truth 已归 `docs/project.md`、`docs/decisions.md` 和 `contracts/runtime-program/current-program.json` 持有。
>
> 当前阅读注记：本文中的 `Hermes Kernel`、`OPL Runtime Manager` 与 `OPL family orchestration surface` 等旧表述，应按当前链路理解为 `OPL stage-led runtime framework with Agent executors as the minimum execution unit -> MAG projection/descriptor -> Med Auto Grant Product Entry / MedAutoGrantDomainEntry`。除非活跃合同显式选择其他 provider，`Codex CLI` 是默认最小执行单元。OPL 可以托管、调度、唤醒、handoff、receipt、retry 和投影 MAG stage，但不持有 MAG grant truth、authoring semantics、quality gates 或 submission-ready export truth。

## 1. 当前真相

`Med Auto Grant` 现在已经有稳定的：

- `operator entry`
  - workspace 准备、检查、gate、调试
- `agent entry`
  - `CLI` / `MedAutoGrantDomainEntry`，由 `Codex` 或其他 host-agent 调用

同时，这个历史文档里的 runtime substrate 口径已经被后续 OPL stage-led runtime framework 决策取代；MAG 当前默认正文执行仍继承 `Codex CLI`，OPL 侧负责 stage lifecycle、唤醒、队列、handoff、receipt、retry 和 projection。

在此基础上，`product build-entry` 已经把轻量结构化 `product entry` shell 落到仓库里，并让 `direct` 与 `opl-handoff` 共用同一套 envelope。
但即便如此，它仍然不等于成熟的用户级 `product entry` 或完整最终 UX。
当前在这层 shell 之上，`workspace progress / workspace cockpit` 已经先落了只读 projection，而 `product direct-entry` 也已经进一步把 projection + direct / `opl-handoff` envelope 收成一份 direct-entry composition contract。

## 2. 目标形态

这个仓理想中的 domain 级产品链路应是：

`User or agent caller -> Med Auto Grant Product Entry -> MedAutoGrantDomainEntry -> OPL explicit provider or Codex CLI executor -> Med Auto Grant domain logic`

在 `OPL` 家族级入口下，则应兼容：

`User or agent caller -> OPL Product Entry -> OPL stage-led runtime framework -> Domain Handoff -> Med Auto Grant Product Entry / MedAutoGrantDomainEntry`

按当前口径，上面两条历史链路里的 `Hermes Kernel` / `OPL Runtime Manager` 应理解为 OPL stage-led runtime framework 的 provider-specific 或历史实现记录；`OPL family orchestration surface` 应理解为 OPL 对外部 domain agent 的托管、投影和 handoff，不接管 MAG grant truth。Temporal / Hermes 只在显式 provider 或 proof lane 中出现。

这意味着：

- `Med Auto Grant` 是独立 grant domain agent，可 direct entry，也可被 `OPL` 托管和投影。
- `OPL` 只保留 family-level session/runtime/projection 与 shared modules/contracts/indexes
- runtime substrate 已经具备，当前剩下的是产品入口层和 handoff 层

## 3. 为什么现在重点不再是 runtime substrate

这个仓与另外两个业务仓不同：

- 真实 upstream `Hermes-Agent` substrate 已经 landed
- `MedAutoGrantDomainEntry` 已经 landed
- repo-side adapter 与 domain logic 也已经对齐

所以当前最主要的缺口已经不是“怎么让它跑在 Hermes 上”，而是：

- 怎么围绕已 landed 的 `product build-entry` shell 做更完整的 direct-entry 编排
- 怎么让 `OPL` 能稳定消费这份 handoff envelope
- 怎么在不改写 grant domain 语义的前提下，继续补产品层而不是偷换成熟度

当前 `product direct-entry` 已经完成的是：

- 一次性带出 `workspace progress`
- 一次性带出 `workspace cockpit`
- 一次性带出 direct / `opl-handoff` 两份 `product_entry`

但它仍然不是 mature 前台，也不是新的 domain executor。

## 4. 共享 handoff envelope

`OPL -> Med Auto Grant` 至少共享下面这组最小字段：

- `target_domain_id`
- `task_intent`
- `entry_mode`
- `workspace_locator`
- `runtime_session_contract`
- `return_surface_contract`

在这层公共 envelope 之上，grant 域继续补充：

- `workspace_id`
- `draft_id`
- `funding_call`
- `executor_routing_contract`

其中 `executor_routing_contract` 当前至少要把：

- `current_stage_route`
- `recommended_executor_route`
- `author_side_route_catalog`

显式带出来。`direction_screening -> frozen` 这一组 author-side route 现已全部进入 landed command catalog，旧的 `handoff_requirements` 假设只保留为历史形成过程。

## 5. 当前不应过度宣称的事

- 不能把 runtime substrate 已落地，误写成产品入口也已成熟
- 不能把 `MedAutoGrantDomainEntry` 直接等同成最终用户产品前台
- 不能把 `OPL -> Med Auto Grant` handoff 写成已经完整拥有最终 UX 的产品入口
- 不能为了赶产品入口，把 grant object boundary 和 authoring semantics 改乱

## 6. 下一步落地方向

1. 继续保持真实 upstream `Hermes-Agent` substrate、service-safe domain entry 与 `product build-entry` 全绿。
2. 让 `OPL -> Med Auto Grant` handoff 与 direct entry 持续共用同一套结构化 envelope，而不是再起第二套入口语义。
3. 继续把 critique / revision / export 的 executor route truth 显式冻结到同一份 `executor_routing_contract`，不让 `pending` route 偷偷漂成“已 landed”。
4. 在轻量结构化 shell 已 landed 的前提下，仍然克制表述成熟度，不把它写成完整最终 UX。
