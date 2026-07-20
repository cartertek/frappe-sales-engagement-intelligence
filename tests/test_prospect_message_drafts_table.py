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


def test_expanded_message_draft_editor_has_done_and_no_duplicate_insert_controls():
    script = PROSPECT_JS.read_text()
    assert "normalize_managed_grid_editor(field, 'message-draft')" in script
    assert "__('Done')" in script
    assert ".grid-insert-row-below, .grid-append-row" in script
    assert ".remove()" in script
