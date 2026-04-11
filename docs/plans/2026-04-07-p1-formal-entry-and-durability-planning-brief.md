# P1 Planning Brief：Formal Entry Matrix Freeze 与 Durability Model Clarification

Date: `2026-04-07`

> Historical / completed planning brief：该 brief 对应的 `P1` 规划冻结已完成，现已被 `formal-entry matrix current truth` 与 `durability model clarification` 吸收，不再代表当前 active runtime productization program。

## 目标

本 brief 只冻结下一阶段规划边界，不进入任何实现。

当前 `P1` 只允许解决两件事：

1. `formal entry matrix freeze`
2. `durability model clarification`

## P1 要解决什么

### 1. formal entry matrix freeze

要把当前仓的正式入口矩阵写成单独、可 review、可回归的 current truth，至少明确：

- 当前哪些入口是**正式支持**
- 当前哪些入口只是**future scope**
- 每个入口各自面向：
  - user-facing runtime entry
  - developer control-plane entry
  - recovery / resume entry

当前预期需要冻结的最小结论是：

- user-facing runtime formal entry：当前仅正式支持 `CLI`
- developer control-plane durable entry：`OMX_TEAM_PROMPT + CURRENT_PROGRAM + PROGRAM_ROUTING + active plans + active reports`
- `MCP / controller`：当前仍是 future scope，不得在 `P1` 内伪装成已实现能力

### 2. durability model clarification

要把当前仓的 durable surface 分层写清楚，至少明确：

- 哪些是 repo-tracked review surfaces
- 哪些是 local durable handoff surfaces
- 哪些状态必须 repo-native 才能成为 review truth
- 哪些状态可以继续只留在 `.runtime-program/**`
- `grant_run_id / workspace_id / draft_id / program_id` 分别落在哪一层语义里

这里要解决的不是“把 `.omx` 改成 tracked”，而是把：

- repo review truth
- local handoff truth
- runtime object identity
- control-plane pointer identity

这四类东西的边界写清楚。

## P1 不解决什么

P1 明确不做：

- 不进入 `P1` 开发实现
- 不扩 `MCP`
- 不扩 `controller`
- 不做 `write / export / HITL` skeleton
- 不扩 runtime 能力面
- 不新增 grant family
- 不改 `.omx` / `.codex` 的跟踪策略
- 不把 current CLI baseline 重新包装成 submission-grade runtime

## 进入 P1 前的前置条件

只有下面条件同时成立，才允许进入 `P1`：

1. `grant_run_id` 这组变更已经 review 通过
2. `grant_run_id / workspace_id / draft_id / program_id` 边界没有新的冲突
3. repo-tracked review surface 已足以让 reviewer 理解 `grant_run_id` 合同
4. 当前 required verification 至少满足：
   - `python3 -m unittest discover -s tests -p 'test_*.py'`
   - `git diff --check`
   - 至少一条 CLI smoke path
5. 外部 verifier 状态已被明确记录
   - 若继续把 `omx_project_installer.py diff --target ...` 视为当前 tranche required verification，则必须先恢复它
   - 若它不再作为本轮 closeout gate，也必须先由 durable truth 明确改写，而不是口头忽略

## 实现前必须先冻结的合同

在任何 `P1` 实现动作前，必须先冻结以下合同：

### A. formal entry matrix

至少要写明：

- `CLI`：当前正式支持
- `MCP`：当前是否正式支持；若不支持，必须明确写成 not-yet-supported
- `controller`：当前是否正式支持；若不支持，必须明确写成 not-yet-supported
- `resume / recovery`：当前通过哪组 durable surfaces 进入

### B. durability surface contract

至少要写明：

- repo-tracked review surface 列表
- local durable handoff surface 列表
- 哪些结论必须 repo-native 才能成为 review truth
- 哪些状态允许只存在于 `.runtime-program/**`

### C. verification contract

至少要写明：

- 当前 tranche 的 required verification commands
- 哪些命令属于 hard gate
- 哪些命令若因外部工具故障失败，应如何在 durable truth 中显式记录

### D. identity boundary contract

至少要写明：

- `grant_run_id`：运行句柄
- `workspace_id`：聚合根身份
- `draft_id`：草稿身份
- `program_id`：control-plane / report routing 身份

并明确这些 ID 不得互相替代。

## 规划冻结结论

当前可进入的下一步不是实现，而是：

1. 先把 `formal entry matrix` 冻结成单独真相文档
2. 再把 `durability model clarification` 冻结成单独真相文档或同等级 planning artifact
3. 只有这两份合同都冻结后，才讨论是否开始 `P1` 实现

以上结论属于已完成的历史 `P1` 规划阶段；当前 active program 已不再停留在 `P3.A`，而是已经进入 runtime-first ladder absorbed through `R5.A` 的后续 hardening 语境。
