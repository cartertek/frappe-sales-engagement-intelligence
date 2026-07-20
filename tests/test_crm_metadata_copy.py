from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = (
    ROOT
    / "sales_engagement_intelligence"
    / "sales_engagement_and_intelligence"
    / "services"
    / "crm_preparation.py"
).read_text()


def test_metadata_copy_covers_all_frappe_collaboration_records():
    assert "def _copy_prospect_metadata" in SOURCE
    assert '"ToDo"' in SOURCE
    assert '"File"' in SOURCE
    assert '"Tag Link"' in SOURCE
    assert '"DocShare"' in SOURCE


def test_metadata_copy_is_idempotent_for_each_metadata_type():
    helper = SOURCE.split("def _copy_prospect_metadata", 1)[1].split(
        "def _assert_not_protected", 1
    )[0]
    assert helper.count("frappe.db.exists") >= 3
    assert 'frappe.db.get_value("DocShare", duplicate_filters, "name")' in helper


def test_metadata_is_copied_to_created_or_linked_crm_resources():
    assert '_copy_prospect_metadata(prospect_name, "CRM Lead", lead.name)' in SOURCE
    assert (
        '_copy_prospect_metadata(prospect_name, "CRM Organization", organization.name)'
        in SOURCE
    )
    assert '_copy_prospect_metadata(prospect_name, "Contact", contact.name)' in SOURCE
    assert '_copy_prospect_metadata(prospect.name, "Contact", doc.name)' in SOURCE
    assert '_copy_prospect_metadata(prospect_name, "CRM Organization", org.name)' in SOURCE
    assert '_copy_prospect_metadata(prospect_name, doctype, record_name)' in SOURCE
