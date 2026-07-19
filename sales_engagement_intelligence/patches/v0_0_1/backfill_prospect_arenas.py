from sales_engagement_intelligence.sales_engagement_and_intelligence.services import (
    prospect_signal_type_sync,
    thesis_arena_sync,
)


def execute():
    prospect_signal_type_sync.sync_all_prospect_signal_types()

    import frappe

    for thesis_name in frappe.get_all("SEI Thesis", pluck="name"):
        thesis_arena_sync.sync_from_thesis(frappe.get_doc("SEI Thesis", thesis_name))
