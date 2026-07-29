from pathlib import Path

SCRIPT = Path(
    "sales_engagement_intelligence/sales_engagement_and_intelligence/doctype/"
    "sei_signal/sei_signal.js"
).read_text()


def _source_url_handler_block():
    return SCRIPT.split("const isolate_source_url_link", 1)[1].split(
        "$(frm.wrapper).on('grid-row-render.sei-observed-facts'", 1
    )[0]


def test_source_url_link_is_intercepted_during_capture_before_row_editor():
    block = _source_url_handler_block()
    assert '.grid-static-col[data-fieldname="source_url"] a[href]' in block
    assert "addEventListener('mousedown', isolate_source_url_link, true)" in block
    assert "addEventListener('click', isolate_source_url_link, true)" in block
    assert "event.stopPropagation()" in block


def test_source_url_handler_does_not_cancel_link_navigation():
    block = _source_url_handler_block()
    assert "preventDefault" not in block
    assert "stopImmediatePropagation" not in block


def test_source_url_handler_is_not_delegated_from_grid_wrapper():
    assert "mousedown.sei-observed-fact-url" not in SCRIPT
    assert "click.sei-observed-fact-url" not in SCRIPT
