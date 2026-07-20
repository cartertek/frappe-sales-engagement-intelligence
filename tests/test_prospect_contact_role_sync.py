from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SERVICES = ROOT / "sales_engagement_intelligence" / "sales_engagement_and_intelligence" / "services"
SYNC = SERVICES / "prospect_signal_type_sync.py"
CONTACTS = SERVICES / "contacts.py"


def test_taxonomy_sync_only_updates_taxonomy_snapshots():
    source = SYNC.read_text()
    assert "sync_required_contact_roles" not in source
    assert 'frappe.get_doc("SEI Prospect", prospect)' not in source


def test_contact_service_no_longer_persists_required_roles():
    source = CONTACTS.read_text()
    assert "sync_required_contact_roles" not in source
    assert "ensure_required_contact_roles" not in source
    assert "missing_required_contact_roles" in source
