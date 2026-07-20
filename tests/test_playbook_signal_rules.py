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
