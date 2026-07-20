from pathlib import Path

SCRIPT = Path(
    "sales_engagement_intelligence/sales_engagement_and_intelligence/doctype/"
    "sei_prospect/sei_prospect.js"
).read_text()


def test_crm_actions_are_registered_in_prospect_actions_menu():
    actions = SCRIPT.split("function reload_if_cached_document_is_stale", 1)[0]
    expected = [
        "add_crm_action(frm, 'Find Duplicates'",
        "add_crm_action(frm, 'Preview Conversion'",
        "add_crm_action(frm, 'Create Lead'",
        "add_crm_action(frm, 'Create Organization'",
        "add_crm_action(frm, 'Create Contact'",
        "add_crm_action(frm, 'Create Deal'",
        "add_link_button(frm, 'CRM Lead', 'crm_lead', 'CRM — Link Existing Lead')",
        "add_link_button(frm, 'CRM Organization', 'crm_organization', 'CRM — Link Existing Organization')",
        "add_link_button(frm, 'Contact', 'crm_contact', 'CRM — Link Existing Contact')",
        "add_link_button(frm, 'CRM Deal', 'crm_deal', 'CRM — Link Existing Deal')",
    ]
    for item in expected:
        assert item in actions
    assert "PROSPECT_ACTIONS_MENU" in actions
    assert "CRM Preparation" not in actions


def test_convert_to_crm_lead_remains_in_menu_for_authorized_users():
    actions = SCRIPT.split("function reload_if_cached_document_is_stale", 1)[0]
    assert "if (is_manager_or_admin())" in actions
    assert "add_crm_action(frm, 'Convert to CRM Lead'" in actions
    assert "show_conversion_preview(frm, { allow_convert: true })" in actions


def test_conversion_popup_always_exposes_real_conversion_action():
    assert "if (options.allow_convert)" in SCRIPT
    assert "options.allow_convert && eligible" not in SCRIPT
    assert "primary_action_label = __('Convert to CRM Lead')" in SCRIPT
    assert "convert_from_preview(frm, dialog)" in SCRIPT
    assert "api.convert_to_crm_lead" in SCRIPT
    assert "show_crm_readiness_checklist(message)" in SCRIPT
