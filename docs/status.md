# 当前状态

Date: `2026-04-18`

## 当前角色

- 仓库角色：`OPL` 是位于 MAG 之上的 family gateway 与 handoff surface；`Med Auto Grant` 负责 author-side grant truth、route、review gate 与 package export。
- 当前执行口径：`Hermes-Agent` 作为外部 runtime substrate owner 持有长期在线与 proof 语义；repo-side grant adapter 继续持有 direct entry、route contract 与导出边界。
- formal-entry matrix：`CLI` 是 formal entry，`MCP` 是 supported protocol layer，`controller` 是 internal surface。
- 当前主线：`Auto-only`。
- OMX 状态：已退场，仅保留历史入口。

## 当前入口

- 用户路径收口为 `product frontdesk` -> `product user-loop` -> `workspace progress / workspace cockpit` -> `product direct-entry` -> landed `pass` / `package` commands。
- `product build-entry` 与 lightweight `product entry` shell 继续作为 machine-readable domain/API catalog 的构建层。
- `product frontdesk` 是 controller-owned direct frontdoor contract，读取当前 user loop、projection 与 route truth，并通过 `product-frontdesk.schema.json` generation-time fail-closed 校验。
- `product direct-entry` 组合 `workspace progress`、`workspace cockpit` 与 direct / `opl-handoff` entry mode，是 controller-owned product contract。
- `mainline status` 负责 current line / current focus / completed records / remaining gaps；`mainline phase` 继续保留为维护者参考记录查询。

## 当前执行线

- 当前公开执行线：`direct MAG entry / OPL handoff -> product frontdesk -> product user-loop -> workspace progress / workspace cockpit -> product direct-entry -> pass / package commands`
- 当前公开用户回路：`product frontdesk -> product user-loop -> workspace progress / workspace cockpit -> product direct-entry -> pass / package commands`
- 当前公开 CLI 入口面：`product build-entry`、`product manifest`、`product frontdesk` 与 `package submission-ready`
- 当前 controller-owned projection：`workspace progress`、`workspace cockpit`、`product direct-entry` 与 `product user-loop`
- 当前 repo 级投影：`mainline status` 输出 current line / current focus；`mainline phase` 只承担维护者参考记录。
- `pass critique --executor hermes_native_proof` 继续作为显式 proof lane；默认执行器继续保持 `Codex CLI autonomous executor`

## 默认验证

- 最小验证：`scripts/verify.sh`
- meta 验证：`scripts/verify.sh meta`
- CLI smoke：`scripts/verify.sh cli-smoke`
- full 验证：`scripts/verify.sh full`

## 参考入口

- 当前技术记录：`docs/specs/` 与 `contracts/runtime-program/current-program.json`
- 追溯记录：`docs/references/` 与 `docs/history/`
- 当前规范与边界：`docs/architecture.md`、`docs/invariants.md`、`docs/decisions.md`
