from __future__ import annotations

import frappe
from frappe.model.document import Document

from sales_engagement_intelligence.sales_engagement_and_intelligence.services import (
    message_draft_validation,
)


class SEIMessageDraft(Document):
    def validate(self):
        self.cc = message_draft_validation.normalize_email_list(self.cc, label="CC")
        if self.sent and not self.sent_on:
            frappe.throw("Use Mark as Sent after the prospect has been converted to CRM.")
