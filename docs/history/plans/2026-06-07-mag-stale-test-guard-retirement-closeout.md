# MAG stale test guard retirement closeout 2026-06-07

Owner: `Med Auto Grant`
Purpose: `mag_stale_test_guard_retirement_closeout`
State: `history_closeout`
Machine boundary: 本文只记录本轮测试层旧 facade 负断言退役过程。当前 truth 继续归 `contracts/runtime-program/current-program.json`、contracts/schema/source、CLI/API behavior、tests、runtime receipts、MAG owner receipt / typed blocker 与 fresh verification output。

## Scope

本轮只退役两个已经被当前直接 owner surface 覆盖的测试层旧 facade 负断言：

| Surface | Action | Current owner |
| --- | --- | --- |
| `tests/test_structural_direct_coverage.py::test_workspace_index_has_direct_behavior_and_facade_export_helper_is_retired` | 删除重复行为覆盖与 `facade_exports.py` 缺席断言。 | `_index_objects` 行为由 `tests/test_workspace_index.py` 直接覆盖；repo-wide retired facade policy 继续由 no-resurrection / private surface tests 和 contracts 承担。 |
| `tests/test_runtime_cli_structural_helpers.py::test_cli_rendering_no_longer_reexports_render_text_facade` | 删除 `_render_text` re-export 缺席断言和渲染 smoke。 | CLI rendering 行为由 CLI/output tests 与 `cli_rendering_parts` owner module 承担；本测试文件继续保留 active patch-surface、runtime-parts、domain-entry lazy loader 和 workspace stage helper guards。 |

本轮没有删除 `domain_runtime_patch_bridge` tombstone、retired command negative tests、Sentrux governance tests、private functional surface policy tests 或任何仍被 contract/evidence refs 点名的 no-resurrection guard。

## Boundary

这不是 MAG product/runtime shell physical delete，也不是 OPL generated/default caller cutover claim。Product-entry、domain handler、domain runtime、CLI target、lifecycle/memory/package projection 和 explicit non-default executor helper 的 physical delete 仍以 active gap plan、private inventory、contracts、owner receipt / typed blocker、no-active-caller 和 no-forbidden-write proof 为准。

## Verification

Observed in `mag-stale-test-guard-retirement-20260607` worktree:

```bash
rtk ./scripts/run-pytest-clean.sh -q tests/test_workspace_index.py tests/test_structural_direct_coverage.py tests/test_runtime_cli_structural_helpers.py tests/test_cli_validate_workspace.py tests/product_entry_cases/test_cli_dispatch.py
rtk grep -RIn "facade_exports\\|cli_rendering_no_longer_reexports_render_text_facade\\|workspace_index_has_direct_behavior_and_facade_export_helper_is_retired" tests src contracts
rtk git diff --check
```

Result:

- Focused pytest batch passed.
- Retired test-name scan no longer finds active tests.
- `facade_exports.py` remains absent from source.

## Remaining Scope

Broader MAG cleanup remains open. The next physical deletion pass still needs per-surface proof:

- OPL generated/default caller parity or replacement owner proof.
- No-active-caller scan.
- MAG owner receipt or typed blocker authorizing deletion.
- No-forbidden-write proof.
- Tombstone/provenance refs only where history remains useful.
