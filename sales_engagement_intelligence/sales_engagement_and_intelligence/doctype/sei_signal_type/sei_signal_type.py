from __future__ import annotations

import frappe
from frappe.model.document import Document


class SEISignalType(Document):
    def validate(self):
        self.validate_playbook_arena_pair()

    def on_update(self) -> None:
        from sales_engagement_intelligence.sales_engagement_and_intelligence.services import (
            prospect_signal_type_sync,
        )

        prospects = frappe.get_all("SEI Signal", filters={"signal_type": self.name}, pluck="prospect")
        from sales_engagement_intelligence.sales_engagement_and_intelligence.services import qualification
        from sales_engagement_intelligence.sales_engagement_and_intelligence.services.lifecycle import (
            apply_lifecycle_status,
            is_terminal_status,
        )

        for prospect in dict.fromkeys(prospects):
            prospect_signal_type_sync.sync_prospect_signal_types(prospect)
            if not prospect:
                continue
            qualification.apply_qualification_result(prospect)
            status = frappe.db.get_value("SEI Prospect", prospect, "lifecycle_status")
            if not is_terminal_status(status):
                apply_lifecycle_status(prospect)

    def validate_playbook_arena_pair(self) -> None:
        if not self.playbook or not self.research_arena:
            return
        allowed = frappe.db.exists(
            "SEI Playbook Research Arena",
            {
                "parent": self.playbook,
                "parenttype": "SEI Playbook",
                "parentfield": "research_arenas",
                "research_arena": self.research_arena,
            },
        )
        if not allowed:
            frappe.throw(f"Research Arena {self.research_arena} is not assigned to Playbook {self.playbook}.")
