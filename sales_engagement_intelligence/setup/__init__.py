import frappe


def after_migrate() -> None:
    """Refresh Desk state after app metadata and standard records sync."""

    frappe.clear_cache()


def after_app_install(app_name: str) -> None:
    """Refresh Desk state when dependent apps are installed after SEI."""

    if app_name not in {"crm", "erpnext"}:
        return
    frappe.clear_cache()


def before_app_uninstall(app_name: str) -> None:
    """Refresh Desk state when dependent apps are removed."""

    if app_name not in {"crm", "erpnext"}:
        return
    frappe.clear_cache()
