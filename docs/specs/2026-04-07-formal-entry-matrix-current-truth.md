# Formal Entry Matrix Support Record

Owner: `Med Auto Grant`
Purpose: `formal_entry_support_record`
State: `support_current_truth`
Machine boundary: 本文是人读支撑记录。当前机器真相继续归 `contracts/runtime-program/current-program.json`、`contracts/generated_surface_handoff.json`、schemas、source、CLI/API behavior 与语义化 `human_doc:*` id。
Last reviewed: `2026-06-12`

## 当前读法

Formal-entry owner line 由核心文档和 `current-program.json` 持有。

当前 formal-entry matrix：

| 面 | 当前状态 | Owner |
| --- | --- | --- |
| `CLI` | 默认正式入口；通过 grouped public command tokens 与 `MedAutoGrantDomainEntry` 收敛到同一 MAG route / quality / workspace / export surface。 | MAG |
| `MCP` | supported protocol layer / descriptor projection；`descriptor_only=true`、`public_runtime=false`，不表示当前 public runtime 已正式开放。 | OPL 读取 descriptor，MAG 持有 grant truth |
| `controller` | internal command contract / projection surface；用于 product status、user-loop、direct-entry、quality governance 和 autonomy controller 报告。 | MAG |

当前 direct path 是：

`Med Auto Grant app skill -> OPL/App generated status or manifest refs -> MAG CLI / MedAutoGrantDomainEntry / domain-handler target -> generated grant-progress / grant-cockpit refs -> generated grant-direct-entry / grant-user-loop refs -> pass / package commands`

Repo-local grouped CLI 提供 workspace audit、mainline、domain-handler、authority、pass 与 package command target；进度、cockpit、direct-entry、user-loop、manifest 与 status 由 OPL generated surfaces 提供。

OPL-hosted path 可以读取 MAG descriptor、stage/control plane、domain-handler/projection 和 owner receipt refs，但必须回到同一套 MAG-owned grant truth、fundability / quality / export verdict、package authority、memory accept/reject、owner receipt 和 typed blocker。

## 当前 hard boundary

- `grant_run_id` 只作为 execution handle，不替代 `workspace_id`、`draft_id` 或 `program_id`。
- `Codex CLI` 是当前第一公民 concrete executor；`hermes_agent` / Claude Code 只能作为显式 opt-in executor adapter / proof lane。
- `build-hosted-contract-bundle` 是 integration/reference export surface，不表示 actual hosted runtime、production/default caller 或 Temporal long soak 已完成。
- `package submission-ready` 是本地严格导出 gate，不等于外部基金官网提交完成。
- 新 public runtime entry 或 controller public entry 需要先更新核心文档、contracts/schema/source 和验证入口。
