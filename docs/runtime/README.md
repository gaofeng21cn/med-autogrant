# Runtime 文档

Owner: `Med Auto Grant`
Purpose: `runtime_boundary_index`
State: `active_support`
Machine boundary: 人读索引。Runtime truth归 OPL/provider readback、current-program、source、runtime receipts 与 live progress contract。

OPL/Temporal 持有 durable runtime、stage attempt lifecycle、scheduler、queue、retry/resume、attempt ledger、session 与 operator projection。MAG 只提供 bounded domain controller、direct handler、authority function 和 receipt/blocker refs。

当前机器入口：

- `contracts/runtime-program/current-program.json`
- `contracts/stage_run_kernel_profile.json`
- `contracts/live_stage_run_progress_evidence.json`
- `contracts/stage_artifact_kernel_adoption.json`
- `contracts/owner_receipt_contract.json`

本机非仓库状态统一进入 `$CODEX_HOME/projects/med-autogrant/runtime-state/`。Repo 不保存 runtime receipt body、workspace body、artifact/package body、queue 或 provider attempt body。

旧 local journal、attempt ledger、runtime wrapper、Hermes/Gateway/local-manager probe 和 compatibility alias 只从 history读取，不得恢复为 current runtime owner。
