import json
from pathlib import Path

SCHEMA = json.loads(Path(
    "sales_engagement_intelligence/sales_engagement_and_intelligence/doctype/sei_prospect/sei_prospect.json"
).read_text())
HELPER = Path(
    "sales_engagement_intelligence/sales_engagement_and_intelligence/services/prospect_crm_links.py"
).read_text()


def test_prospect_has_no_singular_crm_lead_field():
    assert "crm_lead" not in SCHEMA["field_order"]
    assert not any(field.get("fieldname") == "crm_lead" for field in SCHEMA["fields"])


def test_prospect_crm_leads_are_derived_from_crm_lead_backlink():
    assert "def get_prospect_crm_leads" in HELPER
    assert 'filters={"sei_prospect": prospect_name}' in HELPER
    assert '"CRM Lead"' in HELPER
