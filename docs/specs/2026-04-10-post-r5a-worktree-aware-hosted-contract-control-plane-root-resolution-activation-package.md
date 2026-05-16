# Post-R5A Worktree-Aware Hosted Contract Control-Plane Root Resolution Activation Package

> 生命周期注记（`2026-05-17`）：这份 dated spec 是 path-stable 的历史/支撑记录；只有 `docs/specs/README.md`、`docs/specs/specs_lifecycle_map.md`、`docs/status.md` 或 `contracts/runtime-program/current-program.json` 明确指定的仍 current subsection 才可作为当前边界阅读。请先读取 `docs/status.md`、核心五件套与 `contracts/runtime-program/current-program.json`。本文中的旧 `Current Truth`、Hermes、OPL Gateway、host-agent 或 federation wording 只作 provenance，不是当前 default owner line。

Date: `2026-04-10`

## Activation Status

- Phase: `Runtime Productization Program`
- Active tranche: `R5 / Hostedization Prep`
- Active slice: `post-R5A local runtime hardening / worktree-aware hosted-contract control-plane root resolution`
- Status: `frozen / ready for implementation`
- Upstream prerequisite:
  - `R1.A / R1.B / R2.A / R3.A / R4.A / R5.A` 已 absorbed
  - post-`R5.A` revised-workspace validator / walkthrough / output-consistency truth 已冻结
  - `build-hosted-contract-bundle` 当前 contract 与 CLI shape 已 landed，不打开新的 runtime command

## Goal

在不改写 `build-hosted-contract-bundle` object boundary、不引入新 formal entry、也不把 `program_id` 改写成 runtime session handle 的前提下，把一个已存在但仍不够诚实的本地实现细节收紧为 repo-tracked truth：

- `build-hosted-contract-bundle` 继续必须从 **root checkout** 的 `.runtime-program/context/CURRENT_PROGRAM.md` 读取 control-plane `program_id`
- 但 root checkout 的发现方式，不再允许依赖硬编码的机器绝对路径
- 在独立 worktree 内执行时，必须通过 deterministic 的 git worktree metadata 找到当前 repo 的 root `main` checkout
- 如果 root checkout 缺失、`main` worktree 不唯一、或对应 `CURRENT_PROGRAM.md` 缺失，则必须 fail-closed

## Trigger Evidence

当前 repo 已明确要求：

- 重型执行必须在独立 worktree 中进行
- root checkout 只用于 absorb / push / cleanup
- `.runtime-program/` 是本机私有 local state，不会被复制进实现 worktree

这意味着 `build-hosted-contract-bundle` 若仍靠：

- 机器私有绝对路径
- repo 路径写死
- 或“当前 repo 候选 / 单候选即可接受”之类的启发式回退

来定位 `CURRENT_PROGRAM.md`，就会让当前 `CLI-first + host-agent` runtime baseline 的 worktree story 不够诚实，也无法把“root checkout 锚定”表达成 repo-trackable contract。

## In Scope

### 1. root control-plane discovery tightening

`build-hosted-contract-bundle` 的 `program_id` 读取必须采用以下确定性顺序：

1. 若当前 repo root 自身存在 `.runtime-program/context/CURRENT_PROGRAM.md`，直接读取它；
2. 否则读取 `git worktree list --porcelain`；
3. 从中定位唯一的 `branch refs/heads/main` worktree；
4. 读取该 worktree 的 `.runtime-program/context/CURRENT_PROGRAM.md`；
5. 若任一步不满足，fail-closed。

### 2. no semantic drift

这条 slice 只收紧“如何找到 root checkout 的 `CURRENT_PROGRAM.md`”，不改写：

- `formal_entry_matrix`
- `execution_identity`
- `execution_identity.program_id`
- `grant_run_id / workspace_id / draft_id / program_id` 分工
- `build-hosted-contract-bundle` 的 payload shape
- overwrite identity guard

### 3. regression coverage

至少补齐：

- 当前 repo root 自身带 `.runtime-program/context/CURRENT_PROGRAM.md` 时的 direct-resolution regression
- 当前实现 worktree 缺少 `.runtime-program/` 时，fallback 到唯一 `main` worktree 的 regression
- `main` worktree 缺失或不唯一时的 fail-closed regression

## Out Of Scope

- actual hosted runtime
- remote execution / Web UI / multi-tenant
- `P5.A / P5.B`
- same-repo `Human-in-the-loop`
- `MCP / controller` public formal entry
- `program_id` 语义改写

## Object Boundary

当前 slice 只允许修改下面这个局部 object boundary：

- `build-hosted-contract-bundle`
  - 读取 current final package
  - 读取 root checkout `CURRENT_PROGRAM.program_id`
  - 组装 hosted-friendly contract bundle

其中被收紧的仅是：

- `root checkout CURRENT_PROGRAM` 的定位逻辑

不允许顺带改动：

- final package contract
- revision executor
- artifact bundle
- route / checkpoint semantics
- `.runtime-program/reports/**` 的 durable 含义

## Required Verification

至少覆盖：

1. `python3 -m unittest discover -s tests -p 'test_program_control_surfaces.py'`
2. `python3 -m unittest discover -s tests -p 'test_hosted_contract_bundle.py'`
3. `python3 -m unittest discover -s tests -p 'test_*.py'`
4. `PYTHONPATH=src python3 -m med_autogrant build-artifact-bundle --input examples/nsfc_workspace_p3c_presubmission_frozen.json --output "$TMPDIR/r5a-bundle.json" --format json`
5. `PYTHONPATH=src python3 -m med_autogrant build-final-package --input examples/nsfc_workspace_p3c_presubmission_frozen.json --artifact-bundle "$TMPDIR/r5a-bundle.json" --output "$TMPDIR/r5a-final-package.json" --format json`
6. `PYTHONPATH=src python3 -m med_autogrant build-hosted-contract-bundle --final-package "$TMPDIR/r5a-final-package.json" --output "$TMPDIR/r5a-hosted-contract.json" --format json`
7. `git diff --check`

## Promotion Invariants

- `build-hosted-contract-bundle` 仍只是 hosted-friendly contract export
- `formal_entry_matrix.default_formal_entry` 仍固定为 `CLI`
- `supported_protocol_layer` 仍固定为 `MCP`
- `internal_controller_surface` 仍固定为 `controller`
- `program_id` 仍只属于 control-plane routing identity
- worktree-aware root discovery 只能收紧路径解析，不得引入新的 host/runtime semantics

## Honest Stop Rule

如果这条 slice 完成后，剩余事项已经需要：

- actual hosted runtime
- 新 formal entry
- `P5.A / P5.B`
- 或非确定性的路径猜测 / 启发式 root 发现

则必须回到：

`NO_NEW_POST_R5A_LOCAL_RUNTIME_DELTA_HONEST_STOP`
