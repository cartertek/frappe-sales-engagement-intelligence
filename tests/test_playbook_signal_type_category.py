from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCTYPE_ROOT = ROOT / "sales_engagement_intelligence" / "sales_engagement_and_intelligence" / "doctype"


def test_playbook_signal_type_view_is_derived_from_signal_type_playbook():
    source = (DOCTYPE_ROOT / "sei_playbook" / "sei_playbook.js").read_text()
    assert "frappe.db.get_list('SEI Signal Type'" in source
    assert "filters: { playbook: frm.doc.name }" in source
    assert "Manage Signal Types" in source
    assert "frappe.set_route('List', 'SEI Signal Type', { playbook: frm.doc.name })" in source


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
