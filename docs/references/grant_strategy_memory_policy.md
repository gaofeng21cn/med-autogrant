# Grant Strategy Memory Policy

Owner: `Med Auto Grant`
Purpose: `grant_strategy_memory_policy`
State: `reference`
Machine boundary: 本文是人读 memory policy。机器真相继续归 MAG contracts、schemas、source、workspace records、quality scorecards、closure dossiers、stage route reports、submission-ready package surfaces、`contracts/runtime-program/current-program.json`、`contracts/memory_descriptor.json` 与 `contracts/runtime-program/domain-memory-seed-fixture.json`。
Last reviewed: `2026-06-12`

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

OPL 可以索引 memory refs、携带 stage knowledge refs、展示 consumed-memory provenance、路由 writeback receipts。OPL 不持有 MAG grant strategy content、fundability judgment、authoring quality verdict 或 submission-ready export authority。

MAG 保留 memory body、accept/reject decision、writeback receipt、fundability/quality 影响判断和 owner receipt。真实 memory writeback 只在 MAG accept/reject 后写入 workspace/runtime artifact root；repo source 只保存 descriptor、schema、locator、fixture 模板和 proof surface。

Family-level governance 参考：`/Users/gaofeng/workspace/one-person-lab/docs/references/operating-governance/family-domain-memory-governance.md`。

## 非目标

- cross-funder recipe engine；
- schema 自动选择 aims；
- OPL-owned grant strategy content；
- 仅由 memory 生成 quality 或 fundability score；
- 用 memory writeback 绕过 MAG owner receipt、quality gate 或 submission-ready export gate。

当前执行计划、证据门和 next action 不在本文维护，统一回到 [MAG 理想目标态差距与完善计划](../active/mag-ideal-state-cross-repo-gap-plan.md)。
