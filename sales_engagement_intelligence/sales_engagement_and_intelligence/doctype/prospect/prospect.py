from urllib.parse import urlparse

import frappe
from frappe.model.document import Document


class Prospect(Document):
    def validate(self):
        self.set_normalized_domain()
        self.apply_do_not_contact_rules()
        self.validate_manual_override_reason()

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
            self.lifecycle_status = 'Do Not Contact'

        if self.qualification_status == 'Do Not Contact':
            self.do_not_contact = 1
            self.lifecycle_status = 'Do Not Contact'

    def validate_manual_override_reason(self):
        if self.manual_qualification_override and not self.manual_qualification_reason:
            frappe.throw(
                'Manual Qualification Reason is required when Manual Qualification Override is checked.'
            )
