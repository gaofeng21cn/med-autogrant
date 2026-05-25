# Formal Entry Matrix Support Record

Owner: `Med Auto Grant`
Purpose: `formal_entry_support_record`
State: `support_current_truth`
Machine boundary: 本文是人读支撑记录。当前机器真相继续归 `contracts/runtime-program/current-program.json`、schemas、source、CLI/API behavior、product-entry manifest 与语义化 `human_doc:*` id。
Date: `2026-05-19`

## 当前读法

本文件保留 `2026-04-07` formal-entry vocabulary 的 path-stable 支撑位置，但当前 owner line 已由核心文档和 `current-program.json` 持有。早期 post-R5A local runtime / journal / recovery 叙事已经退为 history/provenance，不能从本文恢复旧 public CLI alias、compatibility test、local journal、attempt ledger、Gateway/local-manager path 或 MAG-owned generic runtime。

当前 formal-entry matrix：

| 面 | 当前状态 | Owner |
| --- | --- | --- |
| `CLI` | 默认正式入口；通过 grouped public command tokens 与 `MedAutoGrantDomainEntry` 收敛到同一 MAG route / quality / workspace / export surface。 | MAG |
| `MCP` | supported protocol layer / descriptor projection；`descriptor_only=true`、`public_runtime=false`，不表示当前 public runtime 已正式开放。 | OPL 读取 descriptor，MAG 持有 grant truth |
| `controller` | internal command contract / projection surface；用于 product status、user-loop、direct-entry、quality governance 和 autonomy controller 报告。 | MAG |

当前 direct path 是：

`Med Auto Grant app skill -> CLI / MedAutoGrantDomainEntry -> product status / user-loop / direct-entry -> workspace progress / cockpit -> pass / package commands`

OPL-hosted path 可以读取 MAG descriptor、stage/control plane、domain-handler/projection 和 owner receipt refs，但必须回到同一套 MAG-owned grant truth、fundability / quality / export verdict、package authority、memory accept/reject、owner receipt 和 typed blocker。

## 已退役入口

以下旧面只作为历史 provenance 或 regression-oracle 词汇阅读：

- `runtime-run`
- `runtime-resume`
- `probe-upstream-hermes`
- local run journal / local attempt ledger
- Gateway/local-manager default path
- flat shell alias
- compatibility aggregate test

这些面已从 MAG public CLI、`MedAutoGrantDomainEntry` service-safe catalog、product-entry session continuity、hosted bundle schema 和默认 smoke 断言中退役。Session/resume 语义改由 OPL generated surface refs 与 MAG owner receipt / typed blocker refs 表达。

## 当前 hard boundary

- `grant_run_id` 只作为 execution handle，不替代 `workspace_id`、`draft_id` 或 `program_id`。
- `Codex CLI` 是当前第一公民 concrete executor；`hermes_agent` / Claude Code 只能作为显式 opt-in executor adapter / proof lane。
- `build-hosted-contract-bundle` 是 integration/reference export surface，不表示 actual hosted runtime、production/default caller 或 Temporal long soak 已完成。
- `package submission-ready` 是本地严格导出 gate，不等于外部基金官网提交完成。
- 任何新 public runtime entry、controller public entry、旧兼容别名或 local runtime recovery entry 都必须先更新核心五件套、contracts/schema/source 和验证入口。

## 历史入口

旧 post-R5A local runtime walkthrough、honest-stop 和 fail-closed hardening 记录已归档到 [历史 specs](../history/specs/README.md)。直接阅读历史文件时，以本文件、核心五件套、[Specs 生命周期地图](./specs_lifecycle_map.md) 和 `current-program.json` 为准。
