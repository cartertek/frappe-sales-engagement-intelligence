import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCTYPE_ROOT = (
    ROOT
    / "sales_engagement_intelligence"
    / "sales_engagement_and_intelligence"
    / "doctype"
)
PROSPECT_JSON = DOCTYPE_ROOT / "sei_prospect" / "sei_prospect.json"
PROSPECT_JS = DOCTYPE_ROOT / "sei_prospect" / "sei_prospect.js"
CHILD_JSON = DOCTYPE_ROOT / "sei_prospect_message_draft" / "sei_prospect_message_draft.json"
PATCH = (
    ROOT
    / "sales_engagement_intelligence"
    / "patches"
    / "v0_0_1"
    / "migrate_message_drafts_to_prospect_table.py"
)


def test_prospect_uses_managed_message_draft_table():
    prospect = json.loads(PROSPECT_JSON.read_text())
    fields = {field["fieldname"]: field for field in prospect["fields"]}
    assert "message_drafts_html" not in fields
    assert fields["message_drafts"]["fieldtype"] == "Table"
    assert fields["message_drafts"]["options"] == "SEI Prospect Message Draft"


def test_message_draft_child_doctype_is_editable_grid():
    child = json.loads(CHILD_JSON.read_text())
    assert child["istable"] == 1
    fields = {field["fieldname"]: field for field in child["fields"]}
    assert {"platform", "from_user", "to_contact", "subject", "body"} <= fields.keys()


def test_prospect_has_no_standalone_message_draft_menu():
    script = PROSPECT_JS.read_text()
    assert "frappe.new_doc('SEI Message Draft'" not in script
    assert "render_message_drafts" not in script
    assert "configure_message_draft_grid" in script


def test_existing_drafts_are_migrated_idempotently():
    text = PATCH.read_text()
    assert 'legacy_message_draft' in text
    assert 'if row.name in existing' in text
    assert 'doc.append(' in text


def test_message_draft_cc_is_single_line_input():
    fields = {field["fieldname"]: field for field in json.loads(CHILD_JSON.read_text())["fields"]}
    assert fields["cc"]["fieldtype"] == "Data"


def test_expanded_message_draft_editor_has_x_close_and_no_duplicate_insert_controls():
    script = PROSPECT_JS.read_text()
    assert "normalize_managed_grid_editor(field, 'message-draft')" in script
    assert ".html('&times;')" in script
    assert ".grid-footer-toolbar .row-actions" in script
    assert ".text(__('Done'))" in script
    assert ".grid-insert-row-below, .grid-append-row" in script
    assert ".remove()" in script


def test_message_draft_rows_use_sent_checkbox():
    fields = {field["fieldname"]: field for field in json.loads(CHILD_JSON.read_text())["fields"]}
    assert "mark_as_sent" not in fields
    assert fields["sent"]["fieldtype"] == "Check"
    assert not fields["sent"].get("read_only")
    script = PROSPECT_JS.read_text()
    assert "sent(frm, cdt, cdn)" in script
    assert "args: { draft: row.name }" in script



def test_send_api_supports_managed_child_drafts():
    api_path = ROOT / "sales_engagement_intelligence" / "sales_engagement_and_intelligence" / "api.py"
    api = api_path.read_text()
    assert 'frappe.db.exists("SEI Prospect Message Draft", draft)' in api
    assert '_check_doc_permission("SEI Prospect", doc.parent, "write")' in api
    assert 'prospect = frappe.get_doc("SEI Prospect", doc.parent)' in api


def test_message_draft_sent_checkbox_does_not_open_row_editor():
    script = PROSPECT_JS.read_text()
    assert "isolate_message_draft_sent_checkbox(field)" in script
    assert "[data-fieldname=\"sent\"] input" in script
    assert '[data-fieldname="sent"]' in script
    assert "event.stopPropagation()" in script
