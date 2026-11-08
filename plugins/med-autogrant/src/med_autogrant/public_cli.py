from __future__ import annotations

from typing import Final


PUBLIC_COMMAND_GROUP_SUMMARIES: Final[dict[str, str]] = {
    "workspace": "工作区诊断、摘要、阶段路由与 grant quality refs。",
    "domain-handler": "OPL standard domain handler target：export refs 与 dispatch guarded actions。",
    "authority": "MAG-owned memory、receipt、typed-blocker 与 closeout authority targets。",
    "pass": "authoring pass 执行入口。",
    "package": "artifact/final/hosted/submission package 导出入口。",
}

PUBLIC_COMMAND_ORDER: Final[tuple[str, ...]] = (
    "workspace",
    "domain-handler",
    "authority",
    "pass",
    "package",
)

INTERNAL_TO_PUBLIC_COMMAND: Final[dict[str, tuple[str, str]]] = {
    "validate-workspace": ("workspace", "validate"),
    "summarize-workspace": ("workspace", "summarize"),
    "grant-intake-audit": ("workspace", "intake-audit"),
    "grant-evidence-grounding": ("workspace", "evidence-grounding"),
    "grant-quality-scorecard": ("workspace", "quality-scorecard"),
    "grant-quality-closure-dossier": ("workspace", "quality-closure-dossier"),
    "grant-quality-diff": ("workspace", "quality-diff"),
    "discover-funding-opportunities": ("workspace", "discover-funding"),
    "refresh-funding-opportunities-cache": ("workspace", "refresh-funding-cache"),
    "select-project-profile": ("workspace", "select-profile"),
    "initialize-intake-workspace": ("workspace", "initialize-intake"),
    "next-step": ("workspace", "next-step"),
    "critique-summary": ("workspace", "critique-summary"),
    "stage-route-report": ("workspace", "route-report"),
    "domain-handler-export": ("domain-handler", "export"),
    "domain-handler-dispatch": ("domain-handler", "dispatch"),
    "product-domain-memory-proposal": ("authority", "memory-proposal"),
    "product-domain-memory-decision": ("authority", "memory-decision"),
    "product-domain-memory-receipt-evidence": ("authority", "memory-receipt-evidence"),
    "product-owner-receipt-evidence": ("authority", "owner-receipt-evidence"),
    "execute-strategy-authoring-pass": ("pass", "strategy-authoring"),
    "execute-direction-screening-pass": ("pass", "direction-screening"),
    "execute-question-refinement-pass": ("pass", "question-refinement"),
    "execute-argument-building-pass": ("pass", "argument-building"),
    "execute-fit-alignment-pass": ("pass", "fit-alignment"),
    "execute-outline-pass": ("pass", "outline"),
    "execute-drafting-pass": ("pass", "drafting"),
    "execute-critique-pass": ("pass", "critique"),
    "execute-revision-pass": ("pass", "revision"),
    "execute-freeze-pass": ("pass", "freeze"),
    "build-artifact-bundle": ("package", "artifact-bundle"),
    "build-final-package": ("package", "final-package"),
    "build-hosted-contract-bundle": ("package", "hosted-contract-bundle"),
    "build-submission-ready-package": ("package", "submission-ready"),
}

GENERATED_SURFACE_COMMAND_REFS: Final[dict[str, str]] = {
    "product-entry-manifest": "opl://generated-surfaces/mag/product-entry-manifest",
    "product-status": "opl://generated-surfaces/mag/product-status",
    "build-product-entry": "opl://generated-surfaces/mag/product-entry-session",
}

PUBLIC_GROUP_COMMANDS: Final[dict[str, tuple[str, ...]]] = {
    group: tuple(
        subcommand
        for _, (candidate_group, subcommand) in INTERNAL_TO_PUBLIC_COMMAND.items()
        if candidate_group == group
    )
    for group in PUBLIC_COMMAND_ORDER
}


def public_command_tokens(command: str) -> tuple[str, str] | None:
    return INTERNAL_TO_PUBLIC_COMMAND.get(command)


def public_command_label(command: str) -> str:
    generated_ref = GENERATED_SURFACE_COMMAND_REFS.get(command)
    if generated_ref is not None:
        return generated_ref
    tokens = public_command_tokens(command)
    if tokens is None:
        return command
    return " ".join(tokens)
