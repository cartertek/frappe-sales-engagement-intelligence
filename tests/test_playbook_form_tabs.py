import json
from pathlib import Path

SCHEMA_PATH = Path(
    "sales_engagement_intelligence/sales_engagement_and_intelligence/doctype/"
    "sei_playbook/sei_playbook.json"
)


def _schema():
    return json.loads(SCHEMA_PATH.read_text())


def test_playbook_form_has_three_tabs_in_order():
    schema = _schema()
    fields = {field["fieldname"]: field for field in schema["fields"]}
    order = schema["field_order"]

    assert fields["overview_tab"]["fieldtype"] == "Tab Break"
    assert fields["overview_tab"]["label"] == "Overview"
    assert fields["qualification_tab"]["fieldtype"] == "Tab Break"
    assert fields["qualification_tab"]["label"] == "Qualification"
    assert fields["outreach_tab"]["fieldtype"] == "Tab Break"
    assert fields["outreach_tab"]["label"] == "Outreach"
    assert order.index("overview_tab") < order.index("qualification_tab") < order.index("outreach_tab")


def test_playbook_fields_are_grouped_by_purpose():
    order = _schema()["field_order"]
    overview = order[order.index("overview_tab") + 1 : order.index("qualification_tab")]
    qualification = order[order.index("qualification_tab") + 1 : order.index("outreach_tab")]
    outreach = order[order.index("outreach_tab") + 1 :]

    assert overview == [
        "playbook_name",
        "active",
        "description",
        "thesis",
        "typical_prospect_types",
        "notes",
    ]
    assert qualification == [
        "research_arenas_section",
        "research_arenas",
        "signal_types_section",
        "signal_types",
        "signal_rules",
        "qualification_guidance_section",
        "qualifying_signal_guidance",
        "disqualifying_guidance",
    ]
    assert outreach == [
        "default_offer",
        "default_asset",
        "recommended_first_action",
        "follow_up_guidance",
        "contact_roles_section",
        "contact_roles",
    ]
