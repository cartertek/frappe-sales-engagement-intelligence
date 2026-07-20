from pathlib import Path

SOURCE = Path(
    "sales_engagement_intelligence/sales_engagement_and_intelligence/services/crm_preparation.py"
).read_text()
SCRIPT = Path(
    "sales_engagement_intelligence/sales_engagement_and_intelligence/doctype/sei_prospect/sei_prospect.js"
).read_text()


def test_existing_contact_child_tables_use_document_setter():
    assert 'field.fieldtype in ("Table", "Table MultiSelect")' in SOURCE
    assert "doc.set(key, value)" in SOURCE


def test_unexpected_conversion_errors_are_not_shown_as_readiness_requirements():
    assert "CRM Conversion Failed" in SCRIPT
    assert "CRM_READINESS_REQUIREMENTS_NOT_MET" in SCRIPT
    assert "Unexpected CRM conversion error." in SCRIPT
