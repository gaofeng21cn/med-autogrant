# OPL-Aligned Ideal Target And Phase Map Current Truth

Date: `2026-04-12`

## Activation Status

- Phase: `OPL-Aligned Target Shape Freeze`
- Active tranche: `Ideal target / phase map`
- Status: `landed / current truth`

## 文档目的

这份文档不声明新的 landed runtime。

它只解决两件事：

1. 按 `OPL` 与当前仓设计，明确 `Med Auto Grant` 的理想目标到底是什么。
2. 明确当前已经完成到哪个阶段、下一阶段应该推进什么、哪些还只是 future scope。

## 理想目标

按 `OPL` 对齐后的理想目标应固定为：

- `OPL`：family-level 顶层入口与 gateway owner
- `Med Auto Grant Product Entry`：grant domain direct entry owner
- `Hermes-Agent`：runtime substrate owner
- `Med Auto Grant`：author-side grant truth / route / export owner

理想 direct user route 是：

`User -> Med Auto Grant Product Entry -> MedAutoGrantDomainEntry -> Hermes Kernel -> Med Auto Grant Domain Harness OS`

理想 family-level route 是：

`User -> OPL Product Entry -> OPL Gateway -> Hermes Kernel -> Domain Handoff -> Med Auto Grant Product Entry / MedAutoGrantDomainEntry`

当前这条目标强调的是 owner split，而不是把所有能力混成同一个 runtime body。

## 当前已经完成的部分

### P1. Hermes substrate cutover

这阶段当前已完成：

- 真实 upstream `Hermes-Agent` substrate 已接住 runtime owner
- `run-local / resume-local` 与 attempt durability 已切到 Hermes session substrate
- `grant_run_id / workspace_id / draft_id / program_id` 边界保持 canonical
- `NSFCWorkspace`、critique / revision / final package / hosted contract bundle 没有漂移

### P2. service-safe domain contract convergence

这阶段当前也已完成：

- `MedAutoGrantDomainEntry` 已 landed
- `build-product-entry` 已 landed
- `executor_routing_contract` 已冻结
- `pending_handoff_requirements` 已冻结
- `build-hosted-contract-bundle` 已显式导出 `domain_entry_contract`、`schema_contract`、`authoring_contract`
- `product_entry` 与 hosted bundle 都已经 schema-backed、fail-closed

因此当前可以诚实写成：

- `P1` completed
- `P2` completed

## 下一阶段

### P3. hosted caller / OPL consumption proof

这阶段当前也已完成。

当前已经 landed 的事实是：

- external hosted caller / future `OPL` caller 可以直接消费：
  - `domain_entry_contract`
  - `schema_contract`
  - `authoring_contract`
- `domain_entry_contract` 现在还会显式导出：
  - `supported_commands`
  - `command_contracts`
- external caller 可以只按冻结合同构造 request，而不需要 repo-local helper
- direct entry 与 family-level handoff 继续共用同一份 contract truth
- pending route 的 owner 与状态没有被改写

因此当前 `P3` 的 honest status 应更新为：

- `completed`

相关 proof 现已冻结在：

- `docs/specs/2026-04-12-hosted-caller-consumption-proof-current-truth.md`

## 更远阶段

### P4. mature direct grant product entry

更远的 future target 才是：

- 在同一 substrate 上形成更成熟的 direct grant product entry
- 让 grant-facing UX 成为 product layer，而不是重新发明 runtime owner

因此当前 `P4` 只能诚实写成：

- `next`

## 不在本线内的事

这份理想目标与阶段图不允许偷带：

- `P5` federation / platform story 扩写
- future `Human-in-the-loop` sibling
- new grant family expansion
- actual hosted runtime 已完成
- `OPL Gateway` 已在本仓落地

## 当前结论

当前 phase map 应固定为：

- `P1` completed
- `P2` completed
- `P3` completed
- `P4` next

这份 phase map 是当前 repo-tracked honest target，不是 overclaim。
