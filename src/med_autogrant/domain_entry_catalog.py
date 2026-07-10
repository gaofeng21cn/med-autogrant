from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DomainEntryCommandSpec:
    runtime_method: str
    required_fields: tuple[str, ...]
    optional_fields: tuple[str, ...] = ()
    help_text: str = ""
    exclusive_fields: tuple[str, ...] = ()


SERVICE_SAFE_DOMAIN_COMMANDS: dict[str, DomainEntryCommandSpec] = {
    "validate-workspace": DomainEntryCommandSpec(
        "validate_workspace", ("input_path",), help_text="校验 NSFC workspace。"
    ),
    "summarize-workspace": DomainEntryCommandSpec(
        "summarize_workspace", ("input_path",), help_text="输出当前 workspace 摘要。"
    ),
    "grant-intake-audit": DomainEntryCommandSpec(
        "grant_intake_audit", ("input_path",), help_text="输出 grant intake audit surface。"
    ),
    "grant-evidence-grounding": DomainEntryCommandSpec(
        "grant_evidence_grounding", ("input_path",), help_text="输出 grant evidence grounding surface。"
    ),
    "grant-quality-scorecard": DomainEntryCommandSpec(
        "grant_quality_scorecard", ("input_path",), help_text="输出当前版本的质量治理 scorecard。"
    ),
    "grant-quality-closure-dossier": DomainEntryCommandSpec(
        "grant_quality_closure_dossier",
        ("input_path",),
        help_text="输出当前版本的质量 closure dossier。",
    ),
    "grant-quality-diff": DomainEntryCommandSpec(
        "grant_quality_diff",
        ("input_path", "previous_input_path"),
        help_text="对比两个版本的质量 scorecard 与问题关闭进度。",
    ),
    "discover-funding-opportunities": DomainEntryCommandSpec(
        "discover_funding_opportunities",
        ("input_path",),
        help_text="从材料与方向 hint 发现 funding opportunity pool。",
    ),
    "refresh-funding-opportunities-cache": DomainEntryCommandSpec(
        "refresh_funding_opportunities_cache",
        ("input_path",),
        ("output_path",),
        help_text="刷新官方 funding discovery cache，支持默认 runtime-state 落点。",
    ),
    "select-project-profile": DomainEntryCommandSpec(
        "select_project_profile",
        ("input_path",),
        help_text="从材料池与 funding pool 中选择推荐 project profile。",
    ),
    "initialize-intake-workspace": DomainEntryCommandSpec(
        "initialize_intake_workspace",
        ("input_path",),
        ("output_path", "workspace_root", "initialize_git"),
        help_text="根据推荐 project profile 初始化 input_intake workspace。",
        exclusive_fields=("output_path", "workspace_root"),
    ),
    "next-step": DomainEntryCommandSpec(
        "next_step", ("input_path",), help_text="输出当前 workspace 的下一步建议。"
    ),
    "critique-summary": DomainEntryCommandSpec(
        "critique_summary", ("input_path",), help_text="输出当前激活导师批注摘要。"
    ),
    "stage-route-report": DomainEntryCommandSpec(
        "stage_route_report", ("input_path",), help_text="按固定 stage route 聚合输出当前 workspace 状态。"
    ),
    "execute-direction-screening-pass": DomainEntryCommandSpec(
        "execute_direction_screening_pass",
        ("input_path", "output_path"),
        help_text="执行方向筛选 pass，生成 direction_screening workspace。",
    ),
    "execute-question-refinement-pass": DomainEntryCommandSpec(
        "execute_question_refinement_pass",
        ("input_path", "output_path"),
        help_text="执行科学问题提纯 pass，生成 question_refinement workspace。",
    ),
    "execute-argument-building-pass": DomainEntryCommandSpec(
        "execute_argument_building_pass",
        ("input_path", "output_path"),
        help_text="执行立项依据构建 pass，生成 argument_building workspace。",
    ),
    "execute-fit-alignment-pass": DomainEntryCommandSpec(
        "execute_fit_alignment_pass",
        ("input_path", "output_path"),
        help_text="执行 applicant-problem fit 对齐 pass，生成 fit_alignment workspace。",
    ),
    "execute-outline-pass": DomainEntryCommandSpec(
        "execute_outline_pass",
        ("input_path", "output_path"),
        help_text="执行提纲冻结 pass，生成 outline workspace。",
    ),
    "execute-drafting-pass": DomainEntryCommandSpec(
        "execute_drafting_pass",
        ("input_path", "output_path"),
        help_text="执行正文起草 pass，生成 drafting workspace。",
    ),
    "build-artifact-bundle": DomainEntryCommandSpec(
        "build_artifact_bundle",
        ("input_path", "output_path"),
        help_text="把当前 workspace 的已冻结对象写成本地 artifact bundle。",
    ),
    "execute-critique-pass": DomainEntryCommandSpec(
        "execute_critique_pass",
        ("input_path", "output_path"),
        ("executor_kind",),
        help_text="通过 Codex CLI critique executor 生成导师式批注与 revision plan。",
    ),
    "execute-critique-revision-loop": DomainEntryCommandSpec(
        "execute_critique_revision_loop",
        ("input_path", "output_dir", "opl_stage_attempt"),
        ("max_rounds", "executor_kind"),
        help_text="执行多轮 critique/revision closed loop，直到通过或 fail-closed 停止。",
    ),
    "execute-authoring-mainline-loop": DomainEntryCommandSpec(
        "execute_authoring_mainline_loop",
        ("input_path", "output_dir", "opl_stage_attempt"),
        ("max_cycles", "executor_kind"),
        help_text="执行跨 question/argument/fit/drafting/critique/revision/frozen 的全链路主线 loop。",
    ),
    "execute-grant-autonomy-controller": DomainEntryCommandSpec(
        "execute_grant_autonomy_controller",
        ("input_path", "output_dir", "opl_stage_attempt"),
        ("executor_kind",),
        help_text="执行长期自治 controller，调度 pre-workspace、mainline 与 quality gate。",
    ),
    "execute-revision-pass": DomainEntryCommandSpec(
        "execute_revision_pass",
        ("input_path", "output_path"),
        help_text="按冻结的 section-level deterministic contract 执行 revision pass。",
    ),
    "execute-freeze-pass": DomainEntryCommandSpec(
        "execute_freeze_pass",
        ("input_path", "output_path"),
        help_text="执行送审前冻结 pass，生成 frozen workspace。",
    ),
    "build-final-package": DomainEntryCommandSpec(
        "build_final_package",
        ("input_path", "artifact_bundle_path", "output_path"),
        help_text="把 freeze-ready / submission-frozen workspace 写成本地 final package。",
    ),
    "build-hosted-contract-bundle": DomainEntryCommandSpec(
        "build_hosted_contract_bundle",
        ("final_package_path", "output_path"),
        help_text="把 final package 写成 hosted-friendly contract bundle。",
    ),
    "build-submission-ready-package": DomainEntryCommandSpec(
        "build_submission_ready_package",
        ("input_path", "output_dir"),
        help_text="把 frozen workspace 一次性写成 submission-ready 本地交付目录。",
    ),
}
