import frappe
from frappe.model.document import Document


class Signal(Document):
    def validate(self):
        if self.counts_toward_qualification and self.evidence_basis == 'Inferred':
            frappe.msgprint(
                'This inferred signal is marked as counting toward qualification. '
                'Milestone 3 should decide whether inferred signals can qualify a prospect.',
                alert=True,
            )
