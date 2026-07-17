# MAG 私有面 Owner Map

Owner: `Med Auto Grant`
Purpose: `private_surface_machine_owner_router`
State: `active_support`
Machine boundary: 本文是人读路由表，不是 source/path inventory、scanner snapshot、物理删除授权或 readiness 证明。当前分类必须从下列 machine owners 和 fresh readback 获取。

## Current Owner Map

| Theme | Canonical owner | Human read rule |
| --- | --- | --- |
| Current runtime/domain split | `contracts/runtime-program/current-program.json` | 读取当前 phase、tranche、runtime owner 与 domain authority owner |
| Declarative Grant Pack | `contracts/pack_compiler_input.json`, `agent/` | MAG 声明 domain pack；OPL 生成通用 hosted surfaces |
| Public actions and Stage routing | `contracts/action_catalog.json`, `agent/stages/manifest.json` | action 与 route 只从声明源读取，不从本文复制 |
| Retained authority functions and adapters | `contracts/functional_privatization_audit.json` | 由 machine classification 判断 retain、owner 与 caller；本文不维护文件清单 |
| Private/generic surface prohibition | `contracts/private_functional_surface_policy.json` | generic runtime、projection、compiler 与 lifecycle 不得在 MAG 复活 |
| Sensitive source effects | `contracts/source_closure_audit.json` | exact file、symbol、digest、effect 与 target 只从 audit/readback 读取 |
| Generated product/status/workbench | `contracts/generated_surface_handoff.json` | OPL 持有生成/投影；MAG 不保留第二实现 |
| Package lifecycle | `contracts/opl_agent_package_manifest.json` + OPL package receipts | MAG 声明 package；install/update/rollback/currentness 归 OPL Packages |
| Live progress and acceptance | `contracts/live_stage_run_progress_evidence.json`, `contracts/production_acceptance/mag-production-acceptance.json`, MAG owner receipts | 只接受真实 runtime/owner evidence，不从结构状态推断 ready |

## Stable Boundary

- MAG 保留 grant truth、fundability/quality/export verdict、package body authority、strategy memory decision、owner receipt signer、typed blocker 与 grant-native validation。
- OPL 保留通用 runtime、Attempt/session lifecycle、executor transport、workspace/source transport、generated surfaces 与 package lifecycle。
- retained source 必须有 active caller、明确 authority、允许/禁止写入和可执行验证；否则按 machine policy 进入 retirement review。
- retired surface 只从 [retired-surface provenance](../history/docs-portfolio-coverage-ledger/retired-surface-provenance.md) 或 Git history 追溯，不恢复 compatibility entry。

## How To Audit

1. Fresh 读取 current-program 和上述 machine owners。
2. 运行 MAG `./scripts/verify.sh`；需要完整 source closure 时运行 OPL `agents source-closure|conformance --json`。
3. 只把新发现的 active-caller conflict、owner mismatch、forbidden effect 或 no-resurrection failure 写入当前 active plan。
4. 固定 commit、digest、path count、graph count、测试计数和一次性 closeout 进入 history/evidence，不写回本文件。

## Evidence Boundary

本文件只能解释去哪里读取 private-surface truth。它不能授权物理删除，不能证明结构 currentness，不能签 MAG owner receipt，也不能声明 grant、quality、export、submission 或 production readiness。
