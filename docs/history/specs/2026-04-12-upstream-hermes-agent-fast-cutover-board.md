# Upstream Hermes-Agent Fast Cutover Board

> 生命周期注记（`2026-05-17`）：这份 dated spec 是已物理归档到 `docs/history/specs/` 的 `retired_provider_proof`。请先读取 `docs/status.md`、核心五件套、`docs/specs/specs_lifecycle_map.md` 与 `contracts/runtime-program/current-program.json`。本文中的旧 `Current Truth`、Hermes、OPL Gateway、host-agent 或 federation wording 只作 provenance，不是当前 default owner line。

Owner: `Med Auto Grant`
Purpose: `historical_upstream_hermes_fast_cutover_board_provenance`
State: `history`
Machine boundary: 本文是人读历史 spec，保留 2026-04-12 upstream Hermes-Agent fast cutover board 与 proof-lane planning。当前 default runtime owner、OPL/Temporal provider、executor adapter、hosted caller boundary 与机器行为以核心五件套、`docs/specs/README.md`、`docs/specs/specs_lifecycle_map.md`、contracts、schemas、source、CLI/API 行为与 `contracts/runtime-program/current-program.json` 为准。

状态锚点：`2026-04-12`

## 2026-05 后读取守卫

本文是 2026-04-12 fast-cutover board，不是当前可执行 baton。下文的 “real upstream Hermes-Agent runtime substrate”、`runtime-run`、`runtime-resume`、local run journal、`OPL Gateway` 和 hosted-friendly session boundary 只能作为 retired provider proof / planning provenance 阅读。当前默认 task runtime owner 是 OPL/Temporal；MAG 不实现 daemon、scheduler、attempt loop 或 attempt ledger；`hermes_agent` 只保留为显式非默认 executor / proof / provenance lane。

当前 active domain-entry 和 grouped public CLI catalog 不包含 `run-local`、`runtime-run`、`runtime-resume` 或 `probe-upstream-hermes`。本文的 F1-F4 completed 与长线 Codex 提示词不再作为当前 implementation queue、compatibility target、provider owner、Gateway/federation readiness、production readiness 或 physical-delete authority。

## 文档目的

这份文档把 `Med Auto Grant` 从“已可运行的本地 `CLI` runtime 基线”切到“真实上游 `Hermes-Agent` runtime substrate”的最快路径冻结下来。

它不再继续围绕旧本地 runtime 做无限硬化，而是要求：

- 以当前本地基线为回归 oracle
- 尽快把真正的 runtime substrate owner 切到上游 `Hermes-Agent`

## 一句话目标

把当前：

- `CLI-first + repo-local runtime baseline`

切成：

- `CLI-first + real upstream Hermes-Agent runtime substrate`

同时保留 author-side grant domain truth：

- `NSFCWorkspace`
- critique / revision / final package
- grant-specific gate / audit / export semantics

## 成功条件

只有同时满足下面几项，才可以把这条线写成完成：

1. 能给出真实上游 `Hermes-Agent` 依赖与连接证据。
2. `runtime-run`、`runtime-resume`、local run journal、session / resume / interrupt / recovery、hosted-friendly session boundary 不再由 repo-local helper 自己主责。
3. `grant_run_id`、`workspace_id`、`draft_id`、`program_id`、`critique-summary`、`stage-route-report`、`artifact bundle / final package / hosted contract bundle` 继续保持 canonical。
4. 形成可被未来 `OPL Gateway` 调用的 service-safe domain entry surface。

## 明确排除范围

本线不做：

- 新 grant family 扩面
- `P5` federation / platform 故事扩写
- future `Human-in-the-loop` sibling
- 把 repo-local helper 写成已完成上游接管

## 固定阶段顺序

### F1. 真实 Hermes substrate 接入证据

先冻结：

- external / upstream `Hermes-Agent` 依赖
- profile / runtime root
- session substrate
- repo-side adapter / client proof

### F2. Local runtime ladder 迁到 Hermes substrate

把当前本地梯子切过去：

- `runtime-run`
- `runtime-resume`
- local run journal / stop reason
- revision pass / final package / hosted contract bundle 所需的 session / run substrate

### F3. Domain entry adapter 收口

形成一个 service-safe domain entry：

- 保留 `CLI`
- 为未来 `OPL Gateway` 预留稳定 adapter / entry contract
- 不先做自然语言壳

### F4. End-to-end fresh proof

至少证明：

- critique
- revision
- final package
- hosted contract bundle

已经能在真实 `Hermes-Agent` substrate 上跑通，且 object boundary 不漂移。

## 当前落点（2026-04-12）

当前这条 fast cutover board 可以诚实视为已完成：

- `F1` completed
- `F2` completed
- `F3` completed
- `F4` completed

但这不等于整个理想目标已经完成。

按新的 `OPL` 对齐 phase map，当前主线位置应理解为：

- `P1 Hermes substrate cutover`：completed
- `P2 service-safe domain contract convergence`：completed
- `P3 hosted caller / OPL consumption proof`：next
- `P4 mature direct grant product entry`：future

因此，board 完成后的正确下一棒已经不再是继续深磨 repo-local runtime，也不是直接把 `OPL Gateway` / hosted runtime 写成 landed。

当前已完成的下一棒是：

- `P3 hosted caller / OPL consumption proof`

而当前继续前进的 honest 落点是：

- `P4.A direct grant progress / cockpit projection`
- `P4.B direct grant entry composition`
- `P4.C mainline status and grant user loop`

这条 `P4.A` 的定位必须固定为：

- controller-owned
- read-only
- product-facing direct projection

而不是：

- 新的 service-safe domain entry executor
- repo-local hosted helper
- mature Web UI / hosted runtime

## 默认验证

- `scripts/verify.sh meta`
- `scripts/verify.sh cli-smoke`
- full canonical example walkthrough
- 真实 `Hermes-Agent` substrate proof

## 长线 Codex 提示词

以下提示词只保留为历史 planning artifact，不是当前可执行 agent baton；其中 `docs/specs/2026-04-11-*` / `docs/specs/2026-04-12-*` 路径和 `OPL Gateway` / upstream Hermes 默认 owner 语义已由当前核心五件套、history specs index、active specs index 与 `current-program.json` 接管。

> 你现在负责 `Med Auto Grant` 的 `upstream Hermes-Agent fast cutover` 主线。先完整读取并遵守：`AGENTS.md`、`README.md`、`docs/project.md`、`docs/status.md`、`docs/architecture.md`、`contracts/runtime-program/current-program.json`、`docs/specs/2026-04-11-upstream-hermes-agent-truth-reset-current-truth.md`、`docs/specs/2026-04-12-upstream-hermes-agent-fast-cutover-board.md`。你的目标不是继续深磨 repo-local runtime，也不是继续发明新的本地 helper；你的目标是以最快速度把真实上游 `Hermes-Agent` 接成运行 substrate，同时保持 `NSFCWorkspace`、critique / revision / final package / hosted contract bundle 这条 author-side grant mainline不漂移。你必须按 board 顺序自行推进：先冻结真实上游连接证据，再把 local runtime ladder 迁到 Hermes substrate，再收口 service-safe domain entry，再做 end-to-end fresh proof。你可以自己写 activation package、docs、tests、contracts，并在每个 honest tranche 完成后直接 absorb 到 `main`、提交、push、继续下一棒；不要因为完成一个小 tranche 就停车。只有遇到真实硬 blocker 才允许停下，例如：外部安装/凭证/运行环境必须由用户提供，或继续前进会造成 truth drift。禁止做的事：把 repo-local helper 继续写成已接入上游、提前扩 family、提前做 Human-in-the-loop sibling、提前讲平台 federation 故事。
