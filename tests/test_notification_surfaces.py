from pathlib import Path

MODULE = Path("sales_engagement_intelligence/sales_engagement_and_intelligence")


def test_non_actionable_form_notifications_use_toasts():
    prospect = (MODULE / "doctype" / "sei_prospect" / "sei_prospect.js").read_text()
    imports = (MODULE / "doctype" / "sei_import_batch" / "sei_import_batch.js").read_text()

    assert "frappe.show_alert" in prospect
    assert "frappe.show_alert" in imports
    assert "title: __('SEI Action Complete')" not in prospect
    assert "title: __('Draft Preview Failed')" not in prospect
    assert "Templates are committed under docs/import_templates" in imports

    # Keep dialogs that present a checklist, preview, prompt, or confirmation.
    assert "CRM Readiness Requirements" in prospect
    assert "new frappe.ui.Dialog" in prospect
    assert "frappe.confirm" in prospect
