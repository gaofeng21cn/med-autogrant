# Med Auto Grant

本仓是基金写作 domain agent；`contracts/opl_agent_package_manifest.json` 定义 `agent_id/package_id=mag`，领域和能力边界以 `contracts/` 为准。

- MAG 持有 grant strategy、quality/fundability verdict、submission package、artifact、memory 和 owner receipt authority；Framework 只提供通用 runtime、transport 与 projection。
- `mas-scholar-skills` 是 MAG 的 required dependency；缺失或不可调用必须阻断 MAG，但不得 fail-open 或阻断无关 Package。
- `agent/primary_skill/SKILL.md` 是主路由；Package carrier 或 executor 不取得 MAG identity、installed truth 或领域 authority。
- 当前实现冲突和迁移目标留在 `README.md` 与 active plans；根规则不覆盖机器合同，也不把目标态声称为已实现。
- 默认验证运行 `scripts/verify.sh`；按影响选择 smoke、regression、structure 或 full lane。

<!-- CODEGRAPH_START -->
## CodeGraph

- 本仓库使用本地 `.codegraph/` 索引；该目录不得纳入 Git。
- 定义、调用、影响范围和代码路径等结构检索优先使用 CodeGraph；字面文本检索使用 `rg`。
- 索引缺失或过期时运行 `codegraph init .` 或 `codegraph sync .`。
<!-- CODEGRAPH_END -->
