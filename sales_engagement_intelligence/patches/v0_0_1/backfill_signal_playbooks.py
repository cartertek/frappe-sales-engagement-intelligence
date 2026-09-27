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
        UPDATE `tabSEI Signal` AS s
        LEFT JOIN `tabSEI Signal Type` AS st ON st.name = s.signal_type
        SET s.playbook = st.playbook
        """
    )
