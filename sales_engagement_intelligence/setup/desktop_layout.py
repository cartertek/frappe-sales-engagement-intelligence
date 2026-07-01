"""Desktop layout maintenance for Sales Engagement and Intelligence."""

import frappe

LEGACY_ASSET_RENAMES = {
    "sei_app.svg": "app.svg",
    "sei_prospecting.svg": "prospecting.svg",
    "sei_signals.svg": "signals.svg",
    "sei_touchpoints.svg": "touchpoints.svg",
    "sei_assets.svg": "assets.svg",
    "sei_crm_conversion.svg": "crm_conversion.svg",
    "sei_reports.svg": "reports.svg",
    "sei_settings.svg": "settings.svg",
}


def after_migrate() -> None:
    """Update saved desktop layouts after SEI desktop asset renames."""

    updated_users = []
    for name in frappe.get_all("Desktop Layout", pluck="name"):
        layout = frappe.db.get_value("Desktop Layout", name, "layout") or ""
        updated_layout = layout
        for old, new in LEGACY_ASSET_RENAMES.items():
            updated_layout = updated_layout.replace(old, new)

        if updated_layout != layout:
            frappe.db.set_value("Desktop Layout", name, "layout", updated_layout)
            updated_users.append(name)

    if updated_users:
        frappe.db.commit()
        for user in updated_users:
            frappe.clear_cache(user=user)
        frappe.clear_cache()
