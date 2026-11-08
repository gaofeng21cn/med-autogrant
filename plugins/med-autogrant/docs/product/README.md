# 用户入口

本页负责用户 action、内部 authority target 和产品投影的区别。入口事实来自 [primary Skill](../../agent/primary_skill/SKILL.md)、[action catalog](../../contracts/action_catalog.json)与 [domain descriptor](../../contracts/domain_descriptor.json)。

## 正式使用

安装后的 `med-autogrant` Skill 选择 OPL-generated action。默认使用 `open_grant_user_loop`，在同一 funding call 下开展或继续工作；已具备 accepted call、strategy 和 aims/structure 时，才用 `build_direct_entry` 进入有界 authoring。显式要求本地 package、提供 output directory 且满足 `submission_ready_export_gate` 时，使用 `build_submission_ready_package`。

三个 action 都通过 Stage manifest 绑定执行，输入字段和允许阶段由各自 closed input schema 与 catalog 定义。OPL 的 hosted command 形态为：

```text
opl agents run --domain med-autogrant --action <action_id> --workspace <absolute_path>
```

具体附加输入和 executor readiness 以当前安装的 OPL action surface 回读为准。MCP 在 MAG catalog 中仍为 `descriptor_only=true`、`public_runtime=false`，不能推断 public MCP server 已开放。

## 内部调用

`medautogrant` grouped CLI、`MedAutoGrantDomainEntry` 与 `domain-handler export|dispatch` 是 generated caller 后面的 direct authority targets，不是 Skill 要求用户手工运行的默认入口。CLI 的实际 token、参数和静态分派由 [cli_parts](../../src/med_autogrant/cli_parts/) 和 [domain entry catalog](../../src/med_autogrant/domain_entry_catalog.py)持有；维护者使用 `--help` 与现有行为测试核对，不另抄完整命令目录。

MAG 的 service-safe、executor-routing 和 product-entry schemas 仍描述 domain entry spec、command contracts、workspace locator、runtime session envelope 与 domain payload；`/product_entry_manifest/*` 是 OPL-generated output 中的 JSON pointer，不代表 MAG 保存本地 manifest builder。

## 产品投影

Mini App 使用 [Framework 统一工作入口规范](https://github.com/gaofeng21cn/one-person-lab/blob/main/docs/mcp-apps/SPEC.md)。当前注册工作区和精确任务身份随入口传递；MAG 的 canonical `workspace.json` 是阶段、当前草稿和领域评审证据的读取来源。显式选择其他 workspace 或质量文件用于导入与审阅，不能按文件更新时间猜测当前申请。存在多个候选时由用户或 Agent 明确选择。

阶段与质量视图共用同一申请上下文，保留草稿、评审、证据和质量债的 owner 原义。页面打开和刷新只读；开展或继续工作仍走本页的 OPL-generated action。共享界面、连接与凭证由 Framework、Studio 和 Connect 负责，MAG 不维护第二套调度、会话或凭据状态。

Status、progress、cockpit、direct-entry、user-loop、session 和 workbench 从 [generated surface handoff](../../contracts/generated_surface_handoff.json)、Stage/action descriptor 与 runtime refs 投影。它们展示 owner answer、freshness、next action 与 human gate，并调用 MAG target；grant body、verdict 和 owner receipt 的写入仍归 MAG。

长期工作台按 Status、Workspace、Quality、Artifacts、Memory 与 Attention 组织申请任务。这是产品组织目标，不表示本仓已实现独立 GUI，也不构成部署或持续 App 消费证据。当前缺口统一见[外部证据](../active/mag-ideal-state-cross-repo-gap-plan.md)。
