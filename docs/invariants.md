# 不变量

## Runtime 与 formal-entry

- formal-entry matrix 当前固定为：默认正式入口 `CLI`、支持协议层 `MCP`（future layer）、内部控制面 `controller`。
- 不得把 `supported_protocol_layer=MCP` 解释成“当前 public runtime 已正式支持 MCP”。
- 不得把 developer control-plane entry 的存在解释成“产品 controller 已正式支持”。
- 当前产品 runtime mainline 固定为 `CLI-first + Hermes-backed runtime substrate`。
- 旧 local host-agent runtime 只允许作为 compatibility bridge / regression oracle，不得继续写成长期产品 runtime。

## Control-plane 与 repo-tracked truth

- `contracts/runtime-program/current-program.json` 是 repo-tracked 的 current-program pointer。
- 项目级 `.runtime-program/` 已退役；机器本地 runtime state 统一迁到 `$CODEX_HOME/projects/med-autogrant/runtime-state/`。
- 项目级 `.codex/` 与 `.omx/` 已退役，不再作为仓库本地状态入口。
- 如需保留历史 session、prompt、log 或 hook 状态，应迁入用户级 `~/.codex/` 归档。
- repo-tracked current truth 以 `docs/specs/*current-truth.md` 与相关 activation package 为准。
- 当前 Hermes owner line 固定为 `Hermes-backed runtime substrate migration`。
- 历史 owner line 仍保留为 `post-R5A local runtime closeout / honest stop`，只作为旧 host-agent 线的 closeout anchor。
- `NO_NEW_POST_R5A_LOCAL_RUNTIME_DELTA_HONEST_STOP` 继续只作为旧 host-agent 线的历史 closeout baseline。
- 在没有新的 repo-tracked tranche truth 前，不得把当前 `R5.A` 之后的旧 host-agent runtime closeout 口径重新写回“还有默认续推中的 active delta”。

## 目标优先级

- 一旦新的 runtime substrate 目标已经明确，新增投入默认服务目标形态，而不是继续深磨已放弃的旧本地宿主路线。
- 当前 `CLI-first + host-agent runtime` 是 repo-verified baseline，但它只允许作为迁移桥、兼容层或回归 oracle 存在，不应再被误写为长期终态。
- 当前基线与长线目标并存时，必须在 `docs/status.md` 与 `docs/README*` 中显式拆开。

## 执行句柄边界

- `grant_run_id` 是执行句柄，不替代或污染 `workspace_id`、`draft_id`、`program_id`。
- 所有 CLI 输出必须保持句柄分离并稳定回显。

## 验证与审计

- 旧五个 canonical CLI surfaces 仍是 verifier/audit baseline。
- `stage-route-report` 是唯一 canonical route/checkpoint 聚合面，必须输出 `verification_checkpoint` 与 `checkpoint_status`。
- 最小验证入口是 `scripts/verify.sh`；默认执行 `make test-fast`，保留 `meta`、`cli-smoke`、`full` 分层 lane。

## 文档治理

- `AGENTS.md` 只管工作方式，不堆项目事实。
- 项目事实优先收敛到 `docs/project.md`、`docs/status.md`、`docs/architecture.md`、`docs/invariants.md`、`docs/decisions.md`。
- 历史 OMX 资料只从 `docs/history/omx/` 进入。
