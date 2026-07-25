import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCTYPE_DIR = (
    ROOT
    / 'sales_engagement_intelligence'
    / 'sales_engagement_and_intelligence'
    / 'doctype'
    / 'sei_playbook'
)


def test_playbook_fields_are_declared_once_and_grouped_by_tabs():
    data = json.loads((DOCTYPE_DIR / 'sei_playbook.json').read_text())
    field_order = data['field_order']
    actual = [field['fieldname'] for field in data['fields']]
    assert len(actual) == len(set(actual))
    assert set(actual) == set(field_order)
    assert (
        field_order.index('overview_tab')
        < field_order.index('qualification_tab')
        < field_order.index('outreach_tab')
    )
    assert field_order.index('signal_types') < field_order.index('signal_qualification_script')
    assert field_order.index('signal_qualification_script') < field_order.index(
        'qualification_guidance_section'
    )
    assert field_order.index('default_offer') < field_order.index('contact_roles')


def test_playbook_textareas_match_signal_form_height():
    script = (DOCTYPE_DIR / 'sei_playbook.js').read_text()
    text_fields = {
        'description',
        'thesis',
        'typical_prospect_types',
        'qualifying_signal_guidance',
        'disqualifying_guidance',
        'follow_up_guidance',
        'notes',
    }
    for fieldname in text_fields:
        assert f"'{fieldname}'" in script
    assert "height: '88px'" in script
    assert "'min-height': '88px'" in script


def test_playbook_contact_roles_support_signal_specific_relevance():
    path = DOCTYPE_DIR.parent / 'sei_playbook_contact_role' / 'sei_playbook_contact_role.json'
    fields = {field['fieldname']: field for field in json.loads(path.read_text())['fields']}
    assert fields['signal_specific_relevance']['fieldtype'] == 'Check'
    assert fields['signal_specific_relevance']['default'] == 0
    assert fields['signal_specific_relevance']['in_list_view'] == 1
