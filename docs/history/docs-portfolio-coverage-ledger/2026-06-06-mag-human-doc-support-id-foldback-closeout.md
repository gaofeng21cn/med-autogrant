# MAG human_doc support-id foldback closeout

Owner: `Med Auto Grant`
Purpose: `human_doc_support_id_foldback_closeout`
State: `history_closeout`
Machine boundary: 本文是人读 closeout。当前机器真相继续归 `contracts/runtime-program/current-program.json`、schemas、source、CLI/API behavior、runtime receipts 和语义化 `human_doc:*` id。

## Scope

本轮只处理仍出现在 repo-tracked current-program 与 `mainline_status` 维护参考里的历史 dated `human_doc:*` support ids。

已退役为 history/provenance 的 ids：

- `human_doc:2026_04_12_hosted_caller_consumption_proof_current_truth`
- `human_doc:2026_04_12_opl_aligned_ideal_target_and_phase_map_current_truth`
- `human_doc:2026_04_12_p4a_direct_grant_cockpit_and_progress_projection_current_truth`
- `human_doc:2026_04_12_p4b_direct_grant_entry_composition_current_truth`
- `human_doc:2026_04_12_p4c_mainline_status_and_grant_user_loop_current_truth`
- `human_doc:2026_04_12_hosted_contract_bundle_entry_and_route_catalog_current_truth`
- `human_doc:2026_04_12_lightweight_product_entry_and_opl_handoff_current_truth`
- `human_doc:2026_04_12_author_side_executor_routing_contract_current_truth`
- `human_doc:2026_04_13_p4e_schema_backed_product_status_and_manifest_current_truth`
- `human_doc:2026_04_13_p4f_local_submission_ready_package_current_truth`

## Current Reading

旧 P4A/P4B/P4C/P4E/P4F 的 current support 语义统一折回：

- `human_doc:product_entry_support_record`

Schema-backed product-entry / route contract、full authoring executor、formal-entry、durability 与 active quality/completion specs 仍按当前 lifecycle map 的 active/support 边界阅读。

Hosted caller、hosted contract bundle route catalog、lightweight OPL handoff、OPL alignment 与 old author-side route snapshot 只作为 `docs/history/specs/` provenance 阅读；当前 contract export、route catalog、OPL provider/App readiness 与机器行为回到 source、schemas、contracts、core docs 和 `current-program.json`。

## Changes

- `contracts/runtime-program/current-program.json#repo_tracked_truth_surfaces` 移除历史 dated support/provenance ids，并加入 `human_doc:product_entry_support_record`。
- `src/med_autogrant/mainline_status.py` 的 P4 `phase_docs` 改为当前 support record；P2/P3 维护参考不再暴露已归档 hosted/proof/handoff ids。
- `tests/test_program_control_surfaces.py` 与 `tests/test_mainline_status.py` 增加 no-resurrection guard，防止历史 dated ids 重新成为 active truth surfaces。

## Verification

本 closeout 对应验证命令：

```bash
./scripts/run-pytest-clean.sh tests/test_program_control_surfaces.py tests/test_mainline_status.py tests/product_entry_cases/test_manifest_and_status.py tests/product_entry_cases/test_status_start_cases.py -q
./scripts/verify.sh
git diff --check
```

历史 ids 可以留在 `docs/history/**` 与 no-resurrection tests 中；不得重新出现在 `contracts/runtime-program/current-program.json` 或 source-owned active maintainer references 中。
