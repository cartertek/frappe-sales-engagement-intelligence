from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
API = (
    ROOT
    / "sales_engagement_intelligence"
    / "sales_engagement_and_intelligence"
    / "api.py"
).read_text()
SCRIPT = (
    ROOT
    / "sales_engagement_intelligence"
    / "sales_engagement_and_intelligence"
    / "doctype"
    / "sei_prospect"
    / "sei_prospect.js"
).read_text()


def test_unchecking_sent_calls_unsent_endpoint():
    assert "mark_message_draft_unsent" in SCRIPT
    assert "frappe.model.set_value(cdt, cdn, 'sent', 1)" in SCRIPT


def test_unsent_endpoint_deletes_communication_and_clears_fields():
    assert "def mark_message_draft_unsent" in API
    assert 'frappe.db.exists("Communication", communication_name)' in API
    assert "communication.delete(ignore_permissions=True)" in API
    assert 'doc.db_set({"sent": 0, "sent_on": None, "crm_email": None})' in API
