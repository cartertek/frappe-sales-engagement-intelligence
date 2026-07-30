from pathlib import Path

SIGNAL_JS = Path(
    "sales_engagement_intelligence/sales_engagement_and_intelligence/doctype/sei_signal/sei_signal.js"
).read_text()


def test_observed_fact_text_keeps_explicit_emphasis_while_draft_fields_are_optional():
    assert '.grid-static-col[data-fieldname="fact"] .static-area' in SIGNAL_JS
    assert "'font-weight': '600'" in SIGNAL_JS
