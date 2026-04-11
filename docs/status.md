# 当前状态

Date: `2026-04-11`

## 当前角色

- 仓库角色：医学 `Grant Ops` 的 author-side / proposal-facing `Domain Harness OS` 方向。
- 当前执行口径：本地 `CLI-first` runtime（上游 `Hermes-Agent` 尚未落地）。
- formal-entry matrix：`CLI` 是 formal entry，`MCP` 是 supported protocol layer，`controller` 是 internal surface。
- 当前主线：`Auto-only`。
- OMX 状态：已退场，仅保留历史入口。

## 当前基线（repo-verified）

- Latest absorbed runtime slice：`R5.A / Hosted-Friendly Session Boundary`
- Historical owner line：`post-R5A local runtime closeout / honest stop`
- Previous truthful closeout baseline：`NO_NEW_POST_R5A_LOCAL_RUNTIME_DELTA_HONEST_STOP`
- repo-tracked current truth 入口：
  - `contracts/runtime-program/current-program.json`
  - `docs/specs/2026-04-11-upstream-hermes-agent-truth-reset-current-truth.md`
  - `docs/specs/2026-04-07-formal-entry-matrix-current-truth.md`
  - `docs/specs/2026-04-07-durability-model-clarification.md`
  - `docs/specs/2026-04-10-post-r5a-local-runtime-walkthrough-and-output-consistency-current-truth.md`
  - `docs/specs/2026-04-11-post-r5a-local-runtime-upper-bound-honest-stop-current-truth.md`

## 当前阶段（active mainline）

- Current phase：`Truth Reset / Upstream Hermes-Agent Pilot Prep`
- Active tranche：`Local Runtime Honesty + Upstream Substrate Migration`
- Current owner line：`repo-local runtime baseline with upstream Hermes-Agent pending`

## 长线目标（规划层）

- 让上游 `Hermes-Agent` 成为新的产品 runtime substrate。
- 保留当前 `CLI-first + host-agent` 本地 runtime 作为已验证基线、兼容桥和回归 oracle，而不是长期终态。
- 在真实上游 substrate 上延续 `workspace -> critique -> revision -> final package -> hosted contract bundle` 这条 author-side grant mainline。

## 当前优先事项

1. 保持当前本地 runtime baseline、artifact/export surface 与 canonical CLI examples 持续全绿。
2. 继续把 CLI/runtime path 从 repo-local helper ownership 收紧到真实的上游 `Hermes-Agent` substrate，但不漂移 object boundary 与 authoring semantics。
3. 项目级 `.runtime-program/` 已退役；机器本地 session / log / report / prompt 统一迁到 `$CODEX_HOME/projects/med-autogrant/runtime-state/`。

## 默认验证

- 默认最小验证：`scripts/verify.sh`（`make test-fast`）。
- meta 验证：`scripts/verify.sh meta`。
- CLI smoke：`scripts/verify.sh cli-smoke`。
- full 验证：`scripts/verify.sh full`。
