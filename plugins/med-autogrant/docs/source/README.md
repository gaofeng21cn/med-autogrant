# Source 文档

Owner: `Med Auto Grant`
Purpose: `source_and_workspace_boundary_index`
State: `active_support`
Machine boundary: 人读索引。Workspace/source truth归 workspace artifacts、schemas、source、`contracts/workspace_lifecycle_policy.json` 与 domain handler refs。

真实 funding call、私人 source body、grant body、用户/主题/项目 memory body、artifact/package body 和 receipt instance 不进入 repo source。Repo 保存可分发的产品知识、schema、locator、policy、descriptor、body-free refs 与 authority implementation。

个人与团队知识正文可以来自既有 Obsidian 等 Markdown 库，项目正文可以留在业务工作目录；没有个人库时，工作区共享知识和项目知识目录直接作为正文主源。来源由已有 Profile/Workspace 控制面绑定，知识身份与 scope 不依赖绝对路径。Framework 按权限和已接受版本直接冻结选中的正文，不要求工作区维护中间全文副本。项目资料、最终正文和分析成果具有自己的生命周期，不随运行缓存清理。

OPL 可以提供 workspace/source intake shell、locator/index 和 lifecycle transport；MAG 保持 source interpretation、grant truth、verdict 与 package authority。

当前入口：

- `contracts/workspace_lifecycle_policy.json`
- `contracts/artifact_locator_contract.json`
- `contracts/domain_descriptor.json`
- `domain-handler export`

新增 source helper 必须证明是 grant-native authority或已有 caller需要；generic intake/index/lifecycle helper应上收到 OPL，不在 MAG 再建 wrapper。
