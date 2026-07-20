from __future__ import annotations

import frappe
from frappe.model.document import Document


class SEIMessageDraft(Document):
    def validate(self):
        if self.sent and not self.sent_on:
            frappe.throw("Use Mark as Sent after the prospect has been converted to CRM.")
