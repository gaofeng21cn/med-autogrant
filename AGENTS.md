# AGENTS 工作方式规则

## 适用范围

本文件适用于仓库根目录及其所有子目录；若更深层目录存在 `AGENTS.md`，以更近者为准。

## 定位

- AGENTS 只管工作方式、少量稳定身份边界和文档生命周期纪律，不承载项目真相、规格或阶段判断。
- 用户级 `~/.codex/TASTE.md` 记录 OPL family 共享维护开发偏好；进行架构、代码、文档、测试、review、cleanup 和 closeout 判断时，先按用户级 taste 校准，再读取 MAG 事实、contracts、docs 与源码。
- 项目知识默认从 `README*`、`docs/README*`、`docs/project.md`、`docs/status.md`、`docs/architecture.md`、`docs/invariants.md`、`docs/decisions.md` 读取。
- repo-tracked current-program pointer 固定为 `contracts/runtime-program/current-program.json`。
- `Med Auto Grant` 是独立 grant domain agent，也可以作为 `OPL` stage-led 智能体运行框架中的 admitted domain agent 被托管。`Stage` 表示大型基金写作/评审步骤，Agent executor 是 stage 内最小执行单位；`Codex CLI` 是当前第一公民 executor，其他 executor adapter 只能显式接入且不承诺行为效果等价。MAG 持有 grant truth、fundability/quality/export verdict、route owner、package authority、grant strategy memory accept/reject authority 和 owner receipt；通用 runtime、queue、attempt ledger、state-machine runner、workspace/source intake shell、memory locator、package/artifact lifecycle、quality/readiness projection 与 App/workbench shell 归 OPL Framework / shared family layer。
- MAG 的理想形态是标准 OPL Agent：`Declarative Grant Pack + OPL generated/hosted surfaces + minimal authority functions`。当前仓内已存在的 product-entry、sidecar、grouped CLI/API、projection builder、lifecycle adapter、local journal、attempt ledger、workspace/source intake 或 package/memory helper 只能作为迁移输入；不能因为已有 active caller 就写成长期合理私有平台。
- `agent/primary_skill/SKILL.md` 是标准 OPL Agent 的 canonical rich primary skill；`plugins/<agent>/skills/<agent>/SKILL.md` 是 Codex plugin 安装要求的 materialized full-skill carrier mirror。该关系以 `contracts/capability_map.json` 中的 `carrier_projection_contract` 为机器权威；两者字节相同表示同步健康，不表示应删除重复，mirror 漂移才是问题。
- OPL canonical agent id 与 OPL Agent Package id 都固定为 `mag`。`med-autogrant` 仅作为 repo、Python distribution、plugin/skill 与 OCI carrier locator，`medautogrant` 仅作为 module/CLI locator；这些载体名不得形成第二个 package identity。
- 文档和开发计划先设理想态，再找差距；差距不是妥协清单。为了标准 OPL Agent 目标态，可以革命式重构 MAG 并完全抛弃旧模块、旧接口、旧测试、旧目录和旧文案，不以兼容为理由保留历史污染面。

## 工作原则

- 保持 diff 小、可审查、可回退。
- 能删就别加；能复用现有模式就别新起抽象。
- 没有明确必要不要新增依赖。
- repo-tracked 源码与测试默认都应保持文件边界清晰，优先控制在 `1000` 行以内；超过 `1500` 行应视为明确的拆分信号，而不是继续堆叠实现。
- 新增能力或继续重构时，优先采用稳定薄入口加 `parts/`、`cases/`、`modules/` 等子模块拆分；不要把新逻辑继续堆回单个超长文件。
- 若文档提到 `Hermes-Agent`，只能指上游外部 runtime 项目 / 服务；仓内自写的 runtime helper、shim、pilot 或 scaffold，不得写成“已接入 Hermes-Agent”。
- 一旦新的 runtime substrate 目标已经明确，新增投入默认服务目标形态；旧本地 runtime 只允许作为迁移桥、兼容层或回归 oracle 存在。
- 私有功能面是例外而不是默认。保留在 MAG 的程序面必须是 fundability、authoring quality/export verdict、package authority、grant strategy memory accept/reject、owner receipt signing 或 grant-native helper 这类无法声明化的最小 authority function，并写清接口、active caller、不能上收原因、receipt/blocker/ref 输出边界和退役门。
- 已被当前 owner surface 替代的模块、接口、CLI alias、wrapper、facade、patch bridge、聚合测试和文档入口，默认迁移 active caller 后直接退役；需要来龙去脉时只保留 history/tombstone/provenance，不新增 compatibility shim、re-export facade、别名或兼容测试。
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
- `docs/**` 默认只维护中文 canonical 内容；稳定路径优先使用无语言后缀 `.md`。
- 根层 `README*` 是否保留公开双语入口，由产品分发和 public 需求单独决定。
- MAG 采用 OPL-family canonical docs taxonomy：`active/public/product/runtime/delivery/source/policies/specs/references/history`。目录按长期生命周期职责保留，不按当前文件数量判断。
- `docs/public/domain-positioning.md` 与 `docs/public/mvp-scope.md` 是 docs 层公开补充入口，承载 public subject、domain owner、MVP boundary 与 non-goals；新增 root-level docs 必须先更新 portfolio note。
- 核心骨架文档、activation package、active plan 与 current truth 严格分层。
- `docs/active/`：当前执行、当前计划、当前差距、active baton 与 closeout evidence；旧 `docs/plans/` 活跃计划层已退役，新增 recurring active material 不再进入旧目录。
- `docs/public/`：public narrative index 与公开补充说明。
- `docs/product/`：app skill、product status、user-loop、direct entry 与 operator guidance。
- `docs/runtime/`：runtime/control/projection、OPL-hosted boundary、receipt/projection 支撑；机器真相仍归 contracts/source/runtime evidence。
- `docs/delivery/`：submission-ready package、export、delivery 和 manual portal boundary 支撑。
- `docs/source/`：funder/task/source intake、workspace canonical document 和 source truth consumption 支撑。
- `docs/policies/`：稳定治理规则、文档规则和 repo-local operating discipline。
- `docs/specs/`：path-stable 技术记录和 active specs；只有 `docs/specs/README.md` 与 `docs/specs/specs_lifecycle_map.md` 明确列为 active 的 specs 才是 current owner，其余 dated specs 按 support/history/provenance 阅读。
- `docs/references/`：north-star、OPL adoption、memory policy、governance checklist、定位、背景、审计、handoff 与非活跃支持材料。
- `docs/history/`：完成计划、旧 specs、旧 provider/runtime/OMX/provenance 和 tombstone；`docs/history/plans/` 承载已完成、已替代或只剩追溯价值的历史计划。
- `README*`、`docs/**` 与参考文档是人读面。代码、测试、contracts、dashboard 或 runtime 不得把 prose path、Markdown 章节或文案当成稳定机器接口；MAG 的机器真相以 `contracts/runtime-program/current-program.json`、schema/source 与 CLI/API 行为为准，确需关联人读材料时使用 `human_doc:*` 语义 ID。

## Worktree 规则

- 牵涉多文件或多步骤变更，默认从 `main` 新建独立 worktree 再实现。
- 共享根 checkout 只用于审阅、吸收、提交、push 与清理，不承担重型实现。
- 新 lane 开始前确认 worktree 干净，并清理用户级 `$CODEX_HOME/projects/med-autogrant/runtime-state/sessions/*`、tmux session 与 stale `skill-active` 状态。
- worktree 内实现和验证完成后，应尽快吸收回 `main`，并清理对应 worktree、分支与临时状态。

## 验证规则

- 默认最小验证入口是 `scripts/verify.sh`。
- `scripts/verify.sh` 默认执行 `make test-fast`；`scripts/verify.sh full` 执行 `make test-full`。
- `scripts/verify.sh` 默认只检查 repo hygiene，不自动删除本地 ignored 产物；需要清理时显式运行 `scripts/verify.sh cleanup`。
- `make test-fast` 是默认开发验证，并默认排除 `meta` 套件。
- `make test-meta` 仅用于 repo-tracked program control 与 repo hygiene 检查。
- `make test-cli-smoke` 是 CLI/local-runtime smoke lane，`make test-full` 是 clean-clone baseline。
- 更新验证命令、控制面或测试入口时，必须同步更新 `Makefile`、`pyproject.toml`、`README*`、`docs/README*`、`scripts/verify.sh` 与相关 tests。
- 叙述性 `README*`、`docs/**` 和参考文档不作为脚本/测试的断言对象；可以测试 machine-readable contract、schema、CLI/API 行为、生成产物结构与路径，但不要用测试固定文档措辞、章节或状态文案。
- 默认 Python / pytest 验证必须经由 `scripts/run-python-clean.sh` 或 `scripts/run-pytest-clean.sh`，把 bytecode、pytest cache、`uv sync` project venv 和安装/同步副产物导向仓库外部；禁止把 `.venv`、`__pycache__`、`.pytest_cache` 或 `*.egg-info` 写回开发 checkout 后再靠清理兜底。

## 变更同步

- 涉及 `grant_run_id`、`workspace_id`、`draft_id`、`program_id` 的语义或表述变更，必须同步更新核心骨架、current truth 与相关 tests。

## 本地控制面（runtime-state）

- 项目级 `.codex/` 与 `.omx/` 已退役，不再作为仓库本地状态入口。
- 项目级 `.runtime-program/` 已退役，不再作为仓库本地状态入口。
- 机器本地 session、prompt、log、report 与 hook 状态统一迁入 `$CODEX_HOME/projects/med-autogrant/runtime-state/`。
- 用户级 runtime-state 不是产品 runtime，也不是 repo-tracked current truth。
- 任何本机 overlay 也只允许放在用户级 runtime-state 根目录，不进入 repo-tracked 主线。

<!-- OPL_FLOW_MANAGED_START -->
OPL Flow managed surface: repo_agent_instructions
Plugin: opl-flow
Plugin version: 0.1.7
Profile pointer: contracts/opl-native-profile.json
本块只声明 OPL Flow 工作流 profile 指针；repo-specific 规则、项目事实、contracts、source、tests 和 runtime 输出继续归本仓既有 owner。
请只通过 OPL Flow repo_profile sync 更新本块；本块外内容由目标 repo 自己维护。
<!-- OPL_FLOW_MANAGED_END -->

<!-- CODEGRAPH_START -->
## CodeGraph

- 本仓库使用本地 `.codegraph/` 索引；该目录不得纳入 Git。
- 定义、调用、影响范围和代码路径等结构检索优先使用 CodeGraph；字面文本检索使用 `rg`。
- 索引缺失或过期时运行 `codegraph init .` 或 `codegraph sync .`。
<!-- CODEGRAPH_END -->
