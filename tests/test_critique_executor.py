from __future__ import annotations

import sys
import unittest
from copy import deepcopy
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from med_autogrant.workspace import load_workspace_document, validate_workspace_document  # noqa: E402


DRAFTING_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2c_drafting.json"
REVISION_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2c_revision.json"


def _codex_runner_with_packet(
    testcase: unittest.TestCase,
    input_path: Path,
    packet: dict[str, object],
):
    def fake_codex_runner(_prompt: str, *, cwd: Path) -> dict[str, object]:
        testcase.assertEqual(cwd, input_path.resolve().parent)
        return packet

    return fake_codex_runner


def _critique_closeout_packet(*, owner: str) -> dict[str, object]:
    return {
        "mentor_critique": {
            "metadata": {
                "schema_version": "v1",
                "created_at": "2026-04-13T12:00:00Z",
                "updated_at": "2026-04-13T12:00:00Z",
                "source_mode": "auto",
                "owner": owner,
            },
            "critique_id": "critique-v1",
            "draft_id": "should-be-overridden",
            "overall_diagnosis": "草稿已经具备基本结构，但必要性链条仍需要收紧。",
            "current_scientific_question": "should-be-overridden",
            "suggested_question": "需要把关键科学问题改写得更聚焦机制级未知。",
            "verdict": "major_revision",
            "necessity_scientific_value": {
                "weight": 1,
                "score": 76,
                "judgment": "必要性主线方向正确，但机制未知和理论损失还需要更锋利。",
                "blocking_issues": ["尚未明确说明为什么现有现象学研究不能回答机制问题。"],
            },
            "applicant_fit": {
                "weight": 1,
                "score": 81,
                "judgment": "申请人基础较好，但既有成果与当前问题映射还不够直接。",
                "blocking_issues": ["需要让前期成果直接回指当前机制验证路径。"],
            },
            "feasibility": {
                "weight": 1,
                "score": 79,
                "judgment": "总体可行，但关键实验闭环还需要更明确。",
                "blocking_issues": [],
            },
            "logic_chain_repairs": ["补出从现象相关到机制未知的关键过渡段。"],
            "applicant_fit_repairs": ["把申请人既有单细胞资源与关键验证节点逐点绑定。"],
            "blocking_issues": ["必要性表述仍偏现象描述。"],
        },
        "revision_plan": {
            "metadata": {
                "schema_version": "v1",
                "created_at": "2026-04-13T12:05:00Z",
                "updated_at": "2026-04-13T12:05:00Z",
                "source_mode": "auto",
                "owner": owner,
            },
            "revision_plan_id": "revision-v1",
            "draft_id": "should-be-overridden",
            "critique_id": "should-be-overridden",
            "pre_revision_version_label": "should-be-overridden",
            "post_revision_version_label": "v0.2",
            "items": [
                {
                    "item_id": "rev-item-1",
                    "priority": "p0",
                    "action_type": "rebuild_argument",
                    "target_ref": "section:basis",
                    "action": "收紧立项依据中从现象到机制缺口的推导。",
                    "done_criteria": "读者能清楚理解知识边界、未知机制与理论损失。",
                    "required_input_ids": ["arg-001", "question-immune-fibrosis"],
                    "mutation_payload": {
                        "operation": "replace_draft_section",
                        "target_section_key": "basis",
                        "replacement_text": "当前关键知识缺口不在于心梗后炎症与纤维化是否相关，而在于炎症巨噬细胞如何通过时间窗依赖的旁分泌通讯触发成纤维细胞致纤维化重编程。",
                        "replacement_core_claim": "本研究的必要性在于解释炎症巨噬细胞驱动纤维化重编程的时间窗机制缺口。",
                        "linked_object_ids": ["arg-001", "question-immune-fibrosis"],
                    },
                }
            ],
            "next_review_focus": ["必要性链条是否真正闭合"],
        },
    }


def _rereview_closeout_packet() -> dict[str, object]:
    packet = _critique_closeout_packet(owner="Codex CLI critique executor")
    critique = packet["mentor_critique"]
    critique.update(
        {
            "critique_id": "critique-v2",
            "draft_id": "ignored",
            "reviewed_revision_plan_id": "ignored",
            "overall_diagnosis": "上一轮修订改善明显，但研究基础与验证路线还需继续收紧。",
            "current_scientific_question": "ignored",
            "suggested_question": "保持核心科学问题不变，继续收紧研究基础与验证路线的闭环。",
            "necessity_scientific_value": {
                **critique["necessity_scientific_value"],
                "score": 81,
                "judgment": "必要性链条改善明显，但仍存在机制跳步。",
                "blocking_issues": ["需要继续压缩修订后机制跳步。"],
            },
            "applicant_fit": {
                **critique["applicant_fit"],
                "score": 85,
                "judgment": "申请人适配度较强，但仍需更直接回指关键验证节点。",
                "blocking_issues": [],
            },
            "feasibility": {**critique["feasibility"], "score": 82, "judgment": "整体可行。"},
            "blocking_issues": ["re-review 必须保留上一轮 completed revision evidence。"],
        }
    )
    revision_plan = packet["revision_plan"]
    revision_plan.update(
        {
            "revision_plan_id": "revision-v2",
            "draft_id": "ignored",
            "critique_id": "ignored",
            "pre_revision_version_label": "ignored",
            "post_revision_version_label": "v0.5",
            "items": [
                {
                    "item_id": "rev2-item-1",
                    "priority": "p0",
                    "action_type": "rewrite_section",
                    "target_ref": "section:foundation",
                    "action": "让研究基础直接回指当前方案关键验证节点。",
                    "done_criteria": "研究基础段落能直接解释为什么该团队能完成当前机制验证。",
                    "required_input_ids": ["output-1", "project-1"],
                    "mutation_payload": {
                        "operation": "replace_draft_section",
                        "target_section_key": "foundation",
                        "replacement_text": "申请人的单细胞时序资源、动物模型和既有验证路径可以直接承接当前机制验证假设，从而把研究基础与关键实验闭环为同一条执行链。",
                        "replacement_core_claim": "研究基础能够直接支撑当前机制验证闭环。",
                        "linked_object_ids": ["output-1", "project-1"],
                    },
                }
            ],
        }
    )
    return packet


class CritiqueExecutionDocumentTest(unittest.TestCase):
    def assertDraftingCritiquePayload(self, payload: dict[str, object]) -> None:
        self.assertEqual(payload["grant_run_id"], "grant-run-nsfc-demo-001-baseline-001")
        self.assertEqual(payload["workspace_id"], "nsfc-demo-001")
        self.assertEqual(payload["draft_id"], "draft-v1")
        self.assertEqual(payload["active_revision_plan_id"], "revision-v1")
        self.assertEqual(payload["lifecycle_stage"], "critique")

    def test_critique_executor_kind_vocabulary_rejects_retired_aliases(self) -> None:
        from med_autogrant.critique_executor import _resolve_critique_executor_kind
        from med_autogrant.workspace import WorkspaceStateError

        self.assertEqual(_resolve_critique_executor_kind(None), "codex_cli")
        self.assertEqual(_resolve_critique_executor_kind("codex_cli"), "codex_cli")
        self.assertEqual(_resolve_critique_executor_kind("hermes_agent"), "hermes_agent")

        retired_aliases = ["codex_cli" + "_autonomous", "hermes" + "_native" + "_proof"]
        for retired_alias in retired_aliases:
            with self.subTest(retired_alias=retired_alias):
                with self.assertRaisesRegex(WorkspaceStateError, "不支持该 executor_kind"):
                    _resolve_critique_executor_kind(retired_alias)

    def test_build_critique_prompt_spells_out_weighted_score_block_field_names(self) -> None:
        from med_autogrant.critique_executor import _build_critique_context, _build_critique_prompt
        from med_autogrant.workspace_projection_parts import _build_workspace_state

        document = load_workspace_document(DRAFTING_EXAMPLE_PATH)
        context = _build_critique_context(
            document=document,
            state=_build_workspace_state(document),
        )

        prompt = _build_critique_prompt(context=context, input_path=DRAFTING_EXAMPLE_PATH)

        for fragment in (
            "must each be an object with exactly weight, score, judgment",
            "do not emit rationale or verdict inside these weighted score blocks",
            "Critique policy/persona contract:", "weight split: necessity_scientific_value=60, applicant_fit=30, feasibility=10",
            "diagnose necessity and scientific question first", "clearly separate scientific question framing from engineering task decomposition",
            "overall_diagnosis", "suggested_question", "logic_chain_repairs", "applicant_fit_repairs",
        ):
            self.assertIn(fragment, prompt)

    def test_build_critique_prompt_uses_project_profile_policy_resolver(self) -> None:
        from med_autogrant.critique_executor import _build_critique_context, _build_critique_prompt
        from med_autogrant.workspace_projection_parts import _build_workspace_state

        document = deepcopy(load_workspace_document(DRAFTING_EXAMPLE_PATH))
        document["project_profile"]["preset_id"] = "nih_r21_translational_v1"
        document["project_profile"]["profile_label"] = "NIH R21 translational profile"
        document["project_profile"]["critique_policy"] = {
            "preset_id": "nih_r21_significance_innovation_v1",
            "policy_id": "nih_r21_significance_innovation_v1",
        }

        context = _build_critique_context(
            document=document,
            state=_build_workspace_state(document),
        )

        prompt = _build_critique_prompt(context=context, input_path=DRAFTING_EXAMPLE_PATH)

        self.assertIn("policy_id: nih_r21_significance_innovation_v1", prompt)
        self.assertIn("persona role: NIH R21 scientific reviewer", prompt)
        self.assertIn("significance=45, innovation=35, investigator_environment_fit=20", prompt)

    def test_build_critique_execution_document_materializes_landed_critique_workspace(self) -> None:
        from med_autogrant.critique_executor import build_critique_execution_document

        document = load_workspace_document(DRAFTING_EXAMPLE_PATH)

        payload = build_critique_execution_document(
            document=document,
            input_path=DRAFTING_EXAMPLE_PATH,
            codex_runner=_codex_runner_with_packet(
                self,
                DRAFTING_EXAMPLE_PATH,
                _critique_closeout_packet(owner="Codex CLI critique executor"),
            ),
        )

        critique_workspace = payload["critique_workspace"]
        critique = critique_workspace["mentor_critiques"][-1]
        revision_plan = critique_workspace["revision_plans"][-1]
        evidence = critique["metadata"]["independent_review_evidence"]
        self.assertDraftingCritiquePayload(payload)
        self.assertEqual(payload["critique_execution"]["executor"]["kind"], "codex_cli")
        self.assertEqual(payload["critique_execution"]["critique_id"], "critique-v1")
        self.assertEqual(payload["critique_execution"]["active_revision_plan_id"], "revision-v1")
        self.assertEqual(payload["critique_execution"]["verdict"], "major_revision")
        self.assertEqual(critique_workspace["lifecycle_stage"], "critique")
        self.assertEqual(critique_workspace["current_selection"]["active_revision_plan_id"], "revision-v1")
        self.assertEqual(critique["draft_id"], "draft-v1")
        self.assertEqual(
            critique["current_scientific_question"],
            document["scientific_question_cards"][0]["core_question"],
        )
        self.assertEqual(critique["necessity_scientific_value"]["weight"], 60)
        self.assertEqual(critique["applicant_fit"]["weight"], 30)
        self.assertEqual(critique["feasibility"]["weight"], 10)
        self.assertEqual(evidence["review_attempt_ref"], "mentor_critiques::critique-v1")
        self.assertTrue(evidence["no_shared_context_verified"])
        self.assertEqual(revision_plan["draft_id"], "draft-v1")
        self.assertEqual(revision_plan["critique_id"], "critique-v1")
        self.assertEqual(revision_plan["pre_revision_version_label"], "v0.1")
        self.assertEqual(validate_workspace_document(critique_workspace).ok, True)

    def test_build_critique_execution_document_binds_completed_revision_evidence_on_rereview(self) -> None:
        from med_autogrant.critique_executor import build_critique_execution_document

        document = load_workspace_document(REVISION_EXAMPLE_PATH)

        payload = build_critique_execution_document(
            document=document,
            input_path=REVISION_EXAMPLE_PATH,
            codex_runner=_codex_runner_with_packet(self, REVISION_EXAMPLE_PATH, _rereview_closeout_packet()),
        )

        critique_workspace = payload["critique_workspace"]
        critique = critique_workspace["mentor_critiques"][-1]
        revision_plan = critique_workspace["revision_plans"][-1]
        evidence = critique["metadata"]["independent_review_evidence"]
        self.assertEqual(payload["active_revision_plan_id"], "revision-v2")
        self.assertEqual(critique_workspace["current_selection"]["active_revision_plan_id"], "revision-v2")
        self.assertEqual(critique["critique_id"], "critique-v2")
        self.assertEqual(critique["reviewed_revision_plan_id"], "revision-v1")
        self.assertEqual(
            evidence["execution_attempt_ref"],
            "draft_artifact::grant-run-nsfc-demo-001-baseline-001::draft-v1",
        )
        self.assertEqual(
            evidence["review_receipt_ref"],
            "mentor_critiques::critique-v2::metadata.independent_review_evidence",
        )
        self.assertEqual(revision_plan["revision_plan_id"], "revision-v2")
        self.assertEqual(revision_plan["critique_id"], "critique-v2")
        self.assertEqual(revision_plan["pre_revision_version_label"], "v0.4")
        self.assertEqual(validate_workspace_document(critique_workspace).ok, True)

    def test_build_critique_execution_document_supports_explicit_hermes_agent_receipt(self) -> None:
        from med_autogrant.critique_executor import build_critique_execution_document

        document = load_workspace_document(DRAFTING_EXAMPLE_PATH)

        def fake_opl_executor_runner(request: dict[str, object], *, cwd: Path) -> dict[str, object]:
            self.assertEqual(cwd, DRAFTING_EXAMPLE_PATH.resolve().parent)
            self.assertEqual(request["executor_kind"], "hermes_agent")
            self.assertEqual(request["mode"], "agent_loop")
            self.assertEqual(
                request["domain_payload"],
                {
                    "domain_id": "med-autogrant",
                    "route_id": "critique",
                    "input_path": str(DRAFTING_EXAMPLE_PATH.resolve()),
                },
            )
            event_summary = [
                {"type": "tool_start", "tool": "read_file"},
                {"type": "tool_complete", "tool": "read_file"},
            ]
            proof = {
                "proof_kind": "full_agent_loop_aiaagent",
                "full_agent_loop_proved": True,
                "session_id": "hermes-session-proof-001",
                "api_calls": 2,
                "tool_call_count": 1,
                "event_count": 4,
                "provider_reasoning_status": "unproven_custom_chat_completions",
                "event_stream": event_summary,
            }
            return {
                "surface_kind": "opl_agent_execution_receipt",
                "executor_kind": "hermes_agent",
                "mode": "agent_loop",
                "cwd": str(DRAFTING_EXAMPLE_PATH.resolve().parent),
                "prompt_preview": "critique prompt",
                "session_id": "hermes-session-proof-001",
                "event_summary": event_summary,
                "stdout_preview": "{}",
                "stderr_preview": "",
                "exit_code": 0,
                "closeout_packet": {
                    "surface_kind": "mag_critique_closeout_packet",
                    **_critique_closeout_packet(owner="OPL executor adapter critique receipt owner"),
                },
                "capabilities": ["full_agent_loop_receipt", "tool_event_proof", "session_id"],
                "non_equivalence_notice": "connectivity_lifecycle_receipt_audit_only",
                "proof": proof,
                "executor_contract": {
                    "entrypoint": "OPL AgentExecutionRequest -> AgentExecutionReceipt",
                    "model": "gpt-5.4",
                    "provider": "custom",
                    "api_mode": "chat_completions",
                    "reasoning_effort": "xhigh",
                },
            }

        payload = build_critique_execution_document(
            document=document,
            input_path=DRAFTING_EXAMPLE_PATH,
            executor_kind="hermes_agent",
            opl_executor_runner=fake_opl_executor_runner,
        )

        critique_workspace = payload["critique_workspace"]
        executor = payload["critique_execution"]["executor"]
        evidence = critique_workspace["mentor_critiques"][-1]["metadata"]["independent_review_evidence"]
        self.assertDraftingCritiquePayload(payload)
        self.assertEqual(executor["kind"], "hermes_agent")
        self.assertEqual(executor["mode"], "agent_loop")
        self.assertEqual(executor["adapter_owner"], "one-person-lab")
        self.assertEqual(
            executor["adapter_contract_ref"],
            "contracts/opl-framework/family-executor-adapter-defaults.json",
        )
        self.assertEqual(executor["request_contract"], "AgentExecutionRequest")
        self.assertEqual(executor["receipt_contract"], "AgentExecutionReceipt")
        self.assertFalse(executor["fallback_allowed"])
        self.assertEqual(
            executor["non_equivalence_notice"],
            "connectivity_lifecycle_receipt_audit_only",
        )
        self.assertEqual(executor["entrypoint"], "OPL AgentExecutionRequest -> AgentExecutionReceipt")
        self.assertEqual(executor["provider"], "custom")
        self.assertEqual(executor["api_mode"], "chat_completions")
        self.assertEqual(executor["reasoning_effort"], "xhigh")
        self.assertTrue(executor["full_agent_loop_proved"])
        self.assertEqual(executor["session_id"], "hermes-session-proof-001")
        self.assertEqual(executor["tool_call_count"], 1)
        self.assertEqual(executor["reasoning_semantics_status"], "unproven_custom_chat_completions")
        receipt = executor["agent_execution_receipt"]
        self.assertEqual(receipt["surface_kind"], "opl_agent_execution_receipt")
        self.assertEqual(receipt["executor_kind"], "hermes_agent")
        self.assertEqual(receipt["mode"], "agent_loop")
        self.assertEqual(receipt["proof"]["full_agent_loop_proved"], True)
        self.assertEqual(receipt["proof"]["tool_call_count"], 1)
        self.assertEqual(
            receipt["non_equivalence_notice"],
            "connectivity_lifecycle_receipt_audit_only",
        )
        self.assertEqual(critique_workspace["lifecycle_stage"], "critique")
        self.assertEqual(critique_workspace["current_selection"]["active_revision_plan_id"], "revision-v1")
        self.assertEqual(evidence["review_receipt_ref"], "opl_agent_execution_receipt::hermes-session-proof-001")
        self.assertEqual(validate_workspace_document(critique_workspace).ok, True)

    def test_hermes_agent_executor_requires_opl_receipt_shape(self) -> None:
        from med_autogrant.critique_executor import build_critique_execution_document
        from med_autogrant.workspace import WorkspaceStateError

        document = load_workspace_document(DRAFTING_EXAMPLE_PATH)

        def fake_opl_executor_runner(_request: dict[str, object], *, cwd: Path) -> dict[str, object]:
            self.assertEqual(cwd, DRAFTING_EXAMPLE_PATH.resolve().parent)
            return {
                "proof": {
                    "full_agent_loop_proved": True,
                    "session_id": "hermes-session-proof-001",
                    "tool_call_count": 1,
                },
                "executor_contract": {
                    "entrypoint": "OPL AgentExecutionRequest -> AgentExecutionReceipt",
                    "model": "gpt-5.4",
                },
                "closeout_packet": {
                    "surface_kind": "mag_critique_closeout_packet",
                    "mentor_critique": {},
                    "revision_plan": {},
                },
            }

        with self.assertRaisesRegex(WorkspaceStateError, "surface_kind"):
            build_critique_execution_document(
                document=document,
                input_path=DRAFTING_EXAMPLE_PATH,
                executor_kind="hermes_agent",
                opl_executor_runner=fake_opl_executor_runner,
            )
