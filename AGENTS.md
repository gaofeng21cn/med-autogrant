# AGENTS 工作方式规则

## 适用范围

本文件适用于仓库根目录及其所有子目录；若更深层目录存在 `AGENTS.md`，以更近者为准。

## 定位

- AGENTS 只管工作方式，不承载项目真相、规格或阶段判断。
- 项目知识默认从 `README*`、`docs/README*`、`docs/project.md`、`docs/status.md`、`docs/architecture.md`、`docs/invariants.md`、`docs/decisions.md` 读取。
- repo-tracked current-program pointer 固定为 `contracts/runtime-program/current-program.json`。
- `Med Auto Grant` 是独立 grant domain agent，也可以作为 `OPL` Codex-first、stage-led 智能体运行框架中的 admitted domain agent 被托管。`Stage` 表示大型基金写作/评审步骤，`Codex CLI` 是 stage 内默认最小执行单元；MAG 持有 grant truth、quality/fundability verdict、route owner 和 export authority。

## 工作原则

- 保持 diff 小、可审查、可回退。
- 能删就别加；能复用现有模式就别新起抽象。
- 没有明确必要不要新增依赖。
- repo-tracked 源码与测试默认都应保持文件边界清晰，优先控制在 `1000` 行以内；超过 `1500` 行应视为明确的拆分信号，而不是继续堆叠实现。
- 新增能力或继续重构时，优先采用稳定薄入口加 `parts/`、`cases/`、`modules/` 等子模块拆分；不要把新逻辑继续堆回单个超长文件。
- 若文档提到 `Hermes-Agent`，只能指上游外部 runtime 项目 / 服务；仓内自写的 runtime helper、shim、pilot 或 scaffold，不得写成“已接入 Hermes-Agent”。
- 一旦新的 runtime substrate 目标已经明确，新增投入默认服务目标形态；旧本地 runtime 只允许作为迁移桥、兼容层或回归 oracle 存在。
- 不做降级处理、兜底补丁、启发式修补或“先糊住再说”式实现。

## 文档分层与生命周期治理

- `docs/project.md`：项目定位与边界。
- `docs/architecture.md`：系统结构与核心数据流。
- `docs/invariants.md`：必须长期保持的约束与不变量。
- `docs/decisions.md`：关键决策记录与变更原因。
- `docs/status.md`：当前阶段、活跃 tranche 与近期进度。
- `README*` 与 `docs/README*`：默认公开入口与索引。
- `docs/docs_portfolio_consolidation.md` 是当前文档组合治理入口；维护者应先读核心五件套，再按该文件判断新增、更新、归档或 tombstone。
- 每份长期文档都必须能说明 `owner`、`purpose`、`state`、`machine boundary`；缺少任一信号时，先补入口或归位，再继续扩写。
- 文档治理按内容生命周期判断，文件名、日期和目录名只作为辅助信号；同一文档内的当前事实、active spec、support reference、历史 spec 和 completed plan 应分别归入当前 owner doc、spec/reference 层或 history/tombstone 语境。
- 入口文档应先呈现当前状态、层级、新旧关系和下一跳；历史 specs、旧 hosted/provider 说明、已完成 plans 与追溯材料进入 provenance 层。
- 公开文档保持中英双语；内部技术、规划、实现和历史记录默认中文。
- `docs/domain-positioning*` 与 `docs/mvp-scope*` 是当前 root allowlist 的一部分，因为它们仍承载 public subject、domain owner、MVP boundary 与 non-goals；新增 root-level docs 必须先更新 portfolio note。
- 核心骨架文档与 activation package / current truth 严格分层。
- `docs/specs/**`：repo-tracked current truth、activation package、设计冻结文档与硬门槛描述。
- `docs/references/**`：定位、背景、审计、handoff 与非活跃支持材料。
- `docs/plans/**`：仅承载尚未被核心文档、合同面或历史归档吸收的活跃计划或明确 future work；完成、替代或只剩追溯价值后进入 `docs/history/plans/**`。
- `docs/history/**`：历史归档入口（含 OMX）。
- `README*`、`docs/**` 与参考文档是人读面。代码、测试、contracts、dashboard 或 runtime 不得把 prose path、Markdown 章节或文案当成稳定机器接口；MAG 的机器真相以 `contracts/runtime-program/current-program.json`、schema/source 与 CLI/API 行为为准，确需关联人读材料时使用 `human_doc:*` 语义 ID。

## Worktree 规则

- 牵涉多文件或多步骤变更，默认从 `main` 新建独立 worktree 再实现。
- 共享根 checkout 只用于审阅、吸收、提交、push 与清理，不承担重型实现。
- 新 lane 开始前确认 worktree 干净，并清理用户级 `$CODEX_HOME/projects/med-autogrant/runtime-state/sessions/*`、tmux session 与 stale `skill-active` 状态。
- worktree 内实现和验证完成后，应尽快吸收回 `main`，并清理对应 worktree、分支与临时状态。

## 验证规则

- 默认最小验证入口是 `scripts/verify.sh`。
- `scripts/verify.sh` 默认执行 `make test-fast`；`scripts/verify.sh full` 执行 `make test-full`。
- `make test-fast` 是默认开发验证，并默认排除 `meta` 套件。
- `make test-meta` 仅用于 repo-tracked program control 与 repo hygiene 检查。
- `make test-cli-smoke` 是 CLI/local-runtime smoke lane，`make test-full` 是 clean-clone baseline。
- 更新验证命令、控制面或测试入口时，必须同步更新 `Makefile`、`pyproject.toml`、`README*`、`docs/README*`、`scripts/verify.sh` 与相关 tests。
- 叙述性 `README*`、`docs/**` 和参考文档不作为脚本/测试的断言对象；可以测试 machine-readable contract、schema、CLI/API 行为、生成产物结构与路径，但不要用测试固定文档措辞、章节或状态文案。

## 变更同步

- 涉及 `grant_run_id`、`workspace_id`、`draft_id`、`program_id` 的语义或表述变更，必须同步更新核心骨架、current truth 与相关 tests。

## 本地控制面（runtime-state）

- 项目级 `.codex/` 与 `.omx/` 已退役，不再作为仓库本地状态入口。
- 项目级 `.runtime-program/` 已退役，不再作为仓库本地状态入口。
- 机器本地 session、prompt、log、report 与 hook 状态统一迁入 `$CODEX_HOME/projects/med-autogrant/runtime-state/`。
- 用户级 runtime-state 不是产品 runtime，也不是 repo-tracked current truth。
- 任何本机 overlay 也只允许放在用户级 runtime-state 根目录，不进入 repo-tracked 主线。
