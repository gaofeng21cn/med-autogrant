# P4.F Local Submission-Ready Package Current Truth

Owner: `Med Auto Grant`
Purpose: `local_submission_ready_package_support_record`
State: `support_current_truth`
Machine boundary: 本文是人读支撑记录，只在本地 submission-ready package export gate subsection 内有效。机器真相继续归 source、schemas、product-entry manifest、contracts、workspace artifacts 和 `contracts/runtime-program/current-program.json`。

> 生命周期注记（`2026-05-17`）：这份 dated spec 只在 MAG package/export authority、schema/source 与 product-entry manifest 仍持有的本地 `submission-ready package` export gate 范围内是 `support_current_truth`。请先读取 `docs/status.md`、核心五件套、`docs/active/mag-ideal-state-cross-repo-gap-plan.md` 与 `contracts/runtime-program/current-program.json`。下方旧 Gateway/hosted runtime language 是 provenance，不得读成当前 OPL target 或 compatibility surface。

当前处置：

- Keep：`build-submission-ready-package`、`submission-ready-package.schema.json`、fail-closed local export gate、AI-first MAG owner export verdict gate，以及 authoring completion 和 package readiness 之间的诚实边界。
- Superseded：旧 `OPL Gateway` / hosted runtime implication。OPL 通过当前 stage-led framework 消费 MAG descriptor/projection；MAG 保留 package/export authority。
- Direct retirement posture：只为保留 superseded Gateway reading 的旧 wrappers、tests 或 docs，应迁到最新 package/export owner surface 后删除或归档，不新增 compatibility aliases。

Date: `2026-04-13`

## Activation Status

- Phase: `P4 mature direct grant product entry`
- Active boundary: `local submission-ready package export gate`
- Status: `support_current_truth_by_subsection`

## Goal

把“本地 submission-ready 交付”从零散的 `artifact_bundle -> final_package -> hosted_contract_bundle` 导出链，收口成一个面向用户、可一键执行、可 fail-closed 拒绝不完整材料或缺少 owner export verdict 的正式命令 `build-submission-ready-package`，同时保持下面这些边界不变：

- `Codex CLI` 继续是默认 concrete executor
- `Hermes-Agent` 只作为显式 OPL receipt/proof lane，不持有默认 runtime、authoring executor、grant truth 或 quality verdict
- `Med Auto Grant` 继续持有 grant domain truth、author-side route 与导出物 owner
- 当前 landed 的只是“本地 submission-ready 交付包导出”，不是外部官网自动提交、不是成熟 Web UI，也不是 Word/PDF 全自动定稿系统
- 这条命令面也不重写 MAG 的正文 authoring 完成语义；它只定义更严格的本地交付 gate
- 机械材料完整性只能形成 `mechanical_package_completeness`；submission-ready 授权必须来自 MAG owner 或 AI-backed reviewer/export artifact/receipt 的 `submission_ready_export_verdict`

## Landed Facts

### 1. 新增正式导出命令 `build-submission-ready-package`

当前用户、Agent、`MedAutoGrantDomainEntry` 与 future caller 都可以通过同一条 service-safe 命令触发本地 submission-ready 导出：

- `uv run python -m med_autogrant build-submission-ready-package --input <workspace-path> --output-dir <submission-ready-output-dir> --format json`

这条命令已经进入：

- `cli.py`
- `domain_entry.py`
- `domain_runtime_parts/substrate.py`
- `product_entry.py`
- hosted contract bundle / product entry command catalog / grant cockpit command surface

因此它已经不是 repo-local helper，而是当前 repo-tracked command surface 的正式组成部分。

### 2. 导出链现在一键收口成四份本地交付物

当输入 workspace 满足 submission-ready 条件时，当前命令会一次性导出：

- `artifact_bundle`
- `final_package`
- `hosted_contract_bundle`
- `submission_ready_package`

其中 `submission_ready_package` 由 `submission-ready-package.schema.json` 冻结，当前至少包含：

- `readiness_verdict`
- `fully_automatic`
- `submission_ready`
- `external_submission_performed`
- `mechanical_package_completeness`
- `submission_ready_export_verdict`
- `audit_summary`
- `artifact_manifest`
- `submission_dossier`
- `blocking_issues`

这里保留的 `fully_automatic` 不再表示 AI-first submission readiness；本地 materialization 可以自动执行，但 `submission_ready=true` 只能由 owner-backed `submission_ready_export_verdict` 授权。

### 3. 导出逻辑保持 fail-closed，而不是凑合导出

当前命令不会对不完整的 frozen workspace，也不会对缺少 MAG/AI-backed owner export verdict 的 workspace 勉强写出交付目录。

只要出现下面任一问题，就会直接报错并拒绝写出输出目录：

- `final_package.package_kind != final_package`
- `hosted_contract_bundle.bundle_kind != hosted_contract_bundle`
- `checkpoint_status != submission_frozen`
- `draft_status != frozen`
- `presubmission_frozen != true`
- funding brief 要求的 mandatory sections 未补齐
- `preliminary_evidence_pack.evidence_items` 为空
- evidence item 仍有未关闭 `gaps`
- 缺少 representative outputs
- 缺少 active projects / reusable research assets
- 缺少带 `owner`、`export_verdict_ref`、`source_kind` 与 `provenance_ref` 的 `submission_ready_export_verdict`
- `submission_ready_export_verdict.verdict_state != submission_ready`

这意味着当前口径不是“能导出一个差不多的包”，而是“只有达到 submission-ready gate 才允许导出本地交付目录”。

机械 gate 现在只写入 `mechanical_package_completeness.status=passed|blocked`。它可以说明必备章节、证据、代表作、在研项目和 frozen package chain 是否完整，但不能签署或替代 submission-ready export verdict。

### 3.5 这条严格 gate 不等于正文 authoring 的唯一完成条件

在当前 MAG 任务边界下，申请书正文的科学问题、论证闭合、申请人适配与技术路线已经达到 `near_submission_candidate` / `submission_grade_candidate` 时，可以先停在供申请人审查的 authoring stop surface。

签字、伦理编号、行政附件、预算表单、portal 字段等客观补件，默认属于 TODO / explicit wake-up follow-up，而不是正文 authoring blocker。只有这些缺口直接破坏正文中已经使用的科学主张时，它们才会回到 authoring blocker 语义。

因此：

- `package submission-ready` 继续保持严格 fail-closed
- MAG 的正文 authoring 完成语义继续由科学质量和申请人侧可审查性决定

### 4. `product product entry` 已把这条导出动作暴露给用户

`product-entry-manifest`、`product-status`、`grant-cockpit` 与 `product_entry_quickstart` 现在都已经显式带出：

- `build_submission_ready_package`

因此从用户侧看，当前 direct grant product entry 已能回答：

- 下一步如何继续主线
- 如何查看 progress / cockpit
- 如何在冻结且材料齐备后，一键导出本地 submission-ready package

### 5. `grant_authoring_readiness` 的诚实边界仍然不变

即使本地 submission-ready package 已 landed，当前 readiness 仍然保持：

- `fully_automatic = false`
- `usable_now = true`
- `good_to_use_now = false`

原因是用户视角的“fully automatic submission-ready product”还缺：

- 自动补齐真实材料
- 文献检索与引用绑定产品化
- 图件生成与结果图补全
- Word/PDF 定稿与版式审查
- 外部官网代投 / 自动提交

因此当前最诚实的说法是：

- `Med Auto Grant` 已经可以把“机械完整且通过 MAG/AI-backed owner export verdict gate 的本地 submission-ready 交付目录”一键导出
- 它也允许在正文科学性已收口但客观补件尚未齐备时，先把任务停在申请人审查 / TODO / 显式唤醒边界
- 但它仍不是“从零材料到官网提交”的全自动成熟产品

## Verification

本 tranche 至少覆盖：

- `uv run pytest tests/test_submission_ready_package.py -q`
- `uv run pytest tests/test_domain_entry.py tests/test_hosted_contract_bundle.py tests/test_schema_registry.py tests/product_entry_cases -q`
- `uv run pytest tests/test_domain_runtime.py tests/test_mainline_status.py tests/test_program_control_surfaces.py -q`
- `scripts/verify.sh`
- `scripts/verify.sh full`

重点验证：

- `build-submission-ready-package` 已进入 CLI / domain entry / hosted bundle / product entry command catalog
- `submission-ready-package.schema.json` 已进入 schema index 与相关 bundle/export truth
- incomplete frozen workspace 会 fail-closed 拒绝导出
- 缺少 owner-backed `submission_ready_export_verdict` 的 mechanically complete workspace 会 fail-closed 拒绝导出
- complete frozen workspace 只有在 MAG/AI-backed owner export verdict 存在时才会稳定导出四份本地交付物
- docs / current-program / mainline-status / product product entry 对 `P4.F` 口径保持同步

## Honest Boundary

这条 current truth 只说明：

- 本地 submission-ready 交付包已经 landed 为正式 command surface
- 当前系统已经能对满足 mechanical completeness 与 owner export verdict gate 的 workspace 一键导出本地交付目录
- 当前导出逻辑保持 fail-closed，不会为缺材料的 workspace 生成伪完成包

它不意味着：

- mature direct grant Web UI / hosted runtime 已完成
- 旧 `OPL Gateway` landed wording 只保留为 provenance，不是 current owner line
- 图件、Word/PDF、官网提交流程已经全自动产品化
- 系统可以在缺少真实材料时凭空生成可信、可提交的国自然标书
- Gateway / hosted runtime compatibility surface 不是当前目标
