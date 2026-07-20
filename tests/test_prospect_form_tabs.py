import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROSPECT = (
    ROOT
    / "sales_engagement_intelligence"
    / "sales_engagement_and_intelligence"
    / "doctype"
    / "sei_prospect"
    / "sei_prospect.json"
)


def test_prospect_field_records_match_declared_order_and_idx():
    data = json.loads(PROSPECT.read_text())
    actual = [field["fieldname"] for field in data["fields"]]
    assert actual == data["field_order"]
    assert [field.get("idx") for field in data["fields"]] == list(
        range(1, len(data["fields"]) + 1)
    )


def test_prospect_layout_break_fieldnames_are_valid():
    data = json.loads(PROSPECT.read_text())
    pattern = re.compile(r"^[a-z][a-z0-9_]*$")
    for field in data["fields"]:
        if field["fieldtype"] in {"Tab Break", "Section Break", "Column Break"}:
            assert pattern.fullmatch(field["fieldname"]), field["fieldname"]


def test_each_prospect_tab_starts_with_a_section_break():
    data = json.loads(PROSPECT.read_text())
    fields = data["fields"]
    for index, field in enumerate(fields):
        if field["fieldtype"] == "Tab Break":
            assert fields[index + 1]["fieldtype"] == "Section Break"
