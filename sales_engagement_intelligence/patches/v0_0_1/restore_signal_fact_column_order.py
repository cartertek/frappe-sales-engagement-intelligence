import frappe

ORDER = (
    "fact",
    "source_url",
    "source_date",
    "evidence_basis",
    "evidence_specificity",
)


def execute():
    parent = "SEI Signal Observed Fact"
    if not frappe.db.exists("DocType", parent):
        return
    for offset, fieldname in enumerate(ORDER, start=101):
        frappe.db.set_value(
            "DocField",
            {"parent": parent, "fieldname": fieldname},
            "idx",
            offset,
            update_modified=False,
        )
    for idx, fieldname in enumerate(ORDER, start=1):
        frappe.db.set_value(
            "DocField",
            {"parent": parent, "fieldname": fieldname},
            "idx",
            idx,
            update_modified=False,
        )
    frappe.clear_cache(doctype=parent)
