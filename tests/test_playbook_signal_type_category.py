from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCTYPE_ROOT = ROOT / "sales_engagement_intelligence" / "sales_engagement_and_intelligence" / "doctype"


def test_playbook_signal_type_view_is_derived_from_signal_type_playbook():
    source = (DOCTYPE_ROOT / "sei_playbook" / "sei_playbook.js").read_text()
    assert "frappe.db.get_list('SEI Signal Type'" in source
    assert "filters: { playbook: frm.doc.name }" in source
    assert "Add / Move Existing" in source
    assert "New Signal Type" in source
    assert "sei-edit-signal-type" in source
    assert "sei-move-signal-type" in source
    assert "assign_signal_type" in source
    assert "update_signal_type_from_playbook" in source
    assert "move_signal_type" in source


def test_legacy_duplicate_playbook_signal_type_rows_are_removed():
    patch = (
        ROOT
        / "sales_engagement_intelligence"
        / "patches"
        / "v0_0_1"
        / "remove_duplicate_playbook_signal_type_relationship.py"
    ).read_text()
    patches = (ROOT / "sales_engagement_intelligence" / "patches.txt").read_text()
    assert 'frappe.db.delete("SEI Playbook Signal Type")' in patch
    assert "remove_duplicate_playbook_signal_type_relationship" in patches


def test_playbook_signal_type_management_writes_canonical_signal_type_link():
    controller = (DOCTYPE_ROOT / "sei_playbook" / "sei_playbook.py").read_text()
    assert "def assign_signal_type(" in controller
    assert "signal_type_doc.playbook = playbook_doc.name" in controller
    assert "def update_signal_type_from_playbook(" in controller
    assert "def move_signal_type(" in controller
    assert "signal_type_doc.playbook = target.name" in controller
    assert "SEI Playbook Signal Type" not in controller
