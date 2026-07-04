import frappe


def check_app_permission() -> bool:
    """Return whether the current user should see the SEI app entry."""

    allowed_roles = {
        "System Manager",
        "Sales Engagement Manager",
        "Sales Engagement User",
    }
    return bool(allowed_roles.intersection(frappe.get_roles()))
