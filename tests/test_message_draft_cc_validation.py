from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SERVICE = (
    ROOT
    / "sales_engagement_intelligence"
    / "sales_engagement_and_intelligence"
    / "services"
    / "message_draft_validation.py"
).read_text()
STANDALONE = (
    ROOT
    / "sales_engagement_intelligence"
    / "sales_engagement_and_intelligence"
    / "doctype"
    / "sei_message_draft"
    / "sei_message_draft.py"
).read_text()
PROSPECT = (
    ROOT
    / "sales_engagement_intelligence"
    / "sales_engagement_and_intelligence"
    / "doctype"
    / "sei_prospect"
    / "sei_prospect.py"
).read_text()
CHILD = (
    ROOT
    / "sales_engagement_intelligence"
    / "sales_engagement_and_intelligence"
    / "doctype"
    / "sei_prospect_message_draft"
    / "sei_prospect_message_draft.py"
).read_text()


def test_cc_validation_is_applied_to_both_draft_doctypes():
    assert "normalize_email_list(self.cc" in STANDALONE
    assert "normalize_email_list(self.cc" in CHILD
    assert "validate_message_draft_cc_addresses" in PROSPECT
    assert 'self.get("message_drafts")' in PROSPECT


def test_cc_validation_accepts_lists_and_rejects_invalid_addresses():
    assert 're.split(r"[,;\\n]+"' in SERVICE
    assert "validate_email_address(address, throw=True)" in SERVICE
    assert "must contain only valid email addresses" in SERVICE
