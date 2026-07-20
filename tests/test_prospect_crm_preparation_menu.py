from pathlib import Path

SCRIPT = Path(
    "sales_engagement_intelligence/sales_engagement_and_intelligence/doctype/"
    "sei_prospect/sei_prospect.js"
).read_text()


def test_crm_preparation_actions_are_registered_from_refresh():
    refresh = SCRIPT.split("function reload_if_cached_document_is_stale", 1)[0]
    expected = [
        "Find CRM Duplicates",
        "Preview CRM Conversion",
        "Create CRM Lead",
        "Create CRM Organization",
        "Create CRM Contact",
        "Create CRM Deal",
        "add_link_button(frm, 'CRM Lead', 'crm_lead')",
        "add_link_button(frm, 'CRM Organization', 'crm_organization')",
        "add_link_button(frm, 'Contact', 'crm_contact')",
        "add_link_button(frm, 'CRM Deal', 'crm_deal')",
    ]
    for item in expected:
        assert item in refresh
