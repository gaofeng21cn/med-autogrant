# 当前状态

Owner: `Med Auto Grant`
Purpose: `current_status_and_evidence_boundary`
State: `current`
Machine boundary: 本文是人读状态摘要。机器真相归 current-program、root contracts、source、CLI/API behavior、live progress、runtime receipts 与 workspace/artifact outputs。

## 结论

MAG 当前以 Declarative Grant Pack 提供领域语义，由 OPL 生成和托管通用运行面；grant 判断、artifact、package、memory 与 owner receipt authority 继续归 MAG。

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

`current-program` 当前为 `structural_cleanup_closed`；后续工作是补充 external owner 与 live evidence。

## OPL Package 组合迁移状态

目标边界已经进入 owner contract：MAG 是 `OPL Package(kind=agent)`，owner 保有
executor-neutral identity、capabilities、required/optional dependency intent、grant
business task 与 typed views；完整一方 bytes 由本 owner 独立发布到本包 GHCR
`latest-stable`。Codex Plugin 只是当前默认 carrier projection，Framework 只应聚合
carrier fresh readback、presence/callability 与动作。

`contracts/opl_agent_package_manifest.json`、Scholar binding、source 和 validators
将 `mas-scholar-skills` 声明为 MAG required hard dependency。MAG admission、launch、
route 与 readiness 只检查该 identity 的 presence/callability；缺失只阻断 MAG，不影响
无关 Package。跨仓阶段与功能等价证据服从 App 的
[跨仓总体迁移 SSOT](https://github.com/gaofeng21cn/one-person-lab-app/blob/main/docs/active/opl-package-platform-composition-migration.md)。
Framework 同名文档只作 Framework compatibility inventory、repo-local migration 与
deletion appendix，不是第二份总体计划。
这项平台减法不删除 MAG 的 grant workflow、领域 verdict、submission package
exact-byte integrity、owner receipt、business task 或 typed views。

ScholarSkills required dependency 的本地合同、版本与载体投影已落地；这不等价于完整
Package publication、installed state 或 live hosted proof 已闭合，后者仍需 owner-authoritative
readback。

## Machine State

| Surface | Current owner/readback | 状态 |
| --- | --- | --- |
| Current program | `contracts/runtime-program/current-program.json` | 3 handler actions、7 authority IDs |
| Agent pack | root contracts + `agent/` | declarative, OPL consumable |
| Agent Package | `pyproject.toml` + plugin manifest + `contracts/opl_agent_package_manifest.json` | source version `0.3.12`，配置的 Codex Plugin carrier 为 `med-autogrant@med-autogrant`，ScholarSkills 为 required hard dependency；目标仍为 owner 独立 GHCR `latest-stable` 与完整 carrier fresh readback |
| Hosted action contract | `contracts/action_catalog.json` + action input schemas | 3 stage-bound actions；progress/cockpit 归 OPL read model |
| Source closure | `contracts/source_closure_audit.json` + OPL scanner | exact classification 归审计合同；currentness 需 fresh scanner readback |
| Standard conformance profile | `contracts/standard_agent_conformance_profile.json` | MAG-owned golden path / morphology，OPL generic validator消费 |
| Foundry consumer + source behavior | OPL conformance scanner | 不冻结 pass/count snapshot；以 fresh conformance JSON 为准 |
| Owner receipt | `contracts/owner_receipt_contract.json` | 3 canonical receipt classes |
| Production acceptance | `contracts/production_acceptance/mag-production-acceptance.json` | provenance only, typed blocker open |
| Live progress | `contracts/live_stage_run_progress_evidence.json` | owner blocker recorded, no ready claim |

## Structural Readback

结构 currentness 通过上面的机器合同、MAG repo-native 验证与 OPL scaffold/interfaces/source-closure/conformance 回读。完成过程和旧版本从 Git 历史读取。

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

`agent/primary_skill/SKILL.md` 是 canonical source；
`plugins/med-autogrant/skills/med-autogrant/SKILL.md` 是 byte-identical Codex carrier
projection。Canonical agent id 与 OPL Agent Package id 都是 `mag`，唯一 OCI Package
repository 是 `ghcr.io/gaofeng21cn/one-person-lab-packages/mag`；公共聚合动作使用
`opl packages install|update|uninstall mag`。安装后的 skill locator 是
`med-autogrant`，module/CLI locator 是 `medautogrant`；这些 locator 不形成兼容 alias、
第二个 package identity、完整 installed truth 或 OCI package coordinate。

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
