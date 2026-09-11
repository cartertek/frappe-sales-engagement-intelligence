from pathlib import Path

SCRIPT = (
    Path("sales_engagement_intelligence")
    / "sales_engagement_and_intelligence"
    / "doctype"
    / "sei_prospect"
    / "sei_prospect.js"
).read_text()


def test_message_draft_warns_when_recipient_is_not_primary_contact():
    assert "function message_draft_recipient_contact(frm, selectedValue)" in SCRIPT
    assert "Boolean(contact.is_primary)" in SCRIPT
    assert "sei-non-primary-recipient-warning" in SCRIPT
    assert "frappe.utils.icon('warning', 'sm')" in SCRIPT
    assert (
        "This recipient is not a primary contact and will not have a CRM Lead after conversion."
        in SCRIPT
    )


def test_warning_is_shown_on_grid_row_and_open_row_editor():
    assert "refresh_message_draft_recipient_warnings(frm, field)" in SCRIPT
    assert ".grid-row[data-name=\"${row.name}\"]" in SCRIPT
    assert "[data-fieldname=\"to_contact\"]" in SCRIPT
    assert "openRow?.doc?.name === row.name" in SCRIPT
    assert "fields_dict?.to_contact?.$wrapper" in SCRIPT


def test_warning_refreshes_when_to_contact_changes():
    assert "to_contact(frm) {" in SCRIPT
    assert "frm.fields_dict.message_drafts" in SCRIPT
