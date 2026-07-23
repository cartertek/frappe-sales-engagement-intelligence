from pathlib import Path

API = (
    Path("sales_engagement_intelligence")
    / "sales_engagement_and_intelligence"
    / "api.py"
).read_text()


def test_sent_and_unsent_drafts_invalidate_crm_lead_activity_cache():
    assert "def _refetch_crm_lead_activity" in API
    assert '"refetch_resource"' in API
    assert '{"cache_key": ["activity", crm_lead]}' in API
    assert "user=frappe.session.user" in API
    assert "after_commit=True" in API
    assert "_refetch_crm_lead_activity(crm_lead)" in API
    assert "crm_lead = communication.reference_name" in API
    assert 'communication.reference_doctype == "CRM Lead"' in API
