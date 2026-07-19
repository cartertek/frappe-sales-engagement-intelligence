from urllib.parse import urlparse

import frappe
from frappe.model.document import Document

from sales_engagement_intelligence.sales_engagement_and_intelligence.services.contacts import (
    ensure_required_contact_roles,
)


class SEIProspect(Document):
    def validate(self):
        ensure_required_contact_roles(self)
        self.set_normalized_domain()
        self.apply_do_not_contact_rules()
        self.validate_manual_override_reason()
        self.apply_milestone_3_workflow_updates()

    def set_normalized_domain(self):
        if not self.website:
            return

        value = self.website.strip()
        parsed = urlparse(value if "://" in value else f"https://{value}")
        hostname = (parsed.hostname or "").lower().strip(".")

        if hostname.startswith("www."):
            hostname = hostname[4:]

        self.normalized_domain = hostname

    def apply_do_not_contact_rules(self):
        if self.do_not_contact:
            self.qualification_status = "Do Not Contact"
            self.lifecycle_status = "Do Not Contact"

        if self.qualification_status == "Do Not Contact":
            self.do_not_contact = 1
            self.lifecycle_status = "Do Not Contact"

    def validate_manual_override_reason(self):
        if self.manual_qualification_override and not self.manual_qualification_reason:
            frappe.throw(
                "Manual Qualification Reason is required when Manual Qualification Override is checked."
            )

    def apply_milestone_3_workflow_updates(self):
        if getattr(frappe.flags, "sei_m3_recalculating", False):
            return
        if not self.name:
            return

        from sales_engagement_intelligence.sales_engagement_and_intelligence.services.lifecycle import (
            apply_lifecycle_to_doc,
            is_terminal_status,
        )
        from sales_engagement_intelligence.sales_engagement_and_intelligence.services.qualification import (
            apply_qualification_to_doc,
        )

        try:
            frappe.flags.sei_m3_recalculating = True
            apply_qualification_to_doc(self)
            if not is_terminal_status(self.lifecycle_status):
                apply_lifecycle_to_doc(self)
        finally:
            frappe.flags.sei_m3_recalculating = False

    def on_trash(self):
        from sales_engagement_intelligence.sales_engagement_and_intelligence.services import (
            delete_unlinking,
        )

        delete_unlinking.unlink_references_before_delete(self)
