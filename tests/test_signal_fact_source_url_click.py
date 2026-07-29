from pathlib import Path

SCRIPT = Path(
    "sales_engagement_intelligence/sales_engagement_and_intelligence/doctype/"
    "sei_signal/sei_signal.js"
).read_text()


def test_source_url_link_click_does_not_open_fact_row_editor():
    assert "mousedown.sei-observed-fact-url click.sei-observed-fact-url" in SCRIPT
    assert '.grid-static-col[data-fieldname="source_url"] a[href]' in SCRIPT
    assert "event => event.stopPropagation()" in SCRIPT


def test_source_url_handler_does_not_cancel_link_navigation():
    block = SCRIPT.split("mousedown.sei-observed-fact-url", 1)[1].split(
        "$(frm.wrapper).on('grid-row-render.sei-observed-facts'", 1
    )[0]
    assert "preventDefault" not in block
    assert "stopImmediatePropagation" not in block
