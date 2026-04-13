# P4.E Schema-Backed Frontdesk And Manifest Current Truth

Date: `2026-04-13`

## Activation Status

- Phase: `P4 mature direct grant product entry`
- Active tranche: `P4.E schema-backed frontdesk and manifest contract landing`
- Status: `landed / current truth`

## Goal

把 `product-entry-manifest` 与 `product-frontdesk` 从“已经有输出 shape 的 controller surface”进一步收口成独立的 schema-backed、generation-time fail-closed direct frontdoor contract，并继续保持以下边界不变：

- `Hermes-Agent` 继续只持有 runtime substrate / orchestration owner
- `Med Auto Grant` 继续持有 grant domain truth、author-side route 与导出物 owner
- `product-entry-manifest` / `product-frontdesk` 继续只是 controller-owned frontdoor / discovery contract，而不是新的 domain executor 或 mature Web UI

## Landed Facts

### 1. `product-entry-manifest` 与 `product-frontdesk` 现在各自拥有独立 schema

当前 frontdoor contract 现在新增两份独立 schema：

- `schemas/v1/product-entry-manifest.schema.json`
- `schemas/v1/product-frontdesk.schema.json`

并且它们已经登记进：

- `schemas/v1/schema-index.json`

这意味着当前 direct grant frontdoor 不再只是“有文档说明、有测试样例”的 surface，而是与 `product-entry`、`grant-progress`、`grant-cockpit`、`grant-direct-entry`、`grant-user-loop` 并列的 repo-tracked、machine-readable contract。

### 2. manifest / frontdesk 现在在生成时 fail-closed

`product_entry.py` 当前在生成：

- `build_product_entry_manifest(...)`
- `build_product_frontdesk(...)`

之后，会分别立即执行对应的 contract 校验。

因此当前 frontdoor contract 的 truth 约束不再只靠：

- 文档描述
- 调用侧约定
- 测试样例

而是直接由生成期 schema 校验 fail-closed 兜住。

### 3. `family_orchestration` companion 的 route status 已回到共享 truth 单源

此前 `family_orchestration` companion 在 `grant-progress` / `product-entry-manifest` / `product-frontdesk` 上仍可能使用本地过期的 landed-route 集合判断 gate / route status。

当前已经统一改成直接读取共享 author-side route contract。

这意味着像：

- `question_refinement`
- `argument_building`
- `fit_alignment`
- `outline`
- `drafting`

这类在 `P4.D` 已经 landed 的 authoring route，不会再在 frontdoor companion 上被误投成 `pending / requested`。

### 4. 当前 direct grant frontdoor 已形成一致的 contract 组合

现在 direct grant frontdoor 的 machine-readable 组合至少包括：

- `product-entry-manifest`
- `product-frontdesk`
- `grant-progress`
- `grant-cockpit`
- `grant-direct-entry`
- `grant-user-loop`

其中：

- `product-entry-manifest` 负责 discovery / quickstart / mainline snapshot
- `product-frontdesk` 负责 direct frontdoor / operator loop / projection action surface
- 其余 projection / loop surface 继续承载 progress、cockpit、composition 与 inbox-like user loop

它们现在共同对齐的是：

- 同一份 mainline snapshot
- 同一份 controller-owned frontdoor truth
- 同一份 shared author-side route truth

## Verification

本 tranche 至少覆盖：

- `uv run pytest tests/test_schema_registry.py tests/test_product_entry.py -q`
- `uv run pytest tests/test_mainline_status.py tests/test_program_control_surfaces.py tests/test_cli_validate_workspace.py -q`
- `scripts/verify.sh`

重点验证：

- 新 schema 已进入 `schema-index.json`
- manifest / frontdesk 在生成时执行 fail-closed 校验
- `family_orchestration` companion 在 frontdoor / projection surface 上与 landed route truth 保持一致
- `current-program`、`mainline-status`、README / docs / tests 对当前 `P4.E` 口径保持同步

## Honest Boundary

这条 current truth 只说明：

- `product-entry-manifest` 与 `product-frontdesk` 已 landed 为独立 schema-backed contract
- 当前 frontdoor / projection / user loop 看到的是同一份 shared route truth
- 当前 direct grant frontdoor 的 machine-readable contract 边界已经进一步冻结

它不意味着：

- mature direct grant Web UI / hosted runtime 已完成
- `OPL Gateway` 已在本仓落地
- family product-entry manifest v2、event envelope、checkpoint lineage 已经全部落地
