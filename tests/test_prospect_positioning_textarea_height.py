from pathlib import Path

PROSPECT_JS = Path(
    "sales_engagement_intelligence/sales_engagement_and_intelligence/doctype/"
    "sei_prospect/sei_prospect.js"
)


def test_prospect_positioning_textareas_match_signal_form_height():
    source = PROSPECT_JS.read_text()

    assert "'signal_summary'" in source
    assert "'contact_target_notes'" in source
    assert "height: '88px'" in source
    assert "'min-height': '88px'" in source
    assert "size_prospect_positioning_textareas(frm);" in source
