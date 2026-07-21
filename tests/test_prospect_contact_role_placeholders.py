import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SERVICES = ROOT / "sales_engagement_intelligence" / "sales_engagement_and_intelligence" / "services"
CONTACTS = SERVICES / "contacts.py"
SYNC = SERVICES / "prospect_signal_type_sync.py"
PROSPECT = (
    ROOT
    / "sales_engagement_intelligence"
    / "sales_engagement_and_intelligence"
    / "doctype"
    / "sei_prospect"
    / "sei_prospect.py"
)
SCRIPT = (
    ROOT
    / "sales_engagement_intelligence"
    / "sales_engagement_and_intelligence"
    / "doctype"
    / "sei_prospect"
    / "sei_prospect.js"
)
PATCH = (
    ROOT
    / "sales_engagement_intelligence"
    / "patches"
    / "v0_0_1"
    / "remove_persisted_contact_role_placeholders.py"
)


def test_taxonomy_sync_does_not_persist_contact_role_placeholders():
    source = SYNC.read_text()
    assert "sync_required_contact_roles" not in source
    assert "SEI Prospect Contact" not in source


def test_prospect_validation_removes_role_only_contact_rows():
    source = PROSPECT.read_text()
    assert "remove_empty_contact_role_placeholders(self)" in source


def test_contact_service_distinguishes_real_contacts_and_missing_roles():
    tree = ast.parse(CONTACTS.read_text())
    names = {node.name for node in tree.body if isinstance(node, ast.FunctionDef)}
    assert {"is_real_contact", "required_contact_roles", "missing_required_contact_roles"} <= names
    assert "def sync_required_contact_roles" not in CONTACTS.read_text()
    assert "def ensure_required_contact_roles" not in CONTACTS.read_text()


def test_contact_grid_renders_virtual_roles_without_mutating_the_document_on_load():
    source = SCRIPT.read_text()
    assert "grid.get_data =" not in source
    assert "__sei_original_get_data" not in source
    assert "render_virtual_contact_role_rows(frm, field)" in source
    assert "template.clone(false, false)" in source
    assert "rows.append(placeholder)" in source
    assert "load_missing_contact_roles(frm, field)" in source
    render_start = source.index("function render_virtual_contact_role_rows")
    materialize_start = source.index("function materialize_virtual_contact_role")
    assert "frm.add_child('contacts'" not in source[render_start:materialize_start]
    assert "frm.doc.__unsaved" not in source
    assert "__sei_contact_role_placeholder" not in source


def test_virtual_contact_role_materializes_only_after_user_click():
    source = SCRIPT.read_text()
    assert "placeholder.on('click.sei_virtual_contact_role'" in source
    assert "materialize_virtual_contact_role(frm, field, role)" in source
    assert "const row = frm.add_child('contacts', { contact_role: role, is_primary: 0 })" in source
    assert "grid_row.toggle_view(true)" in source


def test_patch_deletes_only_role_only_contact_children():
    source = PATCH.read_text()
    for field in ("contact_name", "emails", "notes", "crm_contact"):
        assert field in source
    assert "is_primary" not in source
    assert "DELETE FROM `tabSEI Prospect Contact`" in source
