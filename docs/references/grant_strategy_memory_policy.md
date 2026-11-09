# Grant Strategy Memory Policy

Owner: `Med Auto Grant`
Purpose: `grant_strategy_memory_policy`
State: `reference`
Machine boundary: 本文是人读 memory policy。机器真相继续归 MAG contracts、schemas、source、workspace records、quality scorecards、closure dossiers、stage route reports、submission-ready package surfaces、`contracts/runtime-program/current-program.json`、`contracts/durable_knowledge_catalog.json`。

## 结论

MAG 可以沉淀可复用的基金写作经验，例如 fundability strategy、specific aims structure、funder family grammar、reviewer-style critique patterns、template strategy 和 closure-package experience。它们应以自然语言策略 memory 为主，帮助 Codex 在对应 MAG stage 内推理，而不是在读取 workspace context 前机械决定基金策略。

正确形态：

- prose-first strategy memory cards；
- 最小 searchable metadata；
- stage-specific retrieval；
- closeout / critique rounds 产生 writeback proposal；
- 与 quality、fundability 和 export authority 严格分离。

错误形态：

- universal grant recipe engine；
- 把所有 funder strategy 塞入单个 prompt；
- 由 rigid schema 自动决定 aims、innovation 或 fundability；
- 绕过 MAG quality gates 的 scorecard replacement。

## 适合进入 Memory 的内容

适合沉淀：

- 跨 workspace 反复出现的 funder/call fit 经验；
- 让 biomedical proposal 更容易答辩的 specific aims pattern；
- 反复需要前置 evidence、feasibility、applicant fit 或 risk mitigation 的 reviewer objection；
- 在同一 funding-call task 内提升 fundability 的 route pivot；
- NSFC、NIH R21、Wellcome Discovery 或未来 admitted profile 的 family-specific strategy caveat；
- 说明哪类 evidence 通常能关闭 hard issue 的 closure-package pattern。

不适合沉淀：

- 当前申请书的 claim support；
- 属于 authoring record 的私有 workspace evidence；
- 属于 `grant-quality-scorecard` 或 `grant-quality-closure-dossier` 的 quality verdict；
- submission/export readiness assertion；
- portal checklist state 或 administrative supplement completion。

## 当前 Surface 分类

| Surface | Memory treatment |
| --- | --- |
| `fundability_strategy` stage lessons | 自然语言 memory candidate。 |
| `specific_aims_and_structure` stage lessons | 自然语言 memory candidate。 |
| `grant_family_registry.py` common grant grammar and funder-specific profile split | source 仍是 active structured profile layer；可复用的 profile reasoning 可以进入 memory。 |
| reviewer-style critique and rebuttal patterns | 自然语言 memory candidate；当前 workspace issue 留在 quality ledger。 |
| template strategy and proposal structure examples | 默认是自然语言 memory；只有成为 audited export/package template 时才进入结构化 authority。 |
| `grant-quality-scorecard`、`grant-quality-diff`、`grant-quality-closure-dossier` | schema-backed governance surface；不是 memory。 |
| OPL-hosted stage closeout receipt / typed blocker refs | runtime closeout surface；memory 只能引用 closeout 后的可复用经验。 |
| `package submission-ready` | local export authority；不是 memory authority。 |

## Stage 使用边界

Memory 应小批量、按 stage 检索：

- `call_and_candidate_intake`：call fit、topic scope、early red flags。
- `fundability_strategy`：funder-specific strategy、prior fundability failure modes。
- `specific_aims_and_structure`：aims patterns、innovation framing、claim-evidence structure lessons。
- `proposal_authoring`：prose strategy、section-structure caveats、applicant-fit handling。
- `review_and_rebuttal`：recurring reviewer objections、closure-package patterns。
- `package_and_submit_ready`：只检索不覆盖 submission-ready gates 的 export-process lessons。

检索到的 memory 可以影响 reasoning 和 drafting strategy；它不能发出 fundability、quality 或 export verdict。

## OPL 边界

OPL 可以索引 memory refs、携带 stage knowledge refs、展示 consumed-memory provenance、路由 writeback receipts。OPL 不取得 MAG grant strategy 的语义 authority、fundability judgment、authoring quality verdict 或 submission-ready export authority。

MAG 保留策略正文的领域判断、accept/reject decision、fundability/quality 影响判断和 owner receipt。通用方法属于 product，用户或团队政策属于 owner，跨申请持续复用的研究方向与基金经验属于 topic，单次申请的设计和决定属于 project。`content_kind` 另行区分 mechanism、policy、state 和 decision；当前 call 要求是带时点的 state，不再是一种与项目并列的物理记忆层。

用户已有 Obsidian 或其他 Markdown 资料库时，原正文继续由其既有目录维护，MAG 按授权绑定来源；没有个人库时，工作区普通 Markdown 直接承担正文主源。一个任务可同时使用个人库中的团队约束、研究主题经验与项目目录中的申请决策。目录路径不定义知识身份，不生成第二套可编辑个人记忆，也不强制中间全文投影。原始申请材料和不可再生的分析产物仍留业务工作区。

OPL 提供共同的来源登记、版本与权限校验、有效性过滤、冻结快照和机械写回。生产、审阅与修复消费同一份阶段快照；公开投影只含 refs。来源改变、过期或撤权后，旧摘要和旧快照不能继续作为新任务的当前事实；申请人资格、call 截止与其他行动关键约束在相关行动前重新核验。可选策略经验缺失只形成质量缺口，必需事实缺失则阻断依赖它的决定。

MAG proposal/decision 命令只产生候选和语义决定，receipt writer 记录决定。接受后，由有权维护者通过 Framework 共用写回能力应用到唯一原文，并回读来源版本和写回回执；接受记录不等于正文已持久化。跨项目或产品推广需明确目标范围与重新审阅，不自动把私人经验写入 Agent 包。用户直接编辑原文时，由共同来源机制识别差异并按已有授权复核，不要求用户手工计算哈希。

跨仓知识归属、来源与记忆规则以 [Framework SSOT](https://github.com/gaofeng21cn/one-person-lab/blob/main/docs/policies/knowledge-source-and-memory-policy.md) 为准；本页持有 MAG strategy memory 的领域分工。`target_scope` 只声明建议归属，不授予读取或写入该范围的权限；真实权限与主源位置由已授权来源登记决定。

## 非目标

- cross-funder recipe engine；
- schema 自动选择 aims；
- OPL-owned grant strategy content；
- 仅由 memory 生成 quality 或 fundability score；
- 用 memory writeback 绕过 MAG owner receipt、quality gate 或 submission-ready export gate。

当前摘要、证据门和下一轮执行入口不在本文维护，统一回到 [MAG Active Truth](../active/mag-ideal-state-cross-repo-gap-plan.md)。
