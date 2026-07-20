import json
from pathlib import Path

CONTACT = Path(
    "sales_engagement_intelligence/sales_engagement_and_intelligence/doctype/"
    "sei_prospect_contact/sei_prospect_contact.json"
)


def test_prospect_contacts_use_inline_managed_grid():
    doctype = json.loads(CONTACT.read_text())
    assert doctype["istable"] == 1
    assert doctype["editable_grid"] == 1


def test_contact_grid_exposes_core_fields_inline():
    fields = {field["fieldname"]: field for field in json.loads(CONTACT.read_text())["fields"]}
    assert fields["contact_role"]["in_list_view"] == 1
    assert fields["contact_name"]["in_list_view"] == 1
    assert fields["emails"]["in_list_view"] == 1
    assert fields["is_primary"]["in_list_view"] == 1


def test_expanded_contact_editor_uses_single_x_close_control():
    script = Path(
        "sales_engagement_intelligence/sales_engagement_and_intelligence/doctype/"
        "sei_prospect/sei_prospect.js"
    ).read_text()
    assert "configure_contact_grid(frm)" in script
    assert "normalize_managed_grid_editor(field, 'contact')" in script
    assert ".grid-collapse-row" in script
    assert ".html('&times;')" in script
    assert "__('Done')" not in script


def test_expanded_contact_editor_removes_duplicate_insert_below_controls():
    script = Path(
        "sales_engagement_intelligence/sales_engagement_and_intelligence/doctype/"
        "sei_prospect/sei_prospect.js"
    ).read_text()
    assert ".grid-insert-row-below, .grid-append-row" in script
    assert ".remove()" in script


def test_contact_grid_formats_emails_as_comma_separated_truncated_text():
    script = Path(
        "sales_engagement_intelligence/sales_engagement_and_intelligence/doctype/"
        "sei_prospect/sei_prospect.js"
    ).read_text()
    assert "field.grid.get_field('emails')" in script
    assert ".join(', ')" in script
    assert 'class="ellipsis"' in script
