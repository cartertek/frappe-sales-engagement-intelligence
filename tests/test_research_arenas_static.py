import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DT = ROOT / "sales_engagement_intelligence" / "sales_engagement_and_intelligence" / "doctype"


def load(name):
    return json.loads((DT / name / f"{name}.json").read_text())


def field(doc, name):
    return next((item for item in doc["fields"] if item["fieldname"] == name), None)


def test_research_arena_is_first_class_doctype():
    arena = load("sei_research_arena")
    assert arena["name"] == "SEI Research Arena"
    assert field(arena, "arena_name")["reqd"] == 1


def test_signal_type_belongs_to_exactly_one_thesis_and_arena():
    signal_type = load("sei_signal_type")
    assert field(signal_type, "thesis")["reqd"] == 1
    arena = field(signal_type, "research_arena")
    assert arena["fieldtype"] == "Link"
    assert arena["options"] == "SEI Research Arena"
    assert arena["reqd"] == 1
    assert field(signal_type, "active")["default"] == 1


def test_signal_does_not_duplicate_thesis_or_arena():
    signal = load("sei_signal")
    assert field(signal, "signal_type")["reqd"] == 1
    assert field(signal, "research_arena") is None
    assert field(signal, "thesis") is None


def test_thesis_preserves_many_to_many_arena_relationship():
    thesis = load("sei_thesis")
    arenas = field(thesis, "research_arenas")
    assert arenas and arenas["fieldtype"] == "Table"
    assert arenas["options"] == "SEI Thesis Research Arena"


def test_prospect_arenas_are_derived_and_snapshotted_for_queries():
    prospect = load("sei_prospect")
    assert field(prospect, "source_arena") is None
    arenas = field(prospect, "arenas")
    assert arenas["read_only"] == 1
    assert arenas["in_standard_filter"] == 1
    taxonomy_path = (
        ROOT
        / "sales_engagement_intelligence"
        / "sales_engagement_and_intelligence"
        / "services"
        / "taxonomy.py"
    )
    taxonomy = taxonomy_path.read_text()
    assert "def get_prospect_arenas" in taxonomy
    assert 'return _get_prospect_signal_type_values(prospect, "research_arena")' in taxonomy


def test_inactive_signal_type_is_blocked_only_for_new_signals():
    source = (DT / "sei_signal" / "sei_signal.py").read_text()
    assert "self.is_new() and not signal_type.active" in source
    assert "Signal Type must belong to exactly one Thesis and one Research Arena" in source


def test_migration_backfills_signal_types():
    patch_path = (
        ROOT
        / "sales_engagement_intelligence"
        / "patches"
        / "v0_0_1"
        / "backfill_research_arenas.py"
    )
    source = patch_path.read_text()
    assert "UPDATE `tabSEI Signal Type`" in source
    assert "Legacy / Unclassified" in source


def test_signal_type_validates_thesis_arena_pair():
    controller_path = (
        ROOT
        / "sales_engagement_intelligence"
        / "sales_engagement_and_intelligence"
        / "doctype"
        / "sei_signal_type"
        / "sei_signal_type.py"
    )
    source = controller_path.read_text()
    assert "SEI Thesis Research Arena" in source
    assert "Thesis" in source and "is not assigned to Research Arena" in source
