from pathlib import Path

SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "sales_engagement_intelligence"
    / "sales_engagement_and_intelligence"
    / "doctype"
    / "sei_prospect"
    / "sei_prospect.js"
).read_text()


def test_saved_message_draft_recipient_is_preserved_in_dynamic_options():
    assert "const saved = (frm.doc.message_drafts || [])" in SCRIPT
    assert "new Set([...available, ...saved])" in SCRIPT


def test_open_message_draft_recipient_control_is_refreshed_after_options_load():
    assert "refresh_open_message_draft_recipient(field)" in SCRIPT
    assert "control.refresh()" in SCRIPT
    assert "control.set_value(openRow.doc.to_contact || '')" in SCRIPT
