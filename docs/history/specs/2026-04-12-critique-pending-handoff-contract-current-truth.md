# Critique Pending Handoff Contract Current Truth (Historical, Superseded)

> 生命周期注记（`2026-05-25`）：这份 dated spec 已归档为 `historical_handoff_snapshot`，只保留 2026-04-12 critique 仍被误读为 pending / handoff-required 时的历史状态。当前 critique route truth、Codex CLI executor boundary、quality gate 与机器行为回到 active specs、contracts/schema/source、CLI/API 行为和 `contracts/runtime-program/current-program.json`。

Owner: `Med Auto Grant`
Purpose: `historical_critique_pending_handoff_snapshot`
State: `history`
Machine boundary: 本文是人读历史 spec，保留 critique pending handoff 的 superseded snapshot。当前 critique executor truth 以 `docs/specs/2026-04-13-critique-codex-cli-executor-current-truth.md`、核心五件套、`docs/specs/specs_lifecycle_map.md`、contracts、schemas、source、CLI/API 行为与 `contracts/runtime-program/current-program.json` 为准。

Date: `2026-04-12`

## Historical Status

- Phase: `Upstream Hermes-Agent Fast Cutover`
- Recorded at: `2026-04-12`
- Current status: `historical note / superseded`

## Note

本文件记录的是 `2026-04-12` 时点，`critique` 仍被当作 `pending / handoff-required` 的历史冻结状态。

它已经被下面这份 current truth supersede：

- `docs/specs/2026-04-13-critique-codex-cli-executor-current-truth.md`

当前 repo-tracked truth 不再是 `critique-pending-handoff`，而是：

- `critique -> execute-critique-pass`
- `route_status = landed`
- `Codex CLI autonomous executor`
- `default model / reasoning = inherit_local_codex_default`

保留这个文件的唯一目的，是给后续审计与迁移追踪提供历史上下文，而不是继续充当当前真相入口。
