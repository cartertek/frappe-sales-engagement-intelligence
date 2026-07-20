import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROSPECT = (
    ROOT
    / "sales_engagement_intelligence/sales_engagement_and_intelligence/doctype/sei_prospect"
    / "sei_prospect.json"
)


def _doc():
    return json.loads(PROSPECT.read_text())


def test_prospect_layout_fieldnames_are_valid_identifiers():
    doc = _doc()
    invalid = [
        field["fieldname"]
        for field in doc["fields"]
        if field.get("fieldtype") in {"Tab Break", "Section Break", "Column Break"}
        and not re.fullmatch(r"[a-z][a-z0-9_]*", field["fieldname"])
    ]
    assert invalid == []


def test_each_prospect_tab_starts_with_a_section_boundary():
    doc = _doc()
    fields = {field["fieldname"]: field for field in doc["fields"]}
    order = doc["field_order"]
    tabs = [i for i, name in enumerate(order) if fields[name].get("fieldtype") == "Tab Break"]
    for index in tabs:
        first = fields[order[index + 1]]
        assert first.get("fieldtype") == "Section Break"


def test_prospect_field_order_matches_fields_array():
    doc = _doc()
    assert doc["field_order"] == [field["fieldname"] for field in doc["fields"]]
