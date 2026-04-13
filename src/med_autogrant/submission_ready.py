from __future__ import annotations

from copy import deepcopy
from typing import Any


SUBMISSION_READY_PACKAGE_VERSION = 1
SUBMISSION_READY_PACKAGE_KIND = "submission_ready_package"
AUTOMATION_SCOPE = "local_submission_package"


def build_submission_ready_package_document(
    *,
    document: dict[str, Any],
    artifact_bundle: dict[str, Any],
    final_package: dict[str, Any],
    hosted_contract_bundle: dict[str, Any],
    program_id: str,
) -> dict[str, Any]:
    active_draft = _require_active_draft(document)
    funding_brief = _optional_mapping(document.get("funding_opportunity_brief"))
    mandatory_sections = _string_list(funding_brief.get("mandatory_sections")) if funding_brief else []
    draft_sections = _mapping_list(active_draft.get("sections"))
    draft_section_titles = [
        section["section_title"]
        for section in draft_sections
        if isinstance(section.get("section_title"), str) and section["section_title"].strip()
    ]
    missing_mandatory_sections = [
        section_title for section_title in mandatory_sections if section_title not in draft_section_titles
    ]

    preliminary_evidence_pack = _optional_mapping(document.get("preliminary_evidence_pack")) or {}
    evidence_items = _mapping_list(preliminary_evidence_pack.get("evidence_items"))
    evidence_items_with_gaps = [
        _nonempty_or_unknown(item.get("item_id"))
        for item in evidence_items
        if _string_list(item.get("gaps"))
    ]
    representative_outputs = _mapping_list(
        (_optional_mapping(document.get("track_record")) or {}).get("representative_outputs")
    )
    active_projects = _mapping_list((_optional_mapping(document.get("active_project_set")) or {}).get("projects"))

    freeze_manifest = _optional_mapping(final_package.get("freeze_manifest")) or {}
    checkpoint_summary = _optional_mapping(final_package.get("checkpoint_summary")) or {}
    blocking_issues = _build_blocking_issues(
        final_package=final_package,
        hosted_contract_bundle=hosted_contract_bundle,
        freeze_manifest=freeze_manifest,
        checkpoint_summary=checkpoint_summary,
        missing_mandatory_sections=missing_mandatory_sections,
        evidence_items=evidence_items,
        evidence_items_with_gaps=evidence_items_with_gaps,
        representative_outputs=representative_outputs,
        active_projects=active_projects,
    )
    submission_ready = not blocking_issues

    return {
        "package_version": SUBMISSION_READY_PACKAGE_VERSION,
        "package_kind": SUBMISSION_READY_PACKAGE_KIND,
        "grant_run_id": final_package["grant_run_id"],
        "workspace_id": final_package["workspace_id"],
        "draft_id": final_package["draft_id"],
        "program_id": program_id,
        "lifecycle_stage": final_package["lifecycle_stage"],
        "automation_scope": AUTOMATION_SCOPE,
        "readiness_verdict": "submission_ready" if submission_ready else "blocked",
        "fully_automatic": submission_ready,
        "submission_ready": submission_ready,
        "external_submission_performed": False,
        "audit_summary": {
            "checkpoint_status": checkpoint_summary.get("checkpoint_status"),
            "draft_status": freeze_manifest.get("draft_status"),
            "presubmission_frozen": bool(freeze_manifest.get("presubmission_frozen")),
            "mandatory_sections": mandatory_sections,
            "matched_mandatory_sections": [
                section_title for section_title in mandatory_sections if section_title in draft_section_titles
            ],
            "missing_mandatory_sections": missing_mandatory_sections,
            "preliminary_evidence_count": len(evidence_items),
            "unresolved_evidence_gap_count": len(evidence_items_with_gaps),
            "representative_output_count": len(representative_outputs),
            "active_project_count": len(active_projects),
            "blocking_issue_count": len(blocking_issues),
        },
        "artifact_manifest": {
            "artifact_bundle_kind": artifact_bundle.get("bundle_kind"),
            "artifact_bundle_manifest": deepcopy(artifact_bundle.get("manifest")),
            "final_package_kind": final_package.get("package_kind"),
            "final_package_manifest": deepcopy(final_package.get("freeze_manifest")),
            "hosted_contract_bundle_kind": hosted_contract_bundle.get("bundle_kind"),
            "hosted_execution_identity": deepcopy(hosted_contract_bundle.get("execution_identity")),
        },
        "submission_dossier": {
            "project_title": active_draft.get("project_title"),
            "final_draft_markdown": _build_final_draft_markdown(active_draft),
            "evidence_index": _build_evidence_index(evidence_items=evidence_items),
            "formal_checklist": _build_formal_checklist(
                mandatory_sections=mandatory_sections,
                missing_mandatory_sections=missing_mandatory_sections,
                evidence_items=evidence_items,
                evidence_items_with_gaps=evidence_items_with_gaps,
                representative_outputs=representative_outputs,
                active_projects=active_projects,
            ),
        },
        "blocking_issues": blocking_issues,
    }


def _build_blocking_issues(
    *,
    final_package: dict[str, Any],
    hosted_contract_bundle: dict[str, Any],
    freeze_manifest: dict[str, Any],
    checkpoint_summary: dict[str, Any],
    missing_mandatory_sections: list[str],
    evidence_items: list[dict[str, Any]],
    evidence_items_with_gaps: list[str],
    representative_outputs: list[dict[str, Any]],
    active_projects: list[dict[str, Any]],
) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    if final_package.get("package_kind") != "final_package":
        issues.append(_issue("invalid_final_package", "final package kind 必须为 final_package。"))
    if hosted_contract_bundle.get("bundle_kind") != "hosted_contract_bundle":
        issues.append(_issue("invalid_hosted_contract_bundle", "hosted contract bundle kind 必须为 hosted_contract_bundle。"))
    if checkpoint_summary.get("checkpoint_status") != "submission_frozen":
        issues.append(_issue("checkpoint_not_submission_frozen", "checkpoint_status 必须为 submission_frozen。"))
    if freeze_manifest.get("draft_status") != "frozen":
        issues.append(_issue("draft_not_frozen", "draft_status 必须为 frozen。"))
    if freeze_manifest.get("presubmission_frozen") is not True:
        issues.append(_issue("presubmission_gate_open", "presubmission_frozen 必须为 true。"))
    if missing_mandatory_sections:
        issues.append(
            _issue(
                "missing_mandatory_sections",
                f"缺少 funding brief 要求的必备章节: {', '.join(missing_mandatory_sections)}。",
            )
        )
    if not evidence_items:
        issues.append(_issue("missing_preliminary_evidence", "缺少预实验 / 研究基础 evidence items。"))
    if evidence_items_with_gaps:
        issues.append(
            _issue(
                "unresolved_preliminary_evidence_gaps",
                f"仍有预实验 evidence gaps 未关闭: {', '.join(evidence_items_with_gaps)}。",
            )
        )
    if not representative_outputs:
        issues.append(_issue("missing_representative_outputs", "缺少代表性成果。"))
    if not active_projects:
        issues.append(_issue("missing_active_projects", "缺少在研项目或可复用研究资产。"))
    return issues


def _issue(issue_id: str, message: str) -> dict[str, str]:
    return {
        "issue_id": issue_id,
        "severity": "blocking",
        "message": message,
    }


def _build_final_draft_markdown(active_draft: dict[str, Any]) -> str:
    lines = [f"# {_nonempty_or_unknown(active_draft.get('project_title'))}", ""]
    for section in _mapping_list(active_draft.get("sections")):
        section_title = _nonempty_or_unknown(section.get("section_title"))
        section_text = _nonempty_or_unknown(section.get("text"))
        lines.extend([f"## {section_title}", "", section_text, ""])
    return "\n".join(lines).strip() + "\n"


def _build_evidence_index(*, evidence_items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    index: list[dict[str, Any]] = []
    for item in evidence_items:
        evidence = _optional_mapping(item.get("evidence")) or {}
        index.append(
            {
                "item_id": _nonempty_or_unknown(item.get("item_id")),
                "title": _nonempty_or_unknown(item.get("title")),
                "source_type": evidence.get("source_type"),
                "supports": _string_list(item.get("supports")),
                "gaps": _string_list(item.get("gaps")),
            }
        )
    return index


def _build_formal_checklist(
    *,
    mandatory_sections: list[str],
    missing_mandatory_sections: list[str],
    evidence_items: list[dict[str, Any]],
    evidence_items_with_gaps: list[str],
    representative_outputs: list[dict[str, Any]],
    active_projects: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    return [
        {
            "check_id": "mandatory_sections",
            "passed": not missing_mandatory_sections,
            "detail": "所有 funding brief 必备章节均已进入正文。"
            if not missing_mandatory_sections
            else f"缺少章节: {', '.join(missing_mandatory_sections)}。",
        },
        {
            "check_id": "preliminary_evidence",
            "passed": bool(evidence_items) and not evidence_items_with_gaps,
            "detail": "预实验 / 研究基础 evidence items 已存在且无未关闭 gaps。"
            if bool(evidence_items) and not evidence_items_with_gaps
            else "预实验 evidence 缺失或仍有未关闭 gaps。",
        },
        {
            "check_id": "representative_outputs",
            "passed": bool(representative_outputs),
            "detail": "代表性成果已绑定。" if representative_outputs else "缺少代表性成果。",
        },
        {
            "check_id": "active_projects",
            "passed": bool(active_projects),
            "detail": "在研项目 / 可复用资产已绑定。" if active_projects else "缺少在研项目或可复用资产。",
        },
    ]


def _require_active_draft(document: dict[str, Any]) -> dict[str, Any]:
    selection = _optional_mapping(document.get("current_selection")) or {}
    active_draft_id = selection.get("active_draft_id")
    drafts = _mapping_list(document.get("application_drafts"))
    for draft in drafts:
        if draft.get("draft_id") == active_draft_id:
            return draft
    if drafts:
        return drafts[-1]
    raise KeyError("submission ready package 需要 active draft。")


def _mapping_list(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]


def _optional_mapping(value: Any) -> dict[str, Any] | None:
    return value if isinstance(value, dict) else None


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str) and item.strip()]


def _nonempty_or_unknown(value: Any) -> str:
    if isinstance(value, str) and value.strip():
        return value.strip()
    return "unknown"
