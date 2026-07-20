import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SYNC = (
    ROOT
    / "sales_engagement_intelligence/sales_engagement_and_intelligence/services"
    / "prospect_signal_type_sync.py"
)
CONTACTS = (
    ROOT
    / "sales_engagement_intelligence/sales_engagement_and_intelligence/services"
    / "contacts.py"
)


def test_taxonomy_sync_also_synchronizes_contact_roles():
    text = SYNC.read_text()
    assert "ensure_required_contact_roles(prospect_doc)" in text
    assert "prospect_doc.save(ignore_permissions=True)" in text


def test_contact_role_sync_reports_whether_it_changed_the_document():
    tree = ast.parse(CONTACTS.read_text())
    fn = next(
        node
        for node in tree.body
        if isinstance(node, ast.FunctionDef)
        and node.name == "ensure_required_contact_roles"
    )
    returns = [node for node in ast.walk(fn) if isinstance(node, ast.Return)]
    assert any(
        isinstance(node.value, ast.Name) and node.value.id == "changed"
        for node in returns
    )
