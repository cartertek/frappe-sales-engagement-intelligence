from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "sales_engagement_intelligence" / "sales_engagement_and_intelligence"


def test_runtime_code_does_not_write_legacy_playbook_signal_type_rows():
    runtime_files = [
        APP / "doctype/sei_playbook/sei_playbook.py",
        APP / "doctype/sei_signal_type/sei_signal_type.py",
    ]
    for path in runtime_files:
        source = path.read_text()
        assert "SEI Playbook Signal Type" not in source


def test_playbook_form_explains_canonical_assignment_location():
    schema = (APP / "doctype/sei_playbook/sei_playbook.json").read_text()
    assert "Derived from the Playbook field on SEI Signal Type" in schema
    assert "Edit Signal Types to change assignments" in schema
