# 决策记录

## 2026-04-26：MAG 对齐 OPL Runtime Manager 薄管理层

- 决策：MAG 与 OPL 的长期托管对齐采用 `OPL Product Entry -> OPL Runtime Manager -> external Hermes-Agent runtime substrate -> Med Auto Grant Product Entry / MedAutoGrantDomainEntry`。MAG 只提供 domain entry contract、runtime_control、runtime_continuity、workspace projection、artifact locator 与 explicit wakeup/TODO queue；`OPL Runtime Manager` 只负责 OPL 侧 profile/provisioning、registration hydration、status index、doctor/repair/resume 与 native helper catalog。
- 理由：MAG 的核心价值在 author-side grant truth、route/export contract、quality gate 和 submission-ready export gate。把长期在线管理先放在 OPL Runtime Manager 这一薄层，可以利用 Hermes 常驻服务并为未来自有 sidecar 预留 promotion 边界，同时不制造第二套 grant truth。
- 影响：`current-program.json` 增加 runtime manager boundary；后续 docs/contracts 若提到 OPL 长期托管，必须明确 Runtime Manager 不是 MAG 的 scheduler kernel、session store、memory store、grant truth owner、authoring executor 或 private Hermes fork。

## 2026-04-24：公开主语收口为单一 app skill 与内部 command contract

- 决策：公开文案与技术索引的第一主语收口为单一 `Med Auto Grant` app skill；`CLI` / `MedAutoGrantDomainEntry` 保持底层 agent entry，而 `product entry/frontdesk/direct-entry/user-loop` 统一降级为这个 app skill 下的内部 command contract / direct-product projection。
- 理由：此前的公开叙事把 frontdesk、user-loop、runtime_control 和 hosted bundle 写得过于靠前，容易让读者把内部投影面误判成产品第一入口，也会削弱单一 app skill 的对外定位。
- 影响：README、docs 索引、项目/状态/架构/合同说明与 app skill 文档需要同步保持这一层级；`hosted-contract-bundle` 与 `runtime_control` 仅保留 integration/reference 角色，不再暗示 OPL 或 hosted caller 是默认主入口。

## 2026-04-23：默认公开能力面收口为稳定 capability surface

- 决策：当前对外默认合同优先冻结为 `CLI`、`MedAutoGrantDomainEntry`、本地脚本、product-entry/projection commands 与 schema-backed contract；默认正文执行继续继承本机 `Codex` 配置。
- 理由：如果继续把 hosted runtime carrier 写成默认公开主语，就会把真正稳定、可调用、可被 `Codex` / `OPL` skill activation 复用的能力面淹没掉。
- 影响：`Hermes-Agent` 相关 lane 继续保留为显式 hosted/proof backend 或技术参考；默认公开口径回到稳定 capability surface，避免把 backend 位置误写成产品第一身份。

## 2026-04-23：完成语义收口到 authoring quality 主线（P4.G）

- 决策：当前 tranche 收口为 `P4.G authoring-quality-first completion semantics alignment`，主任务完成语义以正文科学性与 authoring quality 为主。
- 理由：如果把 `submission-ready` 本地导出能力写成主任务唯一完成条件，容易把“交付包可导出”误写成“正文科学论证已闭环”。
- 影响：`package submission-ready` 继续保留为更严格的本地提交包导出面，但不作为 authoring 主任务唯一完成判据；`current-program`、`mainline-status`、`status` 与 current-truth spec 统一对齐此口径。

## 2026-04-23：形式审查/客观补件采用 TODO + 显式唤醒链路

- 决策：形式审查项与客观补件项默认进入 `TODO` 与显式唤醒链路，不默认阻塞正文 authoring。
- 理由：多数形式补件属于可排程闭环事项，默认 hard-block 会打断正文主线推进并降低主任务收敛效率。
- 影响：只有当缺口直接破坏科学论证成立性时，才升级为正文 authoring blocker；其余场景保持可追踪待办与显式恢复点。

## 2026-04-23：锁定 funder 任务线禁止 opportunistic 跨 funder 切换叙事

- 决策：已锁定 funder/family 的任务线保持同一 funder 语义闭环推进，不写成 opportunistic 跨 funder 切换。
- 理由：跨 funder opportunistic 切换会破坏已锁定材料、评审语境与质量治理闭环的一致性。
- 影响：current-truth 文案与 projection 输出默认保持 locked-funder continuity；跨 funder 变更必须作为显式重规划事件处理。

## 2026-04-21：公开主语收口为独立 medical grant domain agent

- 决策：公开文案与 machine-readable 描述统一收口为 `Med Auto Grant` 是独立 medical grant domain agent，可被 `Codex` / `OPL` / 其他通用 agent 直接调用；`OPL` 只保留 family-level session/runtime/projection 与 shared modules/contracts/indexes。
- 理由：此前公开叙述里仍混入了“位于 OPL 内部 workspace”或把 `gateway / harness` 作为第一身份的表达，容易让 caller 误判 MAG 的独立边界与 direct-entry 能力。
- 影响：`CLI` / `MedAutoGrantDomainEntry` 继续固定为 agent entry；`product entry/frontdesk/direct-entry/user-loop` 继续固定为 lightweight direct entry / projection；`gateway / harness` 继续保留为内部架构层级术语，避免对外身份漂移。

## 2026-04-17：冻结托管运行时三层 owner contract

- 决策：把当前主线统一明确成三层 owner：`Hermes-Agent` 只持有长期运行与托管能力，`Med Auto Grant` 只持有 grant-domain governance / progress / review / package gate truth，而 route-selected executor 只持有具体 authoring execution。
- 理由：如果只写成“上游 Hermes substrate + repo-side domain logic”，仍然容易把 domain supervision 和具体 executor 混成一层，后续跨仓对齐时也会反复漂移。
- 影响：文档、spec 与入口 wording 都必须显式区分 runtime owner、domain owner 与 executor owner；这轮只冻结 contract / 文档 / 入口同构，不宣称跨仓共享代码模块已抽离完成。

## 2026-04-13：把本地 submission-ready 交付导出收口成正式 command surface

- 决策：新增 `build-submission-ready-package`，把 `artifact_bundle -> final_package -> hosted_contract_bundle` 这条导出链再向前收口成一个正式的本地交付命令，并新增 `submission-ready-package.schema.json` 作为独立的 repo-tracked contract。
- 理由：从用户视角看，“能不能把当前冻结且材料齐备的国自然标书一次性导出成可交付目录”已经不该再靠人工拼三四个命令；同时这一步又必须 fail-closed，不能对缺章节、缺证据或有 gaps 的 frozen workspace 勉强导出。
- 影响：`build-submission-ready-package` 现在已经进入 CLI / domain entry / hosted bundle / product frontdoor command catalog；`current-program`、`mainline-status`、核心骨架、README、`contracts/README` 与测试都要同步进入 `P4.F` 口径，并明确“本地 package 导出”不等于“外部官网提交已完成”。

## 2026-04-13：把 `product-entry-manifest` 与 `product-frontdesk` 升级为独立 schema-backed contract

- 决策：把 `product-entry-manifest` 与 `product-frontdesk` 从“复用 product-entry shell 的 controller surface”进一步收口成独立 schema-backed、generation-time fail-closed 的 direct frontdoor contract，并把它们显式登记进 `schema-index.json`。
- 理由：当前 direct grant frontdoor 已经不只是几段人话描述，而是 future caller / `OPL` 需要直接消费的 machine-readable frontdoor contract；如果没有独立 schema，manifest/frontdesk 的 shape、companion 字段与 quickstart 结构仍可能在不知不觉中漂移。
- 影响：`product_entry.py` 现在会在生成 `product-entry-manifest` / `product-frontdesk` 后直接做 fail-closed schema 校验；`schemas/v1/product-entry-manifest.schema.json` 与 `schemas/v1/product-frontdesk.schema.json` 成为新的 repo-tracked truth surface；`current-program`、`mainline-status`、核心骨架、README 与测试都要同步进入 `P4.E` 口径。

## 2026-04-13：`family_orchestration` 的 route status 统一回到共享 author-side route truth

- 决策：`grant-progress`、`product-entry-manifest` 与 `product-frontdesk` 上的 `family_orchestration` companion，不再使用本地过期的 landed-route 集合判断 human gate 状态，而是统一读取共享 author-side route contract。
- 理由：`direction_screening -> frozen` 已经在 `P4.D` 收口为 landed route catalog；如果 frontdoor companion 还继续看旧集合，就会把诸如 `question_refinement` 这类已 landed route 错标成 `pending/requested`，制造第二真相。
- 影响：当前 frontdoor / projection / user loop 看到的是同一份 route status；后续继续向 family action graph / human gate / manifest v2 深压时，必须保持这种“共享 route truth 单源读取”的做法。

## 2026-04-13：full authoring executor 升级为全链 landed route catalog

- 决策：把 `direction_screening / question_refinement / argument_building / fit_alignment / outline / drafting / frozen` 从历史上的 `pending / handoff-required` 一次性提升为 landed 的 service-safe command surface，并与 `critique / revision / artifact_bundle / final_package / hosted_contract_bundle` 收敛成完整 author-side route catalog。
- 理由：人工整理的国自然写作流程已经能稳定映射到现有 stage 梯子，而实现层、CLI、domain entry、product loop 与 hosted bundle 也都已经具备同一套 route truth；继续把前半程写成 pending，只会制造第二真相。
- 影响：`current-program`、`mainline-status`、`status/project/architecture/current-truth specs`、`grant-user-loop`、`domain_entry_contract`、hosted bundle route catalog 与 tests 全部改写为 full landed truth；`pending-handoff-requirements.schema.json` 退为历史兼容与追溯材料，并退出 schema index 与当前 contract surface。

## 2026-04-13：critique route 升级为 Codex CLI landed route

- 决策：把 `critique` route 从历史上的 `pending / handoff-required` 正式提升为已 landed 的 `execute-critique-pass` route。
- 理由：实现层 (`hermes_runtime.py` / `critique_executor.py` / `codex_cli.py`) 与现有 route tests 已经稳定落在 landed 口径；继续把它写成 pending 会制造第二真相。
- 影响：`current-program`、status/architecture/current-truth specs、hosted bundle route catalog 与 meta tests 全部改写为 `critique = landed`；而在同日的 full authoring landing 之后，当前 landed author-side route 已进一步扩展成 `direction_screening / question_refinement / argument_building / fit_alignment / outline / drafting / critique / revision / frozen / artifact_bundle / final_package / hosted_contract_bundle`。

## 2026-04-13：critique 的默认 concrete executor 继承本机 Codex 默认

- 决策：`execute-critique-pass` 的默认模型与默认 reasoning effort 统一收口到 `inherit_local_codex_default`，不在 repo 内固定 `gpt-5.4 / xhigh`。
- 理由：当前真实入口是 `read_codex_cli_contract()` + `run_codex_exec(...)`；未显式配置环境变量覆盖时，本就应该跟随本机 Codex 默认配置，避免四仓未来一起追着改 model pin。
- 影响：文档、current-program 与 current-truth 必须显式写出 `default_model / default_reasoning_effort = inherit_local_codex_default`；只有设置 `MED_AUTOGRANT_CODEX_MODEL` / `MED_AUTOGRANT_CODEX_REASONING_EFFORT` 时才会覆盖。

## 2026-04-13：Hermes-native 只指完整 agent loop

- 决策：文档层统一声明，只有带 session substrate、route orchestration、domain mutation 与 durable state transition 的 full agent loop 才算 `Hermes-native`。
- 理由：如果把 chat relay / 单次 chat completion 也写成 `Hermes-native`，就会把 substrate owner 与单步 executor 混写，误导后续跨仓收敛。
- 影响：当前 `critique` landed 只能写成 `Codex CLI` landed route，默认模式是 `autonomous`，不能写成 `Hermes-native landed`；后续若切到 Hermes executor，必须额外拿 full-loop truth 与 proof。

## 2026-04-13：先在 critique route 落一条 Hermes-native experimental proof lane

- 决策：不新增第二条 critique command，也不改默认执行器；而是在现有 `execute-critique-pass` 上增加显式 `executor_kind=hermes_native_proof` 的 experimental proof lane。
- 理由：这样既能保持 service-safe command surface、route catalog 与 hosted contract 不漂移，也能在同一条 route 上真实验证 `Hermes-native` 是否具备 full agent loop 能力，而不是继续停留在纯文档讨论。
- 影响：当前 `execute-critique-pass` 默认仍是 `Codex CLI`，默认模式是 `autonomous`；只有显式 opt-in 时才会走 `run_agent.AIAgent.run_conversation(...)`，并且必须以“读取本机 Hermes config + 真实工具事件 + 完整 loop + 合法 JSON”四重 fail-closed 门槛来证明自己。

## 2026-04-13：Hermes-native proof 必须显式读取本机 Hermes 默认配置

- 决策：`Hermes-native` proof lane 不在 repo 内硬编码 `gpt-5.4 / xhigh`，而是显式读取 `~/.hermes/config.yaml` 里的 `model.default / provider / base_url / api_mode / agent.reasoning_effort`；只有设置 `MED_AUTOGRANT_HERMES_*` 环境变量时才覆盖。
- 理由：当前真实环境里，直接裸实例化 `AIAgent()` 并不会稳定自动补齐 `model.default`，provider 会直接报 `model is required`。如果不显式读取本机 Hermes config，这条 proof lane 根本不成立。
- 影响：repo-tracked truth 必须诚实写明“这条 lane 继承本机 Hermes 默认，而不是 repo-local pin”；同时若运行环境仍是 `custom + chat_completions`，当前只能证明 full-loop 存在，不能把 provider 侧 reasoning 语义直接写成已证明。

## 2026-04-11：统一文档骨架

- 采用核心五件套：`project/architecture/invariants/decisions/status`。
- `docs/README*` 以核心骨架为首读入口，其次是 active specs、active plans、references 与 history 索引。

## 2026-04-11：AGENTS 仅保留工作方式

- `AGENTS.md` 不再承载项目事实与阶段判断，统一回收至核心骨架与 specs。

## 2026-04-11：OMX 仅保留历史入口

- OMX 相关内容只作为历史入口保留在 `docs/history/omx/**`，不再作为活跃执行入口。

## 2026-04-11：移除 OMX-era 外部验证入口

- `omx-project-installer` 相关的外部 verifier 不再出现在 repo-tracked current truth 的验证表述中。
- 如需追溯历史来源，仅在历史说明或本文件记录，不再作为当前验证或 hard gate 入口。

## 2026-04-11：统一最小验证入口

- `scripts/verify.sh` 作为默认最小验证入口，保持分层 lane 与 `Makefile` 一致。

## 2026-04-11：冻结历史本地 runtime closeout 边界

- 在当前 repo-tracked truth 下，`R1 -> R5.A` 本地 runtime ladder 与 post-`R5.A` fail-closed hardening 已达到当前可验证上限。
- 当天 closeout 材料固定了一组历史本地 runtime closeout label 与 baseline，用于归档追溯。
- 继续推进时必须先新增并冻结 tranche truth；不得把未冻结的 hosted/runtime/submission-grade reality 写成当前已有主线。

## 2026-04-11：目标 substrate 优先于旧本地 runtime 延长线

- 一旦新的 runtime substrate 目标已经明确，新增投入默认服务目标形态，而不是继续把旧本地 runtime 深磨成长期产品终态。
- 当前本地 runtime 只保留在归档追溯材料里；任何新 tranche 都必须显式说明是在延续旧基线，还是在服务新的目标形态。

## 2026-04-11：`Hermes-Agent` 只指上游外部 runtime substrate

- 后续凡是提到 `Hermes-Agent`，只能指上游外部 runtime 项目 / 服务本体。
- 仓内 `hermes_runtime.py` 只代表 repo-local migration scaffold，不得写成“已接入 Hermes-Agent”。

## 2026-04-12：runtime substrate 与 grant executor 明确分层

- 决策：既然上游 `Hermes-Agent` 已承担 runtime substrate owner，后续不把这件事偷换成“grant authoring 的每个单步都必须立刻迁成 Hermes-native executor”。
- 理由：当前已经跑通的是长期在线 runtime substrate，不是 authoring semantics 的完全替换。若把二者混在一起，只会让已验证的 grant critique / revision / packaging 主线失去稳定边界。
- 影响：repo-side domain logic、artifact assembly、identity guard 与 executor routing 继续保留为 domain owner；未来若要替换单步执行器，必须以新的 route truth 单独推进。

## 2026-04-12：冻结 author-side executor routing contract

- 决策：`stage_action_envelope` 与 `build-product-entry` 必须共享同一份 `executor_routing_contract`，明确当前 stage、下一步 executor route，以及已 landed 的 author-side route catalog。
- 理由：如果只写“substrate 已统一”，却不把 critique / revision / export 的 route status 显式冻结下来，后续最容易把 `pending` route 误写成“已 landed executor”。
- 影响：这条 contract 仍是 route truth 的锚点；其中关于“前半程 pending、`critique = landed`”的 `2026-04-12` 快照，已经被 `2026-04-13` 的 full authoring executor landed 决策 supersede。未来继续替换任何 route，都必须先改对应 contract truth。

## 2026-04-12：为 critique pending route 冻结直接协作 handoff contract

- 决策：在保持 `critique` 继续为 `pending / handoff-required` 的前提下，为它补一份 machine-readable `handoff_requirements`，明确 future Hermes-side collaborator 必须先读取哪些 domain surfaces。
- 理由：如果 pending route 只有一个状态字段，future host 很容易绕开 grant domain truth，或者误以为需要仓内新增本地 critique helper。把 handoff 要求显式冻结出来，能让“直接协作”与“新 executor 已 landed”保持清楚分层。
- 影响：这份 pending handoff contract 现已退为历史 superseded note；`2026-04-13` 之后的 current truth 已改成 `critique -> execute-critique-pass` landed。旧 contract 只保留作历史迁移说明。

## 2026-04-12：冻结全 pending authoring route handoff matrix

- 决策：不再只为 `critique` 单独定义 pending handoff，而是把 `direction_screening / question_refinement / argument_building / fit_alignment / outline / drafting / critique / frozen` 全部冻结成 route-specific `handoff_requirements`。
- 理由：最终目标是让 `Hermes` 负责 substrate、让 `OPL` / domain 通过统一 envelope 直接协作，而不是继续脑补新的 repo-local executor。没有完整 matrix，future caller 仍会在其他未 landed route 上重新发明 handoff semantics。
- 影响：这份 pending matrix 在 `2026-04-12` 为 future caller 提供了完整 handoff 语义；但到 `2026-04-13` full authoring executor landing 后，整份 matrix 已退为历史迁移说明，当前主线不再存在 remaining pending authoring route。

## 2026-04-12：冻结 schema-backed product entry / routing contract

- 决策：把已 landed 的 `service-safe domain surface`、`executor_routing_contract` 与 `product_entry` 从“文档冻结 + 运行时 dict”进一步收口成 schema-backed contract，并在 `runtime-run` / `build-product-entry` 生成时 fail-closed。
- 理由：`OPL Gateway` 与 future domain caller 最终消费的是 machine-readable contract，而不是 repo 内部约定。如果这些 surface 只有 current truth 没有 schema，后续最容易在 pending route、route catalog、draft-bearing/nullability 边界上悄悄漂移。
- 影响：`schemas/v1/schema-index.json` 现在会显式索引当前主线正在公开承诺的 contract schema；`product_entry` 与 `stage_action_envelope.executor_routing_contract` 必须同时满足 schema 校验和冻结 truth 比对；后续任何 contract 变更都必须同步更新 schema、tests、docs 与 current-program pointer。

## 2026-04-12：冻结 hosted contract bundle entry and route catalog

- 决策：`build-hosted-contract-bundle` 不再只导出 `runtime_substrate_contract`、`runtime_state_contract` 与 `operator_contract`，还要显式导出 `domain_entry_contract`、`schema_contract`、`authoring_contract`，并受 `hosted-contract-bundle.schema.json` 的 fail-closed 约束。
- 理由：future hosted caller / `OPL` caller 真正要消费的不只是 runtime/state/operator pointer，还需要稳定的 service-safe entry、schema registry 与 author-side route catalog；如果这些合同不随 bundle 一起冻结，后续就会在 bundle 外重新发明 handoff semantics。
- 影响：hosted bundle 现在只打包已经冻结好的 domain entry / schema / route truth，不新增 repo-local executor，也不把 hosted runtime、`OPL Gateway` 或 pending route 写成已落地。

## 2026-04-12：冻结 OPL 对齐的理想目标与阶段图

- 决策：把 `Med Auto Grant` 的长线理想目标固定为 `OPL` 顶层入口、`Hermes-Agent` substrate owner、`Med Auto Grant` domain truth owner 的分层结构，并把主线阶段固定成 `P1 completed / P2 completed / P3 completed / P4 next`。
- 理由：如果不把 “理想目标” 和 “当前完成态” 分开冻结，后续最容易一边拿 `OPL` 理想型讲话，一边把未完成的 hosted caller / direct product entry 写成 landed。
- 影响：`current-program` 现在额外携带 `ideal_target` 与 `phase_map`；当前 `P3 hosted caller / OPL consumption proof` 已通过冻结合同与 proof test 落地，后续推进默认转向 `P4 mature direct grant product entry`，而不是回头重写 repo-local helper 或跳到 product overclaim。

## 2026-04-12：冻结 hosted caller contract consumption proof

- 决策：external caller / future `OPL` caller 必须直接消费仓库已经冻结好的 `domain_entry_contract`、`schema_contract`、`authoring_contract`，并且只通过 `supported_commands` 与 `command_contracts` 构造 request；不新增 repo-local hosted helper。
- 理由：如果 external caller 还要回头读仓内 helper 或手写参数拼装逻辑，那么 `P3` 其实并没有完成，合同也还不算真正 machine-readable。
- 影响：`product_entry.return_surface_contract.domain_entry_contract` 与 hosted bundle 的 `domain_entry_contract` 现在共享同一份 command catalog；`P3` 可以诚实标成 completed，而 `P4` 成为下一个 honest phase。

## 2026-04-12：`P4.A` 只落 controller-owned / read-only direct product projection

- 决策：`grant-progress` 与 `grant-cockpit` 当前只作为 controller-owned、read-only 的 direct grant product projection 落地，不进入 `domain_entry_contract.supported_commands`，也不被写成新的 service-safe executor surface。
- 理由：`P4` 的第一棒需要先给 direct user / operator / future caller 一个稳定的人话 projection，但如果把这两条 surface 混进 domain entry command catalog，就会再次把 product projection、domain execution 与 hosted caller contract 语义搅在一起。
- 影响：当前 direct-product projection 只允许读取 `summarize-workspace`、`stage-route-report`、`critique-summary` 与 `build-product-entry` 的既有合同信息；它们不改写 route owner，不新增 repo-local hosted helper，也不等于成熟前台 / hosted runtime。

## 2026-04-12：冻结 `P4.A` direct product projection contract

- 决策：`grant-progress` 与 `grant-cockpit` 不只停留在 CLI projection，而是进一步通过 `grant-progress.schema.json` 与 `grant-cockpit.schema.json` 冻结成 schema-backed、generation-time fail-closed 的 projection contract。
- 理由：如果 `P4.A` 只有命令和 current truth，没有独立 schema，那么 direct product projection 的 shape、blocker 语义、command catalog 展示面和 nullability 边界都可能悄悄漂移；而这两条 surface 又必须和 service-safe domain command catalog 保持严格分层。
- 影响：`read_grant_progress(...)` 与 `read_grant_cockpit(...)` 现在都会在返回前执行 schema 校验；这两条 projection 继续不进入 `domain_entry_contract.supported_commands`，也不进入 hosted contract bundle 的 command catalog。

## 2026-04-12：冻结 `P4.B` direct entry composition contract

- 决策：在 `P4.A` 的基础上新增 `grant-direct-entry`，把 `grant-progress`、`grant-cockpit` 与 direct / `opl-handoff` 两份 `product_entry` envelope 组合成一份 schema-backed、generation-time fail-closed 的 direct-entry contract。
- 理由：理想形态中的 `Med Auto Grant Product Entry` 不能永远停在“只读投影 + 单独 build shell”两个分散 surface 上；但当前又不能发明新的 executor 或 handoff semantics。最诚实的推进方式，就是把已冻结 surface 组合成一份 direct-entry contract。
- 影响：`grant-direct-entry` 继续只复用既有 route truth、grant truth 与 `product_entry` envelope，不进入 `domain_entry_contract.supported_commands`，也不进入 hosted contract bundle 的 command catalog。

## 2026-04-12：冻结 `P4.C` mainline status 与 grant user loop

- 决策：在 `P4.B` 的基础上新增 `mainline-status`、`mainline-phase` 与 `grant-user-loop`，把 repo 主线快照、当前 `grant-direct-entry` 组合面，以及 route-derived next action 收成当前 controller-owned 的 user loop。
- 理由：如果用户仍要自己翻 `current-program`、phase-map docs 和 route contract 才知道“现在在哪个阶段、下一步该执行什么”，那么 `P4` 仍停留在分散 surface；但当前又不能越界把它写成成熟 Web UI、hosted runtime 或新的 executor。
- 影响：`grant-user-loop` 现在通过 `grant-user-loop.schema.json` 受 generation-time fail-closed 校验；`mainline-status / mainline-phase / grant-user-loop` 继续只投影已冻结 truth，不进入 `domain_entry_contract.supported_commands`，也不进入 hosted contract bundle 的 command catalog。

## 2026-04-11：当前主线回到“本地 runtime 诚实 + 上游 Hermes-Agent 目标”

- 当前可执行 runtime owner 仍是 repo-local code。
- 旧 `CLI-first + host-agent runtime` 线只保留为归档参考材料。
- 当前 `hermes_runtime.py` 路径只保留为本地迁移 scaffold。
- `CLI / MCP / controller / upstream Hermes-Agent target / MedAutoGrant domain logic` 的边界必须显式保留，不得偷换 formal entry 或 authoring semantics。

## 2026-04-11：旧 Hermes 命名材料降级为历史本地迁移工件

- `validate-workspace / summarize-workspace / next-step / critique-summary / stage-route-report / runtime-run / runtime-resume` 当前仍运行在 repo-local runtime path 上。
- 旧的 Hermes 命名 program/spec 文档继续保留为历史迁移材料，但不再作为“上游 Hermes-Agent 已落地”的 current truth。

## 2026-04-11：final package / hosted contract 继续保持本地 owner，等待真实上游集成

- `execute-revision-pass`、`build-artifact-bundle`、`build-final-package`、`build-hosted-contract-bundle` 当前仍由 repo-local helper 持有输入加载、identity guard 与输出 handoff。
- `revision_executor.py`、`artifact_bundle.py`、`final_package.py` 继续保留 domain document assembly 责任，不被误写成上游 substrate 已接管。
- 如果未来这些责任要迁到上游 `Hermes-Agent`，必须以新的 repo-tracked truth 重新冻结。
