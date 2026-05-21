# OPL-Aligned Ideal Target And Phase Map Current Truth

> 生命周期注记（`2026-05-17`）：这份 dated spec 是 path-stable 的历史/支撑记录；只有 `docs/specs/README.md`、`docs/specs/specs_lifecycle_map.md`、`docs/status.md` 或 `contracts/runtime-program/current-program.json` 明确指定的仍 current subsection 才可作为当前边界阅读。请先读取 `docs/status.md`、核心五件套与 `contracts/runtime-program/current-program.json`。本文中的旧 `Current Truth`、Hermes、OPL Gateway、host-agent 或 federation wording 只作 provenance，不是当前 default owner line。

Date: `2026-04-12`

## Activation Status

- Phase: `OPL-Aligned Target Shape Freeze`
- Active tranche: `Ideal target / phase map`
- Status: `superseded_reference`

当前阅读规则：本文只保留 2026-04-12 的 OPL 对齐历史快照。当前 MAG 目标态以 `docs/references/med-auto-grant-ideal-state.md`、`docs/active/mag-ideal-state-cross-repo-gap-plan.md`、核心五件套、`docs/specs/specs_lifecycle_map.md` 和 `contracts/runtime-program/current-program.json` 为准。下文旧 `Hermes Kernel`、`OPL Gateway`、`Domain Harness OS`、`runtime substrate owner` 等表述只作为 provenance 阅读，不是当前目标路线、默认 runtime owner 或 active compatibility interface。

## 文档目的

这份文档不声明新的 landed runtime。

它只解决两件事：

1. 按 `OPL` 与当前仓设计，明确 `Med Auto Grant` 的理想目标到底是什么。
2. 明确当前已经完成到哪个阶段、下一阶段应该推进什么、哪些还只是 future scope。

## 当前替代目标

按 `OPL` 对齐后的理想目标应固定为：

- `OPL`：stage-led、以 Agent executor 为最小执行单位的 family runtime framework，负责 provider-backed stage attempt、queue/wakeup、receipt/projection、shared lifecycle/index primitives 和 App/workbench shell。
- `Codex CLI`：当前第一公民 executor；其他 executor adapter 只能显式接入且不承诺行为效果等价。
- `Med Auto Grant Product Entry`：grant domain direct entry owner，与 OPL-hosted path 共享 MAG-owned descriptor/projection/receipt 边界。
- `Med Auto Grant`：author-side grant truth、fundability/quality verdict、route owner 与 export authority。

当前 direct user route 是：

`User -> Med Auto Grant Product Entry -> MedAutoGrantDomainEntry -> Codex CLI executor -> MAG grant truth / route / export surfaces`

当前 OPL-hosted route 是：

`User -> OPL stage-led framework / App shell -> provider-backed stage attempt -> MAG domain entry -> MAG owner receipt / typed blocker / artifact refs`

当前这条目标强调的是 owner split，而不是把所有能力混成同一个 runtime body。

## 历史快照

以下 P1/P2 描述是 2026-04-12 的历史快照，用于说明当时为什么形成 OPL 对齐计划。它不能覆盖当前 MAG docs taxonomy、runtime owner、executor boundary 或 direct retirement 规则。

## 当时已经完成的部分

### P1. Hermes substrate cutover

这阶段当前已完成：

- 真实 upstream `Hermes-Agent` substrate 已接住 runtime owner
- `runtime-run / runtime-resume` 与 attempt durability 已切到 Hermes session substrate
- `grant_run_id / workspace_id / draft_id / program_id` 边界保持 canonical
- `NSFCWorkspace`、critique / revision / final package / hosted contract bundle 没有漂移

### P2. service-safe domain contract convergence

这阶段当前也已完成：

- `MedAutoGrantDomainEntry` 已 landed
- `build-product-entry` 已 landed
- `executor_routing_contract` 已冻结
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

- `docs/history/specs/2026-04-12-hosted-caller-consumption-proof-current-truth.md`

## 更远阶段

### P4. mature direct grant product entry

更远的 future target 才是：

- 在同一 substrate 上形成更成熟的 direct grant product entry
- 让 grant-facing UX 成为 product layer，而不是重新发明 runtime owner

因此当前 `P4` 只能诚实写成：

- `next`

但 `P4` 现在已经有第一棒 landed：

- `P4.A direct grant progress / cockpit projection`

并且当前已经继续落到第二棒：

- `P4.B direct grant entry composition`

同时当前也已经继续落到第三棒：

- `P4.C mainline status and grant user loop`

这两条 tranche 当前只落：

- controller-owned
- read-only
- product-facing direct projection
- direct-entry composition

它不是：

- mature 前台
- 新的 service-safe domain entry executor
- actual hosted runtime

也就是说，当前宏观 phase map 继续保持：

- `P4` overall = `next`

而当前更细粒度的 honest 落点已经前进到：

- `P4.A landed`
- `P4.B landed`
- `P4.C landed`

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
