# Source 文档

Owner: `Med Auto Grant`
Purpose: `source_and_workspace_boundary_index`
State: `active_support`
Machine boundary: 人读索引。Workspace/source truth归 workspace artifacts、schemas、source、`contracts/workspace_lifecycle_policy.json` 与 domain handler refs。

真实 funding call、source body、grant body、memory body、artifact/package body 和 receipt instance 不进入 repo source。Repo 只保存 schema、locator、policy、descriptor、body-free refs 与 authority implementation。

OPL 可以提供 workspace/source intake shell、locator/index 和 lifecycle transport；MAG 保持 source interpretation、grant truth、verdict 与 package authority。

当前入口：

- `contracts/workspace_lifecycle_policy.json`
- `contracts/artifact_locator_contract.json`
- `contracts/domain_descriptor.json`
- `domain-handler export`

新增 source helper 必须证明是 grant-native authority或已有 caller需要；generic intake/index/lifecycle helper应上收到 OPL，不在 MAG 再建 wrapper。
