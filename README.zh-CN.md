<p align="center">
  <a href="./README.md">English</a> | <a href="./README.zh-CN.md"><strong>中文</strong></a>
</p>

# Med Auto Grant

**面向申请人侧 `NSFC` 风格申请的医学基金主线**

> `Med Auto Grant` 是 `Grant Foundry` 家族中的医学基金主线。它的目标，是帮助申请人把个人基础、既有成果、预实验和候选方向收成一条可治理的 authoring / revision 流程，而不是继续在零散草稿和临时对话里反复打补丁。

<table>
  <tr>
    <td width="33%" valign="top">
      <strong>面向谁</strong><br/>
      准备申请人侧医学基金的研究者、临床团队、青年教师与 PI
    </td>
    <td width="33%" valign="top">
      <strong>能帮什么</strong><br/>
      问题提纯、申请人与方向匹配判断、结构化写作、导师式批注、修订，以及本地 submission package 整理
    </td>
    <td width="33%" valign="top">
      <strong>公开角色</strong><br/>
      当前活跃的医学 `Grant Ops` 业务仓主线，而顶层 federation admission / handoff wording 仍在 `OPL` 单独门控
    </td>
  </tr>
</table>

## 它能帮你做什么

- 把申请人材料、既有成果、在研项目、预实验和候选方向收成更清楚的 `NSFC` 风格申请主线。
- 让问题提纯、论证搭建、草稿写作、导师式批注和修订保持在同一条 author-side 路线上。
- 把修订证据和 verdict checkpoint 保留下来，而不是散落在文档版本和聊天记录里。
- 在 workspace 冻结且证据齐备后，导出本地 `submission-ready` package。

## 当前公开可走的路径

| 路径 | 状态 | 含义 |
| --- | --- | --- |
| 结构化基金 authoring 主线 | Active | 当前从问题提纯到草稿冻结的诚实主路径 |
| 导师式批注与修订证据 | Active | review、revision 和 re-review evidence 已能收在同一条作者侧主线里 |
| 本地 `submission-ready` package 导出 | Active local output | 对 frozen 且证据齐备的 workspace 已落地；但这仍不是外部官网提交流程 |
| 成熟 hosted runtime / 自动官网提交 | Not landed | 仍是后续工作 |

## 更适合什么场景

- 你在准备申请人侧医学基金，且已有可复用的申请材料。
- 你需要在正式写作前先把科学问题和方向收紧。
- 你希望批注与修订保持结构化、可审计，而不是靠口头感觉推进。
- 你希望先拿到更接近 submission readiness 的本地 package，再做人类最终审阅。

## 这个仓库应该怎么读

1. 潜在用户先读当前首页，再继续看 [文档索引](./docs/README.zh-CN.md)、[领域定位](./docs/domain-positioning.zh-CN.md) 和 [MVP 范围](./docs/mvp-scope.zh-CN.md)。
2. 技术规划、架构判断和方向同步，继续读 [项目概览](./docs/project.md)、[当前状态](./docs/status.md)、[架构](./docs/architecture.md)、[不变量](./docs/invariants.md)、[决策记录](./docs/decisions.md) 以及 [合同说明](./contracts/README.md)。
3. 开发者和维护者再进入 `docs/specs/`、`docs/references/`、`docs/plans/` 与 `docs/history/omx/`。

## 用人话解释它的边界

`Med Auto Grant` 不是整个顶层联邦，也不是外部提交官网。
它的职责，是对申请人侧的 grant truth 负责。

```text
User / Agent
  -> OPL Gateway（可选）
      -> Med Auto Grant
          -> Runtime Substrate
              -> Grant-Domain Truth
```

更直白地说：

- `OPL` 在这个仓之上，负责 family-level 的 admission 和 handoff wording。
- `Med Auto Grant` 负责基金写作 workflow、修订逻辑和申请人侧 grant truth。
- runtime substrate 不应和公开产品入口混成一层。

## 这个仓库不是什么

- 它不是“成熟 hosted 基金前台已经落地”的宣传口径。
- 它不是“会替你自动完成外部官网提交”的自动驾驶产品。
- 它不是把 `OPL`、runtime substrate 和申请人侧 grant truth 混成一层的理由。

<details>
  <summary><strong>面向技术读者的运行时真相说明</strong></summary>

当前可执行主线是 `CLI-first + real upstream Hermes-Agent runtime substrate`。
repo-tracked truth 里也继续显式保留真实上游 `Hermes-Agent` runtime substrate 这句主线表述。
遗留的 repo-local runtime helper 现在只保留为 compatibility bridge 与 regression oracle，而不是 substrate owner。
仓内 `hermes_runtime.py`、`domain_entry.py` 这一类 repo-local adapter 保留的是 domain 语义，不是 runtime substrate owner。

当前 formal-entry matrix 仍然是 `CLI`、`MCP` 和 `controller`。
仓库主线仍按 `Auto-only` 理解。

轻量结构化 `product entry` shell 已经落地。
当前已经冻结好的产品相关合同里，`product entry`、projection 与 hosted contract bundle 都按 schema-backed 收口；对应的托管友好的 handoff contract 会继续通过 `domain_entry_contract`、`schema_contract`、`authoring_contract`、`supported_commands` 与 `command_contracts` 暴露给 hosted caller / 外部 caller。
这些 repo-tracked surface 仍不等于 actual hosted runtime 已经落地，更完整的 grant-facing 产品体验仍要继续补。
当前理想目标仍是让 `OPL` 保持在 domain 之上，而申请人侧 grant truth 继续保持 machine-readable。

当前已 landed 的产品相关表面主要包括：

- 作为 service-safe domain entry contract 的 `MedAutoGrantDomainEntry`
- `product build-entry`、`product preflight`、`product start`、`product manifest`、`product frontdesk`
- `workspace progress`、`workspace cockpit`、`product direct-entry`、`product user-loop`
- 用于本地 fail-closed submission packaging 的 `package submission-ready`
- 面向 hosted caller / 外部 caller 的 `hosted contract bundle`
- 机器可读的 `domain_entry_contract`、`schema_contract`、`authoring_contract`、`supported_commands` 与 `command_contracts`

这些表面已经让 grant 主线更可发现、更机器可读，但并不等于成熟 hosted 产品前台或官网自动提交流程已经落地。
</details>

## 开发验证

- `make test-fast`
- `make test-meta`
- `make test-cli-smoke`
- `make test-full`

## 延伸阅读

- [文档索引](./docs/README.zh-CN.md)
- [领域定位](./docs/domain-positioning.zh-CN.md)
- [MVP 范围](./docs/mvp-scope.zh-CN.md)
- [项目概览](./docs/project.md)
- [当前状态](./docs/status.md)
- [架构](./docs/architecture.md)
- [不变量](./docs/invariants.md)
- [决策记录](./docs/decisions.md)
- [合同说明](./contracts/README.md)
