# 不变量

## Runtime 与 formal-entry

- `Med Auto Grant` 对外第一身份固定为独立 medical grant domain agent，不写成 `OPL` 内部 workspace 模块。
- `CLI` / `MedAutoGrantDomainEntry` 固定为 agent entry；`product entry/frontdesk/direct-entry/user-loop` 固定为 lightweight direct entry / projection。
- `gateway / harness` 继续保留为内部架构分层术语，不作为对外第一身份。
- formal-entry matrix 当前固定为：默认正式入口 `CLI`、支持协议层 `MCP`（future layer）、内部控制面 `controller`。
- 不得把 `supported_protocol_layer=MCP` 解释成“当前 public runtime 已正式支持 MCP”。
- 不得把 developer control-plane entry 的存在解释成“产品 controller 已正式支持”。
- 当前可执行 runtime mainline 固定为 `CLI-first + real upstream Hermes-Agent runtime substrate`。
- 历史 local host-agent runtime 材料只允许作为归档追溯材料，不得继续写成当前产品 runtime。
- 当前 `hermes_runtime.py` 与 `domain_entry.py` 只允许被写成 repo-side domain adapter / entry adapter，不得再被误写成 runtime substrate owner。

## Control-plane 与 repo-tracked truth

- `contracts/runtime-program/current-program.json` 是 repo-tracked 的 current-program pointer。
- 项目级 `.runtime-program/` 已退役；机器本地 runtime state 统一迁到 `$CODEX_HOME/projects/med-autogrant/runtime-state/`。
- 项目级 `.codex/` 与 `.omx/` 已退役，不再作为仓库本地状态入口。
- 如需保留历史 session、prompt、log 或 hook 状态，应迁入用户级 `~/.codex/` 归档。
- repo-tracked current truth 以 `docs/specs/*current-truth.md` 与相关 activation package 为准。
- 当前 owner line 固定为“CLI-first with real upstream Hermes-Agent runtime substrate”。
- 历史 closeout label 与 baseline 只保留在归档 current-truth 材料中；核心五件套不再把它们写成当前 owner line。
- 在没有新的 repo-tracked tranche truth 前，不得把旧 host-agent runtime closeout 材料重新写回“还有默认续推中的 active delta”。

## 目标优先级

- `OPL` 当前固定只承担 family-level session/runtime/projection 与 shared modules/contracts/indexes，不承担本仓 domain truth owner 身份。
- 一旦新的 runtime substrate 目标已经明确，新增投入默认服务目标形态，而不是继续深磨已放弃的旧本地宿主路线。
- 当前 `CLI-first + host-agent runtime` 是历史 repo-verified baseline，但它只允许留在归档追溯材料中，不应再被误写为长期终态。
- 当前 Hermes substrate 已落地主线时，不得把 repo-side adapter 重新写回“runtime 仍由本地 helper 主责”。
- 当前 landed substrate、兼容桥与 future scope 必须在 `docs/status.md` 与 `docs/README*` 中显式拆开。

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
