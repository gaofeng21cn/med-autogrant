from __future__ import annotations

from med_autogrant.workspace_index import _index_objects
from med_autogrant.workspace_types import ValidationIssue


def test_index_objects_reports_duplicate_keys() -> None:
    issues: list[ValidationIssue] = []

    indexed = _index_objects(
        [{"item_id": "a"}, {"item_id": "a"}],
        "item_id",
        "items",
        issues,
    )

    assert indexed == {"a": {"item_id": "a"}}
    assert [(issue.path, issue.message) for issue in issues] == [("items[1].item_id", "item_id 不能重复。")]
