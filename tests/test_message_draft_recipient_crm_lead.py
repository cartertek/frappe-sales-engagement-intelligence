from pathlib import Path

API = Path(
    "sales_engagement_intelligence/sales_engagement_and_intelligence/api.py"
).read_text()


def test_sent_message_resolves_crm_lead_from_recipient_email():
    assert "def _message_draft_crm_lead(prospect, recipient: str) -> str:" in API
    assert 'filters = {"email": recipient}' in API
    assert 'filters["sei_prospect"] = prospect.name' in API
    assert "crm_lead = _message_draft_crm_lead(prospect, recipient)" in API
    assert '\"reference_name\": crm_lead' in API
    assert "_refetch_crm_lead_activity(crm_lead)" in API


def test_recipient_lead_resolution_never_falls_back_to_a_singular_prospect_lead():
    assert 'prospect.get("crm_lead")' not in API
    assert "No CRM Lead linked to prospect" in API
    assert "Multiple CRM Leads for" in API
