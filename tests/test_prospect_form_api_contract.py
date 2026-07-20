import ast
import re
from pathlib import Path

ROOT = Path("sales_engagement_intelligence/sales_engagement_and_intelligence")
SCRIPT = (ROOT / "doctype/sei_prospect/sei_prospect.js").read_text()
API = (ROOT / "api.py").read_text()


def api_functions():
    tree = ast.parse(API)
    return {
        node.name
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }


def test_every_prospect_call_and_reload_action_has_api_method():
    actions = set(re.findall(r"call_and_reload\(frm, ['\"]([a-zA-Z0-9_]+)['\"]", SCRIPT))
    missing = sorted(actions - api_functions())
    assert not missing, f"Prospect form references missing API methods: {missing}"


def test_retired_mark_ready_action_is_not_rendered():
    assert "mark_ready_for_crm_conversion" in SCRIPT
    assert "mark_not_ready_for_crm_conversion" in SCRIPT
    assert "Mark as Ready for CRM Conversion" in SCRIPT
    assert "Mark as Not Ready for CRM" in SCRIPT


def test_current_crm_preparation_actions_have_api_methods():
    expected = {
        "preview_crm_conversion",
        "create_crm_lead",
        "create_or_link_crm_organization",
        "create_or_link_crm_contact",
        "create_crm_deal",
        "link_existing_crm_record",
        "sync_sei_context_to_crm",
    }
    missing = sorted(expected - api_functions())
    assert not missing, f"Missing CRM Preparation API methods: {missing}"


def test_crm_handoff_statuses_and_queues_remain_available():
    import json

    prospect = json.loads(
        Path(
            "sales_engagement_intelligence/sales_engagement_and_intelligence/doctype/"
            "sei_prospect/sei_prospect.json"
        ).read_text()
    )
    lifecycle = next(field for field in prospect["fields"] if field["fieldname"] == "lifecycle_status")
    options = lifecycle["options"].splitlines()
    assert "Find Contact" in options
    assert "Ready for CRM Conversion" in options

    api = API
    assert "def get_find_contact_queue" in api
    assert "def get_ready_for_crm_conversion_queue" in api
