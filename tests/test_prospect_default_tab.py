from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = (
    ROOT
    / "sales_engagement_intelligence"
    / "sales_engagement_and_intelligence"
    / "doctype"
    / "sei_prospect"
    / "sei_prospect.js"
)


def test_prospect_activates_status_appropriate_default_tab_after_render():
    source = SCRIPT.read_text()

    assert "onload_post_render(frm)" in source
    assert "activate_default_prospect_tab(frm)" in source
    assert "'Needs Research': 'qualification_tab'" in source
    assert "'Research Complete': 'qualification_tab'" in source
    assert "Qualified: 'qualification_tab'" in source
    assert "'Find Contact': 'outreach_tab'" in source
    assert "'Ready for CRM Conversion': 'outreach_tab'" in source
    assert "|| 'overview_tab'" in source
    assert "tab?.set_active()" in source


def test_default_tab_selection_does_not_run_on_each_refresh():
    source = SCRIPT.read_text()
    refresh_body = source.split("refresh(frm) {", 1)[1].split("\n    },", 1)[0]

    assert "activate_default_prospect_tab" not in refresh_body
