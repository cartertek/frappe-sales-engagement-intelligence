from __future__ import annotations

import json
from pathlib import Path

APP = Path("sales_engagement_intelligence")
DOCTYPE_ROOT = APP / "sales_engagement_and_intelligence" / "doctype"
API = APP / "sales_engagement_and_intelligence" / "api.py"
SETUP = APP / "setup" / "__init__.py"
PROSPECT_JS = DOCTYPE_ROOT / "sei_prospect" / "sei_prospect.js"
PROSPECTING_WORKSPACE = (
    APP / "sales_engagement_and_intelligence" / "workspace" / "prospecting" / "prospecting.json"
)


def _doctype(folder: str) -> dict:
    return json.loads((DOCTYPE_ROOT / folder / f"{folder}.json").read_text())


def test_milestone_8_doctypes_exist_with_required_links_and_no_sending_fields():
    playbook = _doctype("sei_playbook")
    template = _doctype("sei_message_template")
    rule = _doctype("sei_playbook_signal_rule")

    assert playbook["name"] == "SEI Playbook"
    assert playbook["autoname"] == "field:playbook_name"
    assert playbook["title_field"] == "playbook_name"
    playbook_fields = {field["fieldname"]: field for field in playbook["fields"]}
    assert playbook_fields["default_thesis"]["options"] == "SEI Thesis"
    assert playbook_fields["default_asset"]["options"] == "SEI Asset"
    assert playbook_fields["signal_rules"]["options"] == "SEI Playbook Signal Rule"

    assert rule.get("istable") == 1
    rule_fields = {field["fieldname"]: field for field in rule["fields"]}
    assert rule_fields["signal_type"]["fieldtype"] == "Select"
    assert rule_fields["exclude_from_qualification"]["fieldtype"] == "Check"

    assert template["name"] == "SEI Message Template"
    template_fields = {field["fieldname"]: field for field in template["fields"]}
    assert template_fields["playbook"]["options"] == "SEI Playbook"
    assert template_fields["thesis"]["options"] == "SEI Thesis"
    assert template_fields["asset"]["options"] == "SEI Asset"
    assert "Email" in template_fields["channel"]["options"]

    forbidden = {"send", "send_email", "smtp", "communication"}
    assert not forbidden & set(playbook_fields)
    assert not forbidden & set(template_fields)


def test_prospect_has_playbook_assignment_fields():
    prospect = _doctype("sei_prospect")
    fields = {field["fieldname"]: field for field in prospect["fields"]}
    assert fields["sei_playbook"]["fieldtype"] == "Link"
    assert fields["sei_playbook"]["options"] == "SEI Playbook"
    assert fields["suggested_message_template"]["options"] == "SEI Message Template"
    assert fields["playbook_guidance"].get("read_only") == 1


def test_api_exposes_draft_and_playbook_helpers_without_send_operations():
    source = API.read_text()
    assert "def apply_playbook_defaults" in source
    assert "def preview_message_draft" in source
    assert "@api_endpoint\ndef preview_message_draft" in source
    assert "sendmail" not in source
    assert "enqueue" not in source

    drafting = (APP / "sales_engagement_and_intelligence" / "services" / "drafting.py").read_text()
    assert "preview_message_draft" in drafting
    assert "sendmail" not in drafting
    assert "Communication" not in drafting
    assert "lifecycle_status" not in drafting


def test_seed_patch_includes_required_playbooks_and_templates():
    seed = (APP / "patches" / "v0_0_1" / "seed_playbooks_and_templates.py").read_text()
    for playbook in [
        "Agency Overflow",
        "Failed Hiring",
        "Launch Aftermath",
        "Technical Distress",
        "Partner / Referral",
        "Reactivation",
    ]:
        assert playbook in seed
    assert "SEI Message Template" in seed
    assert "seed_playbooks_and_templates" in (APP / "patches.txt").read_text()


def test_workspace_and_after_migrate_include_final_navigation_validation():
    setup_source = SETUP.read_text()
    assert "ensure_milestone_8_seed_data()" in setup_source
    assert "ensure_milestone_8_workspace_items()" in setup_source
    assert "def validate_milestone_8_workspace_items()" in setup_source

    workspace = json.loads(PROSPECTING_WORKSPACE.read_text())
    labels = {shortcut["label"] for shortcut in workspace["shortcuts"]}
    assert {"SEI Playbooks", "SEI Message Templates", "Interaction Attribution"} <= labels
    content = json.loads(workspace["content"])
    content_labels = {
        item.get("data", {}).get("shortcut_name")
        for item in content
        if isinstance(item, dict) and item.get("type") == "shortcut"
    }
    assert {"SEI Playbooks", "SEI Message Templates"} <= content_labels


def test_prospect_form_has_user_triggered_draft_and_playbook_actions():
    source = PROSPECT_JS.read_text()
    assert "Apply Playbook Defaults" in source
    assert "Preview Message Draft" in source
    assert "preview_message_draft" in source
    assert "sendmail" not in source
    assert "frappe.confirm(__('Apply playbook defaults to blank fields only?" in source


def test_prospect_form_uses_operator_tabs_for_large_schema():
    prospect = _doctype("sei_prospect")
    tabs = [
        field["label"]
        for field in prospect["fields"]
        if field.get("fieldtype") == "Tab Break"
    ]
    assert tabs == [
        "Overview",
        "Playbook & Drafting",
        "Contact Path",
        "Qualification",
        "Lifecycle & Safety",
        "CRM Conversion",
    ]

    field_order = prospect["field_order"]
    assert field_order.index("playbook_drafting_tab") < field_order.index("sei_playbook")
    assert field_order.index("crm_conversion_tab") < field_order.index("ready_for_crm_conversion")


def test_large_operator_forms_use_tabs():
    import_batch = _doctype("sei_import_batch")
    import_tabs = [
        field["label"]
        for field in import_batch["fields"]
        if field.get("fieldtype") == "Tab Break"
    ]
    assert import_tabs == ["Import Setup", "Run Results", "Import Rows"]

    attribution = _doctype("sei_interaction_attribution")
    attribution_tabs = [
        field["label"]
        for field in attribution["fields"]
        if field.get("fieldtype") == "Tab Break"
    ]
    assert attribution_tabs == [
        "Attribution Sources",
        "CRM Links",
        "Interaction Outcome",
    ]
