import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SERVICES = (
    ROOT
    / "sales_engagement_intelligence"
    / "sales_engagement_and_intelligence"
    / "services"
)
SYNC = SERVICES / "prospect_signal_type_sync.py"
CONTACTS = SERVICES / "contacts.py"


def test_taxonomy_sync_persists_contact_roles_directly():
    text = SYNC.read_text()
    assert "sync_required_contact_roles(prospect)" in text
    assert 'frappe.get_doc("SEI Prospect", prospect)' not in text


def test_direct_contact_role_sync_inserts_child_rows():
    tree = ast.parse(CONTACTS.read_text())
    fn = next(
        node
        for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name == "sync_required_contact_roles"
    )
    calls = [node for node in ast.walk(fn) if isinstance(node, ast.Call)]
    assert any(
        isinstance(call.func, ast.Attribute) and call.func.attr == "db_insert"
        for call in calls
    )
    assert any(
        isinstance(node, ast.Constant) and node.value == "SEI Prospect Contact"
        for node in ast.walk(fn)
    )


def test_validation_helper_reports_whether_document_changed():
    tree = ast.parse(CONTACTS.read_text())
    fn = next(
        node
        for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name == "ensure_required_contact_roles"
    )
    returns = [node for node in ast.walk(fn) if isinstance(node, ast.Return)]
    assert any(
        isinstance(node.value, ast.Name) and node.value.id == "changed"
        for node in returns
    )
