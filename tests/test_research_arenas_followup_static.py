import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "sales_engagement_intelligence" / "sales_engagement_and_intelligence"


def load(path):
    return json.loads((APP / path).read_text())


def field(doc, name):
    return next(item for item in doc["fields"] if item["fieldname"] == name)


def test_research_arena_has_editable_playbook_table():
    arena = load("doctype/sei_research_arena/sei_research_arena.json")
    assigned = field(arena, "assigned_playbooks")
    assert assigned["options"] == "SEI Research Arena Playbook"
    child = load("doctype/sei_research_arena_playbook/sei_research_arena_playbook.json")
    assert field(child, "playbook")["options"] == "SEI Playbook"


def test_playbook_arena_tables_are_bidirectionally_synchronized():
    source = (APP / "services/playbook_arena_sync.py").read_text()
    assert "def sync_from_playbook" in source
    assert "def sync_from_arena" in source
    assert 'SYNC_FLAG = "sei_syncing_playbook_arenas"' in source
    assert "def validate_playbook_relationships" in source
    assert "def validate_arena_relationships" in source


def test_no_runtime_thesis_arena_implementation_remains():
    assert not (APP / "services/thesis_arena_sync.py").exists()
    assert not (APP / "doctype/sei_research_arena_thesis").exists()
