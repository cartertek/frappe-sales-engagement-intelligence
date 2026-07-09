import frappe


def test_reset_import_batch_to_draft_api_is_exposed():
    method = frappe.get_attr(
        "sales_engagement_intelligence.sales_engagement_and_intelligence.api.reset_import_batch_to_draft"
    )
    assert callable(method)
