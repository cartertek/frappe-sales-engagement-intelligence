from __future__ import annotations

import json
from pathlib import Path

APP = Path("sales_engagement_intelligence")
MODULE = APP / "sales_engagement_and_intelligence"
SIGNAL_JSON = MODULE / "doctype" / "sei_signal" / "sei_signal.json"
SIGNAL_JS = MODULE / "doctype" / "sei_signal" / "sei_signal.js"
PROSPECTING_SIDEBAR = APP / "workspace_sidebar" / "prospecting.json"
TOUCHPOINTS_SIDEBAR = APP / "workspace_sidebar" / "touchpoints.json"


def test_signal_form_uses_collapsed_type_definition_and_compact_textareas():
    signal = json.loads(SIGNAL_JSON.read_text())
    fields = {field["fieldname"]: field for field in signal["fields"]}

    for fieldname in (
        "signal_type_definition_section",
        "qualification_section",
        "review_section",
    ):
        section = fields[fieldname]
        assert section["fieldtype"] == "Section Break"
        assert section["collapsible"] == 1
    assert signal["field_order"].index("signal_type_definition_section") < signal[
        "field_order"
    ].index("criteria_html")

    source = SIGNAL_JS.read_text()
    assert "onload_post_render(frm)" in source
    assert "collapse_default_sections(frm)" in source
    assert "field.section.collapse(true)" in source
    assert "'qualification_section'" in source
    assert "'review_section'" in source
    assert "height: '88px'" in source
    for fieldname in (
        "observed_fact",
        "signal_claim",
        "why_this_signal_type",
        "why_not_weak",
        "disqualifiers_checked",
        "evidence_gap_reason",
        "evidence_notes",
        "manual_override_reason",
    ):
        assert f"'{fieldname}'" in source


def test_prospecting_is_the_only_sidebar_owner_for_prospects_and_signals():
    canonical = json.loads(PROSPECTING_SIDEBAR.read_text())
    canonical_targets = {item.get("link_to") for item in canonical["items"]}
    assert {"SEI Prospect", "SEI Signal"} <= canonical_targets

    for sidebar_path in (APP / "workspace_sidebar").glob("*.json"):
        if sidebar_path == PROSPECTING_SIDEBAR:
            continue
        sidebar = json.loads(sidebar_path.read_text())
        targets = {item.get("link_to") for item in sidebar["items"]}
        assert not ({"SEI Prospect", "SEI Signal"} & targets), sidebar_path


def test_touchpoints_is_the_only_sidebar_owner_for_interaction_attribution():
    canonical = json.loads(TOUCHPOINTS_SIDEBAR.read_text())
    canonical_targets = {item.get("link_to") for item in canonical["items"]}
    assert "SEI Interaction Attribution" in canonical_targets

    for sidebar_path in (APP / "workspace_sidebar").glob("*.json"):
        if sidebar_path == TOUCHPOINTS_SIDEBAR:
            continue
        sidebar = json.loads(sidebar_path.read_text())
        targets = {item.get("link_to") for item in sidebar["items"]}
        assert "SEI Interaction Attribution" not in targets, sidebar_path

    prospecting = json.loads(
        (MODULE / "workspace" / "prospecting" / "prospecting.json").read_text()
    )
    shortcuts = {shortcut.get("link_to") for shortcut in prospecting["shortcuts"]}
    assert "SEI Interaction Attribution" in shortcuts


def test_redundant_signals_workspace_is_removed_and_migration_cleans_live_records():
    assert not (APP / "desktop_icon" / "signals.json").exists()
    assert not (APP / "workspace_sidebar" / "signals.json").exists()
    assert not (MODULE / "workspace" / "signals" / "signals.json").exists()

    setup = (APP / "setup" / "__init__.py").read_text()
    assert "consolidate_prospecting_navigation()" in setup
    assert '("Workspace Sidebar", "Signals")' in setup
    assert '("Workspace", "Signals")' in setup
    assert "SEI_CANONICAL_RESEARCH_DOCTYPES" in setup
    assert "SEI_CANONICAL_TOUCHPOINT_DOCTYPES" in setup
