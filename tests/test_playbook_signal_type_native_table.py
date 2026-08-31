import json
from pathlib import Path

ROOT = Path("sales_engagement_intelligence/sales_engagement_and_intelligence")


def test_playbook_uses_native_managed_signal_type_child_table():
    schema = json.loads((ROOT / "doctype/sei_playbook/sei_playbook.json").read_text())
    fields = {field["fieldname"]: field for field in schema["fields"]}
    signal_types = fields["signal_types"]
    assert signal_types["fieldtype"] == "Table"
    assert signal_types["options"] == "SEI Playbook Signal Type"


def test_bidirectional_sync_keeps_native_table_and_signal_type_link_aligned():
    playbook = (ROOT / "doctype/sei_playbook/sei_playbook.py").read_text()
    signal_type = (ROOT / "doctype/sei_signal_type/sei_signal_type.py").read_text()
    assert "self.validate_signal_types()" in playbook
    assert "self.sync_signal_type_links()" in playbook
    assert "self.sync_playbook_child_row()" in signal_type


def test_restore_patch_repopulates_native_table_from_signal_type_playbook():
    patch = Path(
        "sales_engagement_intelligence/patches/v0_0_1/restore_playbook_signal_type_management_table.py"
    ).read_text()
    patches = Path("sales_engagement_intelligence/patches.txt").read_text()
    assert 'frappe.db.delete("SEI Playbook Signal Type")' in patch
    assert '"parent": row.playbook' in patch
    assert "restore_playbook_signal_type_management_table" in patches
