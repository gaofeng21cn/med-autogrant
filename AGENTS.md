# Med Auto Grant

本仓是基金写作 domain agent；`contracts/opl_agent_package_manifest.json` 定义 `agent_id/package_id=mag`，领域和能力边界以 `contracts/` 为准。

- MAG 持有 grant strategy、quality/fundability verdict、submission package、artifact、memory 和 owner receipt authority；Framework 只提供通用 runtime、transport 与 projection。
- 当前 `contracts/opl_agent_package_manifest.json` 仍把 `mas-scholar-skills` 声明为 optional/fail-open；这是当前机器事实，不得表述成 required edge 已实现。
- 目标态（尚未实现）是只按 Package identity presence/callability 把 `mas-scholar-skills` 作为 MAG required dependency；缺失时只阻断 MAG，不阻断无关 Package。
- `agent/primary_skill/SKILL.md` 是主路由；Package carrier 或 executor 不取得 MAG identity、installed truth 或领域 authority。
- 当前实现冲突和迁移目标留在 `README.md` 与 active plans；根规则不覆盖机器合同，也不把目标态声称为已实现。
- OPL Package 跨仓总体迁移唯一 SSOT 是 App 的 [`docs/active/opl-package-platform-composition-migration.md`](https://github.com/gaofeng21cn/one-person-lab-app/blob/main/docs/active/opl-package-platform-composition-migration.md)；Framework 同名文档只作 Framework compatibility inventory、repo-local migration 与 deletion appendix。
- 默认验证运行 `scripts/verify.sh`；按影响选择 smoke、regression、structure 或 full lane。

<!-- CODEGRAPH_START -->
## CodeGraph

- 本仓库使用本地 `.codegraph/` 索引；该目录不得纳入 Git。
- 定义、调用、影响范围和代码路径等结构检索优先使用 CodeGraph；字面文本检索使用 `rg`。
- 索引缺失或过期时运行 `codegraph init .` 或 `codegraph sync .`。
<!-- CODEGRAPH_END -->
