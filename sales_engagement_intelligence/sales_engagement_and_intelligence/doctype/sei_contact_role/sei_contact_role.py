import frappe
from frappe.model.document import Document


class SEIContactRole(Document):
    def validate(self):
        if "/" in (self.role_name or ""):
            frappe.throw("Contact roles must represent one role and cannot contain a slash.")
