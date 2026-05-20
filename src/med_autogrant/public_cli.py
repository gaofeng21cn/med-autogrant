from __future__ import annotations

from typing import Final


PUBLIC_COMMAND_GROUP_SUMMARIES: Final[dict[str, str]] = {
    "workspace": "工作区诊断、摘要、阶段路由与 progress cockpit。",
    "mainline": "当前 line/current focus 概览与维护者参考记录。",
    "product": "OPL-hosted caller 可消费的 MAG domain handler refs 与 authority contract。",
    "pass": "authoring pass 执行入口。",
    "package": "artifact/final/hosted/submission package 导出入口。",
}

PUBLIC_COMMAND_ORDER: Final[tuple[str, ...]] = (
    "workspace",
    "mainline",
    "product",
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
    "grant-progress": ("workspace", "progress"),
    "grant-cockpit": ("workspace", "cockpit"),
    "mainline-status": ("mainline", "status"),
    "mainline-phase": ("mainline", "phase"),
    "grant-direct-entry": ("product", "direct-entry"),
    "grant-user-loop": ("product", "user-loop"),
    "skill-catalog": ("product", "skill-catalog"),
    "product-entry-manifest": ("product", "manifest"),
    "product-status": ("product", "status"),
    "product-preflight": ("product", "preflight"),
    "product-start": ("product", "start"),
    "build-product-entry": ("product", "build-entry"),
    "product-sidecar-export": ("product", "sidecar-export"),
    "product-sidecar-dispatch": ("product", "sidecar-dispatch"),
    "product-domain-memory-proposal": ("product", "domain-memory-proposal"),
    "product-domain-memory-decision": ("product", "domain-memory-decision"),
    "product-domain-memory-receipt-evidence": ("product", "domain-memory-receipt-evidence"),
    "product-owner-receipt-evidence": ("product", "owner-receipt-evidence"),
    "product-lifecycle-receipt-evidence": ("product", "lifecycle-receipt-evidence"),
    "controlled-soak-receipt-reconciliation-proof": ("product", "receipt-reconciliation-proof"),
    "controlled-soak-receipt-reconciliation-inventory": (
        "product",
        "receipt-reconciliation-inventory",
    ),
    "focused-hosted-receipt-verification": ("product", "hosted-receipt-verification"),
    "lifecycle-receipt-bundle": ("product", "lifecycle-receipt-bundle"),
    "memory-receipt-projection": ("product", "memory-receipt-projection"),
    "package-lifecycle-handoff": ("product", "package-lifecycle-handoff"),
    "continuous-receipt-reconciliation": ("product", "continuous-receipt-reconciliation"),
    "production-live-acceptance-receipt": ("product", "production-live-acceptance-receipt"),
    "codex-stage-receipts": ("product", "codex-stage-receipts"),
    "operator-closeout-readiness": ("product", "operator-closeout-readiness"),
    "physical-morphology-guard": ("product", "physical-morphology-guard"),
    "executor-first-closeout-bundle": ("product", "executor-first-closeout-bundle"),
    "execute-direction-screening-pass": ("pass", "direction-screening"),
    "execute-question-refinement-pass": ("pass", "question-refinement"),
    "execute-argument-building-pass": ("pass", "argument-building"),
    "execute-fit-alignment-pass": ("pass", "fit-alignment"),
    "execute-outline-pass": ("pass", "outline"),
    "execute-drafting-pass": ("pass", "drafting"),
    "execute-critique-pass": ("pass", "critique"),
    "execute-critique-revision-loop": ("pass", "critique-loop"),
    "execute-authoring-mainline-loop": ("pass", "mainline-loop"),
    "execute-grant-autonomy-controller": ("pass", "autonomy-controller"),
    "execute-revision-pass": ("pass", "revision"),
    "execute-freeze-pass": ("pass", "freeze"),
    "build-artifact-bundle": ("package", "artifact-bundle"),
    "build-final-package": ("package", "final-package"),
    "build-hosted-contract-bundle": ("package", "hosted-contract-bundle"),
    "build-submission-ready-package": ("package", "submission-ready"),
}

PUBLIC_TO_INTERNAL_COMMAND: Final[dict[tuple[str, str], str]] = {
    value: key for key, value in INTERNAL_TO_PUBLIC_COMMAND.items()
}

PUBLIC_THREE_TOKEN_COMMANDS: Final[dict[tuple[str, str, str], str]] = {
    ("product", "sidecar", "export"): "product-sidecar-export",
    ("product", "sidecar", "dispatch"): "product-sidecar-dispatch",
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
    tokens = public_command_tokens(command)
    if tokens is None:
        return command
    return " ".join(tokens)


def public_cli_command(command: str, *args: str) -> str:
    tokens = public_command_tokens(command)
    command_words = list(tokens) if tokens is not None else [command]
    return " ".join(["uv", "run", "python", "-m", "med_autogrant", *command_words, *args])


def public_cli_argv(argv: list[str] | tuple[str, ...]) -> list[str]:
    return list(argv)
