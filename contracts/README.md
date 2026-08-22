# Contracts

Owner: `Med Auto Grant`
Purpose: `machine_contract_index`
State: `current_index`
Machine boundary: 本文是人读索引。机器真相归本目录 JSON contracts、schemas、source、CLI/API behavior、runtime receipts 与 `contracts/runtime-program/current-program.json`。

## Current Program

`contracts/runtime-program/current-program.json` 是 compact pointer，声明 canonical identity、OPL runtime binding、direct domain handler、minimal authority function ref 与当前 contract refs。

## Declarative Pack

- `domain_descriptor.json`
- `pack_compiler_input.json`
- `capability_map.json`
- `action_catalog.json`：3 个 public action 使用 `stage_binding`。
- `schemas/*action*.input.schema.json`：3 个 hosted action 的 exact closed input schema。
- `source_closure_audit.json`：OPL source-closure scanner 消费的 exact file/symbol/effect classification。
- `../agent/stages/manifest.json`
- `generated_surface_handoff.json`
- `standard_agent_conformance_profile.json`：MAG-owned golden path 与 physical morphology 声明；OPL 只做通用读取和校验。
- `opl_agent_package_manifest.json`：声明 `mag` identity、capabilities、dependency intent、
  Codex carrier 与 `medautogrant` runtime locator。MAG owner 发布完整 GHCR bytes；
  Framework 聚合 carrier actions 与 fresh readback。
- `scholar_skill_binding_contract.json`：把 `mas-scholar-skills` 声明为 MAG 的 required hard
  dependency；readiness 只检查 identity presence/callability，缺失时只对 MAG fail
  closed，不做 provider version/ABI/lock/payload/digest 求解。

OPL Pack 从 declarative stage manifest 生成 `family_stage_control_plane`，并托管 CLI/MCP/skill/product/status/user-loop/workbench caller。MAG 持有 grant truth、memory/artifact/package body、verdict、receipt 与 typed blocker authority。

OPL Package 的跨仓目标与删除门禁归
[App 跨仓总体迁移 SSOT](https://github.com/gaofeng21cn/one-person-lab-app/blob/main/docs/active/opl-package-platform-composition-migration.md)。
本文只解释当前 MAG machine surface；文档更新不表示迁移完成。

## MAG Authority

- `functional_privatization_audit.json`：七项 retained authority/refs adapter 的逐文件分类与 bridge gate。Declarative pack inventory 位于 `pack_compiler_input.json#declarative_domain_pack`。
- `owner_receipt_contract.json`：`domain_owner_receipt`、`typed_blocker`、`no_regression_evidence`。
- `epistemic_review_scope_profile.json`：`package_and_submit_ready` 的 grant content、methodology、reference、display、export 与 package dependency graph；hash 仅作 locator/stale hint，exact-byte release integrity 单独建模。
- `memory_descriptor.json`、`artifact_locator_contract.json`：body-free locator/refs contract。
- `production_acceptance/mag-production-acceptance.json`：provenance-only acceptance tail；不是 live readiness。
- `live_stage_run_progress_evidence.json`：真实 owner refs 与 typed blocker source。

## Runtime Boundary

OPL/Temporal 持有 generic stage runtime、queue、attempt ledger、retry/resume、lifecycle transport 与 generated surfaces。MAG runtime state 写入 `$CODEX_HOME/projects/med-autogrant/runtime-state/` 或 workspace/artifact roots，不进入 repo source。
