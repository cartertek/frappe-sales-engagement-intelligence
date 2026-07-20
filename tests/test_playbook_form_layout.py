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


def test_playbook_scalar_fields_precede_managed_tables():
    data = json.loads((DOCTYPE_DIR / 'sei_playbook.json').read_text())
    field_order = data['field_order']
    scalar_fields = [
        'playbook_name',
        'active',
        'description',
        'thesis',
        'typical_prospect_types',
        'default_offer',
        'default_asset',
        'qualifying_signal_guidance',
        'disqualifying_guidance',
        'recommended_first_action',
        'follow_up_guidance',
        'notes',
    ]
    managed_fields = [
        'research_arenas_section',
        'research_arenas',
        'contact_roles_section',
        'contact_roles',
        'signal_types_section',
        'signal_types',
        'signal_rules',
    ]
    assert field_order == scalar_fields + managed_fields


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
