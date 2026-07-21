import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCTYPE = ROOT / 'sales_engagement_intelligence/sales_engagement_and_intelligence/doctype'


def test_signal_rule_requires_signal_type():
    data = json.loads((DOCTYPE / 'sei_playbook_signal_rule/sei_playbook_signal_rule.json').read_text())
    fields = {field['fieldname']: field for field in data['fields']}
    assert fields['signal_type']['reqd'] == 1


def test_playbook_drops_completely_blank_signal_rules_before_validation():
    source = (DOCTYPE / 'sei_playbook/sei_playbook.py').read_text()
    assert 'self.remove_blank_signal_rules()' in source
    assert 'def remove_blank_signal_rules' in source
    assert 'self.set("signal_rules", rows)' in source


def test_playbook_form_removes_blank_signal_rules_on_load_and_before_save():
    source = (DOCTYPE / 'sei_playbook/sei_playbook.js').read_text()
    assert 'refresh(frm)' in source
    assert 'before_save(frm)' in source
    assert source.count('remove_blank_signal_rule_rows(frm);') == 2
    assert "frm.doc.signal_rules = retained;" in source
    assert "frm.refresh_field('signal_rules');" in source
    assert "value.trim()" in source


def test_blank_signal_rule_cleanup_patch_is_registered():
    patches = (ROOT / 'sales_engagement_intelligence/patches.txt').read_text()
    entry = 'sales_engagement_intelligence.patches.v0_0_1.remove_blank_playbook_signal_rules'
    assert entry in patches.splitlines()

    patch = (
        ROOT
        / 'sales_engagement_intelligence/patches/v0_0_1/remove_blank_playbook_signal_rules.py'
    ).read_text()
    assert 'DELETE FROM `tabSEI Playbook Signal Rule`' in patch
    assert "TRIM(COALESCE(signal_type, '')) = ''" in patch
    assert "TRIM(COALESCE(notes, '')) = ''" in patch
