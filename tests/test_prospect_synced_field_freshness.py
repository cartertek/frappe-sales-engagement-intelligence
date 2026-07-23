from pathlib import Path

SERVICES = Path(
    "sales_engagement_intelligence/sales_engagement_and_intelligence/services"
)


def test_taxonomy_sync_invalidates_cached_prospect_rows_only_on_change():
    source = (SERVICES / "prospect_signal_type_sync.py").read_text()
    assert 'frappe.db.get_value(' in source
    assert 'update_modified=True' in source
    assert 'frappe.get_doc("SEI Prospect", prospect).notify_update()' in source
    assert 'update_modified=False' not in source


def test_emails_sent_sync_invalidates_cached_prospect_rows_only_on_change():
    source = (SERVICES / "prospect_message_draft_sync.py").read_text()
    assert 'current = frappe.db.get_value("SEI Prospect", prospect, "emails_sent") or 0' in source
    assert 'if int(current) == emails_sent:' in source
    assert 'update_modified=True' in source
    assert 'frappe.get_doc("SEI Prospect", prospect).notify_update()' in source
    assert 'update_modified=False' not in source


def test_prospect_list_requests_all_synced_fields():
    script = Path(
        "sales_engagement_intelligence/sales_engagement_and_intelligence/doctype/"
        "sei_prospect/sei_prospect_list.js"
    ).read_text()
    for fieldname in ("signals", "playbooks", "arenas", "emails_sent"):
        assert f"'{fieldname}'" in script
