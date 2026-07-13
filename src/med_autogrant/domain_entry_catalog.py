from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DomainEntryCommandSpec:
    required_fields: tuple[str, ...]
    optional_fields: tuple[str, ...] = ()
    help_text: str = ""
    exclusive_fields: tuple[str, ...] = ()


SERVICE_SAFE_DOMAIN_COMMANDS: dict[str, DomainEntryCommandSpec] = {
    "validate-workspace": DomainEntryCommandSpec(
        ("input_path",), help_text="校验 NSFC workspace。"
    ),
    "summarize-workspace": DomainEntryCommandSpec(
        ("input_path",), help_text="输出当前 workspace 摘要。"
    ),
    "grant-intake-audit": DomainEntryCommandSpec(
        ("input_path",), help_text="输出 grant intake audit surface。"
    ),
    "grant-evidence-grounding": DomainEntryCommandSpec(
        ("input_path",), help_text="输出 grant evidence grounding surface。"
    ),
    "grant-quality-scorecard": DomainEntryCommandSpec(
        ("input_path",), help_text="输出当前版本的质量治理 scorecard。"
    ),
    "grant-quality-closure-dossier": DomainEntryCommandSpec(
        ("input_path",),
        help_text="输出当前版本的质量 closure dossier。",
    ),
    "grant-quality-diff": DomainEntryCommandSpec(
        ("input_path", "previous_input_path"),
        help_text="对比两个版本的质量 scorecard 与问题关闭进度。",
    ),
    "discover-funding-opportunities": DomainEntryCommandSpec(
        ("input_path",),
        help_text="从材料与方向 hint 发现 funding opportunity pool。",
    ),
    "refresh-funding-opportunities-cache": DomainEntryCommandSpec(
        ("input_path",),
        ("output_path",),
        help_text="刷新官方 funding discovery cache，支持默认 runtime-state 落点。",
    ),
    "select-project-profile": DomainEntryCommandSpec(
        ("input_path",),
        help_text="从材料池与 funding pool 中选择推荐 project profile。",
    ),
    "initialize-intake-workspace": DomainEntryCommandSpec(
        ("input_path",),
        ("output_path", "workspace_root", "initialize_git"),
        help_text="根据推荐 project profile 初始化 input_intake workspace。",
        exclusive_fields=("output_path", "workspace_root"),
    ),
    "next-step": DomainEntryCommandSpec(
        ("input_path",), help_text="输出当前 workspace 的下一步建议。"
    ),
    "critique-summary": DomainEntryCommandSpec(
        ("input_path",), help_text="输出当前激活导师批注摘要。"
    ),
    "stage-route-report": DomainEntryCommandSpec(
        ("input_path",), help_text="按固定 stage route 聚合输出当前 workspace 状态。"
    ),
    "execute-strategy-authoring-pass": DomainEntryCommandSpec(
        ("input_path", "output_path"),
        help_text="默认 attempt 用一次 Codex 调用共同收敛方向、问题、论证、fit、提纲与 reviewable draft；失败或反馈仍可重试或 route back。",
    ),
    "execute-direction-screening-pass": DomainEntryCommandSpec(
        ("input_path", "output_path"),
        help_text="执行方向筛选 pass，生成 direction_screening workspace。",
    ),
    "execute-question-refinement-pass": DomainEntryCommandSpec(
        ("input_path", "output_path"),
        help_text="执行科学问题提纯 pass，生成 question_refinement workspace。",
    ),
    "execute-argument-building-pass": DomainEntryCommandSpec(
        ("input_path", "output_path"),
        help_text="执行立项依据构建 pass，生成 argument_building workspace。",
    ),
    "execute-fit-alignment-pass": DomainEntryCommandSpec(
        ("input_path", "output_path"),
        help_text="执行 applicant-problem fit 对齐 pass，生成 fit_alignment workspace。",
    ),
    "execute-outline-pass": DomainEntryCommandSpec(
        ("input_path", "output_path"),
        help_text="执行提纲冻结 pass，生成 outline workspace。",
    ),
    "execute-drafting-pass": DomainEntryCommandSpec(
        ("input_path", "output_path"),
        help_text="执行正文起草 pass，生成 drafting workspace。",
    ),
    "build-artifact-bundle": DomainEntryCommandSpec(
        ("input_path", "output_path"),
        help_text="把当前 workspace 的已冻结对象写成本地 artifact bundle。",
    ),
    "execute-critique-pass": DomainEntryCommandSpec(
        ("input_path", "output_path"),
        ("executor_kind",),
        help_text="通过 Codex CLI critique executor 生成导师式批注与 revision plan。",
    ),
    "execute-revision-pass": DomainEntryCommandSpec(
        ("input_path", "output_path"),
        help_text="应用 AI 明确给出的局部或 whole-draft revision mutation。",
    ),
    "execute-freeze-pass": DomainEntryCommandSpec(
        ("input_path", "output_path"),
        help_text="执行送审前冻结 pass，生成 frozen workspace。",
    ),
    "build-final-package": DomainEntryCommandSpec(
        ("input_path", "artifact_bundle_path", "output_path"),
        help_text="把 freeze-ready / submission-frozen workspace 写成本地 final package。",
    ),
    "build-hosted-contract-bundle": DomainEntryCommandSpec(
        ("final_package_path", "output_path"),
        help_text="把 final package 写成 hosted-friendly contract bundle。",
    ),
    "build-submission-ready-package": DomainEntryCommandSpec(
        ("input_path", "output_dir"),
        help_text="把 frozen workspace 一次性写成 submission-ready 本地交付目录。",
    ),
}
