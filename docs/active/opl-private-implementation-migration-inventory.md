# MAG 私有实现与 OPL 迁移台账

Owner: `Med Auto Grant`
Purpose: `opl_private_implementation_migration_inventory`
State: `active_inventory`
Machine boundary: 本文是 human-readable 迁移治理台账。机器真相继续归 `contracts/`、schemas、CLI/API 行为、product-entry manifest、sidecar export/dispatch、runtime receipts、workspace artifact 与 MAG owner receipt。
Date: `2026-05-21`

## 当前 clean truth

MAG 是 OPL-compatible grant domain agent。OPL Framework 持有通用 provider runtime、queue、attempt ledger、generic transition runner、workspace/source shell、memory locator、artifact/package lifecycle shell、generated wrapper、observability/SLO 和 App/workbench shell。MAG 必须保留 grant truth、fundability / quality / export verdict、package authority、grant strategy memory body 与 accept/reject decision、owner receipt、transition oracle、typed blocker 和 grant-native helper。

本轮 scan 没有发现需要迁入 OPL 的 grant authority；风险集中在 hand-written product-entry / sidecar / CLI / autonomy controller / domain-runtime 命名和大型聚合文件，容易被误读成 MAG 私有平台。当前这些 surface 只能按 direct domain handler、refs-only adapter、minimal authority function、diagnostic、migration input 或 history/tombstone 读取。

2026-05-21 本轮最小清理已把 `product_entry_parts/sidecar.py` 的 TODO/wakeup 投影从历史 Hermes 24h substrate 口径收薄为 `opl_wakeup_contract`：OPL 持有 typed family queue / provider wakeup shell，MAG 只暴露 `open_grant_user_loop` / `product user-loop` refs-only authoring continuation action target、owner receipt / typed blocker / no-regression return shape 和 no private runtime role flags；`status/read`、`user-loop/wakeup` 与 `notification/receipt` 不再是 sidecar dispatch actions。该改动不声明 OPL generated sidecar 已 default 化，也不迁移 grant truth、quality/export verdict、package authority 或 controller decision。

## 分类词表

| class | 含义 |
| --- | --- |
| `domain_authority_retained` | MAG 必须保留的 grant truth、AI-first verdict、package/memory/receipt authority 或 grant-native helper。 |
| `opl_framework_migration_candidate` | 当前手写外壳长期应由 OPL generated/hosted surface 或 shared primitive 承担。 |
| `already_thin_adapter` | 已收薄为 refs-only adapter/projection/diagnostic，仍因 direct path 或 evidence caller 暂留。 |
| `needs_split_before_migration` | 同一文件混合 grant authority 与 generic shell，必须先拆 owner 子域。 |

## Inventory

| surface | lines | class | current active caller | 当前实际职责 | 为什么属于该分类 | MAG 必须保留的 authority | 可迁往 OPL 的 generic 子域 | 迁移/退役门槛 | 推荐验证入口 |
| --- | ---: | --- | --- | --- | --- | --- | --- | --- | --- |
| `src/med_autogrant/product_entry_parts/manifest_builder.py` | 987 | `needs_split_before_migration` | product-entry manifest/status、direct entry、sidecar export、tests/product_entry_cases | 聚合 domain entry contract、stage control plane、runtime registration、workspace locator、artifact/package/memory projections、consumer-thinning surfaces | manifest builder 同时组装 grant refs 和 generic product/status/workbench shell；迁移前需把 grant authority refs 与 generic manifest shell 分开 | grant truth refs、fundability/quality/export refs、package authority refs、owner receipt refs、transition oracle refs | generated product-entry/status/workbench manifest shell、App operator projection shell | OPL generated/hosted caller evidence、direct/hosted parity、owner receipt/typed blocker roundtrip、no-forbidden-write、no-active compatibility alias | `tests/product_entry_cases/test_manifest_and_status.py`、`tests/test_opl_family_contract_adoption.py`、`scripts/verify.sh` |
| `src/med_autogrant/product_entry_parts/sidecar.py` | 911 | `opl_framework_migration_candidate` | `product sidecar export|dispatch`、OPL family provider bridge、sidecar tests | refs-only sidecar export、guarded action dispatch、stage/memory/lifecycle receipt dispatch、notification receipt | sidecar shell 与 typed queue/dispatch transport 长期归 OPL；MAG 只应保留 guarded domain action handler 与 receipt signer | package authority、grant memory accept/reject receipt、owner receipt、typed blocker、safe action metadata | generated sidecar wrapper、typed queue dispatch shell、generic lifecycle/memory/package transport envelope | OPL sidecar wrapper default 化、owner receipt roundtrip、direct/hosted no-regression、no-active compat alias | `tests/product_entry_cases/test_sidecar.py`、`make test-meta` |
| `src/med_autogrant/product_entry_parts/consumer_thinning.py` | 954 | `already_thin_adapter` | manifest/sidecar/functional audit projection | MAG consumer-thinning / external evidence request pack / bridge exit gate | 当前已是 refs-only migration contract，不应扩写成 runtime owner | retained authority taxonomy、request refs、forbidden output boundary | OPL functional privatization audit projection shell | 保持 refs-only；路径漂移时刷新 source refs；不声明 OPL replacement production ready | `make test-meta`、`tests/test_opl_family_contract_adoption.py` |
| `src/med_autogrant/product_entry_parts/consumer_thinning_audit.py` | 909 | `already_thin_adapter` | product-entry manifest、functional audit tests | 私有功能面审计与 no-resurrection policy | 它是 audit/read model，不应持有 runtime/action authority | grant authority surface classification | OPL audit detail projection | 保持 no generic owner flags；新增 surface 必须有 class 和 authority boundary | `make test-meta` |
| `src/med_autogrant/product_entry_parts/consumer_thinning_pack.py` | 901 | `already_thin_adapter` | pack compiler / manifest read projection | generated surface handoff、pack source refs、bridge gate refs | 已是 machine handoff/projection | authority refs and pack boundary | OPL generated surface compiler/read model | OPL compile/readiness proof；不写 production caller complete | `tests/test_opl_family_contract_adoption.py` |
| `src/med_autogrant/grant_autonomy_controller.py` | 961 | `needs_split_before_migration` | autonomy controller command、sidecar guarded action、controller tests | grant route/budget/reselection/rollback/quality scheduling policy | 包含 domain route policy 与 loop/scheduler-like control；必须防止被读成 MAG-owned runtime loop | grant route truth、budget/blocker policy、owner receipt/typed blocker、AI-first review handoff refs | scheduler/watch shell、generic attempt lifecycle、retry/dead-letter、operator loop shell | AI-first review evidence、OPL provider/attempt parity、no scheduler owner claim、focused tests、no-forbidden-write | `tests/test_grant_autonomy_controller.py`、`tests/test_grant_governance_adapter.py` |
| `src/med_autogrant/grant_autonomy_parts.py` | 883 | `domain_authority_retained` with split pressure | autonomy controller internals | grant-specific route/budget/helper policy | 大但主要是 grant-native route helper；不迁 OPL，但应避免继续承载 generic loop | grant controller helper, typed blocker policy | none except generic loop envelope | 只做 semantic split，不迁 authority | `tests/test_grant_autonomy_controller.py` |
| `src/med_autogrant/cli.py` | 620 | `opl_framework_migration_candidate` | direct MAG CLI、product/user-loop/status/sidecar commands | grouped CLI dispatch | CLI wrapper 长期由 OPL generated surface 承担；MAG 保留 direct handler target until cutover | direct domain entry、owner receipt reader、grant command target | generated CLI/MCP/product shell | generated caller parity、no old alias/facade active caller、direct path no-regression | `tests/product_entry_cases/test_cli_dispatch.py`、`scripts/verify.sh` |
| `src/med_autogrant/domain_runtime_parts/io.py` | 625 | `already_thin_adapter` | final package / workspace IO helpers | workspace/package IO helper | IO helper 是 domain handler support；不应成为 runtime substrate owner | package/source IO validation | generic workspace/source locator only | OPL locator parity before any shell migration; package authority remains MAG | `tests/test_final_package.py` |
| `src/med_autogrant/product_entry_parts/runtime_surfaces.py` | 679 | `already_thin_adapter` | manifest/status/sidecar runtime projection | OPL provider/runtime contract refs and runtime-readiness projection | 已是 refs-only runtime contract projection；不能声明 MAG runtime owner | runtime authority boundary refs | OPL runtime/readiness projection owner | keep `opl_provider_runtime_contract`; no provider-ready => grant-ready claim | product-entry status tests |
| `src/med_autogrant/product_entry_parts/owner_receipts.py` | 744 | `domain_authority_retained` | owner receipt / production acceptance / sidecar closeout | MAG owner receipt materialization | owner receipt signer 必须留 MAG | owner receipt signing, typed blocker refs | OPL receipt ledger/index only | 不迁 signer；OPL only stores/queries refs | `tests/test_production_acceptance.py`、owner receipt tests |
| `src/med_autogrant/stage_control_plane.py` | 725 | `domain_authority_retained` | pack compiler, manifest, OPL stages readiness | MAG stage semantics and transition oracle | stage semantics 属于 grant domain pack；OPL 可消费但不能改写 verdict | stage prompt/skill/quality gate semantics, transition oracle | generic stage runner/attempt shell | OPL consumes stage refs; no quality verdict generation | stage control / OPL family contract tests |
| `src/med_autogrant/opl_standard_pack.py` | 885 | `domain_authority_retained` | pack/conformance tests | declarative grant pack contract materialization | domain pack/contract source，不是 generic runtime；private policy builder 已拆出以满足 repo line budget | grant semantic pack, required refs | OPL pack compiler only consumes | Keep pack source; split only if maintainability requires | `tests/test_opl_family_contract_adoption.py` |
| `src/med_autogrant/opl_standard_pack_private_policy.py` | 196 | `already_thin_adapter` | `opl_standard_pack.py` policy builder | private functional surface policy materialization | 从 standard pack 拆出的同语义 builder，只生成 audit policy，不持有 runtime/action authority | private authority taxonomy and no-resurrection policy | OPL audit/policy consumer only | 保持生成合同无漂移；不加入 runtime owner 字段 | `tests/test_opl_standard_pack.py`、`make test-meta` |

## Bad-smell flags

- Large hand-written CLI aggregator: `src/med_autogrant/cli.py`.
- Private sidecar/runtime-looking shell: `product_entry_parts/sidecar.py`, `runtime_surfaces.py`, `domain_runtime_parts/io.py`.
- Status/read-model mixed with runtime authority risk: `manifest_builder.py` and product status surfaces.
- Compatibility wrapper risk: grouped CLI and old local runtime/Hermes language must remain tombstone/provenance only.
- Descriptor/external receipt ready must not be written as grant-ready, fundability-ready, export-ready or production long-soak complete.
- Mechanical scorecard/schema/package existence must not replace AI-first grant review / export verdict.

## Immediate thinning items

1. Split `manifest_builder.py` into manifest shell assembly vs grant authority ref builders before any migration claim.
2. Keep `sidecar.py` dispatch as MAG domain handler target until OPL generated sidecar is default; do not add more generic dispatch actions. Current TODO/wakeup output now uses `opl_wakeup_contract`, targets `open_grant_user_loop` outside sidecar dispatch, and forbids Hermes 24h substrate / MAG scheduler / MAG attempt ledger / MAG App workbench ownership.
3. Treat `grant_autonomy_controller.py` as grant route/budget/blocker policy only; move any generic loop/scheduler language to OPL evidence gates.
4. Keep consumer-thinning files as refs-only audit/projection; do not add runtime owner fields.

## OPL primitive dependencies

- generated product/status/workbench/sidecar default caller;
- typed queue and sidecar dispatch shell with owner receipt roundtrip;
- OPL wakeup/provider queue shell consuming `open_grant_user_loop` refs, with MAG returning only owner receipt / typed blocker / no-regression refs;
- generic lifecycle/session/package locator shell;
- App/operator read model consuming MAG refs without grant verdict generation;
- production/default caller and Temporal long-soak evidence from OPL/App side.

## Forbidden claims

- `mag_functional_structure_gap_count=0` does not mean physical source cleanup complete.
- OPL stage evidence receipt verified does not mean grant-ready or submission-ready.
- package existence, quality scorecard, schema completeness, controller route or queue completion cannot become fundability/quality/export verdict.
- active caller still in MAG means OPL has not fully taken over that surface.
