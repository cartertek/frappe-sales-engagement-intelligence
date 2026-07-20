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
