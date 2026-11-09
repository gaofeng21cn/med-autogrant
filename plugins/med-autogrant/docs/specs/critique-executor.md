# Critique Executor

Owner: `Med Auto Grant`
Purpose: `critique_executor_vocabulary_active_spec`
State: `active_current_spec`
Machine boundary: 本文冻结 critique 的 domain vocabulary 与 OPL executor-client boundary。机器接口归 source、contracts、OPL `AgentExecutionRequest` / `AgentExecutionReceipt` 和 runtime receipts。

## Current Route

`critique` 是 landed service-safe domain route：

- `route_id = critique`
- command = `execute-critique-pass`
- 默认 executor kind = `codex_cli`
- 显式非默认 lane = `hermes_agent`
- 其他 executor kind fail closed

`codex_cli` 是默认 concrete executor，但 Codex transport 不归 MAG。默认与非默认 executor 都通过 `opl_framework.executor_client.run_agent_execution_request` 进入 OPL Runway。

## Owner Boundary

OPL 持有：

- `opl executor run --request`
- Codex / Hermes 等 concrete executor discovery 与 subprocess
- timeout、process-group cleanup、JSON event/receipt envelope
- canonical `AgentExecutionReceipt`

MAG 持有：

- grant critique prompt 与 policy/persona
- `executor_kind` allow-list
- `domain_stage_closeout_packet` contract
- `mentor_critique` / `revision_plan` domain output normalization
- grant quality evidence、owner metadata 和 workspace mutation

MAG 不读取 Codex config，不声明 model/reasoning override 环境变量，不 spawn `codex exec`，也不从 stdout 或 final-message 文件恢复 domain output。

## Typed Closeout

executor 必须返回 canonical receipt，其中 `closeout_packet` 为：

```json
{
  "surface_kind": "domain_stage_closeout_packet",
  "route_id": "critique",
  "domain_output_kind": "mag_critique_output",
  "domain_output": {
    "mentor_critique": {},
    "revision_plan": {}
  }
}
```

缺少 receipt、executor kind 不一致、非零 exit code、closeout kind/route 不一致或 domain output 非 object 时，MAG fail closed；不得回退到 repo-local Codex transport。

## 审阅反馈后的同申请续跑

正式任务仍由原 OPL Task/StageRun 的 action 或 human gate 继续。维护者可通过以下现有 owner CLI 核对读取、记录和下一次 critique；`workspace.json` 为当前任务引用的同一申请，`--revision` 使用 `review-feedback` 的原样返回值：

```bash
medautogrant workspace review-feedback --input /path/to/workspace.json --json
medautogrant workspace record-review --input /path/to/workspace.json --workspace-id "<workspace_id>" --grant-run-id "<grant_run_id>" --revision "sha256:<source_digest>" --request-id "<unique_review_id>" --note '请比较两组预实验，并明确主要终点。' --json
medautogrant pass critique --input /path/to/workspace.json --output /path/to/reviewed-workspace.json --json
```

意见记录保留精确源版本和 `review_ref`。critique 将匹配版本的意见及引用送入原 OPL executor-client，随后通过原规范化、校验、输出路径产生新的 MentorCritique/RevisionPlan；输出保留原 `grant_run_id`、`workspace_id`、`draft_id`。这不是新建 Framework Task，也不自动完成 human gate 或开启 StageRun。原任务回读 `output_path` 与 `critique_execution` 后继续；正文质量和最终 export gate 仍由对应 owner 接受。

`tests/test_app_contribution.py::test_recorded_feedback_continues_same_grant_through_actual_critique_cli` 运行真实 CLI parser、domain dispatch、critique 规范化与持久输出，仅以已有合成 executor receipt 替代外部模型调用。该用例检查意见进入执行 prompt、同申请身份延续、新评审实际写盘及预提交冻结仍为 false。

## Verification

- `tests/test_critique_executor.py`
- `tests/test_ai_first_quality_boundary.py`
- `tests/test_authoring_executor.py`
- OPL standard-agent conformance / default-caller readback
- source scan 检查真实 executor 调用均经 OPL client，不能以文档中的计数替代调用链验证。

这些结构与行为验证不证明 live grant ready、quality ready、provider long-soak 或 production readiness。
