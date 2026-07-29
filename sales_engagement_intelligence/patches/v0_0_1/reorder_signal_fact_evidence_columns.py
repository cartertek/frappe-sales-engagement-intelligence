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
    # Move them out of the active range first so idx swaps cannot conflict.
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
