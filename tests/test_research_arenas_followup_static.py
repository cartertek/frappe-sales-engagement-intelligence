from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "sales_engagement_intelligence" / "sales_engagement_and_intelligence"


def load_doctype(path: str) -> dict:
    return json.loads((APP / path).read_text())


def field(doc: dict, fieldname: str) -> dict | None:
    return next((row for row in doc["fields"] if row.get("fieldname") == fieldname), None)


def test_prospect_has_queryable_arena_snapshot():
    prospect = load_doctype("doctype/sei_prospect/sei_prospect.json")
    arenas = field(prospect, "arenas")
    assert arenas is not None
    assert arenas["fieldtype"] == "Data"
    assert arenas["read_only"] == 1
    assert arenas["in_standard_filter"] == 1

    sync = (APP / "services/prospect_signal_type_sync.py").read_text()
    assert '"arenas": ", ".join(arenas)' in sync
    signal = (APP / "doctype/sei_signal/sei_signal.py").read_text()
    assert "sync_prospect_signal_types" in signal


def test_research_arena_has_editable_thesis_table():
    arena = load_doctype("doctype/sei_research_arena/sei_research_arena.json")
    assigned = field(arena, "assigned_theses")
    assert assigned is not None
    assert assigned["fieldtype"] == "Table"
    assert assigned["options"] == "SEI Research Arena Thesis"

    child = load_doctype("doctype/sei_research_arena_thesis/sei_research_arena_thesis.json")
    assert child["istable"] == 1
    assert field(child, "thesis")["options"] == "SEI Thesis"


def test_thesis_arena_tables_are_bidirectionally_synchronized():
    source = (APP / "services/thesis_arena_sync.py").read_text()
    assert "def sync_from_thesis" in source
    assert "def sync_from_arena" in source
    assert 'SYNC_FLAG = "sei_syncing_thesis_arenas"' in source
    assert "def validate_thesis_relationships" in source
    assert "def validate_arena_relationships" in source


def test_signal_type_error_uses_thesis_assigned_to_arena_language():
    source = (APP / "doctype/sei_signal_type/sei_signal_type.py").read_text()
    assert "Thesis {self.thesis} is not assigned to Research Arena {self.research_arena}." in source
    assert "Research Arena {self.research_arena} is not assigned to Thesis" not in source


def test_prospecting_sidebar_links_research_arenas():
    sidebar = json.loads(
        (ROOT / "sales_engagement_intelligence" / "workspace_sidebar" / "prospecting.json").read_text()
    )
    assert any(item.get("link_to") == "SEI Research Arena" for item in sidebar["items"])
