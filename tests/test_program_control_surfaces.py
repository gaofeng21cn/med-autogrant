from __future__ import annotations

import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CURRENT_PROGRAM = REPO_ROOT / ".omx" / "context" / "CURRENT_PROGRAM.md"
PROGRAM_ROUTING = REPO_ROOT / ".omx" / "context" / "PROGRAM_ROUTING.md"
TEAM_PROMPT = REPO_ROOT / ".omx" / "context" / "OMX_TEAM_PROMPT.md"
EXECUTION_PROMPT = REPO_ROOT / ".omx" / "context" / "OMX_EXECUTION_PROMPT.md"
OMX_BRIDGE = REPO_ROOT / "docs" / "specs" / "2026-04-06-med-autogrant-mainline-and-omx-bridge.md"
PRD = REPO_ROOT / ".omx" / "plans" / "prd-med-autogrant-mainline.md"
TEST_SPEC = REPO_ROOT / ".omx" / "plans" / "test-spec-med-autogrant-mainline.md"
IMPLEMENTATION = REPO_ROOT / ".omx" / "plans" / "implementation-med-autogrant-mainline.md"
PROGRAM_OPERATING_MODEL = REPO_ROOT / ".omx" / "plans" / "spec-program-operating-model.md"
REPORT_DIR = REPO_ROOT / ".omx" / "reports" / "med-autogrant-mainline"
LATEST_STATUS = REPORT_DIR / "LATEST_STATUS.md"
ITERATION_LOG = REPORT_DIR / "ITERATION_LOG.md"
OPEN_ISSUES = REPORT_DIR / "OPEN_ISSUES.md"
REPORT_README = REPORT_DIR / "README.md"

REQUIRED_COMMAND_SNIPPETS = (
    "python3 -m unittest discover -s tests -p 'test_*.py'",
    "PYTHONPATH=src python3 -m med_autogrant validate-workspace --input examples/nsfc_workspace_minimal.json --format json",
    "PYTHONPATH=src python3 -m med_autogrant summarize-workspace --input examples/nsfc_workspace_minimal.json --format json",
    "PYTHONPATH=src python3 -m med_autogrant next-step --input examples/nsfc_workspace_minimal.json --format json",
    "PYTHONPATH=src python3 -m med_autogrant critique-summary --input examples/nsfc_workspace_minimal.json --format json",
    "PYTHONPATH=src python3 -m med_autogrant stage-route-report --input examples/nsfc_workspace_minimal.json --format json",
    "python3 /Users/gaofeng/workspace/omx-project-installer/skills/omx-project-installer/scripts/omx_project_installer.py diff --target /Users/gaofeng/workspace/med-autogrant",
    "git diff --check",
)

FUTURE_TRANCHE_SNIPPETS = (
    "P2.A / Intake-Direction-Question Mainline",
    "P2.B / Argument-Fit-Outline Mainline",
    "P2.C / Draft-Critique-Revision Skeleton",
    "P3.A / Mentor Verdict Contract Freeze",
    "P3.B / Revision Transition And Re-Review Hardening",
    "P3.C / Forced Rollback And Presubmission Gate",
    "P4.A / Dual-Mode Gate Surface",
    "P4.B / Verification OS And Checkpoint Surface",
    "P5.A / Second Grant Family Onboarding",
    "P5.B / Federation Contract Freeze",
)

REVISION_TRANSITION_SNIPPETS = (
    "RevisionPlan.execution_status",
    "pre_revision_version_label",
    "post_revision_version_label",
    "comparison_summary",
    "draft_id",
    "frozen_question_id",
)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def extract_phase_pointer(document: str) -> tuple[str, str]:
    match = re.search(
        r"## Current Phase\s+\s*-\s+`([^`]+)`\s+\s*-\s+当前唯一活跃子线：`([^`]+)`",
        document,
        re.MULTILINE,
    )
    if match is None:
        raise AssertionError("CURRENT_PROGRAM.md 缺少可解析的 Current Phase 段落。")
    return match.group(1), match.group(2)


def extract_truth_sources(document: str) -> list[Path]:
    match = re.search(r"## Governing Truth Sources\s+(.+?)\n## ", document, re.MULTILINE | re.DOTALL)
    if match is None:
        raise AssertionError("CURRENT_PROGRAM.md 缺少 Governing Truth Sources 段落。")

    paths: list[Path] = []
    for raw_line in match.group(1).splitlines():
        line = raw_line.strip()
        if not line.startswith("- "):
            continue
        value = line[2:].strip().strip("`")
        paths.append(Path(value))
    return paths


def extract_section(document: str, title: str) -> list[str]:
    match = re.search(rf"## {re.escape(title)}\n\n(.+?)(?:\n## |\Z)", document, re.MULTILINE | re.DOTALL)
    if match is None:
        raise AssertionError(f"OPEN_ISSUES.md 缺少 {title} 段落。")
    return [line.strip() for line in match.group(1).splitlines() if line.strip().startswith("- ")]


class ProgramControlSurfaceTest(unittest.TestCase):
    def test_current_program_truth_sources_exist(self) -> None:
        document = read_text(CURRENT_PROGRAM)
        for path in extract_truth_sources(document):
            with self.subTest(path=str(path)):
                self.assertTrue(path.exists(), f"truth source 不存在: {path}")

    def test_active_pointer_is_repeated_across_control_surfaces(self) -> None:
        current_program = read_text(CURRENT_PROGRAM)
        phase, tranche = extract_phase_pointer(current_program)

        for path in (
            TEAM_PROMPT,
            EXECUTION_PROMPT,
            OMX_BRIDGE,
            PRD,
            TEST_SPEC,
            IMPLEMENTATION,
            LATEST_STATUS,
            ITERATION_LOG,
            OPEN_ISSUES,
        ):
            with self.subTest(path=path.name):
                text = read_text(path)
                self.assertIn(phase, text, f"{path.name} 缺少当前 phase 指针")
                self.assertIn(tranche, text, f"{path.name} 缺少当前 tranche 指针")

    def test_required_control_surfaces_exist(self) -> None:
        for path in (
            CURRENT_PROGRAM,
            PROGRAM_ROUTING,
            TEAM_PROMPT,
            EXECUTION_PROMPT,
            PROGRAM_OPERATING_MODEL,
            PRD,
            TEST_SPEC,
            IMPLEMENTATION,
            REPORT_README,
            LATEST_STATUS,
            ITERATION_LOG,
            OPEN_ISSUES,
        ):
            with self.subTest(path=path.name):
                self.assertTrue(path.exists(), f"control surface 不存在: {path}")

    def test_execution_entry_and_test_spec_share_required_commands(self) -> None:
        execution_prompt_text = read_text(EXECUTION_PROMPT)
        test_spec_text = read_text(TEST_SPEC)
        latest_status_text = read_text(LATEST_STATUS)

        for snippet in REQUIRED_COMMAND_SNIPPETS:
            with self.subTest(command=snippet):
                self.assertIn(snippet, execution_prompt_text)
                self.assertIn(snippet, test_spec_text)

        self.assertIn("Verification Snapshot", latest_status_text)
        for keyword in ("validate-workspace", "summarize-workspace", "next-step", "critique-summary"):
            with self.subTest(keyword=keyword):
                self.assertIn(keyword, latest_status_text)

    def test_report_surface_documents_required_files_and_sync_rule(self) -> None:
        report_text = read_text(REPORT_README)
        for required_name in ("LATEST_STATUS.md", "ITERATION_LOG.md", "OPEN_ISSUES.md"):
            with self.subTest(file=required_name):
                self.assertIn(required_name, report_text)
                self.assertTrue((REPORT_DIR / required_name).exists())

        self.assertIn("current pointer", report_text.lower())
        self.assertIn("promotion", report_text.lower())

    def test_open_issues_blockers_section_only_contains_active_blockers(self) -> None:
        blockers = extract_section(read_text(OPEN_ISSUES), "blockers")
        self.assertTrue(blockers, "OPEN_ISSUES.md 的 blockers 段落不能为空。")

        if len(blockers) == 1 and "无 active blocker" in blockers[0]:
            return

        rejected_markers = ("无硬 blocker", "无新增 blocker", "已修复", "已将")
        for line in blockers:
            with self.subTest(line=line):
                self.assertFalse(any(marker in line for marker in rejected_markers), "blockers 段落只能保留当前 active blocker。")
                self.assertTrue(
                    any(keyword in line for keyword in ("P1.B", "promotion", "revision", "tranche", "phase boundary")),
                    "blockers 段落必须只记录与当前 pointer 或 promotion 直接相关的 active blocker。",
                )

    def test_future_tranche_map_and_same_phase_autopromotion_are_frozen(self) -> None:
        current_program_text = read_text(CURRENT_PROGRAM)
        prd_text = read_text(PRD)
        implementation_text = read_text(IMPLEMENTATION)
        bridge_text = read_text(OMX_BRIDGE)

        for snippet in FUTURE_TRANCHE_SNIPPETS:
            for path, text in (
                (CURRENT_PROGRAM, current_program_text),
                (PRD, prd_text),
                (IMPLEMENTATION, implementation_text),
                (OMX_BRIDGE, bridge_text),
            ):
                with self.subTest(path=path.name, snippet=snippet):
                    self.assertIn(snippet, text)

        for path in (CURRENT_PROGRAM, PROGRAM_OPERATING_MODEL, PRD, TEST_SPEC, IMPLEMENTATION, OMX_BRIDGE):
            with self.subTest(path=path.name):
                self.assertIn("same-phase auto-promotion", read_text(path))

    def test_revision_transition_contract_is_frozen_in_active_truth_surfaces(self) -> None:
        for path in (OMX_BRIDGE, PRD, TEST_SPEC, IMPLEMENTATION):
            text = read_text(path)
            for snippet in REVISION_TRANSITION_SNIPPETS:
                with self.subTest(path=path.name, snippet=snippet):
                    self.assertIn(snippet, text)


if __name__ == "__main__":
    unittest.main()
