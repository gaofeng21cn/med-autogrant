# Med Auto Grant

本仓是基金写作 domain agent；`contracts/opl_agent_package_manifest.json` 定义 `agent_id/package_id=mag`，领域和能力边界以 `contracts/` 为准。

- MAG 持有 grant strategy、quality/fundability verdict、submission package、artifact、memory 和 owner receipt authority；Framework 只提供通用 runtime、transport 与 projection。
- `contracts/opl_agent_package_manifest.json` 已按 Package identity presence/callability 把 `mas-scholar-skills` 声明为 MAG required dependency；缺失时只阻断 MAG，不阻断无关 Package。
- `agent/primary_skill/SKILL.md` 是主路由；Package carrier 或 executor 不取得 MAG identity、installed truth 或领域 authority。
- 文档职责和生命周期由 [docs/README.md](docs/README.md) 维护；当前实现归 `docs/status.md`，外部证据缺口归 `docs/active/`，根规则不覆盖机器合同。已替代文档直接删除并修复入链，历史由 Git 保存。
- 跨仓平台实现与迁移分别由 [App 文档](https://github.com/gaofeng21cn/one-person-lab-app/tree/main/docs)和 [Framework 文档](https://github.com/gaofeng21cn/one-person-lab/tree/main/docs)持有；本仓只解释 MAG owner 边界，不复制其他仓的当前状态或兼容清单。
- 默认验证运行 `scripts/verify.sh`；按影响选择 smoke、regression、structure 或 full lane。

<!-- CODEGRAPH_START -->
## CodeGraph

- 本仓库使用本地 `.codegraph/` 索引；该目录不得纳入 Git。
- 定义、调用、影响范围和代码路径等结构检索优先使用 CodeGraph；字面文本检索使用 `rg`。
- 索引缺失或过期时运行 `codegraph init .` 或 `codegraph sync .`。
<!-- CODEGRAPH_END -->
