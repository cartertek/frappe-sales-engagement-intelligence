from urllib.parse import urlparse

import frappe
from frappe.model.document import Document


class SEIProspect(Document):
    def validate(self):
        self.set_normalized_domain()
        self.apply_do_not_contact_rules()
        self.validate_manual_override_reason()

    def on_update(self):
        self.apply_milestone_3_workflow_updates()

    def set_normalized_domain(self):
        if not self.website:
            return

        value = self.website.strip()
        parsed = urlparse(value if '://' in value else f'https://{value}')
        hostname = (parsed.hostname or '').lower().strip('.')

        if hostname.startswith('www.'):
            hostname = hostname[4:]

        self.normalized_domain = hostname

    def apply_do_not_contact_rules(self):
        if self.do_not_contact:
            self.qualification_status = 'Do Not Contact'
            self.lifecycle_status = 'Do Not Contact'
            self.ready_for_crm_conversion = 0

        if self.qualification_status == 'Do Not Contact':
            self.do_not_contact = 1
            self.lifecycle_status = 'Do Not Contact'
            self.ready_for_crm_conversion = 0

    def validate_manual_override_reason(self):
        if self.manual_qualification_override and not self.manual_qualification_reason:
            frappe.throw(
                'Manual Qualification Reason is required when Manual Qualification Override is checked.'
            )

    def apply_milestone_3_workflow_updates(self):
        if getattr(frappe.flags, 'sei_m3_recalculating', False):
            return
        if not self.name:
            return

        from sales_engagement_intelligence.sales_engagement_and_intelligence.services.lifecycle import (
            apply_lifecycle_status,
            is_terminal_status,
        )
        from sales_engagement_intelligence.sales_engagement_and_intelligence.services.qualification import (
            apply_qualification_result,
        )

        try:
            frappe.flags.sei_m3_recalculating = True
            apply_qualification_result(self.name)
            fresh_status = frappe.db.get_value('SEI Prospect', self.name, 'lifecycle_status')
            if not is_terminal_status(fresh_status):
                apply_lifecycle_status(self.name)
        finally:
            frappe.flags.sei_m3_recalculating = False
