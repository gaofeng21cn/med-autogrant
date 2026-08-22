# Product Entry Support Record

Owner: `Med Auto Grant`
Purpose: `product_entry_support_record`
State: `support_current_truth`
Machine boundary: 本文是人读 support record。机器真相继续归 `contracts/runtime-program/current-program.json`、`contracts/generated_surface_handoff.json`、schemas、source、CLI/API behavior、runtime receipts 和语义化 `human_doc:*` id。

## 当前读法

本文件说明 generated caller、product/status/user-loop 与 package/export 边界。

MAG 的 public identity 仍是单一 `Med Auto Grant` app skill。OPL/App 根据 declarative pack 与 generated-surface handoff 提供 product-entry、status、user-loop 和 workbench；这些 caller 只能回到 MAG domain handler 与 authority surface，不能成为第二份 grant truth。Package/export authority 仍归 MAG。

## Support Matrix

| Surface | Current owner | Machine source | Boundary |
| --- | --- | --- | --- |
| Grant cockpit / progress projection | OPL/App generated surface | `contracts/generated_surface_handoff.json`, stage/action descriptors, runtime refs | 展示 refs、进度和 owner answer。 |
| Direct grant entry composition | OPL generated caller -> MAG route/action target | action/stage contracts, schemas, CLI/API behavior | 调用 MAG authority target。 |
| Mainline status / grant user loop | OPL/App generated surface | stage/action descriptors, runtime/owner receipt refs | 展示 runtime 与 owner receipt 状态。 |
| Schema-backed product descriptors | OPL generated surface | `contracts/pack_compiler_input.json`, `contracts/generated_surface_handoff.json`, schemas | 描述 hosted product interface。 |
| Local submission-ready package | MAG package/export authority | package/export source, artifact refs, submission/export gates | 本地 package 与外部人工 portal action 分层。 |

## Package / Export SSOT Readout

`Local submission-ready package` 按三层读取：

| Layer | Current owner | Current reading |
| --- | --- | --- |
| Scientific review-ready | MAG fundability / authoring quality owner surface | grant draft 或 review artifact 已通过对应质量判断。 |
| Local submission-ready package / export gate | MAG package authority、package/export gate、owner receipt 或 typed blocker | package refs、artifact refs、provenance、manual portal boundary 和 `submission_ready_export_verdict`。 |
| External submitted / portal submission | Human-supervised portal action receipt | 独立人工 portal receipt。 |

Package/export 的机器 SSOT 分层如下：

- MAG authority truth: `agent/stages/manifest.json`、`agent/knowledge/package_authority.md`、`agent/quality_gates/export_and_package.md`、package/export source、owner receipts 和 typed blockers。
- Refs-only handoff: `contracts/generated_surface_handoff.json`、`contracts/runtime-program/current-program.json` 与 direct domain handler export。
- OPL/shared surfaces: artifact/package lifecycle shell、Stage Folder kernel、locator、retention UI 和 refs projection。
