from pathlib import Path

API = Path(
    "sales_engagement_intelligence/sales_engagement_and_intelligence/api.py"
).read_text()
SERVICE = Path(
    "sales_engagement_intelligence/sales_engagement_and_intelligence/services/crm_preparation.py"
).read_text()
SCRIPT = Path(
    "sales_engagement_intelligence/sales_engagement_and_intelligence/doctype/"
    "sei_prospect/sei_prospect.js"
).read_text()


def test_post_conversion_primary_contact_lead_api_is_manager_guarded():
    assert "def create_primary_contact_crm_lead(prospect: str, contact_row: str) -> dict:" in API
    endpoint = API.split("def create_primary_contact_crm_lead", 1)[1].split("@api_endpoint", 1)[0]
    assert '_check_prospect_permission(prospect, "write")' in endpoint
    assert "_require_manager()" in endpoint
    assert "create_crm_lead_for_primary_contact(prospect, contact_row)" in endpoint


def test_service_only_promotes_missing_primary_contacts_after_conversion():
    assert "def primary_contacts_missing_crm_leads(prospect_name: str) -> list[dict]:" in SERVICE
    assert "def create_crm_lead_for_primary_contact(prospect_name: str, contact_row: str) -> dict:" in SERVICE
    assert '{"Converted to CRM Lead", "Converted to CRM Deal"}' in SERVICE
    assert "if not row.is_primary:" in SERVICE
    assert "Only a primary prospect contact can be promoted to a CRM Lead." in SERVICE
    assert "existing = _crm_lead_for_contact_row(row)" in SERVICE
    assert "already exists for this primary contact" in SERVICE
    assert "contact = _upsert_contact_row(prospect, row)" in SERVICE
    assert "lead = frappe.get_doc(_lead_payload_for_contact(prospect, row))" in SERVICE
    assert '"Created CRM Lead for Primary Contact"' in SERVICE


def test_existing_initial_conversion_reuses_contact_lead_lookup():
    conversion = SERVICE.split("def convert_prospect_to_crm_leads", 1)[1]
    assert "existing = _crm_lead_for_contact_row(row)" in conversion


def test_converted_prospect_menu_exposes_primary_contact_lead_workflow():
    assert "add_crm_action(frm, 'Create Lead for Primary Contact'" in SCRIPT
    assert "function create_lead_for_primary_contact(frm)" in SCRIPT
    assert "api.get_primary_contacts_missing_crm_leads" in SCRIPT
    assert "api.create_primary_contact_crm_lead" in SCRIPT
    assert "Every primary contact with an email already has a CRM Lead." in SCRIPT
    assert "Create CRM Lead for Primary Contact" in SCRIPT
