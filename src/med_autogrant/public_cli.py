from __future__ import annotations

from typing import Final


PUBLIC_COMMAND_GROUP_SUMMARIES: Final[dict[str, str]] = {
    "workspace": "工作区诊断、摘要、阶段路由与 progress cockpit。",
    "mainline": "当前 line/current focus 概览与维护者参考记录。",
    "product": "grant direct entry、frontdesk 与 product-entry contract。",
    "runtime": "Hermes substrate 探测与本地 runtime 运行/恢复。",
    "pass": "authoring pass 执行入口。",
    "package": "artifact/final/hosted/submission package 导出入口。",
}

PUBLIC_COMMAND_ORDER: Final[tuple[str, ...]] = (
    "workspace",
    "mainline",
    "product",
    "runtime",
    "pass",
    "package",
)

INTERNAL_TO_PUBLIC_COMMAND: Final[dict[str, tuple[str, str]]] = {
    "validate-workspace": ("workspace", "validate"),
    "summarize-workspace": ("workspace", "summarize"),
    "next-step": ("workspace", "next-step"),
    "critique-summary": ("workspace", "critique-summary"),
    "stage-route-report": ("workspace", "route-report"),
    "grant-progress": ("workspace", "progress"),
    "grant-cockpit": ("workspace", "cockpit"),
    "mainline-status": ("mainline", "status"),
    "mainline-phase": ("mainline", "phase"),
    "grant-direct-entry": ("product", "direct-entry"),
    "grant-user-loop": ("product", "user-loop"),
    "product-entry-manifest": ("product", "manifest"),
    "product-frontdesk": ("product", "frontdesk"),
    "product-preflight": ("product", "preflight"),
    "product-start": ("product", "start"),
    "build-product-entry": ("product", "build-entry"),
    "probe-upstream-hermes": ("runtime", "probe-hermes"),
    "runtime-run": ("runtime", "run"),
    "runtime-resume": ("runtime", "resume"),
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

PUBLIC_TO_INTERNAL_COMMAND: Final[dict[tuple[str, str], str]] = {
    value: key for key, value in INTERNAL_TO_PUBLIC_COMMAND.items()
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
    resolved = list(argv)
    if len(resolved) >= 1:
        command = resolved[0]
        if command in INTERNAL_TO_PUBLIC_COMMAND:
            group, subcommand = INTERNAL_TO_PUBLIC_COMMAND[command]
            return [group, subcommand, *resolved[1:]]
    return resolved
