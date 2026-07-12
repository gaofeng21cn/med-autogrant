# MAG 私有实现与 OPL 迁移台账

Owner: `Med Auto Grant`
Purpose: `private_surface_inventory`
State: `current`
Machine boundary: 本文是人读 inventory。机器分类归 `contracts/functional_privatization_audit.json`、`contracts/private_functional_surface_policy.json`、current-program 与 OPL conformance output。

## 当前 Inventory

| Surface | 当前分类 | Owner / 结果 |
| --- | --- | --- |
| `agent/` stages/prompts/skills/knowledge/gates | declarative pack | 唯一 inventory 在 `contracts/pack_compiler_input.json#declarative_domain_pack`；MAG source，OPL compiler消费 |
| action catalog / stage control plane | declarative contract | MAG声明，OPL runtime消费 |
| domain handler export/dispatch | refs-only domain adapter | MAG，3 actions |
| fundability/quality/export verdict | minimal authority function | MAG retained |
| final package authority | minimal authority function | MAG retained |
| memory accept/reject | minimal authority function | MAG retained |
| owner receipt signer / typed blocker | minimal authority function | MAG retained |
| AI route policy | declarative declared-stage scope | Codex-owned semantic route; no MAG program authority |
| grant prompt / typed closeout and answer validation / direct CLI-domain handler | refs-only domain adapter | MAG retained；所有 executor transport直接消费 `opl_framework.executor_client` |
| Codex/OPL executor subprocess / timeout / request temp / process cleanup / receipt envelope | OPL Runway | MAG private transport全部 deleted |
| Codex plugin install/update/remove、marketplace/symlink lifecycle | OPL Connect | MAG installer 与 shell wrapper deleted；canonical module id=`medautogrant` |
| generated product/status/user-loop/workbench | OPL generated surface | MAG private implementations deleted |
| scheduler/queue/attempt ledger/session/lifecycle transport | OPL platform | MAG private implementations deleted |
| private pack compiler/source scanner/consumer-thinning mesh | OPL platform | deleted |
| stale production/adoption snapshots | provenance | active copies deleted |
| compatibility alias/bootstrap/facade tests | retired | deleted |

## Exact Allowed Source Matches

OPL scanner allowed matches 只能由 compact functional audit 对具体文件声明。该 audit 只枚举八项 authority/refs adapter；declarative pack 不再作为第二份 module inventory：

- `domain_executor_client.py`
- `authoring_executor.py` / `authoring_executor_parts.py`
- `critique_executor.py`
- direct domain handler files
- `primitives.py`
- `domain_memory_runtime.py`
- owner receipt/typed blocker files

允许分类只包括 `domain_authority`、`minimal_authority_function`、`refs_only_domain_adapter` 或明确 provenance。禁止 blanket directory coverage，也禁止改名躲扫描。

## Morphology Policy

`contracts/private_functional_surface_policy.json#/physical_source_morphology_policy` 只保留 OPL scanner要求的 12 surface classifications、forbidden residue classes 与 false-owner guards。它不复制 source scanner、deleted-path inventory 或 physical delete workflow。

## Retirement Rule

无 production caller且不属于八项 authority 的程序面直接删除。Tests/docs/contracts 只能更新到新 owner surface，不得恢复 wrapper。历史来源从 git history 或 `docs/history/**` 读取。

Default caller 中 `product_entry/product_status/product_session/workbench` 已物理不存在，机器声明为 retired；`cli/domain_handler` 是合法 direct authority adapter，以 `keep_as_authority_adapter_ref`、no-forbidden-write 和 provenance refs 关闭退休门，不得误删。

## Verification

- `make test-descriptor-contracts`
- `./scripts/verify.sh full`
- OPL conformance latest HEAD
- active deleted-path inventory = 0
- source matched/blocking = 0
