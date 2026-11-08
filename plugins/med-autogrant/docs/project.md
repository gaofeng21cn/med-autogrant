# 项目定位

Med Auto Grant（MAG）服务申请人侧的医学基金申请：围绕同一 funding call，完成材料理解、可资助性判断、specific aims、正文、独立评审、修订和本地交付包。它不承担研究执行、论文投稿或基金评审机构的决定。

用户入口是安装后的 `med-autogrant` Skill 和 OPL-generated actions。`mag` 是稳定 Agent/Package identity；仓库、distribution 和 Skill locator 为 `med-autogrant`，Python module 为 `med_autogrant`，CLI 为 `medautogrant`。入口条件见[产品入口](./product/README.md)，安装见[仓库首页](../README.zh-CN.md)。

## 业务范围

申请人提供 funding call、履历与团队条件、论文和预实验、当前草稿与交付要求。MAG 将它们组织为可追踪的 claim/evidence、strategy、aims、draft、critique、revision 和 package；每次修订沿用当前申请任务身份，改变目标基金须遵守明确的人工作业决定。

支持的 profile 由 [grant_family_registry.py](../src/med_autogrant/grant_family_registry.py) 定义，当前含 NSFC、NIH R21 和 Wellcome；真实资格、期限和格式仍须读取本次 call。评审权重是 profile 的报告字段，不是固定认知顺序或自动资助裁决算法。

正文达到可评审质量、本地包通过 export gate、外部 portal 已提交是不同结果。形式补件默认作为独立待办；直接影响科学成立性的缺口须回到正文或其证据 owner。外部提交、签字与认证保持 human-owned。

## 目标与边界

MAG 的长期形态是 `Declarative Grant Pack + OPL generated/hosted surfaces + minimal MAG authority functions`。它独立拥有领域判断、artifact/package、memory 决策与 owner receipt；Framework 提供通用运行和投影，App 提供用户界面。具体分层由[架构](./architecture.md)解释。

目标是同一申请任务在 direct authority target 与 hosted path 之间保留同一 workspace、artifact identity 和领域判断，并能用真实独立评审和交付回执证明结果。当前实现与尚未取得的运行证据见[状态](./status.md)；本页不声明 production readiness。
