import frappe


def execute() -> None:
    if not frappe.db.table_exists("SEI Signal") or not frappe.db.has_column("SEI Signal", "signal_name"):
        return

    frappe.db.sql(
        """
        UPDATE `tabSEI Signal`
        SET `signal_name` = `signal_type`
        WHERE (`signal_name` IS NULL OR TRIM(`signal_name`) = '')
          AND `signal_type` IS NOT NULL
          AND TRIM(`signal_type`) != ''
        """
    )
