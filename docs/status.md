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
| Agent Package | `pyproject.toml` + plugin manifest + `contracts/opl_agent_package_manifest.json` | repo-local version `0.3.0`；published ref、digest 与 channel receipt 仍由 OPL release authority 生成 |
| Hosted action contract | `contracts/action_catalog.json` + action input schemas | 3 stage-bound actions；progress/cockpit 归 OPL read model |
| Source closure | `contracts/source_closure_audit.json` + OPL scanner | 9 exact audited entries；unresolved/private generic/unreachable sensitive/audit mismatch 为 0 |
| Standard conformance profile | `contracts/standard_agent_conformance_profile.json` | MAG-owned golden path / morphology，OPL generic validator消费 |
| Foundry consumer + source behavior | OPL conformance scanner | thin consumer ABI passed；matched 0；blockers 0；allowed 9 |
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

## Structural Closeout

Contract V2 fresh MAG candidate readback：

- OPL snapshot `eb4634f1f9fa74a8171c7e1cfef492420f2280c4`：scaffold `passed`、interfaces `ready`、source closure `passed`、isolated conformance `1 passed / 0 blocked`、structural/ordinary-path guard `passed`、MAG blockers `[]`。
- Source closure：4 entrypoints、384 reachable symbols、1348 call edges、17 observed effects；unresolved edges、private generic effects、unreachable sensitive residue、audit mismatch均为 `0`，digest=`sha256:d2e91403e3bb4d4c8bf82570da7d41e18ef97bc85a24a6eaf4630349213ddbc1`。
- Default callers：`8/8` retirement gates closed、blocked/worklist `0`、`keep_as_authority_adapter_observed_no_further_opl_delete_work`；projection仍明确 `physical_delete_authorized=false`。Residue decisions：`decision_item_count=0`、`residue_verification_status=verified_zero`。
- 本机历史安装 descriptor 会污染未隔离 family readback；fresh admission 使用空 `OPL_STATE_DIR` / `OPL_MODULES_ROOT`，不通过恢复已退役 command template兼容陈旧状态。最终吸收后仍须在 promoted OPL main 上重放 currentness。
- 单 Agent readback 的 Foundry Agent OS aggregate 因未输入其余四个 Agent 与 `mas-scholar-skills` 而保持 family-level blocked；MAG domain report为 `passed` 且 blockers为空。该聚合缺席只由最终五 Agent closeout关闭。

以下 readback 是 Contract V2 前的已吸收结构基线，只保留 provenance；旧 `matched 0`、`allowed 9` 不能替代上面的新 scanner 结果。

- Foundry consumer ABI基线：OPL `ddcc3242adac530b03f0a66bfe27a6a83bd835b5`、policy bundle `sha256:2abdcbe6e7c238dfc0bcbff2251fb0eda505647927446a6fbf47ae8b28253415`；`contracts/foundry_agent_series.json` 只保留 MAG identity/domain delta、canonical policy refs 和 `opl-generated:family_stage_control_plane` locator，不复制 OPL policy body。
- OPL StageRun 持有 cycle、rollback、resume、dispatch、attempt ledger 与 output orchestration；MAG 只返回 domain refs、verdict、typed blocker 与 owner receipt。
- Final source-behavior scanner：`status=passed`、`matched_source_behavior_count=0`、`blockers=[]`、`allowed_source_behavior_count=9`。
- Allowed matches只覆盖 typed executor closeout adapter、domain handler、memory accept/reject、owner receipt signer与 typed blocker projection；没有 repo-local executor transport、unclassified generic behavior或 active private generic residue。
- Framework Python helper 由 OPL 在 `opl_framework` namespace 托管；MAG manifest / lock 不声明或锁定 OPL implementation。
- MAG production base为 `3fd7cd3dc5bd3102ac8bf95b33a90a439b82e7fc`；tests-only consolidation `c755594d7a005176fab1e687de58f42a49ab0ece` 已线性吸收，严格只改 `tests/**`，净删 `1695` 行。
- Final tests boundary：`sys.path.insert` 为0，6个 retired owner tests未复活；fresh focused、smoke、fast、meta与full均为零失败，independent review `ACCEPT`。
- Tests replay与三个 superseded tests clones已完成 absorption audit并清理；无关 `stage-size-mag` lane继续保留。

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

当前 declarative pack 已声明独立上下文 Stage Review 与 `review_and_rebuttal` Grant Meta Review 合同。`package_and_submit_ready` 的 producer bytes 固定为 review-pending candidate；真实本地 readiness 同时要求 exact-byte `opl_stage_review_receipt` 与 MAG-owned export/owner verdict。该状态只表示 domain policy 已落盘；真实 Review receipt、route-back generation、owner acceptance 与 live ready 仍需 OPL runtime/owner evidence。
