import json
from pathlib import Path

SCHEMA_PATH = Path(
    "sales_engagement_intelligence/sales_engagement_and_intelligence/doctype/"
    "sei_prospect/sei_prospect.json"
)


def _schema():
    return json.loads(SCHEMA_PATH.read_text())


def test_only_requested_positioning_fields_move_to_outreach():
    order = _schema()["field_order"]
    overview = order[order.index("overview_tab") + 1 : order.index("status_tab")]
    outreach = order[order.index("outreach_tab") + 1 : order.index("crm_conversion_tab")]

    assert overview[-5:] == [
        "classification_section",
        "signals",
        "playbooks",
        "arenas",
        "notes",
    ]
    assert outreach[:4] == [
        "positioning_section",
        "offer",
        "signal_summary",
        "contact_target_notes",
    ]


def test_positioning_fields_keep_existing_types():
    fields = {field["fieldname"]: field for field in _schema()["fields"]}

    assert fields["positioning_section"]["fieldtype"] == "Section Break"
    assert fields["offer"]["fieldtype"] == "Data"
    assert fields["signal_summary"]["fieldtype"] == "Small Text"
    assert fields["contact_target_notes"]["fieldtype"] == "Small Text"
    assert fields["classification_section"] == {
        "fieldname": "classification_section",
        "label": "Classification",
        "fieldtype": "Section Break",
        "idx": fields["classification_section"]["idx"],
    }
