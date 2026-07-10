# MAG 文档组合治理

Owner: `Med Auto Grant`
Purpose: `docs_lifecycle_governance`
State: `active_support`
Machine boundary: 本文是人读治理入口。机器真相归 contracts、schemas、source、CLI/API behavior、runtime receipts 和语义化 `human_doc:*` id。

## Canonical 组合

MAG 使用 `active/public/product/runtime/delivery/source/policies/specs/references/history` taxonomy。

- 核心五件套承担 current 人读 truth。
- `docs/active/mag-ideal-state-cross-repo-gap-plan.md` 是唯一 active gap plan。
- `docs/active/opl-private-implementation-migration-inventory.md` 是 per-surface inventory。
- `docs/specs/specs_lifecycle_map.md` 判断 spec 的 active/support/history 角色。
- `docs/history/**` 保存旧 runtime、provider、proof、worktree、snapshot 与 tombstone。

## Direct Retirement

旧 module、CLI alias、wrapper、facade、compatibility test 或 docs entry 被当前 owner surface 替代后，迁移 caller并直接删除。需要追溯时依赖 history 或 git history，不新增 shim、re-export、别名或 compatibility-only 文档。

2026-07-10 cleanup 后，product/status/user-loop/workbench 等通用 surface 由 OPL/App generated caller承担；MAG active docs 不再描述私有 builder、pack compiler、source-purity wrapper 或 snapshot ledger 为 current。

## 写入路由

| 内容 | Owner |
| --- | --- |
| 项目角色、架构、约束、状态、决策 | 核心五件套 |
| 当前差距与完成门 | active plan |
| retained/deleted source role | migration inventory + contracts |
| package/export/manual portal | `delivery/` |
| runtime/OPL boundary | `runtime/` |
| source/workspace body boundary | `source/` |
| 技术 support record | `specs/` |
| 形成过程与旧证明 | `history/` |

新增文档前先证明现有 owner 无法承载。文档不得复制长 contract 字段、测试清单、receipt id、分支 SHA 或 frozen inventory count。

## Currentness

文档只解释如何读取 machine owner。OPL conformance、current-program、live progress、owner receipt、workspace artifact 与 package output 分别给出结构、运行、authority 和交付真相；任何文档都不能替代这些证据。
