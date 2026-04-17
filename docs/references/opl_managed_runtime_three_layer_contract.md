# OPL 托管运行时三层合同

这份参考文档冻结 `OPL` 家族仓在托管运行时上的统一 owner 口径。

目标不是这轮就完成跨仓共享代码抽取，而是先把跨仓不能再漂移的 contract 写死。

## 一句话形状

统一按三层理解：

- `Hermes-Agent`
  - 长期运行与托管能力 owner
- domain supervision
  - 领域治理、质量门控、进度真相、恢复判断 owner
- quest executor
  - 具体干活、产生 artifact 与具体副作用

对应到 `Med Auto Grant`：

- `Hermes-Agent`
  - runtime substrate / session / run / watch / resume owner
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

- `Hermes-Agent` 只负责长期在线、调度、恢复和托管宿主
- `Med Auto Grant` 只负责 grant truth、review / package gate 与进度判断
- route-selected executor 只负责把被放行的 authoring route 跑出来

## MAG 当前落点

- 这轮已完成的是跨仓 contract / 入口 / 文档同构
- 这轮没有宣称跨仓共享代码模块已经抽离完成
- 默认 concrete executor 仍是 `Codex CLI autonomous executor`
- `hermes_native_proof` 继续只是 opt-in proof lane，不改写默认 executor owner

## 共享框架下一步

当前最适合先共享的是 contract，不是代码包。

第一批共享内容：

- 三层角色命名与 owner truth
- runtime owner / domain owner / executor owner 的 machine-readable envelope
- frontdesk / cockpit / progress 上的用户可见术语
- domain supervision 不得越过 runtime 的 fail-closed 规则

第二批再考虑代码共享：

- hosted runtime job / status manifest shape
- attention queue / recovery contract
- 如果三个仓的 controller 形状已经高度同构，再抽 `opl-runtime-contracts` 一类共享模块

## 当前不做的事

- 不在这一轮直接做跨仓 monorepo
- 不把 `Med Auto Grant` 的 domain logic 和其他仓硬揉成一个 controller
- 不把“未来共享代码模块”提前写成已完成事实
