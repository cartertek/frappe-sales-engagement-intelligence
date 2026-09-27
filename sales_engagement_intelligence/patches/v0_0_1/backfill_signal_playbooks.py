import frappe


def execute():
    if not (
        frappe.db.table_exists("SEI Signal")
        and frappe.db.table_exists("SEI Signal Type")
        and frappe.db.has_column("SEI Signal", "playbook")
    ):
        return

    frappe.db.sql(
        """
        UPDATE `tabSEI Signal` signal
        LEFT JOIN `tabSEI Signal Type` signal_type ON signal_type.name = signal.signal_type
        SET signal.playbook = signal_type.playbook
        """
    )
