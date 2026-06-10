# 决策记录

Owner: `Med Auto Grant`
Purpose: `current_decision_log`
State: `current`
Machine boundary: 本文是人读决策记录。机器真相继续归 contracts、schemas、source、CLI/API 行为、product-entry manifest、runtime receipts 与 workspace/artifact outputs；历史决策若与当前 status/current-program 冲突，以当前 owner surfaces 为准。

## 读法

本文只保留当前仍有效、会影响后续维护判断的决策，不冻结某次运行日期、分支、worktree、receipt id、计数或 closeout 流水。consumer thinning、receipt proof、external evidence、physical cleanup、stale worktree 等过程性增量，统一回到 [MAG standard agent 文档过程归档 2026-05](./history/plans/mag-standard-agent-doc-process-history-2026-05.md) 或对应 history/provenance。当前差距和执行顺序回到 [MAG 理想目标态差距与完善计划](./active/mag-ideal-state-cross-repo-gap-plan.md)，当前机器事实回到 `contracts/runtime-program/current-program.json`、production acceptance / external evidence contracts、source、CLI/API 和 live OPL/App read-model。

## 当前有效决策

### Grant progress 必须映射到 OPL shared deliverable/platform delta

- 决策：MAG stage admission、product-entry progress 和 typed blocker projection 采用 OPL family Progress-First shared contract；grant 实质推进写入 `deliverable_progress_delta`，platform/refs/evidence 修复写入 `platform_repair_delta`，并用 `progress_delta_classification` 明确区分 `deliverable_progress`、`platform_repair`、`mixed`、`typed_blocker`、`human_gate` 或 `stop_loss`。`grant_work_progress` 与 `platform_evidence_progress` 只作为 MAG domain alias 保留。
- 理由：基金申请 agent 与 MAS/RCA/OMA 一样需要让 App/operator 直接看出下一步是否产出 grant delta，还是只在修 platform/currentness/evidence surface。shared contract 可以避免各 domain read model 自行判鲜或把 platform repair 算成交付推进。
- 影响：currentness resolver 统一读取 current-program、workspace truth、last receipt/blocker、stage refs 与 manifest refs；stage admission packet 必须声明 expected grant delta、closeout target、human gate 和 blocker budget；product-entry progress projection 与 typed blocker 必须携带实例级 `next_forced_delta`，指向 MAG owner receipt、typed blocker 或 no-regression evidence；typed blocker 必须携带 lineage、repeat budget、next forced delta 与 escalation owner。该决策不授权 OPL/App 写 grant truth、读取 grant body、生成 fundability/quality/export verdict 或绕过 submission human gate。

### Grant-facing user stage log 由 MAG closeout 提供，OPL 只做投影

- 决策：MAG 每个 grant stage 的 closeout 必须按 OPL 标准 `user_stage_log_contract` 返回用户可读 stage 语义，说明本阶段的基金问题、stage 目标、实际完成的 grant work、变更 surface、结果、剩余 blocker 和证据 refs；无法给出时返回 typed blocker。
- 理由：用户需要知道 grant 申请推进到哪一步、解决了什么问题、是否真做了工作、花了多长时间和多少 token。duration、token、cost 属于 OPL 通用观测；基金语义必须由 MAG owner 产出，不能由 OPL 从正文、artifact 或运行痕迹里猜。
- 影响：`contracts/stage_control_plane.json` 的每个 `stage_contract` 都声明 `user_stage_log_contract`。该合同不授权 OPL 写 grant truth、读取 grant artifact body、生成 fundability / quality / export verdict，provider completion 也不能宣称 stage 语义完整。

### MAG stage output 接入 OPL Stage Folder Kernel

- 决策：MAG 每个 grant stage 必须在 `stage_native_artifact_contract` 中声明 required output role、manifest requirements、owner receipt / typed blocker requirements、current pointer 规则、artifact classification boundary，以及对 OPL physical Stage Folder Kernel 的 locator/conformance 语义映射。该映射必须覆盖 `stage.json`、`attempt.json`、`manifest.json`、`receipts/receipt.json`、`current.json`、`latest.json`、canonical pointer、export artifact、lineage refs、retention policy 和 conformance summary。`artifact_bundle` 只能作为某个 MAG stage output role 的 manifest/ref projection 存在，不能作为孤立 bundle truth。`package_and_submit_ready` 额外把 stage folder lifecycle projection 固定为三类 refs：`artifact_bundle=stage_output_artifact_ref`、`final_package=canonical_promotion_ref`、`submission_ready_package=export_artifact_ref`，并要求 package lifecycle handoff 输出 OPL 可消费的 physical kernel locator / conformance refs。
- 理由：OPL generated shell 需要可恢复、可索引、可审计的 stage-native artifact refs，但 grant artifact body、package authority、fundability、quality、export 和 submission-ready verdict 仍归 MAG。把 output role、manifest ref、current pointer 与 owner receipt/typed blocker 绑定在 stage contract 上，可以避免 OPL/App 从 bundle presence、provider completion 或 schema completeness 推断 domain readiness。
- 影响：`contracts/stage_control_plane.json` 的每个 stage 都暴露 `stage_contract.stage_native_artifact_contract.physical_stage_folder_kernel`；`src/med_autogrant/artifact_bundle.py` 生成的 payload 在 `stage_output_projection` 和 `manifest` 中投影 `stage_id`、`stage_output_role`、`lifecycle_contract_role`、`artifact_classification`、`manifest_ref`、`current_pointer_ref` 与 `owner_receipt_or_typed_blocker_ref`。`product package-lifecycle-handoff` 只投影 stage folder refs、physical kernel locator refs、conformance refs、manifest/missing-output policy、receipt/blocker 和 handoff，不输出 package body。MAG 对 OPL State Index Kernel / SQLite sidecar index 的 adoption 是 `sqlite_migration_required=false` 的 refs-only consumption：OPL 持有 generic state index/read-model/SQLite sidecar，MAG 只消费 opaque refs-only index；文件与 MAG-owned artifacts 仍是 grant truth。SQLite sidecar 不得存 grant body、grant strategy memory body、fundability/quality/export/submission verdict body、package body 或 artifact body。OPL 只能消费 refs、manifest、current/canonical/export/lineage/retention/conformance refs、missing output、receipt/blocker 和 handoff；不得读取 artifact body、写 grant truth、生成 MAG owner receipt、解释 grant quality、声明 fundability-ready、quality-ready、export-ready 或 submission-ready。

### OPL/Temporal 是默认任务运行 owner，MAG 保留 grant authority

- 决策：任务启动后的默认运行 owner 是 OPL/Temporal hosted autonomous runtime；MAG 不实现 daemon、scheduler、attempt loop 或 attempt ledger；`Codex CLI` 是默认 stage executor。
- 理由：标准 OPL Agent 应提交 declarative pack、domain handler、refs、typed blocker、owner receipt 和 grant authority surface。持久在线调度、唤醒、retry、resume、attempt ledger 和 long-running provider residency 是 OPL/Temporal 职责。
- 影响：Direct app skill / CLI / `MedAutoGrantDomainEntry` 仍是一等入口；MAG 继续持有 grant truth、fundability / quality / export verdict、package authority、memory accept/reject 和 owner receipt authority。该决策不声明 Temporal long-soak window evidence 已关闭。

### MAG 目标形态是 Declarative Grant Pack + OPL generated/hosted surfaces + minimal authority functions

- 决策：MAG 以 `agent/` declarative pack、contracts、domain handler、refs-only adapter 和最小 authority function 作为长期形态；product-entry、旧 product-sidecar、grouped CLI/API、projection builder、lifecycle adapter、memory/package helper、workspace/source intake 和 status/user-loop wrapper 只能作为 direct handler、refs-only adapter、migration input、diagnostic 或 tombstone 阅读。
- 理由：通用 runtime、queue、attempt ledger、workspace/source shell、memory locator、artifact/package lifecycle、operator workbench、observability/SLO、generated wrapper 和 App/workbench shell 归 OPL Framework / shared family layer；MAG 的核心价值在 grant-specific judgment 和交付 authority。
- 影响：旧 module/interface/test/docs entry 若只服务 local runtime、Hermes/Gateway/local-manager、patch bridge、flat alias 或 compatibility aggregate test，active caller 迁出后直接退役或归档，不新增 compatibility shim、re-export facade 或 compatibility-only test。

### MAG 接入 OPL Family Foundry Agent OS target pattern

- 决策：MAG 采用 family-level `OPL Agent OS + Declarative Grant Pack + Grant Authority Kernel + Grant Capability Registry` 目标形态，target delta 维护在 [`docs/active/foundry-agent-os-target-delta.md`](./active/foundry-agent-os-target-delta.md)。
- 决策：`contracts/foundry-agent-os-domain-kernel-manifest.json` 是 W4 domain-kernel manifest 的机器合同入口，固定 MAG retained authority kernel、OPL upcollect surfaces、`current_owner_delta` 默认读根、domain signer surfaces 和 false-authority flags。
- 理由：MAS/MAG/RCA/OMA 应共享同一 Agent OS pattern，避免每个 domain 自建 runtime、generated surface、workbench、evidence ledger 或 capability registry；grant 判断和交付 authority 仍由 MAG kernel 持有。
- 影响：默认读根必须是 `current_owner_delta`；Capability Registry 只能是 Atlas/Pack/Stagecraft 的 catalog / ABI / use-policy，不是 grant authority；OPL/Vault/Console/Runway/Pack 不能签 MAG owner receipt、创建 MAG typed blocker 或授权 fundability / quality / export / submission verdict。该决策与 manifest 不声明 MAG production-ready、grant-ready、submission-ready 或 physical delete authority。

### AI-first authority surface 不由程序机械生成 ready verdict

- 决策：fundability、quality、export、submission-ready verdict 与 memory accept/reject 是 AI-first / MAG-owner judgment surface；package authority、owner receipt 和 grant helper 是 programmatic guard surface。程序只能验证、物化 refs、签 receipt、返回 typed blocker 或 safe action metadata。
- 理由：schema completeness、scorecard 分数、package existence、provider completion 或 controller route 都不能替代 grant reviewer / authoring executor / MAG owner 的判断。
- 影响：缺少 AI-authored artifact、independent review receipt、MAG owner receipt、MAG-owned typed blocker 或等价 owner-backed export artifact ref 时，fundability、quality、export 和 submission-ready verdict 都必须 fail-closed。`mag_owner_typed_blocker` 只能签出 blocked verdict，不是 readiness approval。

### External evidence ledger 是 refs-only consumption surface，不是 production completion claim

- 决策：external evidence request pack 和 `contracts/external_evidence/mag-evidence-receipt-ledger.json` 只记录外部 caller/App/workbench/owner receipt roundtrip/no-forbidden-write/direct-hosted parity/Temporal reconciliation 的 refs、receipt shapes、typed blocker 和 no-regression evidence。
- 理由：MAG 可以消费外部证据 refs，但不能在仓内伪造 OPL generated caller、Codex App workbench、production/default caller、continuous guard 或 Temporal long-soak 成功。
- 影响：first live production evidence refs 可消费不等于真实 grant workspace 扩面、App 用户路径、Temporal long soak、grant-ready、fundability-ready、quality/export-ready 或 submission-ready 完成。

### Domain memory 只由 MAG 决定 body 与 accept/reject

- 决策：OPL 可以索引 memory refs、携带 consumed refs、显示 provenance 和路由 writeback receipts；MAG 持有 grant strategy memory body、accept/reject authority、fundability/quality 影响判断和 owner receipt。
- 理由：grant strategy memory 是辅助 Codex stage reasoning 的自然语言经验，不是跨 funder recipe engine 或 quality/export verdict generator。
- 影响：真实 memory store、receipt instance 和 workspace artifact 只进入 workspace/runtime artifact root 或 `$CODEX_HOME/projects/med-autogrant/runtime-state/`；repo source 只保存 descriptor、schema、locator、fixture 模板和 proof surface。

### Submission-ready package 是本地交付 gate，不等于官网提交或正文质量完成

- 决策：`package submission-ready` 保留为严格 fail-closed 的本地 package/export surface；authoring 主任务完成语义仍以正文科学性、authoring quality 和 owner-backed export verdict 为准。
- 理由：材料完整性、导出包存在和 portal checklist 状态不能替代正文科学闭合、review/revision closure 或申请人侧质量判断。
- 影响：外部官网提交、人工 portal gate、形式补件和客观材料补齐继续独立表达；缺少 MAG owner 或 AI-backed export verdict 时，submission-ready 必须 fail-closed。

### 文档生命周期按 owner surface 分层，不保留旧 specs 兼容层

- 决策：核心五件套承载 current 人读 truth；`docs/active/` 承载当前 gap / 完善计划；`docs/specs/` 只保留 active specs、support current-truth records 和 integration references；纯历史 activation package、provider proof、local-runtime closeout、future-P5 和 superseded hosted/handoff specs 进入 `docs/history/`。
- 理由：dated spec 标题里的 `Current Truth` 容易被 direct-file reader 误读为当前完整产品状态；生命周期必须由 owner/purpose/state/machine boundary 和 specs lifecycle map 约束。
- 影响：旧 OPL Runtime Manager、上游 Hermes 作为默认 provider 的旧口径、Gateway/federation、local journal、attempt ledger、patch bridge、旧兼容别名或 legacy hosted wording 只能作为 provenance 读，不再定义当前目标、默认 runtime owner 或兼容保留理由。

## Superseded 决策入口

以下旧决策只作为历史背景，不再承担 current owner：

- 旧 OPL Runtime Manager 薄管理层口径：已被 OPL stage-led framework + Temporal default runtime owner 取代。
- 上游 Hermes 作为默认 provider 的 sidecar adapter 口径：已被 Temporal-backed OPL hosted autonomy 和显式 executor adapter/proof lane 口径取代。
- local runtime / journal / attempt ledger closeout：已归入 history/provenance；当前测试明确拒绝 `runtime-run`、`runtime-resume` 和 `probe-upstream-hermes`。
- 旧 domain runtime facade patch bridge、flat alias、compat aggregate test：active caller 迁出后直接退役，当前不保留 compatibility surface。
- step-by-step receipt/proof/lane closeout：统一从 history 归档读取，不作为当前状态页或决策页的增量 ledger。
