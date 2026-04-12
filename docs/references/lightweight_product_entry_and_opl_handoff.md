# Med Auto Grant 轻量产品入口与 OPL Handoff

## 1. 当前真相

`Med Auto Grant` 现在已经有稳定的：

- `operator entry`
  - workspace 准备、检查、gate、调试
- `agent entry`
  - `CLI` / `MedAutoGrantDomainEntry`，由 `Codex` 或其他 host-agent 调用

同时，这个仓的 runtime substrate 已经真正落在上游 `Hermes-Agent` 上。

但即便如此，它仍然没有成熟的用户级 `product entry`。

## 2. 目标形态

这个仓理想中的 domain 级产品链路应是：

`User -> Med Auto Grant Product Entry -> MedAutoGrantDomainEntry -> Hermes Kernel -> Med Auto Grant Domain Harness OS`

在 `OPL` 家族级入口下，则应兼容：

`User -> OPL Product Entry -> OPL Gateway -> Hermes Kernel -> Domain Handoff -> Med Auto Grant Product Entry / MedAutoGrantDomainEntry`

这意味着：

- `OPL` 是 family-level 总入口
- `Med Auto Grant` 是 grant domain 自己的 lightweight direct entry
- runtime substrate 已经具备，当前剩下的是产品入口层和 handoff 层

## 3. 为什么现在重点不再是 runtime substrate

这个仓与另外两个业务仓不同：

- 真实 upstream `Hermes-Agent` substrate 已经 landed
- `MedAutoGrantDomainEntry` 已经 landed
- repo-side adapter 与 domain logic 也已经对齐

所以当前最主要的缺口已经不是“怎么让它跑在 Hermes 上”，而是：

- 怎么让用户能直接进入它
- 怎么让 `OPL` 能把任务平滑 handoff 给它
- 怎么在不改写 grant domain 语义的前提下，补出 product shell

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

## 5. 当前不应过度宣称的事

- 不能把 runtime substrate 已落地，误写成产品入口也已成熟
- 不能把 `MedAutoGrantDomainEntry` 直接等同成最终用户产品前台
- 不能把 `OPL -> Med Auto Grant` handoff 写成已经完整拥有最终 UX 的产品入口
- 不能为了赶产品入口，把 grant object boundary 和 authoring semantics 改乱

## 6. 下一步落地方向

1. 继续保持真实 upstream `Hermes-Agent` substrate 与 service-safe domain entry 全绿。
2. 在此基础上补 `Med Auto Grant Product Entry` shell。
3. 让 `OPL -> Med Auto Grant` handoff 与 direct entry 共用同一套结构化 envelope，而不是再起第二套入口语义。
