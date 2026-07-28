import frappe

FIELDS = ("evidence_basis", "evidence_specificity", "source_url", "source_date")

def execute():
    if not frappe.db.table_exists("SEI Signal Observed Fact"):
        return
    available = [field for field in FIELDS if frappe.db.has_column("SEI Signal", field)]
    if not available:
        return
    signals = frappe.get_all("SEI Signal", fields=["name", *available])
    for signal in signals:
        facts = frappe.get_all(
            "SEI Signal Observed Fact",
            filters={"parent": signal.name, "parenttype": "SEI Signal"},
            pluck="name",
        )
        for fact in facts:
            values = {field: signal.get(field) for field in available if signal.get(field) is not None}
            if values:
                frappe.db.set_value("SEI Signal Observed Fact", fact, values, update_modified=False)
