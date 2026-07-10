# MAG 私有实现与 OPL 迁移台账

Owner: `Med Auto Grant`
Purpose: `private_surface_inventory`
State: `current`
Machine boundary: 本文是人读 inventory。机器分类归 `contracts/functional_privatization_audit.json`、`contracts/private_functional_surface_policy.json`、current-program 与 OPL conformance output。

## 当前 Inventory

| Surface | 当前分类 | Owner / 结果 |
| --- | --- | --- |
| `agent/` stages/prompts/skills/knowledge/gates | declarative pack | MAG source，OPL compiler消费 |
| action catalog / stage control plane | declarative contract | MAG声明，OPL runtime消费 |
| domain handler export/dispatch | refs-only domain adapter | MAG，3 actions |
| fundability/quality/export verdict | domain authority | MAG retained |
| final package authority | domain authority | MAG retained |
| memory accept/reject | minimal authority function | MAG retained |
| owner receipt signer / typed blocker | minimal authority function | MAG retained |
| transition oracle | domain authority | MAG retained |
| codex/grant-native helper | refs-only domain adapter | MAG retained |
| generated product/status/user-loop/workbench | OPL generated surface | MAG private implementations deleted |
| scheduler/queue/attempt ledger/session/lifecycle transport | OPL platform | MAG private implementations deleted |
| private pack compiler/source scanner/consumer-thinning mesh | OPL platform | deleted |
| stale production/adoption snapshots | provenance | active copies deleted |
| compatibility alias/bootstrap/facade tests | retired | deleted |

## Exact Allowed Source Matches

OPL scanner allowed matches 只能由 functional audit 对具体文件声明：

- `codex_cli.py`
- direct domain handler files
- `primitives.py`
- `domain_memory_runtime.py`
- owner receipt/typed blocker files

允许分类只包括 `domain_authority`、`minimal_authority_function`、`refs_only_domain_adapter` 或明确 provenance。禁止 blanket directory coverage，也禁止改名躲扫描。

## Morphology Policy

`contracts/private_functional_surface_policy.json#/physical_source_morphology_policy` 只保留 OPL scanner要求的 12 surface classifications、forbidden residue classes 与 false-owner guards。它不复制 source scanner、deleted-path inventory 或 physical delete workflow。

## Retirement Rule

无 production caller且不属于八项 authority 的程序面直接删除。Tests/docs/contracts 只能更新到新 owner surface，不得恢复 wrapper。历史来源从 git history 或 `docs/history/**` 读取。

## Verification

- `make test-descriptor-contracts`
- `./scripts/verify.sh full`
- OPL conformance latest HEAD
- active deleted-path inventory = 0
- source matched/blocking = 0
