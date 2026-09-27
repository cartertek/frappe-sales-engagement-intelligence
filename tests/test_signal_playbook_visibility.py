import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SIGNAL_JSON = ROOT / 'sales_engagement_intelligence/sales_engagement_and_intelligence/doctype/sei_signal/sei_signal.json'
PROSPECT_JS = ROOT / 'sales_engagement_intelligence/sales_engagement_and_intelligence/doctype/sei_prospect/sei_prospect.js'
API = ROOT / 'sales_engagement_intelligence/sales_engagement_and_intelligence/api.py'
SIGNAL_PY = ROOT / 'sales_engagement_intelligence/sales_engagement_and_intelligence/doctype/sei_signal/sei_signal.py'
SIGNAL_TYPE_PY = ROOT / 'sales_engagement_intelligence/sales_engagement_and_intelligence/doctype/sei_signal_type/sei_signal_type.py'


def test_signal_form_shows_read_only_playbook_immediately_before_signal_type():
    schema = json.loads(SIGNAL_JSON.read_text())
    order = schema['field_order']
    field = next(f for f in schema['fields'] if f.get('fieldname') == 'playbook')
    assert order.index('playbook') + 1 == order.index('signal_type')
    assert field['fieldtype'] == 'Link'
    assert field['options'] == 'SEI Playbook'
    assert field['read_only'] == 1
    assert field['fetch_from'] == 'signal_type.playbook'


def test_signal_playbook_is_derived_and_exposed_to_prospect_table():
    assert 'self.playbook = get_signal_type_playbook(self.signal_type)' in SIGNAL_PY.read_text()
    assert '"playbook",' in API.read_text()
    source = PROSPECT_JS.read_text()
    assert "<th>${__('Signal Type')}</th>\n                            <th>${__('Playbook')}</th>" in source
    assert "frappe.utils.escape_html(signal.playbook || '')" in source


def test_signal_type_playbook_changes_resync_existing_signals():
    source = SIGNAL_TYPE_PY.read_text()
    assert 'UPDATE `tabSEI Signal`' in source
    assert 'SET playbook = %s' in source
    assert 'WHERE signal_type = %s' in source
