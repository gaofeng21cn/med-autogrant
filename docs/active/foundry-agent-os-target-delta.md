# MAG Foundry Agent OS 目标差异页

Owner: `Med Auto Grant`
Purpose: `foundry_agent_os_target_delta`
State: `active_support`
Machine boundary: 本文是人读 target delta。机器真相继续归 `contracts/runtime-program/current-program.json`、MAG contracts/source/tests、owner receipts、typed blockers、workspace/runtime evidence，以及 OPL family `foundry_agent_os_standard` 合同。

## 读法

本文只回答 MAG 在 OPL family `Foundry Agent OS` 目标形态下“哪些上收到 OPL，哪些保留为 MAG authority kernel”。当前完成口径、证据门和执行顺序仍回到 [MAG 理想目标态差距与完善计划](./mag-ideal-state-cross-repo-gap-plan.md)；per-surface active caller 和物理退役门回到 [MAG 私有实现与 OPL 迁移台账](./opl-private-implementation-migration-inventory.md)。

机器落点是 `contracts/foundry-agent-os-domain-kernel-manifest.json`。该 manifest 固定 retained Grant Authority Kernel、OPL upcollect surfaces、`current_owner_delta` 默认读根、domain signer surfaces 和 false-authority flags；本文只做人读解释，不作为第二机器真相。

目标形态固定为：

```text
OPL Agent OS
  + Declarative Grant Pack
  + Grant Authority Kernel
  + Grant Capability Registry
```

这不是新 runtime，也不是 MAG 私有平台升级。它把 MAG 的通用运行、生成入口、状态投影、证据索引和 capability ABI 收回 OPL family 层，同时把 grant 判断和交付 authority 收窄到最小 kernel。

## 上收到 OPL

| 上收域 | OPL owner | MAG 侧保留 |
| --- | --- | --- |
| StageRun / runtime | Runway / Stagecraft | grant stage descriptors、allowed action refs、MAG owner receipt / typed blocker return shape |
| queue / attempt ledger / retry / dead-letter / human gate shell | Runway / Vault / Console | grant human gate identity、submission-ready blocker、MAG-owned gate answer |
| Pack compiler / generated CLI-MCP-App-status-workbench surfaces | Pack / Connect / Console | `agent/` Declarative Grant Pack、domain handler target、authority function refs |
| workspace/source/package/artifact lifecycle shell | Atlas / Runway / Vault | grant workspace truth refs、package/export authority refs、manual portal boundary |
| memory locator / receipt ledger / evidence lineage | Vault / Atlas | grant strategy memory body、accept/reject decision、owner receipt signer |
| operator cockpit / default next action | Console | MAG `current_owner_delta` answer shape：owner receipt、typed blocker、quality/export/package refs 或 no-regression evidence |
| capability catalog / ABI / use policy | Atlas / Pack / Stagecraft | grant-native capability declaration、safe action refs、capability-specific authority guard |

OPL 只能持有 refs、descriptor、generated surface、routing shell、ledger 和 projection。OPL / Vault / Console / Runway / Pack / Capability Registry 都不能写 grant truth、不能签 MAG owner receipt、不能创建 MAG typed blocker、不能授权 fundability / quality / export / submission verdict。

## 保留为 MAG Authority Kernel

MAG 必须保留：

- funding call 解释、profile/task lock、fundability strategy、specific aims 和 proposal route truth；
- grant stage pack、prompt/skill、policy table、transition oracle、quality/review/export gate；
- grant strategy memory body、accept/reject decision、writeback receipt 和 owner boundary；
- submission-ready package、manual portal boundary、package/export authority 和 owner receipt；
- typed blocker、safe action refs、no-forbidden-write guard 和 MAG domain projection refs；
- grant-native helper：只用于校验、物化、receipt signer、guard 或 refs projection，不生成 ready verdict。

这些 surface 不能被 schema completeness、scorecard 分数、package existence、provider completion、queue completion、generated surface parity 或 controller route 替代。

## 默认读根

MAG 的 OPL-hosted / App-facing 默认读根必须是 `current_owner_delta`：

```text
current owner -> current grant delta -> accepted answer shape -> hard gate / typed blocker
```

默认 operator view 不应从 raw worklist、evidence ledger、receipt count 或 provider completion 推导下一步。只有当前 owner delta 明确要求某个 route-required ref，且缺失会影响 source/data/evidence、owner-route identity、forbidden write、irreversible mutation、reviewer/publication hard gate 时，才升级为 MAG-owned typed blocker。其他 capability / evidence 缺口进入 advisory 或 audit，不阻断 grant 主线。

## 实施门

MAG 后续落地按下面的 gate 收口：

| Gate | 关闭条件 |
| --- | --- |
| Pack compile parity | OPL generated surfaces 能从 `agent/`、stage control、action catalog 和 MAG contracts 生成同一 command / descriptor / status shape。 |
| Default caller parity | direct path 与 OPL-hosted path 都回到同一 MAG owner receipt / typed blocker / no-regression return shape。 |
| No forbidden authority | OPL generated surface、Vault、Console、Runway、Capability Registry 不能写 grant body、memory body、package body、verdict body 或 owner receipt body。 |
| Physical thinning | product-entry、domain-handler、grouped CLI/API、projection、lifecycle、memory/package/status shell 的 active caller 迁出后直接退役或 tombstone，不保留 compatibility shell。 |
| Production evidence | App/operator sustained consumption、real workspace receipt scaleout、Temporal long-soak、submission-ready human gate 和 no-active-legacy-caller scan 形成真实证据。 |

## 禁止声明

- 不把 `Foundry Agent OS` target delta 写成 grant-ready、fundability-ready、quality-ready、export-ready、submission-ready 或 production-ready。
- 不把 generated surface parity、stage replay projection、external evidence ledger、package existence、scorecard 分数、provider completion 或 refs-only accounting 写成 MAG owner verdict。
- 不把 capability registry 写成 grant authority，也不把 optional capability ref 缺失写成默认 blocker。
- 不把 `current_owner_delta` projection 写成 owner answer；owner answer 必须来自 MAG authority kernel。
