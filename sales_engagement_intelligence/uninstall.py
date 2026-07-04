import frappe


def before_uninstall() -> None:
    """Clear cached Desk state before SEI is removed."""

    frappe.clear_cache()
