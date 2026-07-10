# Product Entry Support Record

Owner: `Med Auto Grant`
Purpose: `product_entry_support_record`
State: `support_current_truth`
Machine boundary: 本文是人读 support record。机器真相继续归 `contracts/runtime-program/current-program.json`、`contracts/generated_surface_handoff.json`、schemas、source、CLI/API behavior、runtime receipts 和语义化 `human_doc:*` id。

## 当前读法

本文件吸收旧 P3/P4 dated specs 中仍 current 的 generated caller、product/status/user-loop 与 package/export 边界。旧逐 tranche 长正文已压缩到 `docs/history/specs/README.md` 与 git history，只作为 provenance 阅读。

MAG 的 public identity 仍是单一 `Med Auto Grant` app skill。OPL/App 根据 declarative pack 与 generated-surface handoff 提供 product-entry、status、user-loop 和 workbench；这些 caller 只能回到 MAG domain handler 与 authority surface，不能成为第二份 grant truth。Package/export authority 仍归 MAG。

## Support Matrix

| Surface | Current owner | Machine source | Forbidden reading |
| --- | --- | --- | --- |
| Grant cockpit / progress projection | OPL/App generated surface | `contracts/generated_surface_handoff.json`, stage/action descriptors, runtime refs | 不写成 MAG-owned runtime、OPL grant truth 或 production ready。 |
| Direct grant entry composition | OPL generated caller -> MAG route/action target | action/stage contracts, schemas, CLI/API behavior | 不恢复旧 direct-entry/Gateway wrapper，不让 caller 绕过 MAG authority。 |
| Mainline status / grant user loop | OPL/App generated surface | stage/action descriptors, runtime/owner receipt refs | 不把 status prose、projection 或 checklist 写成 fundability/quality/export verdict。 |
| Schema-backed product descriptors | OPL generated surface | `contracts/pack_compiler_input.json`, `contracts/generated_surface_handoff.json`, schemas | 不把 descriptor completeness 写成 authoring completion、submission readiness 或 hosted product maturity。 |
| Local submission-ready package | MAG package/export authority support | package/export source, artifact refs, submission/export gates | 不把 local package existence 写成 portal submission, human approval, fundability verdict or final submission authority。 |

## Package / Export SSOT Readout

`Local submission-ready package` 按三层读取：

| Layer | Current owner | Current reading |
| --- | --- | --- |
| Scientific review-ready | MAG fundability / authoring quality owner surface | 只说明 grant draft 或 review artifact 已通过对应质量判断；不能推出 export gate、portal action 或 submission-ready package。 |
| Local submission-ready package / export gate | MAG package authority、package/export gate、owner receipt 或 typed blocker | 需要 package refs、artifact refs、provenance、manual portal boundary 和 `submission_ready_export_verdict` owner/provenance signature。package existence、schema completeness、lifecycle completion、provider completion 或 grouped CLI success 都不能单独声明 ready。 |
| External submitted / portal submission | Human-supervised portal action receipt | 只在独立人工 portal receipt 存在时成立；MAG 和 OPL 不能静默声明外部提交完成。 |

Package/export 的机器 SSOT 分层如下：

- MAG authority truth: `agent/knowledge/package_authority.md`、`agent/quality_gates/export_and_package.md`、`contracts/stage_control_plane.json`、`contracts/private_functional_surface_policy.json`、package/export source、owner receipts 和 typed blockers。
- Refs-only handoff truth: `contracts/generated_surface_handoff.json`、`contracts/runtime-program/current-program.json` 与 direct domain handler export。OPL 只消费 package/artifact/receipt/blocker refs；不读取或输出 package body、grant artifact body、private evidence 或 verdict body。
- OPL/shared truth: OPL 持有 artifact/package lifecycle shell、stage artifact physical kernel、locator、retention UI 和 refs projection consumption；OPL 不持有 MAG package authority，不能声明 export-ready、submission-ready、quality-ready 或 portal-submitted。

## 历史入口

旧 hosted caller / OPL handoff / P4 product-entry support specs 已压缩为 [历史 specs](../history/specs/README.md) 的主题记录。当前 generated caller / product status / user-loop / package-export 支撑读法以本文、核心五件套、`current-program.json`、generated-surface handoff、schemas/source/tests 和 owner receipts 为准；原逐文件长正文只从 git history 读取。
