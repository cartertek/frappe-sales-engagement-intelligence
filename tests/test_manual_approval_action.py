import json
from pathlib import Path

ROOT = Path('sales_engagement_intelligence/sales_engagement_and_intelligence')
JS = (ROOT / 'doctype/sei_prospect/sei_prospect.js').read_text()
API = (ROOT / 'api.py').read_text()
LIFECYCLE = (ROOT / 'services/lifecycle.py').read_text()
QUALIFICATION = (ROOT / 'services/qualification.py').read_text()
SCHEMA = json.loads((ROOT / 'doctype/sei_prospect/sei_prospect.json').read_text())

def test_manual_approval_uses_required_popup_action():
    assert "add_prospect_action(frm, 'Manually Approve'" in JS
    assert "call_and_reload(frm, 'manually_approve_prospect'" in JS
    assert "__('Manual Qualification Reason')" in JS
    assert "}, true);" in JS

def test_manual_approval_has_manager_protected_api_and_service():
    block = API.split('def manually_approve_prospect', 1)[1].split('@api_endpoint', 1)[0]
    assert '_require_manager()' in block
    assert 'return manually_approve_prospect(prospect, reason)' in block
    assert 'def manually_approve_prospect(prospect_name: str, reason: str)' in LIFECYCLE
    assert 'Manual Qualification Reason is required.' in LIFECYCLE
    assert 'lifecycle = apply_lifecycle_status(prospect_name)' in LIFECYCLE

def test_manual_approval_status_replaces_boolean_override():
    fields = {f['fieldname']: f for f in SCHEMA['fields']}
    assert 'manual_qualification_override' not in fields
    assert fields['manual_qualification_reason']['hidden'] == 1
    assert fields['manual_qualification_reason']['read_only'] == 1
    assert 'prospect.qualification_status == "Manually Approved"' in QUALIFICATION
    assert 'prospect.manual_qualification_override' not in QUALIFICATION
