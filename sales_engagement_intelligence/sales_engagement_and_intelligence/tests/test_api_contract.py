import inspect

import frappe

API_PATH = "sales_engagement_intelligence.sales_engagement_and_intelligence.api"

REQUIRED_ENDPOINTS = [
    "create_prospect",
    "update_prospect",
    "get_prospect",
    "get_prospect_summary",
    "find_prospects",
    "add_signal",
    "update_signal",
    "get_signals",
    "find_duplicate_signal",
    "recalculate_qualification",
    "apply_lifecycle",
    "mark_ready_for_crm_conversion",
    "mark_not_ready_for_crm_conversion",
    "mark_rejected",
    "mark_do_not_contact",
    "reopen_prospect",
    "apply_playbook_defaults",
    "preview_message_draft",
    "preview_crm_conversion",
    "find_crm_duplicates",
    "create_crm_lead",
    "create_or_link_crm_organization",
    "create_or_link_contact",
    "create_crm_deal",
    "link_existing_crm_record",
    "sync_sei_context_to_crm",
    "create_import_batch",
    "dry_run_import",
    "run_import",
    "reset_import_batch_to_draft",
    "get_import_batch_status",
    "get_import_batch_rows",
    "find_duplicate_sei_prospects",
    "find_duplicate_sei_signals",
    "backfill_normalized_domains",
    "recalculate_selected_prospects",
    "apply_lifecycle_to_selected_prospects",
    "get_needs_research_queue",
    "get_ready_for_crm_conversion_queue",
    "get_find_contact_queue",
    "get_protected_status_queue",
    "get_recent_import_batches",
    "create_interaction_attribution",
    "get_interaction_attributions",
]


def test_milestone_7_endpoints_are_exposed_and_whitelisted():
    for name in REQUIRED_ENDPOINTS:
        method = frappe.get_attr(f"{API_PATH}.{name}")
        assert callable(method), name
        assert method in frappe.whitelisted, name


def test_response_helpers_match_contract():
    api = frappe.get_module(API_PATH)
    assert api.success({"x": 1}) == {"ok": True, "data": {"x": 1}, "warnings": [], "messages": []}
    assert api.failure("VALIDATION_ERROR", "Bad")["error"] == {
        "code": "VALIDATION_ERROR",
        "message": "Bad",
        "details": {},
    }


def test_queue_endpoints_do_not_import_report_modules():
    api = frappe.get_module(API_PATH)
    for name in [
        "get_needs_research_queue",
        "get_ready_for_crm_conversion_queue",
        "get_find_contact_queue",
        "get_protected_status_queue",
        "get_recent_import_batches",
    ]:
        source = inspect.getsource(getattr(api, name))
        assert ".report" not in source
        assert "reporting" not in source
