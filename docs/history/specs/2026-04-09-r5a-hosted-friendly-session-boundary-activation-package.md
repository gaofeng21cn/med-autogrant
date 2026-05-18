# R5.A Hosted-Friendly Session Boundary Activation Package

> 生命周期注记（`2026-05-17`）：这份 dated spec 是 path-stable 的历史/支撑记录；只有 `docs/specs/README.md`、`docs/specs/specs_lifecycle_map.md`、`docs/status.md` 或 `contracts/runtime-program/current-program.json` 明确指定的仍 current subsection 才可作为当前边界阅读。请先读取 `docs/status.md`、核心五件套与 `contracts/runtime-program/current-program.json`。本文中的旧 `Current Truth`、Hermes、OPL Gateway、host-agent 或 federation wording 只作 provenance，不是当前 default owner line。

Date: `2026-04-09`

## Activation Status

- Future phase: `Runtime Productization Program`
- Future tranche: `R5 / Hostedization Prep`
- Future slice: `R5.A / Hosted-Friendly Session Boundary`
- Status: `pre-frozen / not activated`
- Upstream prerequisite:
  - `R1.A / R1.B / R2.A / R3.A / R4.A` 必须已 absorbed
  - local final package / export surface 必须稳定且可验证

## Goal

在不改写 `CLI` formal entry、不把 `MCP / controller` 写成已支持 public runtime、不破坏 `grant_run_id / workspace_id / draft_id / program_id` 边界、也不把 author-side mainline 改写成 reviewer / HITL / actual hosted runtime 产品的前提下，预冻结 `R5.A` 的最小 hostedization-prep contract：

- 把本地 runtime 的 session / state / artifact / audit surface 收成 hosted-friendly contract bundle
- 明确未来托管环境必须保留的 identity、state、artifact 与 audit boundary
- 让当前 repo 在不实现 web runtime 的前提下，先把可迁移的 contract 固定下来

这里冻结的不是“已经实现 hosted runtime”的事实，而是：

- 哪些 local runtime surface 是 future host 必须兼容的
- contract bundle 必须长什么样
- 进入实现前必须满足哪些 verification / invariants / stop conditions

当前 formal-entry matrix 继续固定为：

- `CLI`：当前唯一 formal entry
- `MCP`：`not-yet-supported` 的 future protocol layer
- `controller`：`not-yet-supported` 的 internal surface，不是 public formal entry

## Hard Boundary Docs

必须同时服从：

- `/Users/gaofeng/workspace/med-autogrant/AGENTS.md`
- `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-08-runtime-first-productization-program.md`
- `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-08-runtime-first-r1-to-r5-boundary-map.md`
- `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-09-r4a-final-freeze-and-export-package-activation-package.md`
- `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-07-formal-entry-matrix-current-truth.md`
- `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-07-durability-model-clarification.md`
- `/Users/gaofeng/workspace/med-autogrant/docs/specs/2026-04-08-p4b-verification-os-and-checkpoint-surface-current-truth.md`

## Object Boundary

`R5.A` 预冻结的对象边界是一个 **CLI-first local hosted-contract export pass**：

1. 从 current final package 读取：
   - `grant_run_id`
   - `workspace_id`
   - `draft_id`
   - `freeze_manifest`
   - `lineage`
   - `checkpoint_summary`
2. 从 absorbed local runtime surface 读取：
   - `runtime-run`
   - `runtime-resume`
   - `build-artifact-bundle`
   - `build-final-package`
   - `run journal`
   - `stage_action_envelope`
3. 输出 machine-readable hosted contract bundle

这意味着：

- `R5.A` 只抽 host-compatible contract
- `R5.A` 不实现 multi-tenant runtime
- `R5.A` 不实现 web UI / remote execution / credits / billing

## Canonical CLI Surface

`R5.A` 一旦进入实现，只允许先新增一个 `CLI-first` 本地 contract export 命令：

1. `build-hosted-contract-bundle`
   - final package：`--final-package <final-package-json-path>`
   - 输出路径：`--output <hosted-contract-json-path>`
   - 输出：本次 hosted contract 生产的 machine-readable payload

约束：

- 新命令仍属于 `CLI` formal entry，不新增第二 formal entry
- `build-hosted-contract-bundle` 不得替代既有 runtime commands
- `build-hosted-contract-bundle` 只写 contract bundle output，不写 `.runtime-program/**`
- `build-hosted-contract-bundle` 不授权 actual hosted runtime

## Hosted Contract Bundle

`R5.A` 的 hosted contract bundle 最小字段集冻结为：

- `contract_version`
- `bundle_kind`
  - 当前固定为 `hosted_contract_bundle`
- `formal_entry_matrix`
  - `default_formal_entry`
  - `supported_protocol_layer`
  - `internal_controller_surface`
- `execution_identity`
  - `grant_run_id`
  - `workspace_id`
  - `draft_id`
  - `program_id`
- `session_contract`
  - `session_handle_kind`
  - `start_entry`
  - `resume_entry`
  - `required_local_surfaces`
- `state_contract`
  - `workspace_surface_kind`
  - `run_journal_kind`
  - `stage_action_envelope_kind`
  - `artifact_bundle_kind`
  - `final_package_kind`
- `artifact_contract`
  - `artifact_bundle_manifest_kind`
  - `final_package_manifest_kind`
  - `lineage_fields`
- `audit_contract`
  - `verification_checkpoint_kind`
  - `checkpoint_status_kind`
  - `reviewed_revision_evidence_kind`

冻结语义：

- `bundle_kind` 当前固定为 `hosted_contract_bundle`
- `formal_entry_matrix.default_formal_entry` 继续固定为 `CLI`
- `formal_entry_matrix.supported_protocol_layer` 继续固定为 `MCP`
- `formal_entry_matrix.internal_controller_surface` 继续固定为 `controller`
- `execution_identity.grant_run_id` 继续是 runtime-side session handle
- `program_id` 继续只属于 control-plane routing identity，不转写为 runtime-side session id

## Local Output Contract

`R5.A` 的本地 output 只能是调用方显式提供的 hosted contract path：

- `--output <hosted-contract-json-path>` 为必填
- 若 output 已存在且其 `grant_run_id / workspace_id / draft_id` 与当前 final package 不一致，必须 fail-closed
- 若 output 已存在且其 `execution_identity.program_id` 与当前 root-checkout `CURRENT_PROGRAM.program_id` 不一致，也必须 fail-closed；`program_id` 仍只作为 control-plane routing identity，不得改写成 runtime session handle
- hosted contract bundle 是本地 exported contract artifact，不代表 actual hosted runtime 已存在

## Relation To Existing Canonical Surfaces

`R5.A` 必须继续围绕以下 surfaces 聚合，不得重写它们的 canonical 语义：

- `runtime-run`
- `runtime-resume`
- `build-artifact-bundle`
- `build-final-package`
- `verification_checkpoint`
- `checkpoint_status`
- `.runtime-program/reports/**`

关系冻结如下：

- `R5.A` 只抽出 contract compatibility，不重写 current product runtime
- `R5.A` 不改变 `grant_run_id / workspace_id / draft_id / program_id` 分工
- `R5.A` 不把 `.runtime-program/reports/**` 伪装成 hosted audit store
- `R5.A` 不把 local final package 伪装成 remote object store

## Required Verification

### Activation Package Freeze Gate

在 `OMX` 允许进入 `R5.A` implementation 前，必须同时满足：

1. active `CURRENT_PROGRAM / PRD / test-spec / implementation / reports` 已显式引用本 activation package
2. `tests/test_program_control_surfaces.py` 已对本 activation package 的存在性与控制面对齐做出断言
3. baseline hard gate 继续全绿：
   - `python3 -m unittest discover -s tests -p 'test_*.py'`
   - `python3 -m unittest discover -s tests -p 'test_program_control_surfaces.py'`
   - 当前 canonical CLI examples
   - `git diff --check`

### Implementation Promotion Gate

当 `R5.A` 进入实现时，必须补齐并通过以下新增验证：

1. hosted contract bundle regression tests
2. identity / session / state / artifact / audit contract alignment tests
3. `PYTHONPATH=src python3 -m med_autogrant build-artifact-bundle --input examples/nsfc_workspace_p3c_presubmission_frozen.json --output "$TMPDIR/r5a-bundle.json" --format json`
4. `PYTHONPATH=src python3 -m med_autogrant build-final-package --input examples/nsfc_workspace_p3c_presubmission_frozen.json --artifact-bundle "$TMPDIR/r5a-bundle.json" --output "$TMPDIR/r5a-final-package.json" --format json`
5. `PYTHONPATH=src python3 -m med_autogrant build-hosted-contract-bundle --final-package "$TMPDIR/r5a-final-package.json" --output "$TMPDIR/r5a-hosted-contract.json" --format json`
6. `git diff --check`

## Promotion Invariants

- 只做 hosted-friendly contract prep，不做 actual hosted runtime
- 不改写 domain contract
- 不改写 formal entry matrix
- 不进入 `P5.A / P5.B`
- 不引入 web UI / hosted platform / credits / billing

## Enter-Implementation Preconditions

只有以下条件全部满足，才允许进入 `R5.A` implementation：

1. `R1.A / R1.B / R2.A / R3.A / R4.A` 已 absorbed
2. active `CURRENT_PROGRAM / PRD / test-spec / implementation / reports` 已把 `R5.A` 写成当前 active next slice
3. 新增能力仍然只属于 hostedization prep contract，而不是 actual hosted runtime / `P5`
4. 当前 baseline hard gate 继续全绿

## Stop Conditions

以下情况出现时，必须诚实停车：

- 当前看似要做的能力其实已经需要 remote execution / web runtime / multi-tenant runtime
- 必须改写 formal entry、`MCP`、`controller`、或 `P5` 才能让 `R5.A` 成立
- 必须把 control-plane identity 混写成 runtime session identity 才能继续
- 必须引入 hosted credits / billing / registry / federation 才能继续

## Excluded Scope

- actual hosted runtime
- web UI
- remote execution
- multi-tenant platform
- credits / billing
- second-family / federation
- same-repo HITL
