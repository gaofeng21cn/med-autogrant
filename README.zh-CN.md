<p align="center">
  <img src="assets/branding/medautogrant-logo.png" alt="Med Auto Grant 标志" width="132" />
</p>

[English](./README.md) | [中文](./README.zh-CN.md)

# Med Auto Grant

Med Auto Grant 围绕同一 funding call，帮助申请人规划、撰写、独立评审、修订和组装医学基金申请。来源证据、科学问题、申请人适配、草稿版本、评审发现与本地交付物保存在同一申请工作区。

<p align="center">
  <img src="assets/branding/medautogrant-overview-v3.png" alt="Med Auto Grant 从想法到本地提交包的工作流" width="100%" />
</p>

## 开始申请任务

提供目标基金指南、申请人和团队材料、既有论文或预实验、当前草稿，以及希望得到的结果。例如：

> 按这个国自然指南和草稿修订研究目标与方法，独立评审科学论证，并在不改变目标基金的前提下形成可评审的申请书包。

安装后的 `med-autogrant` Skill 选择 OPL-generated action。默认 action 继续申请流程；有界正文写作须有 accepted upstream context，本地 package export 须有明确请求、输出目录和 export human gate。详细条件见[产品入口](./docs/product/README.md)。

科学上可评审、本地提交包已就绪和外部门户已提交是不同结果。形式补件作为明确待办，除非直接影响科学成立性。门户上传、签字、认证和最终提交仍须人工授权。

## 安装 Codex Carrier

本仓提供 Codex plugin carrier `med-autogrant`；OPL Agent/Package identity 为 `mag`。在克隆仓库中执行：

```bash
codex plugin marketplace add .
codex plugin marketplace list --json
codex plugin list --marketplace med-autogrant --available --json
codex plugin add med-autogrant@med-autogrant --json
codex plugin list --marketplace med-autogrant --json
```

安装后新开 Codex App 任务或 CLI session，以加载 Skill。移除本 carrier 及其 marketplace：

```bash
codex plugin remove med-autogrant@med-autogrant --json
codex plugin marketplace remove med-autogrant --json
```

这些命令只管理 Codex carrier，不能证明 Framework 可用、required ScholarSkills 可调用、完整 runtime 已安装或基金质量/生产验收已通过。使用当前 OPL Base 读取完整 Package 状态：

```bash
opl packages status mag --json
```

Runtime 或依赖证据不足时，沿返回的 owner action 处理。`packages` 命令不存在时需检查当前 OPL Base；plugin 安装成功不等于完整 Package ready。

## 项目与开发

MAG 持有基金判断、artifact/package、策略记忆决定和 owner receipt；OPL 持有通用 runtime、executor transport、generated action/status 和恢复，App 消费这些表面。实现与未闭合证据见[状态](./docs/status.md)，不能从仓库版本推导运行结论。

- [项目范围](./docs/project.md)
- [文档与验证](./docs/README.md)
- [架构](./docs/architecture.md)
- [机器合同](./contracts/README.md)

本地检查使用 `./scripts/verify.sh`；定向/full lane、clean runner 前提与文档生命周期见[文档指南](./docs/README.md#验证)。
