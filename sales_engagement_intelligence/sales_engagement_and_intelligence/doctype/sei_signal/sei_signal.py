from __future__ import annotations

import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime

from sales_engagement_intelligence.sales_engagement_and_intelligence.services.taxonomy import (
    resolve_signal_type,
)

QUALIFYING_STRENGTHS = {"Moderate", "Strong"}
PUBLISHED = "Published"

PUBLISH_REQUIRED_FIELDS = (
    ("signal_name", "Name"),
    ("prospect", "Prospect"),
    ("signal_type", "Signal Type"),
    ("signal_strength", "Signal Strength"),
)


def _has_value(value) -> bool:
    return bool(str(value or "").strip())


def _observed_fact_values(signal) -> list[str]:
    return [
        str(row.fact).strip()
        for row in (signal.get("observed_facts") or [])
        if _has_value(row.fact)
    ]


class SEISignal(Document):
    @property
    def observed_fact(self):
        """Backward-compatible view of the first managed Observed Fact row."""
        facts = _observed_fact_values(self)
        return facts[0] if facts else None

    @observed_fact.setter
    def observed_fact(self, value):
        """Map legacy single-fact writes into the managed Observed Facts table."""
        if not _has_value(value):
            self.set("observed_facts", [])
            return
        rows = self.get("observed_facts") or []
        if rows:
            rows[0].fact = str(value).strip()
            return
        self.append("observed_facts", {"fact": str(value).strip()})

    def validate(self):
        self.status = self.status or "Draft"
        if self.signal_type:
            self.signal_type = resolve_signal_type(self.signal_type)
        self.set_prospect_name()
        self.set_prospect_tags()
        if self.status == PUBLISHED:
            self.validate_publishable()
            self.validate_signal_type_and_arena()
            self.apply_evidence_guardrails()

    def validate_publishable(self) -> None:
        missing = [
            label
            for fieldname, label in PUBLISH_REQUIRED_FIELDS
            if not _has_value(self.get(fieldname))
        ]
        if not self.get("observed_facts"):
            missing.append("Observed Facts")
        if missing:
            frappe.throw(
                "Cannot publish Signal. Required fields are missing: " + ", ".join(missing)
            )

        incomplete_facts = []
        for index, row in enumerate(self.get("observed_facts") or [], start=1):
            row_missing = [
                label
                for fieldname, label in (
                    ("fact", "Fact"),
                    ("evidence_basis", "Evidence Basis"),
                    ("evidence_specificity", "Evidence Specificity"),
                )
                if not _has_value(row.get(fieldname))
            ]
            if row_missing:
                incomplete_facts.append(f"row {index}: {', '.join(row_missing)}")
        if incomplete_facts:
            frappe.throw(
                "Cannot publish Signal. Observed Facts are incomplete: "
                + "; ".join(incomplete_facts)
            )

    def validate_signal_type_and_arena(self) -> None:
        if not self.signal_type:
            return

        signal_type = frappe.db.get_value(
            "SEI Signal Type",
            self.signal_type,
            ["playbook", "research_arena", "active"],
            as_dict=True,
        )
        if not signal_type:
            frappe.throw(f"SEI Signal Type not found: {self.signal_type}")

        if (self.is_new() or self.has_value_changed("status")) and not signal_type.active:
            frappe.throw("Signals cannot be published with an inactive Signal Type.")

        if not signal_type.playbook or not signal_type.research_arena:
            frappe.throw("Signal Type must belong to exactly one Playbook and one Research Arena.")

        arena_active = frappe.db.get_value(
            "SEI Research Arena", signal_type.research_arena, "active"
        )
        if (self.is_new() or self.has_value_changed("status")) and not arena_active:
            frappe.throw(
                "Signals cannot be published with a Signal Type whose Research Arena is inactive."
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

    def apply_evidence_guardrails(self) -> None:
        fact_rows = self.get("observed_facts") or []
        observed_facts = _observed_fact_values(self)
        observed_rows = [row for row in fact_rows if row.evidence_basis == "Observed"]
        inferred_rows = [row for row in fact_rows if row.evidence_basis == "Inferred"]

        if self.signal_strength in QUALIFYING_STRENGTHS:
            missing = [
                label
                for fieldname, label in (
                    ("signal_claim", "Signal Claim"),
                    ("why_this_signal_type", "Why This Signal Type"),
                    ("why_not_weak", "Why Not Weak"),
                    ("disqualifiers_checked", "Disqualifiers Checked"),
                )
                if not _has_value(self.get(fieldname))
            ]
            if not observed_facts:
                missing.insert(0, "Observed Facts")
            if missing:
                frappe.throw(
                    "Moderate or Strong signals require structured evidence fields: "
                    + ", ".join(missing)
                )

        if self.signal_strength == "Weak" and not (
            observed_facts or _has_value(self.evidence_gap_reason)
        ):
            frappe.throw("Weak signals require either Observed Facts or Evidence Gap Reason.")

        if (
            self.signal_strength == "Strong"
            and inferred_rows
            and not observed_rows
            and not self.has_manual_override()
        ):
            frappe.throw(
                "Signals supported only by inferred facts cannot be Strong without "
                "a Manual Override Reason."
            )
        if inferred_rows and not observed_rows and not self.exclude_from_qualification:
            self.exclude_from_qualification = 1
            frappe.msgprint(
                "Signals supported only by inferred facts are automatically excluded "
                "from qualification unless manually reviewed.",
                alert=True,
            )

        if self.has_manual_override():
            self.mark_manual_override_audit_fields()

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
        if (
            self.status != PUBLISHED
            or not self.prospect
            or getattr(frappe.flags, "sei_m3_recalculating", False)
        ):
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
