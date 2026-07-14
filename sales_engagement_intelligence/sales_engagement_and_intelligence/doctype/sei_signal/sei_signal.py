import frappe
from sales_engagement_intelligence.sales_engagement_and_intelligence.services.taxonomy import resolve_signal_type
from frappe.model.document import Document


class SEISignal(Document):
    def validate(self):
        if self.signal_type:
            self.signal_type = resolve_signal_type(self.signal_type)
        self.set_prospect_name()
        if not self.exclude_from_qualification and self.evidence_basis == 'Inferred':
            frappe.msgprint(
                'Inferred signals do not count toward automatic qualification. '
                'Only observed Moderate or Strong signals are counted by the qualification engine.',
                alert=True,
            )

    def set_prospect_name(self):
        if not self.prospect:
            self.prospect_name = None
            return

        self.prospect_name = frappe.db.get_value(
            'SEI Prospect',
            self.prospect,
            'prospect_name',
        )

    def after_insert(self):
        self.recalculate_prospect()

    def on_update(self):
        self.recalculate_prospect()

    def on_trash(self):
        self.recalculate_prospect()

    def after_delete(self):
        self.recalculate_prospect()

    def recalculate_prospect(self):
        if not self.prospect or getattr(frappe.flags, 'sei_m3_recalculating', False):
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
            apply_qualification_result(self.prospect)
            status = frappe.db.get_value('SEI Prospect', self.prospect, 'lifecycle_status')
            if not is_terminal_status(status):
                apply_lifecycle_status(self.prospect)
        finally:
            frappe.flags.sei_m3_recalculating = False
