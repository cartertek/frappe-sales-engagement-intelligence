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


def test_convert_to_crm_lead_is_always_registered_for_authorized_users():
    refresh = SCRIPT.split("function reload_if_cached_document_is_stale", 1)[0]
    assert "if (is_manager_or_admin())" in refresh
    assert "Convert to CRM Lead" in refresh
    assert "show_conversion_preview(frm, { allow_convert: true })" in refresh
    assert "}, __('CRM Preparation'));" in refresh
    convert_block = refresh.split("Convert to CRM Lead", 1)[1].split("configure_message_draft_grid", 1)[0]
    assert "CRM Preparation" in convert_block
    assert "CRM Conversion" not in convert_block
    assert "lifecycle_status === 'Ready for CRM Conversion'" not in refresh


def test_conversion_popup_always_exposes_real_conversion_action():
    assert "if (options.allow_convert)" in SCRIPT
    assert "options.allow_convert && eligible" not in SCRIPT
    assert "primary_action_label = __('Convert to CRM Lead')" in SCRIPT
    assert "convert_from_preview(frm, dialog)" in SCRIPT
    assert "api.convert_to_crm_lead" in SCRIPT
    assert "show_crm_readiness_checklist(message)" in SCRIPT
