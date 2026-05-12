# Contracts

- `contracts/runtime-program/current-program.json`：当前 repo-tracked 的 Med Auto Grant 主线合同。
- `current-program.json` 现在还携带 `product_layer_metadata`，把 MAG 的公开发布定位固定为 `Foundry Agent / OPL-compatible package built on OPL Framework`，并把 skill catalog、stage control plane、hosted-contract-bundle 与 submission-ready export 归并为同一发布形态。
- 当前 machine-readable 稳定能力面固定为：`CLI` / `MedAutoGrantDomainEntry`（agent entry），以及单一 Med Auto Grant app skill 之下的 `product entry/status/direct-entry/user-loop`、本地脚本与 schema-backed contract 这一组内部 command contract / direct-product projection / callable surface。
- 当前 `product build-entry` / `product manifest` / `product status` / `executor routing` / `workspace progress` / `workspace cockpit` / `product direct-entry` / `product user-loop` / `package submission-ready` 也已经作为 schema-backed contract 固定在 `schemas/v1/`，并由 `schema-index.json` 统一索引；其中 `product-entry-manifest.schema.json`、`product-status.schema.json`、`grant-progress.schema.json`、`grant-cockpit.schema.json`、`grant-direct-entry.schema.json`、`grant-user-loop.schema.json` 与 `submission-ready-package.schema.json` 会把 direct product entry surface / direct-product projection / composition / user loop / local submission-ready delivery 收口成 generation-time fail-closed contract，但它们仍是 app skill 的内部 contract，而不是对外第一主语。
- 机器本地 session、log、report、prompt 与其他运行态不再落在仓库根目录，统一下沉到 `$CODEX_HOME/projects/med-autogrant/runtime-state/`。
- 本地 `runtime run / runtime resume` journal 默认写到 `$CODEX_HOME/projects/med-autogrant/runtime-state/sessions/`。
- `package hosted-contract-bundle` 会把当前 `current-program` pointer、runtime-state durable surface 与 canonical operator surface 一起导出到 hosted-friendly contract bundle，并额外显式携带 `domain_entry_contract`、`schema_contract`、`authoring_contract`；这类 bundle 继续只作为 integration/reference surface 供 hosted caller / external caller 消费。
- `package submission-ready` 会把当前本地导出链进一步收口成 submission-ready delivery surface；它只在 frozen gate、必备章节、预实验、代表作和在研项目都满足时写出 `submission_ready_package`，不会宣称已执行外部官网提交，也不替代正文科学完成或作者最终判断。
- MAG 继续独立持有 grant truth、fundability verdict、authoring quality verdict、route owner 与 submission/export authority；OPL 持有 generic Agent Executor Adapter / registry，`Hermes-Agent` / `Claude Code` 只属于显式 provider / receipt / migration / provenance 语境。
- 共享 `domain_entry_contract` 当前还会固定 `supported_commands` 与 `command_contracts`，供 external caller 直接消费。
- `schemas/v1/hosted-contract-bundle.schema.json` 现在定义整份 hosted contract bundle 的 fail-closed 结构。
- `contracts/runtime-program/current-program.json` 现在还额外固定了 `stage_led_framework_boundary`、`executor_defaults`、`ideal_target` 与 `phase_map`，用于说明 `Med Auto Grant` 独立 domain agent、`OPL` Codex-first stage-led framework、显式 opt-in executor backend（如外部 `Hermes-Agent` / `Claude Code`）的技术位置，以及 `OPL` family-level 协作边界与当前阶段。
