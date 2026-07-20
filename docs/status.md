# 当前状态

Owner: `Med Auto Grant`
Purpose: `current_status_and_evidence_boundary`
State: `current`
Machine boundary: 本文是人读状态摘要。机器真相归 current-program、root contracts、source、CLI/API behavior、live progress、runtime receipts 与 workspace/artifact outputs。

## 结论

MAG 已完成 private OPL platform cleanup 的结构收口：私有 standard-pack/compiler、consumer-thinning/self-audit mesh、generic autonomy scheduler、product/status/user-loop/runtime shell、旧 evidence snapshots、editable bootstrap、`mag` console alias 和无 caller receipt/lifecycle wrapper 已退役。

当前 repo-local 程序面是：

- Declarative Grant Pack
- `medautogrant` CLI / `MedAutoGrantDomainEntry`
- direct domain handler 3 actions
- 七项 minimal MAG authority functions
- schema-backed grant authoring/package behavior

OPL hosted interface 已由 `contracts/domain_descriptor.json#/standard_agent_interface` 声明：grant workspace topology、`input_path` locator、runtime domain identity、registration ref、progress alias 和 routing signal 归 MAG descriptor；私有 entry/manifest/dispatch command template 已退出 closed interface。Hosted action 统一从 closed `family-action-catalog.v2`、stage manifest 和 action-specific input schema生成，canonical 入口是 `opl agents run --domain med-autogrant --action <action_id> --workspace <absolute_path>`。该接口落地只关闭结构/功能边界，不声明任何 live grant、quality、export、submission 或 production readiness。

Repo-local CLI 现为 declarative parser metadata + explicit static dispatch：command specs 不再保存 runtime method，argparse 不注入 `handler`，执行路径不存在 `args.handler` 或 `getattr` 动态分派。资金来源抓取的 HTTPS request、redirect、timeout 与 decode 已迁入 `opl_framework.source_transport.fetch_text`；MAG 只保留 NIH/NSFC 三个官方 URL exact allowlist、User-Agent 和 funding HTML 解析语义。

Stage contract 当前保持 6 个 top-level Stage，不做拆分。Stage Pack v2 的 manifest allow-list、closed action catalog 与 pack input parity 已由 contract test 固定；3 个 public action 全部通过 `stage_binding` 声明 manifest 对齐的 `ai_selected_progress_route`，`inspect_progress` 与 `inspect_cockpit` 已归 OPL generated read model，不再进入 MAG Stage allow-list。Manifest 的 `next_stage_refs` 与 grant transition fixtures 都只是 Codex 的推荐路线和回归样例，不能拒绝 advance、skip、repeat、reverse 或 route-back 到任一 declared stage。Human decision 使用 `completed_and_wait_owner` 与 `human_gate_ref`；普通 repair/rollback、零/损坏输出和质量缺口使用 quality debt、diagnostic 或 `route_back_ref`；typed blocker 只保留给 executor unavailable、真实安全/权限/authority、identity/currentness、不可逆动作或显式 human decision。

Prompt/current caller 已按强自主 executor 收口：Stage prompt 删除重复 blocker/禁令剧本；默认 strategy-authoring 在正常 attempt 中通常用一次 Codex invocation 共同收敛 direction/question/argument/fit/outline/draft，六个 checkpoint 只做 deterministic projection、六个原子 pass 只作为定点 route-back。Observed invocation count 不是成功条件或调用上限；失败/反馈仍可经 attempt retry 或 route-back 迭代。候选数量按判断需要、outline 作为条件默认；critique 的权重仅作 profile reporting，不规定审阅顺序。专业硬依赖仍保留为 call/eligibility -> strategy basis、draft -> independent review -> revision -> risk-matched re-review，以及 MAG package authority -> fresh package proof -> human portal gate。

OPL/App 负责 generated product/status/user-loop/workbench caller。

`contracts/standard_agent_conformance_profile.json` 现由 MAG 声明六阶段 ordinary golden path、唯一默认阶段 `call_and_candidate_intake`、12 项 physical morphology 分类，以及 generated default caller / OPL Python executor client / no-forbidden-write parity gates。OPL conformance 只通用读取该 profile，不再内置 MAG stage 或 morphology 分支。

当前结构阶段已关闭，`current-program` 为 `structural_cleanup_closed`。后续 tranche 只接收 external owner/live evidence，不再恢复 MAG 私有 runtime、projection、compiler 或 self-audit 平台面。

## Machine State

| Surface | Current owner/readback | 状态 |
| --- | --- | --- |
| Current program | `contracts/runtime-program/current-program.json` | 3 handler actions、7 authority IDs |
| Agent pack | root contracts + `agent/` | declarative, OPL consumable |
| Agent Package | `pyproject.toml` + plugin manifest + `contracts/opl_agent_package_manifest.json` | repo-local version `0.3.4`；published ref、digest 与 channel receipt 仍由 OPL release authority 生成 |
| Hosted action contract | `contracts/action_catalog.json` + action input schemas | 3 stage-bound actions；progress/cockpit 归 OPL read model |
| Source closure | `contracts/source_closure_audit.json` + OPL scanner | exact classification 归审计合同；currentness 需 fresh scanner readback |
| Standard conformance profile | `contracts/standard_agent_conformance_profile.json` | MAG-owned golden path / morphology，OPL generic validator消费 |
| Foundry consumer + source behavior | OPL conformance scanner | 不冻结 pass/count snapshot；以 fresh conformance JSON 为准 |
| Owner receipt | `contracts/owner_receipt_contract.json` | 3 canonical receipt classes |
| Production acceptance | `contracts/production_acceptance/mag-production-acceptance.json` | provenance only, typed blocker open |
| Live progress | `contracts/live_stage_run_progress_evidence.json` | owner blocker recorded, no ready claim |

## 已退役

- MAG-owned pack compiler、source scanner 与 generated aggregate checker
- private product entry/status/progress/cockpit/user-loop/workbench builders
- generic scheduler/daemon/queue/attempt-ledger/session/lifecycle shells
- stale production/consumer snapshots and patch/worktree closeout ledgers
- compatibility console alias、editable dependency bootstrap、proof-only lane
- implementation-bound and snapshot-bound tests

这些内容不再作为 current source、active contract 或 active docs 入口。历史只能从 `docs/history/**` 或 git history 读取。

## Structural Readback

结构 currentness 不在本文冻结 commit、digest、测试计数或 worktree closeout。需要判断当前状态时，直接读取上面的机器合同，并运行本文件末尾的 MAG repo-native 验证与 OPL scaffold/interfaces/source-closure/conformance 命令。旧 Contract V2 snapshot、consumer ABI pin、tests-only consolidation 和 absorption 明细已折回 [历史 closeout](./history/plans/2026-07-11-mag-structural-and-tests-closeout.md)。

这些 readback 只证明对应结构门；`physical_delete_authorized`、grant/quality/export/submission/production readiness、owner acceptance 与 live evidence 仍由各自 owner surface 决定。

## 仍开放的 Evidence Gate

- 真实 OPL-hosted grant stage attempts
- submission human-gate receipt
- real quality/export receipt
- sustained App/operator/default-caller consumption
- provider long-soak evidence
- owner acceptance或 production success/no-regression evidence

因此当前不能声明 grant-ready、quality-ready、export-ready、submission-ready 或 production-ready。

## Skill 与安装

`agent/primary_skill/SKILL.md` 是 canonical source；`plugins/med-autogrant/skills/med-autogrant/SKILL.md` 是 byte-identical materialized carrier。Canonical agent id 与 OPL Agent Package id 都是 `mag`，唯一 OCI Package repository 是 `ghcr.io/gaofeng21cn/one-person-lab-packages/mag`；公共 package lifecycle 使用 `opl packages install|update|uninstall mag`。安装后的 skill locator 是 `med-autogrant`，module/CLI locator 是 `medautogrant`；这些 locator 不形成兼容 alias、第二个 package identity 或 OCI package coordinate。

## 验证入口

- `./scripts/verify.sh`
- `./scripts/verify.sh full`
- `make test-descriptor-contracts`
- OPL: `./bin/opl agents scaffold --validate <repo> --json`
- OPL: `./bin/opl agents interfaces --repo-dir <repo> --json`
- OPL: `./bin/opl agents source-closure --agent mag=<repo> --json`
- OPL: isolated `./bin/opl agents conformance --agent mag=<repo> --json`

测试通过和 structural conformance 只证明对应 gate 通过，不提升 readiness。

Package review currentness 与 local readiness 分别以 `contracts/epistemic_review_scope_profile.json` 和 `contracts/owner_receipt_contract.json` 为准；declarative policy 不能替代真实 runtime/owner evidence。
