from pathlib import Path

SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "sales_engagement_intelligence"
    / "sales_engagement_and_intelligence"
    / "doctype"
    / "sei_prospect"
    / "sei_prospect.js"
).read_text()


def test_all_actions_use_single_prospect_actions_menu():
    assert "const PROSPECT_ACTIONS_MENU = __('Prospect Actions');" in SCRIPT
    assert "__('SEI Actions')" not in SCRIPT
    assert "__('CRM Preparation')" not in SCRIPT
    assert "__('Outreach Drafting')" not in SCRIPT
    assert "frm.add_custom_button" in SCRIPT
    assert "}, PROSPECT_ACTIONS_MENU);" in SCRIPT


def test_crm_actions_are_grouped_by_label():
    assert "function add_crm_action" in SCRIPT
    assert "`CRM — ${label}`" in SCRIPT
    for label in (
        "Mark as Ready for CRM Conversion",
        "Find Duplicates",
        "Preview Conversion",
        "Create Lead",
        "Create Organization",
        "Create Contact",
        "Create Deal",
        "Convert to CRM Lead",
        "Sync SEI Context",
    ):
        assert f"add_crm_action(frm, '{label}'" in SCRIPT


def test_primary_action_matches_supported_lifecycles_only():
    block = SCRIPT.split("function configure_primary_prospect_action", 1)[1].split(
        "function reload_if_cached_document_is_stale", 1
    )[0]
    assert "lifecycle === 'Qualified'" in block
    assert "label = __('Mark as Ready for CRM Conversion')" in block
    assert "lifecycle === 'Ready for CRM Conversion'" in block
    assert "label = __('Convert to CRM Lead')" in block
    assert "lifecycle === 'Rejected'" in block
    assert "label = __('Reopen Prospect')" in block
    assert "lifecycle === 'Do Not Contact'" in block
    assert "label = __('Remove Do Not Contact')" in block
    assert "frm.page.set_primary_action(label, handler)" in block
    assert "frm.page.clear_primary_action()" in block


def test_primary_actions_reuse_menu_handlers():
    assert "handler = () => mark_ready_for_crm_conversion(frm);" in SCRIPT
    assert "handler = () => convert_to_crm_lead(frm);" in SCRIPT
    assert SCRIPT.count("handler = () => reopen_prospect(frm);") == 2
