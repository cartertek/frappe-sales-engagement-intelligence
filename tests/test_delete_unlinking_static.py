from __future__ import annotations

from pathlib import Path

APP = Path("sales_engagement_intelligence")
MODULE = APP / "sales_engagement_and_intelligence"
SERVICE = MODULE / "services" / "delete_unlinking.py"


def test_delete_unlinking_covers_the_sei_crm_cycle():
    source = SERVICE.read_text()

    expected_links = {
        '("CRM Deal", "sei_prospect")',
        '("CRM Deal", "sei_primary_signal")',
        '("SEI Signal", "prospect")',
        '("SEI Prospect", "crm_deal")',
        '("SEI Interaction Attribution", "prospect")',
        '("SEI Interaction Attribution", "signal")',
        '("SEI Interaction Attribution", "crm_deal")',
    }
    for link in expected_links:
        assert link in source

    assert "update_modified=False" in source
    assert "frappe.db.set_value" in source
    assert "frappe.delete_doc" not in source


def test_prospect_and_signal_unlink_before_frappe_link_validation():
    prospect = (MODULE / "doctype" / "sei_prospect" / "sei_prospect.py").read_text()
    signal = (MODULE / "doctype" / "sei_signal" / "sei_signal.py").read_text()

    assert "def on_trash(self):" in prospect
    assert "delete_unlinking.unlink_references_before_delete(self)" in prospect
    assert "def on_trash(self):" in signal
    assert signal.index("delete_unlinking.unlink_references_before_delete(self)") < signal.index(
        "self.recalculate_prospect()", signal.index("def on_trash(self):")
    )


def test_crm_deal_hooks_unlink_and_repair_prospect_lifecycle():
    hooks = (APP / "hooks.py").read_text()
    service = SERVICE.read_text()

    assert '"CRM Deal": {' in hooks
    assert '"on_trash"' in hooks
    assert "unlink_references_before_delete" in hooks
    assert '"after_delete"' in hooks
    assert "restore_prospect_lifecycle_after_deal_delete" in hooks
    assert '"Converted to CRM Lead"' in service
    assert "suggest_pre_crm_handoff_status" in service
