# Med Auto Grant

本仓是 OPL 的基金写作 domain agent，canonical id 为 `mag`。

- MAG 是 `OPL Package(kind=agent)`；持有 executor-neutral package identity、capability/dependency
  声明、grant business task/typed view，以及 grant truth、fundability/quality/export verdict、
  submission package authority、strategy memory 和 owner receipts。
- OPL Framework 持有通用 runtime、attempt lifecycle、workspace/source transport、carrier
  readback/动作聚合与 generated interfaces，不持有 MAG identity、领域状态或第二份 package
  currentness。
- Package、carrier、executor 必须分离。Codex Plugin 是当前默认 carrier projection，不是
  完整 Package identity 或 installed truth；一方完整 Package bytes 由 owner 独立发布到
  自己的 GHCR `latest-stable`。
- 普通 Package 依赖只按 required/optional identity presence 与 callability 组合；版本范围、
  ABI、lock、payload、digest、原子闭包或共享 Release Set 不得成为日常 readiness 门。
- `mas-scholar-skills` 是 MAG 的 required hard dependency：缺失或不可调用时 MAG
  install/activation/readiness 必须 fail closed，但不得阻断无关 Package，也不得恢复
  provider version/ABI/lock/payload/digest 求解。
- MAG owner 定义 runtime activation、health、grant business task 与 typed view 接口；
  carrier 执行，Framework 只按 fresh readback 聚合，App 只消费。
- current-program、package identity 和 primary-skill carrier 关系以 `contracts/` 中的机器合同
  为当前实现准绳；其中旧 lifecycle/version/ABI 字段仍可能是迁移期表面，不得据此宣称
  平台组合迁移完成。当前 ScholarSkills optional/fail-open 合同与上述 required 边界冲突，
  只能作为待迁移实现读取。
- 当前事实以 contracts、源码、runtime artifacts 和验证输出为准。

默认验证入口：`scripts/verify.sh`。

<!-- CODEGRAPH_START -->
## CodeGraph

- 本仓库使用本地 `.codegraph/` 索引；该目录不得纳入 Git。
- 定义、调用、影响范围和代码路径等结构检索优先使用 CodeGraph；字面文本检索使用 `rg`。
- 索引缺失或过期时运行 `codegraph init .` 或 `codegraph sync .`。
<!-- CODEGRAPH_END -->
