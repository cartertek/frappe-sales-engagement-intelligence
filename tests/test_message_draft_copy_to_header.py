from pathlib import Path

SCRIPT = (
    Path("sales_engagement_intelligence")
    / "sales_engagement_and_intelligence"
    / "doctype"
    / "sei_prospect"
    / "sei_prospect.js"
).read_text()


def test_message_draft_editor_adds_copy_button_next_to_recipient():
    assert "normalize_managed_grid_editor(field, 'message-draft', frm)" in SCRIPT
    assert "add_message_draft_recipient_copy_button(frm, field, $form)" in SCRIPT
    assert "[data-fieldname=\"to_contact\"]" in SCRIPT
    assert "sei-copy-email-to" in SCRIPT
    assert ".text(__('Copy'))" in SCRIPT


def test_copy_button_copies_valid_email_to_header():
    assert "message_draft_email_to_header(frm, row?.to_contact)" in SCRIPT
    assert "frappe.utils.copy_to_clipboard(header" in SCRIPT
    assert "contact.contact_name || contact.contact_role || email" in SCRIPT
    assert "split(/[\\n,;]+/)" in SCRIPT
    assert "format_email_display_name" in SCRIPT
    assert "<${email}>" in SCRIPT


def test_saved_header_value_is_normalized_before_copying():
    assert "selected.match(" in SCRIPT
    assert "<${parsed[2]}>" in SCRIPT
