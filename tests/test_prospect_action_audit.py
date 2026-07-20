from pathlib import Path

SCRIPT = Path(
    "sales_engagement_intelligence/sales_engagement_and_intelligence/doctype/"
    "sei_prospect/sei_prospect.js"
).read_text()


def test_complete_prospect_action_contract_is_registered():
    expected = [
        "Recalculate Qualification",
        "Apply Lifecycle Suggestion",
        "Apply Playbook Defaults",
        "Preview Message Draft",
        "Mark as Not Ready for CRM",
        "Mark as Ready for CRM Conversion",
        "Find Duplicates",
        "Preview Conversion",
        "Create Lead",
        "Create Organization",
        "Create Contact",
        "Create Deal",
        "Convert to CRM Lead",
        "Sync SEI Context",
        "Mark Rejected",
        "Mark Do Not Contact",
        "Reopen Prospect",
        "Remove Do Not Contact",
    ]
    for label in expected:
        assert label in SCRIPT, f"Missing Prospect action: {label}"


def test_apply_playbook_defaults_uses_derived_playbook_endpoint():
    assert "add_prospect_action(frm, 'Apply Playbook Defaults'" in SCRIPT
    assert "call_and_reload(frm, 'apply_playbook_defaults'" in SCRIPT
    assert "frm.doc.sei_playbook" not in SCRIPT
    assert "blank fields only" in SCRIPT


def test_replaced_actions_have_current_ui_paths():
    assert "render_crm_links(frm)" in SCRIPT
    assert "configure_message_draft_grid(frm)" in SCRIPT


def test_lifecycle_readiness_actions_are_not_crm_prefixed():
    assert "add_prospect_action(frm, 'Mark as Ready for CRM Conversion'" in SCRIPT
    assert "add_prospect_action(frm, 'Mark as Not Ready for CRM'" in SCRIPT
    assert "add_crm_action(frm, 'Mark as Ready for CRM Conversion'" not in SCRIPT
    assert "add_crm_action(frm, 'Mark as Not Ready for CRM'" not in SCRIPT


def test_primary_action_is_scheduled_after_toolbar_refresh():
    assert "schedule_primary_prospect_action(frm)" in SCRIPT
    assert "window.setTimeout(() => configure_primary_prospect_action(frm), 0)" in SCRIPT


def test_reject_action_precedes_crm_action_block():
    reject_index = SCRIPT.index("add_prospect_action(frm, 'Mark Rejected'")
    crm_index = SCRIPT.index("add_crm_action(frm, 'Find Duplicates'")
    assert reject_index < crm_index


def test_freshness_check_does_not_clear_primary_action():
    start = SCRIPT.index("function reload_if_cached_document_is_stale")
    end = SCRIPT.index("function can_prepare_crm", start)
    freshness = SCRIPT[start:end]
    assert "frm.disable_save()" not in freshness
    assert "frm.enable_save()" not in freshness
    assert "frm.page.clear_primary_action()" not in freshness
