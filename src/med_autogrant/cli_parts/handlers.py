from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from med_autogrant.domain_entry_catalog import SERVICE_SAFE_DOMAIN_COMMANDS
from med_autogrant.foundry_series_cli import (
    build_foundry_series_doctor,
    build_foundry_series_inspect,
    build_foundry_series_interfaces,
    build_foundry_series_peers,
    build_foundry_series_status,
    build_foundry_series_validate,
)
from med_autogrant.product_entry_parts.domain_handler import build_domain_handler_export
from med_autogrant.product_entry_parts.domain_handler_dispatch import dispatch_domain_handler_task
from med_autogrant.product_entry_parts.domain_memory_runtime import (
    build_domain_memory_writeback_decision,
    build_domain_memory_writeback_proposal,
    write_domain_memory_receipt_evidence,
)
from med_autogrant.product_entry_parts.owner_receipt_writers import (
    write_owner_receipt_evidence,
)


@dataclass(frozen=True)
class DirectCommandSpec:
    target: Callable[..., dict[str, Any]]
    help_text: str
    required_fields: tuple[str, ...] = ()
    optional_fields: tuple[str, ...] = ()


DIRECT_CLI_COMMANDS: dict[str, DirectCommandSpec] = {
    "foundry-status": DirectCommandSpec(
        build_foundry_series_status, "输出 MAG 的 OPL Foundry Agent series 状态。"
    ),
    "foundry-inspect": DirectCommandSpec(
        build_foundry_series_inspect, "检查 MAG 的 Foundry Agent identity、输入输出与 authority profile。"
    ),
    "foundry-interfaces": DirectCommandSpec(
        build_foundry_series_interfaces, "列出 MAG 的 Foundry Agent public interface grammar。"
    ),
    "foundry-validate": DirectCommandSpec(
        build_foundry_series_validate, "校验 MAG 的 Foundry Agent series contract 与 CLI command surface。"
    ),
    "foundry-doctor": DirectCommandSpec(
        build_foundry_series_doctor, "输出 MAG 的 Foundry Agent authority/currentness diagnostic。"
    ),
    "foundry-peers": DirectCommandSpec(
        build_foundry_series_peers, "列出同系列 Foundry Agent peers 与 MAG topology profile。"
    ),
    "domain-handler-export": DirectCommandSpec(
        build_domain_handler_export,
        "导出 OPL standard domain handler refs surface。",
        ("input_path",),
    ),
    "domain-handler-dispatch": DirectCommandSpec(
        dispatch_domain_handler_task,
        "执行 OPL standard domain handler guarded action。",
        ("task_path",),
    ),
    "product-domain-memory-proposal": DirectCommandSpec(
        build_domain_memory_writeback_proposal,
        "生成 MAG-owned domain memory writeback proposal projection。",
        ("input_path", "stage_id", "source_ref", "lesson_summary"),
        ("proposal_id",),
    ),
    "product-domain-memory-decision": DirectCommandSpec(
        build_domain_memory_writeback_decision,
        "生成 MAG-owned domain memory accept/reject decision projection。",
        ("proposal_path", "decision", "decision_reason"),
        ("memory_id",),
    ),
    "product-domain-memory-receipt-evidence": DirectCommandSpec(
        write_domain_memory_receipt_evidence,
        "把 MAG-owned domain memory accept/reject decision 写成 runtime receipt evidence。",
        ("decision_payload",),
        ("runtime_root",),
    ),
    "product-owner-receipt-evidence": DirectCommandSpec(
        write_owner_receipt_evidence,
        "把 OPL-hosted stage attempt closeout 写成 MAG owner receipt runtime evidence。",
        ("input_path", "receipt_shape", "stage_id", "source_ref", "closeout_summary"),
        ("runtime_root", "receipt_id"),
    ),
}

def handle_domain_command(args: argparse.Namespace) -> dict[str, Any]:
    spec = SERVICE_SAFE_DOMAIN_COMMANDS[args.command]
    request: dict[str, Any] = {"command": args.command}
    for field in spec.required_fields + spec.optional_fields:
        value = getattr(args, field)
        if field == "opl_stage_attempt":
            value = _read_json_object(value)
        if value is not None:
            request[field] = value
    return _domain_entry().dispatch(request)


def handle_direct_command(args: argparse.Namespace) -> dict[str, Any]:
    spec = DIRECT_CLI_COMMANDS[args.command]
    return spec.target(
        **{
            field: getattr(args, field)
            for field in spec.required_fields + spec.optional_fields
        }
    )


def _domain_entry() -> Any:
    from med_autogrant import domain_entry

    return domain_entry.MedAutoGrantDomainEntry()


def _read_json_object(path: str) -> dict[str, Any]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Expected JSON object at {path}.")
    return payload
