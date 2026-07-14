from __future__ import annotations

from typing import Any

from med_autogrant.grant_quality import build_grant_quality_scorecard
from med_autogrant.opl_execution_boundary import build_ai_route_boundary
from med_autogrant.workspace_projection_parts import _require_workspace_context
from med_autogrant.workspace_types import WorkspaceStateError
from med_autogrant.workspace_validation import validate_workspace_document


def determine_next_step(document: dict[str, Any]) -> dict[str, Any]:
    try:
        structural_route = _determine_structural_next_step(document)
    except WorkspaceStateError as error:
        current_stage = str(document.get("lifecycle_stage") or "call_and_candidate_intake")
        return _with_ai_route_context(
            {
                "grant_run_id": document.get("grant_run_id"),
                "workspace_id": document.get("workspace_id"),
                "current_stage": current_stage,
                "recommended_stage": current_stage,
                "reason": "Workspace validation findings are preserved as Codex input; they do not block stage progress.",
                "actions": ["Continue from the readable workspace content and repair structure within the quality budget."],
                "requires_human_confirmation": False,
                "quality_debt": {
                    "status": "open",
                    "debt_code": "workspace_projection_invalid",
                    "findings": [
                        {"path": item.path, "message": item.message}
                        for item in error.errors
                    ],
                    "blocks_stage_transition": False,
                    "blocks_quality_export_or_ready_claims": True,
                },
            }
        )
    return _apply_quality_gate_to_route(
        route=structural_route,
        quality_scorecard=build_grant_quality_scorecard(document),
    )


def _determine_structural_next_step(document: dict[str, Any]) -> dict[str, Any]:
    validation = validate_workspace_document(document)
    if not validation.ok:
        first = validation.errors[0]
        raise WorkspaceStateError(
            f"{first.path}: {first.message}",
            errors=validation.errors,
            grant_run_id=document.get("grant_run_id"),
            workspace_id=document.get("workspace_id"),
            lifecycle_stage=document.get("lifecycle_stage"),
        )

    stage = document["lifecycle_stage"]
    gates = document["gates"]
    identity = {
        "grant_run_id": document["grant_run_id"],
        "workspace_id": document["workspace_id"],
        "presubmission_frozen": bool(gates.get("presubmission_frozen")),
    }

    if stage in {"critique", "revision"}:
        context = _require_workspace_context(document)
        critique = context.active_critique
        revision_plan = context.active_revision_plan
        active_draft = context.active_draft
        verdict = critique["verdict"]
        forced_rollback_stage = critique.get("forced_rollback_stage")
        forced_rollback_reason = critique.get("forced_rollback_reason")
        if forced_rollback_stage is not None:
            return _with_ai_route_context(
                {
                **identity,
                "current_stage": stage,
                "recommended_stage": forced_rollback_stage,
                "forced_rollback_stage": forced_rollback_stage,
                "reason": f"当前批注触发 forced rollback，应回退到 {forced_rollback_stage}：{forced_rollback_reason}",
                "actions": _build_forced_rollback_actions(forced_rollback_stage),
                "requires_human_confirmation": (
                    document["mode"] != "auto"
                    if forced_rollback_stage in {"direction_screening", "question_refinement"}
                    else False
                ),
                }
            )
        if verdict == "major_reframe":
            return _with_ai_route_context(
                {
                **identity,
                "current_stage": stage,
                "recommended_stage": "question_refinement",
                "reason": "导师批注判定需要重塑科学问题，应回退到 question_refinement。",
                "actions": [
                    "重塑科学问题，并核查是否仍与当前方向匹配。",
                    "如当前方向无法支撑机制级问题，回退到 direction_screening。",
                ],
                "requires_human_confirmation": document["mode"] != "auto",
                }
            )
        if verdict in {"major_revision", "minor_revision"}:
            if (
                active_draft["status"] == "revised"
                and revision_plan.get("execution_status") == "completed"
            ):
                return _with_ai_route_context(
                    {
                    **identity,
                    "current_stage": stage,
                    "recommended_stage": "critique",
                    "reason": "当前 revision 已完成显式 revised 切换，应带着 revised 草稿回到 critique 做 re-review。",
                    "actions": [
                        "提交 revised 草稿进入新一轮导师批注。",
                        "基于 comparison_summary 核对本轮修订是否覆盖前一轮 blocking issues。",
                    ],
                    "requires_human_confirmation": False,
                    }
                )
            return _with_ai_route_context(
                {
                **identity,
                "current_stage": stage,
                "recommended_stage": "revision",
                "reason": f"导师批注 verdict={verdict}，应先执行结构化修订。",
                "actions": [
                    "执行 revision plan 中的 P0/P1 项。",
                    "修订后重新进入导师批注闭环。",
                ],
                "requires_human_confirmation": False,
                }
            )
        if verdict == "ready_for_submission":
            return _with_ai_route_context(
                {
                **identity,
                "current_stage": stage,
                "recommended_stage": "frozen" if gates["presubmission_frozen"] else "frozen",
                "reason": "当前批注已经达到 ready_for_submission，可进入送审前冻结。",
                "actions": [
                    "冻结 presubmission 版本。",
                    "记录最终送审前版本和下一轮外部 review 入口。",
                ],
                "requires_human_confirmation": True,
                }
            )

    if not gates["direction_frozen"]:
        return _with_ai_route_context(
            {
            **identity,
            "current_stage": stage,
            "recommended_stage": "direction_screening",
            "reason": "方向尚未冻结；建议 Codex 优先补齐方向判断，也可携带当前草稿与该质量债推进其他 declared stage。",
            "actions": [
                "筛选并冻结唯一主方向。",
            ],
            "requires_human_confirmation": document["mode"] != "auto",
            }
        )
    if not gates["scientific_question_frozen"]:
        return _with_ai_route_context(
            {
            **identity,
            "current_stage": stage,
            "recommended_stage": "question_refinement",
            "reason": "科学问题尚未冻结，应先完成问题提纯。",
            "actions": [
                "明确知识边界、未知机制和可证伪表述。",
            ],
            "requires_human_confirmation": document["mode"] != "auto",
            }
        )
    if not gates["argument_chain_frozen"]:
        return _with_ai_route_context(
            {
            **identity,
            "current_stage": stage,
            "recommended_stage": "argument_building",
            "reason": "立项依据主链尚未冻结，应先闭合必要性论证。",
            "actions": [
                "补足 field gap、necessity claim 和非任意路线理由。",
            ],
            "requires_human_confirmation": document["mode"] != "auto",
            }
        )
    if not gates["fit_alignment_frozen"]:
        return _with_ai_route_context(
            {
            **identity,
            "current_stage": stage,
            "recommended_stage": "fit_alignment",
            "reason": "申请人适配度映射尚未冻结，应先完成 applicant-problem fit 对齐。",
            "actions": [
                "补足申请人既有基础、方法栈与当前问题的显式映射。",
                "把 applicant fit 证据链绑定到当前 ArgumentChain。",
            ],
            "requires_human_confirmation": document["mode"] != "auto",
            }
        )
    if not gates["outline_frozen"]:
        return _with_ai_route_context(
            {
            **identity,
            "current_stage": stage,
            "recommended_stage": "outline",
            "reason": "提纲尚未冻结；建议 Codex 优先补齐提纲，也可携带当前草稿与该质量债推进其他 declared stage。",
            "actions": [
                "冻结章节提纲及每节核心论点。",
            ],
            "requires_human_confirmation": document["mode"] != "auto",
            }
        )
    if stage == "outline":
        return _with_ai_route_context(
            {
            **identity,
            "current_stage": stage,
            "recommended_stage": "drafting",
            "reason": "提纲已冻结，可在不改写上游 contract 的前提下进入 drafting。",
            "actions": [
                "基于已冻结 outline 展开章节草稿。",
                "保持当前 question / argument chain / fit mapping 链接不漂移。",
            ],
            "requires_human_confirmation": document["mode"] != "auto",
            }
        )
    if stage == "drafting":
        return _with_ai_route_context(
            {
            **identity,
            "current_stage": stage,
            "recommended_stage": "critique",
            "reason": "当前草稿已形成，下一步进入导师批注。",
            "actions": [
                "生成导师批注并抽取结构化修订计划。",
            ],
            "requires_human_confirmation": False,
            }
        )
    return _with_ai_route_context(
        {
        **identity,
        "current_stage": stage,
        "recommended_stage": stage,
        "reason": "当前状态已与冻结 gate 对齐，保持当前阶段继续推进。",
        "actions": [
            "沿当前阶段继续执行主线任务。",
        ],
        "requires_human_confirmation": document["mode"] != "auto",
        }
    )


def _apply_quality_gate_to_route(
    *,
    route: dict[str, Any],
    quality_scorecard: dict[str, Any],
) -> dict[str, Any]:
    resolved_route = dict(route)
    quality_gate = quality_scorecard.get("loop_gate")
    if not isinstance(quality_gate, dict):
        return resolved_route

    resolved_route["quality_gate"] = dict(quality_gate)
    gate_action = str(quality_gate.get("action") or "").strip()
    gate_reason = str(quality_gate.get("reason") or "").strip()
    gate_stage = str(quality_gate.get("recommended_stage") or "").strip()
    route_stage = str(resolved_route.get("recommended_stage") or "").strip()

    if gate_action in {"route_back_recommended", "continue"} and gate_reason:
        resolved_route["quality_debt"] = {
            "status": "open",
            "debt_code": f"quality_gate_{gate_action}",
            "reason": gate_reason,
            "recommended_repair_stage": gate_stage or None,
            "blocks_stage_transition": False,
            "blocks_quality_export_or_ready_claims": True,
        }
        resolved_route["reason"] = (
            f"{resolved_route.get('reason') or ''} 当前质量缺口已登记为非阻断债务：{gate_reason}".strip()
        )
    elif gate_action == "ready_for_submission" and gate_reason:
        resolved_route["reason"] = f"{resolved_route.get('reason') or ''} {gate_reason}".strip()

    return resolved_route


def _with_ai_route_context(payload: dict[str, Any]) -> dict[str, Any]:
    current_stage = str(payload.get("current_stage") or "")
    recommended_stage = str(payload.get("recommended_stage") or "")
    return {
        "surface_kind": "mag_ai_route_context",
        **payload,
        "current_stage_role": "workspace_lifecycle_observation",
        "recommended_stage_role": "non_authoritative_repair_hint",
        "semantic_route_owner": "decisive_codex_attempt",
        "authority_boundary": build_ai_route_boundary(
            surface_id="mag.next-step",
            mag_role="route_context_projection_only",
        ),
        "ai_route_policy": {
            "semantic_route_owner": "decisive_codex_attempt",
            "declared_stage_scope_only": True,
            "program_recommendation_can_block_or_select_route": False,
            "advance_repeat_skip_or_route_back_allowed": True,
            "suggested_source_stage": current_stage,
            "suggested_target_stage": recommended_stage,
        },
    }
def _build_forced_rollback_actions(target_stage: str) -> list[str]:
    if target_stage == "direction_screening":
        return [
            "重新筛选主方向，并判断当前题目是否还值得保留。",
            "只保留能够承载机制级科学问题的方向候选。",
        ]
    if target_stage == "question_refinement":
        return [
            "回退重塑核心科学问题，并重新冻结知识边界与可证伪表述。",
            "确认当前问题仍与所选方向严格一致。",
        ]
    if target_stage == "argument_building":
        return [
            "回退重建立项依据主链，重新闭合 field gap、necessity claim 与 route justification。",
            "让新的 argument chain 显式回指当前问题与关键证据。",
        ]
    if target_stage == "fit_alignment":
        return [
            "回退重建 applicant-problem fit 映射，并重新核对研究基础与关键验证节点的对齐。",
            "补足申请人与问题之间的不可替代性证据链。",
        ]
    return [
        "按当前 rollback target 回退并重建上游对象。",
    ]
