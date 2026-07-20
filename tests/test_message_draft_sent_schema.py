from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
API = (ROOT / "sales_engagement_intelligence" / "sales_engagement_and_intelligence" / "api.py").read_text()


def test_mark_sent_uses_standard_communication_doctype():
    assert '"doctype": "Communication"' in API
    assert '"reference_doctype": "CRM Lead"' in API
    assert '"sent_or_received": "Sent"' in API
    assert 'CRM Lead Email is unavailable' not in API


def test_mark_sent_logs_without_sending_email():
    assert 'frappe.core.doctype.communication.email.make' not in API
    assert 'communication.insert(ignore_permissions=True)' in API


def test_mark_sent_resolves_contact_display_name_to_email():
    assert "def _message_draft_recipient" in API
    assert '_message_draft_recipient(prospect, doc.to_contact)' in API
    assert "def _message_draft_sender" in API
    assert 'frappe.db.get_value(\n        "User", raw, ["email", "full_name"], as_dict=True\n    )' in API
    assert "sender, sender_full_name = _message_draft_sender(doc.from_user)" in API
    assert '"sender": sender' in API
    assert '"sender_full_name": sender_full_name' in API


def test_mark_sent_ignores_invalid_optional_cc():
    assert "def _optional_email_list" in API
    assert '"cc": _optional_email_list(doc.cc)' in API
