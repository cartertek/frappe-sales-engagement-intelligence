from frappe.model.document import Document

from sales_engagement_intelligence.sales_engagement_and_intelligence.services import (
    message_draft_validation,
)


class SEIProspectMessageDraft(Document):
    def validate(self):
        self.cc = message_draft_validation.normalize_email_list(self.cc, label="CC")
