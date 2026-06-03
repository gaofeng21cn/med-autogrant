# Product Entry Support Record

Owner: `Med Auto Grant`
Purpose: `product_entry_support_record`
State: `support_current_truth`
Machine boundary: 本文是人读 support record。机器真相继续归 `contracts/runtime-program/current-program.json`、schemas、source、CLI/API behavior、product-entry manifest、runtime receipts 和语义化 `human_doc:*` id。

## 当前读法

本文件吸收旧 P4A/P4B/P4C/P4E/P4F dated specs 中仍 current 的 product-entry、product status、user-loop、manifest 和 package/export 支撑语义。旧文件已经进入 `docs/history/specs/`，只作为 provenance 阅读。

MAG 的 public identity 仍是单一 `Med Auto Grant` app skill。Product-entry、product status、direct-entry、user-loop 和 package/export surfaces 都位于这个 skill 之下，作为 command contract、projection 或 export support；它们不能升级为第二个 public product、旧 Gateway/hosted runtime owner、submission-ready authority 或 OPL-owned grant truth。

## Support Matrix

| Surface | Current owner | Machine source | Forbidden reading |
| --- | --- | --- | --- |
| Direct grant cockpit / progress projection | MAG product-entry support under the app skill | product-entry manifest, status/read-model source, `current-program.json` | 不写成 public runtime owner、Gateway surface、OPL grant truth 或 production ready。 |
| Direct grant entry composition | MAG route/action contract with OPL discoverability | action/stage contracts, schemas, CLI/API behavior | 不恢复旧 direct-entry/Gateway 兼容入口，不把 OPL handoff 写成 MAG runtime owner。 |
| Mainline status / grant user loop | MAG status projection and user-loop support | status/source surfaces, controller/runtime receipts | 不把 status prose、projection 或 checklist 写成 fundability/quality/export verdict。 |
| Schema-backed product status and manifest | MAG manifest support | schemas, `current-program.json`, product-entry manifest | 不把 manifest completeness 写成 authoring completion、submission readiness 或 hosted product maturity。 |
| Local submission-ready package | MAG package/export authority support | package/export source, artifact refs, submission/export gates | 不把 local package existence 写成 portal submission, human approval, fundability verdict or final submission authority。 |

## 历史入口

旧 P4 support specs 保留在 [历史 specs](../history/specs/README.md)：

- `2026-04-12-p4a-direct-grant-cockpit-and-progress-projection-current-truth.md`
- `2026-04-12-p4b-direct-grant-entry-composition-current-truth.md`
- `2026-04-12-p4c-mainline-status-and-grant-user-loop-current-truth.md`
- `2026-04-13-p4e-schema-backed-product-status-and-manifest-current-truth.md`
- `2026-04-13-p4f-local-submission-ready-package-current-truth.md`

