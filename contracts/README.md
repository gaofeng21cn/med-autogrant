# Contracts

Owner: `Med Auto Grant`
Purpose: `machine_contract_index`
State: `current_index`
Machine boundary: 本文是人读索引。机器真相归本目录 JSON contracts、schemas、source、CLI/API behavior、runtime receipts 与 `contracts/runtime-program/current-program.json`。

## Current Program

`contracts/runtime-program/current-program.json` 是 compact pointer，只声明 canonical identity、OPL runtime binding、direct domain handler、minimal authority function ref 与当前 contract refs。它不再嵌入 product/status/user-loop、consumer-thinning、phase map、executor registry 或 production evidence snapshot。

## Declarative Pack

- `domain_descriptor.json`
- `pack_compiler_input.json`
- `capability_map.json`
- `action_catalog.json`：3 个 public action 都使用 `stage_binding`，没有 `handler_ref`，因此不声明空 handler registry。
- `schemas/*action*.input.schema.json`：3 个 hosted action 的 exact closed input schema。
- `source_closure_audit.json`：OPL canonical source-closure scanner消费的 exact audit；未分类 generic effect 不得通过扩张 domain authority 放行。
- `../agent/stages/manifest.json`
- `generated_surface_handoff.json`
- `standard_agent_conformance_profile.json`：MAG-owned golden path 与 physical morphology 声明；OPL 只做通用读取和校验。
- `opl_agent_package_manifest.json`：声明 OPL Packages 持有 Agent Package/Codex carrier 的 install、update、uninstall 生命周期；MAG 只提供 carrier source 与 `medautogrant` runtime source locator。

OPL Pack 直接从 declarative stage manifest 生成 `family_stage_control_plane`，不在 MAG 跟踪生成快照。这些合同让 OPL 生成或托管 CLI/MCP/skill/product/status/user-loop/workbench caller；OPL 不能写 grant truth、memory/artifact/package body，不能签发 MAG verdict、receipt 或 typed blocker。

## MAG Authority

- `functional_privatization_audit.json`：canonical compact audit；七项 retained authority/refs adapter 的逐文件分类、三条 retired generated-surface provenance 与不授权物理删除的 bridge gate。Declarative pack inventory 只在 `pack_compiler_input.json#declarative_domain_pack`。
- `owner_receipt_contract.json`：`domain_owner_receipt`、`typed_blocker`、`no_regression_evidence`。
- `epistemic_review_scope_profile.json`：`package_and_submit_ready` 的 grant content、methodology、reference、display、export 与 package dependency graph；hash 仅作 locator/stale hint，exact-byte release integrity 单独建模。
- `memory_descriptor.json`、`artifact_locator_contract.json`：body-free locator/refs contract。
- `production_acceptance/mag-production-acceptance.json`：provenance-only acceptance tail；不是 live readiness。
- `live_stage_run_progress_evidence.json`：真实 owner refs 与 typed blocker source。

## Runtime Boundary

OPL/Temporal 持有 generic stage runtime、queue、attempt ledger、retry/resume、lifecycle transport 与 generated surfaces。MAG runtime state 写入 `$CODEX_HOME/projects/med-autogrant/runtime-state/` 或 workspace/artifact roots，不进入 repo source。
