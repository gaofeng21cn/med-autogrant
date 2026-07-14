# MAG 私有实现与 OPL 迁移台账

Owner: `Med Auto Grant`
Purpose: `private_surface_inventory`
State: `current`
Machine boundary: 本文是人读 inventory。机器分类归 `contracts/functional_privatization_audit.json`、`contracts/private_functional_surface_policy.json`、current-program 与 OPL conformance output。

## 当前 Inventory

| Surface | 当前分类 | Owner / 结果 |
| --- | --- | --- |
| `agent/` stages/prompts/skills/knowledge/gates | declarative pack | 唯一 inventory 在 `contracts/pack_compiler_input.json#declarative_domain_pack`；MAG source，OPL compiler消费 |
| action catalog / stage control plane | declarative contract | MAG只声明 3 个 closed `stage_binding` action 与 exact input schema；OPL runtime消费并生成 hosted surfaces |
| CLI parser / execution dispatch | declarative metadata + explicit static dispatch | MAG只用 command specs声明参数；已删除 argparse `handler` 注入、`runtime_method` 与 `getattr` 动态分派 |
| domain handler export/dispatch | refs-only domain adapter | MAG，3 actions；显式静态路由到实际 authority/runtime function |
| fundability/quality/export verdict | minimal authority function | MAG retained |
| final package authority | minimal authority function | MAG retained |
| memory accept/reject | minimal authority function | MAG retained |
| owner receipt signer / typed blocker | minimal authority function | MAG retained |
| AI route policy | declarative declared-stage scope | decisive Codex Attempt owns semantic route decision；OPL StageRun controller 只校验并物化 transition；MAG 无 program authority |
| grant prompt / typed closeout and answer validation / direct CLI-domain handler | refs-only domain adapter | MAG retained；所有 executor transport直接消费 `opl_framework.executor_client` |
| Codex/OPL executor subprocess / timeout / request temp / process cleanup / receipt envelope | OPL Runway | MAG private transport全部 deleted |
| HTTPS source transport / redirect、timeout、decode与 policy enforcement | OPL Framework `source_transport` | MAG只保留 3 个官方 URL exact allowlist、User-Agent 与 funding HTML解析语义；`urllib` transport已删除 |
| Agent Package/Codex carrier install/update/uninstall、marketplace/symlink lifecycle | OPL Packages | MAG installer 与 shell wrapper deleted；canonical package id=`mag`，runtime source module locator=`medautogrant` |
| generated product/status/user-loop/workbench | OPL generated surface | MAG private implementations deleted |
| scheduler/queue/attempt ledger/session/lifecycle transport | OPL platform | MAG private implementations deleted |
| private pack compiler/source scanner/consumer-thinning mesh | OPL platform | deleted |
| stale production/adoption snapshots | provenance | active copies deleted |
| compatibility alias/bootstrap/facade tests | retired | deleted |

## Exact Allowed Source Matches

OPL scanner 的 sensitive-effect 放行只能由 `contracts/source_closure_audit.json` 对 exact file、symbol、source digest、effect 与 target声明。当前 audit 是 closed 9-entry surface：1 个不可达 developer tool `git` process spawn、6 个 domain output writer、1 个 domain-memory receipt writer、1 个 owner-receipt writer；scanner readback 的 unresolved/private generic/unreachable sensitive/audit mismatch 均为 `0`。

Functional audit 的 allowed source matches 只枚举七项 authority/refs adapter；declarative pack 不再作为第二份 module inventory：

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

无 production caller且不属于七项 authority 的程序面直接删除。Tests/docs/contracts 只能更新到新 owner surface，不得恢复 wrapper。历史来源从 git history 或 `docs/history/**` 读取。

Default caller 中 `product_entry/product_status/product_session/workbench` 已物理不存在，机器声明为 retired；`cli/domain_handler` 是合法 direct authority adapter，以 `keep_as_authority_adapter_ref`、no-forbidden-write 和 provenance refs 关闭退休门，不得误删。

## Verification

- `make test-descriptor-contracts`
- `./scripts/verify.sh full`
- OPL `agents scaffold --validate` / `agents interfaces` / `agents source-closure` / isolated `agents conformance`
- active deleted-path inventory = 0
- source closure unresolved/private generic/unreachable sensitive/audit mismatch = 0
