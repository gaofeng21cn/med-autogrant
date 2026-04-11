# Med Auto Grant 硬约束

## Runtime 与 formal-entry

- formal-entry matrix 当前固定为：默认正式入口 `CLI`、支持协议层 `MCP`（future layer）、内部控制面 `controller`。
- 不得把 `supported_protocol_layer=MCP` 解释成“当前 public runtime 已正式支持 MCP”。
- 不得把 developer control-plane entry 的存在解释成“产品 controller 已正式支持”。

## Control-plane 与 repo-tracked truth

- `.runtime-program/**` 是本地 operator control-plane，不是 repo-tracked 产品真相。
- repo-tracked current truth 以 `docs/specs/*current-truth.md` 与相关 activation package 为准。

## 文档治理

- `AGENTS.md` 只管工作方式，不堆项目事实。
- 项目事实优先收敛到 `docs/project.md`、`docs/status.md`、`docs/architecture.md`、`docs/invariants.md`、`docs/decisions.md`。
- 历史 OMX 资料只从 `docs/history/omx/` 进入。

## 验证治理

- 最小验证入口是 `scripts/verify.sh`。
- `make test-fast` 是默认 smoke。
- `make test-meta` 与 `make test-cli-smoke` 是显式 lane。
- `make test-full` 是 clean-clone 基线。
