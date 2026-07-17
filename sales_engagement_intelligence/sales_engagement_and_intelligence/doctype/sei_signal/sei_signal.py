from __future__ import annotations

import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime

from sales_engagement_intelligence.sales_engagement_and_intelligence.services.taxonomy import (
    resolve_signal_type,
)

QUALIFYING_STRENGTHS = {"Moderate", "Strong"}


def _has_value(value) -> bool:
    return bool(str(value or "").strip())


class SEISignal(Document):
    def validate(self):
        if self.signal_type:
            self.signal_type = resolve_signal_type(self.signal_type)
        self.validate_signal_type_and_arena()
        self.set_prospect_name()
        self.set_prospect_tags()
        self.sync_disqualifier_check_rows()
        self.apply_evidence_guardrails()

    def validate_signal_type_and_arena(self) -> None:
        if not self.signal_type:
            return

        signal_type = frappe.db.get_value(
            "SEI Signal Type", self.signal_type, ["thesis", "research_arena", "active"], as_dict=True
        )
        if not signal_type:
            frappe.throw(f"SEI Signal Type not found: {self.signal_type}")

        if self.is_new() and not signal_type.active:
            frappe.throw("New signals cannot be created with an inactive Signal Type.")

        if not signal_type.thesis or not signal_type.research_arena:
            frappe.throw("Signal Type must belong to exactly one Thesis and one Research Arena.")

        arena_active = frappe.db.get_value(
            "SEI Research Arena", signal_type.research_arena, "active"
        )
        if self.is_new() and not arena_active:
            frappe.throw("New signals cannot use a Signal Type whose Research Arena is inactive.")

    def set_prospect_name(self):
        if not self.prospect:
            self.prospect_name = None
            return

        self.prospect_name = frappe.db.get_value(
            'SEI Prospect',
            self.prospect,
            'prospect_name',
        )

    def sync_disqualifier_check_rows(self) -> None:
        for row in self.get("disqualifier_checks") or []:
            row.signal = self.name
            row.signal_type = self.signal_type

    def apply_evidence_guardrails(self) -> None:
        self.is_strength_capped = 1 if self.has_applied_disqualifier() else 0

        if self.evidence_basis == "Observed" and not _has_value(self.observed_fact):
            frappe.throw("Observed Fact is required when Evidence Basis is Observed.")

        if self.signal_strength in QUALIFYING_STRENGTHS:
            missing = [
                label
                for fieldname, label in (
                    ("observed_fact", "Observed Fact"),
                    ("signal_claim", "Signal Claim"),
                    ("why_this_signal_type", "Why This Signal Type"),
                    ("why_not_weak", "Why Not Weak"),
                    ("disqualifiers_checked", "Disqualifiers Checked"),
                )
                if not _has_value(self.get(fieldname))
            ]
            if missing:
                frappe.throw(
                    "Moderate or Strong signals require structured evidence fields: "
                    + ", ".join(missing)
                )

        if self.signal_strength == "Weak" and not (
            _has_value(self.observed_fact) or _has_value(self.evidence_gap_reason)
        ):
            frappe.throw("Weak signals require either Observed Fact or Evidence Gap Reason.")

        if self.evidence_basis == "Inferred":
            if self.signal_strength == "Strong" and not self.has_manual_override():
                frappe.throw("Inferred signals cannot be Strong without a Manual Override Reason.")
            if not self.exclude_from_qualification:
                self.exclude_from_qualification = 1
                frappe.msgprint(
                    "Inferred signals are automatically excluded from qualification unless "
                    "manually reviewed.",
                    alert=True,
                )

        if self.is_strength_capped and self.signal_strength in QUALIFYING_STRENGTHS:
            if not self.has_manual_override():
                frappe.throw(
                    "One or more disqualifier checks apply, so this signal is capped at Weak unless "
                    "Manual Override Reason is documented."
                )
            self.mark_manual_override_audit_fields()

        if self.has_manual_override():
            self.mark_manual_override_audit_fields()

    def has_applied_disqualifier(self) -> bool:
        return any(row.applies for row in self.get("disqualifier_checks") or [])

    def has_manual_override(self) -> bool:
        return _has_value(self.manual_override_reason)

    def mark_manual_override_audit_fields(self) -> None:
        if not self.manual_override_by:
            self.manual_override_by = frappe.session.user
        if not self.manual_override_date:
            self.manual_override_date = now_datetime()

    def set_prospect_tags(self):
        if not self.prospect:
            self.prospect_tags = None
            return

        self.prospect_tags = frappe.db.get_value(
            'SEI Prospect',
            self.prospect,
            '_user_tags',
            ignore=True,
        ) or ''

    def after_insert(self):
        self.sync_prospect_signal_types()
        self.recalculate_prospect()

    def on_update(self):
        self.sync_prospect_signal_types(include_previous=True)
        self.recalculate_prospect()

    def on_trash(self):
        from sales_engagement_intelligence.sales_engagement_and_intelligence.services import (
            delete_unlinking,
        )

        delete_unlinking.unlink_references_before_delete(self)
        self.recalculate_prospect()

    def after_delete(self):
        self.sync_prospect_signal_types()
        self.recalculate_prospect()

    def sync_prospect_signal_types(self, *, include_previous: bool = False) -> None:
        from sales_engagement_intelligence.sales_engagement_and_intelligence.services import (
            prospect_signal_type_sync,
        )

        prospects = {self.prospect}
        if include_previous:
            previous = self.get_doc_before_save()
            prospects.add(previous.prospect if previous else None)

        for prospect in prospects:
            prospect_signal_type_sync.sync_prospect_signal_types(prospect)

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
