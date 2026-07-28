import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SIGNAL_JSON = (
    ROOT
    / "sales_engagement_intelligence/sales_engagement_and_intelligence/doctype/sei_signal/sei_signal.json"
)
PROSPECT_JS = (
    ROOT
    / "sales_engagement_intelligence/sales_engagement_and_intelligence/doctype/sei_prospect/sei_prospect.js"
)
API = ROOT / "sales_engagement_intelligence/sales_engagement_and_intelligence/api.py"


def test_signal_name_is_required_and_used_as_title():
    schema = json.loads(SIGNAL_JSON.read_text())
    field = next(field for field in schema["fields"] if field.get("fieldname") == "signal_name")
    assert field["label"] == "Name"
    assert field["reqd"] == 1
    assert field["in_list_view"] == 1
    assert schema["title_field"] == "signal_name"
    assert "signal_name" in schema["search_fields"]


def test_nested_signal_table_displays_name_and_type():
    source = PROSPECT_JS.read_text()
    assert "'signal_name'" in source
    assert "signal.signal_name || signal.signal_type || signal.name" in source
    assert "<th>${__('Name')}</th>" in source
    assert "<th>${__('Signal Type')}</th>" in source


def test_signal_api_exposes_signal_name():
    source = API.read_text()
    assert 'SIGNAL_FIELDS = {\n    "signal_name",' in source
    assert '            "signal_name",\n            "signal_type",' in source
