from __future__ import annotations

from med_autogrant.grant_autonomy_common import (
    _CONTROLLER_ACTIONS,
    _CONTROLLER_STATUSES,
    _GATE_STATUSES,
    _QUALITY_STATUSES,
    _dedupe,
    _extract_mapping,
    _normalized_string,
    _string_list,
)


def test_common_status_and_action_sets_cover_controller_protocol() -> None:
    assert _CONTROLLER_STATUSES == {
        "submission_grade_candidate",
        "near_submission_candidate",
        "failed_closed",
    }
    assert _QUALITY_STATUSES == {
        "submission_grade_candidate",
        "near_submission_candidate",
        "not_ready",
    }
    assert _CONTROLLER_ACTIONS == {
        "continue_mainline",
        "stop_success",
        "rollback_upstream",
        "reselect_project_profile",
        "fail_closed",
    }
    assert _GATE_STATUSES == {
        "open",
        "passed",
        "blocked",
        "failed_closed",
    }


def test_common_string_helpers_trim_and_fail_closed_on_invalid_items() -> None:
    assert _normalized_string("  near_submission_candidate  ") == "near_submission_candidate"
    assert _normalized_string(123) == ""
    assert _string_list([" blocker ", "evidence gap"]) == ["blocker", "evidence gap"]
    assert _string_list(["valid", "  "]) is None
    assert _string_list(("valid",)) is None


def test_dedupe_preserves_first_seen_order() -> None:
    assert _dedupe(["a", "b", "a", "c", "b"]) == ["a", "b", "c"]


def test_extract_mapping_returns_deepcopy_for_preferred_mapping_or_payload() -> None:
    payload = {"workspace": {"workspace_id": "ws-001", "nested": {"stage": "drafting"}}}

    extracted = _extract_mapping(payload, preferred_keys=("workspace",))
    assert extracted == {"workspace_id": "ws-001", "nested": {"stage": "drafting"}}
    assert extracted is not payload["workspace"]
    extracted["nested"]["stage"] = "changed"
    assert payload["workspace"]["nested"]["stage"] == "drafting"

    assert _extract_mapping({"workspace": "invalid"}, preferred_keys=("workspace",)) is None
    fallback = _extract_mapping({"workspace_id": "ws-002"}, preferred_keys=("workspace",))
    assert fallback == {"workspace_id": "ws-002"}
    assert fallback is not None
