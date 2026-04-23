# Contracts

- `contracts/runtime-program/current-program.json`：当前 repo-tracked 的 Med Auto Grant 主线合同。
- 当前 machine-readable 稳定能力面固定为：`CLI` / `MedAutoGrantDomainEntry`（agent entry），以及 `product entry/frontdesk/direct-entry/user-loop`、本地脚本与 schema-backed contract 这一组 lightweight direct entry / projection / callable surface。
- 当前 `product build-entry` / `product manifest` / `product frontdesk` / `executor routing` / `pending handoff` / `workspace progress` / `workspace cockpit` / `product direct-entry` / `product user-loop` / `package submission-ready` 也已经作为 schema-backed contract 固定在 `schemas/v1/`，并由 `schema-index.json` 统一索引；其中 `product-entry-manifest.schema.json`、`product-frontdesk.schema.json`、`grant-progress.schema.json`、`grant-cockpit.schema.json`、`grant-direct-entry.schema.json`、`grant-user-loop.schema.json` 与 `submission-ready-package.schema.json` 会把 direct frontdoor / direct-product projection / composition / user loop / local submission-ready delivery 收口成 generation-time fail-closed contract。
- 机器本地 session、log、report、prompt 与其他运行态不再落在仓库根目录，统一下沉到 `$CODEX_HOME/projects/med-autogrant/runtime-state/`。
- 本地 `runtime run / runtime resume` journal 默认写到 `$CODEX_HOME/projects/med-autogrant/runtime-state/sessions/`。
- `package hosted-contract-bundle` 会把当前 `current-program` pointer、runtime-state durable surface 与 canonical operator surface 一起导出到 hosted-friendly contract bundle，并额外显式携带 `domain_entry_contract`、`schema_contract`、`authoring_contract`。
- `package submission-ready` 会把当前本地导出链进一步收口成 submission-ready delivery surface；它只在 frozen gate、必备章节、预实验、代表作和在研项目都满足时写出 `submission_ready_package`，不会宣称已执行外部官网提交。
- 共享 `domain_entry_contract` 当前还会固定 `supported_commands` 与 `command_contracts`，供 external caller 直接消费。
- `schemas/v1/hosted-contract-bundle.schema.json` 现在定义整份 hosted contract bundle 的 fail-closed 结构。
- `contracts/runtime-program/current-program.json` 现在还额外固定了 `ideal_target` 与 `phase_map`，用于说明 `Med Auto Grant` 独立 domain agent、显式 hosted runtime carrier（如 `Hermes-Agent`）的技术位置，以及 `OPL` family-level 协作边界与当前阶段。
