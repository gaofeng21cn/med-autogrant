# MAG 文档组合治理

Status: `active_docs_governance`
Owner: `Med Auto Grant`
Purpose: `docs_lifecycle_governance`
State: `active_support`
Machine boundary: 本文是人读治理入口。MAG 机器真相继续归 `contracts/runtime-program/current-program.json`、schema、source、CLI/API 行为、product-entry manifest、runtime receipts 和语义化 `human_doc:*` id。

## 当前结论

`docs/**` 是 MAG 的中文内部开发与维护参考，不再维护 docs 层双语镜像。稳定路径优先使用无语言后缀 `.md` 承载中文 canonical 内容。历史文件可以保留旧双语或旧路径描述作为 provenance，但 active/reference 索引必须指向当前无后缀路径。

MAG 采用 OPL-family canonical docs taxonomy：

`active/public/product/runtime/delivery/source/policies/specs/references/history`

这个目录集合按长期职责保留，不按当前文件数量决定。MAG 当前真实 owner 主要在核心五件套、`active/`、`references/`、`specs/` 和 `history/`；`public/product/runtime/delivery/source/policies` 当前较薄，但都有长期职责，后续按 current 内容小批量吸收。

## 与 OPL 的分层

OPL 系列项目全局主参考是 `/Users/gaofeng/workspace/one-person-lab/docs/active/opl-family-development-reference.md`。它持有全局 framework 目标、跨仓差距顺序、shared primitive 上收、App/workbench 目标和同名 docs taxonomy。

MAG 文档只维护 grant domain agent 的目标、差距、grant truth、fundability/quality/export authority、direct app skill path、OPL-hosted sidecar/projection/receipt 边界，以及 MAG-to-OPL 上收候选。MAS、RCA、MDS 或 OPL-owned App/workbench 的并行 backlog 不写入 MAG active docs。

## 目录职责

| 目录 | 长期职责 | 当前 MAG 承载 |
| --- | --- | --- |
| `docs/` root | docs 入口、核心五件套、docs governance、root public allowlist | `README.md`、核心五件套、`domain-positioning.md`、`mvp-scope.md`、本文件。 |
| `docs/active/` | 当前计划、当前 gap、active baton、closeout evidence | `mag-ideal-state-cross-repo-gap-plan.md`。 |
| `docs/public/` | public narrative index | 当前较薄；未来可吸收 `domain-positioning.md`、`mvp-scope.md`，但需先处理 path stability。 |
| `docs/product/` | app skill、product status、user-loop、direct entry、operator guidance | 当前较薄；后续从 core docs/specs/contracts 抽取仍 current 的 product-entry 内容。 |
| `docs/runtime/` | runtime/control/projection、OPL-hosted boundary、receipt/projection 支撑 | 当前较薄；runtime truth 仍在 contracts/source/status/specs。 |
| `docs/delivery/` | submission-ready package、export、delivery、manual portal boundary | 当前较薄；grant artifact/export authority 仍 MAG-owned。 |
| `docs/source/` | funder/task/source intake、workspace canonical document、source truth consumption | 当前较薄；后续承接 workspace/source intake 和 funder-source 边界。 |
| `docs/policies/` | 稳定治理规则、文档规则、repo-local operating discipline | 当前较薄；长期规则可从 invariants/decisions/governance checklist 抽取。 |
| `docs/specs/` | path-stable 技术记录和 active specs | 真实承载但混合；`specs_lifecycle_map.md` 负责 active/support/history 分流。 |
| `docs/references/` | north-star、OPL adoption、memory policy、governance checklist | 真实承载；不承担 active owner。 |
| `docs/history/` | 完成计划、旧 specs、旧 provider/runtime/OMX/provenance | 真实承载；不承担 current truth。 |

## 非 canonical 目录

旧 `docs/plans/` 已物理退役，不再作为 active owner。完成计划留在 `docs/history/plans/`。如果历史计划仍含 current truth，先抽取内容进入 `active/product/runtime/delivery/source/policies/specs` 的当前 owner，再保留原文件作为 provenance。

`docs/specs/` 是 path-stable 混合层，不是旧接口兼容层。只有 README 和 `specs_lifecycle_map.md` 明确列为 active 的 specs 才能作为 current owner；其余 dated specs 按 support/history/provenance 阅读。

## 内容级整合规则

1. 当前 public identity 和 product boundary 回到根层 allowlist、核心五件套和 current-program。
2. 当前 gap、计划和 evidence ledger 留在 `docs/active/`。
3. Product-entry、user-loop、operator guidance 进入 `docs/product/`；grant truth 不迁出 MAG。
4. Runtime/control/projection 支撑进入 `docs/runtime/`；machine truth 仍归 contracts/source/runtime evidence。
5. Submission-ready package/export/delivery 支撑进入 `docs/delivery/`；fundability、quality、export verdict 和 package authority 仍归 MAG。
6. Funder/source/workspace 支撑进入 `docs/source/`；generic shell 候选记录为 MAG-to-OPL 上收边界。
7. 稳定规则进入 `docs/policies/`；一次性计划不得放入 policies。

## Direct Retirement

当旧模块、旧接口、旧 CLI alias、旧 wrapper、旧 facade、patch bridge、旧测试入口或旧文档入口已被当前 owner surface 替代时，默认直接退役。迁移 active caller 后删除旧面；需要来龙去脉时只保留 history/tombstone/provenance，不新增 compatibility shim、别名、re-export facade 或 compatibility-only 聚合测试。
