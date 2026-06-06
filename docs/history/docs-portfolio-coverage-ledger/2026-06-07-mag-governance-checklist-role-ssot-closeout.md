# MAG governance checklist role SSOT closeout

Owner: `Med Auto Grant`
Purpose: `governance_checklist_role_ssot_closeout`
State: `history_provenance`
Machine boundary: 本文是人读治理 closeout。当前机器真相继续归 `contracts/runtime-program/current-program.json`、schemas、source、CLI/API behavior、runtime receipts、owner receipts、MAG grant authority surfaces 和当前 owner docs；本文不作为 grant readiness、submission readiness、production readiness、OPL-hosted long-soak、App/workbench consumption 或 physical-delete authorization 证据。

本文记录 2026-06-07 OPL Doc 语义治理中 `series docs governance checklist role` 主题的 Single Source of Truth 收敛。本轮把 `docs/references/governance/series-doc-governance-checklist.md` 明确为 OPL series 跨仓 docs intake / 对齐巡检支撑，避免它与 `docs/docs_portfolio_consolidation.md` 竞争 MAG 文档生命周期治理 owner。

## Semantic Theme

本轮治理主题是 MAG 文档生命周期治理规则与 OPL series 巡检支撑清单的 owner 边界。

Single Source of Truth 分层：

- Docs lifecycle governance owner: `docs/docs_portfolio_consolidation.md`。
- Docs entry index owner: `docs/README.md`。
- Series cross-repo checklist support: `docs/references/governance/series-doc-governance-checklist.md`。
- Current project truth owners: `docs/project.md`、`docs/status.md`、`docs/architecture.md`、`docs/invariants.md`、`docs/decisions.md`。
- Active completion plan owner: `docs/active/mag-ideal-state-cross-repo-gap-plan.md`。
- Specs lifecycle owner: `docs/specs/README.md` and `docs/specs/specs_lifecycle_map.md`。
- Machine truth owners: `contracts/runtime-program/current-program.json`、schemas、source、tests、CLI/API behavior、runtime receipts and product-entry manifest。

## Peer Docs and Classification

| Surface | Classification | Governance action |
| --- | --- | --- |
| `docs/docs_portfolio_consolidation.md` | `lifecycle_governance_ssot` | Kept as the current lifecycle governance owner; clarified that reference checklist material is not lifecycle governance or active owner. |
| `docs/README.md` | `covered_by_ssot` | Rewrote the governance note so lifecycle rules point to `docs/docs_portfolio_consolidation.md`; the checklist is now support only. |
| `docs/references/README.md` | `more_specific_detail` | Kept the checklist in the reference grouping and routed lifecycle governance back to the SSOT. |
| `docs/references/governance/series-doc-governance-checklist.md` | `active_support` | Kept as OPL series cross-repo docs intake / alignment checklist; added explicit non-owner wording. |
| `docs/history/docs-portfolio-coverage-ledger/2026-06-02-mag-docs-portfolio-coverage-ledger-archive.md` | `history_or_provenance` | Earlier reference-body audit provenance remains historical; current lifecycle rules do not live there. |
| Core five docs, active plan, specs lifecycle map and contracts | `current_or_machine_truth_owner` | No rewrite; they already own current truth, active plan, specs lifecycle and machine truth respectively. |

## Content-Level Consolidation

- MAG document lifecycle governance now has exactly one current owner: `docs/docs_portfolio_consolidation.md`.
- The series checklist remains useful as a cross-repo inspection aid for six-repo scope, same-name taxonomy, public/internal layering and MAG grant-authority boundary.
- The checklist does not own current truth, active completion progress, active gaps, specs lifecycle, machine contracts, public identity, lifecycle taxonomy or physical-delete authorization.
- No source, contract, test, workflow, CLI/API entry, runtime behavior, grant authority surface or physical module retirement was newly authorized by this docs-support role lane.

## Verification

Commands run from `/Users/gaofeng/workspace/med-autogrant/.worktrees/codex/mag-docs-checklist-role` after this closeout and support-doc role updates:

```bash
rtk git diff --check
rtk rg -n '^(<<<<<<<|=======|>>>>>>>)' docs/README.md docs/docs_portfolio_consolidation.md docs/references/README.md docs/references/governance/series-doc-governance-checklist.md docs/history/docs-portfolio-coverage-ledger/README.md docs/history/docs-portfolio-coverage-ledger/2026-06-07-mag-governance-checklist-role-ssot-closeout.md
rtk rg -n "文档生命周期治理|文档治理统一冻结|series-doc-governance-checklist|docs_portfolio_consolidation|治理说明|跨仓 docs intake|对齐巡检" docs/README.md docs/docs_portfolio_consolidation.md docs/references/README.md docs/references/governance/series-doc-governance-checklist.md docs/history/docs-portfolio-coverage-ledger/README.md
rtk opl-doc-doctor doctor /Users/gaofeng/workspace/med-autogrant/.worktrees/codex/mag-docs-checklist-role --format json
```

Result:

- `rtk git diff --check`: passed.
- Conflict-marker scan: passed with no matches.
- Targeted SSOT scan confirmed lifecycle governance rules point to `docs/docs_portfolio_consolidation.md`, while `series-doc-governance-checklist.md` is described only as OPL series cross-repo docs intake / alignment support.
- OPL Doc doctor reported `finding_count=0` and `active_truth_health.status=pass`.

## Remaining Scope

This lane closes only the MAG governance-checklist role split. It does not claim full MAG docs portfolio completion and does not close the six-repo OPL series `/goal`.

Open carry-forward:

- Actual MAG owner delete authorization / keep-as-authority-adapter receipt / typed blocker outcome remains separate from checklist governance.
- Direct/hosted parity follow-through, production/App sustained consumption, Temporal long-soak and broader docs portfolio remain separate lanes.
