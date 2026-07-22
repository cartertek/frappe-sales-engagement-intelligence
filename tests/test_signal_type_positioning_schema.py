import json
from pathlib import Path

SCHEMA = Path(
    'sales_engagement_intelligence/sales_engagement_and_intelligence/doctype/'
    'sei_signal_type/sei_signal_type.json'
)


def load_schema():
    return json.loads(SCHEMA.read_text())


def test_signal_type_form_has_expected_tabs_and_order():
    schema = load_schema()
    order = schema['field_order']
    fields = {field['fieldname']: field for field in schema['fields']}

    assert [fields[name]['label'] for name in ('overview_tab', 'definition_tab', 'positioning_tab')] == [
        'Overview',
        'Definition',
        'Positioning',
    ]
    assert all(fields[name]['fieldtype'] == 'Tab Break' for name in (
        'overview_tab',
        'definition_tab',
        'positioning_tab',
    ))
    assert order.index('overview_tab') < order.index('signal_type_name')
    assert order.index('definition_tab') < order.index('evidence_criteria_section')
    assert order.index('positioning_tab') > order.index('positive_examples')


def test_overview_tab_contains_only_overview_fields_before_definition():
    order = load_schema()['field_order']
    overview_fields = order[order.index('overview_tab') + 1 : order.index('definition_tab')]
    assert overview_fields == [
        'signal_type_name',
        'description',
        'playbook',
        'research_arena',
        'active',
    ]


def test_positioning_tab_contains_three_long_text_fields():
    schema = load_schema()
    order = schema['field_order']
    fields = {field['fieldname']: field for field in schema['fields']}
    positioning_fields = order[order.index('positioning_tab') + 1 :]

    assert positioning_fields == [
        'likely_business_impact',
        'cartertek_relevance',
        'message_guidance',
    ]
    assert all(fields[name]['fieldtype'] == 'Long Text' for name in positioning_fields)
