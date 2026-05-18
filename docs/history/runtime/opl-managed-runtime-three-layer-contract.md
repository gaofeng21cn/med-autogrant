# OPL 托管运行时三层合同

这份参考文档保留 `OPL` 家族仓在托管运行时上的三层 owner 口径。2026-05-11 之后，当前主线应先按 `OPL = stage-led、以 Agent executor 为最小执行单位的完整智能体运行框架` 理解；本文件中的 `OPL Runtime Manager` / `Hermes-Agent runtime owner` 表述只作为历史分层和 provider-specific 迁移背景，不替代核心文档。

目标不是完成跨仓共享代码抽取，而是保留当时不能漂移的 owner contract，并说明它如何被当前 OPL runtime framework 口径吸收。

## 一句话形状

历史上统一按三层理解：

- `OPL stage-led runtime framework`
  - 长期运行、托管、唤醒、队列、回执与 provider 编排 owner
- domain supervision
  - 领域治理、质量门控、进度真相、恢复判断 owner
- quest executor
  - 具体干活、产生 artifact 与具体副作用

对应到 `Med Auto Grant`：

- `OPL`
  - stage attempt lifecycle / session / queue / wakeup / handoff / receipt / retry / projection owner
- `Med Auto Grant`
  - grant-domain governance / progress / review / package gate owner
- route-selected executor
  - 具体 authoring / critique / export execution
  - 当前默认 concrete executor 仍是 `Codex CLI autonomous executor`

## 为什么这样切

如果长期托管 owner 和领域治理 owner 不分开，就会反复出现两类错误：

- 上层不知道 live run 有没有掉线
- domain repo 抢先越过 runtime，自己去做 executor 还没完成的活

三层切开后：

- `OPL` 只负责长期在线、调度、恢复、托管、投影和 provider 编排
- `Med Auto Grant` 只负责 grant truth、review / package gate 与进度判断
- route-selected executor 只负责把被放行的 authoring route 跑出来

## MAG 当前落点

- 这轮已完成的是跨仓 contract / 入口 / 文档同构
- 这轮没有宣称跨仓共享代码模块已经抽离完成
- 默认 concrete executor 仍是 `codex_cli` / `Codex CLI` executor，默认模式是 `autonomous`；在 OPL stage attempt 中它也是最小执行单元
- `hermes_agent` 继续只是 opt-in proof lane，不改写默认 executor owner

## 共享框架下一步

当前最适合先共享的是 contract，不是代码包。

第一批共享内容：

- 三层角色命名与 owner truth
- runtime owner / domain owner / executor owner 的 machine-readable envelope
- product status / user-loop / cockpit / progress 上的用户可见术语
- domain supervision 不得越过 runtime 的 fail-closed 规则

第二批再考虑代码共享：

- hosted runtime job / status manifest shape
- attention queue / recovery contract
- 如果三个仓的 controller 形状已经高度同构，再抽 `opl-runtime-contracts` 一类共享模块

## 当前不做的事

- 不在这一轮直接做跨仓 monorepo
- 不把 `Med Auto Grant` 的 domain logic 和其他仓硬揉成一个 controller
- 不把“未来共享代码模块”提前写成已完成事实
