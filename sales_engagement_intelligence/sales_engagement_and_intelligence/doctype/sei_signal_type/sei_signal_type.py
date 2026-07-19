from __future__ import annotations

import frappe
from frappe.model.document import Document


class SEISignalType(Document):
    def validate(self):
        self.validate_thesis_arena_pair()

    def validate_thesis_arena_pair(self) -> None:
        if not self.thesis or not self.research_arena:
            return
        allowed = frappe.db.exists(
            "SEI Thesis Research Arena",
            {
                "parent": self.thesis,
                "parenttype": "SEI Thesis",
                "parentfield": "research_arenas",
                "research_arena": self.research_arena,
            },
        )
        if not allowed:
            frappe.throw(
                f"Thesis {self.thesis} is not assigned to Research Arena {self.research_arena}."
            )

    def on_update(self):
        from sales_engagement_intelligence.sales_engagement_and_intelligence.services import (
            prospect_signal_type_sync,
        )

        prospects = frappe.get_all(
            "SEI Signal", filters={"signal_type": self.name}, pluck="prospect"
        )
        for prospect in dict.fromkeys(prospects):
            prospect_signal_type_sync.sync_prospect_signal_types(prospect)
