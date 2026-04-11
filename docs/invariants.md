# 不变量

## 入口与控制面

- CLI 是当前唯一正式 runtime formal entry。
- `MCP` 与 `controller` 仅保留为 not-yet-supported / internal surfaces，不得被描述成已开放入口。
- `.runtime-program/**` 是本地控制面，不是产品 runtime，也不是 repo-tracked truth。

## 执行句柄边界

- `grant_run_id` 是执行句柄，不替代或污染 `workspace_id`、`draft_id`、`program_id`。
- 所有 CLI 输出必须保持句柄分离并稳定回显。

## 验证与审计

- 旧五个 canonical CLI surfaces 仍是 verifier/audit baseline。
- `stage-route-report` 是唯一 canonical route/checkpoint 聚合面，必须输出 `verification_checkpoint` 与 `checkpoint_status`。

## 文档层次

- 核心骨架文档与 activation package/current truth 严格分层。
- `docs/specs/**` 承载 current truth 与 activation package，`docs/plans/**` 仅保留历史规划。
