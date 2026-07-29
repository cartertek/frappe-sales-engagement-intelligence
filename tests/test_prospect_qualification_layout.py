import json
from pathlib import Path

SCHEMA = json.loads(Path(
    'sales_engagement_intelligence/sales_engagement_and_intelligence/doctype/'
    'sei_prospect/sei_prospect.json'
).read_text())


def test_qualification_explanation_stays_in_left_column_before_count_column_break():
    order = [field['fieldname'] for field in SCHEMA['fields']]
    assert order.index('qualification_status') < order.index('qualification_explanation')
    assert order.index('qualification_explanation') < order.index('column_break_2')
    assert order.index('column_break_2') < order.index('qualified_signal_count')
    assert order.index('qualified_signal_count') < order.index('strong_observed_signal_count')
    assert order.index('strong_observed_signal_count') < order.index('moderate_observed_signal_count')
    assert order.index('moderate_observed_signal_count') < order.index('signals_section')
