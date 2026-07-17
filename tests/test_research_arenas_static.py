import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DT = ROOT / "sales_engagement_intelligence" / "sales_engagement_and_intelligence" / "doctype"


def load(name):
    return json.loads((DT / name / f"{name}.json").read_text())


def field(doc, name):
    return next(item for item in doc["fields"] if item["fieldname"] == name)


def test_research_arena_is_first_class_doctype():
    arena = load("sei_research_arena")
    assert arena["name"] == "SEI Research Arena"
    assert field(arena, "arena_name")["unique"] == 1
    assert field(arena, "active")["default"] == 1


def test_thesis_has_many_to_many_arena_child_table():
    thesis = load("sei_thesis")
    assert field(thesis, "research_arenas")["options"] == "SEI Thesis Research Arena"
    child = load("sei_thesis_research_arena")
    assert child["istable"] == 1
    assert field(child, "research_arena")["options"] == "SEI Research Arena"


def test_signal_requires_one_arena_and_signal_type_has_active_state():
    signal = load("sei_signal")
    arena = field(signal, "research_arena")
    assert arena["options"] == "SEI Research Arena"
    assert arena["reqd"] == 1
    signal_type = load("sei_signal_type")
    assert field(signal_type, "active")["default"] == 1


def test_server_validation_enforces_taxonomy_and_inactive_type_on_create():
    source = (DT / "sei_signal" / "sei_signal.py").read_text()
    assert "self.is_new() and not signal_type.active" in source
    assert '"SEI Thesis Research Arena"' in source
    assert "is not assigned to Thesis" in source


def test_migration_backfills_pre_feature_signals():
    patch = (ROOT / "sales_engagement_intelligence" / "patches" / "v0_0_1" / "backfill_research_arenas.py").read_text()
    assert 'LEGACY_ARENA = "Legacy / Unclassified"' in patch
    assert "UPDATE `tabSEI Signal`" in patch
    assert 'thesis.append("research_arenas"' in patch
