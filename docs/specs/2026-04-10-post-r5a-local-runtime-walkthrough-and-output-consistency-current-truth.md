# Post-R5A Local Runtime Walkthrough And Output Consistency Current Truth

Date: `2026-04-10`

## Goal

在不打开任何新 formal entry、不进入 actual hosted runtime、也不改写 `R1 -> R5.A` 已冻结对象边界的前提下，把 post-`R5.A` 的第一条诚实本地 hardening 线冻结为：

- `execute-revision-pass` 生成的 revised workspace，必须能立即重新进入当前 canonical validator / summary / route / checkpoint surfaces；
- `build-artifact-bundle -> build-final-package -> build-hosted-contract-bundle` 的本地产物链，必须继续保持同一组 execution identity 与 checkpoint truth；
- operator 需要一条 repo-tracked、可执行、不会把 `R5.A` 误写成 hosted runtime 的 canonical local walkthrough。

## Scope

### In Scope

1. revised workspace validator truth tightening
   - `validate-workspace` 必须接受 `execute-revision-pass` 的输出；
   - `summarize-workspace`、`next-step`、`critique-summary`、`stage-route-report` 必须能对 generated revised workspace 给出一致结果；
   - `stage-route-report.verification_checkpoint` 继续是 revised workspace 之后的 canonical checkpoint aggregation surface。
2. local output consistency
   - `build-final-package` 继续只从 workspace + artifact bundle 生成本地 final package；
   - `build-hosted-contract-bundle` 继续只从 final package 导出 hosted-friendly contract bundle；
   - `grant_run_id / workspace_id / draft_id / program_id` 分工不漂移。
   - 已存在 hosted contract output 的 `execution_identity.grant_run_id / execution_identity.workspace_id / execution_identity.draft_id / execution_identity.program_id` 必须与当前生成链一致，否则 fail-closed。
3. operator walkthrough freeze
   - 用 repo-tracked 文档把真实已 landed 的本地 operator path 写清楚；
   - public README 只承认已 landed 的本地 runtime ladder，不再把 walkthrough / output consistency 写成悬空口号。

### Out of Scope

- actual hosted runtime
- remote execution / Web UI / multi-tenant
- `P5.A / P5.B`
- same-repo `Human-in-the-loop`
- 新 `MCP / controller` public formal entry

## Truth Alignment Conclusions

1. `execute-revision-pass` 不只是写一个新的 workspace 文件；它的输出必须马上被当前 canonical validator / checkpoint surfaces 接住。
2. `verification_checkpoint / checkpoint_status` 的 canonical 聚合地仍然是 `stage-route-report`；`build-final-package` 只消费它，不重新发明第二套 final gate。
3. `build-hosted-contract-bundle` 仍然只是本地 contract export surface：
   - 继续保留 `formal_entry_matrix.default_formal_entry=CLI`
   - 继续保留 `supported_protocol_layer=MCP`
   - 继续保留 `internal_controller_surface=controller`
   - 不把 `program_id` 改写成 runtime-side session id
   - 覆盖已存在 output 时继续把 `program_id` 纳入 `execution_identity` 边界校验
4. 这条线只做 truth tightening、walkthrough freeze 与 regression coverage，不新增任何新的 runtime command。

## Canonical Local Walkthrough

以下 walkthrough 是当前 repo-tracked 的 canonical 本地 operator path：

```bash
TMPDIR="$(mktemp -d)"

# 1) 对 critique workspace 做 baseline audit
PYTHONPATH=src python3 -m med_autogrant validate-workspace --input examples/nsfc_workspace_p2c_critique.json --format json
PYTHONPATH=src python3 -m med_autogrant summarize-workspace --input examples/nsfc_workspace_p2c_critique.json --format json
PYTHONPATH=src python3 -m med_autogrant next-step --input examples/nsfc_workspace_p2c_critique.json --format json
PYTHONPATH=src python3 -m med_autogrant critique-summary --input examples/nsfc_workspace_p2c_critique.json --format json
PYTHONPATH=src python3 -m med_autogrant stage-route-report --input examples/nsfc_workspace_p2c_critique.json --format json

# 2) 执行 deterministic local revision pass
PYTHONPATH=src python3 -m med_autogrant execute-revision-pass --input examples/nsfc_workspace_p2c_critique.json --output "$TMPDIR/r3a-p2c-revised.json" --format json

# 3) 对 generated revised workspace 做 fresh validate / route / checkpoint
PYTHONPATH=src python3 -m med_autogrant validate-workspace --input "$TMPDIR/r3a-p2c-revised.json" --format json
PYTHONPATH=src python3 -m med_autogrant summarize-workspace --input "$TMPDIR/r3a-p2c-revised.json" --format json
PYTHONPATH=src python3 -m med_autogrant next-step --input "$TMPDIR/r3a-p2c-revised.json" --format json
PYTHONPATH=src python3 -m med_autogrant critique-summary --input "$TMPDIR/r3a-p2c-revised.json" --format json
PYTHONPATH=src python3 -m med_autogrant stage-route-report --input "$TMPDIR/r3a-p2c-revised.json" --format json

# 4) 进入 local final/export/hosted-contract chain
PYTHONPATH=src python3 -m med_autogrant build-artifact-bundle --input examples/nsfc_workspace_p3c_presubmission_frozen.json --output "$TMPDIR/r5a-bundle.json" --format json
PYTHONPATH=src python3 -m med_autogrant build-final-package --input examples/nsfc_workspace_p3c_presubmission_frozen.json --artifact-bundle "$TMPDIR/r5a-bundle.json" --output "$TMPDIR/r5a-final-package.json" --format json
PYTHONPATH=src python3 -m med_autogrant build-hosted-contract-bundle --final-package "$TMPDIR/r5a-final-package.json" --output "$TMPDIR/r5a-hosted-contract.json" --format json
```

补充要求：

- `P3.B` 的 re-review workspace 也必须能通过同一条 generated revised workspace fresh-validation path；
- walkthrough 只解释当前 landed local runtime ladder，不构成 actual hosted runtime 承诺。

## Required Verification

1. `python3 -m unittest discover -s tests -p 'test_program_control_surfaces.py'`
2. `python3 -m unittest discover -s tests -p 'test_revision_executor.py'`
3. `python3 -m unittest discover -s tests -p 'test_final_package.py'`
4. `python3 -m unittest discover -s tests -p 'test_hosted_contract_bundle.py'`
5. `python3 -m unittest discover -s tests -p 'test_*.py'`
6. walkthrough 中的 generated revised workspace fresh validate / route commands
7. walkthrough 中的 local final / hosted-contract chain commands
8. `git diff --check`

## Promotion Invariants

- 不得改写 `grant_run_id / workspace_id / draft_id / program_id`
- 不得把 `verification_checkpoint / checkpoint_status` 从 `stage-route-report` 挪到第二个 canonical source
- 不得让 `build-final-package` 或 `build-hosted-contract-bundle` 反向写回 workspace / `.runtime-program/**`
- 不得把 walkthrough 写成 actual hosted runtime、remote execution 或 `P5` expansion

## Honest Stop Rule

如果本 slice 完成后已经没有新的 concrete、本地、repo-trackable runtime delta，就应以：

`NO_NEW_POST_R5A_LOCAL_RUNTIME_DELTA_HONEST_STOP`

作为 truthful closeout，而不是继续发明新的“自然下一棒”。
