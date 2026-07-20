import json
from pathlib import Path

ROOT = Path("sales_engagement_intelligence/sales_engagement_and_intelligence")


def dt(name):
    return json.loads((ROOT / "doctype" / name / f"{name}.json").read_text())


def fields(name):
    return {f["fieldname"]: f for f in dt(name)["fields"]}


def test_theses_are_replaced_by_playbooks():
    assert not (ROOT / "doctype/sei_thesis").exists()
    assert fields("sei_playbook")["thesis"]["fieldtype"] == "Small Text"
    assert fields("sei_signal_type")["playbook"]["options"] == "SEI Playbook"


def test_prospect_outreach_schema():
    f = fields("sei_prospect")
    for old in (
        "sei_playbook",
        "playbook_guidance",
        "primary_contact_name",
        "primary_contact_email",
        "ready_for_crm_conversion",
        "conversion_target",
    ):
        assert old not in f
    assert f["playbooks"]["in_standard_filter"] == 1
    assert f["contacts"]["options"] == "SEI Prospect Contact"
    tabs = [x["label"] for x in dt("sei_prospect")["fields"] if x.get("fieldtype") == "Tab Break"]
    assert tabs == ["Overview", "Status", "Qualification", "Outreach", "CRM Conversion"]


def test_managed_roles_and_drafts():
    assert fields("sei_playbook")["contact_roles"]["options"] == "SEI Playbook Contact Role"
    assert fields("sei_prospect_contact")["contact_role"]["options"] == "SEI Contact Role"
    draft = fields("sei_message_draft")
    assert draft["from_user"]["options"] == "User"
    assert draft["to_contact"]["fieldtype"] == "Select"


def test_unified_conversion_and_crm_routes():
    api = (ROOT / "api.py").read_text()
    js = (ROOT / "doctype/sei_prospect/sei_prospect.js").read_text()
    assert "def convert_to_crm_lead" in api
    assert "def mark_ready_for_crm_conversion" not in api
    assert "Convert to CRM Lead" in js
    assert "/crm/${collections[doctype]}" in js


def test_playbook_manages_assigned_signal_types():
    playbook = dt("sei_playbook")
    fields = {field["fieldname"]: field for field in playbook["fields"]}
    assert fields["signal_types"]["fieldtype"] == "Table"
    assert fields["signal_types"]["options"] == "SEI Playbook Signal Type"

    child = dt("sei_playbook_signal_type")
    child_fields = {field["fieldname"]: field for field in child["fields"]}
    assert child["istable"] == 1
    assert child_fields["signal_type"]["options"] == "SEI Signal Type"
    assert child_fields["signal_type"]["reqd"] == 1

    playbook_controller = (ROOT / "doctype/sei_playbook/sei_playbook.py").read_text()
    signal_type_controller = (ROOT / "doctype/sei_signal_type/sei_signal_type.py").read_text()
    assert "sync_signal_type_links" in playbook_controller
    assert "sync_playbook_child_row" in signal_type_controller
