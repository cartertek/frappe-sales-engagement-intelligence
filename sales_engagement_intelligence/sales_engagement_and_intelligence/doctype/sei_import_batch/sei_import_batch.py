from __future__ import annotations

import frappe
from frappe.model.document import Document


class SEIImportBatch(Document):
    def before_insert(self):
        if not self.imported_by:
            self.imported_by = frappe.session.user

    def validate(self):
        if self.status == "Cancelled" and self.has_value_changed("status"):
            if self.get_doc_before_save() and self.get_doc_before_save().status not in ("Draft", "Failed"):
                frappe.throw("Only Draft or Failed import batches can be cancelled.")

