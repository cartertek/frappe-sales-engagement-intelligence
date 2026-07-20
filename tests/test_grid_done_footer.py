from pathlib import Path

SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "sales_engagement_intelligence"
    / "sales_engagement_and_intelligence"
    / "doctype"
    / "sei_prospect"
    / "sei_prospect.js"
).read_text()


def test_done_footer_is_moved_outside_scrollable_grid_body():
    assert ".insertAfter($body)" in SCRIPT
    assert "data-sei-fixed-footer" in SCRIPT
    assert "$form.children('.grid-footer-toolbar')" in SCRIPT
