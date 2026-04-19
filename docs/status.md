# 当前状态

Date: `2026-04-18`

## 当前角色

- 仓库角色：`OPL` 顶层 GUI / management shell 下的一级医学基金 domain module / agent，负责 author-side grant truth、route、review gate 与 package export。
- 当前执行口径：Codex 是默认交互与执行路径；`Hermes-Agent` 是显式选择时的备用模式、长期在线网关与 proof lane。
- formal-entry matrix：`CLI` 是 formal entry，`MCP` 是 supported protocol layer，`controller` 是 internal surface。
- 当前主线：`Auto-only`。
- OMX 状态：已退场，仅保留历史入口。

## 当前入口

- 用户路径收口为 `product frontdesk` -> `product user-loop` -> `workspace progress / workspace cockpit` -> `product direct-entry` -> landed `pass` / `package` commands。
- `product build-entry` 与 lightweight `product entry` shell 继续作为 machine-readable domain/API catalog 的构建层。
- `product frontdesk` 是 controller-owned direct frontdoor contract，读取当前 user loop、projection 与 route truth，并通过 `product-frontdesk.schema.json` generation-time fail-closed 校验。
- `product direct-entry` 组合 `workspace progress`、`workspace cockpit` 与 direct / `opl-handoff` entry mode，是 controller-owned product contract。

## 当前执行线

- 当前公开执行线：`OPL shell + MAG domain agent + Codex default execution + Hermes-Agent backup gateway`
- 当前公开用户回路：`product frontdesk -> product user-loop -> workspace progress / workspace cockpit -> product direct-entry -> pass / package commands`
- 当前公开 CLI 入口面：`product build-entry`、`product manifest`、`product frontdesk` 与 `package submission-ready`
- 当前 controller-owned projection：`workspace progress`、`workspace cockpit`、`product direct-entry` 与 `product user-loop`
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
