import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCTYPE_ROOT = (
    ROOT
    / "sales_engagement_intelligence"
    / "sales_engagement_and_intelligence"
    / "doctype"
)


def load_doctype(name: str) -> dict:
    path = DOCTYPE_ROOT / name / f"{name}.json"
    return json.loads(path.read_text())


def test_prospect_metadata_table_is_in_identity_section():
    prospect = load_doctype("sei_prospect")
    fields = {field["fieldname"]: field for field in prospect["fields"]}
    order = prospect["field_order"]

    assert fields["metadata"] == {
        "fieldname": "metadata",
        "label": "Metadata",
        "fieldtype": "Table",
        "options": "SEI Prospect Metadata",
        "idx": fields["metadata"]["idx"],
    }
    assert order.index("identity_section") < order.index("metadata")
    assert order.index("metadata") < order.index("positioning_section")


def test_prospect_metadata_child_table_has_name_and_value():
    metadata = load_doctype("sei_prospect_metadata")
    fields = metadata["fields"]

    assert metadata["istable"] == 1
    assert metadata["editable_grid"] == 1
    assert metadata["field_order"] == ["metadata_name", "metadata_value"]
    assert [(field["label"], field["fieldtype"], field["reqd"]) for field in fields] == [
        ("Name", "Data", 1),
        ("Value", "Data", 1),
    ]
    assert all(field["in_list_view"] == 1 for field in fields)
