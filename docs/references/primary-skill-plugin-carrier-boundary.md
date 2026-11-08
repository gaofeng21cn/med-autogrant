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
| `plugins/med-autogrant/skills/med-autogrant/SKILL.md` | Codex plugin install carrier 的实体完整 Skill 投影。Codex plugin 安装需要真实 `SKILL.md` 文件。 | 不定义第二套 MAG 业务能力，不持有 agent membership / status 权威，不覆盖 canonical source，也不写 grant truth、fundability/export verdict、submission-ready verdict、owner receipt、typed blocker 或 runtime queue。 |

`contracts/capability_map.json` 的 `med-autogrant.primary_skill.carrier_projection_contract` 是机器可读边界：`canonical_source=agent/primary_skill/SKILL.md`，`carrier_materialization=materialized_full_skill_copy`，`codex_install_requires_real_skill_md=true`，`carrier_role=transport_install_detail_not_agent_membership_or_status`，`authority=false`。

## 为什么两者都保留

MAG 目标态是标准 OPL Agent：`Declarative Grant Pack + OPL generated/hosted surfaces + minimal authority functions`。`agent/primary_skill/SKILL.md` 属于 repo-local semantic pack，是 MAG primary skill 的 canonical source。

Codex plugin 安装和发现需要 plugin 目录下的真实 `SKILL.md`。`plugins/med-autogrant/` 同时承载该 Skill 使用的 Stage、合同、领域代码和资源，安装后以 carrier 根目录解析引用。用户通过 Framework 聚合入口触发 `opl packages install mag`、`opl packages update mag`、`opl packages uninstall mag`，物理动作与 readback 由当前配置的原生 carrier 持有；MAG 持有 Package identity、领域源与 publication。

## 源码投影

修改 canonical 源后运行 `python3 scripts/sync_carrier.py`。脚本从 Git 已跟踪的 `agent/`、`contracts/`、`schemas/`、`runtime/`、`src/med_autogrant/` 和 `docs/` 生成逐字节相同的 carrier 文件，并同步主 Skill、App adapter、包元数据和首页引用的品牌资源。新增 canonical 文件先加入 Git index，再生成投影。目录布局保持一致，使 schema loader、domain handler 与 Stage refs 可直接使用安装根目录。

`python3 scripts/sync_carrier.py --check` 校验资源存在性、字节一致性和已删除源的残留；`scripts/verify.sh structure` 包含此检查。原生 plugin metadata 与 carrier descriptor 保留各自声明语义，正式 payload allowlist 和 digest 由 Framework 的标准生成器维护。本脚本只构建本仓载荷，不执行安装、配置或发布动作。

Framework Python helpers 和 required `mas-scholar-skills` Package 继续从各自 owner 提供。工作区材料、私有凭证、缓存和运行状态不属于源码投影。

## 权威边界

- MAG grant truth、fundability / quality / export verdict、submission/package authority、grant strategy memory accept/reject、owner receipt、typed blocker、human gate 和 route-back 仍归 MAG owner chain、contracts、source、runtime receipt 与 workspace/artifact outputs。
- Plugin carrier 可以承载 full skill copy 供 Codex 安装发现，但不能成为第二业务真相、agent membership/status 权威或 runtime readiness evidence。
- 安装物化与物理 lifecycle receipt 由实际 carrier 持有，Framework 聚合 fresh readback 与委托动作；本仓的源码投影不持有 installed truth 或运行状态。
