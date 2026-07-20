import importlib.util
import sys
import types
from pathlib import Path

CONTACTS = Path(
    "sales_engagement_intelligence/sales_engagement_and_intelligence/services/contacts.py"
)
CRM = Path(
    "sales_engagement_intelligence/sales_engagement_and_intelligence/services/crm_preparation.py"
)


def load_contacts_module(monkeypatch):
    monkeypatch.setitem(sys.modules, "frappe", types.SimpleNamespace())
    spec = importlib.util.spec_from_file_location("contacts_under_test", CONTACTS)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_populated_contacts_requires_name_or_email(monkeypatch):
    contacts = load_contacts_module(monkeypatch)
    rows = [
        {"contact_role": "Owner"},
        {"contact_role": "CTO", "notes": "Research this person"},
        {"contact_role": "CEO", "contact_name": "Ada Lovelace"},
        {"contact_role": "VP", "emails": "first@example.com\nsecond@example.com"},
    ]
    assert contacts.populated_contacts({"contacts": rows}) == rows[2:]


def test_crm_conversion_only_upserts_populated_contacts():
    source = CRM.read_text()
    assert "for row in populated_contacts(prospect)" in source
