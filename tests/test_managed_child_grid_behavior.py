import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCTYPE = (
    ROOT / "sales_engagement_intelligence" / "sales_engagement_and_intelligence"
    / "doctype" / "sei_prospect_message_draft" / "sei_prospect_message_draft.json"
)
SCRIPT = (
    ROOT / "sales_engagement_intelligence" / "sales_engagement_and_intelligence"
    / "doctype" / "sei_prospect" / "sei_prospect.js"
).read_text()


def test_both_managed_grids_use_footer_done_and_x_close():
    assert ".sei-grid-done" in SCRIPT
    assert "$form.children('.grid-footer-toolbar')" in SCRIPT
    assert ".html('&times;')" in SCRIPT
    assert "normalize_managed_grid_editor(field, 'contact')" in SCRIPT
    assert "normalize_managed_grid_editor(field, 'message-draft')" in SCRIPT


def test_dismissing_empty_new_rows_removes_them():
    assert "row.__islocal" in SCRIPT
    assert "removeEmptyLocalRow" in SCRIPT
    assert "grid_rows_by_docname[cdn]?.remove()" in SCRIPT


def test_message_draft_grid_is_inline_editable_like_contacts():
    doctype = json.loads(DOCTYPE.read_text())
    assert doctype["editable_grid"] == 1


def test_message_draft_uses_sent_checkbox_not_send_button():
    fields = {f["fieldname"]: f for f in json.loads(DOCTYPE.read_text())["fields"]}
    assert "mark_as_sent" not in fields
    assert fields["sent"]["fieldtype"] == "Check"
    assert not fields["sent"].get("read_only")
    assert "sent(frm, cdt, cdn)" in SCRIPT
    assert "isolate_message_draft_sent_checkbox(field)" in SCRIPT
    assert "data-sei-sent-bound" in SCRIPT


def test_crm_contact_path_requires_primary_contact_email():
    source = Path(
        "sales_engagement_intelligence/sales_engagement_and_intelligence/doctype/sei_prospect/sei_prospect.js"
    ).read_text()

    assert "row.is_primary && Boolean((row.emails || '').trim())" in source
    assert "row.contact_name || row.emails || row.notes" not in source
