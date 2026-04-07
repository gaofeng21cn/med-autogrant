from __future__ import annotations

from typing import Any

from med_autogrant.workspace import WorkspaceStateError, _require_workspace_context, validate_workspace_document


def determine_next_step(document: dict[str, Any]) -> dict[str, Any]:
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
    }

    if stage in {"critique", "revision"}:
        context = _require_workspace_context(document)
        critique = context.active_critique
        revision_plan = context.active_revision_plan
        active_draft = context.active_draft
        verdict = critique["verdict"]
        if verdict == "major_reframe":
            return {
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
        if verdict in {"major_revision", "minor_revision"}:
            if (
                stage == "revision"
                and active_draft["status"] == "revised"
                and revision_plan.get("execution_status") == "completed"
            ):
                return {
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
            return {
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
        if verdict == "ready_for_submission":
            return {
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

    if not gates["direction_frozen"]:
        return {
            **identity,
            "current_stage": stage,
            "recommended_stage": "direction_screening",
            "reason": "方向尚未冻结，不能继续向下游阶段推进。",
            "actions": [
                "筛选并冻结唯一主方向。",
            ],
            "requires_human_confirmation": document["mode"] != "auto",
        }
    if not gates["scientific_question_frozen"]:
        return {
            **identity,
            "current_stage": stage,
            "recommended_stage": "question_refinement",
            "reason": "科学问题尚未冻结，应先完成问题提纯。",
            "actions": [
                "明确知识边界、未知机制和可证伪表述。",
            ],
            "requires_human_confirmation": document["mode"] != "auto",
        }
    if not gates["argument_chain_frozen"]:
        return {
            **identity,
            "current_stage": stage,
            "recommended_stage": "argument_building",
            "reason": "立项依据主链尚未冻结，应先闭合必要性论证。",
            "actions": [
                "补足 field gap、necessity claim 和非任意路线理由。",
            ],
            "requires_human_confirmation": document["mode"] != "auto",
        }
    if not gates["fit_alignment_frozen"]:
        return {
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
    if not gates["outline_frozen"]:
        return {
            **identity,
            "current_stage": stage,
            "recommended_stage": "outline",
            "reason": "提纲尚未冻结，不能直接进入稳定 drafting/critique 闭环。",
            "actions": [
                "冻结章节提纲及每节核心论点。",
            ],
            "requires_human_confirmation": document["mode"] != "auto",
        }
    if stage == "outline":
        return {
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
    if stage == "drafting":
        return {
            **identity,
            "current_stage": stage,
            "recommended_stage": "critique",
            "reason": "当前草稿已形成，下一步进入导师批注。",
            "actions": [
                "生成导师批注并抽取结构化修订计划。",
            ],
            "requires_human_confirmation": False,
        }
    return {
        **identity,
        "current_stage": stage,
        "recommended_stage": stage,
        "reason": "当前状态已与冻结 gate 对齐，保持当前阶段继续推进。",
        "actions": [
            "沿当前阶段继续执行主线任务。",
        ],
        "requires_human_confirmation": document["mode"] != "auto",
    }
