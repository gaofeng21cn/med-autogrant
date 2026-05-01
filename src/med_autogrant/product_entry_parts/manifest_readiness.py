from __future__ import annotations

from typing import Any

from med_autogrant.product_entry_parts.primitives import PRODUCT_FRONTDESK_KIND, GRANT_USER_LOOP_KIND

from opl_harness_shared.product_entry_program_companions import (
    build_detailed_readiness as _build_shared_detailed_readiness,
    build_workflow_coverage_item as _build_shared_workflow_coverage_item,
)
from opl_harness_shared.product_entry_companions import (
    build_product_entry_readiness as _build_shared_product_entry_readiness,
)


def build_manifest_readiness_surfaces(
    *,
    product_frontdesk_command: str,
    grant_user_loop_command: str,
) -> dict[str, dict[str, Any]]:
    grant_authoring_readiness = _build_shared_detailed_readiness(
        surface_kind="grant_authoring_readiness",
        verdict="agent_assisted_cli_ready_not_full_autopilot",
        fully_automatic=False,
        usable_now=True,
        good_to_use_now=False,
        user_experience_level="usable_for_agent_assisted_cli_authoring_not_yet_polished_product",
        summary=(
            "当前可以作为 Agent 协同的 CLI/controller 标书写作主线使用；"
            "对满足冻结与材料齐备条件的 workspace，已经能一键导出本地 submission-ready 交付包，"
            "但还不是无需人工材料、无需判断、可直接官网提交的全自动国自然标书产品。"
        ),
        recommended_start_surface=PRODUCT_FRONTDESK_KIND,
        recommended_start_command=product_frontdesk_command,
        recommended_loop_surface=GRANT_USER_LOOP_KIND,
        recommended_loop_command=grant_user_loop_command,
        workflow_coverage=[
            _build_shared_workflow_coverage_item(
                step_id="accumulation_direction_screening",
                manual_flow_label="从已有积累中筛选方向",
                coverage_status="landed_route",
                current_surface="execute-direction-screening-pass",
                remaining_gap="需要用户先提供真实课题、论文、前期结果和在研工作材料。",
            ),
            _build_shared_workflow_coverage_item(
                step_id="hotspot_literature_fit",
                manual_flow_label="筛选可嵌入的热点",
                coverage_status="partially_supported",
                current_surface="question_refinement / argument_building",
                remaining_gap="自动文献检索、热点筛选和引用证据绑定尚未作为 repo-tracked runtime contract 落地。",
            ),
            _build_shared_workflow_coverage_item(
                step_id="clinical_question_refinement",
                manual_flow_label="锚定具体临床问题",
                coverage_status="landed_route",
                current_surface="execute-question-refinement-pass",
                remaining_gap="仍需要用户或导师确认问题是否真实、有价值且不跑偏。",
            ),
            _build_shared_workflow_coverage_item(
                step_id="innovation_framework",
                manual_flow_label="设计创新点和跨尺度框架",
                coverage_status="landed_route",
                current_surface="execute-argument-building-pass / execute-fit-alignment-pass",
                remaining_gap="跨尺度组学、指南更新和多学科交叉证据仍依赖用户输入材料与后续证据补强。",
            ),
            _build_shared_workflow_coverage_item(
                step_id="mainline_closure",
                manual_flow_label="搭建整体课题并反复校验主线",
                coverage_status="landed_route",
                current_surface="grant-user-loop / stage-route-report",
                remaining_gap="当前能投影 route 与 gate，但还不是成熟 Web UI 里的连续审稿体验。",
            ),
            _build_shared_workflow_coverage_item(
                step_id="significance_background_drafting",
                manual_flow_label="先写研究意义，再写研究背景",
                coverage_status="landed_route",
                current_surface="execute-outline-pass / execute-drafting-pass",
                remaining_gap="背景文献的新鲜性、引用准确性和段落风格仍需要人工或 Agent 复核。",
            ),
            _build_shared_workflow_coverage_item(
                step_id="preliminary_evidence_and_basis",
                manual_flow_label="补足预实验、研究基础和前期结果",
                coverage_status="partially_supported",
                current_surface="workspace evidence surfaces / build-artifact-bundle",
                remaining_gap="不会凭空生成真实预实验；缺失证据、图片和原始结果仍必须由用户补充。",
            ),
            _build_shared_workflow_coverage_item(
                step_id="expected_results_timeline",
                manual_flow_label="完善预期结果与研究进度",
                coverage_status="partially_supported",
                current_surface="execute-drafting-pass / build-artifact-bundle",
                remaining_gap="研究进度、经费/时间排布与申请书表格化输出尚未形成成熟产品面。",
            ),
            _build_shared_workflow_coverage_item(
                step_id="final_review_figures_package",
                manual_flow_label="全文反复检查并补图补结果",
                coverage_status="partially_supported",
                current_surface="execute-critique-pass / execute-revision-pass / build-submission-ready-package",
                remaining_gap="本地 submission-ready 交付包已可一键导出，但图件生成、Word/PDF 版式化、官网代投与最终格式审查仍未全自动产品化。",
            ),
        ],
        blocking_gaps=[
            "还不是 mature direct grant Web UI / hosted runtime。",
            "还不能在缺少用户真实材料、前期结果和图片素材时全自动生成可信标书。",
            "文献热点检索、引用证据绑定、图件生产、Word/PDF 定稿与外部官网提交仍未完整产品化。",
        ],
    )
    product_entry_readiness = _build_shared_product_entry_readiness(
        verdict="agent_assisted_ready_not_product_grade",
        usable_now=True,
        good_to_use_now=False,
        fully_automatic=False,
        summary=grant_authoring_readiness["summary"],
        recommended_start_surface=grant_authoring_readiness["recommended_start_surface"],
        recommended_start_command=grant_authoring_readiness["recommended_start_command"],
        recommended_loop_surface=grant_authoring_readiness["recommended_loop_surface"],
        recommended_loop_command=grant_authoring_readiness["recommended_loop_command"],
        blocking_gaps=list(grant_authoring_readiness["blocking_gaps"]),
    )
    return {
        "grant_authoring_readiness": grant_authoring_readiness,
        "product_entry_readiness": product_entry_readiness,
    }
