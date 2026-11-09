from __future__ import annotations

import argparse
from dataclasses import dataclass
from typing import Any

from med_autogrant.domain_entry import dispatch_domain_request
from med_autogrant.domain_entry_catalog import SERVICE_SAFE_DOMAIN_COMMANDS
from med_autogrant.product_entry_parts.domain_handler import build_domain_handler_export
from med_autogrant.product_entry_parts.domain_handler_dispatch import dispatch_domain_handler_task
from med_autogrant.product_entry_parts.domain_memory_runtime import (
    build_domain_memory_writeback_decision,
    build_domain_memory_writeback_proposal,
    export_framework_knowledge_writeback_proposal,
    write_domain_memory_receipt_evidence,
)
from med_autogrant.product_entry_parts.owner_receipt_writers import (
    write_owner_receipt_evidence,
)


@dataclass(frozen=True)
class DirectCommandSpec:
    help_text: str
    required_fields: tuple[str, ...] = ()
    optional_fields: tuple[str, ...] = ()


DIRECT_CLI_COMMANDS: dict[str, DirectCommandSpec] = {
    "domain-handler-export": DirectCommandSpec(
        "导出 OPL standard domain handler refs surface。",
        ("input_path",),
    ),
    "domain-handler-dispatch": DirectCommandSpec(
        "执行 OPL standard domain handler guarded action。",
        ("task_path",),
    ),
    "product-domain-memory-proposal": DirectCommandSpec(
        "生成 MAG-owned domain memory writeback proposal projection。",
        ("input_path", "workspace_root", "project_root", "stage_id", "source_ref", "lesson_summary",
         "knowledge_id", "scope_kind", "scope_id", "content_kind", "evidence_class", "review_requirement"),
        ("proposal_id",),
    ),
    "product-domain-memory-decision": DirectCommandSpec(
        "生成 MAG-owned domain memory accept/reject decision projection。",
        ("proposal_path", "decision", "decision_reason"),
    ),
    "product-domain-memory-export": DirectCommandSpec(
        "导出已校验的 Framework 六字段 knowledge writeback proposal JSON。",
        ("proposal_path",),
    ),
    "product-domain-memory-receipt-evidence": DirectCommandSpec(
        "把 MAG-owned domain memory accept/reject decision 写成 runtime receipt evidence。",
        ("decision_payload",),
        ("runtime_root",),
    ),
    "product-owner-receipt-evidence": DirectCommandSpec(
        "把 OPL-hosted stage attempt closeout 写成 MAG owner receipt runtime evidence。",
        ("input_path", "receipt_shape", "stage_id", "source_ref", "closeout_summary"),
        ("runtime_root", "receipt_id"),
    ),
}


def dispatch_cli_command(args: argparse.Namespace) -> dict[str, Any]:
    if args.command in SERVICE_SAFE_DOMAIN_COMMANDS:
        return handle_domain_command(args)
    return handle_direct_command(args)


def handle_domain_command(args: argparse.Namespace) -> dict[str, Any]:
    spec = SERVICE_SAFE_DOMAIN_COMMANDS[args.command]
    values = vars(args)
    request: dict[str, Any] = {"command": args.command}
    for field in spec.required_fields + spec.optional_fields:
        value = values.get(field)
        if value is not None:
            request[field] = value
    return dispatch_domain_request(request)


def handle_direct_command(args: argparse.Namespace) -> dict[str, Any]:
    command = args.command
    values = vars(args)
    if command == "domain-handler-export":
        return build_domain_handler_export(input_path=values["input_path"])
    if command == "domain-handler-dispatch":
        return dispatch_domain_handler_task(task_path=values["task_path"])
    if command == "product-domain-memory-proposal":
        return build_domain_memory_writeback_proposal(
            input_path=values["input_path"],
            stage_id=values["stage_id"],
            source_ref=values["source_ref"],
            lesson_summary=values["lesson_summary"],
            knowledge_id=values["knowledge_id"],
            scope_kind=values["scope_kind"],
            scope_id=values["scope_id"],
            content_kind=values["content_kind"],
            evidence_class=values["evidence_class"],
            review_requirement=values["review_requirement"],
            workspace_root=values["workspace_root"],
            project_root=values["project_root"],
            proposal_id=values.get("proposal_id"),
        )
    if command == "product-domain-memory-decision":
        return build_domain_memory_writeback_decision(
            proposal_path=values["proposal_path"],
            decision=values["decision"],
            decision_reason=values["decision_reason"],
        )
    if command == "product-domain-memory-export":
        return export_framework_knowledge_writeback_proposal(proposal_path=values["proposal_path"])
    if command == "product-domain-memory-receipt-evidence":
        return write_domain_memory_receipt_evidence(
            decision_payload=values["decision_payload"],
            runtime_root=values.get("runtime_root"),
        )
    if command == "product-owner-receipt-evidence":
        return write_owner_receipt_evidence(
            input_path=values["input_path"],
            receipt_shape=values["receipt_shape"],
            stage_id=values["stage_id"],
            source_ref=values["source_ref"],
            closeout_summary=values["closeout_summary"],
            runtime_root=values.get("runtime_root"),
            receipt_id=values.get("receipt_id"),
        )
    raise ValueError(f"unsupported direct CLI command: {command}")
