from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "v1"
SCHEMA_ROOT = Path(__file__).resolve().parents[2] / "schemas" / SCHEMA_VERSION


@dataclass
class SchemaStore:
    root: Path = SCHEMA_ROOT

    def load_json(self, file_name: str) -> dict[str, Any]:
        path = self.root / file_name
        return json.loads(path.read_text(encoding="utf-8"))

    def load_schema_index(self) -> dict[str, Any]:
        return self.load_json("schema-index.json")

    def load_aggregate_root_schema(self) -> dict[str, Any]:
        index = self.load_schema_index()
        aggregate_root = index["aggregate_root"]
        return self.load_json(aggregate_root)


def load_schema_index() -> dict[str, Any]:
    return SchemaStore().load_schema_index()


def load_aggregate_root_schema() -> dict[str, Any]:
    return SchemaStore().load_aggregate_root_schema()
