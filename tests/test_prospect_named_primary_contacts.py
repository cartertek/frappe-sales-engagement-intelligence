import json
from pathlib import Path

SCHEMA = json.loads(
    Path(
        "sales_engagement_intelligence/sales_engagement_and_intelligence/doctype/"
        "sei_prospect/sei_prospect.json"
    ).read_text()
)
CONTROLLER = Path(
    "sales_engagement_intelligence/sales_engagement_and_intelligence/doctype/"
    "sei_prospect/sei_prospect.py"
).read_text()
LIST_SCRIPT = Path(
    "sales_engagement_intelligence/sales_engagement_and_intelligence/doctype/"
    "sei_prospect/sei_prospect_list.js"
).read_text()


def test_prospect_has_named_primary_contacts_counter_after_emails_sent():
    fields = {field["fieldname"]: field for field in SCHEMA["fields"]}
    counter = fields["named_primary_contacts"]

    assert counter["label"] == "Named Primary Contacts"
    assert counter["fieldtype"] == "Int"
    assert counter["read_only"] == 1
    assert counter["default"] == "0"
    assert SCHEMA["field_order"].index("named_primary_contacts") == (
        SCHEMA["field_order"].index("emails_sent") + 1
    )


def test_named_primary_contacts_counts_only_primary_rows_with_nonblank_names():
    assert "self.set_named_primary_contacts()" in CONTROLLER
    assert 'if row.get("is_primary")' in CONTROLLER
    assert '(row.get("contact_name") or "").strip()' in CONTROLLER


def test_named_primary_contacts_is_available_to_prospect_list_view():
    assert "'named_primary_contacts'" in LIST_SCRIPT

PATCH = Path(
    "sales_engagement_intelligence/patches/v0_0_1/"
    "backfill_named_primary_contacts.py"
).read_text()
PATCHES = Path("sales_engagement_intelligence/patches.txt").read_text()


def test_existing_prospects_are_backfilled_from_named_primary_contact_rows():
    assert "backfill_named_primary_contacts" in PATCHES
    assert "contact.is_primary = 1" in PATCH
    assert "TRIM(contact.contact_name)" in PATCH
    assert "contact.parentfield = 'contacts'" in PATCH
