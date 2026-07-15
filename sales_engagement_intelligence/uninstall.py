import frappe


def before_uninstall() -> None:
    """Clear cached Desk state before SEI is removed."""

    from sales_engagement_intelligence.sales_engagement_and_intelligence.services.prospect_tag_sync import (
        drop_signal_prospect_tag_trigger,
    )

    drop_signal_prospect_tag_trigger()
    frappe.clear_cache()
