import frappe


def execute():
    if not (
        frappe.db.table_exists("SEI Signal")
        and frappe.db.has_column("SEI Signal", "observed_fact")
        and frappe.db.table_exists("SEI Signal Observed Fact")
    ):
        return

    rows = frappe.db.sql(
        """
        SELECT name, observed_fact
        FROM `tabSEI Signal`
        WHERE COALESCE(TRIM(observed_fact), '') != ''
        """,
        as_dict=True,
    )
    for row in rows:
        exists = frappe.db.exists(
            "SEI Signal Observed Fact",
            {
                "parent": row.name,
                "parenttype": "SEI Signal",
                "parentfield": "observed_facts",
            },
        )
        if exists:
            continue
        frappe.get_doc(
            {
                "doctype": "SEI Signal Observed Fact",
                "parent": row.name,
                "parenttype": "SEI Signal",
                "parentfield": "observed_facts",
                "idx": 1,
                "fact": row.observed_fact.strip(),
            }
        ).db_insert()
