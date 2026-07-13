# Primary Skill 与 Plugin Carrier 边界

Owner: `Med Auto Grant`
Purpose: `primary_skill_plugin_carrier_boundary_reference`
State: `active_support`
Machine boundary: 人读边界说明。机器真相继续归 `contracts/capability_map.json`、`agent/primary_skill/SKILL.md`、`plugins/med-autogrant/.codex-plugin/plugin.json` 和 `plugins/med-autogrant/skills/med-autogrant/SKILL.md`；本文不声明 grant truth、fundability ready、submission ready、domain ready 或 production ready。

本文说明 MAG rich primary skill 与 Codex plugin skill 的职责区别。两处 `SKILL.md` 同时存在是 Codex 安装 carrier 需求，不表示 MAG 有两套业务 skill 真相。

## 当前读法

| Surface | 职责 | 不承担 |
| --- | --- | --- |
| `agent/primary_skill/SKILL.md` | MAG 标准 OPL primary skill canonical source。`contracts/capability_map.json#/capabilities?surface_role=primary_skill` 以它作为 `canonical_source`。 | 不直接写 grant truth、fundability/export verdict、submission-ready verdict、owner receipt、typed blocker 或 runtime queue。 |
| `plugins/med-autogrant/skills/med-autogrant/SKILL.md` | Codex plugin install carrier 的 materialized full skill copy / compat mirror。Codex plugin 安装需要真实 `SKILL.md` 文件，所以这里保留物理文件，而不是 stub、symlink 或纯指针。 | 不定义第二套 MAG 业务能力，不持有 agent membership / status 权威，不覆盖 canonical source，也不写 grant truth、fundability/export verdict、submission-ready verdict、owner receipt、typed blocker 或 runtime queue。 |

`contracts/capability_map.json` 的 `med-autogrant.primary_skill.carrier_projection_contract` 是机器可读边界：`canonical_source=agent/primary_skill/SKILL.md`，`carrier_materialization=materialized_full_skill_copy`，`codex_install_requires_real_skill_md=true`，`carrier_role=transport_install_detail_not_agent_membership_or_status`，`authority=false`。

## 为什么两者都保留

MAG 目标态是标准 OPL Agent：`Declarative Grant Pack + OPL generated/hosted surfaces + minimal authority functions`。`agent/primary_skill/SKILL.md` 属于 repo-local semantic pack，是 MAG primary skill 的 canonical source。

Codex plugin 安装和发现需要 plugin 目录下的真实 `SKILL.md` carrier。`plugins/med-autogrant/` 因此保留 `.codex-plugin/plugin.json` 与 `skills/med-autogrant/SKILL.md`，只提供 carrier source，不改变 MAG owner surface。安装、更新和卸载统一由 OPL Packages 执行：`opl packages install mag`、`opl packages update mag`、`opl packages uninstall mag`。MAG 不提供 repo-local installer，也不修改用户 symlink 或 marketplace。

## 权威边界

- MAG grant truth、fundability / quality / export verdict、submission/package authority、grant strategy memory accept/reject、owner receipt、typed blocker、human gate 和 route-back 仍归 MAG owner chain、contracts、source、runtime receipt 与 workspace/artifact outputs。
- Plugin carrier 可以承载 full skill copy 供 Codex 安装发现，但不能成为第二业务真相、agent membership/status 权威或 runtime readiness evidence。
- 同步/物化与 lifecycle receipt 由 OPL Packages 负责；本边界不授权手写同步脚本，也不授权把 carrier 改成 stub、symlink 或纯指针。
