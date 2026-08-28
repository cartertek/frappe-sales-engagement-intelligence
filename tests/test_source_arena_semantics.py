import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "sales_engagement_intelligence" / "sales_engagement_and_intelligence"


def _doctype(name):
    return json.loads((APP / "doctype" / name / f"{name}.json").read_text())


def test_signal_source_arena_is_distinct_provenance_field():
    fields = {f["fieldname"]: f for f in _doctype("sei_signal")["fields"]}
    field = fields["source_arena"]
    assert field["label"] == "Source Arena"
    assert field["fieldtype"] == "Link"
    assert field["options"] == "SEI Signal Source Arena"
    assert "distinct from the Signal Type's Research Arena" in field["description"]


def test_interaction_attribution_no_longer_stores_source_arena():
    fields = {f["fieldname"] for f in _doctype("sei_interaction_attribution")["fields"]}
    assert "source_arena" not in fields


def test_import_source_arena_defaults_signal_source_arena():
    source = (APP / "services" / "imports.py").read_text()
    assert '"source_arena": row.get("source_arena")' in source
    assert 'row.get("source_arena") or batch_doc.source_arena' in source


def test_drafting_uses_research_arena_not_source_arena():
    source = (APP / "services" / "drafting.py").read_text()
    assert '"research_arena"' in source
    assert '"source_arena"' not in source
