# 设计决策

本文只保留仍能约束后续设计的理由与取舍；当前组件在[架构](./architecture.md)，可执行边界在 contracts/source，历史过程在 Git。已落实的改动不按日期或编号继续追加。

## 领域包依赖平台运行能力

基金质量与通用运行有不同 owner。MAG 以声明式 Grant Pack 配合最小 authority functions，让 Framework 承担 executor transport、durable lifecycle、generated caller 和结构扫描。这使 direct target 与 hosted caller 复用同一基金判断，避免运行完成被误当作领域完成。新增 helper 必须服务真实 grant caller，不能恢复私有 queue、scanner、product builder 或 runtime platform。

## 声明与执行分开

CLI catalog 只声明 parser 字段与帮助；静态 dispatch 调用明确的 runtime/authority function。这样 command metadata 不携带隐式 callable，调用链与 effect owner 可直接审查。Transition oracle 中的 runner locator 指向 OPL owner；MAG 不复制 runner 或用固定 Stage 表替代 decisive Attempt 的语义判断。

## 独立评审与交付授权分开

同一生成上下文的自查不能证明独立 Review。Formal Review 使用新的 Attempt/session，缺陷回到最早能修复它的 Stage；repair 预算限制迭代成本，可消费 artifact 在预算耗尽后携质量债继续，不能因此获得 ready verdict。

Package review 按声明的语义依赖失效，避免 wrapper/layout 变化迫使无关科学内容重复评审；exact-byte release integrity 独立保护最终文件身份。MAG owner 消费 current scoped evidence、identity-bound Review、release integrity 和 export verdict 后才决定本地 readiness，外部 portal 仍需独立人工授权。具体约束在[不变量](./invariants.md)与[交付](./delivery/README.md)。

## 专业依赖约束结果，不冻结思考顺序

真实 call/eligibility、source/claim、独立评审和 human gate 构成专业因果依赖。方向、科学问题、论证、申请人 fit、候选数量与修订粒度由 Codex 在这些依赖内判断。Profile 权重与 schema-backed checkpoint 服务可追踪报告，不能成为认知配方或全局 invocation 上限。

## 验证观察行为与真实证据

测试守身份、权限、可观察行为、schema、资源和链接；文档语义由维护者结合源码与合同判断，不能用关键词、章节、行数或历史快照充当当前真相。Clean runner 将 cache/bytecode 留在 checkout 外；默认 fast lane 只做一次 pytest 收集。结构验证与真实 owner/production readiness 分开，开放证据由[证据页](./active/mag-ideal-state-cross-repo-gap-plan.md)维护。
