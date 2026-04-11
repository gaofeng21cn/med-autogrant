# 不变量

## Runtime 与 formal-entry

- formal-entry matrix 当前固定为：默认正式入口 `CLI`、支持协议层 `MCP`（future layer）、内部控制面 `controller`。
- 不得把 `supported_protocol_layer=MCP` 解释成“当前 public runtime 已正式支持 MCP”。
- 不得把 developer control-plane entry 的存在解释成“产品 controller 已正式支持”。

## Control-plane 与 repo-tracked truth

- `.runtime-program/**` 是本地 operator control-plane，不是 repo-tracked 产品真相。
- repo-tracked current truth 以 `docs/specs/*current-truth.md` 与相关 activation package 为准。

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
