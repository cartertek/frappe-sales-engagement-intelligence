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
    assert fields["is_primary"]["in_list_view"] == 1
