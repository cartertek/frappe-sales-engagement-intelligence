from __future__ import annotations

import frappe
from frappe.model.document import Document


class SEISignalType(Document):
    def validate(self):
        self.validate_playbook_arena_pair()

    def on_update(self) -> None:
        self.sync_playbook_child_row()
        from sales_engagement_intelligence.sales_engagement_and_intelligence.services import (
            prospect_signal_type_sync,
        )

        prospects = frappe.get_all("SEI Signal", filters={"signal_type": self.name}, pluck="prospect")
        for prospect in dict.fromkeys(prospects):
            prospect_signal_type_sync.sync_prospect_signal_types(prospect)

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

    def sync_playbook_child_row(self) -> None:
        if getattr(frappe.flags, "sei_syncing_playbook_signal_types", False) or not self.playbook:
            return

        try:
            frappe.flags.sei_syncing_playbook_signal_types = True
            frappe.db.delete(
                "SEI Playbook Signal Type",
                {"signal_type": self.name, "parent": ["!=", self.playbook]},
            )
            if not frappe.db.exists(
                "SEI Playbook Signal Type",
                {
                    "parent": self.playbook,
                    "parenttype": "SEI Playbook",
                    "parentfield": "signal_types",
                    "signal_type": self.name,
                },
            ):
                frappe.get_doc(
                    {
                        "doctype": "SEI Playbook Signal Type",
                        "parent": self.playbook,
                        "parenttype": "SEI Playbook",
                        "parentfield": "signal_types",
                        "signal_type": self.name,
                    }
                ).insert(ignore_permissions=True)
        finally:
            frappe.flags.sei_syncing_playbook_signal_types = False
