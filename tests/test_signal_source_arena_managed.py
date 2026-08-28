import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "sales_engagement_intelligence" / "sales_engagement_and_intelligence"


def test_signal_source_arena_is_managed_link():
    signal = json.loads((APP / "doctype/sei_signal/sei_signal.json").read_text())
    fields = {row["fieldname"]: row for row in signal["fields"]}
    field = fields["source_arena"]
    assert field["fieldtype"] == "Link"
    assert field["options"] == "SEI Signal Source Arena"


def test_signal_source_arena_doctype_is_manager_managed():
    schema = json.loads((APP / "doctype/sei_signal_source_arena/sei_signal_source_arena.json").read_text())
    assert schema["autoname"] == "field:arena_name"
    fields = {row["fieldname"]: row for row in schema["fields"]}
    assert fields["arena_name"]["unique"] == 1
    assert fields["active"]["default"] == 1


def test_imports_create_missing_signal_source_arenas():
    source = (APP / "services/imports.py").read_text()
    assert "def resolve_signal_source_arena" in source
    assert 'frappe.db.exists("SEI Signal Source Arena", value)' in source
    assert '"doctype": "SEI Signal Source Arena"' in source
    assert 'resolve_signal_source_arena(row.get("source_arena"))' in source
